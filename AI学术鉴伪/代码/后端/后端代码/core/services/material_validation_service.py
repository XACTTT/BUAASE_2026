from core.models import FileManagement, ImageUpload, ReviewTextResource
from core.services.audit_service import audit_log


class MaterialValidationService:
    PAPER_FILE_ROLES = {'paper_main', 'paper_supplementary', 'paper_revision'}
    REVIEW_FILE_ROLES = {'review_main', 'review_attachment'}

    @staticmethod
    def validate_container_materials(user, container):
        has_images = ImageUpload.objects.filter(container=container).exists()

        has_paper_file = FileManagement.objects.filter(
            container=container,
            resource_role__in=MaterialValidationService.PAPER_FILE_ROLES,
        ).exists()

        has_review_material = (
            FileManagement.objects.filter(
                container=container,
                resource_role__in=MaterialValidationService.REVIEW_FILE_ROLES,
            ).exists()
            or ReviewTextResource.objects.filter(container=container).exists()
        )

        material_types_present = []
        if has_paper_file:
            material_types_present.append('paper')
        if has_images:
            material_types_present.append('image')
        if has_review_material:
            material_types_present.append('review')

        missing_required = []
        valid = len(material_types_present) >= 2
        if not valid:
            if not has_paper_file:
                missing_required.append('paper')
            if not (has_images or has_review_material):
                missing_required.append('image_or_review')

        result = {
            'valid': valid,
            'material_types_present': material_types_present,
            'missing_required': missing_required,
            'message': '校验通过' if valid else '至少需要两类材料',
        }

        audit_log(user, 'material_validation', 'ResourceContainer', container.id)
        return result
