import functools
import json
from django.utils import timezone
from ..models import Log
from rest_framework.response import Response

def get_client_ip(request):
    """获取客户端真实IP"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_action(user, operation_type, target_type=None, target_id=None, detail=None, ip=None, result='success', error_msg=None):
    """
    手动记录日志的辅助函数
    """
    if not user or user.is_anonymous:
        return None
    
    try:
        # 转换 detail 为 JSON 兼容格式
        if detail and not isinstance(detail, (dict, list)):
            detail = {"info": str(detail)}

        log = Log.objects.create(
            user=user,
            user_role=getattr(user, 'role', 'unknown'),
            operation_type=operation_type,
            target_type=target_type,
            target_id=target_id,
            operation_detail=detail,
            ip_address=ip,
            result=result,
            error_msg=error_msg,
            operation_time=timezone.now()
        )
        return log
    except Exception as e:
        print(f"Error creating log: {e}")
        return None

def action_log(operation_type, target_type=None, target_id_field=None):
    """
    用于视图函数记录操作日志的装饰器
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 处理 DRF 视图方法 (self, request, ...) 或普通视图函数 (request, ...)
            if len(args) > 1:
                request = args[1]
            else:
                request = args[0]
                
            user = getattr(request, 'user', None)
            ip = get_client_ip(request)
            
            try:
                response = func(*args, **kwargs)
                
                # 记录成功操作 (HTTP 2xx 或 3xx)
                if isinstance(response, Response) and response.status_code < 400:
                    t_id = None
                    # 尝试从 kwargs 或 response.data 中提取 target_id
                    if target_id_field:
                        if target_id_field in kwargs:
                            t_id = kwargs[target_id_field]
                        elif hasattr(response, 'data') and isinstance(response.data, dict) and target_id_field in response.data:
                            t_id = response.data[target_id_field]
                    
                    log_action(
                        user=user,
                        operation_type=operation_type,
                        target_type=target_type,
                        target_id=t_id,
                        ip=ip,
                        result='success',
                        detail={'method': request.method, 'path': request.path}
                    )
                # 记录失败操作 (HTTP 4xx 或 5xx)
                elif isinstance(response, Response) and response.status_code >= 400:
                    log_action(
                        user=user,
                        operation_type=operation_type,
                        target_type=target_type,
                        ip=ip,
                        result='failure',
                        error_msg=str(response.data) if hasattr(response, 'data') else 'Error status code',
                        detail={'method': request.method, 'path': request.path, 'status_code': response.status_code}
                    )
                
                return response
                
            except Exception as e:
                # 记录异常导致的失败
                log_action(
                    user=user,
                    operation_type=operation_type,
                    target_type=target_type,
                    ip=ip,
                    result='failure',
                    error_msg=str(e),
                    detail={'method': request.method, 'path': request.path, 'exception': type(e).__name__}
                )
                raise e
        return wrapper
    return decorator