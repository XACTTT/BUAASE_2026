from django.db import connection
from core.models import Log


def _safe_create_log(payload: dict) -> None:
    """按当前数据库实际列写入日志，避免历史库缺列时中断主业务流程。"""
    try:
        table_name = Log._meta.db_table
        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(cursor, table_name)
            existing_columns = {col.name for col in description}

        filtered_payload = {}
        for field_name, value in payload.items():
            try:
                field = Log._meta.get_field(field_name)
            except Exception:
                continue

            column_name = getattr(field, 'column', None)
            if column_name and column_name in existing_columns:
                filtered_payload[field_name] = value

        if not filtered_payload:
            return

        Log.objects.create(**filtered_payload)
    except Exception:
        # 审计日志失败不应影响上传/检测等主流程
        return


def audit_log(user, operation_type: str, related_model: str, related_id: int) -> None:
    if not user or not getattr(user, 'is_authenticated', False):
        return
    _safe_create_log(
        {
            'user': user,
            'operation_type': operation_type,
            'target_type': related_model,
            'target_id': related_id,
        }
    )
