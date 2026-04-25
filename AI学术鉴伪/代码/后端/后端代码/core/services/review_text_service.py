from core.models import ReviewTextResource
from core.services.audit_service import audit_log


class ReviewTextService:
    MAX_RAW_TEXT_LENGTH = 50000

    @staticmethod
    def _normalize_text(raw_text: str) -> str:
        return '\n'.join(line.strip() for line in raw_text.splitlines()).strip()

    @staticmethod
    def create_review_text(user, container, payload):
        if container.container_type not in {'review', 'multi_material'}:
            raise ValueError('INVALID_CONTAINER_TYPE')

        raw_text = (payload.get('raw_text') or '').strip()
        if not raw_text:
            raise ValueError('EMPTY_REVIEW_TEXT')
        if len(raw_text) > ReviewTextService.MAX_RAW_TEXT_LENGTH:
            raise ValueError('REVIEW_TEXT_TOO_LARGE')

        normalized_text = ReviewTextService._normalize_text(raw_text)
        token_count = len(normalized_text.split())

        review_text = ReviewTextResource.objects.create(
            container=container,
            source_type=payload.get('source_type', 'paste'),
            language=payload.get('language', 'zh'),
            raw_text=raw_text,
            normalized_text=normalized_text,
            token_count=token_count,
            parse_status='parsed',
        )

        audit_log(user, 'review_text', 'ReviewTextResource', review_text.id)
        return review_text

    @staticmethod
    def list_review_texts(container):
        return ReviewTextResource.objects.filter(container=container).order_by('-created_at')
