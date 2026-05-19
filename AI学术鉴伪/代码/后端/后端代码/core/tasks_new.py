"""Celery pipeline (GPU + CPU) for fake‑image‑detector
====================================================

此文件演示 **完整** 的 3‑阶段拆分方案：
    1. `fetch_batch`  与 AI/GPU 服务通信（独占 GPU）
    2. `process_single_result`  CPU & I/O 后处理（并行）
    3. `finalize_task`  统计收尾、生成报告

> ❗ 如需拆文件，可把辅助函数移到 utils.py / services.py，
>   为了示例完整性全部写在同一文件。
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import time
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from celery import shared_task, group, chord
from django.db import transaction
from django.utils import timezone

# ───────────────────────────────────────────────────────────────────────────────
#  Model & 服务导入
#   实际项目请根据 app 名称修改 import 路径即可。
# ───────────────────────────────────────────────────────────────────────────────
from core.models import (
    DetectionResult,      # 主结果表
    SubDetectionResult,   # 子检测方法结果表
    DetectionTask,        # 整体任务表
    LLMAnalysisRun,
    OrganizationModelConfig,
    TextDetectionResult,  # 文本检测结果表
    ReviewTextResource,   # 文本资源表
)
from core.services.bert_text_ai_bridge import (
    BertTextAIPermanentError,
    BertTextAITransientError,
    BertTextAIDetectionBridge,
)
from core.services.structured_ai_bridge import StructuredAITransientError
from core.services.structured_detection_service import StructuredDetectionService
from core.services.llm_service import build_chat_completion_payload, call_openai_compatible_chat
from core.utils.log_utils import log_action
from .utils.report_generator import generate_detection_task_report
from .utils.image_saver import save_ndarray_as_image
from .utils.fanyi import fanyi_text
from .call_figure_detection import get_result, reconnect
from core.call_figure_detection import (
    get_result,                       # GPU 远程调用
    reconnect,                        # 重连逻辑
)

from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_task_progress_update(task_id, status, progress, message=None, eta=None):
    """发送任务进度更新到 WebSocket 频道"""
    channel_layer = get_channel_layer()
    group_name = f'task_{task_id}'
    
    event_data = {
        'type': 'task_status_update',
        'message': {
            'task_id': task_id,
            'status': status,
            'progress': progress,
        }
    }
    if message:
        event_data['message']['detail'] = message
    if eta:
        event_data['message']['eta'] = eta

    async_to_sync(channel_layer.group_send)(
        group_name,
        event_data
    )

def send_task_completion_notification(user, task_id):
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}_notifications"  # 为每个用户创建唯一的组名

    # 获取当前时间并格式化为字符串
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 创建消息内容，分开任务ID和完成时间
    notification_data = {
        'task_id': task_id,
        'completion_time': current_time
    }

    # # wyt shit here
    # send_ai_detection_complete_notification(user.id, user.username,task_id)

    # 发送通知到 WebSocket 群组
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',  # 调用消费者中的 send_notification 方法
            'notification': notification_data  # 使用 JSON 格式传递字段
        }
    )


IMAGE_LLM_PROMPT = (
    '你是学术图像鉴伪专家，专精于检测学术论文中的图像伪造与篡改。'
    '你将收到每张待检测图片的原始图像、ELA误差分析图、以及各检测方法的mask热力图，'
    '同时附带结构化的检测数据（篡改判定、置信度、EXIF标记、子方法概率等）。'
    '\n\n'
    '请综合分析视觉证据与结构化数据，关注以下造假手段：\n'
    '1. 图像拼接/复制移动：mask图中出现规则形状高亮区域\n'
    '2. AI生成/Deepfake：ELA图呈均匀噪声分布，纹理不自然\n'
    '3. Photoshop篡改：EXIF中检测到Adobe痕迹，ELA异常集中在编辑区域\n'
    '4. 数据图表造假：图表中数据点异常对齐、误差棒缺失或不合理\n'
    '5. 重复使用：不同图片间存在相同区域或完全重复\n'
    '\n\n'
    '请输出严格符合以下JSON Schema的结果：\n'
    '{\n'
    '  "summary": "综合判定摘要，2-4句话概括整体情况和关键发现",\n'
    '  "risk_level": "high/medium/low",\n'
    '  "confidence": 0.0-1.0,\n'
    '  "manipulation_signals": ["具体的造假信号，每条50字以内"],\n'
    '  "mask_hints": ["对各mask图中可疑区域的解读"],\n'
    '  "recommendations": ["建议的人工复核方向或进一步检测措施"]\n'
    '}'
)


def _resolve_llm_config(task: DetectionTask):
    if not task.organization_id:
        return None

    return OrganizationModelConfig.objects.filter(
        organization_id=task.organization_id,
        enabled=True,
        provider_model__is_active=True,
        provider_model__source__status='active',
    ).select_related('provider_model', 'provider_model__source').order_by('-updated_at').first()


def _encode_image_data_url(path: str | None) -> str | None:
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, 'rb') as handle:
            raw = handle.read()
        mime, _ = mimetypes.guess_type(path)
        if not mime or mime == 'application/octet-stream':
            mime = 'image/png'
        return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"
    except OSError:
        return None


def _build_image_llm_summary(task: DetectionTask, failed_count: int) -> dict:
    results = []
    queryset = (
        DetectionResult.objects.filter(detection_task=task)
        .select_related('image_upload')
        .prefetch_related('sub_results')
        .order_by('image_upload_id')
    )

    for dr in queryset:
        sub_methods = []
        for sub in dr.sub_results.all():
            sub_methods.append({
                'method': sub.method,
                'probability': float(sub.probability) if sub.probability is not None else None,
            })

        results.append({
            'image_id': dr.image_upload_id,
            'is_fake': dr.is_fake,
            'confidence_score': dr.confidence_score,
            'exif_photoshop': dr.exif_photoshop,
            'exif_time_modified': dr.exif_time_modified,
            'llm_judgment': dr.llm_judgment,
            'sub_methods': sub_methods,
        })

    return {
        'task_id': task.id,
        'task_name': task.task_name,
        'detect_type': task.detect_type,
        'summary': {
            'image_count': len(results),
            'failed_count': failed_count,
            'fake_count': sum(1 for item in results if item.get('is_fake')),
        },
        'results': results,
    }


def _run_llm_analysis_for_image_task(task: DetectionTask, failed_count: int):
    config = _resolve_llm_config(task)
    if config is None:
        return None

    provider_model = config.provider_model
    source = provider_model.source
    summary = _build_image_llm_summary(task, failed_count)

    user_content = [
        {
            'type': 'text',
            'text': f"input_payload:\n{json.dumps(summary, ensure_ascii=False, indent=2)}",
        },
    ]

    queryset = (
        DetectionResult.objects.filter(detection_task=task)
        .select_related('image_upload')
        .prefetch_related('sub_results')
        .order_by('image_upload_id')
    )

    for dr in queryset:
        prefix = f'[image_id={dr.image_upload_id}]' if dr.image_upload_id else ''

        orig = _encode_image_data_url(dr.image_upload.image.path if dr.image_upload else None)
        if orig:
            user_content.append({'type': 'text', 'text': f'{prefix} 原始图像：'})
            user_content.append({'type': 'image_url', 'image_url': {'url': orig}})

        ela = _encode_image_data_url(dr.ela_image.path if dr.ela_image else None)
        if ela:
            user_content.append({'type': 'text', 'text': f'{prefix} ELA误差分析图：'})
            user_content.append({'type': 'image_url', 'image_url': {'url': ela}})

        for sub in dr.sub_results.all():
            prob = sub.probability
            if sub.mask_image and prob is not None and float(prob) > 0.1:
                mask = _encode_image_data_url(sub.mask_image.path)
                if mask:
                    user_content.append({
                        'type': 'text',
                        'text': f'{prefix} {sub.method} mask（概率 {float(prob):.4f}）：',
                    })
                    user_content.append({'type': 'image_url', 'image_url': {'url': mask}})

    messages = [
        {'role': 'system', 'content': IMAGE_LLM_PROMPT},
        {'role': 'user', 'content': user_content},
    ]

    payload = build_chat_completion_payload(
        model=provider_model.model_id,
        messages=messages,
        temperature=float(config.temperature),
        top_p=float(config.top_p),
        max_tokens=int(config.max_tokens),
    )

    run_record = LLMAnalysisRun.objects.create(
        task=task,
        model_config=config,
        stage='image',
        prompt=IMAGE_LLM_PROMPT,
        messages=messages,
        input_payload=summary,
        status='pending',
        created_by=task.user,
    )

    try:
        result = call_openai_compatible_chat(
            base_url=source.base_url,
            api_key=source.api_key,
            payload=payload,
            timeout=int(source.timeout or 30),
        )
    except (OSError, ValueError) as exc:
        run_record.status = 'failed'
        run_record.error_message = str(exc)
        run_record.save(update_fields=['status', 'error_message', 'updated_at'])
        return None

    content = None
    try:
        content = result['choices'][0]['message']['content']
    except (KeyError, IndexError, TypeError):
        content = None

    parsed = None
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = None

    run_record.status = 'success'
    run_record.output_text = content
    if isinstance(parsed, dict):
        run_record.output_json = parsed
    run_record.save(update_fields=['status', 'output_text', 'output_json', 'updated_at'])

    return parsed if isinstance(parsed, dict) else {'raw_text': content}

# 若使用 redis-lock 之类库，也可以导入 lock 来替代 queue=\'ai\' 的单并发做法
# from redis_lock import Lock

# ───────────────────────────────────────────────────────────────────────────────
# 1.  GPU 阶段 – 串行
# ───────────────────────────────────────────────────────────────────────────────

@shared_task(queue="ai", bind=True, acks_late=True, max_retries=3, default_retry_delay=15)
def fetch_batch(
    self,
    detection_result_ids: List[int],
    batch_dir: str | Path,
    image_num: int,
    task_pk: int,
    cmd_block_size: int = 64,
    urn_k: float = 0.3,
    if_use_llm: bool = False,
) -> None:
    """同 AI 服务器通信，负责写 zip 和 json，并拿到整批结果，防止阻塞主线程。"""

    t0 = time.time()
    batch_dir = Path(batch_dir)
    batch_dir.mkdir(parents=True, exist_ok=True)
    zip_path = batch_dir / "img.zip"
    data_path = batch_dir / "data.json"

    # 1️⃣  标记任务 & 子结果为 in_progress（DB I/O 很少，可以接受）
    dr_qs = (
        DetectionResult.objects.select_related("detection_task", "image_upload")
        .filter(id__in=detection_result_ids)
        .order_by("id")
    )
    if not dr_qs:
        return

    task = dr_qs[0].detection_task
    if task.status != "in_progress":
        task.status = "in_progress"
        task.save(update_fields=["status"])
    dr_qs.update(status="in_progress")
    
    # WebSocket 进度推送：开始准备批次数据
    send_task_progress_update(
        task_id=task_pk, 
        status="in_progress", 
        progress=5, 
        message="开始处理批次，准备打包数据"
    )

    # 1.5️⃣ 异步写 img.zip 和 data.json
    import zipfile, json
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        sorted_drs = sorted(list(dr_qs), key=lambda dr: dr.image_upload.id)
        for dr in sorted_drs:
            src = dr.image_upload.image.path
            arcname = f"{int(dr.image_upload.id):08d}{Path(src).suffix}"
            zf.write(src, arcname=arcname)

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(
            {"cmd_block_size": cmd_block_size, "urn_k": urn_k, "if_use_llm": if_use_llm},
            f, ensure_ascii=False, indent=4
        )

    # WebSocket 进度推送：开始检测
    send_task_progress_update(
        task_id=task_pk, 
        status="in_progress", 
        progress=10, 
        message="开始连接AI服务器进行检测",
        eta=10 if if_use_llm else 3  # 简单估算剩余时间
    )

    # 2️⃣  GPU / 网络 调用
    results = get_result(zip_path, data_path)
    retry_count = 0
    while (results is None or len(results[1][1]) != len(detection_result_ids)) and retry_count < 3:
        reconnect()
        retry_count += 1
        results = get_result(zip_path, data_path)

    if results is None:
        log_action(
            user=task.user,
            operation_type='ai_detect',
            target_type='DetectionTask',
            target_id=task.id,
            result='failure',
            error_msg='GPU server connection failed, retrying...',
            detail={'retry': True}
        )
        send_task_progress_update(task_pk, "failed", 0, "AI 服务器连接失败，正在重试...")
        raise self.retry(exc=RuntimeError("AI 服务器不可达"))

    # WebSocket 进度推送：GPU计算完成，开始后处理
    send_task_progress_update(
        task_id=task_pk, 
        status="in_progress", 
        progress=60, 
        message="AI检测完成，正在处理检测结果"
    )

    # 3️⃣  将每张图片拆成独立 payload，fan‑out 给 CPU worker
    subtasks = []
    for idx, dr_id in enumerate(detection_result_ids):
        one_result = _extract_single_result(results, idx)
        subtasks.append(process_single_result.s(dr_id, one_result))

    # 4️⃣  fan‑in：全部子任务结束后触发收尾
    chord(group(subtasks), finalize_task.s(task_pk, image_num)).delay()
    # finalize_task(task_pk, image_num)

    # 5️⃣  （可选）清理批次临时文件 – 放到 GPU 任务尾部即可
    try:
        zip_path.unlink(missing_ok=True)
        data_path.unlink(missing_ok=True)
        batch_dir.rmdir()  # 目录为空才会删除
    except OSError:
        pass

    print("[fetch_batch] 完成，用时", time.time() - t0, "s")


# ───────────────────────────────────────────────────────────────────────────────
# 2.  CPU & I/O 阶段 – 并行
# ───────────────────────────────────────────────────────────────────────────────

@shared_task(queue="cpu", acks_late=True)
def process_single_result(dr_pk: int, result_dict: Dict[str, Any]) -> bool:
    """把单张图片的检测结果写入数据库 & 文件系统。"""

    dr = DetectionResult.objects.select_related("image_upload").get(pk=dr_pk)

    try:
        # --- 还原 ndarray ---------------------------------------
        ela_np = np.array(result_dict["ela"], dtype=np.float32)
        llm_img_np = None
        if result_dict.get("llm_img") is not None:
            llm_img_np = np.array(result_dict["llm_img"], dtype=np.float32)

        # 2‑1  文件写入（磁盘 I/O）
        ela_path = save_ndarray_as_image(ela_np, subdir="ela_results", prefix=f"ela_{dr_pk}")
        llm_image_path = None
        if llm_img_np is not None:
            llm_image_path = save_ndarray_as_image(llm_img_np, subdir="llm_results", prefix=f"llm_{dr_pk}")

        # 2‑2  更新 DetectionResult 主表
        dr.is_fake = result_dict["overall_is_fake"]
        dr.confidence_score = result_dict["overall_confidence"]
        dr.llm_judgment = fanyi_text(result_dict["llm_text"])
        dr.ela_image = ela_path
        if llm_image_path:
            dr.llm_image = llm_image_path
        dr.exif_photoshop = result_dict["exif_flags"]["photoshop"]
        dr.exif_time_modified = result_dict["exif_flags"]["time_modified"]
        dr.detection_time = timezone.now()
        dr.status = "completed"
        dr.save(
            update_fields=[
                "is_fake",
                "confidence_score",
                "llm_judgment",
                "ela_image",
                "llm_image",
                "exif_photoshop",
                "exif_time_modified",
                "detection_time",
                "status",
            ]
        )

        # 2‑3  子检测方法批量写入
        subs = []
        for sub in result_dict["sub_method_results"]:
            mask_path = save_ndarray_as_image(
                np.array(sub["mask"]), subdir="masks", prefix=f"mask_{sub['method']}_{dr_pk}"
            )
            subs.append(
                SubDetectionResult(
                    detection_result=dr,
                    method=sub["method"],
                    probability=sub["prob"],
                    mask_image=mask_path,
                    mask_matrix=sub["mask"],
                )
            )
        SubDetectionResult.objects.bulk_create(subs, ignore_conflicts=True)

        # 2‑4  更新 ImageUpload 标志位
        iu = dr.image_upload
        iu.isFake = dr.is_fake
        iu.isDetect = True
        iu.save(update_fields=["isFake", "isDetect"])

        return True
        
    except Exception as e:
        import traceback
        log_action(
            user=dr.detection_task.user,
            operation_type='ai_detect_subtask',
            target_type='DetectionResult',
            target_id=dr.id,
            result='failure',
            error_msg=f"Subtask failed: {str(e)}",
            detail={'traceback': traceback.format_exc()}
        )
        dr.status = "failed"
        dr.save(update_fields=["status"])
        return False


# ───────────────────────────────────────────────────────────────────────────────
# 3.  收尾阶段 – 判断任务是否全部完成，然后生成报告 & 通知
# ───────────────────────────────────────────────────────────────────────────────

@shared_task(queue="cpu", acks_late=True)
def finalize_task(_chord_results: list | None, task_pk: int, image_num: int, _=None) -> None:  # body 签名固定
    task = DetectionTask.objects.get(pk=task_pk)
    processed = (
        DetectionResult.objects.filter(detection_task=task, status__in=["completed", "failed"]).count()
    )
    if processed != image_num:
        # 说明还有图片未完成，直接返回即可
        return

    failed_count = DetectionResult.objects.filter(detection_task=task, status="failed").count()

    # 判断最终状态
    if failed_count == image_num:
        final_status = "failed"
    elif failed_count > 0:
        final_status = "partially_completed"
    else:
        final_status = "completed"

    # ── Phase 1：标记"大模型分析中"，发进度通知 ──
    DetectionTask.objects.filter(pk=task_pk).update(status="analyzing")
    send_task_progress_update(
        task_id=task_pk,
        status="analyzing",
        progress=90,
        message="正在进行大模型综合智能分析..."
    )

    # ── Phase 2：调用大模型 ──
    llm_result = _run_llm_analysis_for_image_task(task, failed_count)
    if llm_result is not None:
        extra_payload = task.extra_payload or {}
        extra_payload['llm_analysis'] = llm_result
        DetectionTask.objects.filter(pk=task.pk).update(extra_payload=extra_payload)

    # ── Phase 3：标记最终状态 & 生成报告 ──
    with transaction.atomic():
        task = DetectionTask.objects.select_for_update().get(pk=task_pk)
        task.status = final_status
        task.completion_time = timezone.now()
        task.save(update_fields=["status", "completion_time"])
        generate_detection_task_report(task)

    log_action(
        user=task.user,
        operation_type='ai_detect',
        target_type='DetectionTask',
        target_id=task.id,
        result='success' if final_status == "completed" else "partial_success" if final_status == "partially_completed" else "failure",
        detail={'message': f'Task finalized with status: {final_status}', 'failed_count': failed_count}
    )

    send_task_progress_update(
        task_id=task_pk,
        status=final_status,
        progress=100,
        message=f"检测任务完成" if failed_count == 0 else f"任务完成，{failed_count} 张图片处理失败"
    )
    send_task_completion_notification(task.user, task_pk)


# ───────────────────────────────────────────────────────────────────────────────
# 4. 文本专属：全篇论文和 Review 文本的异步检测
# ───────────────────────────────────────────────────────────────────────────────

@shared_task(queue="ai", bind=True, acks_late=True, max_retries=3, default_retry_delay=15)
def process_text_detection_task(self, text_result_ids: List[int], task_pk: int, is_review: bool = False) -> None:
    """处理全篇论文或 Review 的检测（通常调用外部 LLM API 或特定的文本鉴伪算法）"""
    t0 = time.time()
    
    # 1. 标记任务为 in_progress
    tr_qs = (
        TextDetectionResult.objects.select_related("detection_task", "text_resource")
        .filter(id__in=text_result_ids)
        .order_by("id")
    )
    if not tr_qs:
        return
        
    task = tr_qs[0].detection_task
    if task.status != "in_progress":
        task.status = "in_progress"
        task.save(update_fields=["status"])
    tr_qs.update(status="in_progress")
    
    # WebSocket 进度推送
    task_type_str = "Review" if is_review else "论文"
    send_task_progress_update(
        task_id=task_pk, 
        status="in_progress", 
        progress=10, 
        message=f"开始连接大模型进行{task_type_str}文本分析",
        eta=15
    )
    
    # 2. 分发单个文本的处理任务
    subtasks = []
    for tr in tr_qs:
        # 提取需要检测的文本内容
        text_content = tr.text_resource.raw_text
        if tr.text_resource.normalized_text:
            text_content = tr.text_resource.normalized_text
            
        subtasks.append(
            process_single_text_result.s(tr.id, text_content, is_review).set(queue="ai")
        )
        
    # 3. fan-in: 全部结束后触发文本专属的 finalize
    chord(
        group(subtasks),
        finalize_text_task.s(task_pk, len(text_result_ids)).set(queue="ai"),
    ).delay()
    
    print(f"[process_text_detection_task] 分发完成，用时 {time.time() - t0} s")


@shared_task(queue="ai", acks_late=True)
def process_single_text_result(tr_pk: int, text_content: str, is_review: bool) -> bool:
    """单个文本的 Bert 文本鉴伪调用与数据库写回。"""
    tr = TextDetectionResult.objects.select_related("detection_task", "text_resource").get(pk=tr_pk)
    
    try:
        ai_result = BertTextAIDetectionBridge.submit_text(
            text=text_content,
            language=tr.text_resource.language,
        )

        is_fake = bool(ai_result.get("is_aigc"))
        overall_score = float(ai_result.get("confidence_score") or 0.0)
        probabilities = ai_result.get("probabilities") or {}
        reason = _build_bert_reason(ai_result, is_review=is_review)

        tr.is_fake = is_fake
        tr.confidence_score = overall_score

        if not is_review:
            tr.ai_generated_paragraphs = [
                {
                    "paragraph_index": 1,
                    "text": text_content[:200],
                    "ai_probability": float(probabilities.get("aigc", overall_score) or 0.0),
                    "label_name": ai_result.get("label_name"),
                    "reason": reason,
                    "input_summary": ai_result.get("input_summary") or {},
                }
            ]
            tr.factual_fake_reason = reason
            tr.template_tendency_score = None
            tr.template_analysis_reason = None
        else:
            tr.ai_generated_paragraphs = None
            tr.factual_fake_reason = None
            tr.template_tendency_score = overall_score
            tr.template_analysis_reason = reason

        tr.detection_time = timezone.now()
        tr.status = "completed"
        tr.save(update_fields=[
            "is_fake", "confidence_score", "ai_generated_paragraphs", 
            "factual_fake_reason", "template_tendency_score", "template_analysis_reason",
            "detection_time", "status"
        ])
        return True
        
    except BertTextAITransientError as e:
        import traceback
        _record_text_task_failure(tr.detection_task, str(e))
        log_action(
            user=tr.detection_task.user,
            operation_type='review_detect' if is_review else 'paper_detect',
            target_type='TextDetectionResult',
            target_id=tr.id,
            result='failure',
            error_msg=f"Bert text transient failure: {str(e)}",
            detail={'traceback': traceback.format_exc()}
        )
        tr.status = "failed"
        tr.save(update_fields=["status"])
        return False
    except (BertTextAIPermanentError, Exception) as e:
        import traceback
        _record_text_task_failure(tr.detection_task, str(e))
        log_action(
            user=tr.detection_task.user,
            operation_type='review_detect' if is_review else 'paper_detect',
            target_type='TextDetectionResult',
            target_id=tr.id,
            result='failure',
            error_msg=f"Text Subtask failed: {str(e)}",
            detail={'traceback': traceback.format_exc()}
        )
        tr.status = "failed"
        tr.save(update_fields=["status"])
        return False


@shared_task(queue="ai", acks_late=True)
def finalize_text_task(_chord_results: list | None, task_pk: int, text_num: int, _=None) -> None:
    """文本任务全部检测完成后的收尾"""
    task = DetectionTask.objects.get(pk=task_pk)
    processed = (
        TextDetectionResult.objects.filter(detection_task=task, status__in=["completed", "failed"]).count()
    )
    if processed != text_num:
        return

    with transaction.atomic():
        # 获取悲观锁，防止并发写入导致状态覆盖
        task = DetectionTask.objects.select_for_update().get(pk=task_pk)
        
        failed_count = TextDetectionResult.objects.filter(detection_task=task, status="failed").count()
        if failed_count == text_num:
            task.status = "failed"
        elif failed_count > 0:
            task.status = "partially_completed"
        else:
            task.status = "completed"
            
        task.completion_time = timezone.now()
        task.save(update_fields=["status", "completion_time"])
        
        # TODO: generate_text_detection_task_report(task) 如果有针对文本的报告生成的话
        # generate_detection_task_report(task)

    log_action(
        user=task.user,
        operation_type='paper_detect' if task.task_type == 'paper_text' else 'review_detect',
        target_type='DetectionTask',
        target_id=task.id,
        result='success' if task.status == "completed" else "partial_success" if task.status == "partially_completed" else "failure",
        detail={'message': f'Text Task finalized with status: {task.status}', 'failed_count': failed_count}
    )

    send_task_progress_update(
        task_id=task_pk, 
        status=task.status, 
        progress=100, 
        message="文本检测任务已全部完成"
    )
    send_task_completion_notification(task.user, task_pk)


@shared_task(queue="cpu", bind=True, acks_late=True, max_retries=2, default_retry_delay=10)
def run_structured_detection_task(self, task_pk: int):
    try:
        task = DetectionTask.objects.get(pk=task_pk)
    except DetectionTask.DoesNotExist:
        return

    if task.status == 'completed':
        return

    task.status = 'in_progress'
    task.failure_reason = None
    task.save(update_fields=['status', 'failure_reason'])
    send_task_progress_update(
        task_id=task_pk,
        status='in_progress',
        progress=30,
        message='正在进行结构化检测分析...'
    )

    try:
        StructuredDetectionService.execute_task(task)
    except StructuredAITransientError as exc:
        StructuredDetectionService.mark_failed(task, str(exc))
        send_task_progress_update(
            task_id=task_pk,
            status='failed',
            progress=0,
            message=f'检测失败: {exc}'
        )
        raise self.retry(exc=exc)
    except Exception as exc:
        StructuredDetectionService.mark_failed(task, str(exc))
        send_task_progress_update(
            task_id=task_pk,
            status='failed',
            progress=0,
            message=f'检测失败: {exc}'
        )
        return

    send_task_completion_notification(task.user, task_pk)


# ───────────────────────────────────────────────────────────────────────────────
#  Helper：把 get_result 的原始大 tuple 拆成易于序列化的 dict
# ───────────────────────────────────────────────────────────────────────────────

def _extract_single_result(raw_results: Any, idx: int) -> Dict[str, Any]:
    """根据你给出的原始格式，对 idx 处图片提取所需字段。
    为了示例清晰，没有做异常防御，请按实际格式自行调整。
    """
    # —— LLM 输出 ——
    llm_entry = raw_results[0][1][idx]
    llm_text = llm_entry[1][0] if llm_entry[1] is not None else "无"
    llm_img = llm_entry[1][1] if llm_entry[1] is not None else None  # 如有 mask，可自行提取

    # —— ELA ndarray ——
    ela_np = raw_results[1][1][idx][1]
    ela_list = np.asarray(ela_np).tolist()

    # —— EXIF 结果 ——
    exif_raw = raw_results[2][1][idx][1][1]
    exif_flags = {"photoshop": False, "time_modified": False}
    if exif_raw:
        exif_flags["photoshop"] = "使用了Photoshop进行修改" in exif_raw
        exif_flags["time_modified"] = "修改了拍摄或制作时间" in exif_raw

    # —— 五种 urn_* 方法 ——
    urn_offset = 4  # 第 4 个开始是 urn_*，每种方法取 2 切片
    if len(raw_results[0][1]) == 1:
        sub_raw = [
            ("splicing", raw_results[urn_offset + 0][1][0][2 * idx : 2 * idx + 2]),
            ("blurring", raw_results[urn_offset + 1][1][0][2 * idx : 2 * idx + 2]),
            ("bruteforce", raw_results[urn_offset + 2][1][0][2 * idx : 2 * idx + 2]),
            ("contrast", raw_results[urn_offset + 3][1][0][2 * idx : 2 * idx + 2]),
            ("inpainting", raw_results[urn_offset + 4][1][0][2 * idx : 2 * idx + 2]),
        ]
    else:
        sub_raw = [
            ("splicing", raw_results[urn_offset + 0][1][2 * idx: 2 * idx + 2]),
            ("blurring", raw_results[urn_offset + 1][1][2 * idx: 2 * idx + 2]),
            ("bruteforce", raw_results[urn_offset + 2][1][2 * idx: 2 * idx + 2]),
            ("contrast", raw_results[urn_offset + 3][1][2 * idx: 2 * idx + 2]),
            ("inpainting", raw_results[urn_offset + 4][1][2 * idx: 2 * idx + 2]),
        ]

    bar = 0.5
    overall_is_fake = any(v[1] > bar for _, v in sub_raw) or exif_raw is not None
    overall_confidence = max(v[1] for _, v in sub_raw)
    if exif_raw is not None:
        overall_confidence = 1.0

    sub_method_results: List[Dict[str, Any]] = []
    for method_key, (mask_np, prob) in sub_raw:
        sub_method_results.append(
            {
                "method": method_key,
                "prob": float(prob),
                "mask": np.squeeze(mask_np).tolist(),
            }
        )

    return {
        "llm_text": llm_text,
        "llm_img": np.asarray(llm_img).tolist(),
        "ela": ela_list,
        "overall_is_fake": overall_is_fake,
        "overall_confidence": overall_confidence,
        "exif_flags": exif_flags,
        "sub_method_results": sub_method_results,
    }


def _build_bert_reason(ai_result: Dict[str, Any], is_review: bool) -> str:
    label_name = ai_result.get("label_name") or ("aigc" if ai_result.get("is_aigc") else "human")
    score = float(ai_result.get("confidence_score") or 0.0)
    probabilities = ai_result.get("probabilities") or {}
    aigc_prob = float(probabilities.get("aigc") or 0.0)
    human_prob = float(probabilities.get("human") or 0.0)

    if is_review:
        if ai_result.get("is_aigc"):
            return (
                f"Bert 文本鉴伪判定该评审文本存在较强模板化/AI生成倾向，"
                f"标签为 {label_name}，置信度 {score:.4f}，AIGC 概率 {aigc_prob:.4f}。"
            )
        return (
            f"Bert 文本鉴伪判定该评审文本更接近人工撰写，"
            f"标签为 {label_name}，置信度 {score:.4f}，人工概率 {human_prob:.4f}。"
        )

    if ai_result.get("is_aigc"):
        return (
            f"Bert 文本鉴伪判定该文本存在 AI 生成倾向，"
            f"标签为 {label_name}，置信度 {score:.4f}，AIGC 概率 {aigc_prob:.4f}。"
        )
    return (
        f"Bert 文本鉴伪判定该文本更接近人工撰写，"
        f"标签为 {label_name}，置信度 {score:.4f}，人工概率 {human_prob:.4f}。"
    )


def _record_text_task_failure(task: DetectionTask, reason: str) -> None:
    reason = (reason or "").strip()
    if not reason:
        return

    DetectionTask.objects.filter(pk=task.pk).update(failure_reason=reason)


# ───────────────────────────────────────────────────────────────────────────────
#  CELERY 启动示例（写在 README 或部署脚本）
# ───────────────────────────────────────────────────────────────────────────────
# GPU 专用 worker（始终 1 并发）
#   celery -A fake_image_detector worker -Q ai --concurrency 1 -n ai@%h
# CPU/I‑O worker（并发可调）
#   celery -A fake_image_detector worker -Q cpu,default --concurrency 8 -n cpu@%h
# ----------------------------------------------------------------------------
