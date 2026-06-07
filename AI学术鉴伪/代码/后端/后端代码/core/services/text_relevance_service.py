import logging
import re

import numpy as np

logger = logging.getLogger(__name__)


class TextRelevanceService:
    """Compute text-level correlation between paper and review materials."""

    MAX_CORPUS_CHARS = 10000
    TFIDF_MAX_FEATURES = 500
    TOP_KEYWORDS_COUNT = 50

    @staticmethod
    def _chinese_tokenizer(text: str) -> list[str]:
        import jieba
        return [w for w in jieba.lcut(text) if len(w.strip()) > 1]

    @staticmethod
    def compute_topic_overlap(paper_corpus: str, review_corpus: str) -> dict:
        """Compute TF-IDF based topic overlap between paper and review."""
        paper_text = paper_corpus[:TextRelevanceService.MAX_CORPUS_CHARS]
        review_text = review_corpus[:TextRelevanceService.MAX_CORPUS_CHARS]

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vectorizer = TfidfVectorizer(
                tokenizer=TextRelevanceService._chinese_tokenizer,
                token_pattern=None,
                max_features=TextRelevanceService.TFIDF_MAX_FEATURES,
                lowercase=False,
            )
            tfidf_matrix = vectorizer.fit_transform([paper_text, review_text])

            cos_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])

            feature_names = vectorizer.get_feature_names_out()
            paper_scores = tfidf_matrix[0].toarray()[0]
            review_scores = tfidf_matrix[1].toarray()[0]

            n_top = TextRelevanceService.TOP_KEYWORDS_COUNT
            paper_top_indices = paper_scores.argsort()[-n_top:][::-1]
            review_top_indices = review_scores.argsort()[-n_top:][::-1]

            paper_top_kw = [feature_names[i] for i in paper_top_indices if paper_scores[i] > 0]
            review_top_kw = [feature_names[i] for i in review_top_indices if review_scores[i] > 0]

            paper_set = set(paper_top_kw)
            review_set = set(review_top_kw)
            shared = list(paper_set & review_set)
            jaccard = len(shared) / max(len(paper_set | review_set), 1)

            return {
                'jaccard_similarity': round(jaccard, 4),
                'cosine_similarity': round(cos_sim, 4),
                'shared_keywords': shared[:20],
                'paper_top_keywords': paper_top_kw[:30],
                'review_top_keywords': review_top_kw[:30],
            }
        except Exception as e:
            logger.warning(f'topic_overlap computation failed: {e}')
            return {
                'jaccard_similarity': 0.0,
                'cosine_similarity': 0.0,
                'shared_keywords': [],
                'paper_top_keywords': [],
                'review_top_keywords': [],
            }

    @staticmethod
    def detect_content_references(paper_text: str, review_text: str) -> dict:
        """Detect if review references specific paper content."""
        details = []

        fig_patterns = [
            r'图\s*(\d+)', r'Fig\.?\s*(\d+)', r'Figure\s*(\d+)',
            r'表\s*(\d+)', r'Table\s*(\d+)', r'Tab\.?\s*(\d+)',
        ]
        fig_refs = []
        for pat in fig_patterns:
            for m in re.finditer(pat, review_text, re.IGNORECASE):
                fig_refs.append(m.group(1))
                details.append(m.group(0))

        section_patterns = [
            r'Section\s*(\d+)', r'第\s*(\d+)\s*章', r'第\s*(\d+)\s*节',
            r'[Ss]ection\s*(\d+\.?\d*)',
        ]
        section_refs = []
        for pat in section_patterns:
            for m in re.finditer(pat, review_text, re.IGNORECASE):
                section_refs.append(m.group(1))
                details.append(m.group(0))

        # Extract CamelCase terms from paper (likely method names)
        cap_terms = set(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', paper_text))
        method_refs = []
        for term in cap_terms:
            if term in review_text:
                method_refs.append(term)
                details.append(term)

        method_keywords = ['method', 'approach', 'framework', 'algorithm', 'model',
                           'technique', '方法', '算法', '框架', '模型', '技术', '策略', 'strategy']
        review_lower = review_text.lower()
        paper_lower = paper_text.lower()
        for kw in method_keywords:
            if kw in review_lower and kw in paper_lower:
                method_refs.append(kw)

        seen = set()
        unique_details = []
        for d in details:
            d_clean = d.strip()
            if d_clean and d_clean not in seen:
                seen.add(d_clean)
                unique_details.append(d_clean)

        return {
            'has_figure_references': len(fig_refs) > 0,
            'has_method_references': len(method_refs) > 0,
            'has_section_references': len(section_refs) > 0,
            'reference_count': len(set(fig_refs)) + len(set(method_refs)) + len(set(section_refs)),
            'reference_details': unique_details[:10],
        }

    @staticmethod
    def compute_aigc_distribution(paper_sections: list[dict], review_sections: list[dict]) -> dict:
        """Compare AIGC probability distributions between paper and review."""
        def _extract_scores(sections):
            scores = []
            for s in sections:
                prob = s.get('probabilities', {})
                aigc = prob.get('aigc') if isinstance(prob, dict) else None
                if aigc is None:
                    aigc = s.get('confidence_score', 0)
                scores.append(float(aigc) if aigc is not None else 0.0)
            return scores

        paper_scores = _extract_scores(paper_sections)
        review_scores = _extract_scores(review_sections)

        if not paper_scores or not review_scores:
            return {
                'paper_mean': 0, 'paper_std': 0,
                'review_mean': 0, 'review_std': 0,
                'distribution_divergence': 0,
                'paper_bins': [0, 0, 0], 'review_bins': [0, 0, 0],
            }

        p_mean = float(np.mean(paper_scores))
        p_std = float(np.std(paper_scores))
        r_mean = float(np.mean(review_scores))
        r_std = float(np.std(review_scores))

        divergence = min(abs(p_mean - r_mean) / max(max(p_mean, r_mean), 0.01), 1.0)

        def _bin(scores):
            low = sum(1 for s in scores if s < 0.3)
            mid = sum(1 for s in scores if 0.3 <= s < 0.7)
            high = sum(1 for s in scores if s >= 0.7)
            return [low, mid, high]

        return {
            'paper_mean': round(p_mean, 4),
            'paper_std': round(p_std, 4),
            'review_mean': round(r_mean, 4),
            'review_std': round(r_std, 4),
            'distribution_divergence': round(divergence, 4),
            'paper_bins': _bin(paper_scores),
            'review_bins': _bin(review_scores),
        }
