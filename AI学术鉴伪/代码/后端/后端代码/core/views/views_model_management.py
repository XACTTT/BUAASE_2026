import json
from urllib import error as url_error
from urllib import request as url_request

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from core.models import AIModelSource, OrganizationModelConfig, ProviderModel, User
from ..utils.log_utils import action_log


def _is_software_admin(user: User) -> bool:
    return user.email == 'admin@mail.com' or (user.is_staff and user.organization is None)


def _is_organization_admin(user: User) -> bool:
    return user.is_staff and not _is_software_admin(user) and user.organization is not None


def _serialize_provider_model(model: ProviderModel) -> dict:
    return {
        'id': model.id,
        'modelId': model.model_id,
        'displayName': model.display_name,
        'module': model.module,
        'useCase': model.use_case or '',
        'description': model.description or '',
    }


def _serialize_org_model_config(config: OrganizationModelConfig) -> dict:
    provider_model = config.provider_model
    return {
        'id': config.id,
        'providerModelId': provider_model.id,
        'modelId': provider_model.model_id,
        'displayName': provider_model.display_name,
        'module': provider_model.module,
        'useCase': provider_model.use_case or '',
        'enabled': config.enabled,
        'temperature': config.temperature,
        'topP': config.top_p,
        'maxTokens': config.max_tokens,
        'description': config.description or provider_model.description or '',
        'updatedAt': timezone.localtime(config.updated_at).strftime('%Y-%m-%d %H:%M:%S'),
    }


def _serialize_source(source: AIModelSource, user: User) -> dict:
    provider_models = list(source.provider_models.filter(is_active=True))

    if user.organization is not None:
        configs = list(
            OrganizationModelConfig.objects.filter(
                organization=user.organization,
                provider_model__source=source,
            ).select_related('provider_model')
        )
    else:
        configs = []

    return {
        'id': source.id,
        'name': source.name,
        'vendor': source.vendor,
        'scope': 'global',
        'status': source.status,
        'baseUrl': source.base_url,
        'apiKey': source.api_key if _is_software_admin(user) else '',
        'defaultModel': source.default_model,
        'timeout': source.timeout,
        'retryCount': source.retry_count,
        'description': source.description or '',
        'updatedAt': timezone.localtime(source.updated_at).strftime('%Y-%m-%d %H:%M:%S'),
        'availableModels': [_serialize_provider_model(model) for model in provider_models],
        'models': [_serialize_org_model_config(config) for config in configs],
    }


def _extract_model_ids(payload: dict) -> list[str]:
    candidates = payload.get('data')
    if not isinstance(candidates, list):
        candidates = payload.get('models')

    if not isinstance(candidates, list):
        return []

    model_ids = []
    seen = set()
    for item in candidates:
        if isinstance(item, dict):
            model_id = item.get('id') or item.get('model')
        elif isinstance(item, str):
            model_id = item
        else:
            model_id = None

        if not model_id or model_id in seen:
            continue
        model_ids.append(model_id)
        seen.add(model_id)

    return model_ids


def _fetch_models_from_provider(base_url: str, api_key: str, timeout: int = 15) -> list[str]:
    endpoint = f"{base_url.rstrip('/')}/models"
    req = url_request.Request(
        endpoint,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='GET',
    )

    with url_request.urlopen(req, timeout=timeout) as response:
        body = response.read().decode('utf-8', errors='ignore')

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError('模型平台返回了非 JSON 数据') from exc

    model_ids = _extract_model_ids(payload)
    if not model_ids:
        raise ValueError('未从模型平台解析到模型列表')

    return model_ids


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_ai_models(request):
    user = request.user
    sources = AIModelSource.objects.all().order_by('-updated_at')

    return Response({
        'admin_type': 'software_admin' if _is_software_admin(user) else 'organization_admin',
        'sources': [_serialize_source(source, user) for source in sources],
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def verify_ai_model_config(request):
    source_id_raw = request.data.get('source_id')
    source = None

    if source_id_raw not in (None, ''):
        try:
            source_id = int(source_id_raw)
        except (TypeError, ValueError):
            return Response({'error': 'source_id is invalid'}, status=400)

        source = AIModelSource.objects.filter(id=source_id).first()
        if source is None:
            return Response({'error': 'Model source not found'}, status=404)

    base_url = (request.data.get('base_url') or '').strip()
    api_key = (request.data.get('api_key') or '').strip()
    model_name = (request.data.get('model_name') or '').strip()
    timeout_raw = request.data.get('timeout')

    if source is not None:
        if not base_url:
            base_url = (source.base_url or '').strip()
        if not api_key:
            api_key = (source.api_key or '').strip()
        if timeout_raw is None:
            timeout_raw = source.timeout

    if not base_url or not api_key:
        return Response({'error': 'base_url and api_key are required'}, status=400)

    try:
        timeout = int(timeout_raw or 15)
    except (TypeError, ValueError):
        timeout = 15
    timeout = timeout if timeout > 0 else 15

    try:
        model_ids = _fetch_models_from_provider(base_url, api_key, timeout=timeout)
    except (url_error.URLError, TimeoutError):
        return Response({'error': '模型平台连接失败，请检查 base_url 或网络'}, status=400)
    except ValueError as exc:
        return Response({'error': str(exc)}, status=400)

    if model_name and model_name not in model_ids:
        return Response(
            {
                'reachable': True,
                'model_exists': False,
                'message': f'连接成功，但模型 {model_name} 不在模型列表中',
                'models': model_ids,
            }
        )

    return Response(
        {
            'reachable': True,
            'model_exists': True,
            'message': '连接成功',
            'models': model_ids,
        }
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('entity_create', target_type='AIModelSource')
def add_ai_model(request):
    user = request.user
    if not _is_software_admin(user):
        return Response({'error': 'Only software admin can add model sources'}, status=403)

    required_fields = ['name', 'vendor', 'base_url', 'api_key']
    for field in required_fields:
        if not (request.data.get(field) or '').strip():
            return Response({'error': f'{field} is required'}, status=400)

    default_model = (request.data.get('default_model') or '').strip()

    source = AIModelSource.objects.create(
        name=request.data.get('name').strip(),
        vendor=request.data.get('vendor').strip(),
        base_url=request.data.get('base_url').strip(),
        api_key=request.data.get('api_key').strip(),
        default_model=default_model,
        timeout=int(request.data.get('timeout') or 30),
        retry_count=int(request.data.get('retry_count') or 2),
        description=(request.data.get('description') or '').strip(),
        status=(request.data.get('status') or 'active').strip(),
        created_by=user,
    )

    if default_model:
        ProviderModel.objects.create(
            source=source,
            model_id=source.default_model,
            display_name=source.default_model,
            module='LLM解释',
            use_case='默认模型',
            description='模型源创建时自动生成',
            is_active=True,
        )

    return Response({'message': 'Model source created', 'source': _serialize_source(source, user)}, status=201)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@action_log('entity_update', target_type='AIModelSource', target_id_field='source_id')
def update_ai_model(request, source_id: int):
    user = request.user
    if not _is_software_admin(user):
        return Response({'error': 'Only software admin can update model sources'}, status=403)

    try:
        source = AIModelSource.objects.get(id=source_id)
    except AIModelSource.DoesNotExist:
        return Response({'error': 'Model source not found'}, status=404)

    update_fields = {
        'name': 'name',
        'vendor': 'vendor',
        'base_url': 'base_url',
        'api_key': 'api_key',
        'default_model': 'default_model',
        'description': 'description',
        'status': 'status',
        'timeout': 'timeout',
        'retry_count': 'retry_count',
    }

    for request_key, model_field in update_fields.items():
        if request_key in request.data:
            value = request.data.get(request_key)
            if isinstance(value, str):
                value = value.strip()
            setattr(source, model_field, value)

    source.updated_at = timezone.localtime()
    source.save()

    return Response({'message': 'Model source updated', 'source': _serialize_source(source, user)})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@action_log('entity_delete', target_type='AIModelSource', target_id_field='source_id')
def delete_ai_model(request, source_id: int):
    user = request.user
    if not _is_software_admin(user):
        return Response({'error': 'Only software admin can delete model sources'}, status=403)

    deleted_count, _ = AIModelSource.objects.filter(id=source_id).delete()
    if deleted_count == 0:
        return Response({'error': 'Model source not found'}, status=404)

    return Response({'message': 'Model source deleted'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('model_config_change', target_type='AIModelSource', target_id_field='source_id')
def fetch_source_models(request, source_id: int):
    user = request.user
    if not _is_software_admin(user):
        return Response({'error': 'Only software admin can fetch provider models'}, status=403)

    try:
        source = AIModelSource.objects.get(id=source_id)
    except AIModelSource.DoesNotExist:
        return Response({'error': 'Model source not found'}, status=404)

    base_url_override = request.data.get('base_url')
    api_key_override = request.data.get('api_key')
    timeout_override = request.data.get('timeout')

    base_url = (base_url_override if base_url_override is not None else source.base_url or '').strip()
    api_key = (api_key_override if api_key_override is not None else source.api_key or '').strip()

    timeout_value = timeout_override if timeout_override is not None else source.timeout
    try:
        timeout = int(timeout_value or 15)
    except (TypeError, ValueError):
        timeout = source.timeout or 15
    timeout = timeout if timeout > 0 else 15

    if not base_url or not api_key:
        return Response({'error': 'base_url and api_key are required'}, status=400)

    try:
        model_ids = _fetch_models_from_provider(base_url, api_key, timeout=timeout)
    except (url_error.URLError, TimeoutError):
        return Response({'error': '模型平台连接失败，请检查 base_url 或网络'}, status=400)
    except ValueError as exc:
        return Response({'error': str(exc)}, status=400)

    source.base_url = base_url
    source.api_key = api_key
    source.timeout = timeout
    source.provider_models.all().delete()
    for model_id in model_ids:
        ProviderModel.objects.create(
            source=source,
            model_id=model_id,
            display_name=model_id,
            module='LLM解释',
            use_case='从模型平台同步',
            description='自动同步获取',
            is_active=True,
        )

    source.updated_at = timezone.localtime()
    source.save()

    return Response(
        {
            'message': f'Fetched {len(model_ids)} models',
            'availableModels': [_serialize_provider_model(model) for model in source.provider_models.filter(is_active=True)],
        }
    )


@api_view(['POST'])
@permission_classes([IsAdminUser])
@action_log('model_config_change', target_type='OrganizationModelConfig')
def add_organization_model_config(request, source_id: int):
    user = request.user
    if not _is_organization_admin(user):
        return Response({'error': 'Only organization admin can manage organization model configs'}, status=403)

    organization = user.organization
    if organization is None:
        return Response({'error': 'Organization not found for current user'}, status=400)

    provider_model_id = request.data.get('provider_model_id')
    model_id = request.data.get('model_id')

    if provider_model_id:
        provider_model = ProviderModel.objects.filter(id=provider_model_id, source_id=source_id).first()
    elif model_id:
        provider_model = ProviderModel.objects.filter(model_id=model_id, source_id=source_id).first()
    else:
        provider_model = None

    if provider_model is None:
        return Response({'error': 'provider_model_id or model_id is invalid'}, status=400)

    config, _ = OrganizationModelConfig.objects.update_or_create(
        organization=organization,
        provider_model=provider_model,
        defaults={
            'enabled': bool(request.data.get('enabled', True)),
            'temperature': float(request.data.get('temperature', 0.2)),
            'top_p': float(request.data.get('top_p', 0.9)),
            'max_tokens': int(request.data.get('max_tokens', 2048)),
            'description': (request.data.get('description') or '').strip(),
            'updated_by': user,
        },
    )

    return Response({'message': 'Organization model config added', 'config': _serialize_org_model_config(config)}, status=201)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@action_log('model_config_change', target_type='OrganizationModelConfig', target_id_field='config_id')
def update_organization_model_config(request, config_id: int):
    user = request.user
    if not _is_organization_admin(user):
        return Response({'error': 'Only organization admin can manage organization model configs'}, status=403)

    try:
        config = OrganizationModelConfig.objects.select_related('organization', 'provider_model').get(id=config_id)
    except OrganizationModelConfig.DoesNotExist:
        return Response({'error': 'Config not found'}, status=404)

    if config.organization_id != user.organization_id:
        return Response({'error': 'No permission for this config'}, status=403)

    if 'enabled' in request.data:
        config.enabled = bool(request.data.get('enabled'))
    if 'temperature' in request.data:
        config.temperature = float(request.data.get('temperature'))
    if 'top_p' in request.data:
        config.top_p = float(request.data.get('top_p'))
    if 'max_tokens' in request.data:
        config.max_tokens = int(request.data.get('max_tokens'))
    if 'description' in request.data:
        config.description = (request.data.get('description') or '').strip()

    config.updated_by = user
    config.updated_at = timezone.localtime()
    config.save()

    return Response({'message': 'Organization model config updated', 'config': _serialize_org_model_config(config)})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@action_log('model_config_change', target_type='OrganizationModelConfig', target_id_field='config_id')
def delete_organization_model_config(request, config_id: int):
    user = request.user
    if not _is_organization_admin(user):
        return Response({'error': 'Only organization admin can manage organization model configs'}, status=403)

    try:
        config = OrganizationModelConfig.objects.select_related('organization').get(id=config_id)
    except OrganizationModelConfig.DoesNotExist:
        return Response({'error': 'Config not found'}, status=404)

    if config.organization_id != user.organization_id:
        return Response({'error': 'No permission for this config'}, status=403)

    config.delete()
    return Response({'message': 'Organization model config deleted'})
