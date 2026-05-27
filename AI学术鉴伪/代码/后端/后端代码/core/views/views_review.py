from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status

from ..models import (
    ReviewRequest, ManualReview, DetectionResult, User, DetectionTask,
    PublisherReviewerRelationship, ImageReview, TextReview, ReviewTextResource,
    ImageUpload, Log, StructuredDetectionResult, TextDetectionResult,
)
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..utils.log_utils import action_log, log_action, get_client_ip
from rest_framework.permissions import IsAuthenticated
from core.util import send_notification
from core.models import Notification
from core.services.permissions import can_access_detection_task
from core.services.review_indicator_service import (
    get_review_config, get_review_mode, get_task_type_label, get_task_type_color,
    MATERIAL_REVIEW_CONFIG,
)
from core.utils.avatar_utils import safe_avatar_url as _safe_avatar_url


def _resolve_detection_task(review_request):
    """从 ReviewRequest 解析关联的 DetectionTask，统一处理三种检测路径"""
    detection_task = None

    # 路径0: 直接通过 FK (最直接、最可靠)
    if review_request.detection_task_id:
        detection_task = review_request.detection_task

    # 路径1: 通过 DetectionResult (图像检测)
    if not detection_task and review_request.detection_result:
        detection_task = review_request.detection_result.detection_task
    # 路径2: 通过 TextDetectionResult (旧版文本检测)
    elif not detection_task and review_request.text_detection_result:
        detection_task = review_request.text_detection_result.detection_task

    # 路径3: 结构化检测 (paper/review/multi) 反查
    if not detection_task:
        img = review_request.imgs.first()
        txt = review_request.text_resources.first()
        if img and img.detection_task:
            detection_task = img.detection_task
        elif txt:
            detection_task = DetectionTask.objects.filter(
                extra_payload__review_text_ids__contains=[txt.id]
            ).first()
            if not detection_task and txt.container:
                detection_task = DetectionTask.objects.filter(
                    container=txt.container
                ).first()

    return detection_task


def _resolve_task_type(review_request):
    """从 ReviewRequest 解析标准化 task_type (image/paper_text/review_text/multi_material)"""
    detection_task = _resolve_detection_task(review_request)
    if detection_task:
        return detection_task.task_type or detection_task.detect_type
    return 'unknown'


def _resolve_ai_detection_result(review_request):
    """从 ReviewRequest 解析 AI 检测结果摘要"""
    detection_result = review_request.detection_result
    text_detection_result = review_request.text_detection_result
    detection_task = _resolve_detection_task(review_request)

    result = {}
    if detection_result:
        result = {
            'is_fake': detection_result.is_fake,
            'confidence_score': detection_result.confidence_score,
            'detection_time': detection_result.detection_time.strftime('%Y-%m-%d %H:%M:%S')
            if detection_result.detection_time else None,
        }
    elif text_detection_result:
        result = {
            'is_fake': text_detection_result.is_fake,
            'confidence_score': text_detection_result.confidence_score,
            'detection_time': text_detection_result.detection_time.strftime('%Y-%m-%d %H:%M:%S')
            if text_detection_result.detection_time else None,
        }
    elif detection_task:
        try:
            sdr = StructuredDetectionResult.objects.get(detection_task=detection_task)
            overall = (sdr.result_payload or {}).get('overall', {})
            result = {
                'is_fake': overall.get('is_fake', False),
                'confidence_score': overall.get('confidence_score', 0),
                'detection_time': sdr.created_at.strftime('%Y-%m-%d %H:%M:%S')
                if sdr.created_at else None,
            }
        except StructuredDetectionResult.DoesNotExist:
            pass

    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reviewers_in_org(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view all reviewers'}, status=403)

    # 获取查询参数
    query = request.query_params.get('query', '')

    # 构建查询条件
    reviewers = User.objects.filter(
        organization=user.organization,
        role='reviewer'
    )
    if query:
        reviewers = reviewers.filter(username__startswith=query)

    # 筛选具有审核权限的 reviewer
    filtered_reviewers = []
    for reviewer in reviewers:
        if reviewer.has_permission('review'):
            filtered_reviewers.append({
                'id': reviewer.id,
                'username': reviewer.username,
                'avatar': _safe_avatar_url(reviewer),
            })

    return Response(filtered_reviewers)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviewers_for_publisher(request, publisher_id):
    """获取指定Publisher所在组织下的所有reviewer"""
    try:
        publisher = User.objects.get(id=publisher_id, role='publisher')
    except User.DoesNotExist:
        return Response({'error': 'Publisher not found'}, status=404)

    # 获取该 publisher 所属组织
    organization = publisher.organization
    if not organization:
        return Response({'error': 'Publisher does not belong to any organization'}, status=400)

    # 获取该组织下所有 role 为 reviewer 的用户，并且有 review 权限
    reviewers = User.objects.filter(
        organization=organization,
        role='reviewer',
        is_active=True
    )

    # 序列化数据返回
    reviewer_list = [{
        'id': user.id,
        'username': user.username,
        'avatar': _safe_avatar_url(user),
    } for user in reviewers]

    return Response({
        'publisher_id': publisher_id,
        'reviewers': reviewer_list
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@action_log('audit_submit', target_type='ReviewRequest', target_id_field='review_request_id')
def create_review_task_with_admin_check(request):
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if not user.has_permission('publish'):
        return Response({"错误": "该用户没有发布的权限"}, status=403)

    if user.role != 'publisher':
        return Response({'error': 'Only publishers can create review tasks'}, status=403)

    image_ids = request.data.get('image_ids', [])
    text_ids = request.data.get('text_ids', [])
    task_id = request.data.get('task_id', None)
    reviewers = request.data.get('reviewers', [])
    reason = request.data.get('reason', 'No reason provided')
    selected_section_ids = request.data.get('selected_section_ids', [])

    try:
        # 如果提供了 task_id，自动从 DetectionTask 中补全缺失的 image_ids 和 text_ids
        if task_id:
            try:
                det_task = DetectionTask.objects.get(id=task_id, user=request.user)
            except DetectionTask.DoesNotExist:
                return Response({'error': 'DetectionTask not found'}, status=404)

            # --- 自动补全 image_ids ---
            if not image_ids:
                image_ids = list(det_task.image_uploads.values_list('id', flat=True))
                if not image_ids:
                    image_ids = list(
                        DetectionResult.objects.filter(detection_task=det_task)
                        .values_list('image_upload_id', flat=True)
                    )
                if not image_ids and det_task.container:
                    image_ids = list(det_task.container.images.values_list('id', flat=True))

            # --- 自动补全 text_ids ---
            if not text_ids:
                text_ids = list(
                    TextDetectionResult.objects.filter(
                        detection_task=det_task
                    ).values_list('text_resource_id', flat=True)
                )
                if not text_ids and det_task.extra_payload:
                    raw_ids = det_task.extra_payload.get('review_text_ids') or []
                    if raw_ids:
                        text_ids = [int(x) for x in raw_ids if str(x).isdigit()]
                if not text_ids and det_task.container:
                    text_ids = list(det_task.container.review_texts.values_list('id', flat=True))

            # --- 结构化检测任务 (paper_text/review_text/multi_material) 回退 ---
            if not image_ids and not text_ids:
                if StructuredDetectionResult.objects.filter(detection_task=det_task).exists():
                    if det_task.container:
                        image_ids = list(det_task.container.images.values_list('id', flat=True))
                        text_ids = list(det_task.container.review_texts.values_list('id', flat=True))

        # 验证参数
        if not image_ids and not text_ids:
            return Response({'error': 'image_ids or text_ids is required'}, status=400)
        if not reviewers:
            return Response({'error': 'reviewers is required'}, status=400)

        images = []
        texts = []
        
        # 获取图片对象
        if image_ids:
            images = ImageUpload.objects.filter(id__in=image_ids)
            if len(images) != len(image_ids):
                return Response({'error': 'Some image IDs do not exist'}, status=404)
                
        # 获取文本对象
        if text_ids:
            from core.models import ReviewTextResource
            texts = ReviewTextResource.objects.filter(id__in=text_ids)
            if len(texts) != len(text_ids):
                return Response({'error': 'Some text IDs do not exist'}, status=404)

        # 获取审核员对象
        reviewer_users = User.objects.filter(organization=user.organization, id__in=reviewers, role='reviewer')
        if len(reviewer_users) != len(reviewers):
            return Response({'error': 'Some reviewer IDs do not exist or are not reviewers'}, status=404)

        detection_result = None
        text_detection_result = None

        if images:
            detection_result = images[0].detection_results.first()
        if texts:
            text_detection_result = texts[0].detection_results.first()

        # 结构化检测任务（paper/review/multi）使用 StructuredDetectionResult，
        # 不会有逐资源的 DetectionResult / TextDetectionResult
        if not detection_result and not text_detection_result:
            if task_id:
                if not StructuredDetectionResult.objects.filter(detection_task_id=task_id).exists():
                    return Response({'error': 'No detection result found for the provided resources'}, status=404)
            else:
                return Response({'error': 'No detection result found for the provided resources'}, status=404)

        # 创建审核请求，状态设为pending
        review_request = ReviewRequest.objects.create(
            detection_result=detection_result,
            text_detection_result=text_detection_result,
            detection_task=DetectionTask.objects.filter(id=task_id).first() if task_id else None,
            user=request.user,
            reason=reason,
            organization=user.organization,
            selected_section_ids=selected_section_ids if isinstance(selected_section_ids, list) else [],
        )

        if images:
            review_request.imgs.add(*images)
        if texts:
            review_request.text_resources.add(*texts)
        # 添加审核人员
        for reviewer in reviewer_users:
            review_request.reviewers.add(reviewer)

        # 记录创建审核请求日志
        # 推导 task_type：优先从关联的 DetectionTask 获取
        task_type = None
        if task_id:
            try:
                det_task = DetectionTask.objects.get(id=task_id)
                task_type = det_task.task_type or det_task.detect_type
            except DetectionTask.DoesNotExist:
                pass
        elif detection_result:
            task_type = 'image'
        elif text_detection_result:
            task_type = 'text'

        image_count = len(image_ids)
        text_count = len(text_ids)
        if image_count > 0 and text_count > 0:
            material_type = 'mixed'
        elif image_count > 0:
            material_type = 'image'
        else:
            material_type = 'text'

        log_action(
            user=request.user,
            operation_type='create_review_request',
            target_type='review_request',
            target_id=review_request.id,
            ip=get_client_ip(request),
            detail={
                'task_type': task_type,
                'reviewer_count': len(reviewers),
                'material_type': material_type,
                'image_count': image_count,
                'text_count': text_count,
            },
        )

        # 通知管理员进行检查
        organization = user.organization
        if organization and organization.admin_user:
            admin_email = organization.admin_user.email
        else:
            return Response({'error': 'Organization or admin user not found'}, status=404)

        send_mail(
            '新的审核任务',
            '您有一个新的审核任务需要审核，请登录系统进行处理。',
            '2406854677@qq.com',
            [admin_email],
            fail_silently=True,
        )

        return Response(
            {'message': 'Review task created and sent to admin for approval', 'review_request_id': review_request.id},
            status=201
        )

    except ObjectDoesNotExist as e:
        return Response({'error': 'Resource not found'}, status=404)

    except Exception as e:
        return Response({'error': f'Server error: {str(e)}'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_img_review_all(request):
    """
    用于publisher获取指定ReviewRequest的可指定图片的**整体**审核结果
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task details'}, status=403)

    review_request_id = request.query_params.get('review_request_id', '')
    img_id = request.query_params.get('img_id', '')

    if not review_request_id:
        return Response({'error': 'review_request_id is required'}, status=400)
    if not img_id:
        return Response({'error': 'img_id is required'}, status=400)

    try:
        # 获取ReviewRequest对象
        review_request = ReviewRequest.objects.get(id=review_request_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    # 获取所有状态为completed的ManualReview对象
    manual_reviews = ManualReview.objects.filter(
        review_request=review_request,
        status='completed',
        imgs__id=img_id
    ).distinct()

    reviewers_results = []

    for manual_review in manual_reviews:
        reviewer = manual_review.reviewer
        # 获取相关的ImageReview对象
        image_reviews = ImageReview.objects.filter(
            manual_review=manual_review,
            img_id=img_id
        )

        for image_review in image_reviews:
            reviewers_results.append({
                'id': reviewer.id,
                'username': reviewer.username,
                'avatar': _safe_avatar_url(reviewer),
                'result': image_review.result  # 0/1 表示人工审核的结果是真还是假
            })

    return Response({
        'reviewers_results': reviewers_results
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_text_review_all(request):
    """
    用于publisher获取指定ReviewRequest的可指定文本的**整体**审核结果
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task details'}, status=403)

    review_request_id = request.query_params.get('review_request_id', '')
    text_id = request.query_params.get('text_id', '')

    if not review_request_id:
        return Response({'error': 'review_request_id is required'}, status=400)
    if not text_id:
        return Response({'error': 'text_id is required'}, status=400)

    try:
        review_request = ReviewRequest.objects.get(id=review_request_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    manual_reviews = ManualReview.objects.filter(
        review_request=review_request,
        status='completed',
        text_resources__id=text_id
    ).distinct()

    reviewers_results = []

    for manual_review in manual_reviews:
        reviewer = manual_review.reviewer
        from core.models import TextReview
        text_reviews = TextReview.objects.filter(
            manual_review=manual_review,
            text_resource_id=text_id
        )

        for tr in text_reviews:
            reviewers_results.append({
                'id': reviewer.id,
                'username': reviewer.username,
                'avatar': _safe_avatar_url(reviewer),
                'result': tr.result
            })

    return Response({
        'reviewers_results': reviewers_results
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image_review(request):
    """
    用于publisher获取指定ReviewRequest的可指定图片的**单个详细**审核结果
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task details'}, status=403)

    review_request_id = request.query_params.get('review_request_id', '')
    img_id = request.query_params.get('img_id', '')
    reviewer_id = request.query_params.get('reviewer_id', '')

    if not review_request_id:
        return Response({'error': 'review_request_id is required'}, status=400)
    if not img_id:
        return Response({'error': 'img_id is required'}, status=400)
    if not reviewer_id:
        return Response({'error': 'reviewer_id is required'}, status=400)

    try:
        # 获取ReviewRequest对象
        review_request = ReviewRequest.objects.get(id=review_request_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    try:
        # 获取ManualReview对象
        manual_review = ManualReview.objects.get(
            review_request=review_request,
            reviewer_id=reviewer_id,
            imgs__id=img_id
        )
    except ManualReview.DoesNotExist:
        return Response({'error': 'ManualReview not found'}, status=404)

    try:
        # 获取ImageReview对象
        image_review = ImageReview.objects.get(
            manual_review=manual_review,
            img_id=img_id
        )
    except ImageReview.DoesNotExist:
        return Response({'error': 'ImageReview not found'}, status=404)

    scores = [
        image_review.score1,
        image_review.score2,
        image_review.score3,
        image_review.score4,
        image_review.score5,
        image_review.score6,
        image_review.score7
    ]

    reasons = [
        image_review.reason1,
        image_review.reason2,
        image_review.reason3,
        image_review.reason4,
        image_review.reason5,
        image_review.reason6,
        image_review.reason7
    ]

    points = [
        image_review.points1,
        image_review.points2,
        image_review.points3,
        image_review.points4,
        image_review.points5,
        image_review.points6,
        image_review.points7
    ]

    result = image_review.result

    return Response({
        'scores': scores,
        'reasons': reasons,
        'points': points,
        'result': result
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_text_review(request):
    """
    用于publisher获取指定ReviewRequest的可指定文本的**单个详细**审核结果
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task details'}, status=403)

    review_request_id = request.query_params.get('review_request_id', '')
    text_id = request.query_params.get('text_id', '')
    reviewer_id = request.query_params.get('reviewer_id', '')

    if not review_request_id or not text_id or not reviewer_id:
        return Response({'error': 'Missing parameters'}, status=400)

    try:
        review_request = ReviewRequest.objects.get(id=review_request_id)
        manual_review = ManualReview.objects.get(
            review_request=review_request,
            reviewer_id=reviewer_id,
            text_resources__id=text_id
        )
        from core.models import TextReview
        text_review = TextReview.objects.get(
            manual_review=manual_review,
            text_resource_id=text_id
        )
    except (ReviewRequest.DoesNotExist, ManualReview.DoesNotExist, TextReview.DoesNotExist):
        return Response({'error': 'Resource not found'}, status=404)

    return Response({
        'overall_comment': text_review.overall_comment,
        'paragraph_reviews': text_review.paragraph_reviews,
        'template_review_score': text_review.template_review_score,
        'template_review_comment': text_review.template_review_comment,
        'result': text_review.result
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_request_completion_status(request, task_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task completion status'}, status=403)

    try:
        detection_task = DetectionTask.objects.get(id=task_id)
    except DetectionTask.DoesNotExist:
        return Response({'error': 'Task not found'}, status=404)

    review_requests = []
    
    # 获取所有图片和文本检测结果关联的审查请求
    if detection_task.detect_type == 'image' or detection_task.detect_type == 'multi':
        for result in detection_task.detection_results.all():
            review_requests.extend(list(result.review_requests.all()))
            
    if detection_task.detect_type != 'image':
        for result in detection_task.text_detection_results.all():
            review_requests.extend(list(result.review_requests.all()))
            
    # 去重
    review_requests = list(set(review_requests))
    
    total_reviewers = len(review_requests)
    completed_reviewers = sum(1 for r in review_requests if r.status1 == 'completed')

    completion_percentage = (completed_reviewers / total_reviewers) * 100 if total_reviewers > 0 else 0

    return Response({
        'task_id': task_id,
        'completion_percentage': completion_percentage
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_request_detail(request, reviewRequest_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view task details'}, status=403)

    try:
        # 获取ReviewRequest对象
        review_request = ReviewRequest.objects.get(id=reviewRequest_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    # 解析关联的 DetectionTask 和 task_type
    detection_task = _resolve_detection_task(review_request)
    task_type = _resolve_task_type(review_request)

    if not detection_task and not review_request.detection_result and not review_request.text_detection_result:
        return Response({'error': 'No detection result found for the review request'}, status=404)

    # 获取图片列表
    images = []
    for img in review_request.imgs.all():
        images.append({
            'img_id': img.id,
            'img_url': img.image.url,
        })

    # 获取文本信息
    texts = []
    for text in review_request.text_resources.all():
        texts.append({
            'text_id': text.id,
            'raw_text': text.raw_text[:200] + '...' if len(text.raw_text) > 200 else text.raw_text,
            'source_type': text.source_type,
        })

    # 解析AI检测结果
    ai_detection_result = _resolve_ai_detection_result(review_request)

    # 获取审核员检测结果
    manual_reviews = ManualReview.objects.filter(review_request=review_request)

    # 计算状态
    total_reviewers = review_request.reviewers.count()
    completed_reviews_count = manual_reviews.filter(status='completed').count()
    review_status = {
        'done': completed_reviews_count,
        'process': total_reviewers - completed_reviews_count
    }

    # 获取审核配置
    review_config = get_review_config(task_type)

    return Response({
        'images': images,
        'texts': texts,
        'ai_detection_result': ai_detection_result,
        'status': review_status,
        'task_type': task_type,
        'task_type_label': get_task_type_label(task_type),
        'task_id': detection_task.id if detection_task else None,
        'review_config': review_config,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_publisher_review_tasks(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'publisher':
        return Response({'error': 'Only publishers can view their review tasks'}, status=403)

    # 获取查询参数
    status = request.query_params.get('status', '')
    start_time = request.query_params.get('startTime', None)
    end_time = request.query_params.get('endTime', None)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    # 构建查询条件
    review_requests = ReviewRequest.objects.filter(user=user).select_related(
        'detection_result__detection_task').prefetch_related('reviewers', 'manual_reviews')
    review_requests = review_requests.order_by('-request_time')

    if status:
        review_requests = review_requests.filter(status1=status)
    if start_time:
        review_requests = review_requests.filter(request_time__gte=start_time)
    if end_time:
        review_requests = review_requests.filter(request_time__lte=end_time)

    # 分页
    paginator = Paginator(review_requests, page_size)
    try:
        page_obj = paginator.page(page)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

    # 构建返回数据
    tasks = []
    for review_request in page_obj.object_list:
        reviewers_count = review_request.reviewers.count()
        completed_reviews_count = review_request.manual_reviews.filter(status='completed').count()
        progress = f"{completed_reviews_count}/{reviewers_count}"

        # 计算状态逻辑：根据 status2 决定显示哪个状态
        if review_request.status2 == 'accepted':
            display_status = review_request.status1  # 使用 status1
        else:
            display_status = review_request.status2  # 使用 status2

        task_type = _resolve_task_type(review_request)
        tasks.append({
            'review_request_id': review_request.id,
            'request_time': review_request.request_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': display_status,  # 动态选择状态
            'status1': review_request.status1,
            'status2': review_request.status2,
            'progress': progress,
            'task_type': task_type,
            'task_type_label': get_task_type_label(task_type),
        })

    return Response({
        'tasks': tasks,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviewer_request_detail(request, reviewRequest_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'reviewer':
        return Response({'error': 'Only reviewers can view task details'}, status=403)

    try:
        review_request = ReviewRequest.objects.get(id=reviewRequest_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    # 解析 DetectionTask 和 task_type
    detection_task = _resolve_detection_task(review_request)
    task_type = _resolve_task_type(review_request)

    if not detection_task and not review_request.detection_result and not review_request.text_detection_result:
        return Response({'error': 'No detection result found for the review request'}, status=404)

    # 获取图片列表
    image_uploads = review_request.imgs.all()
    image_ids = [img.id for img in image_uploads]
    image_urls = [img.image.url for img in image_uploads]

    # 获取文本列表
    text_resources = review_request.text_resources.all()
    text_ids = [text.id for text in text_resources]
    text_previews = [text.raw_text[:200] + '...' if len(text.raw_text) > 200 else text.raw_text for text in text_resources]

    # 解析AI检测结果
    ai_detection_result = _resolve_ai_detection_result(review_request)

    # 获取审核配置
    review_config = get_review_config(task_type)

    return Response({
        'image_ids': image_ids,
        'image_urls': image_urls,
        'text_ids': text_ids,
        'text_previews': text_previews,
        'ai_detection_result': ai_detection_result,
        'status': review_request.status1,
        'status2': review_request.status2,
        'task_type': task_type,
        'task_type_label': get_task_type_label(task_type),
        'review_config': review_config,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviewer_manual_request(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'reviewer':
        return Response({'error': 'Only reviewers can view tasks'}, status=403)

    # 获取查询参数
    status = request.query_params.get('status', '')
    query = request.query_params.get('query', '')
    start_time = request.query_params.get('start_time', None)
    end_time = request.query_params.get('end_time', None)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    # 确保 page_size 不超过 100
    if page_size > 100:
        page_size = 100

    # 构建查询条件 - 基于ManualReview查询，避免分页后再过滤
    manual_reviews_qs = ManualReview.objects.filter(
        reviewer=user
    ).select_related(
        'review_request',
        'review_request__user',
        'review_request__detection_result__detection_task',
        'review_request__text_detection_result__detection_task',
    ).order_by('-review_request__request_time')

    if status:
        manual_reviews_qs = manual_reviews_qs.filter(status=status)
    if query:
        manual_reviews_qs = manual_reviews_qs.filter(review_request__user__username__startswith=query)
    if start_time:
        manual_reviews_qs = manual_reviews_qs.filter(review_request__request_time__gte=start_time)
    if end_time:
        manual_reviews_qs = manual_reviews_qs.filter(review_request__request_time__lte=end_time)

    # 分页 - 在过滤后分页，确保总数匹配
    paginator = Paginator(manual_reviews_qs, page_size)
    try:
        page_obj = paginator.page(page)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=400)

    # 构建返回数据
    results = []
    for manual_review in page_obj.object_list:
        review_request = manual_review.review_request
        publisher = review_request.user
        image_count = review_request.imgs.count()
        task_type = _resolve_task_type(review_request)

        results.append({
            'manual_review_id': manual_review.id,
            'manual_review_time': manual_review.review_time.strftime('%Y-%m-%d %H:%M:%S')
            if manual_review.review_time else None,
            'publisher_username': publisher.username,
            'publisher_avatar': _safe_avatar_url(publisher),
            'image_count': image_count,
            'status': manual_review.status,
            'task_type': task_type,
            'task_type_label': get_task_type_label(task_type),
            'task_type_color': get_task_type_color(task_type),
        })

    return Response({
        'results': results,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_review_detail(request, manual_review_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'reviewer':
        return Response({'error': 'Only reviewers can view review details'}, status=403)

    try:
        manual_review = ManualReview.objects.get(id=manual_review_id, reviewer=user)
    except ManualReview.DoesNotExist:
        return Response({'error': 'ManualReview not found'}, status=404)

    # 获取关联的ReviewRequest
    review_request = manual_review.review_request

    # 解析 task_type 和审核配置
    task_type = _resolve_task_type(review_request)
    review_config = get_review_config(task_type)

    # 获取图片列表
    image_ids = [img.id for img in manual_review.imgs.all()]
    image_urls = [img.image.url for img in manual_review.imgs.all()]

    # 获取文本列表(返回完整内容供审核使用)
    texts = []
    # 预加载结构化检测结果用于文本AI检测数据
    per_section_list = []
    overall_ai = {}
    detection_task_for_text = _resolve_detection_task(review_request)
    if detection_task_for_text:
        try:
            sdr_for_text = StructuredDetectionResult.objects.get(detection_task=detection_task_for_text)
            payload_for_text = sdr_for_text.result_payload or {}
            evidence_for_text = payload_for_text.get('evidence') or {}
            per_section_list = evidence_for_text.get('per_section') or []
            overall_ai = payload_for_text.get('overall') or {}
        except StructuredDetectionResult.DoesNotExist:
            pass

    for text in manual_review.text_resources.all():
        ai_detection = None
        # 尝试从 TextDetectionResult 获取 AI 检测数据
        text_det = TextDetectionResult.objects.filter(
            detection_task=detection_task_for_text,
            text_resource_id=text.id,
        ).first() if detection_task_for_text else None
        if text_det:
            ai_detection = {
                'is_fake': text_det.is_fake,
                'confidence_score': text_det.confidence_score,
                'ai_generated_paragraphs': text_det.ai_generated_paragraphs or [],
                'factual_fake_reason': getattr(text_det, 'factual_fake_reason', ''),
                'template_tendency_score': getattr(text_det, 'template_tendency_score', None),
                'template_analysis_reason': getattr(text_det, 'template_analysis_reason', ''),
            }
        elif per_section_list:
            # 结构化检测: 聚合所有 per_section 数据为单个 AI 检测结果
            all_high_risk = []
            for sec in per_section_list:
                paragraphs = sec.get('paragraphs') or []
                for idx, p in enumerate(paragraphs):
                    if p.get('ai_probability', 0) > 0.5:
                        all_high_risk.append({
                            'paragraph_index': p.get('paragraph_index', p.get('index', idx)),
                            'ai_probability': p.get('ai_probability', 0),
                            'text': p.get('text', ''),
                            'reason': p.get('reason', ''),
                        })
            ai_detection = {
                'is_fake': overall_ai.get('is_fake'),
                'confidence_score': overall_ai.get('confidence_score'),
                'ai_generated_paragraphs': all_high_risk,
                'factual_fake_reason': overall_ai.get('reason', ''),
                'template_tendency_score': None,
                'template_analysis_reason': '',
            }
        texts.append({
            'text_id': text.id,
            'raw_text': text.raw_text,
            'source_type': text.source_type,
            'ai_detection': ai_detection,
        })

    # 解析AI检测结果
    ai_detection_result = _resolve_ai_detection_result(review_request)

    # 获取已有图片审核结果
    image_review_results = []
    for image_review in manual_review.img_reviews.all():
        scores = [
            image_review.score1, image_review.score2, image_review.score3,
            image_review.score4, image_review.score5, image_review.score6,
            image_review.score7
        ]
        reasons = [
            image_review.reason1, image_review.reason2, image_review.reason3,
            image_review.reason4, image_review.reason5, image_review.reason6,
            image_review.reason7
        ]
        points = [
            image_review.points1, image_review.points2, image_review.points3,
            image_review.points4, image_review.points5, image_review.points6,
            image_review.points7
        ]
        image_review_results.append({
            'image_id': image_review.img.id,
            'scores': scores,
            'reasons': reasons,
            'points': points,
            'result': image_review.result
        })

    # 获取已有文本审核结果
    text_review_results = []
    for text_review in manual_review.text_reviews.all():
        text_review_results.append({
            'text_id': text_review.text_resource.id,
            'paragraph_reviews': text_review.paragraph_reviews,
            'template_review_score': text_review.template_review_score,
            'template_review_comment': text_review.template_review_comment,
            'overall_comment': text_review.overall_comment,
            'result': text_review.result
        })

    # 获取结构化检测结果(文本AI详细数据)
    structured_result = {}
    detection_task = _resolve_detection_task(review_request)
    if detection_task:
        try:
            sdr = StructuredDetectionResult.objects.get(detection_task=detection_task)
            structured_result = sdr.result_payload or {}
        except StructuredDetectionResult.DoesNotExist:
            pass

    # 获取图像子检测结果(7维度)
    sub_detection_results = {}
    if review_request.detection_result:
        for sub in review_request.detection_result.sub_results.all():
            sub_detection_results[sub.image_id] = {
                'method': sub.method_name,
                'probability': float(sub.probability) if sub.probability else 0,
                'mask_url': sub.mask_image.url if sub.mask_image else None,
            }

    return Response({
        'image_ids': image_ids,
        'image_urls': image_urls,
        'texts': texts,
        'ai_detection_result': ai_detection_result,
        'image_reviews': image_review_results,
        'text_reviews': text_review_results,
        'structured_result': structured_result,
        'sub_detection_results': sub_detection_results,
        'task_type': task_type,
        'task_type_label': get_task_type_label(task_type),
        'review_config': review_config,
        'status': manual_review.status,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_manualReview_from_reviewRequestId(request, review_request_id):
    user = request.user

    try:
        # 获取对应的 ReviewRequest
        review_request = ReviewRequest.objects.get(id=review_request_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=status.HTTP_404_NOT_FOUND)

    # 获取所有关联的 ManualReview
    manual_reviews = ManualReview.objects.filter(review_request=review_request).select_related('reviewer')

    if not manual_reviews.exists():
        return Response({'message': 'No manual reviews found for this request'}, status=status.HTTP_404_NOT_FOUND)

    # 构造响应数据
    data = []
    for manual_review in manual_reviews:
        reviewers_results = []

        # 获取该 ManualReview 对应的 ImageReview 数据
        image_reviews = manual_review.image_reviews.all()
        for image_review in image_reviews:
            reviewers_results.append({
                'img_id': image_review.img.id,
                'result': image_review.result,
                'review_time': image_review.review_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if image_review.review_time else None
            })

        # 获取该 ManualReview 对应的 TextReview 数据
        text_reviews_data = []
        for text_review in manual_review.text_reviews.all():
            text_reviews_data.append({
                'text_id': text_review.text_resource.id,
                'result': text_review.result,
                'overall_comment': text_review.overall_comment,
                'review_time': text_review.review_time.strftime(
                    '%Y-%m-%d %H:%M:%S') if text_review.review_time else None
            })

        data.append({
            'manual_review_id': manual_review.id,
            'review_request_id': manual_review.review_request.id,
            'reviewer': {
                'id': manual_review.reviewer.id,
                'username': manual_review.reviewer.username,
                'avatar': _safe_avatar_url(manual_review.reviewer),
            },
            'status': manual_review.status,
            'review_time': manual_review.review_time.strftime(
                '%Y-%m-%d %H:%M:%S') if manual_review.review_time else None,
            'image_reviews': reviewers_results,
            'text_reviews': text_reviews_data,
            'report_file': manual_review.report_file.url if manual_review.report_file else None
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@action_log('audit_op', target_type='ManualReview', target_id_field='manual_review_id')
def post_review(request, manual_review_id):
    """
    reviewer提交审核结果
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if not user.has_permission('review'):
        return Response({"错误": "该用户没有审核的权限"}, status=403)

    if user.role != 'reviewer':
        return Response({'error': 'Only reviewers can submit reviews'}, status=403)

    try:
        # 获取ManualReview对象
        manual_review = ManualReview.objects.get(id=manual_review_id, reviewer=user)
    except ManualReview.DoesNotExist:
        return Response({'error': 'ManualReview not found'}, status=404)

    # 获取请求体数据
    data = request.data
    results = data.get('result', [])
    text_reviews_data = data.get('text_reviews', [])

    if not results and not text_reviews_data:
        return Response({'error': 'result or text_reviews is required'}, status=400)

    with transaction.atomic():
        # 处理图片审核结果
        for item in results:
            img_id = item.get('img_id')
            scores = item.get('score', [])
            reasons = item.get('reason', [])
            points_list = item.get('points', [])
            final_result = item.get('final')

            if not img_id:
                return Response({'error': 'img_id is required in each result item'}, status=400)
            if len(scores) != 7:
                return Response({'error': 'scores must contain exactly 7 elements'}, status=400)
            if len(reasons) != 7:
                return Response({'error': 'reasons must contain exactly 7 elements'}, status=400)
            if len(points_list) != 7:
                return Response({'error': 'points must contain exactly 7 elements (one for each method)'}, status=400)
            if final_result is None:
                return Response({'error': 'final is required in each result item'}, status=400)

            try:
                image_upload = ImageUpload.objects.get(id=img_id)
            except ImageUpload.DoesNotExist:
                return Response({'error': f'Image with ID {img_id} not found'}, status=404)

            ImageReview.objects.update_or_create(
                manual_review=manual_review,
                img=image_upload,
                defaults={
                    'score1': scores[0], 'score2': scores[1], 'score3': scores[2],
                    'score4': scores[3], 'score5': scores[4], 'score6': scores[5],
                    'score7': scores[6],
                    'reason1': reasons[0], 'reason2': reasons[1], 'reason3': reasons[2],
                    'reason4': reasons[3], 'reason5': reasons[4], 'reason6': reasons[5],
                    'reason7': reasons[6],
                    'points1': points_list[0], 'points2': points_list[1], 'points3': points_list[2],
                    'points4': points_list[3], 'points5': points_list[4], 'points6': points_list[5],
                    'points7': points_list[6],
                    'result': final_result,
                    'review_time': timezone.now()
                }
            )

            image_upload.isReview = True
            image_upload.save(update_fields=['isReview'])

        # 处理文本审核结果
        for item in text_reviews_data:
            text_id = item.get('text_id')
            paragraph_reviews = item.get('paragraph_reviews', None)
            template_review_score = item.get('template_review_score', None)
            template_review_comment = item.get('template_review_comment', None)
            overall_comment = item.get('overall_comment', '')
            final_result = item.get('result')

            if not text_id:
                return Response({'error': 'text_id is required in each text_review item'}, status=400)
            if final_result is None:
                return Response({'error': 'result is required in each text_review item'}, status=400)

            try:
                text_resource = ReviewTextResource.objects.get(id=text_id)
            except ReviewTextResource.DoesNotExist:
                return Response({'error': f'Text resource with ID {text_id} not found'}, status=404)

            TextReview.objects.update_or_create(
                manual_review=manual_review,
                text_resource=text_resource,
                defaults={
                    'paragraph_reviews': paragraph_reviews,
                    'template_review_score': template_review_score,
                    'template_review_comment': template_review_comment,
                    'overall_comment': overall_comment,
                    'result': final_result,
                    'review_time': timezone.now()
                }
            )

        # 更新ManualReview状态
        manual_review.status = 'completed'
        manual_review.save()

        # 更新ReviewRequest状态
        review_request = manual_review.review_request
        if review_request.manual_reviews.filter(status='completed').count() == review_request.reviewers.count():
            review_request.status1 = 'completed'
            review_request.review_end_time = timezone.now()
        else:
            review_request.status1 = 'in_progress'
        review_request.save()

    # 日志和通知(在事务外执行)
    has_images = bool(results)
    has_texts = bool(text_reviews_data)
    if has_images and has_texts:
        review_type = 'mixed'
    elif has_images:
        review_type = 'image'
    else:
        review_type = 'text'

    task_type = _resolve_task_type(review_request)

    image_results = [item.get('final') for item in results if item.get('final') is not None]
    text_results = [item.get('result') for item in text_reviews_data if item.get('result') is not None]
    all_results = image_results + text_results
    overall_result = 'fake' if any(all_results) else 'real' if all_results else 'unknown'

    log_action(
        user=request.user,
        operation_type='submit_review',
        target_type='manual_review',
        target_id=manual_review_id,
        ip=get_client_ip(request),
        detail={
            'review_type': review_type,
            'task_type': task_type,
            'result': overall_result,
            'image_review_count': len(results),
            'text_review_count': len(text_reviews_data),
        },
    )

    send_notification(
        receiver_id=review_request.user.id,
        receiver_name=review_request.user.username,
        sender_id=user.id,
        sender_name=user.username,
        category=Notification.R2P,
        title='任务完成通知',
        content=f'审稿人 {user.username} 已完成人工审核任务',
        url=f'/task/{review_request.id}'
    )

    return Response({'message': 'Review submitted successfully'}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def if_publisher_can_access_dectection_task(request):
    """
    检查当前用户是否有权访问某个 detection_task
    """
    task_id = request.query_params.get('task_id')
    if not task_id:
        return Response({'error': 'task_id is required'}, status=400)
    task = DetectionTask.objects.filter(id=task_id).first()
    if not task:
        return Response({'access': False})
    access = can_access_detection_task(request.user, task)
    return Response({'access': access})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def if_reviewer_can_access_manual_review(request):
    """
    只有这个manual_review是由这个reviewer提交的，才可以访问
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'reviewer':
        return Response({'access': False})
    manual_review_id = request.query_params.get('manual_review_id')
    if not manual_review_id:
        return Response({'error': 'manual_review_id is required'}, status=400)
    access = ManualReview.objects.filter(id=manual_review_id, reviewer=user).exists()
    return Response({'access': access})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_review_indicators(request):
    """获取指定材料类型的审核指标配置"""
    task_type = request.query_params.get('task_type', '')
    if not task_type:
        return Response({'error': 'task_type is required'}, status=400)

    config = get_review_config(task_type)
    if not config:
        return Response({'error': f'Unknown task_type: {task_type}'}, status=400)

    return Response({
        'task_type': task_type,
        'task_type_label': get_task_type_label(task_type),
        'task_type_color': get_task_type_color(task_type),
        'review_mode': config['review_mode'],
        'review_method': config['review_method'],
        'dimensions': config.get('dimensions', []),
        'indicators': config.get('indicators', []),
        'ai_assist_fields': config.get('ai_assist_fields', []),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_review_configs(request):
    """获取所有材料类型的审核配置"""
    configs = {}
    for key, config in MATERIAL_REVIEW_CONFIG.items():
        configs[key] = {
            'task_types': config['task_types'],
            'display_name': config['display_name'],
            'review_mode': config['review_mode'],
            'review_method': config['review_method'],
            'dimensions': config.get('dimensions', []),
            'indicators': config.get('indicators', []),
            'ai_assist_fields': config.get('ai_assist_fields', []),
        }
    return Response(configs)
