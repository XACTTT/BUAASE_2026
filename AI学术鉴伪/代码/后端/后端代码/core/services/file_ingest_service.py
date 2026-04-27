import hashlib
import io
import os
import uuid
import zipfile

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import connection

from core.models import FileManagement, ImageUpload
from core.services.audit_service import audit_log
from core.services.permissions import can_upload_to_container

import fitz

class FileIngestService:
    IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}
    _schema_checked = False
    _table_columns_cache = {}
    _column_type_cache = {}
    _column_length_cache = {}

    @staticmethod
    def _table_exists(table_name: str) -> bool:
        return table_name in connection.introspection.table_names()

    @staticmethod
    def _column_exists(table_name: str, column_name: str) -> bool:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE %s", [column_name])
                return cursor.fetchone() is not None

            if vendor == 'sqlite':
                cursor.execute(f"PRAGMA table_info('{table_name}')")
                columns = cursor.fetchall()
                return any(col[1] == column_name for col in columns)

            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = %s AND column_name = %s
                """,
                [table_name, column_name],
            )
            return cursor.fetchone() is not None

    @staticmethod
    def _get_table_columns(table_name: str) -> set:
        cached = FileIngestService._table_columns_cache.get(table_name)
        if cached is not None:
            return cached

        if not FileIngestService._table_exists(table_name):
            FileIngestService._table_columns_cache[table_name] = set()
            return set()

        with connection.cursor() as cursor:
            description = connection.introspection.get_table_description(cursor, table_name)
            columns = {col.name for col in description}

        FileIngestService._table_columns_cache[table_name] = columns
        return columns

    @staticmethod
    def _get_column_type(table_name: str, column_name: str) -> str:
        cache_key = (table_name, column_name)
        if cache_key in FileIngestService._column_type_cache:
            return FileIngestService._column_type_cache[cache_key]

        if not FileIngestService._table_exists(table_name):
            FileIngestService._column_type_cache[cache_key] = ''
            return ''

        vendor = connection.vendor
        column_type = ''
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(
                    """
                    SELECT DATA_TYPE
                    FROM information_schema.columns
                    WHERE table_schema = DATABASE() AND table_name = %s AND column_name = %s
                    """,
                    [table_name, column_name],
                )
                row = cursor.fetchone()
                column_type = (row[0] if row and row[0] else '')
            elif vendor == 'sqlite':
                cursor.execute(f"PRAGMA table_info('{table_name}')")
                for row in cursor.fetchall():
                    # row: cid, name, type, notnull, dflt_value, pk
                    if len(row) >= 3 and row[1] == column_name:
                        column_type = (row[2] or '')
                        break
            else:
                cursor.execute(
                    """
                    SELECT data_type
                    FROM information_schema.columns
                    WHERE table_name = %s AND column_name = %s
                    """,
                    [table_name, column_name],
                )
                row = cursor.fetchone()
                column_type = (row[0] if row and row[0] else '')

        normalized = str(column_type).lower()
        FileIngestService._column_type_cache[cache_key] = normalized
        return normalized

    @staticmethod
    def _get_column_max_length(table_name: str, column_name: str):
        cache_key = (table_name, column_name)
        if cache_key in FileIngestService._column_length_cache:
            return FileIngestService._column_length_cache[cache_key]

        if not FileIngestService._table_exists(table_name):
            FileIngestService._column_length_cache[cache_key] = None
            return None

        vendor = connection.vendor
        max_length = None
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(
                    """
                    SELECT CHARACTER_MAXIMUM_LENGTH
                    FROM information_schema.columns
                    WHERE table_schema = DATABASE() AND table_name = %s AND column_name = %s
                    """,
                    [table_name, column_name],
                )
                row = cursor.fetchone()
                if row and row[0]:
                    max_length = int(row[0])
            elif vendor == 'sqlite':
                # SQLite 对 varchar(n) 长度通常不强约束，这里不做截断限制
                max_length = None
            else:
                cursor.execute(
                    """
                    SELECT character_maximum_length
                    FROM information_schema.columns
                    WHERE table_name = %s AND column_name = %s
                    """,
                    [table_name, column_name],
                )
                row = cursor.fetchone()
                if row and row[0]:
                    max_length = int(row[0])

        FileIngestService._column_length_cache[cache_key] = max_length
        return max_length

    @staticmethod
    def _normalize_resource_role_for_column(table_name: str, column_name: str, value):
        if value is None:
            return value

        column_type = FileIngestService._get_column_type(table_name, column_name)
        is_integer_column = any(token in column_type for token in ('int', 'integer', 'bigint', 'smallint', 'tinyint'))
        if not is_integer_column:
            return value

        if isinstance(value, int):
            return value

        role_to_code = {
            'material_other': 0,
            'paper_main': 1,
            'paper_supplementary': 2,
            'paper_revision': 3,
            'review_main': 4,
            'review_attachment': 5,
        }
        return role_to_code.get(str(value), 0)

    @staticmethod
    def _pick_existing_columns(model_cls, table_name: str, payload: dict) -> dict:
        columns = FileIngestService._get_table_columns(table_name)
        if not columns:
            return payload

        picked = {}
        for key, value in payload.items():
            try:
                field = model_cls._meta.get_field(key)
            except Exception:
                continue

            # Django ORM create 需要字段名（如 user），但是否可写入取决于底层列是否存在（如 user_id）。
            column_name = getattr(field, 'column', None)
            if column_name and column_name in columns:
                normalized_value = value
                if table_name == 'core_filemanagement' and key == 'resource_role':
                    normalized_value = FileIngestService._normalize_resource_role_for_column(
                        table_name,
                        column_name,
                        value,
                    )

                # 对实际存在长度限制的字符串列做截断，避免 Data too long 错误。
                if isinstance(normalized_value, str):
                    max_length = FileIngestService._get_column_max_length(table_name, column_name)
                    if max_length and len(normalized_value) > max_length:
                        normalized_value = normalized_value[:max_length]

                picked[key] = normalized_value

        return picked

    @staticmethod
    def _add_nullable_bigint_column(table_name: str, column_name: str) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` bigint NULL")
            elif vendor == 'sqlite':
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" integer NULL')
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" bigint NULL')

    @staticmethod
    def _add_nullable_varchar_column(table_name: str, column_name: str, length: int) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` varchar({length}) NULL")
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" varchar({length}) NULL')

    @staticmethod
    def _add_nullable_text_column(table_name: str, column_name: str) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` longtext NULL")
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" text NULL')

    @staticmethod
    def _add_nullable_boolean_column(table_name: str, column_name: str) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` tinyint(1) NULL")
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" boolean NULL')

    @staticmethod
    def _add_nullable_integer_column(table_name: str, column_name: str) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` int NULL")
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" integer NULL')

    @staticmethod
    def _add_nullable_datetime_column(table_name: str, column_name: str) -> None:
        vendor = connection.vendor
        with connection.cursor() as cursor:
            if vendor == 'mysql':
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` datetime NULL")
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" timestamp NULL')

    @staticmethod
    def _add_missing_column(table_name: str, column_name: str, column_kind: str, length: int = 0) -> None:
        if column_kind == 'bigint':
            FileIngestService._add_nullable_bigint_column(table_name, column_name)
        elif column_kind == 'varchar':
            FileIngestService._add_nullable_varchar_column(table_name, column_name, length)
        elif column_kind == 'text':
            FileIngestService._add_nullable_text_column(table_name, column_name)
        elif column_kind == 'boolean':
            FileIngestService._add_nullable_boolean_column(table_name, column_name)
        elif column_kind == 'int':
            FileIngestService._add_nullable_integer_column(table_name, column_name)
        elif column_kind == 'datetime':
            FileIngestService._add_nullable_datetime_column(table_name, column_name)

    @staticmethod
    def _ensure_backward_compatible_schema() -> None:
        if FileIngestService._schema_checked:
            return

        compatibility_columns = [
            ('core_filemanagement', 'container_id', 'bigint', 0),
            ('core_filemanagement', 'organization_id', 'bigint', 0),
            ('core_filemanagement', 'resource_role', 'varchar', 40),
            ('core_filemanagement', 'origin_type', 'varchar', 30),
            ('core_filemanagement', 'storage_path', 'varchar', 512),
            ('core_filemanagement', 'file_ext', 'varchar', 30),
            ('core_filemanagement', 'mime_type', 'varchar', 128),
            ('core_filemanagement', 'checksum', 'varchar', 128),
            ('core_filemanagement', 'parse_status', 'varchar', 20),
            ('core_filemanagement', 'parse_error', 'text', 0),
            ('core_filemanagement', 'extra_metadata', 'text', 0),
            ('core_imageupload', 'container_id', 'bigint', 0),
            ('core_imageupload', 'image_role', 'varchar', 40),
            ('core_imageupload', 'source_kind', 'varchar', 40),
            ('core_imageupload', 'file_name', 'varchar', 255),
            ('core_imageupload', 'image_index', 'int', 0),
            ('core_imageupload', 'width', 'int', 0),
            ('core_imageupload', 'height', 'int', 0),
            ('core_imageupload', 'hash_value', 'varchar', 128),
        ]

        for table_name, column_name, column_kind, column_length in compatibility_columns:
            if not FileIngestService._table_exists(table_name):
                continue

            if FileIngestService._column_exists(table_name, column_name):
                continue

            try:
                FileIngestService._add_missing_column(table_name, column_name, column_kind, column_length)
            except Exception:
                # 这里不抛出异常，保留原始错误路径，方便定位其它缺失列
                pass

            # 强制失效列缓存，避免本次启动期间仍读取旧结构
            FileIngestService._table_columns_cache = {}
            FileIngestService._column_type_cache = {}
            FileIngestService._column_length_cache = {}
        FileIngestService._schema_checked = True

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
    def _is_zip_upload(uploaded_file, content_type: str, file_ext: str) -> bool:
        zip_mime_types = {'application/zip', 'application/x-zip-compressed'}

        if content_type in zip_mime_types:
            return True

        if file_ext == 'zip':
            return True

        if content_type == 'application/octet-stream':
            position = uploaded_file.tell()
            try:
                return zipfile.is_zipfile(uploaded_file)
            finally:
                uploaded_file.seek(position)

        return False

    @staticmethod
    def _save_pil_image(image: Image.Image, relative_path: str) -> None:
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        image.save(full_path)

    @staticmethod
    def _create_image_record(file_management, container, relative_path, image_data, image_role, source_kind, image_index=None, page_number=None, extracted_from_pdf=False):
        with Image.open(io.BytesIO(image_data)) as image_obj:
            width, height = image_obj.size

        image_payload = {
            'file_management': file_management,
            'container': container,
            'image': relative_path,
            'extracted_from_pdf': extracted_from_pdf,
            'page_number': page_number,
            'image_role': image_role,
            'source_kind': source_kind,
            'file_name': os.path.basename(relative_path),
            'image_index': image_index,
            'width': width,
            'height': height,
            'hash_value': FileIngestService._image_hash(image_data),
            'isDetect': False,
            'isReview': False,
            'isFake': False,
        }
        ImageUpload.objects.create(
            **FileIngestService._pick_existing_columns(ImageUpload, 'core_imageupload', image_payload)
        )

    @staticmethod
    def _extract_images_from_pdf(file_management, container, file_path, source_kind='pdf_extracted'):

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
    def _extract_images_from_zip(file_management, container, zip_file_path):
        with zipfile.ZipFile(zip_file_path) as zip_file:
            image_counter = 0
            for member_name in zip_file.namelist():
                info = zip_file.getinfo(member_name)
                if info.is_dir():
                    continue

                lower_name = member_name.lower()
                if lower_name.endswith(('.png', '.jpg', '.jpeg')):
                    image_data = zip_file.read(member_name)
                    image_counter += 1
                    file_ext = os.path.splitext(member_name)[1].lstrip('.').lower()
                    if not file_ext or not file_ext.isalnum():
                        file_ext = 'png'
                    unique_name = f"{file_management.id}_{uuid.uuid4().hex}.{file_ext}"
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
    def _store_single_image(file_management, container, source_file_path, image_role, original_ext=None):
        with open(source_file_path, 'rb') as image_file:
            image_data = image_file.read()

        file_ext = (original_ext or os.path.splitext(source_file_path)[1].lstrip('.').lower())
        if not file_ext or not file_ext.isalnum():
            file_ext = 'png'
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        saved_relative_path = os.path.join('extracted_images', f"{file_management.id}_{unique_filename}").replace('\\', '/')
        with Image.open(io.BytesIO(image_data)) as pil_image:
            FileIngestService._save_pil_image(pil_image, saved_relative_path)

        FileIngestService._create_image_record(
            file_management=file_management,
            container=container,
            relative_path=saved_relative_path,
            image_data=image_data,
            image_role=image_role,
            source_kind='direct_image',
            image_index=1,
        )

    @staticmethod
    def ingest_upload(user, uploaded_file, container=None, resource_role='material_other', batch_id=None):
        # 历史库可能缺少 container_id 列，先做一次兼容补齐，避免上传流程直接失败。
        FileIngestService._ensure_backward_compatible_schema()

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
        full_saved_path = os.path.join(settings.MEDIA_ROOT, storage_path)

        file_payload = {
            'organization': container.organization if container else user.organization,
            'user': user,
            'container': container,
            'file_name': file_name,
            'file_size': file_size,
            'file_type': content_type,
            'resource_role': resource_role or 'material_other',
            'origin_type': 'upload',
            'storage_path': storage_path,
            'file_ext': file_ext,
            'mime_type': content_type,
            'checksum': checksum,
            'parse_status': 'validating',
            'extra_metadata': {'batch_id': batch_id} if batch_id else {},
        }
        file_management = FileManagement.objects.create(
            **FileIngestService._pick_existing_columns(FileManagement, 'core_filemanagement', file_payload)
        )

        try:
            file_columns = FileIngestService._get_table_columns('core_filemanagement')

            if 'parse_status' in file_columns:
                file_management.parse_status = 'parsing'
                file_management.save(update_fields=['parse_status'])

            if content_type == 'application/pdf' or file_ext == 'pdf':
                FileIngestService._extract_images_from_pdf(file_management, container, storage_path)
            elif FileIngestService._is_zip_upload(uploaded_file, content_type, file_ext):
                FileIngestService._extract_images_from_zip(file_management, container, full_saved_path)
            elif content_type.startswith('image/') or file_ext in FileIngestService.IMAGE_EXTENSIONS:
                FileIngestService._store_single_image(
                    file_management,
                    container,
                    full_saved_path,
                    image_role='figure',
                    original_ext=file_ext,
                )

            if 'parse_status' in file_columns:
                file_management.parse_status = 'parsed'
            if 'parse_error' in file_columns:
                file_management.parse_error = None

            success_fields = [field for field in ('parse_status', 'parse_error') if field in file_columns]
            if success_fields:
                file_management.save(update_fields=success_fields)
        except Exception as exc:
            if 'parse_status' in file_columns:
                file_management.parse_status = 'failed'
            if 'parse_error' in file_columns:
                file_management.parse_error = str(exc)

            failed_fields = [field for field in ('parse_status', 'parse_error') if field in file_columns]
            if failed_fields:
                file_management.save(update_fields=failed_fields)
            raise

        if container and container.progress_status in ('pending_upload', 'validating', 'parsing'):
            container.progress_status = 'ready'
            if container.status == 'draft':
                container.status = 'uploaded'
            container.save(update_fields=['progress_status', 'status', 'updated_at'])

        audit_log(user, 'upload', 'FileManagement', file_management.id)
        audit_log(user, 'file_bind', 'ResourceContainer' if container else 'FileManagement', container.id if container else file_management.id)

        return file_management, fs.url(storage_path)
