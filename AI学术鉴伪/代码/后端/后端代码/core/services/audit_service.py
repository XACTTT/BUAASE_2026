from core.models import Log


def audit_log(user, operation_type: str, related_model: str, related_id: int) -> None:
    if not user or not getattr(user, 'is_authenticated', False):
        return
    Log.objects.create(
        user=user,
        operation_type=operation_type,
        related_model=related_model,
        related_id=related_id,
    )
