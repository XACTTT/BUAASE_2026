import json

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
from core.services.bert_text_ai_bridge import BertTextAIDetectionBridge
from core.services.llm_service import build_chat_completion_payload, call_openai_compatible_chat


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

        file_ids = task.extra_payload.get('file_ids', [])
        review_text_ids = task.extra_payload.get('review_text_ids', [])

        if file_ids:
            paper_files = FileManagement.objects.filter(
                id__in=file_ids,
                resource_role__in=StructuredDetectionService.PAPER_FILE_ROLES,
            ).order_by('id')
            review_files = FileManagement.objects.filter(
                id__in=file_ids,
                resource_role__in=StructuredDetectionService.REVIEW_FILE_ROLES,
            ).order_by('id')
            images = ImageUpload.objects.filter(file_management_id__in=file_ids).order_by('id')
        else:
            paper_files = FileManagement.objects.filter(
                container=task.container,
                resource_role__in=StructuredDetectionService.PAPER_FILE_ROLES,
            ).order_by('id')
            review_files = FileManagement.objects.filter(
                container=task.container,
                resource_role__in=StructuredDetectionService.REVIEW_FILE_ROLES,
            ).order_by('id')
            images = ImageUpload.objects.filter(container=task.container).order_by('id')

        if review_text_ids:
            review_texts = ReviewTextResource.objects.filter(id__in=review_text_ids).order_by('id')
        else:
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
            meta = section_meta.get(item_id, {})
            per_section.append({
                'item_id': item_id,
                'is_aigc': r.get('is_aigc'),
                'label_name': r.get('label_name'),
                'confidence_score': r.get('confidence_score'),
                'probabilities': r.get('probabilities'),
                'text': text_item.get('text', ''),
                'title': meta.get('title', ''),
                'page_number': meta.get('page_number'),
                'source_file': meta.get('source_file', ''),
            })

        consistency = StructuredDetectionService._score_consistency(scores)

        if detect_type == 'paper':
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AI生成概率（论文全文段落汇总）'},
                {'name': 'section_consistency', 'score': round(consistency, 4),
                 'summary': '各段落预测结果的一致性'},
                {'name': 'aigc_section_ratio', 'score': round(aigc_count / n, 4) if n else 0,
                 'summary': f'{aigc_count}/{n} 个段落被分类为AI生成'},
                {'name': 'max_section_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': '单段落最高AI生成置信度'},
            ]
            material_summary = {
                'paper_file_count': len(snapshot.get('paper_files', [])),
                'image_count': len(snapshot.get('images', [])),
                'section_count': n,
            }
        elif detect_type == 'review':
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AI生成概率（评审文本汇总）'},
                {'name': 'template_tendency', 'score': round(aggregate.get('mean_confidence', 0), 4),
                 'summary': '模型置信度（模板化/套话检测代理指标）'},
                {'name': 'cross_text_consistency', 'score': round(consistency, 4),
                 'summary': '各评审来源预测结果的一致性'},
                {'name': 'peak_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': '单文本最高AI生成风险'},
            ]
            material_summary = {
                'review_file_count': len(snapshot.get('review_files', [])),
                'review_text_count': len(snapshot.get('review_texts', [])),
                'section_count': n,
            }
        else:
            dimensions = [
                {'name': 'aigc_generation', 'score': round(avg_aigc, 4),
                 'summary': 'BERT AI生成概率（全部材料汇总）'},
                {'name': 'cross_material_consistency', 'score': round(consistency, 4),
                 'summary': '论文与评审文本预测结果的一致性'},
                {'name': 'aigc_ratio', 'score': round(aigc_count / n, 4) if n else 0,
                 'summary': f'{aigc_count}/{n} 个文本段被分类为AI生成'},
                {'name': 'max_risk', 'score': round(max(scores) if scores else 0, 4),
                 'summary': '单段最高AI生成风险'},
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
            'summary': f'BERT文本分类完成，共检测 {n} 个文本段落',
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
        evidence_per_section = (ai_response.get('evidence') or {}).get('per_section', [])
        material_cards = []

        # Paper card
        paper_files = snapshot.get('paper_files', [])
        if paper_files:
            paper_sections = [s for s in evidence_per_section
                              if (s.get('item_id') or '').startswith('multi_paper')]
            paper_scores = [s.get('probabilities', {}).get('aigc', 0) for s in paper_sections]
            avg_paper_score = sum(paper_scores) / len(paper_scores) if paper_scores else 0
            total_sections = sum(len(pf.get('sections', [])) for pf in paper_files)
            material_cards.append({
                'type': 'paper',
                'label': '论文材料',
                'summary': f'{len(paper_files)} 篇论文，共 {total_sections} 个章节',
                'score': round(avg_paper_score, 4),
                'file_count': len(paper_files),
                'files': [
                    {'file_id': pf.get('file_id'), 'file_name': pf.get('file_name')}
                    for pf in paper_files
                ],
            })

        # Review card
        review_files = snapshot.get('review_files', [])
        review_texts = snapshot.get('review_texts', [])
        if review_files or review_texts:
            review_sections = [s for s in evidence_per_section
                               if (s.get('item_id') or '').startswith('multi_review')]
            review_scores = [s.get('probabilities', {}).get('aigc', 0) for s in review_sections]
            avg_review_score = sum(review_scores) / len(review_scores) if review_scores else 0
            material_cards.append({
                'type': 'review',
                'label': '评审材料',
                'summary': f'{len(review_files)} 个评审文件，{len(review_texts)} 段评审文本',
                'score': round(avg_review_score, 4),
                'file_count': len(review_files) + len(review_texts),
                'files': [
                    {'file_id': rf.get('file_id'), 'file_name': rf.get('file_name')}
                    for rf in review_files
                ],
            })

        # Image card
        images = snapshot.get('images', [])
        if images:
            image_ids = [img.get('image_id') for img in images if img.get('image_id')]
            detection_map = {}
            if image_ids:
                for dr in DetectionResult.objects.filter(
                    image_upload_id__in=image_ids, status='completed'
                ):
                    detection_map[dr.image_upload_id] = dr

            image_items = []
            for img in images:
                item = {
                    'image_id': img.get('image_id'),
                    'image_url': img.get('image_url'),
                }
                dr = detection_map.get(img.get('image_id'))
                if dr:
                    item['result_id'] = dr.id
                    item['is_fake'] = dr.is_fake
                    item['confidence'] = float(dr.confidence_score) if dr.confidence_score else 0
                image_items.append(item)

            material_cards.append({
                'type': 'image',
                'label': '图片材料',
                'summary': f'{len(images)} 张图片',
                'file_count': len(images),
                'images': image_items,
            })

        return {
            'overall': StructuredDetectionService._normalize_overall(ai_response),
            'task_type': 'multi',
            'validation': snapshot.get('validation', {}),
            'material_cards': material_cards,
            'cross_material_analysis': None,
            'ai_contribution': [],
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
    def _build_basic_cross_analysis(result_payload, ai_response):
        """当LLM不可用时，从BERT结果生成基础交叉分析。"""
        evidence = result_payload.get('evidence') or ai_response.get('evidence') or {}
        per_section = evidence.get('per_section', [])

        paper_aigc = [s for s in per_section if (s.get('item_id') or '').startswith('multi_paper') and s.get('is_aigc')]
        review_aigc = [s for s in per_section if (s.get('item_id') or '').startswith('multi_review') and s.get('is_aigc')]
        paper_total = [s for s in per_section if (s.get('item_id') or '').startswith('multi_paper')]
        review_total = [s for s in per_section if (s.get('item_id') or '').startswith('multi_review')]

        cross_checks = []
        paper_rate = len(paper_aigc) / max(len(paper_total), 1)
        review_rate = len(review_aigc) / max(len(review_total), 1)

        if paper_aigc:
            cross_checks.append(f'论文材料中 {len(paper_aigc)}/{len(paper_total)} 个段落被判定为AI生成（占比 {paper_rate:.0%}）')
        if review_aigc:
            cross_checks.append(f'评审材料中 {len(review_aigc)}/{len(review_total)} 个段落被判定为AI生成（占比 {review_rate:.0%}）')

        mismatches = []
        if paper_aigc and not review_aigc:
            mismatches.append('论文存在AI生成内容但评审材料未检测到异常，建议人工复核评审意见的独立性')
        elif review_aigc and not paper_aigc:
            mismatches.append('评审材料存在AI生成内容但论文未检测到异常，建议关注评审意见的来源')

        recommendations = []
        if paper_aigc or review_aigc:
            recommendations.append('建议对AI生成概率较高的段落进行人工复核')
        if abs(paper_rate - review_rate) > 0.3:
            recommendations.append('论文与评审材料的AI生成比例差异较大，建议进行交叉验证')
        if not cross_checks:
            cross_checks.append('各材料BERT文本分类均未发现明显AI生成痕迹')

        return {
            'cross_checks': cross_checks,
            'mismatches': mismatches,
            'recommendations': recommendations,
        }

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
        if not text_items:
            raise ValueError(f'No extractable text found for detect_type={task.detect_type}')
        batch_response = BertTextAIDetectionBridge.submit_batch(text_items)
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
            # 用LLM生成的中文摘要替换BERT英文摘要
            if llm_result.get('summary'):
                result_payload['summary'] = llm_result['summary']
            if task.detect_type == 'multi':
                cross_analysis = {}
                for key in ('cross_checks', 'mismatches', 'recommendations'):
                    if key in llm_result:
                        cross_analysis[key] = llm_result[key]
                if cross_analysis:
                    result_payload['cross_material_analysis'] = cross_analysis
                ai_contribution = []
                for key in ('suspicious_patterns', 'signals', 'cross_checks'):
                    items = llm_result.get(key)
                    if isinstance(items, list):
                        ai_contribution.extend(str(i) for i in items)
                result_payload['ai_contribution'] = ai_contribution

        # 如果LLM未成功，为multi类型生成基础交叉分析
        if task.detect_type == 'multi' and result_payload.get('cross_material_analysis') is None:
            result_payload['cross_material_analysis'] = StructuredDetectionService._build_basic_cross_analysis(
                result_payload, ai_response
            )
        StructuredDetectionService.store_result(task, result_payload, ai_response)
        return result_payload

    @staticmethod
    def mark_failed(task: DetectionTask, reason: str):
        task.status = 'failed'
        task.failure_reason = reason
        task.save(update_fields=['status', 'failure_reason'])
