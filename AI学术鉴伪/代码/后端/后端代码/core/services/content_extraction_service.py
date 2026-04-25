import os
import re
import zipfile
from xml.etree import ElementTree

import fitz
from django.conf import settings

from core.models import FileManagement, ImageUpload, ReviewTextResource


class ContentExtractionService:
    TEXT_FILE_EXTENSIONS = {'pdf', 'txt', 'docx', 'doc'}

    @staticmethod
    def _normalize_text(raw_text: str) -> str:
        lines = [line.strip() for line in raw_text.splitlines()]
        cleaned = '\n'.join(line for line in lines if line)
        return cleaned.strip()

    @staticmethod
    def _split_text_blocks(text: str, fallback_title: str):
        normalized = ContentExtractionService._normalize_text(text)
        if not normalized:
            return []

        paragraphs = [chunk.strip() for chunk in re.split(r'\n{2,}', normalized) if chunk.strip()]
        if not paragraphs:
            return [{
                'title': fallback_title,
                'text': normalized,
                'source': 'normalized_text',
            }]

        return [
            {
                'title': f'{fallback_title}-{index + 1}',
                'text': paragraph,
                'source': 'normalized_text',
            }
            for index, paragraph in enumerate(paragraphs)
        ]

    @staticmethod
    def _read_text_file(full_path: str):
        for encoding in ('utf-8', 'utf-8-sig', 'gb18030', 'latin1'):
            try:
                with open(full_path, 'r', encoding=encoding) as handle:
                    return handle.read()
            except UnicodeDecodeError:
                continue

        with open(full_path, 'rb') as handle:
            return handle.read().decode('latin1', errors='ignore')

    @staticmethod
    def _extract_pdf_sections(full_path: str):
        sections = []
        with fitz.open(full_path) as pdf_document:
            for page_idx in range(pdf_document.page_count):
                text = pdf_document.load_page(page_idx).get_text('text').strip()
                if not text:
                    continue
                sections.append({
                    'title': f'第{page_idx + 1}页',
                    'text': ContentExtractionService._normalize_text(text),
                    'source': 'pdf_extracted',
                    'page_number': page_idx + 1,
                })
        return sections

    @staticmethod
    def _extract_docx_sections(full_path: str):
        with zipfile.ZipFile(full_path, 'r') as archive:
            xml_data = archive.read('word/document.xml')

        root = ElementTree.fromstring(xml_data)
        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        paragraphs = []

        for paragraph in root.findall('.//w:p', namespaces):
            texts = [
                node.text for node in paragraph.findall('.//w:t', namespaces)
                if node.text
            ]
            merged = ''.join(texts).strip()
            if merged:
                paragraphs.append(merged)

        return [
            {
                'title': f'段落{index + 1}',
                'text': ContentExtractionService._normalize_text(paragraph),
                'source': 'docx_extracted',
            }
            for index, paragraph in enumerate(paragraphs)
        ]

    @staticmethod
    def extract_text_sections_from_file(file_record: FileManagement):
        storage_path = file_record.storage_path
        if not storage_path:
            return []

        full_path = os.path.join(settings.MEDIA_ROOT, storage_path)
        if not os.path.exists(full_path):
            return []

        file_ext = (file_record.file_ext or '').lower()
        if file_ext == 'pdf':
            return ContentExtractionService._extract_pdf_sections(full_path)
        if file_ext == 'txt':
            raw_text = ContentExtractionService._read_text_file(full_path)
            return ContentExtractionService._split_text_blocks(raw_text, '文本')
        if file_ext == 'docx':
            try:
                return ContentExtractionService._extract_docx_sections(full_path)
            except (KeyError, ElementTree.ParseError, zipfile.BadZipFile):
                return []
        if file_ext == 'doc':
            raw_text = ContentExtractionService._read_text_file(full_path)
            return ContentExtractionService._split_text_blocks(raw_text, 'DOC文本')

        return []

    @staticmethod
    def serialize_file_material(file_record: FileManagement):
        sections = ContentExtractionService.extract_text_sections_from_file(file_record)
        return {
            'file_id': file_record.id,
            'file_name': file_record.file_name,
            'resource_role': file_record.resource_role,
            'file_ext': file_record.file_ext,
            'parse_status': file_record.parse_status,
            'sections': sections,
        }

    @staticmethod
    def serialize_image_material(image: ImageUpload):
        image_url = image.image.url if image.image else None
        return {
            'image_id': image.id,
            'file_management_id': image.file_management_id,
            'image_role': image.image_role,
            'source_kind': image.source_kind,
            'page_number': image.page_number,
            'image_url': image_url,
            'width': image.width,
            'height': image.height,
        }

    @staticmethod
    def serialize_review_text(review_text: ReviewTextResource):
        return {
            'review_text_id': review_text.id,
            'source_type': review_text.source_type,
            'language': review_text.language,
            'token_count': review_text.token_count,
            'normalized_text': review_text.normalized_text or '',
            'raw_text': review_text.raw_text,
        }
