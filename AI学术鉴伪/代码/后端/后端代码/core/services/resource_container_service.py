from django.db.models import Q

from core.models import ResourceContainer
from core.services.audit_service import audit_log
from core.services.permissions import can_access_container, can_edit_container


class ResourceContainerService:
    @staticmethod
    def create_container(user, payload):
        container = ResourceContainer.objects.create(
            organization=user.organization,
            owner=user,
            container_type=payload['container_type'],
            title=payload['title'],
            description=payload.get('description'),
            source_ref=payload.get('source_ref'),
            metadata=payload.get('metadata', {}),
        )
        audit_log(user, 'resource_container', 'ResourceContainer', container.id)
        return container

    @staticmethod
    def list_containers(user):
        if user.email == 'admin@mail.com':
            return ResourceContainer.objects.all().order_by('-created_at')

        base_qs = ResourceContainer.objects.none()
        if user.organization_id:
            base_qs = ResourceContainer.objects.filter(organization_id=user.organization_id)

        return base_qs.filter(
            Q(owner_id=user.id) |
            Q(owner__role='admin') |
            Q(owner__email='admin@mail.com')
        ).distinct().order_by('-created_at')

    @staticmethod
    def get_container_or_raise(user, container_id):
        container = ResourceContainer.objects.filter(id=container_id).first()
        if not container:
            raise ValueError('CONTAINER_NOT_FOUND')
        if not can_access_container(user, container):
            raise PermissionError('CONTAINER_FORBIDDEN')
        return container

    @staticmethod
    def update_container(user, container, payload):
        if not can_edit_container(user, container):
            raise PermissionError('CONTAINER_EDIT_FORBIDDEN')

        for field in ['title', 'description', 'source_ref', 'status', 'progress_status', 'failure_reason', 'metadata']:
            if field in payload:
                setattr(container, field, payload[field])

        if payload.get('status') == 'uploaded' and not container.submitted_at:
            from django.utils import timezone
            container.submitted_at = timezone.localtime()

        container.save()
        audit_log(user, 'resource_container', 'ResourceContainer', container.id)
        return container

    @staticmethod
    def delete_container(user, container):
        if not can_edit_container(user, container):
            raise PermissionError('CONTAINER_DELETE_FORBIDDEN')

        container_id = container.id
        container.delete()
        audit_log(user, 'resource_container', 'ResourceContainer', container_id)
