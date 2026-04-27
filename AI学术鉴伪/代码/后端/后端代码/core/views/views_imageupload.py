import io
import uuid
import logging
from PIL import Image
import zipfile
from django.core.files.storage import FileSystemStorage
from ..models import FileManagement, ImageUpload, User, ResourceContainer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import ImageUpload
from core.services.file_ingest_service import FileIngestService
from ..utils.log_utils import action_log


logger = logging.getLogger(__name__)

@api_view(['POST'])
@action_log('upload', target_type='FileManagement', target_id_field='file_id')
@permission_classes([IsAuthenticated])
def upload_file(request):
    user = request.user
    if not user.has_permission('upload'):
        return Response({"错误": "该用户没有上传文件的权限"}, status=403)

    uploaded_files = request.FILES.getlist('file')
    if not uploaded_files:
        return Response({'error_code': 'MISSING_FILE', 'message': 'file is required'}, status=400)

    container = None
    container_id = request.data.get('container_id')
    resource_role = request.data.get('resource_role', 'material_other')
    batch_id = request.data.get('batch_id')

    if container_id:
        container = ResourceContainer.objects.filter(id=container_id).first()
        if not container:
            return Response({'error_code': 'CONTAINER_NOT_FOUND', 'message': 'container not found'}, status=404)

    upload_results = []
    file_types = request.data.getlist('file_type')
    file_type_to_resource_role = {
        'image': 'material_other',
        'paper': 'paper_main',
        'review': 'review_main',
    }

    for index, uploaded_file in enumerate(uploaded_files):
        mapped_resource_role = resource_role
        if index < len(file_types):
            mapped_resource_role = file_type_to_resource_role.get(file_types[index], resource_role)

        try:
            file_management, file_url = FileIngestService.ingest_upload(
                user=user,
                uploaded_file=uploaded_file,
                container=container,
                resource_role=mapped_resource_role,
                batch_id=batch_id,
            )
            upload_results.append({
                "file_id": file_management.id,
                "file_url": file_url,
                "container_id": file_management.container_id,
                "parse_status": file_management.parse_status,
                "file_type": file_types[index] if index < len(file_types) else None,
                "resource_role": file_management.resource_role,
            })
        except PermissionError:
            return Response(
                {'error_code': 'CONTAINER_UPLOAD_FORBIDDEN', 'message': 'no permission to upload to this container'},
                status=403,
            )
        except (ValueError, zipfile.BadZipFile) as exc:
            return Response({'error_code': 'INVALID_FILE_FORMAT', 'message': str(exc)}, status=400)
        except Exception as exc:
            logger.exception('Upload failed', exc_info=exc)
            return Response({'error_code': 'UPLOAD_FAILED', 'message': str(exc)}, status=500)

    first_result = upload_results[0]
    return Response({
        "message": "File uploaded successfully",
        "file_id": first_result["file_id"],
        "file_url": first_result["file_url"],
        "container_id": first_result["container_id"],
        "parse_status": first_result["parse_status"],
        "batch_id": batch_id,
        "file_ids": [item["file_id"] for item in upload_results],
        "files": upload_results,
    })


import os
import mimetypes
import threading
from django.conf import settings
from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_exempt
import fitz

# 全局锁（可选，根据并发需求）
# fitz_lock = threading.Lock()


def extract_images_from_pdf(file_management, file_path):
    import fitz
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # 使用锁确保线程安全（根据实际情况选择是否添加）
    # with fitz_lock:
    with fitz.open(full_file_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            try:
                image_list = page.get_images(full=True)
                for image_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    image_filename = f"{file_management.id}_page{page_number + 1}_image{image_index + 1}.{image_ext}"

                    # 保存图像
                    relative_image_path = save_image_pdf(image_bytes, image_filename)

                    # 创建数据库记录
                    ImageUpload.objects.create(
                        file_management=file_management,
                        image=relative_image_path,
                        extracted_from_pdf=True,
                        page_number=page_number + 1,
                        isDetect=False,
                        isReview=False,
                        isFake=False
                    )
            finally:
                del page  # 帮助GC及时回收
    return


def extract_images_from_zip(file_management, uploaded_file):
    with zipfile.ZipFile(uploaded_file) as zip_file:
        for file_name in zip_file.namelist():
            # 跳过目录
            file_info = zip_file.getinfo(file_name)
            if file_info.is_dir():
                continue

            # 处理图片文件（png/jpg/jpeg）
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img_data = zip_file.read(file_name)
                    image = Image.open(io.BytesIO(img_data))
                    image_name = f"{file_management.id}_{os.path.basename(file_name)}"
                    relative_image_path = save_image_zip(image, image_name)
                    ImageUpload.objects.create(
                        file_management=file_management,
                        image=relative_image_path,
                        extracted_from_pdf=False,
                        isDetect=False,
                        isReview=False,
                        isFake=False
                    )
                except Exception as e:
                    print(f"处理ZIP中的图片文件 {file_name} 时出错: {e}")

            # 处理PDF文件
            elif file_name.lower().endswith('.pdf'):
                temp_pdf_path = None
                try:
                    # 读取PDF内容
                    pdf_data = zip_file.read(file_name)
                    # 创建临时目录和文件名
                    temp_pdf_dir = os.path.join(settings.MEDIA_ROOT, 'temp_pdfs')
                    os.makedirs(temp_pdf_dir, exist_ok=True)
                    temp_pdf_filename = f"{uuid.uuid4().hex}.pdf"
                    temp_pdf_path = os.path.join(temp_pdf_dir, temp_pdf_filename)
                    # 保存到临时文件
                    with open(temp_pdf_path, 'wb') as f:
                        f.write(pdf_data)
                    # 构造相对路径
                    relative_temp_pdf_path = os.path.join('temp_pdfs', temp_pdf_filename)
                    # 调用PDF处理函数
                    extract_images_from_pdf(file_management, relative_temp_pdf_path)
                except Exception as e:
                    print(f"处理ZIP中的PDF文件 {file_name} 时出错: {e}")
                finally:
                    # 清理临时文件
                    if temp_pdf_path and os.path.exists(temp_pdf_path):
                        try:
                            os.remove(temp_pdf_path)
                        except Exception as e:
                            print(f"删除临时文件 {temp_pdf_path} 失败: {e}")


def save_image_pdf(image_data, image_name):
    # 构造相对路径（保存在 MEDIA_ROOT 下的 extracted_images 文件夹中）
    unique_image_name = f"{uuid.uuid4().hex}_{image_name}"
    relative_path = os.path.join('extracted_images', unique_image_name)
    relative_path = relative_path.replace('\\', '/')
    # 组合成完整路径
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    # 确保保存目录存在
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # 使用 PIL 打开并保存图像
    image = Image.open(io.BytesIO(image_data))
    image.save(full_path)

    # 返回相对路径，后续可以通过 settings.MEDIA_URL 进行访问
    return relative_path


def save_image_zip(image, image_name):
    # 构造相对路径，保存在 MEDIA_ROOT 下的 extracted_images 文件夹中
    unique_image_name = f"{uuid.uuid4().hex}_{image_name}"
    relative_path = os.path.join('extracted_images', unique_image_name)
    relative_path = relative_path.replace('\\', '/')
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    image.save(full_path)
    return relative_path


def store_image(file_management, uploaded_file):
    # 构造相对路径，将文件存储在 MEDIA_ROOT 下的 extracted_images 目录中
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
    relative_path = os.path.join('extracted_images', f"{file_management.id}_{unique_filename}")
    relative_path = relative_path.replace('\\', '/')
    fs = FileSystemStorage()
    fs.save(relative_path, uploaded_file)

    ImageUpload.objects.create(
        file_management=file_management,
        image=relative_path,
        extracted_from_pdf=False,
        isDetect=False,  # 初始值设为False
        isReview=False,  # 初始值设为False
        isFake=False  # 初始值设为False
    )


from django.utils import timezone


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file_details(request, file_id):
    try:
        file_management = FileManagement.objects.get(id=file_id, user=request.user)
        extracted_images = ImageUpload.objects.filter(file_management=file_management)
        image_urls = [image.image.url for image in extracted_images]

        is_pdf = file_management.file_type == 'application/pdf'

        return Response({
            "file_id": file_management.id,
            "user_id": file_management.user.id,
            "file_name": file_management.file_name,
            "file_url": file_management.storage_path,
            "upload_time": timezone.localtime(file_management.upload_time),
            "is_pdf": is_pdf,
            "extracted_images": image_urls
        })
    except FileManagement.DoesNotExist:
        return Response({"message": "File not found"}, status=404)


from .views_dectection import CustomPagination


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_extracted_images(request, file_id):
    try:
        # 获取文件对象并验证权限
        file_management = FileManagement.objects.get(id=file_id, user=request.user)

        # 仅在传入 batch_id 时做本次上传隔离，避免混入历史文件。
        request_batch_id = request.query_params.get('batch_id')
        if request_batch_id:
            metadata = file_management.extra_metadata or {}
            file_batch_id = str(metadata.get('batch_id', '')).strip()
            if file_batch_id != str(request_batch_id).strip():
                return Response({
                    "file_id": file_management.id,
                    "page": 1,
                    "page_size": 0,
                    "total": 0,
                    "images": []
                })

        # 按图片ID倒序排列（可根据需要改为其他字段如上传时间）
        extracted_images = ImageUpload.objects.filter(
            file_management=file_management
        ).order_by('-id')

        # 使用自定义分页类
        paginator = CustomPagination()
        paginated_images = paginator.paginate_queryset(extracted_images, request)

        # 构建图片列表（统一回传绝对URL，避免前端环境差异导致预览失败）
        image_list = []
        for image in paginated_images:
            if not image.image or not image.image.name:
                continue

            # 统一回传经 /api 鉴权的预览地址，避免前端环境下 /media 路由404。
            image_url = request.build_absolute_uri(f"/api/preview/image/{image.id}/")

            image_data = {
                "image_id": image.id,
                "image_url": image_url,
                "page_number": image.page_number if image.extracted_from_pdf else None,
                "extracted_from_pdf": image.extracted_from_pdf,
                "isDetect": image.isDetect,
                "isReview": image.isReview,
                "isFake": image.isFake
            }
            image_list.append(image_data)

        # 构造包含分页信息的响应
        return Response({
            "file_id": file_management.id,
            "page": paginator.page.number,
            "page_size": paginator.get_page_size(request),
            "total": paginator.page.paginator.count,
            "images": image_list
        })

    except FileManagement.DoesNotExist:
        return Response({"message": "File not found"}, status=404)


def _resolve_auth_user(request):
    """兼容 Header 与 query token 两种鉴权来源。"""
    auth_user = request.user if getattr(request.user, 'is_authenticated', False) else None
    if not auth_user:
        raw_token = request.query_params.get('token')
        if raw_token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(raw_token)
                auth_user = jwt_auth.get_user(validated_token)
            except Exception:
                auth_user = None
    return auth_user


@api_view(['GET'])
@permission_classes([AllowAny])
@xframe_options_exempt
def preview_resource(request, resource_type, resource_id):
    """统一预览接口：支持 image/file 两类资源。"""
    auth_user = _resolve_auth_user(request)

    if not auth_user:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)

    if resource_type == 'image':
        try:
            image = ImageUpload.objects.select_related('file_management').get(
                id=resource_id,
                file_management__user=auth_user,
            )
        except ImageUpload.DoesNotExist:
            return Response({"message": "Image not found"}, status=404)

        if not image.image or not image.image.name:
            return Response({"message": "Image file missing"}, status=404)

        try:
            image_path = image.image.path
        except Exception:
            return Response({"message": "Image path unavailable"}, status=404)

        if not os.path.exists(image_path):
            return Response({"message": "Image file not found on disk"}, status=404)

        return FileResponse(open(image_path, 'rb'), content_type='image/*')

    if resource_type == 'file':
        try:
            file_management = FileManagement.objects.get(id=resource_id, user=auth_user)
        except FileManagement.DoesNotExist:
            return Response({"message": "File not found"}, status=404)

        storage_path = file_management.storage_path
        if not storage_path:
            return Response({"message": "Stored file path missing"}, status=404)

        full_path = os.path.join(settings.MEDIA_ROOT, storage_path)
        if not os.path.exists(full_path):
            return Response({"message": "Stored file not found"}, status=404)

        guessed_type, _ = mimetypes.guess_type(full_path)
        content_type = guessed_type or file_management.mime_type or 'application/octet-stream'
        force_download = str(request.query_params.get('download', '')).lower() in ('1', 'true', 'yes')
        return FileResponse(
            open(full_path, 'rb'),
            content_type=content_type,
            as_attachment=force_download,
            filename=file_management.file_name,
        )

    return Response({"message": "Unsupported preview resource type"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_extracted_contents(request, file_id):
    try:
        file_management = FileManagement.objects.get(id=file_id, user=request.user)
    except FileManagement.DoesNotExist:
        return Response({"message": "File not found"}, status=404)

    storage_path = file_management.storage_path
    if not storage_path:
        return Response({
            "file_id": file_id,
            "preview_mode": "none",
            "file_ext": (file_management.file_ext or '').lower(),
            "contents": [],
            "page": 1,
            "page_size": 0,
            "total": 0
        })

    full_path = os.path.join(settings.MEDIA_ROOT, storage_path)
    if not os.path.exists(full_path):
        return Response({"message": "Stored file not found"}, status=404)

    file_ext = (file_management.file_ext or '').lower()
    if file_ext in {'pdf', 'doc', 'docx'}:
        preview_url = request.build_absolute_uri(f"/api/preview/file/{file_id}/")
        return Response({
            "file_id": file_id,
            "preview_mode": "file",
            "file_ext": file_ext,
            "file_name": file_management.file_name,
            "preview_url": preview_url,
            "can_inline": file_ext == 'pdf',
            "contents": [],
            "page": 1,
            "page_size": 0,
            "total": 0,
            "message": "file preview mode"
        })

    if file_ext != 'pdf':
        return Response({
            "file_id": file_id,
            "preview_mode": "none",
            "file_ext": file_ext,
            "contents": [],
            "page": 1,
            "page_size": 0,
            "total": 0,
            "message": "content extraction currently supports pdf/doc/docx preview only"
        })

    contents = []
    with fitz.open(full_path) as pdf_document:
        for page_idx in range(pdf_document.page_count):
            text = pdf_document.load_page(page_idx).get_text("text").strip()
            if not text:
                continue
            contents.append({
                "content_id": len(contents) + 1,
                "title": f"第{page_idx + 1}页",
                "text": text,
                "source": "pdf_extracted",
            })

    paginator = CustomPagination()
    paginated_contents = paginator.paginate_queryset(contents, request)

    return Response({
        "file_id": file_id,
        "preview_mode": "text",
        "file_ext": file_ext,
        "page": paginator.page.number,
        "page_size": paginator.get_page_size(request),
        "total": paginator.page.paginator.count,
        "contents": paginated_contents,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_file_tag(request, file_id):
    try:
        file = FileManagement.objects.get(id=file_id)
        tag = request.data.get('tag')

        if tag not in [choice[0] for choice in FileManagement.TAG_CHOICES]:
            return Response({"message": "Invalid tag type."}, status=400)

        file.tag = tag
        file.save()

        return Response({
            "message": "File add tag successfully",
            "file_id": file.id,
            "file_url": f"/media/{file.file_name}"
        })

    except FileManagement.DoesNotExist:
        return Response({"message": "File not found."}, status=404)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_file_images(request, file_management_id):
    """
    获取指定文件的所有图片信息，支持分页和筛选。
    """

    try:
        file_management = FileManagement.objects.get(id=file_management_id)
    except FileManagement.DoesNotExist:
        return Response({"message": "File not found"}, status=404)

    # 获取查询参数
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    is_detect = request.query_params.get('isDetect')
    is_review = request.query_params.get('isReview')
    is_fake = request.query_params.get('isFake')

    # 确保 page_size 不超过最大限制
    if page_size > 100:
        page_size = 100

    # 构建查询集：只获取该 file_management 下的图片
    images = ImageUpload.objects.filter(file_management=file_management)

    # 应用筛选条件
    if is_detect in ['true', 'True', '1']:
        images = images.filter(isDetect=True)
    elif is_detect in ['false', 'False', '0']:
        images = images.filter(isDetect=False)

    if is_review in ['true', 'True', '1']:
        images = images.filter(isReview=True)
    elif is_review in ['false', 'False', '0']:
        images = images.filter(isReview=False)

    if is_fake in ['true', 'True', '1']:
        images = images.filter(isFake=True)
    elif is_fake in ['false', 'False', '0']:
        images = images.filter(isFake=False)

    # 分页处理
    paginator = Paginator(images, page_size)

    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return Response({'error': 'Page not found'}, status=404)

    # 构造返回数据
    results = []
    for image in page_obj.object_list:
        results.append({
            "img_id": image.id,
            "img_url": image.image.url,
            "isDetect": image.isDetect,
            "isReview": image.isReview,
            "isFake": image.isFake,
        })

    return Response({
        "file_id": file_management_id,
        "imgs": results,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "total_count": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous()
    })
