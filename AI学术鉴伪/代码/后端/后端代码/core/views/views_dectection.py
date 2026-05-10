import json
import os
import time
import zipfile
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers

from core.models import (
    DetectionResult,
    DetectionTask,
    FileManagement,
    ImageUpload,
    ResourceContainer,
    StructuredDetectionResult,
    SubDetectionResult,
    User,
)
from core.services.material_validation_service import MaterialValidationService
from core.services.structured_detection_service import StructuredDetectionService
from ..utils.log_utils import action_log
from django.db.models import Q
from ..utils.report_generator import generate_detection_task_report
from ..utils.serializers_safe import serialize_value

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_detection_result(request, image_id):
    try:
        # 获取检测结果
        detection_result = DetectionResult.objects.get(image_upload_id=image_id,
                                                       image_upload__file_management__user=request.user)

        # 检查状态并返回相应数据
        if detection_result.status == 'in_progress':
            return Response({
                "image_id": detection_result.image_upload.id,
                "status": "正在检测中",
                "message": "AI检测正在进行，请稍等"
            })

        # 如果检测已完成
        return Response({
            "image_id": detection_result.image_upload.id,
            "status": "检测已完成",
            "is_fake": detection_result.is_fake,
            "confidence_score": detection_result.confidence_score,
            "detection_time": timezone.localtime(detection_result.detection_time)
        })

    except DetectionResult.DoesNotExist:
        return Response({"message": "Detection result not found"}, status=404)


from ..tasks_new import fetch_batch, run_structured_detection_task


def _check_organization_quota(organization, use_llm: bool, usage_count: int):
    if use_llm:
        if not organization.can_use_llm(usage_count):
            return Response(
                {
                    "message": (
                        "You have exceeded your LLM method usage limit for this week. "
                        f"Your organization can only submit {organization.remaining_llm_uses} more images."
                    )
                },
                status=400,
            )
        organization.decrement_llm_uses(usage_count)
        return None

    if not organization.can_use_non_llm(usage_count):
        return Response(
            {
                "message": (
                    "You have exceeded your non-LLM method usage limit for this week. "
                    f"Your organization can only submit {organization.remaining_non_llm_uses} more images."
                )
            },
            status=400,
        )
    organization.decrement_non_llm_uses(usage_count)
    return None


def _normalize_structured_submit_payload(request):
    detect_type = (request.data.get('detect_type') or 'image').strip().lower()
    container_id = request.data.get('container_id')
    raw_file_ids = request.data.get('file_ids')
    fallback_file_ids = request.data.get('image_ids')

    if raw_file_ids in (None, ''):
        raw_file_ids = fallback_file_ids

    if raw_file_ids in (None, ''):
        raw_file_ids = []

    if isinstance(raw_file_ids, (int, str)):
        raw_file_ids = [raw_file_ids]

    file_ids = []
    for item in raw_file_ids:
        try:
            file_ids.append(int(item))
        except (TypeError, ValueError):
            continue

    raw_review_text_ids = request.data.get('review_text_ids') or []
    if isinstance(raw_review_text_ids, (int, str)):
        raw_review_text_ids = [raw_review_text_ids]

    review_text_ids = []
    for item in raw_review_text_ids:
        try:
            review_text_ids.append(int(item))
        except (TypeError, ValueError):
            continue

    return detect_type, container_id, file_ids, review_text_ids


def _submit_structured_detection(request, user, mode, task_name, cmd_block_size, urn_k, if_use_llm):
    detect_type, container_id, file_ids, review_text_ids = _normalize_structured_submit_payload(request)

    if detect_type not in {'paper', 'review', 'multi'}:
        return Response({"message": "Unsupported detect_type"}, status=400)

    container = None
    if container_id not in (None, ''):
        container = ResourceContainer.objects.filter(
            id=container_id,
            owner=user,
        ).first()
        if container is None:
            return Response({"message": "Container not found"}, status=404)

    file_queryset = FileManagement.objects.filter(id__in=file_ids, user=user).order_by('id')
    if file_ids and file_queryset.count() != len(set(file_ids)):
        return Response({"message": "Some files are invalid"}, status=404)

    if container is None and file_queryset.exists():
        container = file_queryset.first().container

    if detect_type == 'paper':
        if not file_queryset.exists() and container is None:
            return Response({"message": "No valid paper files found"}, status=400)

    if detect_type == 'review':
        has_review_files = file_queryset.exists()
        has_review_texts = bool(review_text_ids)
        if not has_review_files and not has_review_texts and container is None:
            return Response({"message": "No valid review materials found"}, status=400)

    if detect_type == 'multi':
        if container is None:
            return Response({"message": "container_id is required for multi detection"}, status=400)
        validation_result = MaterialValidationService.validate_container_materials(user, container)
        if not validation_result['valid']:
            return Response({"message": validation_result['message'], "details": validation_result}, status=400)

    usage_count = max(len(file_ids), 1)
    quota_error = _check_organization_quota(user.organization, if_use_llm, usage_count)
    if quota_error:
        return quota_error

    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=user,
        container=container,
        task_name=task_name,
        status='pending',
        detect_type=detect_type,
        cmd_block_size=cmd_block_size,
        urn_k=urn_k,
        if_use_llm=if_use_llm,
        extra_payload={
            'mode': mode,
            'file_ids': file_ids,
            'review_text_ids': review_text_ids,
            'container_id': container.id if container else None,
        },
    )

    run_structured_detection_task.apply_async(args=[detection_task.pk], queue='cpu')

    return Response(
        {
            "message": "Detection request submitted successfully",
            "task_id": detection_task.id,
            "task_name": detection_task.task_name,
            "detect_type": detection_task.detect_type,
        }
    )
from ..tasks_new import fetch_batch, process_text_detection_task
from ..models import ReviewTextResource, TextDetectionResult


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def submit_detection(request):
#     user_id = request.user.id
#     user = User.objects.get(id=user_id)
#     if not user.has_permission('submit'):
#         return Response({"错误": "该用户没有提交检测的权限"}, status=403)
#
#     # 获取用户提交的图像ID列表
#     image_ids = request.data.get('image_ids', [])
#     task_name = request.data.get('task_name', 'New Detection Task')  # 从请求中获取任务名称，默认为 "New Detection Task"
#
#     # 获取额外的参数
#     cmd_block_size = request.data.get('cmd_block_size', 64)  # 默认为64
#     urn_k = request.data.get('urn_k', 0.3)  # 默认为0.3
#     if_use_llm = request.data.get('if_use_llm', False)  # 默认为False
#
#     if not image_ids:
#         return Response({"message": "No image IDs provided"}, status=400)
#
#     # 查找用户上传的所有图像
#     image_uploads = ImageUpload.objects.filter(id__in=image_ids, file_management__user=request.user)
#
#     # 检验不为空
#     if not image_uploads.exists():
#         return Response({"message": "No valid images found"}, status=404)
#
#     # 创建一个新的检测任务
#     detection_task = DetectionTask.objects.create(
#         organization=user.organization,
#         user=request.user,
#         task_name=task_name,  # 使用用户提交的任务名称
#         status='pending',  # 初始状态为"排队中"
#         cmd_block_size=cmd_block_size,
#         urn_k=urn_k,
#         if_use_llm=if_use_llm
#     )
#
#     # 在Log表中记录检测任务的创建
#     Log.objects.create(
#         user=request.user,
#         operation_type='detection',
#         related_model='DetectionTask',
#         related_id=detection_task.id
#     )
#
#     # 对每个图像生成检测记录，并将状态设置为"正在检测中"
#     for image_upload in image_uploads:
#         detection_result, created = DetectionResult.objects.get_or_create(
#             image_upload=image_upload,
#             detection_task=detection_task,  # 将任务与检测结果关联
#             defaults={'status': 'in_progress'}
#         )
#
#         if not created:
#             detection_result.status = 'in_progress'
#             detection_result.save()
#
#         # 提交AI检测任务给Celery，传递参数
#         run_ai_detection.delay(detection_result.id, cmd_block_size, urn_k, if_use_llm)
#
#     return Response({
#         "message": "Detection request submitted successfully",
#         "task_id": detection_task.id,
#         "task_name": detection_task.task_name,  # 返回任务名称
#     })
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@action_log('ai_detect', target_type='DetectionTask', target_id_field='task_id')
def submit_detection2(request):
    submit_time = time.time()
    user_id = request.user.id
    mode = int(request.data.get('mode', 1))
    user = User.objects.get(id=user_id)
    organization = user.organization  # 获取用户所属组织
    organization.reset_usage()  # 重置组织内所有用户的共享次数
    if not user.has_permission('submit'):
        return Response({"错误": "该用户没有提交检测的权限"}, status=403)

    detect_type = (request.data.get('detect_type') or 'image').strip().lower()
    # 兼容三种提交流程：image_ids（旧）/ file_id / file_ids（新）
    def _to_int_list(raw_value):
        if raw_value is None:
            return []

        if isinstance(raw_value, (list, tuple)):
            values = raw_value
        elif isinstance(raw_value, str):
            stripped = raw_value.strip()
            if not stripped:
                return []
            if stripped.startswith('[') and stripped.endswith(']'):
                try:
                    parsed = json.loads(stripped)
                    values = parsed if isinstance(parsed, list) else [parsed]
                except json.JSONDecodeError:
                    values = [item for item in stripped.split(',') if item.strip()]
            elif ',' in stripped:
                values = [item for item in stripped.split(',') if item.strip()]
            else:
                values = [stripped]
        else:
            values = [raw_value]

        normalized = []
        for item in values:
            try:
                normalized.append(int(item))
            except (TypeError, ValueError):
                continue
        return normalized

    image_ids = []
    if hasattr(request.data, 'getlist'):
        image_ids.extend(_to_int_list(request.data.getlist('image_ids')))
    image_ids.extend(_to_int_list(request.data.get('image_ids')))

    # 去重并排序，避免重复提交同一图片
    image_ids = sorted(set(image_ids))

    image_uploads = ImageUpload.objects.none()
    resolved_from_file_ids = False
    if image_ids:
        image_uploads = ImageUpload.objects.filter(id__in=image_ids, file_management__user=request.user)
    else:
        file_ids = []
        if hasattr(request.data, 'getlist'):
            file_ids.extend(_to_int_list(request.data.getlist('file_ids')))
            file_ids.extend(_to_int_list(request.data.getlist('file_id')))
        file_ids.extend(_to_int_list(request.data.get('file_ids')))
        file_ids.extend(_to_int_list(request.data.get('file_id')))

        file_ids = sorted(set(file_ids))
        if file_ids:
            files_qs = FileManagement.objects.filter(id__in=file_ids, user=request.user)
            image_uploads = ImageUpload.objects.filter(file_management__in=files_qs, file_management__user=request.user)
            resolved_from_file_ids = True

    # 无论从哪个入口解析，统一回填最终 image_ids 给后续流程使用
    resolved_image_ids = sorted(image_uploads.values_list('id', flat=True))
    if resolved_image_ids:
        image_ids = resolved_image_ids
    task_name = request.data.get('task_name', 'New Detection Task')  # 从请求中获取任务名称，默认为 "New Detection Task"

    # 获取额外的参数
    cmd_block_size = request.data.get('cmd_block_size', 64)  # 默认为64
    urn_k = request.data.get('urn_k', 0.3)  # 默认为0.3
    if_use_llm = request.data.get('if_use_llm', False)  # 默认为False
    if mode == 3:
        if_use_llm = True

    if detect_type != 'image':
        return _submit_structured_detection(
            request=request,
            user=user,
            mode=mode,
            task_name=task_name,
            cmd_block_size=cmd_block_size,
            urn_k=urn_k,
            if_use_llm=if_use_llm,
        )

    if not image_ids:
        if resolved_from_file_ids:
            return Response({"message": "No valid images found for provided file IDs"}, status=400)
        return Response({"message": "No image IDs provided"}, status=400)

    # 检验不为空
    if not image_uploads.exists():
        return Response({"message": "No valid images found"}, status=404)

    num_images = len(image_uploads)
    quota_error = _check_organization_quota(organization, if_use_llm, num_images)
    if quota_error:
        return quota_error

    # 创建一个新的检测任务
    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=request.user,
        task_name=task_name,  # 使用用户提交的任务名称
        status='pending',  # 初始状态为"排队中"
        detect_type='image',
        cmd_block_size=cmd_block_size,
        urn_k=urn_k,
        if_use_llm=if_use_llm,
        extra_payload={'mode': mode, 'image_ids': image_ids},
    )

    # ----① 建 DetectionResult，与原逻辑相同-------------
    detection_results = []          # 用来分批
    for image_upload in image_uploads:
        dr, _ = DetectionResult.objects.get_or_create(
            image_upload=image_upload,
            detection_task=detection_task,
            defaults={'status': 'in_progress'}
        )
        dr.status = 'in_progress'
        dr.save(update_fields=['status'])
        detection_results.append(dr)

    # ----② 20 张一批，调 Celery 异步处理打包和检测 ---------------
    # views.py 片段（其余保持不变）
    temp_root = Path(settings.MEDIA_ROOT) / 'temp'
    temp_root.mkdir(parents=True, exist_ok=True)

    batch_size = 20
    for idx in range(0, len(detection_results), batch_size):
        batch_drs = detection_results[idx: idx + batch_size]

        # ——— ① 为该批创建专属子目录 temp/task_<task_id>_batch_<n>/ ———
        batch_dir = temp_root / f"task_{detection_task.id}_batch_{idx // batch_size}"
        # 不再在此处进行同步的文件写入(zip和json)，转移到 Celery 任务 fetch_batch 中执行

        # ——— ② 调 Celery ———
        celery_time = time.time()
        print('从提交到调用celery耗时', celery_time - submit_time)

        if mode == 2:  # 加急
            pri = 0
        else:
            pri = 1
        fetch_batch.apply_async(
            args=[
                [dr.id for dr in batch_drs], 
                str(batch_dir), 
                len(image_ids), 
                detection_task.pk,
                cmd_block_size,
                urn_k,
                if_use_llm
            ],
            queue='ai',
            priority=pri
        )

    return Response({
        "message": "Detection request submitted successfully",
        "task_id": detection_task.id,
        "task_name": detection_task.task_name,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@action_log('paper_detect', target_type='DetectionTask', target_id_field='task_id')
def submit_text_detection(request):
    """
    提交文本（全篇论文或 Review）进行鉴伪检测
    支持传入 resource_ids (ReviewTextResource 的 ID 列表)
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if not user.has_permission('submit'):
        return Response({"错误": "该用户没有提交检测的权限"}, status=403)

    task_name = request.data.get('task_name', 'New Text Detection Task')
    task_type = request.data.get('task_type', 'paper_text')  # 'paper_text' 或 'review_text'
    
    if task_type not in ['paper_text', 'review_text']:
        return Response({"message": "Invalid task_type. Must be 'paper_text' or 'review_text'"}, status=400)

    # 解析传入的资源 ID 列表
    def _to_int_list(raw_value):
        if raw_value is None:
            return []
        if isinstance(raw_value, (list, tuple)):
            values = raw_value
        elif isinstance(raw_value, str):
            stripped = raw_value.strip()
            if not stripped:
                return []
            if stripped.startswith('[') and stripped.endswith(']'):
                try:
                    parsed = json.loads(stripped)
                    values = parsed if isinstance(parsed, list) else [parsed]
                except json.JSONDecodeError:
                    values = [item for item in stripped.split(',') if item.strip()]
            elif ',' in stripped:
                values = [item for item in stripped.split(',') if item.strip()]
            else:
                values = [stripped]
        else:
            values = [raw_value]

        normalized = []
        for item in values:
            try:
                normalized.append(int(item))
            except (TypeError, ValueError):
                continue
        return normalized

    resource_ids = []
    if hasattr(request.data, 'getlist'):
        resource_ids.extend(_to_int_list(request.data.getlist('resource_ids')))
    resource_ids.extend(_to_int_list(request.data.get('resource_ids')))
    resource_ids = sorted(set(resource_ids))

    if not resource_ids:
        return Response({"message": "No resource_ids provided"}, status=400)

    # 验证资源存在并且属于该用户（这里假定容器拥有者是当前用户）
    text_resources = ReviewTextResource.objects.filter(
        id__in=resource_ids,
        container__owner=request.user
    )

    if not text_resources.exists():
        return Response({"message": "No valid text resources found"}, status=404)

    # 创建检测任务
    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=request.user,
        task_name=task_name,
        task_type=task_type,
        status='pending'
    )

    # 创建文本检测结果记录
    text_detection_results = []
    for tr in text_resources:
        tdr, _ = TextDetectionResult.objects.get_or_create(
            text_resource=tr,
            detection_task=detection_task,
            defaults={'status': 'in_progress'}
        )
        tdr.status = 'in_progress'
        tdr.save(update_fields=['status'])
        text_detection_results.append(tdr)

    # 调用 Celery 任务进行异步处理
    is_review = (task_type == 'review_text')
    process_text_detection_task.apply_async(
        args=[
            [tdr.id for tdr in text_detection_results],
            detection_task.pk,
            is_review
        ],
        queue='ai'
    )

    return Response({
        "message": f"Text detection request ({task_type}) submitted successfully",
        "task_id": detection_task.id,
        "task_name": detection_task.task_name,
        "task_type": detection_task.task_type
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_text_detection_result(request, resource_id):
    """
    获取单个文本资源的检测结果
    """
    try:
        # 获取最新的检测结果
        tdr = TextDetectionResult.objects.filter(
            text_resource_id=resource_id,
            detection_task__user=request.user
        ).order_by('-detection_time').first()

        if not tdr:
            return Response({"message": "Detection result not found"}, status=404)

        if tdr.status == 'in_progress':
            return Response({
                "resource_id": tdr.text_resource.id,
                "status": "正在检测中",
                "message": "大模型文本检测正在进行，请稍等"
            })

        # 返回检测已完成的数据
        return Response({
            "resource_id": tdr.text_resource.id,
            "status": "检测已完成",
            "is_fake": tdr.is_fake,
            "confidence_score": tdr.confidence_score,
            "ai_generated_paragraphs": tdr.ai_generated_paragraphs,
            "factual_fake_reason": tdr.factual_fake_reason,
            "template_tendency_score": tdr.template_tendency_score,
            "template_analysis_reason": tdr.template_analysis_reason,
            "detection_time": timezone.localtime(tdr.detection_time) if tdr.detection_time else None
        })

    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_text_results(request, task_id):
    """
    获取某个检测任务下所有文本的检测结果列表
    """
    try:
        task = DetectionTask.objects.get(id=task_id, user=request.user)
        
        if task.task_type not in ['paper_text', 'review_text', 'multi_material']:
            return Response({"message": "Not a text-related task"}, status=400)
            
        results = TextDetectionResult.objects.filter(detection_task=task)
        
        data = []
        for tdr in results:
            data.append({
                "result_id": tdr.id,
                "resource_id": tdr.text_resource.id,
                "text_type": tdr.text_resource.text_type,
                "status": tdr.status,
                "is_fake": tdr.is_fake,
                "confidence_score": tdr.confidence_score,
                "detection_time": timezone.localtime(tdr.detection_time) if tdr.detection_time else None
            })
            
        return Response({
            "task_id": task.id,
            "task_name": task.task_name,
            "task_type": task.task_type,
            "overall_status": task.status,
            "results": data
        })

    except DetectionTask.DoesNotExist:
        return Response({"message": "Task not found"}, status=404)


import os
from django.http import FileResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import DetectionTask

from ..utils.report_generator import generate_detection_task_report

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_task_report(request, task_id):
    """
    GET /api/tasks/<task_id>/report/
    下载检测报告 PDF
    """
    try:
        task = DetectionTask.objects.get(id=task_id, user=request.user)
        # generate_detection_task_report(task)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "Task not found."}, status=404)

    if task.status not in ["completed", "partially_completed", "failed"]:
        return Response({"detail": "Task not completed yet."}, status=400)

    if not task.report_file:
        # generate_detection_task_report(task)
        return Response({"detail": "Report is still being generated."}, status=202)

    abs_path = os.path.join(settings.MEDIA_ROOT, task.report_file.name)
    if not os.path.exists(abs_path):
        return Response({"detail": "Report file missing."}, status=410)

    return FileResponse(open(abs_path, "rb"),
                        as_attachment=True,
                        filename=f"task_{task.id}_report.pdf")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def image2dr(request, image_id):
    """
    GET /api/images/<image_id>/getdr/
    下载该图片对应任务的检测报告 PDF
    """
    try:
        detection_result = DetectionResult.objects.select_related('detection_task').get(
            image_upload_id=image_id,
        )
    except DetectionResult.DoesNotExist:
        return Response({"detail": "Image or task not found, or permission denied."}, status=404)
    except DetectionResult.MultipleObjectsReturned:
        return Response({"detail": "Multiple detection results found for this image."}, status=500)
    # 返回detection_result的id
    return Response({"detection_result_id": detection_result.id})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_image_report(request, image_id):
    """
    GET /api/images/<image_id>/report/
    下载该图片对应任务的检测报告 PDF
    """
    try:
        # 获取与image_id关联且属于当前用户的DetectionResult及其关联的DetectionTask
        detection_result = DetectionResult.objects.select_related('detection_task').get(
            image_upload_id=image_id,
            # detection_task__user=request.user
        )
    except DetectionResult.DoesNotExist:
        return Response({"detail": "Image or task not found, or permission denied."}, status=404)
    except DetectionResult.MultipleObjectsReturned:
        return Response({"detail": "Multiple detection results found for this image."}, status=500)

    task = detection_result.detection_task

    # 后续逻辑与原接口一致，检查任务状态和报告文件
    if task.status not in ["completed", "partially_completed", "failed"]:
        return Response({"detail": "Task not completed yet."}, status=400)

    if not task.report_file:
        return Response({"detail": "Report is still being generated."}, status=202)

    abs_path = os.path.join(settings.MEDIA_ROOT, task.report_file.name)
    if not os.path.exists(abs_path):
        return Response({"detail": "Report file missing."}, status=410)

    return FileResponse(open(abs_path, "rb"),
                        as_attachment=True,
                        filename=f"task_{task.id}_report.pdf")


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import DetectionTask
from ..utils.serializers_safe import serialize_value

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_task_results(request, task_id):
    """
    ?include_image=1   —— 额外返回原始图像 URL
    """
    task = get_object_or_404(DetectionTask, id=task_id, user=request.user)

    include_img = request.query_params.get("include_image", "0") in ("1", "true", "True")
    result_list = []

    for dr in task.detection_results.select_related("image_upload"):
        item = {"result_id": dr.id, "image_id": dr.image_upload.id, "timestamp": dr.detection_time}
        if include_img:
            item["image_url"] = serialize_value(dr.image_upload.image, request)
        result_list.append(item)

    return Response({
        "task_id": task.id,
        "total_results": len(result_list),
        "results": result_list,
    })

# 增加两个接口，分别返回造假的图片，和正常的图片；判别方式是detection_result.is_fake
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_fake_task_results(request, task_id):
    """
    ?include_image=1   —— 额外返回原始图像 URL
    """
    task = get_object_or_404(DetectionTask, id=task_id, user=request.user)

    include_img = request.query_params.get("include_image", "0") in ("1", "true", "True")
    result_list = []

    for dr in task.detection_results.select_related("image_upload"):
        if dr.status == "completed" and dr.is_fake is True:
            item = {"result_id": dr.id, "image_id": dr.image_upload.id, "timestamp": dr.detection_time}
            if include_img:
                item["image_url"] = serialize_value(dr.image_upload.image, request)
            result_list.append(item)

    return Response({
        "task_id": task.id,
        "total_results": len(result_list),
        "results": result_list,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_normal_task_results(request, task_id):
    """
    ?include_image=1   —— 额外返回原始图像 URL
    """
    task = get_object_or_404(DetectionTask, id=task_id, user=request.user)

    include_img = request.query_params.get("include_image", "0") in ("1", "true", "True")
    result_list = []

    for dr in task.detection_results.select_related("image_upload"):
        if dr.status == "completed" and dr.is_fake is False:
            item = {"result_id": dr.id, "image_id": dr.image_upload.id, "timestamp": dr.detection_time}
            if include_img:
                item["image_url"] = serialize_value(dr.image_upload.image, request)
            result_list.append(item)

    return Response({
        "task_id": task.id,
        "total_results": len(result_list),
        "results": result_list,
    })


from rest_framework import serializers
from ..models import DetectionResult, SubDetectionResult
from django.db.models.fields.files import FieldFile

class SubDetectionResultSerializer(serializers.ModelSerializer):
    mask_image   = serializers.SerializerMethodField()
    mask_matrix  = serializers.SerializerMethodField()   # ← 新增

    class Meta:
        model  = SubDetectionResult
        fields = ["method", "probability", "mask_image", "mask_matrix"]

    # --- helpers ---------------------------------------------------------
    def get_mask_image(self, obj):
        req = self.context["request"]
        if isinstance(obj.mask_image, FieldFile) and obj.mask_image:
            return req.build_absolute_uri(obj.mask_image.url)
        return None

    def get_mask_matrix(self, obj):
        """
        只有调用方在 context 里显式标记 include_matrix=True 时才返回
        """
        if self.context.get("include_matrix"):
            return obj.mask_matrix          # 已经是 list[list[float]]
        return None
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def detection_result_detail(request, result_id):
    dr = get_object_or_404(
        DetectionResult,
        id=result_id,
        # image_upload__file_management__user=request.user
    )

    # -------- 解析 fields & include_matrix ------------------------------
    raw_fields = request.query_params.get("fields")
    requested  = ({f.strip() for f in raw_fields.split(",")} if raw_fields
                  else {"overall", "llm", "llm_image", "ela_image", "exif", "timestamps",
                        "image", "sub_methods"})

    want_matrix = request.query_params.get("include_matrix", "0").lower() in ("1", "true", "yes")

    # -------- 基础信息 ---------------------------------------------------
    data = {"result_id": dr.id}

    def add(name, value):
        if name in requested:
            data[name] = value

    add("overall", {
        "is_fake": dr.is_fake,
        "confidence_score": dr.confidence_score,
    })
    add("llm",          dr.llm_judgment)
    add("llm_image",    serialize_value(dr.llm_image, request))
    add("ela_image",    serialize_value(dr.ela_image, request))
    add("exif", {
        "photoshop_edited":  dr.exif_photoshop,
        "time_modified":     dr.exif_time_modified,
    })
    add("timestamps",   timezone.localtime(dr.detection_time))
    add("image",        serialize_value(dr.image_upload.image, request))

    # -------- 子方法 -----------------------------------------------------
    if "sub_methods" in requested:
        subs = dr.sub_results.all()
        ser  = SubDetectionResultSerializer(
            subs,
            many=True,
            context={"request": request, "include_matrix": want_matrix}
        )
        data["sub_methods"] = ser.data

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def detection_result_by_image(request, image_id):
    # 通过image_id获取对应的DetectionResult
    dr = get_object_or_404(
        DetectionResult,
        image_upload__id=image_id,
        # image_upload__file_management__user=request.user
    )

    # -------- 解析 fields & include_matrix ------------------------------
    raw_fields = request.query_params.get("fields")
    requested = ({f.strip() for f in raw_fields.split(",")} if raw_fields
                 else {"overall", "llm", "ela_image", "exif", "timestamps",
                       "image", "sub_methods"})

    want_matrix = request.query_params.get("include_matrix", "0").lower() in ("1", "true", "yes")

    # -------- 基础信息 ---------------------------------------------------
    data = {"result_id": dr.id}

    def add(name, value):
        if name in requested:
            data[name] = value

    add("overall", {
        "is_fake": dr.is_fake,
        "confidence_score": dr.confidence_score,
    })
    add("llm", dr.llm_judgment)
    add("ela_image", serialize_value(dr.ela_image, request))
    add("exif", {
        "photoshop_edited": dr.exif_photoshop,
        "time_modified": dr.exif_time_modified,
    })
    add("timestamps", dr.detection_time)
    add("image", serialize_value(dr.image_upload.image, request))

    # -------- 子方法 -----------------------------------------------------
    if "sub_methods" in requested:
        subs = dr.sub_results.all()
        ser = SubDetectionResultSerializer(
            subs,
            many=True,
            context={"request": request, "include_matrix": want_matrix}
        )
        data["sub_methods"] = ser.data

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def structured_task_result(request, task_id):
    task = get_object_or_404(DetectionTask, id=task_id, user=request.user)

    if task.detect_type == 'image':
        total_results = task.detection_results.count()
        completed_results = task.detection_results.filter(status='completed').count()
        fake_results = task.detection_results.filter(is_fake=True).count()
        return Response(
            {
                'task_id': task.id,
                'detect_type': task.detect_type,
                'status': task.status,
                'task_name': task.task_name,
                'material_summary': {
                    'image_count': total_results,
                    'completed_count': completed_results,
                    'fake_count': fake_results,
                },
            }
        )

    structured_result = StructuredDetectionResult.objects.filter(detection_task=task).first()
    payload = structured_result.result_payload if structured_result else {}
    return Response(
        {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': task.detect_type,
            'status': task.status,
            'failure_reason': task.failure_reason,
            'container_id': task.container_id,
            'result': payload,
            'summary': structured_result.summary if structured_result else None,
            'confidence_score': structured_result.confidence_score if structured_result else None,
            'overall_is_fake': structured_result.overall_is_fake if structured_result else None,
            'ai_response': structured_result.ai_response if structured_result else {},
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_detection_task_status_normal(request, task_id):
    try:
        # 获取任务和关联的检测结果
        detection_task = DetectionTask.objects.get(id=task_id)
        detection_results = DetectionResult.objects.filter(detection_task=detection_task)

        # 收集任务相关的图像和状态信息
        task_status = {
            "task_id": detection_task.id,
            "task_name": detection_task.task_name,
            "detect_type": detection_task.detect_type,
            "status": detection_task.status,
            "upload_time": timezone.localtime(detection_task.upload_time),
            "completion_time": timezone.localtime(detection_task.completion_time) if detection_task.completion_time else None,
            "detection_results": []
        }

        if detection_task.detect_type != 'image':
            structured_result = StructuredDetectionResult.objects.filter(detection_task=detection_task).first()
            task_status["structured_result"] = structured_result.result_payload if structured_result else {}
            task_status["failure_reason"] = detection_task.failure_reason
            return Response(task_status)

        for result in detection_results:
            task_status["detection_results"].append({
                "image_id": result.image_upload.id,
                "status": result.status,
                "is_fake": result.is_fake,
                "confidence_score": result.confidence_score,
                "detection_time": timezone.localtime(result.detection_time),
            })

        return Response(task_status)

    except DetectionTask.DoesNotExist:
        return Response({"message": "Detection task not found"}, status=404)

from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # 默认每页条数
    page_size_query_param = 'page_size'  # 客户端控制每页数量的参数名
    max_page_size = 100  # 允许客户端设置的最大每页数量

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total': self.page.paginator.count,
            'tasks': data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tasks(request):
    # 获取分页参数
    page = int( request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    status = request.query_params.get('status', '')
    start_time = request.query_params.get('startTime', None)
    end_time = request.query_params.get('endTime', None)

    # 获取当前用户的所有检测任务并应用筛选条件
    tasks = DetectionTask.objects.filter(user=request.user).order_by('-upload_time')
    
    if status:
        tasks = tasks.filter(status=status)
    if start_time:
        tasks = tasks.filter(upload_time__gte=start_time)
    if end_time:
        tasks = tasks.filter(upload_time__lte=end_time)

    paginator = Paginator(tasks, page_size)

    try:
        page_obj = paginator.page(page)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=400)

    task_data = [
        {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': task.detect_type,
            'container_id': task.container_id,
            'upload_time': timezone.localtime(task.upload_time).strftime('%Y-%m-%d %H:%M:%S'),
            'status': task.status,
            'failure_reason': task.failure_reason,
            'completion_time': timezone.localtime(task.completion_time).strftime('%Y-%m-%d %H:%M:%S') if task.completion_time else None
        } for task in page_obj.object_list
    ]

    return Response({
        'tasks': task_data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_tasks': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tasks_depr(request):
    # 获取当前用户的所有检测任务
    detection_tasks = DetectionTask.objects.filter(user=request.user)
    task_list = []
    for task in detection_tasks:
        task_list.append({
            "task_id": task.id,
            "task_name": task.task_name,
            "detect_type": task.detect_type,
            "status": task.status,
            "upload_time": timezone.localtime(task.upload_time),
            "completion_time": timezone.localtime(task.completion_time) if task.completion_time else None,
        })
    return Response(task_list)


from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated           # 如需鉴权
from rest_framework.response import Response
from rest_framework import status

from ..models import (
    DetectionTask, ReviewRequest, ManualReview,
    DetectionResult, SubDetectionResult
)

class DetectionTaskDeleteView(APIView):
    """
    按 task_id 删除检测任务及其所有衍生数据
    仅当任务状态为 'completed' 时允许删除
    """
    permission_classes = [IsAuthenticated]     # 可根据需要替换／删去

    def delete(self, request, task_id, *args, **kwargs):
        try:
            task = DetectionTask.objects.get(pk=task_id)
        except DetectionTask.DoesNotExist:
            return Response(
                {"detail": "任务不存在"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 只能删除 status == completed 的任务
        if task.status != "completed":
            return Response(
                {"detail": "检测尚未完成，无法删除"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚠️ 若只允许本人或管理员删除，可在此再做一次权限校验
        # if request.user != task.user and not request.user.is_staff:
        #     return Response({"detail": "无权限"}, status=status.HTTP_403_FORBIDDEN)

        # 原子事务，确保要么全部删掉，要么回滚
        with transaction.atomic():

            # 1) 先删 ReviewRequest 及人工审核链路
            review_qs = ReviewRequest.objects.filter(
                detection_result__detection_task=task
            )
            ManualReview.objects.filter(review_request__in=review_qs).delete()
            review_qs.delete()

            # 2) 删 DetectionResult 及其子结果
            result_qs = DetectionResult.objects.filter(detection_task=task)
            SubDetectionResult.objects.filter(detection_result__in=result_qs).delete()
            result_qs.delete()

            # 3) 剩余对象（ImageUpload 等）全部由 on_delete=CASCADE 自动清理
            task.delete()

        # 成功：204 No Content（REST 删除的经典返回码）
        return Response(status=status.HTTP_204_NO_CONTENT)
