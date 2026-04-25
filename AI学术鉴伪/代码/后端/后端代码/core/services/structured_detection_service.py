from django.db import transaction
from django.utils import timezone

from core.models import (
    DetectionTask,
    FileManagement,
    ImageUpload,
    ReviewTextResource,
    StructuredDetectionResult,
)
from core.services.content_extraction_service import ContentExtractionService
from core.services.material_validation_service import MaterialValidationService
from core.services.structured_ai_bridge import StructuredAIDetectionBridge


class StructuredDetectionService:
    PAPER_FILE_ROLES = {'paper_main', 'paper_supplementary', 'paper_revision'}
    REVIEW_FILE_ROLES = {'review_main', 'review_attachment'}

    @staticmethod
    def _build_paper_materials(task: DetectionTask):
        file_ids = task.extra_payload.get('file_ids', [])
        if file_ids:
            files = FileManagement.objects.filter(id__in=file_ids, user=task.user).order_by('id')
            images = ImageUpload.objects.filter(file_management_id__in=file_ids).order_by('id')
        else:
            files = FileManagement.objects.filter(
                container=task.container,
                resource_role__in=StructuredDetectionService.PAPER_FILE_ROLES,
            ).order_by('id')
            images = ImageUpload.objects.filter(container=task.container).order_by('id')

        return {
            'paper_files': [
                ContentExtractionService.serialize_file_material(file_record)
                for file_record in files
            ],
            'images': [
                ContentExtractionService.serialize_image_material(image)
                for image in images
            ],
        }

    @staticmethod
    def _build_review_materials(task: DetectionTask):
        file_ids = task.extra_payload.get('file_ids', [])
        review_text_ids = task.extra_payload.get('review_text_ids', [])

        file_queryset = FileManagement.objects.none()
        review_text_queryset = ReviewTextResource.objects.none()

        if file_ids:
            file_queryset = FileManagement.objects.filter(id__in=file_ids, user=task.user).order_by('id')
        elif task.container_id:
            file_queryset = FileManagement.objects.filter(
                container=task.container,
                resource_role__in=StructuredDetectionService.REVIEW_FILE_ROLES,
            ).order_by('id')

        if review_text_ids:
            review_text_queryset = ReviewTextResource.objects.filter(id__in=review_text_ids).order_by('id')
        elif task.container_id:
            review_text_queryset = ReviewTextResource.objects.filter(container=task.container).order_by('id')

        return {
            'review_files': [
                ContentExtractionService.serialize_file_material(file_record)
                for file_record in file_queryset
            ],
            'review_texts': [
                ContentExtractionService.serialize_review_text(item)
                for item in review_text_queryset
            ],
        }

    @staticmethod
    def _build_multi_materials(task: DetectionTask):
        validation = MaterialValidationService.validate_container_materials(task.user, task.container)

        paper_files = FileManagement.objects.filter(
            container=task.container,
            resource_role__in=StructuredDetectionService.PAPER_FILE_ROLES,
        ).order_by('id')
        review_files = FileManagement.objects.filter(
            container=task.container,
            resource_role__in=StructuredDetectionService.REVIEW_FILE_ROLES,
        ).order_by('id')
        images = ImageUpload.objects.filter(container=task.container).order_by('id')
        review_texts = ReviewTextResource.objects.filter(container=task.container).order_by('id')

        return {
            'validation': validation,
            'paper_files': [
                ContentExtractionService.serialize_file_material(item)
                for item in paper_files
            ],
            'review_files': [
                ContentExtractionService.serialize_file_material(item)
                for item in review_files
            ],
            'images': [
                ContentExtractionService.serialize_image_material(item)
                for item in images
            ],
            'review_texts': [
                ContentExtractionService.serialize_review_text(item)
                for item in review_texts
            ],
        }

    @staticmethod
    def build_input_snapshot(task: DetectionTask):
        if task.detect_type == 'paper':
            return StructuredDetectionService._build_paper_materials(task)
        if task.detect_type == 'review':
            return StructuredDetectionService._build_review_materials(task)
        if task.detect_type == 'multi':
            return StructuredDetectionService._build_multi_materials(task)
        raise ValueError('UNSUPPORTED_DETECT_TYPE')

    @staticmethod
    def build_ai_request(task: DetectionTask, snapshot):
        return {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': task.detect_type,
            'mode': task.extra_payload.get('mode'),
            'config': {
                'cmd_block_size': task.cmd_block_size,
                'urn_k': task.urn_k,
                'if_use_llm': task.if_use_llm,
            },
            'container_id': task.container_id,
            'payload': snapshot,
        }

    @staticmethod
    def _normalize_overall(ai_response):
        overall = ai_response.get('overall') or {}
        return {
            'is_fake': overall.get('is_fake'),
            'confidence_score': overall.get('confidence_score'),
            'risk_level': overall.get('risk_level'),
        }

    @staticmethod
    def _normalize_paper_result(task: DetectionTask, snapshot, ai_response):
        return {
            'overall': StructuredDetectionService._normalize_overall(ai_response),
            'task_type': 'paper',
            'material_summary': ai_response.get('material_summary') or {
                'paper_file_count': len(snapshot['paper_files']),
                'image_count': len(snapshot['images']),
            },
            'dimensions': ai_response.get('dimensions', []),
            'evidence': ai_response.get('evidence') or snapshot,
            'summary': ai_response.get('summary'),
        }

    @staticmethod
    def _normalize_review_result(task: DetectionTask, snapshot, ai_response):
        return {
            'overall': StructuredDetectionService._normalize_overall(ai_response),
            'task_type': 'review',
            'material_summary': ai_response.get('material_summary') or {
                'review_file_count': len(snapshot['review_files']),
                'review_text_count': len(snapshot['review_texts']),
            },
            'dimensions': ai_response.get('dimensions', []),
            'evidence': ai_response.get('evidence') or snapshot,
            'summary': ai_response.get('summary'),
        }

    @staticmethod
    def _normalize_multi_result(task: DetectionTask, snapshot, ai_response):
        return {
            'overall': StructuredDetectionService._normalize_overall(ai_response),
            'task_type': 'multi',
            'validation': snapshot.get('validation', {}),
            'material_cards': ai_response.get('material_cards', []),
            'cross_material_analysis': ai_response.get('cross_material_analysis', {}),
            'ai_contribution': ai_response.get('ai_contribution', []),
            'evidence': ai_response.get('evidence') or snapshot,
            'summary': ai_response.get('summary'),
        }

    @staticmethod
    def normalize_result_payload(task: DetectionTask, snapshot, ai_response):
        if task.detect_type == 'paper':
            return StructuredDetectionService._normalize_paper_result(task, snapshot, ai_response)
        if task.detect_type == 'review':
            return StructuredDetectionService._normalize_review_result(task, snapshot, ai_response)
        if task.detect_type == 'multi':
            return StructuredDetectionService._normalize_multi_result(task, snapshot, ai_response)
        raise ValueError('UNSUPPORTED_DETECT_TYPE')

    @staticmethod
    @transaction.atomic
    def store_result(task: DetectionTask, result_payload, ai_response):
        overall = result_payload.get('overall') or {}

        StructuredDetectionResult.objects.update_or_create(
            detection_task=task,
            defaults={
                'overall_is_fake': overall.get('is_fake'),
                'confidence_score': overall.get('confidence_score'),
                'summary': result_payload.get('summary') or ai_response.get('summary'),
                'result_payload': result_payload,
                'ai_response': ai_response,
            },
        )

        task.status = 'completed'
        task.completion_time = timezone.localtime()
        task.failure_reason = None
        task.save(update_fields=['status', 'completion_time', 'failure_reason'])

    @staticmethod
    def execute_task(task: DetectionTask):
        snapshot = StructuredDetectionService.build_input_snapshot(task)

        if task.detect_type == 'multi':
            validation = snapshot.get('validation', {})
            if not validation.get('valid'):
                raise ValueError(validation.get('message') or '多材料校验失败')

        ai_request = StructuredDetectionService.build_ai_request(task, snapshot)
        ai_response = StructuredAIDetectionBridge.submit(ai_request)
        result_payload = StructuredDetectionService.normalize_result_payload(task, snapshot, ai_response)
        StructuredDetectionService.store_result(task, result_payload, ai_response)
        return result_payload

    @staticmethod
    def mark_failed(task: DetectionTask, reason: str):
        task.status = 'failed'
        task.failure_reason = reason
        task.save(update_fields=['status', 'failure_reason'])
