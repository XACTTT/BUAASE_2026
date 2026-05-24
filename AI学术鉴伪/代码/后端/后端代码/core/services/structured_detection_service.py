import json
import re

from django.db import transaction
from django.utils import timezone

from core.models import (
    DetectionTask,
    FileManagement,
    ImageUpload,
    LLMAnalysisRun,
    OrganizationModelConfig,
    ReviewTextResource,
    StructuredDetectionResult,
)
from core.services.content_extraction_service import ContentExtractionService
from core.services.material_validation_service import MaterialValidationService
from core.services.bert_text_ai_bridge import BertTextAIDetectionBridge, BertTextAIPermanentError
from core.services.llm_service import build_chat_completion_payload, call_openai_compatible_chat


STRUCTURED_BERT_MAX_CHARS = 900
STRUCTURED_BERT_MAX_LENGTH = 512


STAGE_PROMPT_TEMPLATES = {
    'paper': (
        '你是论文学术鉴伪专家，专精于检测学术论文中的造假、剽窃与不当行为。'
        '你将收到论文的结构化分析数据，包含整体判定、材料摘要、各维度检测结果、'
        '证据链以及AI服务器的原始响应。\n\n'
        '请重点分析以下维度：\n'
        '1. 文本原创性：是否存在AI生成文本的典型特征（重复句式、逻辑断裂、术语堆砌）\n'
        '2. 图文一致性：图片描述与实际图片内容是否吻合，图片是否来自其他论文\n'
        '3. 数据可信度：统计数据是否合理，图表是否有拼接/篡改痕迹\n'
        '4. 引用异常：参考文献是否虚构、是否与论述内容无关\n'
        '5. 结构完整性：论文章节是否完整，方法部分是否可复现\n'
        '\n\n'
        '请输出严格符合以下JSON Schema的结果：\n'
        '{\n'
        '  "summary": "综合判定摘要，2-4句话概括整体造假风险评估",\n'
        '  "risk_level": "high/medium/low",\n'
        '  "confidence": 0.0-1.0,\n'
        '  "suspicious_patterns": ["发现的可疑模式，每条80字以内"],\n'
        '  "evidence": ["关键证据项，每条引用具体数据支撑"],\n'
        '  "recommendations": ["建议的人工复核方向和进一步检测措施"]\n'
        '}'
    ),
    'review': (
        '你是学术审稿意见鉴伪专家，专精于检测同行评审中的造假、模板复用与利益冲突。'
        '你将收到评审意见的结构化分析数据，包含整体判定、材料摘要、各维度检测结果、'
        '证据链以及AI服务器的原始响应。\n\n'
        '请重点分析以下维度：\n'
        '1. 模板检测：评审意见是否为AI批量生成或模板套用（句式高度雷同、缺乏具体细节）\n'
        '2. 内容一致性：评审意见与论文实际内容是否吻合，是否存在泛泛而谈\n'
        '3. 评分合理性：评分与评语是否一致，是否存在虚高或恶意低分\n'
        '4. 时间异常：评审周期是否异常短，多个评审是否集中提交\n'
        '5. 作者-审稿人关联：是否存在审稿人与作者的潜在利益关联\n'
        '\n\n'
        '请输出严格符合以下JSON Schema的结果：\n'
        '{\n'
        '  "summary": "综合判定摘要，2-4句话概括整体可信度评估",\n'
        '  "risk_level": "high/medium/low",\n'
        '  "confidence": 0.0-1.0,\n'
        '  "signals": ["检测到的异常信号与可疑模式，每条80字以内"],\n'
        '  "consistency_issues": ["发现的一致性问题，每条引用具体证据"],\n'
        '  "recommendations": ["建议的人工复核方向和进一步调查措施"]\n'
        '}'
    ),
    'multi_material': (
        '你是多材料学术鉴伪综合专家，专精于跨材料交叉验证，综合分析论文、'
        '评审意见、图像等多源信息。你将收到各材料的检测结果、交叉分析数据和'
        'AI服务器的原始响应。\n\n'
        '请重点进行交叉验证：\n'
        '1. 跨材料一致性：论文内容与评审意见是否匹配，作者单位与评审人是否关联\n'
        '2. 图文矛盾：论文描述与图像内容是否存在明显矛盾\n'
        '3. 时间线异常：论文提交、修改、评审的时间线是否合理\n'
        '4. 多材料造假关联：是否多个材料出现同一类型的造假特征\n'
        '5. 整体风险画像：综合各维度给出总体造假可能性评估\n'
        '\n\n'
        '请输出严格符合以下JSON Schema的结果：\n'
        '{\n'
        '  "summary": "综合判定摘要，2-4句话概括跨材料交叉验证结论",\n'
        '  "risk_level": "high/medium/low",\n'
        '  "confidence": 0.0-1.0,\n'
        '  "cross_checks": ["跨材料交叉验证发现，每条引用具体矛盾或关联"],\n'
        '  "mismatches": ["发现的多材料不匹配项，每条80字以内"],\n'
        '  "recommendations": ["建议的人工复核方向和进一步调查措施"]\n'
        '}'
    ),
}


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
    def _extract_text_items_from_snapshot(snapshot, detect_type):
        items = []
        if detect_type in ('paper', 'multi'):
            for file_idx, paper_file in enumerate(snapshot.get('paper_files', [])):
                for sec_idx, section in enumerate(paper_file.get('sections', [])):
                    text = (section.get('text') or '').strip()
                    if text:
                        items.append({
                            'id': f"{detect_type}_paper_{file_idx}_{sec_idx}",
                            'text': text,
                            'language': 'chinese',
                        })
        if detect_type in ('review', 'multi'):
            for file_idx, review_file in enumerate(snapshot.get('review_files', [])):
                for sec_idx, section in enumerate(review_file.get('sections', [])):
                    text = (section.get('text') or '').strip()
                    if text:
                        items.append({
                            'id': f"{detect_type}_review_file_{file_idx}_{sec_idx}",
                            'text': text,
                            'language': 'chinese',
                        })
            for text_idx, review_text in enumerate(snapshot.get('review_texts', [])):
                text = (review_text.get('normalized_text') or review_text.get('raw_text') or '').strip()
                if text:
                    items.append({
                        'id': f"{detect_type}_review_text_{text_idx}",
                        'text': text,
                        'language': review_text.get('language', 'chinese'),
                    })
        return items

    @staticmethod
    def _split_text_for_bert(text, max_chars=STRUCTURED_BERT_MAX_CHARS):
        normalized = (text or '').replace('\r\n', '\n').replace('\r', '\n').strip()
        if not normalized:
            return []
        if len(normalized) <= max_chars:
            return [normalized]

        parts = [
            part.strip()
            for part in re.split(r'(?<=[。！？!?；;])\s*|\n\s*\n+', normalized)
            if part.strip()
        ]
        if not parts:
            parts = [normalized]

        chunks = []
        current = ''
        for part in parts:
            if len(part) > max_chars:
                if current:
                    chunks.append(current)
                    current = ''
                chunks.extend(part[index:index + max_chars] for index in range(0, len(part), max_chars))
                continue

            candidate = f'{current}\n{part}'.strip() if current else part
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = part

        if current:
            chunks.append(current)
        return [chunk for chunk in chunks if chunk.strip()]

    @staticmethod
    def _chunk_text_items_for_bert(text_items):
        chunked_items = []
        for item in text_items:
            chunks = StructuredDetectionService._split_text_for_bert(item.get('text') or '')
            if len(chunks) <= 1:
                chunked_items.append(item)
                continue

            for index, chunk in enumerate(chunks, start=1):
                chunked_items.append({
                    **item,
                    'id': f"{item.get('id')}_chunk_{index}",
                    'text': chunk,
                    'source_item_id': item.get('id'),
                    'chunk_index': index,
                    'chunk_count': len(chunks),
                })
        return chunked_items

    @staticmethod
    def _score_consistency(scores):
        if not scores or len(scores) < 2:
            return 1.0
        mean = sum(scores) / len(scores)
        if mean == 0:
            return 1.0
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        return max(0.0, min(1.0, 1.0 - (variance ** 0.5) / mean))

    @staticmethod
    def _aggregate_bert_batch(batch_response, detect_type, snapshot, text_items):
        batch_results = batch_response.get('batch_results', [])
        aggregate = batch_response.get('aggregate', {})
        n = len(batch_results)
        scores = [r.get('confidence_score', 0) for r in batch_results]
        aigc_probs = [r.get('probabilities', {}).get('aigc', 0) for r in batch_results]
        aigc_count = sum(1 for r in batch_results if r.get('is_aigc'))
        avg_aigc = aggregate.get('mean_aigc_probability', sum(aigc_probs) / n if n else 0)
        risk_level = 'high' if avg_aigc >= 0.75 else 'medium' if avg_aigc >= 0.45 else 'low'
        is_fake = avg_aigc >= 0.60

        text_lookup = {item['id']: item for item in text_items}
        section_meta = {}
        if detect_type in ('paper', 'multi'):
            for file_idx, paper_file in enumerate(snapshot.get('paper_files', [])):
                file_name = paper_file.get('file_name', '')
                for sec_idx, section in enumerate(paper_file.get('sections', [])):
                    sid = f"{detect_type}_paper_{file_idx}_{sec_idx}"
                    section_meta[sid] = {
                        'title': section.get('title', ''),
                        'page_number': section.get('page_number'),
                        'source_file': file_name,
                    }
        if detect_type in ('review', 'multi'):
            for file_idx, review_file in enumerate(snapshot.get('review_files', [])):
                file_name = review_file.get('file_name', '')
                for sec_idx, section in enumerate(review_file.get('sections', [])):
                    sid = f"{detect_type}_review_file_{file_idx}_{sec_idx}"
                    section_meta[sid] = {
                        'title': section.get('title', ''),
                        'page_number': section.get('page_number'),
                        'source_file': file_name,
                    }
            for text_idx in range(len(snapshot.get('review_texts', []))):
                sid = f"{detect_type}_review_text_{text_idx}"
                section_meta[sid] = {
                    'title': f'评审文本 {text_idx + 1}',
                    'page_number': None,
                    'source_file': '',
                }

        per_section = []
        for r in batch_results:
            item_id = r.get('item_id')
            text_item = text_lookup.get(item_id, {})
            source_item_id = text_item.get('source_item_id') or item_id
            meta = section_meta.get(source_item_id, {})
            title = meta.get('title', '')
            if text_item.get('chunk_count'):
                title = f"{title} ({text_item.get('chunk_index')}/{text_item.get('chunk_count')})".strip()
            per_section.append({
                'item_id': item_id,
                'source_item_id': source_item_id,
                'is_aigc': r.get('is_aigc'),
                'label_name': r.get('label_name'),
                'confidence_score': r.get('confidence_score'),
                'probabilities': r.get('probabilities'),
                'text': text_item.get('text', ''),
                'title': title,
                'page_number': meta.get('page_number'),
                'source_file': meta.get('source_file', ''),
            })

        consistency = StructuredDetectionService._score_consistency(scores)

        if detect_type == 'paper':
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AIGC probability aggregated across all paper sections'},
                {'name': 'section_consistency', 'score': round(consistency, 4),
                 'summary': 'Cross-section prediction consistency'},
                {'name': 'aigc_section_ratio', 'score': round(aigc_count / n, 4) if n else 0,
                 'summary': f'{aigc_count}/{n} sections classified as AIGC'},
                {'name': 'max_section_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': 'Highest single-section AIGC confidence'},
            ]
            material_summary = {
                'paper_file_count': len(snapshot.get('paper_files', [])),
                'image_count': len(snapshot.get('images', [])),
                'section_count': n,
            }
        elif detect_type == 'review':
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AIGC probability aggregated across all review texts'},
                {'name': 'template_tendency', 'score': round(aggregate.get('mean_confidence', 0), 4),
                 'summary': 'Model confidence as proxy for template/boilerplate detection'},
                {'name': 'cross_text_consistency', 'score': round(consistency, 4),
                 'summary': 'Consistency of predictions across review sources'},
                {'name': 'peak_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': 'Highest single-text AIGC risk'},
            ]
            material_summary = {
                'review_file_count': len(snapshot.get('review_files', [])),
                'review_text_count': len(snapshot.get('review_texts', [])),
                'section_count': n,
            }
        else:
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AIGC probability across all materials'},
                {'name': 'cross_material_consistency', 'score': round(consistency, 4),
                 'summary': 'Consistency across paper and review text predictions'},
                {'name': 'aigc_ratio', 'score': round(aigc_count / n, 4) if n else 0,
                 'summary': f'{aigc_count}/{n} text blocks classified as AIGC'},
                {'name': 'max_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': 'Highest single-block AIGC risk'},
            ]
            material_summary = {
                'paper_file_count': len(snapshot.get('paper_files', [])),
                'review_file_count': len(snapshot.get('review_files', [])),
                'review_text_count': len(snapshot.get('review_texts', [])),
                'image_count': len(snapshot.get('images', [])),
                'section_count': n,
            }

        return {
            'overall': {
                'is_fake': is_fake,
                'confidence_score': round(avg_aigc, 4),
                'risk_level': risk_level,
            },
            'summary': f'BERT text classification completed across {n} text sections',
            'material_summary': material_summary,
            'dimensions': dimensions,
            'evidence': {
                'model_dir': batch_response.get('model_dir'),
                'lang': batch_response.get('lang'),
                'section_count': n,
                'aigc_section_count': aigc_count,
                'aggregate': aggregate,
                'per_section': per_section,
            },
        }

    @staticmethod
    def _run_bert_detection(text_items):
        try:
            return BertTextAIDetectionBridge.submit_batch(text_items, max_length=STRUCTURED_BERT_MAX_LENGTH)
        except (BertTextAIPermanentError, IndexError) as exc:
            if not StructuredDetectionService._is_bert_batch_index_error(exc):
                raise

        batch_results = []
        model_dir = None
        base_model_dir = None
        lang = None
        for item in text_items:
            single_response = StructuredDetectionService._run_single_bert_detection(item)
            result = StructuredDetectionService._normalize_single_bert_result(item, single_response)
            batch_results.append(result)
            model_dir = model_dir or single_response.get('model_dir')
            base_model_dir = base_model_dir or single_response.get('base_model_dir')
            lang = lang or single_response.get('lang')

        if not batch_results:
            raise BertTextAIPermanentError('bert text detection returned no batch results')

        scores = [item.get('confidence_score', 0) or 0 for item in batch_results]
        aigc_probs = [item.get('probabilities', {}).get('aigc', 0) or 0 for item in batch_results]
        n = len(batch_results)
        return {
            'batch_results': batch_results,
            'item_count': n,
            'aggregate': {
                'aigc_ratio': sum(1 for item in batch_results if item.get('is_aigc')) / n if n else 0.0,
                'mean_aigc_probability': sum(aigc_probs) / n if n else 0.0,
                'mean_confidence': sum(scores) / n if n else 0.0,
                'max_confidence': max(scores) if scores else 0.0,
                'min_confidence': min(scores) if scores else 0.0,
            },
            'model_dir': model_dir,
            'base_model_dir': base_model_dir,
            'lang': lang,
            'fallback': 'single_item_after_batch_index_error',
        }

    @staticmethod
    def _is_bert_batch_index_error(exc):
        return isinstance(exc, IndexError) or 'list index out of range' in str(exc)

    @staticmethod
    def _run_single_bert_detection(item):
        try:
            return BertTextAIDetectionBridge.submit_batch([item], max_length=STRUCTURED_BERT_MAX_LENGTH)
        except (BertTextAIPermanentError, IndexError) as exc:
            if not StructuredDetectionService._is_bert_batch_index_error(exc):
                raise

        try:
            return BertTextAIDetectionBridge.submit_text(
                item.get('text') or '',
                language=item.get('language'),
                max_length=STRUCTURED_BERT_MAX_LENGTH,
            )
        except (BertTextAIPermanentError, IndexError) as exc:
            if not StructuredDetectionService._is_bert_batch_index_error(exc):
                raise
            text = item.get('text') or ''
            raise BertTextAIPermanentError(
                f"bert single text failed with list index out of range; "
                f"item_id={item.get('id')}, source_item_id={item.get('source_item_id')}, "
                f"text_length={len(text)}, max_length={STRUCTURED_BERT_MAX_LENGTH}"
            ) from exc

    @staticmethod
    def _normalize_single_bert_result(item, single_response):
        if not isinstance(single_response, dict):
            raise BertTextAIPermanentError('bert text detection returned invalid single result')

        batch_results = single_response.get('batch_results')
        if isinstance(batch_results, list) and batch_results:
            result = dict(batch_results[0])
        elif isinstance(single_response.get('items'), list) and single_response['items']:
            result = BertTextAIDetectionBridge._normalize_batch_result_item(single_response['items'][0])
        else:
            result = dict(single_response)

        result['item_id'] = result.get('item_id') or item.get('id')
        probabilities = result.get('probabilities') or {}
        result['probabilities'] = probabilities
        result['input_summary'] = result.get('input_summary') or {}

        if result.get('confidence_score') is None:
            probability_values = [value for value in probabilities.values() if isinstance(value, (int, float))]
            result['confidence_score'] = max(probability_values) if probability_values else 0.0

        if result.get('is_aigc') is None:
            label = str(result.get('label_name') or result.get('label') or '').strip().lower()
            result['is_aigc'] = label in {'aigc', 'ai', 'generated', 'machine'}

        if not result.get('label_name'):
            result['label_name'] = 'aigc' if result.get('is_aigc') else 'human'

        return result

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
    def _resolve_llm_config(task: DetectionTask):
        if not task.organization_id:
            return None

        return OrganizationModelConfig.objects.filter(
            organization_id=task.organization_id,
            enabled=True,
            provider_model__is_active=True,
            provider_model__source__status='active',
        ).select_related('provider_model', 'provider_model__source').order_by('-updated_at').first()

    @staticmethod
    def _build_llm_prompt(task: DetectionTask):
        if task.detect_type == 'paper':
            return STAGE_PROMPT_TEMPLATES['paper']
        if task.detect_type == 'review':
            return STAGE_PROMPT_TEMPLATES['review']
        if task.detect_type == 'multi':
            return STAGE_PROMPT_TEMPLATES['multi_material']
        return None

    @staticmethod
    def _run_llm_analysis(task: DetectionTask, result_payload, ai_response, text_items=None):
        config = StructuredDetectionService._resolve_llm_config(task)
        if config is None:
            return None

        provider_model = config.provider_model
        source = provider_model.source
        prompt = StructuredDetectionService._build_llm_prompt(task)
        if not prompt:
            return None

        input_payload = {
            'task_id': task.id,
            'task_name': task.task_name,
            'detect_type': task.detect_type,
            'result_payload': result_payload,
            'ai_response': ai_response,
        }
        if text_items:
            input_payload['original_texts'] = text_items

        messages = [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': f"input_payload:\n{json.dumps(input_payload, ensure_ascii=False, indent=2)}"},
        ]

        payload = build_chat_completion_payload(
            model=provider_model.model_id,
            messages=messages,
            temperature=float(config.temperature),
            top_p=float(config.top_p),
            max_tokens=int(config.max_tokens),
        )

        run_record = LLMAnalysisRun.objects.create(
            task=task,
            model_config=config,
            stage=task.detect_type,
            prompt=prompt,
            messages=messages,
            input_payload=input_payload,
            status='pending',
            created_by=task.user,
        )

        try:
            result = call_openai_compatible_chat(
                base_url=source.base_url,
                api_key=source.api_key,
                payload=payload,
                timeout=int(source.timeout or 30),
            )
        except (OSError, ValueError) as exc:
            run_record.status = 'failed'
            run_record.error_message = str(exc)
            run_record.save(update_fields=['status', 'error_message', 'updated_at'])
            return None

        content = None
        try:
            content = result['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError):
            content = None

        parsed = None
        if isinstance(content, str):
            # 清洗 markdown 代码块包裹
            cleaned = content.strip()
            if cleaned.startswith('```'):
                lines = cleaned.splitlines()
                # 去掉首行 ```json 和末行的 ```
                if len(lines) >= 2:
                    lines = lines[1:]
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                cleaned = '\n'.join(lines)
            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                parsed = None

        run_record.status = 'success'
        run_record.output_text = content
        if isinstance(parsed, dict):
            run_record.output_json = parsed
        run_record.save(update_fields=['status', 'output_text', 'output_json', 'updated_at'])

        return parsed if isinstance(parsed, dict) else {'raw_text': content}

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

        text_items = StructuredDetectionService._extract_text_items_from_snapshot(snapshot, task.detect_type)
        text_items = StructuredDetectionService._chunk_text_items_for_bert(text_items)
        if not text_items:
            raise ValueError(f'No extractable text found for detect_type={task.detect_type}')
        batch_response = StructuredDetectionService._run_bert_detection(text_items)
        ai_response = StructuredDetectionService._aggregate_bert_batch(
            batch_response, task.detect_type, snapshot, text_items
        )
        result_payload = StructuredDetectionService.normalize_result_payload(task, snapshot, ai_response)

        # 标记"大模型分析中"
        task.status = 'analyzing'
        task.save(update_fields=['status'])

        # 发送进度通知 (lazy import 避免循环依赖)
        from core.tasks_new import send_task_progress_update
        send_task_progress_update(
            task_id=task.id,
            status='analyzing',
            progress=85,
            message='正在进行大模型综合智能分析...'
        )

        llm_result = StructuredDetectionService._run_llm_analysis(task, result_payload, ai_response, text_items)
        if llm_result is not None:
            result_payload['llm_analysis'] = llm_result
        StructuredDetectionService.store_result(task, result_payload, ai_response)
        return result_payload

    @staticmethod
    def mark_failed(task: DetectionTask, reason: str):
        task.status = 'failed'
        task.failure_reason = reason
        task.save(update_fields=['status', 'failure_reason'])
