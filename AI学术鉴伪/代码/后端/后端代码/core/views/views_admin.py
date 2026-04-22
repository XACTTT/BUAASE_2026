import csv
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import PublisherReviewerRelationship, ImageReview, Organization
from django.http import JsonResponse, HttpResponse
from ..models import DetectionTask, ManualReview
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from rest_framework import serializers, views, status
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from ..models import ReviewRequest
from ..utils.serializers_safe import serialize_value
from ..utils.log_utils import action_log, log_action, get_client_ip
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
from core.models import Log, User
from rest_framework.decorators import api_view, permission_classes
from collections import defaultdict
from core.models import FileManagement, ImageUpload, DetectionResult, SubDetectionResult
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ObjectDoesNotExist
from core.util import send_notification
from core.models import Notification


def _safe_avatar_url(user):
    avatar = getattr(user, 'avatar', None)
    if avatar and avatar.name and avatar.storage.exists(avatar.name):
        return avatar.url
    return None


def _infer_resource_type(file_obj):
    role = file_obj.resource_role or ''
    file_ext = (file_obj.file_ext or '').lower()
    if role.startswith('paper_'):
        return 'paper'
    if role.startswith('review_'):
        return 'review'
    if file_ext in {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}:
        return 'image'
    return 'comprehensive'


def _map_detection_status(parse_status):
    if parse_status in ('uploaded', 'validating'):
        return 'pending'
    if parse_status == 'parsing':
        return 'detecting'
    if parse_status == 'parsed':
        return 'completed'
    return 'failed'


def _serialize_resource(file_obj):
    latest_result = DetectionResult.objects.filter(
        image_upload__file_management=file_obj
    ).order_by('-id').first()

    detection_result = None
    detection_time = None
    if latest_result is not None:
        if latest_result.is_fake is True:
            detection_result = 'fake'
        elif latest_result.is_fake is False:
            detection_result = 'real'
        if latest_result.detection_time:
            detection_time = timezone.localtime(latest_result.detection_time).isoformat()

    metadata = file_obj.extra_metadata or {}

    return {
        'id': file_obj.id,
        'type': _infer_resource_type(file_obj),
        'file_name': file_obj.file_name,
        'file_format': (file_obj.file_ext or '').lower() or file_obj.file_type,
        'upload_time': timezone.localtime(file_obj.upload_time).isoformat(),
        'uploader_id': file_obj.user_id,
        'uploader_name': file_obj.user.username,
        'uploader_email': file_obj.user.email,
        'classification': file_obj.tag,
        'detection_time': detection_time,
        'detection_result': detection_result,
        'detection_status': _map_detection_status(file_obj.parse_status),
        'task_id': latest_result.detection_task_id if latest_result else None,
        'title': metadata.get('title') or file_obj.file_name,
        'author': metadata.get('author'),
        'organization': file_obj.organization.name if file_obj.organization else None,
        'editor': metadata.get('editor'),
        'subject': metadata.get('subject'),
        'status': metadata.get('status'),
        'review_count': metadata.get('review_count', 0),
    }


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_resources(request):
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    if page_size <= 0:
        page_size = 10

    resources = FileManagement.objects.select_related('user', 'organization').all().order_by('-upload_time')

    user = request.user
    if user.email != 'admin@mail.com':
        resources = resources.filter(organization=user.organization)

    resource_type = request.query_params.get('type')
    query = request.query_params.get('query')
    uploader_id = request.query_params.get('user_id')
    classification = request.query_params.get('classification')
    start_time = request.query_params.get('start_time')
    end_time = request.query_params.get('end_time')
    detection_result = request.query_params.get('detection_result')

    if query:
        query_filter = (
            models.Q(file_name__icontains=query)
            | models.Q(user__username__icontains=query)
            | models.Q(user__email__icontains=query)
        )
        if query.isdigit():
            query_filter = query_filter | models.Q(id=int(query))
        resources = resources.filter(query_filter)

    if uploader_id:
        resources = resources.filter(user_id=uploader_id)

    if classification:
        resources = resources.filter(tag=classification)

    try:
        if start_time:
            resources = resources.filter(upload_time__gte=_parse_request_datetime(start_time))
        if end_time:
            resources = resources.filter(upload_time__lte=_parse_request_datetime(end_time))
    except ValueError:
        return Response({'error': 'Invalid datetime format'}, status=400)

    serialized = [_serialize_resource(file_obj) for file_obj in resources]

    if resource_type:
        serialized = [item for item in serialized if item['type'] == resource_type]

    if detection_result in ('real', 'fake'):
        serialized = [item for item in serialized if item['detection_result'] == detection_result]

    total_count = len(serialized)
    total_pages = (total_count + page_size - 1) // page_size if total_count else 0
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return Response({
        'total_count': total_count,
        'page': page,
        'total_pages': total_pages,
        'resources': serialized[start_index:end_index],
    })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_resource_detail(request, resource_id):
    try:
        resource = FileManagement.objects.select_related('user', 'organization').get(id=resource_id)
    except FileManagement.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=404)

    user = request.user
    if user.email != 'admin@mail.com' and resource.organization_id != user.organization_id:
        return Response({'error': 'Forbidden'}, status=403)

    if request.method == 'GET':
        return Response(_serialize_resource(resource))

    if request.method == 'PUT':
        data = request.data
        classification = data.get('classification')
        tags = data.get('tags')
        is_public = data.get('is_public')

        if classification in [choice[0] for choice in FileManagement.TAG_CHOICES]:
            resource.tag = classification

        metadata = resource.extra_metadata or {}
        if tags is not None:
            metadata['tags'] = tags
        if is_public is not None:
            metadata['is_public'] = bool(is_public)
        resource.extra_metadata = metadata
        resource.save(update_fields=['tag', 'extra_metadata'])
        return Response(_serialize_resource(resource))

    resource.delete()
    return Response(status=204)


def _parse_request_datetime(value):
    """将请求中的时间字符串解析为当前时区的 aware datetime。"""
    dt = parse_datetime(value)
    if dt is None:
        dt = datetime.fromisoformat(value)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


class AdminDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    admin_type = serializers.SerializerMethodField()  # 新增字段：区分管理员类型
    organization_name = serializers.SerializerMethodField(read_only=True)  # 动态获取组织名称

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'profile', 'avatar', 'organization', 'organization_name',
                  'admin_type']

    def get_admin_type(self, obj):
        if obj.email == 'admin@mail.com' or (obj.is_staff and obj.organization is None):
            return 'software_admin'  # 软件管理员
        elif obj.is_staff:
            return 'organization_admin'  # 组织管理员（非全局）
        else:
            return 'unknown'  # 非管理员用户

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None

    def get_avatar(self, obj):
        return _safe_avatar_url(obj)


@permission_classes([IsAdminUser])
class AdminDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, user_id=None):
        # 如果没有传入 user_id，默认返回当前用户信息（保持兼容性）
        if user_id is None:
            user = request.user
        else:
            try:
                user = User.objects.get(id=user_id)  # 根据 user_id 获取指定用户
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminDetailSerializer(user)
        return Response(serializer.data)


class AdminDashboardView(APIView):
    """
    管理员仪表盘视图
    """

    @permission_classes([IsAdminUser])
    def get(self, request):
        # 获取所有用户信息
        if request.user.email == 'admin@mail.com':
            users = User.objects.all()
        else:
            users = User.objects.filter(organization=request.user.organization)

        user_data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            } for user in users
        ]

        # 获取最近30天的检测任务统计
        one_month_ago = timezone.now() - timedelta(days=30)
        if request.user.email == 'admin@mail.com':
            recent_tasks = DetectionTask.objects.filter(upload_time__gte=one_month_ago)
        else:
            recent_tasks = DetectionTask.objects.filter(upload_time__gte=one_month_ago,
                                                        organization=request.user.organization)
        task_stats = {
            'total_tasks': recent_tasks.count(),
            'completed_tasks': recent_tasks.filter(status='completed').count(),
            'pending_tasks': recent_tasks.filter(status='pending').count(),
            'in_progress_tasks': recent_tasks.filter(status='in_progress').count(),
        }

        return JsonResponse({'users': user_data, 'task_stats': task_stats})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_img_tag(request):
    """
    返回符合对应Tag的ImageUpload数量统计（包含值为0的tag）
    参数: startTime, endTime（ISO 8601格式）
    示例响应: {"Biology": 1, "Medicine": 5, "Chemistry": 50, "Graphics": 2, "Other": 3, "Math": 0}
    """
    start_time = request.query_params.get('startTime')
    end_time = request.query_params.get('endTime')

    # 默认时间范围为最近一年
    now = timezone.now()
    default_start = now.replace(year=now.year - 1)
    default_end = now

    try:
        if start_time:
            start_time = _parse_request_datetime(start_time)
        else:
            start_time = default_start

        if end_time:
            end_time = _parse_request_datetime(end_time)
        else:
            end_time = default_end
    except ValueError:
        return Response({'error': 'Invalid datetime format'}, status=400)

    # 获取所有预设 tag（从 FileManagement 中提取）
    from core.models import FileManagement
    TAG_CHOICES = dict(FileManagement.TAG_CHOICES)  # [('Biology', 'Biology'), ...]

    # 初始化所有 tag 的计数为 0
    tag_counts = {tag: 0 for tag in TAG_CHOICES.keys()}

    # 查询在时间范围内的所有 FileManagement 数据并预取 image_uploads
    file_managements = FileManagement.objects.filter(
        upload_time__range=[start_time, end_time]
    ).prefetch_related('image_uploads')

    # 统计每个 tag 下的图片数量
    for fm in file_managements:
        count = fm.image_uploads.count()
        tag = fm.get_tag_display()  # 获取 human-readable tag 名称
        if tag in tag_counts:
            tag_counts[tag] += count

    return Response(tag_counts)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def top_publishers_with_fake_ratio(request):
    # 获取所有 publisher 用户
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if request.user.email == 'admin@mail.com':
        publishers = User.objects.filter(role='publisher')
    else:
        publishers = User.objects.filter(role='publisher', organization=user.organization)

    result = []

    for user in publishers:
        # 获取该用户的所有任务
        tasks = DetectionTask.objects.filter(user=user)
        # 获取所有相关图片
        images = ImageUpload.objects.filter(detection_task__in=tasks)
        total_images = images.count()

        if total_images == 0:
            fake_ratio = 0
        else:
            fake_count = images.filter(isFake=True).count()
            fake_ratio = round(fake_count / total_images, 2)

        result.append({
            "username": user.username,
            "total_tasks": tasks.count(),
            "total_images": total_images,
            "fake_count": images.filter(isFake=True).count(),
            "fake_ratio": fake_ratio
        })

    # 排序并取前10
    top_10 = sorted(result, key=lambda x: x['total_tasks'], reverse=True)[:10]

    return Response(top_10)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def top_organizations_with_fake_ratio(request):
    """
    获取假图率最高的前10个组织（按总任务数排序）
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # 权限控制：如果是全局管理员则获取所有组织，否则仅获取当前用户所在组织
    if request.user.email == 'admin@mail.com':
        organizations = Organization.objects.all()
    else:
        organizations = Organization.objects.filter(id=user.organization.id)

    result = []

    for org in organizations:
        # 获取该组织下的所有 publisher 用户
        publishers = User.objects.filter(role='publisher', organization=org)

        # 获取该组织下所有 publisher 的任务
        tasks = DetectionTask.objects.filter(user__in=publishers)

        # 获取这些任务下的所有图片
        images = ImageUpload.objects.filter(detection_task__in=tasks)
        total_images = images.count()

        if total_images == 0:
            fake_count = 0
            fake_ratio = 0.0
        else:
            fake_count = images.filter(isFake=True).count()
            fake_ratio = round(fake_count / total_images, 2)

        result.append({
            "organization_name": org.name,
            "total_tasks": tasks.count(),
            "total_images": total_images,
            "fake_count": fake_count,
            "fake_ratio": fake_ratio
        })

    # 按总任务数排序并取前10
    top_10 = sorted(result, key=lambda x: x['total_tasks'], reverse=True)[:10]

    return Response(top_10)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def daily_active_users(request):
    """
    获取最近一周中每天活跃的 publisher 和 reviewer 数量
    返回示例:
    [
      {"date": "2024-11-25", "publisher_count": 3, "reviewer_count": 2},
      ...
    ]
    """
    # 获取今天和过去六天的日期列表（共7天）
    today = timezone.now().date()
    date_list = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # 最早到今天往前推6天

    result = []

    for target_date in date_list:
        start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

        # 查询当天有操作记录的用户ID
        user_ids = Log.objects.filter(
            operation_time__range=[start_of_day, end_of_day]
        ).values_list('user', flat=True).distinct()

        # 获取这些用户的信息
        users = User.objects.filter(id__in=user_ids)

        # 按角色统计
        roles_count = defaultdict(int)
        for user in users:
            if user.role == 'publisher':
                roles_count['publisher'] += 1
            elif user.role == 'reviewer':
                roles_count['reviewer'] += 1

        result.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'publisher_count': roles_count.get('publisher', 0),
            'reviewer_count': roles_count.get('reviewer', 0),
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def daily_active_organizations(request):
    """
    获取最近一周中每天活跃的组织数量
    返回示例:
    [
      {"date": "2024-11-25", "organization_count": 3},
      ...
    ]
    """
    # 获取今天和过去六天的日期列表（共7天）
    today = timezone.now().date()
    date_list = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # 最早到今天往前推6天

    result = []

    for target_date in date_list:
        start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

        # 查询当天有操作记录的用户ID
        user_ids = Log.objects.filter(
            operation_time__range=[start_of_day, end_of_day]
        ).values_list('user', flat=True).distinct()

        # 获取这些用户所属的组织ID
        organization_ids = User.objects.filter(id__in=user_ids) \
            .exclude(organization=None) \
            .values_list('organization', flat=True) \
            .distinct()

        organization_count = organization_ids.count()

        result.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'organization_count': organization_count,
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def daily_task_count(request):
    """
    获取最近一周每天的 DetectionTask 数量
    返回示例:
    [
      {"date": "2024-11-25", "task_count": 3},
      ...
    ]
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    today = timezone.now().date()
    date_list = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # 最近7天

    result = []

    for target_date in date_list:
        start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

        if request.user.email == 'admin@mail.com':
            count = DetectionTask.objects.filter(upload_time__range=[start_of_day, end_of_day]).count()
        else:
            count = DetectionTask.objects.filter(upload_time__range=[start_of_day, end_of_day],
                                                 user__organization=user.organization).count()

        result.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'task_count': count
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def daily_review_request_count(request):
    """
    获取最近一周每天的 ReviewRequest 数量
    返回示例:
    [
      {"date": "2024-11-25", "review_request_count": 3},
      ...
    ]
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    today = timezone.now().date()
    date_list = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    result = []

    for target_date in date_list:
        start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

        if request.user.email == 'admin@mail.com':
            count = ReviewRequest.objects.filter(request_time__range=[start_of_day, end_of_day]).count()
        else:
            count = ReviewRequest.objects.filter(request_time__range=[start_of_day, end_of_day],
                                                 user__organization=user.organization).count()

        result.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'review_request_count': count
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def daily_completed_manual_review_count(request):
    """
    获取最近一周每天已完成的 ManualReview 数量
    返回示例:
    [
      {"date": "2024-11-25", "manual_review_count": 3},
      ...
    ]
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    today = timezone.now().date()
    date_list = [(today - timedelta(days=i)) for i in range(6, -1, -1)]

    result = []

    for target_date in date_list:
        start_of_day = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_of_day = timezone.make_aware(datetime.combine(target_date, datetime.max.time()))

        if request.user.email == 'admin@mail.com':
            count = ManualReview.objects.filter(
                review_time__range=[start_of_day, end_of_day],
                status='completed'
            ).count()
        else:
            count = ManualReview.objects.filter(
                review_time__range=[start_of_day, end_of_day],
                status='completed',
                reviewer__organization=user.organization
            ).count()

        result.append({
            'date': target_date.strftime('%Y-%m-%d'),
            'manual_review_count': count
        })

    return Response(result)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_sub_method_distribution_by_tag(request):
    """
    根据文件标签返回各子检测方法的使用频率及比例
    支持两种输出格式：
        - flat: 平铺格式（默认）
        - grouped: 按方法分组的嵌套格式（用于图表展示）

    示例请求：
        GET /api/dashboard/sub_method_distribution?format=grouped
    """
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # 获取输出格式参数
    output_format = request.query_params.get('format', 'flat')  # 默认为 flat

    # 获取所有预设标签
    TAG_CHOICES = [tag for tag, _ in FileManagement.TAG_CHOICES]
    SUB_METHOD_DISPLAY = dict(SubDetectionResult._meta.get_field('method').flatchoices)

    result = {}

    for tag in TAG_CHOICES:
        # Step 1: 获取该 tag 下的所有 image_upload
        if request.user.email == 'admin@mail.com':
            image_uploads = ImageUpload.objects.filter(
                file_management__tag=tag
            )
        else:
            image_uploads = ImageUpload.objects.filter(
                file_management__tag=tag,
                detection_task__user__organization=user.organization
            )

        # Step 2: 获取这些 image_upload 对应的 detection_result
        detection_results = DetectionResult.objects.filter(
            image_upload__in=image_uploads
        )

        # Step 3: 获取对应的 sub_detection_results，并统计 method 分布
        sub_results = SubDetectionResult.objects.filter(
            detection_result__in=detection_results
        ).values('method')

        # 初始化计数器
        method_counts = defaultdict(int)
        total_count = 0

        for item in sub_results:
            method_key = item['method']
            method_display = SUB_METHOD_DISPLAY.get(method_key, method_key)
            method_counts[method_display] += 1
            total_count += 1

        # 构造响应数据
        distribution = {
            'total': total_count
        }

        for method_key, display_name in SubDetectionResult._meta.get_field('method').choices:
            count = method_counts.get(display_name, 0)
            percentage = round(count / total_count * 100, 2) if total_count > 0 else 0.0
            distribution[display_name] = count
            distribution[f"{display_name}_percentage"] = percentage

        result[tag] = distribution

    # 如果 format == grouped，则转换为数组形式
    if output_format == 'grouped':
        formatted_result = []
        for tag, data in result.items():
            methods_data = []
            for method_key, display_name in SubDetectionResult._meta.get_field('method').choices:
                methods_data.append({
                    "name": display_name,
                    "count": data.get(display_name, 0),
                    "percentage": data.get(f"{display_name}_percentage", 0.0)
                })
            formatted_result.append({
                "tag": tag,
                "methods": methods_data
            })

        return Response(formatted_result)

    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reviewer_to_publisher(request):
    """为Publisher添加Reviewer关联"""
    publisher_id = request.data.get('publisher_id')
    reviewer_id = request.data.get('reviewer_id')

    # 验证当前用户是否为操作者本人或管理员
    if request.user.id != int(publisher_id) and not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=403)

    try:
        publisher = User.objects.get(id=publisher_id, role='publisher')
        reviewer = User.objects.get(id=reviewer_id, role='reviewer')
    except User.DoesNotExist:
        return Response({'error': 'Invalid user role'}, status=400)

    # 创建或更新关联关系
    rel, created = PublisherReviewerRelationship.objects.update_or_create(
        publisher=publisher,
        reviewer=reviewer,
        defaults={'is_active': True}
    )

    return Response({
        'status': 'created' if created else 'updated',
        'relationship_id': rel.id
    })


class UserPermissionView(APIView):
    """
    用户权限管理视图
    """

    @permission_classes([IsAdminUser])
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            # 获取请求中的权限值
            permission_value = request.data.get('permission')

            try:
                if permission_value is None:
                    permission_value = None
                else:
                    permission_value = int(permission_value)
            except ValueError:
                return JsonResponse({'error': 'Permission value must be an integer'}, status=400)

            # 更新用户权限
            user.permission = permission_value
            user.save_permission()

            if permission_value is not None:
                perm_str = str(permission_value).zfill(4)
                perms_desc = {
                    'upload': '可上传' if perm_str[0] == '1' else '不可上传',
                    'submit': '可提交' if perm_str[1] == '1' else '不可提交',
                    'publish': '可发布' if perm_str[2] == '1' else '不可发布',
                    'review': '可审核' if perm_str[3] == '1' else '不可审核',
                }
            else:
                perms_desc = {
                    'upload': '不可上传',
                    'submit': '不可提交',
                    'publish': '不可发布',
                    'review': '不可审核',
                }

            # 构建通知内容
            permission_description = f"{perms_desc['upload']}、{perms_desc['submit']}、{perms_desc['publish']}、{perms_desc['review']}"

            send_notification(
                receiver_id=user.id,
                receiver_name=user.username,
                sender_id=request.user.id,
                sender_name=request.user.username,
                category=Notification.SYSTEM,
                title='权限更改通知',
                content=f'管理员 {request.user.username} 已将您的权限设置为：{permission_description}'
            )

            return JsonResponse({'message': f'Permission {permission_value} added to user {user.username}'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('report', target_type='DetectionTask', target_id_field='post_id')
def PostReportView(request, post_id):
    """
    帖子举报处理视图
    """
    try:
            # 获取被举报的检测任务
            task = DetectionTask.objects.get(id=post_id)

            # 标记任务为已举报
            task.status = 'reported'
            task.save()

            # 创建举报记录
            report = ReviewRequest.objects.create(
                detection_result=DetectionResult.objects.filter(detection_task=task).first(),
                user=request.user,
                status='pending',
                reason=request.POST.get('reason', 'No reason provided')
            )

            return JsonResponse({'message': f'Post {post_id} reported successfully', 'report_id': report.id})
    except DetectionTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)


class UserActionLogGetView(APIView):
    """
    用户操作日志视图
    """

    @permission_classes([IsAdminUser])
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        # 获取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        query = request.GET.get('query', '')
        role = request.GET.get('role', '')
        operation_type = request.GET.get('operation_type', '')
        target_type = request.GET.get('target_type', '')
        start_time = request.GET.get('startTime', None)
        end_time = request.GET.get('endTime', None)
        organization_name = request.GET.get('organization', None)
        is_anomaly = request.GET.get('is_anomaly', None)
        result = request.GET.get('result', '')

        # 获取所有日志记录并应用筛选条件
        logs = Log.objects.all().order_by('-operation_time')
        # 权限控制
        if request.user.email != 'admin@mail.com':
            organization = user.organization
            logs = logs.filter(user__organization=organization)
        else:
            organization_id = request.query_params.get('organization')
            if organization_id:
                logs = logs.filter(user__organization_id=organization_id)

        if query:
            logs = logs.filter(user__username__startswith=query)
        if role:
            logs = logs.filter(user_role=role)
        if operation_type:
            logs = logs.filter(operation_type=operation_type)
        if target_type:
            logs = logs.filter(target_type=target_type)
        if start_time:
            logs = logs.filter(operation_time__gte=start_time)
        if end_time:
            logs = logs.filter(operation_time__lte=end_time)
        if organization_name:
            logs = logs.filter(user__organization__name__icontains=organization_name)
        if is_anomaly is not None:
            logs = logs.filter(is_anomaly=(is_anomaly.lower() == 'true'))
        if result:
            logs = logs.filter(result=result)

        paginator = Paginator(logs, page_size)

        try:
            page_obj = paginator.page(page)
        except Exception:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        log_data = [
            {
                'id': log.log_id,
                'user_id': log.user.id,
                'user': log.user.username,
                'user_role': log.user_role,
                'operation_type': log.operation_type,
                'target_type': log.target_type,
                'target_id': log.target_id,
                'operation_detail': log.operation_detail,
                'ip_address': log.ip_address,
                'result': log.result,
                'error_msg': log.error_msg,
                'is_anomaly': log.is_anomaly,
                'operation_time': log.operation_time.strftime('%Y-%m-%d %H:%M:%S'),
                'organization': log.user.organization.name if log.user.organization else None
            } for log in page_obj.object_list
        ]

        return JsonResponse({
            'logs': log_data,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_logs': paginator.count,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        })


class UserActionLogDeleteView(APIView):
    @permission_classes([IsAdminUser])
    def delete(self, request, log_id):
        try:
            # 删除指定的日志记录
            log = Log.objects.get(id=log_id)
            log.delete()
            return JsonResponse({'message': f'Log {log_id} deleted successfully'})
        except Log.DoesNotExist:
            return JsonResponse({'error': 'Log not found'}, status=404)


class UserActionLogDownloadView(APIView):
    @permission_classes([IsAdminUser])
    def get(self, request):
        """
        下载日志文件
        """
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        # 获取查询参数
        query = request.query_params.get('query', None)
        operation_type = request.query_params.get('operation_type', '')
        target_type = request.query_params.get('target_type', '')
        start_time = request.query_params.get('startTime', None)
        end_time = request.query_params.get('endTime', None)
        organization_name = request.query_params.get('organization', None)
        is_anomaly = request.query_params.get('is_anomaly', None)

        # 获取所有日志记录并应用筛选条件
        logs = Log.objects.all().order_by('-operation_time')
        # 权限控制
        if request.user.email != 'admin@mail.com':
            organization = user.organization
            logs = logs.filter(user__organization=organization)
        else:
            organization_id = request.query_params.get('organization')
            if organization_id:
                logs = logs.filter(user__organization_id=organization_id)

        if query:
            logs = logs.filter(user__username__icontains=query)
        if operation_type:
            logs = logs.filter(operation_type=operation_type)
        if target_type:
            logs = logs.filter(target_type=target_type)
        if start_time:
            logs = logs.filter(operation_time__gte=start_time)
        if end_time:
            logs = logs.filter(operation_time__lte=end_time)
        if organization_name:
            logs = logs.filter(user__organization__name__icontains=organization_name)
        if is_anomaly is not None:
            logs = logs.filter(is_anomaly=(is_anomaly.lower() == 'true'))

        # 创建CSV文件内容
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_action_logs.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Log ID', 'User', 'User Role', 'Operation Type', 'Target Type', 
            'Target ID', 'Operation Time', 'IP Address', 'Result', 
            'Is Anomaly', 'Organization'
        ])

        for log in logs:
            writer.writerow([
                log.log_id,
                log.user.username,
                log.user_role,
                log.operation_type,
                log.target_type,
                log.target_id,
                log.operation_time.strftime('%Y-%m-%d %H:%M:%S'),
                log.ip_address,
                log.result,
                'Yes' if log.is_anomaly else 'No',
                log.user.organization.name if log.user.organization else ''
            ])

        return response


class UserActionLogMarkAnomalyView(APIView):
    """
    标记日志为异常事件
    """
    @permission_classes([IsAdminUser])
    def put(self, request, log_id):
        try:
            log = Log.objects.get(log_id=log_id)
            # 权限检查：非全局管理员只能操作自己组织的日志
            if request.user.email != 'admin@mail.com':
                if log.user.organization != request.user.organization:
                    return JsonResponse({'error': 'Permission denied'}, status=403)
            
            is_anomaly = request.data.get('is_anomaly', True)
            log.is_anomaly = is_anomaly
            log.save()
            return JsonResponse({'message': f'Log {log_id} marked as anomaly: {is_anomaly}'})
        except Log.DoesNotExist:
            return JsonResponse({'error': 'Log not found'}, status=404)


class LogStatisticsView(APIView):
    """
    操作记录统计 (FR-LOG-003)
    """
    @permission_classes([IsAdminUser])
    def get(self, request):
        from django.db.models import Count
        from django.db.models.functions import TruncDate
        
        # 默认统计最近 30 天
        days = int(request.GET.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        logs = Log.objects.filter(operation_time__gte=start_date)
        
        # 权限控制
        if request.user.email != 'admin@mail.com':
            logs = logs.filter(user__organization=request.user.organization)
        
        # 1. 每日操作次数统计
        daily_stats = logs.annotate(date=TruncDate('operation_time')) \
                          .values('date') \
                          .annotate(count=Count('log_id')) \
                          .order_by('date')
        
        # 2. 操作类型占比
        type_stats = logs.values('operation_type') \
                         .annotate(count=Count('log_id')) \
                         .order_by('-count')
        
        # 3. 异常操作统计
        anomaly_count = logs.filter(is_anomaly=True).count()
        
        return JsonResponse({
            'daily_stats': list(daily_stats),
            'type_stats': list(type_stats),
            'total_count': logs.count(),
            'anomaly_count': anomaly_count
        })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_task_summary(request):
    one_month_ago = timezone.now() - timedelta(days=30)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # 权限控制
    if request.user.email != 'admin@mail.com':
        organization = user.organization
        tasks = DetectionTask.objects.filter(organization=organization)
    else:
        organization_id = request.query_params.get('organization')
        if organization_id:
            tasks = DetectionTask.objects.filter(organization_id=organization_id)
        else:
            tasks = DetectionTask.objects.all()

    completed_tasks = tasks.filter(status='completed')
    recent_tasks = tasks.filter(upload_time__gte=one_month_ago)

    # 统计任务数
    total_task_count = tasks.count()
    completed_task_count = completed_tasks.count()
    recent_task_count = recent_tasks.count()

    # 获取最近任务的详细信息
    task_details = []
    for task in recent_tasks:
        task_details.append({
            "task_id": task.id,
            "task_name": task.task_name,
            "status": task.status,
            "upload_time": timezone.localtime(task.upload_time),
            "completion_time": timezone.localtime(task.completion_time),
            "organization": task.organization.name if task.organization else None,
        })

    return Response({
        "total_task_count": total_task_count,
        "completed_task_count": completed_task_count,
        "recent_task_count": recent_task_count,
        "recent_tasks": task_details,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_detection_task_status(request, task_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    try:
        # 权限控制
        if request.user.email != 'admin@mail.com':
            user_organization = user.organization
            detection_task = DetectionTask.objects.get(id=task_id, organization=user_organization)
        else:
            organization_id = request.query_params.get('organization')
            if organization_id:
                detection_task = DetectionTask.objects.get(id=task_id, organization_id=organization_id)
            else:
                detection_task = DetectionTask.objects.get(id=task_id)

        detection_results = DetectionResult.objects.filter(detection_task=detection_task)

        # 收集任务相关的图像和状态信息
        task_status = {
            "task_id": detection_task.id,
            "task_name": detection_task.task_name,
            "status": detection_task.status,
            "upload_time": timezone.localtime(detection_task.upload_time),
            "completion_time": timezone.localtime(detection_task.completion_time),
            "organization": detection_task.organization.name if detection_task.organization else None,
            "detection_results": []
        }

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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_user_tasks(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    try:
        # 权限控制
        if request.user.email != 'admin@mail.com':
            user_organization = user.organization
            tasks = DetectionTask.objects.filter(organization=user_organization)
        else:
            organization_id = request.query_params.get('organization')
            if organization_id:
                tasks = DetectionTask.objects.filter(organization_id=organization_id)
            else:
                tasks = DetectionTask.objects.all()

        # 收集任务信息
        task_data = [
            {
                "task_id": task.id,
                "task_name": task.task_name,
                "status": task.status,
                "upload_time": timezone.localtime(task.upload_time),
                "completion_time": timezone.localtime(task.completion_time),
                "organization": task.organization.name if task.organization else None,
            } for task in tasks
        ]

        return Response({
            "tasks": task_data
        })

    except DetectionTask.DoesNotExist:
        return Response({"message": "No tasks found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    query = request.query_params.get('query', '')
    role = request.query_params.get('role', '')
    permission = request.query_params.get('permission', '')
    start_time = request.query_params.get('startTime', None)
    end_time = request.query_params.get('endTime', None)
    organization_name = request.query_params.get('organization', None)  # 新增组织筛选参数
    page_number = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)

    # 构建查询条件
    users = User.objects.all().order_by('-date_joined')
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # 权限控制
    if request.user.email != 'admin@mail.com':  # 非软件管理员
        current_organization = user.organization
        users = users.filter(organization=current_organization)  # 仅能访问本组织用户
        organization_id = current_organization.id  # 自动绑定当前组织 ID（可选）
    elif organization_name:  # 软件管理员传入了 organization
        users = users.filter(organization__name__startswith=organization_name)

    # 应用其他筛选条件
    if query:
        users = users.filter(username__startswith=query)
    if role:
        users = users.filter(role=role)
    if permission:
        try:
            permission = int(permission)
            users = users.filter(permission=permission)
        except ValueError:
            return Response({'error': 'Permission value must be an integer'}, status=400)
    if start_time:
        users = users.filter(date_joined__gte=start_time)
    if end_time:
        users = users.filter(date_joined__lte=end_time)

    paginator = Paginator(users, page_size)

    try:
        page = paginator.page(page_number)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=400)

    def get_admin_type(user_obj):
        if user_obj.email == 'admin@mail.com' or (user_obj.is_staff and user_obj.organization is None):
            return 'software_admin'  # 软件管理员
        elif user_obj.is_staff:
            return 'organization_admin'  # 组织管理员（非全局）
        else:
            return 'unknown'  # 非管理员用户

    user_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'permission': user.permission,
            'admin_type': get_admin_type(user),
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'avatar': _safe_avatar_url(user),
            'organization': user.organization.name if user.organization else None,  # 新增字段
        } for user in page.object_list
    ]

    return Response({
        'users': user_data,
        'current_page': page.number,
        'total_pages': paginator.num_pages,
        'total_users': paginator.count,
        'has_next': page.has_next(),
        'has_previous': page.has_previous()
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('entity_create', target_type='User', target_id_field='user_id')
def create_user(request):
    """
    创建新用户
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.role = role
    user.save()

    return Response({'message': 'User created successfully', 'user_id': user.id})


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@action_log('entity_update', target_type='User', target_id_field='user_id')
def update_user(request, user_id):
    """
    更新用户信息
    """
    try:
        user = User.objects.get(id=user_id)
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.role = request.data.get('role', user.role)
        user.state = request.data.get('state', user.state)
        user.permission = request.data.get('permission', user.permission)  # 更新 permission 字段

        if 'password' in request.data:
            user.set_password(request.data['password'])

        user.save()
        return Response({'message': 'User updated successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@action_log('entity_delete', target_type='User', target_id_field='user_id')
def delete_user(request, user_id):
    """
    删除用户
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    # role = serializers.ChoiceField(choices=[('publisher', 'Publisher'), ('reviewer', 'Reviewer')])

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        # role = data.get('role')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        if user.role != 'admin':
            raise serializers.ValidationError("Invalid role. User is not an admin")
        # if user.role != role:
        #     raise serializers.ValidationError(f"Invalid role. User is not a {role}.")

        data['user'] = user
        return data


class AdminLoginView(views.APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            log_action(user, 'login', result='success', ip=get_client_ip(request))
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': user.role,
                'profile': user.profile,  # 返回用户的简介信息
                'avatar': _safe_avatar_url(user)
            })
        log_action(None, 'login', result='failure', error_msg=f'Admin login failed: {str(serializer.errors)}', ip=get_client_ip(request))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_admin(request):
    """
    创建新管理员用户
    """
    if not request.user.is_superuser:
        return Response({'error': 'Only the root admin can create admin users'}, status=403)

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'admin')  # 默认角色为管理员

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    # 创建新用户
    user = User.objects.create_user(username=username, email=email, password=password)
    user.role = role
    user.is_staff = True  # 设置为员工用户
    user.save()

    return Response({'message': 'Admin user created successfully', 'user_id': user.id}, status=201)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@action_log('entity_delete', target_type='FileManagement', target_id_field='file_id')
def delete_upload(request, file_id):
    try:
        file_management = FileManagement.objects.get(id=file_id)
        file_management.delete()
        return Response({"message": "File deleted successfully"}, status=200)
    except FileManagement.DoesNotExist:
        return Response({"message": "File not found"}, status=404)
    except Exception as e:
        return Response({"message": str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_files(request):
    # 获取查询参数
    query = request.query_params.get('query', '')
    categories = request.query_params.get('categories', '')
    start_time = request.query_params.get('startTime', None)
    end_time = request.query_params.get('endTime', None)
    organization_name = request.query_params.get('organization', None)  # 修改为 organization_name
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    # 构建查询条件
    files = FileManagement.objects.all().order_by('-upload_time')
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    # 权限控制
    if user.email != 'admin@mail.com':
        current_organization = user.organization
        files = files.filter(organization=current_organization)
    elif organization_name:
        # 根据 organization_name 查找组织（模糊匹配）
        organizations = Organization.objects.filter(name__icontains=organization_name)
        if not organizations.exists():
            return Response({
                "files": [],
                "current_page": 1,
                "total_pages": 0,
                "total_files": 0,
                "has_next": False,
                "has_previous": False
            })  # 无匹配组织时返回空数据
        files = files.filter(organization__in=organizations)

    # 应用其他筛选条件
    if query:
        files = files.filter(user__username__startswith=query)
    if categories:
        files = files.filter(tag=categories)
    try:
        if start_time:
            start_time = _parse_request_datetime(start_time)
            files = files.filter(upload_time__gte=start_time)
        if end_time:
            end_time = _parse_request_datetime(end_time)
            files = files.filter(upload_time__lte=end_time)
    except ValueError:
        return Response({'error': 'Invalid datetime format'}, status=400)

    # 分页
    paginator = Paginator(files, page_size)
    try:
        page_obj = paginator.page(page)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=400)

    file_data = []
    for file in page_obj.object_list:
        file_data.append({
            "id": file.id,
            "username": file.user.username,
            "email": file.user.email,
            "file_name": file.file_name,
            "file_size": file.file_size,
            "file_type": file.file_type,
            "tag": file.tag,
            "upload_time": timezone.localtime(file.upload_time).strftime('%Y-%m-%d %H:%M:%S'),
            "organization": file.organization.name if file.organization else None,
        })

    return Response({
        "files": file_data,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_files": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_review_requests(request):
    # 获取查询参数
    query = request.query_params.get('query', '')
    status = request.query_params.get('status', '')
    organization_id = request.query_params.get('organization', None)
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    # 构建查询条件
    review_requests = ReviewRequest.objects.all().order_by('-request_time')
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # 权限控制
    if request.user.email != 'admin@mail.com':
        current_organization = user.organization
        review_requests = review_requests.filter(organization=current_organization)
    elif organization_id:
        review_requests = review_requests.filter(organization_id=organization_id)

    # 应用其他筛选条件
    if query:
        review_requests = review_requests.filter(user__username__startswith=query)
    if status:
        review_requests = review_requests.filter(status2=status)

    # 分页
    paginator = Paginator(review_requests, page_size)
    try:
        page_obj = paginator.page(page)
    except Exception:
        return Response({'error': 'Invalid page number'}, status=400)

    request_data = []
    for req in page_obj.object_list:
        request_data.append({
            "id": req.id,
            "username": req.user.username,
            "avatar": _safe_avatar_url(req.user),
            "state": req.status2,
            "time": timezone.localtime(req.request_time).strftime('%Y-%m-%d %H:%M:%S'),
            "organization": req.organization.name if req.organization else None,
        })

    return Response({
        "requests": request_data,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_requests": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_review_request_detail_admin(request, reviewRequest_id):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    try:
        # 权限控制
        if request.user.email != 'admin@mail.com':
            user_organization = user.organization
            review_request = ReviewRequest.objects.get(
                id=reviewRequest_id,
                organization=user_organization
            )
        else:
            organization_id = request.query_params.get('organization')
            if organization_id:
                review_request = ReviewRequest.objects.get(
                    id=reviewRequest_id,
                    organization_id=organization_id
                )
            else:
                review_request = ReviewRequest.objects.get(id=reviewRequest_id)

        # 获取 imgs 数据
        imgs = []
        for img in review_request.imgs.all():
            imgs.append({
                "id": img.id,
                "url": serialize_value(img.image, request) if img.image else None,
            })

        # 获取 persons 数据：所有参与该请求的 reviewer（来自 ManualReview 表）
        persons = []
        for reviewer in review_request.reviewers.all():
            persons.append({
                "id": reviewer.id,
                "username": reviewer.username,
                "avatar": _safe_avatar_url(reviewer),
            })

        return Response({
            "imgs": imgs,
            "persons": persons,
            "reason": review_request.reason,
            "organization": review_request.organization.name if review_request.organization else None,
        })

    except ReviewRequest.DoesNotExist:
        return Response({"error": "ReviewRequest not found"}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_review_request_detail(request, manual_review_id):
    """
    通过 ManualReview ID 获取 ReviewRequest 的详细信息
    """

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user.role != 'reviewer':
        return Response({'error': 'Only reviewers can view task details'}, status=403)

    try:
        # 根据 manual_review_id 获取 ManualReview 对象
        manual_review = ManualReview.objects.get(id=manual_review_id)
    except ManualReview.DoesNotExist:
        return Response({'error': 'ManualReview not found'}, status=404)

    # 获取关联的 ReviewRequest
    review_request = manual_review.review_request

    # 获取 imgs 数据（来自 ManualReview 的 imgs 多对多关系）
    imgs = []
    for img in manual_review.imgs.all():
        imgs.append({
            "id": img.id,
            "url": serialize_value(img.image, request) if img.image else None,
        })

    # 获取 persons 数据：所有参与该请求的 reviewer（来自 ManualReview 表）
    persons = []
    for reviewer in review_request.reviewers.all():
        persons.append({
            "id": reviewer.id,
            "username": reviewer.username,
            "avatar": _safe_avatar_url(reviewer),
        })

    # 构建返回数据
    response_data = {
        "imgs": imgs,
        "persons": persons,
        "reason": review_request.reason,
    }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('audit_op', target_type='ReviewRequest', target_id_field='reviewRequest_id')
def handle_review_request(request, reviewRequest_id):
    """
    管理员处理ReviewRequest，相当于管理员先决定是否通过，然后再给各个reviewer创建ManualReview（和ImageReview）
    """
    try:
        review_request = ReviewRequest.objects.get(id=reviewRequest_id)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)

    choice = request.data.get('choice')
    reason = request.data.get('reason', '')

    if choice is None:
        return Response({'error': 'Choice parameter is required'}, status=400)

    try:
        choice = int(choice)
    except ValueError:
        return Response({'error': 'Choice must be an integer (0 or 1)'}, status=400)

    if choice not in [0, 1]:
        return Response({'error': 'Choice must be 0 (reject) or 1 (accept)'}, status=400)

    if choice == 0:
        review_request.status2 = 'refused'
    elif choice == 1:
        review_request.status2 = 'accepted'

        # 获取所有图片
        images = review_request.imgs.all()

        # 遍历所有审阅人
        for reviewer in review_request.reviewers.all():
            # 创建 ManualReview 实例
            manual_review = ManualReview.objects.create(
                review_request=review_request,
                reviewer=reviewer,
                status='undo'  # 默认状态
            )

            # 设置 imgs 多对多关系
            manual_review.imgs.set(images)

            # 为每张图创建 ImageReview 并添加进 img_reviews
            image_reviews = []
            for img in images:
                image_review = ImageReview.objects.create(
                    manual_review=manual_review,
                    img=img,
                    result=False  # 可根据需要初始化其他字段
                )
                image_reviews.append(image_review)

            # 将所有 ImageReview 添加到 img_reviews 多对多字段
            manual_review.img_reviews.add(*image_reviews)

            # wyt shit here
            send_notification(
                receiver_id=reviewer.id,
                receiver_name=reviewer.username,
                sender_id=review_request.user.id,
                sender_name=review_request.user.username,
                category=Notification.P2R,
                title='新任务通知',
                content=f'出版社 {review_request.user.username} 给您分配了新任务，请及时处理',
                url=f'/task/detail/{manual_review.id}'
            )

    # 更新审核请求的状态和理由
    review_request.check_reason = reason
    review_request.save()

    return Response({'message': 'ReviewRequest handled successfully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
@action_log('entity_delete', target_type='ImageUpload', target_id_field='image_id')
def delete_image_upload(request, image_id):
    try:
        image_upload = ImageUpload.objects.get(id=image_id)
        image_upload.delete()
        return Response({'message': 'Image upload deleted successfully'}, status=200)
    except ObjectDoesNotExist:
        return Response({'error': 'Image upload not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@action_log('entity_delete', target_type='ReviewRequest', target_id_field='review_request_id')
def delete_review_request(request, review_request_id):
    """
    删除指定的 ReviewRequest 记录
    """
    try:
        # 获取 ReviewRequest 实例
        review_request = ReviewRequest.objects.get(id=review_request_id)

        # 删除关联的 ManualReview 和 ImageReview 数据（可选）
        manual_reviews = ManualReview.objects.filter(review_request=review_request)
        for manual_review in manual_reviews:
            manual_review.img_reviews.all().delete()  # 删除关联的 ImageReview
            manual_review.delete()  # 删除 ManualReview

        # 删除 ReviewRequest
        review_request.delete()

        return Response({'message': 'ReviewRequest and related data deleted successfully'}, status=200)
    except ReviewRequest.DoesNotExist:
        return Response({'error': 'ReviewRequest not found'}, status=404)
