from core.models import User


def _is_super_admin(user: User) -> bool:
    return bool(user and user.is_authenticated and user.email == 'admin@mail.com')


def _is_org_admin(user: User) -> bool:
    return bool(user and user.is_authenticated and (user.role == 'admin' or _is_super_admin(user)))


def can_access_container(user: User, container) -> bool:
    if not user or not user.is_authenticated:
        return False
    if _is_super_admin(user):
        return True
    if container.owner_id == user.id:
        return True
    if not user.organization_id or user.organization_id != container.organization_id:
        return False
    if _is_org_admin(user):
        return True
    return any(
        user.has_permission(perm_type)
        for perm_type in ['upload', 'submit', 'publish', 'review']
    )


def can_upload_to_container(user: User, container) -> bool:
    if not can_access_container(user, container):
        return False
    if _is_org_admin(user):
        return True
    return user.has_permission('upload')


def can_edit_container(user: User, container) -> bool:
    if not can_access_container(user, container):
        return False
    if _is_org_admin(user):
        return True
    return container.owner_id == user.id
