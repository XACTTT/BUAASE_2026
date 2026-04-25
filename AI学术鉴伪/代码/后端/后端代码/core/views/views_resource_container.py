from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import FileManagement, ImageUpload, ResourceContainer, ReviewTextResource
from core.services.material_validation_service import MaterialValidationService
from core.services.permissions import can_access_container
from core.services.resource_container_service import ResourceContainerService
from core.services.review_text_service import ReviewTextService


def _error(code, message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({'error_code': code, 'message': message}, status=status_code)


def _serialize_container(container: ResourceContainer):
    return {
        'id': container.id,
        'organization': container.organization_id,
        'owner': container.owner_id,
        'container_type': container.container_type,
        'title': container.title,
        'description': container.description,
        'source_ref': container.source_ref,
        'status': container.status,
        'progress_status': container.progress_status,
        'failure_reason': container.failure_reason,
        'metadata': container.metadata,
        'created_at': container.created_at,
        'updated_at': container.updated_at,
        'submitted_at': container.submitted_at,
    }


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def resource_container_list_create(request):
    if request.method == 'POST':
        required_fields = ['container_type', 'title']
        for field in required_fields:
            if not request.data.get(field):
                return _error('INVALID_PARAMS', f'{field} is required')

        try:
            container = ResourceContainerService.create_container(request.user, request.data)
        except Exception as exc:
            return _error('CONTAINER_CREATE_FAILED', str(exc))

        return Response(_serialize_container(container), status=status.HTTP_201_CREATED)

    containers = ResourceContainerService.list_containers(request.user)
    return Response([_serialize_container(item) for item in containers])


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def resource_container_detail(request, container_id):
    try:
        container = ResourceContainerService.get_container_or_raise(request.user, container_id)
    except ValueError:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    except PermissionError:
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        return Response(_serialize_container(container))

    if request.method == 'PUT':
        try:
            container = ResourceContainerService.update_container(request.user, container, request.data)
        except PermissionError:
            return _error('CONTAINER_EDIT_FORBIDDEN', 'no permission to edit this container', status.HTTP_403_FORBIDDEN)
        except Exception as exc:
            return _error('CONTAINER_UPDATE_FAILED', str(exc))
        return Response(_serialize_container(container))

    try:
        ResourceContainerService.delete_container(request.user, container)
    except PermissionError:
        return _error('CONTAINER_DELETE_FORBIDDEN', 'no permission to delete this container', status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def resource_container_review_text(request, container_id):
    try:
        container = ResourceContainerService.get_container_or_raise(request.user, container_id)
    except ValueError:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    except PermissionError:
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        entries = ReviewTextService.list_review_texts(container)
        return Response([
            {
                'id': entry.id,
                'container': entry.container_id,
                'source_type': entry.source_type,
                'language': entry.language,
                'raw_text': entry.raw_text,
                'normalized_text': entry.normalized_text,
                'token_count': entry.token_count,
                'parse_status': entry.parse_status,
                'parse_error': entry.parse_error,
                'created_at': entry.created_at,
                'updated_at': entry.updated_at,
            }
            for entry in entries
        ])

    try:
        review_text = ReviewTextService.create_review_text(request.user, container, request.data)
        return Response(
            {
                'id': review_text.id,
                'container': review_text.container_id,
                'source_type': review_text.source_type,
                'language': review_text.language,
                'token_count': review_text.token_count,
                'parse_status': review_text.parse_status,
            },
            status=status.HTTP_201_CREATED,
        )
    except ValueError as exc:
        code = str(exc)
        if code == 'INVALID_CONTAINER_TYPE':
            return _error(code, 'container_type must be review or multi_material')
        if code == 'EMPTY_REVIEW_TEXT':
            return _error(code, 'raw_text must not be empty')
        if code == 'REVIEW_TEXT_TOO_LARGE':
            return _error(code, 'raw_text exceeds max length')
        return _error('REVIEW_TEXT_CREATE_FAILED', code)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_materials(request, container_id):
    try:
        container = ResourceContainerService.get_container_or_raise(request.user, container_id)
    except ValueError:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    except PermissionError:
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    result = MaterialValidationService.validate_container_materials(request.user, container)
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_container_files(request, container_id):
    container = ResourceContainer.objects.filter(id=container_id).first()
    if not container:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    if not can_access_container(request.user, container):
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    queryset = FileManagement.objects.filter(container=container).order_by('-upload_time')
    return Response([
        {
            'id': item.id,
            'file_name': item.file_name,
            'file_size': item.file_size,
            'file_type': item.file_type,
            'resource_role': item.resource_role,
            'origin_type': item.origin_type,
            'storage_path': item.storage_path,
            'parse_status': item.parse_status,
            'parse_error': item.parse_error,
            'upload_time': item.upload_time,
        }
        for item in queryset
    ])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_container_images(request, container_id):
    container = ResourceContainer.objects.filter(id=container_id).first()
    if not container:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    if not can_access_container(request.user, container):
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    queryset = ImageUpload.objects.filter(container=container).order_by('-upload_time')
    return Response([
        {
            'id': item.id,
            'file_management_id': item.file_management_id,
            'image_url': item.image.url if item.image else None,
            'image_role': item.image_role,
            'source_kind': item.source_kind,
            'file_name': item.file_name,
            'image_index': item.image_index,
            'width': item.width,
            'height': item.height,
            'hash_value': item.hash_value,
            'upload_time': item.upload_time,
        }
        for item in queryset
    ])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_container_materials_summary(request, container_id):
    container = ResourceContainer.objects.filter(id=container_id).first()
    if not container:
        return _error('CONTAINER_NOT_FOUND', 'container not found', status.HTTP_404_NOT_FOUND)
    if not can_access_container(request.user, container):
        return _error('CONTAINER_FORBIDDEN', 'no permission to access this container', status.HTTP_403_FORBIDDEN)

    file_count = FileManagement.objects.filter(container=container).count()
    image_count = ImageUpload.objects.filter(container=container).count()
    review_text_count = ReviewTextResource.objects.filter(container=container).count()
    failed_parse_count = FileManagement.objects.filter(container=container, parse_status='failed').count()

    validation_result = MaterialValidationService.validate_container_materials(request.user, container)

    return Response(
        {
            'file_count': file_count,
            'image_count': image_count,
            'review_text_count': review_text_count,
            'material_types_present': validation_result['material_types_present'],
            'failed_parse_count': failed_parse_count,
        }
    )
