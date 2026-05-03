import os
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_chat_test_files(request):
    uploaded_files = request.FILES.getlist('file')
    if not uploaded_files:
        return Response({'error': 'file is required'}, status=400)

    upload_dir = os.path.join(settings.MEDIA_ROOT, 'chat_test_uploads')
    os.makedirs(upload_dir, exist_ok=True)
    storage = FileSystemStorage(location=upload_dir)

    results = []
    for uploaded_file in uploaded_files:
        token = uuid.uuid4().hex
        filename = f"{token}_{uploaded_file.name}"
        stored_name = storage.save(filename, uploaded_file)
        rel_path = f"chat_test_uploads/{stored_name}"
        results.append({
            'file_token': token,
            'file_name': uploaded_file.name,
            'file_path': rel_path,
            'file_url': request.build_absolute_uri(f"{settings.MEDIA_URL}{rel_path}"),
            'size': uploaded_file.size,
        })

    return Response({
        'message': 'Files uploaded',
        'files': results,
    })
