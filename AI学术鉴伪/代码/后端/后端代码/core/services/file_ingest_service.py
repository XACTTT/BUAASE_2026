import hashlib
import io
import os
import uuid
import zipfile

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from core.models import FileManagement, ImageUpload
from core.services.audit_service import audit_log
from core.services.permissions import can_upload_to_container


class FileIngestService:
    @staticmethod
    def _checksum_for_upload(uploaded_file):
        sha256 = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            sha256.update(chunk)
        uploaded_file.seek(0)
        return sha256.hexdigest()

    @staticmethod
    def _image_hash(image_data: bytes) -> str:
        return hashlib.sha256(image_data).hexdigest()

    @staticmethod
    def _save_pil_image(image: Image.Image, relative_path: str) -> None:
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        image.save(full_path)

    @staticmethod
    def _create_image_record(file_management, container, relative_path, image_data, image_role, source_kind, image_index=None, page_number=None, extracted_from_pdf=False):
        with Image.open(io.BytesIO(image_data)) as image_obj:
            width, height = image_obj.size

        ImageUpload.objects.create(
            file_management=file_management,
            container=container,
            image=relative_path,
            extracted_from_pdf=extracted_from_pdf,
            page_number=page_number,
            image_role=image_role,
            source_kind=source_kind,
            file_name=os.path.basename(relative_path),
            image_index=image_index,
            width=width,
            height=height,
            hash_value=FileIngestService._image_hash(image_data),
            isDetect=False,
            isReview=False,
            isFake=False,
        )

    @staticmethod
    def _extract_images_from_pdf(file_management, container, file_path, source_kind='pdf_extracted'):
        import fitz

        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        with fitz.open(full_file_path) as pdf_document:
            image_counter = 0
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)
                image_list = page.get_images(full=True)
                for idx, img in enumerate(image_list):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image['image']
                    image_ext = base_image.get('ext', 'png')
                    image_counter += 1
                    image_filename = f"{file_management.id}_page{page_number + 1}_image{idx + 1}.{image_ext}"
                    unique_image_name = f"{uuid.uuid4().hex}_{image_filename}"
                    relative_path = os.path.join('extracted_images', unique_image_name).replace('\\', '/')

                    with Image.open(io.BytesIO(image_bytes)) as pil_image:
                        FileIngestService._save_pil_image(pil_image, relative_path)

                    FileIngestService._create_image_record(
                        file_management=file_management,
                        container=container,
                        relative_path=relative_path,
                        image_data=image_bytes,
                        image_role='figure',
                        source_kind=source_kind,
                        image_index=image_counter,
                        page_number=page_number + 1,
                        extracted_from_pdf=True,
                    )

    @staticmethod
    def _extract_images_from_zip(file_management, container, uploaded_file):
        with zipfile.ZipFile(uploaded_file) as zip_file:
            image_counter = 0
            for member_name in zip_file.namelist():
                info = zip_file.getinfo(member_name)
                if info.is_dir():
                    continue

                lower_name = member_name.lower()
                if lower_name.endswith(('.png', '.jpg', '.jpeg')):
                    image_data = zip_file.read(member_name)
                    image_counter += 1
                    image_filename = f"{file_management.id}_{os.path.basename(member_name)}"
                    unique_name = f"{uuid.uuid4().hex}_{image_filename}"
                    relative_path = os.path.join('extracted_images', unique_name).replace('\\', '/')

                    with Image.open(io.BytesIO(image_data)) as pil_image:
                        FileIngestService._save_pil_image(pil_image, relative_path)

                    FileIngestService._create_image_record(
                        file_management=file_management,
                        container=container,
                        relative_path=relative_path,
                        image_data=image_data,
                        image_role='figure',
                        source_kind='zip_image',
                        image_index=image_counter,
                    )
                elif lower_name.endswith('.pdf'):
                    temp_pdf_dir = os.path.join(settings.MEDIA_ROOT, 'temp_pdfs')
                    os.makedirs(temp_pdf_dir, exist_ok=True)
                    temp_pdf_filename = f"{uuid.uuid4().hex}.pdf"
                    temp_pdf_path = os.path.join(temp_pdf_dir, temp_pdf_filename)
                    with open(temp_pdf_path, 'wb') as temp_file:
                        temp_file.write(zip_file.read(member_name))

                    try:
                        relative_temp_path = os.path.join('temp_pdfs', temp_pdf_filename)
                        FileIngestService._extract_images_from_pdf(
                            file_management=file_management,
                            container=container,
                            file_path=relative_temp_path,
                            source_kind='zip_pdf_extracted',
                        )
                    finally:
                        if os.path.exists(temp_pdf_path):
                            os.remove(temp_pdf_path)

    @staticmethod
    def _store_single_image(file_management, container, uploaded_file, image_role):
        image_data = uploaded_file.read()
        uploaded_file.seek(0)

        unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
        relative_path = os.path.join('extracted_images', f"{file_management.id}_{unique_filename}").replace('\\', '/')
        fs = FileSystemStorage()
        fs.save(relative_path, uploaded_file)

        FileIngestService._create_image_record(
            file_management=file_management,
            container=container,
            relative_path=relative_path,
            image_data=image_data,
            image_role=image_role,
            source_kind='direct_image',
            image_index=1,
        )

    @staticmethod
    def ingest_upload(user, uploaded_file, container=None, resource_role='material_other', batch_id=None):
        if container and not can_upload_to_container(user, container):
            raise PermissionError('CONTAINER_UPLOAD_FORBIDDEN')

        file_name = uploaded_file.name
        file_size = uploaded_file.size
        content_type = uploaded_file.content_type or ''
        file_ext = os.path.splitext(file_name)[1].lstrip('.').lower()

        checksum = FileIngestService._checksum_for_upload(uploaded_file)

        unique_filename = f"{uuid.uuid4().hex}_{file_name}"
        fs = FileSystemStorage()
        storage_path = fs.save(f'uploads/{unique_filename}', uploaded_file)

        file_management = FileManagement.objects.create(
            organization=container.organization if container else user.organization,
            user=user,
            container=container,
            file_name=file_name,
            file_size=file_size,
            file_type=content_type,
            resource_role=resource_role or 'material_other',
            origin_type='upload',
            storage_path=storage_path,
            file_ext=file_ext,
            mime_type=content_type,
            checksum=checksum,
            parse_status='validating',
            extra_metadata={'batch_id': batch_id} if batch_id else {},
        )

        try:
            file_management.parse_status = 'parsing'
            file_management.save(update_fields=['parse_status'])

            if content_type == 'application/pdf':
                FileIngestService._extract_images_from_pdf(file_management, container, storage_path)
            elif content_type in ('application/zip', 'application/x-zip-compressed', 'application/octet-stream'):
                uploaded_file.seek(0)
                FileIngestService._extract_images_from_zip(file_management, container, uploaded_file)
            elif content_type.startswith('image/'):
                uploaded_file.seek(0)
                FileIngestService._store_single_image(file_management, container, uploaded_file, image_role='figure')

            file_management.parse_status = 'parsed'
            file_management.parse_error = None
            file_management.save(update_fields=['parse_status', 'parse_error'])
        except Exception as exc:
            file_management.parse_status = 'failed'
            file_management.parse_error = str(exc)
            file_management.save(update_fields=['parse_status', 'parse_error'])
            raise

        if container and container.progress_status in ('pending_upload', 'validating', 'parsing'):
            container.progress_status = 'ready'
            if container.status == 'draft':
                container.status = 'uploaded'
            container.save(update_fields=['progress_status', 'status', 'updated_at'])

        audit_log(user, 'upload', 'FileManagement', file_management.id)
        audit_log(user, 'file_bind', 'ResourceContainer' if container else 'FileManagement', container.id if container else file_management.id)

        return file_management, fs.url(storage_path)
