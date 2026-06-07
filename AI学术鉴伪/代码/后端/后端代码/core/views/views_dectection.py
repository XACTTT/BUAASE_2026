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
    LLMAnalysisRun,
    ResourceContainer,
    StructuredDetectionResult,
    SubDetectionResult,
    User,
)
from core.services.material_validation_service import MaterialValidationService
from core.services.content_extraction_service import ContentExtractionService
from core.services.structured_detection_service import StructuredDetectionService
from core.services.permissions import can_access_detection_task
from ..utils.log_utils import action_log, log_action, get_client_ip
from django.db.models import Q
from ..utils.report_generator import (
    generate_detection_task_report,
    generate_text_detection_report,
    generate_structured_detection_report,
)
from ..utils.serializers_safe import serialize_value

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_detection_result(request, image_id):
    try:
        # 获取检测结果
        detection_result = DetectionResult.objects.select_related('detection_task').get(
            image_upload_id=image_id)
        if not can_access_detection_task(request.user, detection_result.detection_task):
            return Response({"message": "Permission denied"}, status=403)

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


from ..tasks_new import fetch_batch, process_text_detection_task, run_structured_detection_task
from ..models import ReviewTextResource, TextDetectionResult


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


def _build_text_resource_from_file(user, file_record, task_type, task_name):
    sections = ContentExtractionService.extract_text_sections_from_file(file_record)
    merged_text = '\n\n'.join(
        str(item.get('text') or '').strip()
        for item in sections
        if str(item.get('text') or '').strip()
    ).strip()

    if not merged_text:
        return None

    container = file_record.container
    if container is None:
        container = ResourceContainer.objects.create(
            organization=user.organization,
            owner=user,
            container_type='paper' if task_type == 'paper_text' else 'review',
            title=task_name or f'{file_record.file_name}-text',
            status='uploaded',
            progress_status='ready',
            submitted_at=timezone.localtime(),
        )
        file_record.container = container
        file_record.save(update_fields=['container'])

    existing = ReviewTextResource.objects.filter(
        container=container,
        source_type='file_parsed',
        raw_text=merged_text,
    ).first()
    if existing:
        return existing

    return ReviewTextResource.objects.create(
        container=container,
        source_type='file_parsed',
        language='zh',
        raw_text=merged_text,
        normalized_text=merged_text,
        token_count=len(merged_text.split()),
        parse_status='parsed',
    )


def _file_has_extractable_text(file_record):
    sections = ContentExtractionService.extract_text_sections_from_file(file_record)
    return any(str(item.get('text') or '').strip() for item in sections)


def _text_file_validation_error(files, material_label):
    invalid_files = [
        file_record.file_name
        for file_record in files
        if not _file_has_extractable_text(file_record)
    ]
    if invalid_files:
        names = '、'.join(invalid_files[:3])
        if len(invalid_files) > 3:
            names += f'等{len(invalid_files)}个文件'
        return f'{names} 未提取到可检测的{material_label}文本，请上传包含正文文本的 PDF、DOCX 或 TXT 文件'
    return None


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
        paper_files = file_queryset
        if not paper_files.exists() and container is not None:
            paper_files = FileManagement.objects.filter(
                container=container,
                resource_role__in=StructuredDetectionService.PAPER_FILE_ROLES,
            ).order_by('id')
        validation_error = _text_file_validation_error(paper_files, '论文')
        if validation_error:
            return Response({"message": validation_error}, status=400)

    if detect_type == 'review':
        has_review_files = file_queryset.exists()
        has_review_texts = bool(review_text_ids)
        if not has_review_files and not has_review_texts and container is None:
            return Response({"message": "No valid review materials found"}, status=400)
        review_files = file_queryset
        if not review_files.exists() and container is not None:
            review_files = FileManagement.objects.filter(
                container=container,
                resource_role__in=StructuredDetectionService.REVIEW_FILE_ROLES,
            ).order_by('id')
        validation_error = _text_file_validation_error(review_files, 'Review')
        if validation_error:
            return Response({"message": validation_error}, status=400)

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

    task_type_map = {'paper': 'paper_text', 'review': 'review_text', 'multi': 'multi_material'}
    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=user,
        container=container,
        task_name=task_name,
        task_type=task_type_map.get(detect_type, detect_type),
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

    log_action(
        user=user,
        operation_type='create_detection_task',
        target_type='DetectionTask',
        target_id=detection_task.id,
        ip=get_client_ip(request),
        detail={
            'task_type': task_type_map.get(detect_type, detect_type),
            'detect_type': detect_type,
            'file_count': len(file_ids),
            'review_text_count': len(review_text_ids),
            'container_id': container.id if container else None,
            'if_use_llm': if_use_llm,
        },
    )

    return Response(
        {
            "message": "Detection request submitted successfully",
            "task_id": detection_task.id,
            "task_name": detection_task.task_name,
            "detect_type": detection_task.detect_type,
        }
    )


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
        return Response({"message": "该用户没有提交检测的权限"}, status=403)

    detect_type = (request.data.get('detect_type') or 'image').strip().lower()

    # 组织鉴伪模型配置校验：检查该组织的检测类型是否可用
    from .views_model_management import get_org_detection_config
    org_config = get_org_detection_config(user.organization_id)
    if detect_type not in org_config or not org_config[detect_type]:
        return Response({'error': f'检测类型 "{detect_type}" 暂未启用，请联系管理员'}, status=400)

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
    container_id = request.data.get('container_id')

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

    container = None
    if container_id:
        container = ResourceContainer.objects.filter(id=container_id, owner=user).first()

    num_images = len(image_uploads)
    quota_error = _check_organization_quota(organization, if_use_llm, num_images)
    if quota_error:
        return quota_error

    # 创建一个新的检测任务
    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=request.user,
        container=container,
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

    log_action(
        user=request.user,
        operation_type='create_detection_task',
        target_type='DetectionTask',
        target_id=detection_task.id,
        ip=get_client_ip(request),
        detail={
            'task_type': 'image',
            'detect_type': 'image',
            'file_count': len(image_ids),
            'mode': mode,
            'if_use_llm': if_use_llm,
        },
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
        return Response({"message": "该用户没有提交检测的权限"}, status=403)

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

    file_ids = []
    if hasattr(request.data, 'getlist'):
        file_ids.extend(_to_int_list(request.data.getlist('file_ids')))
        file_ids.extend(_to_int_list(request.data.getlist('file_id')))
    file_ids.extend(_to_int_list(request.data.get('file_ids')))
    file_ids.extend(_to_int_list(request.data.get('file_id')))
    file_ids = sorted(set(file_ids))

    text_resources_qs = ReviewTextResource.objects.filter(
        id__in=resource_ids,
        container__owner=request.user
    )

    text_resources = list(text_resources_qs.order_by('id'))

    # 兼容当前上传页：前端预览阶段拿到的是 FileManagement.id，
    # 旧实现却把它误当成 resource_ids 传入这里。
    candidate_file_ids = file_ids or resource_ids
    if not text_resources and candidate_file_ids:
        file_queryset = FileManagement.objects.filter(
            id__in=candidate_file_ids,
            user=request.user
        ).order_by('id')

        if not file_queryset.exists():
            return Response({"message": "No valid text resources found"}, status=404)

        generated_resources = []
        for file_record in file_queryset:
            review_text = _build_text_resource_from_file(
                user=request.user,
                file_record=file_record,
                task_type=task_type,
                task_name=task_name,
            )
            if review_text is not None:
                generated_resources.append(review_text)

        if not generated_resources:
            return Response({"message": "No textual content extracted from selected files"}, status=400)

        text_resources = generated_resources

    if not text_resources:
        return Response({"message": "No valid text resources found"}, status=404)

    # 创建检测任务
    detection_task = DetectionTask.objects.create(
        organization=user.organization,
        user=request.user,
        task_name=task_name,
        detect_type='paper' if task_type == 'paper_text' else 'review',
        task_type=task_type,
        status='pending',
        container=text_resources[0].container if text_resources and text_resources[0].container_id else None,
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
            is_review,
            request.data.get('detection_mode', 'fast_detect_gpt'),
        ],
        queue='ai'
    )

    log_action(
        user=request.user,
        operation_type='create_detection_task',
        target_type='detection_task',
        target_id=detection_task.id,
        ip=get_client_ip(request),
        detail={
            'task_type': task_type,
            'detect_type': detection_task.detect_type,
            'text_resource_count': len(text_resources),
            'detection_mode': request.data.get('detection_mode', 'fast_detect_gpt'),
        },
    )

    return Response({
        "message": f"Text detection request ({task_type}) submitted successfully",
        "task_id": detection_task.id,
        "task_name": detection_task.task_name,
        "task_type": detection_task.task_type
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def public_detection_methods(request):
    from .views_model_management import get_org_detection_config, DETECTION_METHODS
    user = request.user
    if user.organization is None:
        return Response({'error': '未绑定组织'}, status=400)
    org_config = get_org_detection_config(user.organization_id)
    return Response({
        'config': org_config,
        'methods': DETECTION_METHODS,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_text_detection_result(request, resource_id):
    """
    获取单个文本资源的检测结果
    """
    try:
        # 获取最新的检测结果
        tdr = TextDetectionResult.objects.select_related('detection_task').filter(
            text_resource_id=resource_id
        ).order_by('-detection_time').first()

        if tdr and can_access_detection_task(request.user, tdr.detection_task):
            if tdr.status == 'in_progress':
                return Response({
                    "resource_id": tdr.text_resource.id,
                    "status": "正在检测中",
                    "message": "大模型文本检测正在进行，请稍等"
                })

            detect_type = _resolve_task_detect_type(tdr.detection_task)
            has_independent_template_metric = detect_type not in {'review', 'multi'}

            # 返回检测已完成的数据
            return Response({
                "resource_id": tdr.text_resource.id,
                "status": "检测已完成",
                "is_fake": tdr.is_fake,
                "confidence_score": tdr.confidence_score,
                "ai_generated_paragraphs": tdr.ai_generated_paragraphs,
                "factual_fake_reason": tdr.factual_fake_reason,
                "template_tendency_score": tdr.template_tendency_score if has_independent_template_metric else None,
                "template_analysis_reason": tdr.template_analysis_reason if has_independent_template_metric else '',
                "review_template_metric_available": has_independent_template_metric,
                "detection_time": timezone.localtime(tdr.detection_time) if tdr.detection_time else None
            })

        # Fallback for structured tasks: no per-resource TextDetectionResult exists,
        # build a response from StructuredDetectionResult + per_section data
        try:
            text_resource = ReviewTextResource.objects.select_related('container').get(id=resource_id)
        except ReviewTextResource.DoesNotExist:
            return Response({"message": "Detection result not found"}, status=404)

        # Find the structured result via the container's detection tasks
        task = DetectionTask.objects.filter(
            container=text_resource.container,
            task_type__in=['paper_text', 'review_text', 'multi_material']
        ).order_by('-created_at').first()
        if not task or not can_access_detection_task(request.user, task):
            return Response({"message": "Detection result not found"}, status=404)

        structured_result = StructuredDetectionResult.objects.filter(detection_task=task).first()
        if not structured_result:
            return Response({"message": "Detection result not found"}, status=404)

        payload = structured_result.result_payload or {}
        per_section = payload.get('evidence', {}).get('per_section', [])
        dimensions = payload.get('dimensions', [])

        # Find sections belonging to this resource
        # Resource index = position in container's review_texts (ordered by id)
        container_texts = list(ReviewTextResource.objects.filter(
            container=text_resource.container
        ).order_by('id').values_list('id', flat=True))
        resource_idx = None
        for idx, rid in enumerate(container_texts):
            if rid == resource_id:
                resource_idx = idx
                break

        if resource_idx is None:
            return Response({"message": "Detection result not found"}, status=404)

        detect_type = _resolve_task_detect_type(task)
        # Sections for this review text resource have item_id: {detect_type}_review_text_{idx}
        matching_sections = [
            s for s in per_section
            if s.get('item_id') == f"{detect_type}_review_text_{resource_idx}"
        ]

        # Build response from structured data
        section = matching_sections[0] if matching_sections else {}
        return Response({
            "resource_id": resource_id,
            "status": "检测已完成",
            "is_fake": section.get('is_aigc', False),
            "confidence_score": section.get('confidence_score', 0),
            "ai_generated_paragraphs": [],
            "factual_fake_reason": '',
            "template_tendency_score": None,
            "template_analysis_reason": '',
            "review_template_metric_available": False,
            "detection_time": timezone.localtime(task.updated_at) if task.updated_at else None
        })

    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=500)


def _resolve_text_result_type(text_resource, task=None):
    container = getattr(text_resource, 'container', None)
    container_type = getattr(container, 'container_type', None)
    if container_type in {'paper', 'review', 'multi_material'}:
        return container_type

    task_type = getattr(task, 'task_type', None)
    if task_type == 'paper_text':
        return 'paper'
    if task_type == 'review_text':
        return 'review'
    return 'unknown'


def _resolve_task_detect_type(task):
    task_type = getattr(task, 'task_type', None)
    if task_type == 'paper_text':
        return 'paper'
    if task_type == 'review_text':
        return 'review'
    if task_type == 'multi_material':
        return 'multi'
    return getattr(task, 'detect_type', None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_text_results(request, task_id):
    """
    获取某个检测任务下所有文本的检测结果列表
    """
    try:
        task = DetectionTask.objects.get(id=task_id)
        if not can_access_detection_task(request.user, task):
            return Response({"message": "Permission denied"}, status=403)

        if task.task_type not in ['paper_text', 'review_text', 'multi_material']:
            if task.detect_type in ('paper', 'review', 'multi', 'multi_material'):
                return Response({
                    "task_id": task.id,
                    "task_name": task.task_name,
                    "task_type": task.task_type,
                    "overall_status": task.status,
                    "results": [],
                })
            return Response({"message": "Not a text-related task"}, status=400)
            
        results = TextDetectionResult.objects.filter(detection_task=task)

        data = []
        for tdr in results:
            data.append({
                "result_id": tdr.id,
                "resource_id": tdr.text_resource.id,
                "text_type": _resolve_text_result_type(tdr.text_resource, task),
                "status": tdr.status,
                "is_fake": tdr.is_fake,
                "confidence_score": tdr.confidence_score,
                "detection_time": timezone.localtime(tdr.detection_time) if tdr.detection_time else None
            })

        # 结构化任务 (paper_text/review_text/multi_material) 结果在 StructuredDetectionResult，
        # 没有逐资源的 TextDetectionResult 记录，需要从容器补充文本资源列表
        if not data and task.task_type in ['paper_text', 'review_text', 'multi_material']:
            from core.models import StructuredDetectionResult, ReviewTextResource
            if StructuredDetectionResult.objects.filter(detection_task=task).exists() and task.container:
                container_texts = ReviewTextResource.objects.filter(container=task.container)
                for txt in container_texts:
                    data.append({
                        "result_id": None,
                        "resource_id": txt.id,
                        "text_type": _resolve_text_result_type(txt, task),
                        "status": task.status,
                        "is_fake": False,
                        "confidence_score": 0,
                        "detection_time": None
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

from ..utils.report_generator import (
    generate_detection_task_report,
    generate_text_detection_report,
    generate_structured_detection_report,
)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_task_report(request, task_id):
    """
    GET /api/tasks/<task_id>/report/
    下载检测报告 PDF
    """
    try:
        task = DetectionTask.objects.get(id=task_id)
        if not can_access_detection_task(request.user, task):
            return Response({"detail": "Permission denied."}, status=403)
        # generate_detection_task_report(task)
    except DetectionTask.DoesNotExist:
        return Response({"detail": "Task not found."}, status=404)

    if task.status not in ["completed", "partially_completed", "failed"]:
        return Response({"detail": "Task not completed yet."}, status=400)

    if not task.report_file:
        # On-demand generation: try to generate the report now
        try:
            if task.task_type == 'image':
                generate_detection_task_report(task)
            elif task.task_type in ('paper_text', 'review_text'):
                generate_text_detection_report(task)
            elif task.task_type == 'multi_material':
                generate_structured_detection_report(task)
            task.refresh_from_db()
        except Exception:
            import logging
            logging.getLogger(__name__).exception("On-demand report generation failed for task %s", task_id)

        if not task.report_file:
            return Response({"detail": "报告生成失败，请稍后重试"}, status=500)

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
    task = get_object_or_404(DetectionTask, id=task_id)
    if not can_access_detection_task(request.user, task):
        return Response({"detail": "Permission denied."}, status=403)

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_llm_analysis(request, task_id):
    """
    GET /api/tasks/<task_id>/llm-analysis/
    返回任务级的大模型分析结果
    """
    task = get_object_or_404(DetectionTask, id=task_id)
    if not can_access_detection_task(request.user, task):
        return Response({'error': 'forbidden'}, status=403)
    extra_payload = task.extra_payload or {}
    structured_result = StructuredDetectionResult.objects.filter(detection_task=task).first()
    structured_payload = structured_result.result_payload if structured_result else {}
    latest_run = LLMAnalysisRun.objects.filter(task=task).order_by('-created_at').first()
    return Response({
        "task_id": task.id,
        "llm_analysis": (
            extra_payload.get("llm_analysis")
            or structured_payload.get("llm_analysis")
            or (latest_run.output_json if latest_run and latest_run.output_json else None)
        ),
        "run": _serialize_llm_analysis_run(latest_run) if latest_run else None,
    })

# 增加两个接口，分别返回造假的图片，和正常的图片；判别方式是detection_result.is_fake
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_fake_task_results(request, task_id):
    """
    ?include_image=1   —— 额外返回原始图像 URL
    """
    task = get_object_or_404(DetectionTask, id=task_id)
    if not can_access_detection_task(request.user, task):
        return Response({'error': 'forbidden'}, status=403)

    include_img = request.query_params.get("include_image", "0") in ("1", "true", "True")
    result_list = []

    for dr in task.detection_results.select_related("image_upload"):
        if dr.status == "completed" and dr.is_fake is True:
            item = {
                "result_id": dr.id,
                "image_id": dr.image_upload.id,
                "file_name": dr.image_upload.file_name or (os.path.basename(dr.image_upload.image.name) if dr.image_upload.image else f"image_{dr.image_upload.id}"),
                "page_number": dr.image_upload.page_number,
                "timestamp": dr.detection_time
            }
            if include_img:
                item["image_url"] = f"/api/preview/image/{dr.image_upload.id}/"
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
    task = get_object_or_404(DetectionTask, id=task_id)
    if not can_access_detection_task(request.user, task):
        return Response({'error': 'forbidden'}, status=403)

    include_img = request.query_params.get("include_image", "0") in ("1", "true", "True")
    result_list = []

    for dr in task.detection_results.select_related("image_upload"):
        if dr.status == "completed" and dr.is_fake is False:
            item = {
                "result_id": dr.id,
                "image_id": dr.image_upload.id,
                "file_name": dr.image_upload.file_name or (os.path.basename(dr.image_upload.image.name) if dr.image_upload.image else f"image_{dr.image_upload.id}"),
                "page_number": dr.image_upload.page_number,
                "timestamp": dr.detection_time
            }
            if include_img:
                item["image_url"] = f"/api/preview/image/{dr.image_upload.id}/"
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
        if obj.mask_image and obj.mask_image.name:
            try:
                from PIL import Image
                import numpy as np
                if np.array(Image.open(obj.mask_image.path).convert('L')).max() == 0:
                    return None
            except Exception:
                pass
            return req.build_absolute_uri(f"/api/preview/sub_result/{obj.id}/")
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
    data = {"result_id": dr.id, "status": dr.status}

    def add(name, value):
        if name in requested:
            data[name] = value

    add("overall", {
        "is_fake": dr.is_fake,
        "confidence_score": dr.confidence_score,
    })
    add("llm",          dr.llm_judgment)
    add("llm_image",    request.build_absolute_uri(f"/api/preview/detection/{dr.id}/?image_type=llm")
                        if dr.llm_image and dr.llm_image.name else None)
    add("ela_image",    request.build_absolute_uri(f"/api/preview/detection/{dr.id}/?image_type=ela")
                        if dr.ela_image and dr.ela_image.name else None)
    add("exif", {
        "photoshop_edited":  dr.exif_photoshop,
        "time_modified":     dr.exif_time_modified,
    })
    add("timestamps",   timezone.localtime(dr.detection_time))
    add("image",        f"/api/preview/image/{dr.image_upload.id}/")

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
    # 通过image_id获取对应的DetectionResult（取最新一条，避免多任务重复时报错）
    dr = DetectionResult.objects.filter(
        image_upload__id=image_id,
    ).order_by('-id').first()
    if dr is None:
        return Response({"message": "Detection result not found for this image"}, status=404)

    # -------- 解析 fields & include_matrix ------------------------------
    raw_fields = request.query_params.get("fields")
    requested = ({f.strip() for f in raw_fields.split(",")} if raw_fields
                 else {"overall", "llm", "ela_image", "llm_image", "exif",
                       "timestamps", "image", "sub_methods"})

    want_matrix = request.query_params.get("include_matrix", "0").lower() in ("1", "true", "yes")

    # -------- 基础信息 ---------------------------------------------------
    data = {"result_id": dr.id, "status": dr.status}

    def add(name, value):
        if name in requested:
            data[name] = value

    add("overall", {
        "is_fake": dr.is_fake,
        "confidence_score": dr.confidence_score,
    })
    add("llm", dr.llm_judgment)
    add("llm_image", request.build_absolute_uri(f"/api/preview/detection/{dr.id}/?image_type=llm")
                     if dr.llm_image and dr.llm_image.name else None)
    add("ela_image", request.build_absolute_uri(f"/api/preview/detection/{dr.id}/?image_type=ela")
                     if dr.ela_image and dr.ela_image.name else None)
    add("exif", {
        "photoshop_edited": dr.exif_photoshop,
        "time_modified": dr.exif_time_modified,
    })
    add("timestamps", dr.detection_time)
    add("image", f"/api/preview/image/{dr.image_upload.id}/")

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


def _serialize_llm_analysis_run(run):
    if not run:
        return None

    model_config = run.model_config
    provider_model = model_config.provider_model if model_config else None
    source = provider_model.source if provider_model else None

    return {
        'id': run.id,
        'stage': run.stage,
        'status': run.status,
        'model': provider_model.model_id if provider_model else None,
        'vendor': source.vendor if source else None,
        'output_json': run.output_json,
        'output_text': run.output_text,
        'error_message': run.error_message,
        'created_at': timezone.localtime(run.created_at) if run.created_at else None,
        'updated_at': timezone.localtime(run.updated_at) if run.updated_at else None,
    }


def _serialize_structured_materials(task, request):
    payload = task.extra_payload or {}
    file_ids = payload.get('file_ids') or []

    file_queryset = FileManagement.objects.none()
    if file_ids:
        file_queryset = FileManagement.objects.filter(id__in=file_ids, user=task.user).order_by('id')
    elif task.container_id:
        file_queryset = FileManagement.objects.filter(container=task.container).order_by('id')

    image_queryset = ImageUpload.objects.none()
    if file_ids:
        image_queryset = ImageUpload.objects.filter(file_management_id__in=file_ids).order_by('id')
    elif task.container_id:
        image_queryset = ImageUpload.objects.filter(container=task.container).order_by('id')

    review_text_queryset = ReviewTextResource.objects.none()
    review_text_ids = payload.get('review_text_ids') or []
    if review_text_ids:
        review_text_queryset = ReviewTextResource.objects.filter(id__in=review_text_ids).order_by('id')
    elif task.container_id:
        review_text_queryset = ReviewTextResource.objects.filter(container=task.container).order_by('id')

    files = [
        {
            'id': item.id,
            'file_name': item.file_name,
            'file_size': item.file_size,
            'file_type': item.file_type,
            'resource_role': item.resource_role,
            'parse_status': item.parse_status,
            'parse_error': item.parse_error,
            'preview_url': f'/api/preview/file/{item.id}/',
            'upload_time': timezone.localtime(item.upload_time) if item.upload_time else None,
        }
        for item in file_queryset
    ]

    images = [
        {
            'id': item.id,
            'file_management_id': item.file_management_id,
            'image_url': f'/api/preview/image/{item.id}/',
            'preview_url': f'/api/preview/image/{item.id}/',
            'image_role': item.image_role,
            'source_kind': item.source_kind,
            'page_number': item.page_number,
            'width': item.width,
            'height': item.height,
        }
        for item in image_queryset
    ]

    review_texts = [
        {
            'id': item.id,
            'source_type': item.source_type,
            'language': item.language,
            'token_count': item.token_count,
            'parse_status': item.parse_status,
            'raw_text': item.raw_text,
            'normalized_text': item.normalized_text,
        }
        for item in review_text_queryset
    ]

    return {
        'files': files,
        'images': images,
        'review_texts': review_texts,
    }


def _serialize_structured_sections(task, payload):
    evidence = payload.get('evidence') or {}
    per_section = evidence.get('per_section') or []
    if not isinstance(per_section, list):
        return []

    text_lookup = {}
    try:
        snapshot = StructuredDetectionService.build_input_snapshot(task)
        text_items = StructuredDetectionService._extract_text_items_from_snapshot(snapshot, task.detect_type)
        text_lookup = {
            item.get('id'): item.get('text')
            for item in text_items
            if item.get('id')
        }
    except Exception:
        text_lookup = {}

    sections = []
    for index, item in enumerate(per_section):
        if not isinstance(item, dict):
            continue
        section = dict(item)
        section['index'] = index
        section['text'] = text_lookup.get(item.get('item_id'))
        sections.append(section)
    return sections


def _serialize_legacy_text_detection_results(task):
    results = TextDetectionResult.objects.filter(detection_task=task).select_related('text_resource')
    return [
        {
            'result_id': item.id,
            'resource_id': item.text_resource_id,
            'text_type': _resolve_text_result_type(item.text_resource, task),
            'status': item.status,
            'is_fake': item.is_fake,
            'confidence_score': item.confidence_score,
            'ai_generated_paragraphs': item.ai_generated_paragraphs,
            'factual_fake_reason': item.factual_fake_reason,
            'template_tendency_score': item.template_tendency_score,
            'template_analysis_reason': item.template_analysis_reason,
            'detection_time': timezone.localtime(item.detection_time) if item.detection_time else None,
        }
        for item in results
    ]


def _serialize_structured_task_result(
    task,
    structured_result,
    payload,
    request,
    include_evidence=True,
    include_materials=True,
    include_llm_runs=True,
):
    overall = payload.get('overall') or {}
    material_summary = payload.get('material_summary') or {}
    llm_analysis = payload.get('llm_analysis')
    ai_response = structured_result.ai_response or {}
    detect_type = _resolve_task_detect_type(task)
    review_template_metric_available = False if detect_type in {'review', 'multi'} else True
    dimensions = payload.get('dimensions') or []

    if detect_type in {'paper', 'review'} and isinstance(dimensions, list):
        per_section = ((payload.get('evidence') or {}).get('per_section') or [])
        section_marker = '_paper_' if detect_type == 'paper' else '_review_'
        matched_sections = [
            section for section in per_section
            if section_marker in str(section.get('item_id') or '')
        ]

        def _clamp_probability(value):
            try:
                return max(0.0, min(1.0, float(value)))
            except (TypeError, ValueError):
                return 0.0

        def _resolve_aigc_probability(section):
            probabilities = section.get('probabilities') or {}
            if probabilities.get('aigc') is not None:
                return _clamp_probability(probabilities.get('aigc'))

            confidence = section.get('confidence_score')
            if confidence is None:
                return 0.0

            confidence = _clamp_probability(confidence)
            if section.get('is_aigc') or section.get('label_name') == 'aigc':
                return confidence
            return 1.0 - confidence

        if matched_sections:
            aigc_scores = [_resolve_aigc_probability(section) for section in matched_sections]
            avg_aigc = sum(aigc_scores) / len(aigc_scores) if aigc_scores else 0.0
            peak_aigc = max(aigc_scores) if aigc_scores else 0.0
            aigc_like_count = sum(1 for score in aigc_scores if score > 0.5)
            aigc_ratio = (
                aigc_like_count / len(aigc_scores)
                if aigc_scores else 0.0
            )

            normalized_dimensions = []
            has_aigc_ratio_dimension = False

            for dim in dimensions:
                name = dim.get('name')
                if detect_type == 'review' and name == 'template_tendency':
                    continue
                if name == 'aigc_generation':
                    normalized_dimensions.append({
                        **dim,
                        'score': round(avg_aigc, 4),
                        'summary': 'BERT AI生成概率（论文全文段落汇总）' if detect_type == 'paper' else 'BERT AI生成概率（评审文本汇总）',
                    })
                    continue
                if name == 'aigc_section_ratio':
                    has_aigc_ratio_dimension = True
                    normalized_dimensions.append({
                        **dim,
                        'score': round(aigc_ratio, 4),
                        'summary': (
                            f'{aigc_like_count}/{len(aigc_scores)} 个段落被分类为AI生成'
                            if detect_type == 'paper'
                            else f'{aigc_like_count}/{len(aigc_scores)} 个评审段落被分类为AI生成'
                        ),
                    })
                    continue
                if name == 'max_section_risk':
                    normalized_dimensions.append({
                        **dim,
                        'score': round(peak_aigc, 4),
                        'summary': '单段落最高AI生成概率',
                    })
                    continue
                if name == 'peak_risk':
                    normalized_dimensions.append({
                        **dim,
                        'score': round(peak_aigc, 4),
                        'summary': '单份评审文本中出现的最高AI生成概率',
                    })
                    continue
                normalized_dimensions.append(dim)

            if detect_type == 'review' and not has_aigc_ratio_dimension:
                normalized_dimensions.insert(1, {
                    'name': 'aigc_section_ratio',
                    'score': round(aigc_ratio, 4),
                    'summary': f'{aigc_like_count}/{len(aigc_scores)} 个评审段落被分类为AI生成',
                })

            dimensions = normalized_dimensions

    response_payload = {
        'task_id': task.id,
        'task_name': task.task_name,
        'detect_type': detect_type,
        'task_type': task.task_type,
        'status': task.status,
        'failure_reason': task.failure_reason,
        'container_id': task.container_id,
        'overall': overall,
        'material_summary': material_summary,
        'dimensions': dimensions,
        'summary': structured_result.summary or payload.get('summary'),
        'confidence_score': structured_result.confidence_score,
        'overall_is_fake': structured_result.overall_is_fake,
        'llm_analysis': llm_analysis,
        'validation': payload.get('validation'),
        'material_cards': payload.get('material_cards') or [],
        'cross_material_analysis': payload.get('cross_material_analysis') or {},
        'ai_contribution': payload.get('ai_contribution') or [],
        'review_template_metric_available': review_template_metric_available,
        'result': payload,
        'ai_response': ai_response,
    }

    # Strip internal-only _relevance_data from the nested result payload
    clean_result = response_payload.get('result')
    if isinstance(clean_result, dict):
        clean_result.pop('_relevance_data', None)

    if include_evidence:
        response_payload['evidence'] = payload.get('evidence') or {}
        response_payload['sections'] = _serialize_structured_sections(task, payload)

    if include_materials:
        response_payload['materials'] = _serialize_structured_materials(task, request)

    if include_llm_runs:
        runs = (
            LLMAnalysisRun.objects.filter(task=task)
            .select_related('model_config', 'model_config__provider_model', 'model_config__provider_model__source')
            .order_by('-created_at')
        )
        response_payload['llm_runs'] = [_serialize_llm_analysis_run(run) for run in runs]

    return response_payload


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def structured_task_result(request, task_id):
    task = get_object_or_404(DetectionTask, id=task_id)
    if not can_access_detection_task(request.user, task):
        return Response({'error': 'forbidden'}, status=403)

    # 优先检查结构化检测结果 — paper/review/multi 走 _submit_structured_detection 的任务
    structured_result = StructuredDetectionResult.objects.filter(detection_task=task).first()
    if structured_result is not None:
        payload = structured_result.result_payload or {}
        include_evidence = request.query_params.get("include_evidence", "1").lower() in ("1", "true", "yes")
        include_materials = request.query_params.get("include_materials", "1").lower() in ("1", "true", "yes")
        include_llm_runs = request.query_params.get("include_llm_runs", "1").lower() in ("1", "true", "yes")
        return Response(_serialize_structured_task_result(
            task=task,
            structured_result=structured_result,
            payload=payload,
            request=request,
            include_evidence=include_evidence,
            include_materials=include_materials,
            include_llm_runs=include_llm_runs,
        ))

    if _resolve_task_detect_type(task) == 'image':
        total_results = task.detection_results.count()
        completed_results = task.detection_results.filter(status='completed').count()
        fake_results = task.detection_results.filter(is_fake=True).count()

        fake_images = []
        normal_images = []
        for dr in task.detection_results.select_related('image_upload'):
            if dr.status != 'completed':
                continue
            entry = {
                'result_id': dr.id,
                'image_id': dr.image_upload.id,
                'file_name': dr.image_upload.file_name or (os.path.basename(dr.image_upload.image.name) if dr.image_upload.image else f"image_{dr.image_upload.id}"),
                'page_number': dr.image_upload.page_number,
                'timestamp': dr.detection_time,
            }
            if request:
                entry['image_url'] = f'/api/preview/image/{dr.image_upload.id}/'
            if dr.is_fake is True:
                fake_images.append(entry)
            else:
                normal_images.append(entry)

        fake_count = len(fake_images)
        total_completed = len(fake_images) + len(normal_images)
        confidence_score = fake_count / total_completed if total_completed > 0 else None

        return Response(
            {
                'task_id': task.id,
                'task_type': task.task_type,
                'detect_type': task.detect_type,
                'status': task.status,
                'task_name': task.task_name,
                'confidence_score': confidence_score,
                'overall_is_fake': fake_count > 0 if total_completed > 0 else None,
                'material_summary': {
                    'image_count': total_results,
                    'completed_count': completed_results,
                    'fake_count': fake_results,
                },
                'result': {
                    'fake_images': fake_images,
                    'normal_images': normal_images,
                },
            }
        )

    # 结构化任务尚未完成（还没有 StructuredDetectionResult 记录）
    if _resolve_task_detect_type(task) in ('paper', 'review', 'multi', 'multi_material'):
        return Response(
            {
                'task_id': task.id,
                'task_name': task.task_name,
                'detect_type': _resolve_task_detect_type(task),
                'task_type': task.task_type,
                'status': task.status,
                'failure_reason': task.failure_reason,
                'container_id': task.container_id,
                'result': {},
                'summary': None,
                'confidence_score': None,
                'overall_is_fake': None,
                'ai_response': {},
                'results': _serialize_legacy_text_detection_results(task),
            }
        )

    # 兜底
    return Response(
        {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': task.detect_type,
            'task_type': task.task_type,
            'status': task.status,
            'failure_reason': task.failure_reason,
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

    # 预取材料信息：按 container 批量查 FileManagement
    container_ids = [task.container_id for task in page_obj.object_list if task.container_id]
    file_map = {}  # container_id -> list of {file_name, tag}
    subject_map = {}  # container_id -> tag (取第一个非空 tag)
    if container_ids:
        from ..models import FileManagement
        files = FileManagement.objects.filter(container_id__in=container_ids).order_by('id').values_list('container_id', 'file_name', 'tag')
        for cid, fname, ftag in files:
            file_map.setdefault(cid, []).append({'file_name': fname, 'tag': ftag})
            if cid not in subject_map and ftag:
                subject_map[cid] = ftag

    task_data = [
        {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': _resolve_task_detect_type(task),
            'task_type': task.task_type,
            'container_id': task.container_id,
            'upload_time': timezone.localtime(task.upload_time).strftime('%Y-%m-%d %H:%M:%S') if task.upload_time else None,
            'status': task.status,
            'failure_reason': task.failure_reason,
            'completion_time': timezone.localtime(task.completion_time).strftime('%Y-%m-%d %H:%M:%S') if task.completion_time else None,
            'subject': subject_map.get(task.container_id, '') if task.container_id else '',
            'materials': [f['file_name'] for f in file_map.get(task.container_id, [])] if task.container_id else [],
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
