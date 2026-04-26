import base64
import json
import os
import re
import sys
import time
from typing import Any, Dict, List

from structured_ml_inference import TraditionalMLEngine

try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.ensemble import IsolationForest
    from sklearn.feature_extraction.text import TfidfVectorizer

    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


READY_MARKER = os.getenv("STRUCTURED_AI_READY_MARKER", "structured ready")
RESULT_MARKER = os.getenv("STRUCTURED_AI_RESULT_MARKER", "structured results")
REQUEST_FILENAME = "request.json"
ENABLE_ML = os.getenv("STRUCTURED_AI_ENABLE_ML", "1").strip() not in {"0", "false", "False"}
ML_ENGINE = TraditionalMLEngine()


def _print_ready() -> None:
    print(READY_MARKER, flush=True)


def _print_result(payload: Dict[str, Any]) -> None:
    encoded = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode("utf-8")).decode("utf-8")
    print(RESULT_MARKER, flush=True)
    print(encoded, flush=True)


def _stderr(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _resolve_request_path() -> str:
    request_file = os.getenv("STRUCTURED_AI_REQUEST_FILE")
    if request_file:
        return request_file

    request_dir = os.getenv("STRUCTURED_AI_REQUEST_DIR")
    if not request_dir:
        request_dir = os.getenv("STRUCTURED_AI_REMOTE_REQUEST_DIR", "./structured_test/")

    return os.path.join(request_dir, REQUEST_FILENAME)


def _wait_for_request_file(path: str, timeout_sec: float = 120.0, poll_interval: float = 0.2) -> None:
    deadline = time.time() + timeout_sec
    last_size = -1
    stable_count = 0

    while time.time() < deadline:
        if os.path.exists(path):
            try:
                size = os.path.getsize(path)
            except OSError:
                size = -1

            if size > 0 and size == last_size:
                stable_count += 1
                if stable_count >= 2:
                    return
            else:
                stable_count = 0
                last_size = size

        time.sleep(poll_interval)

    raise TimeoutError(f"request file not ready in time: {path}")


def _load_request(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("request.json must be a JSON object")
    return data


def _ensure_dict(value: Any, field_name: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _ensure_list(value: Any, field_name: str) -> List[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value


def _validate_request(request_data: Dict[str, Any]) -> None:
    detect_type = (request_data.get("detect_type") or "").strip().lower()
    if detect_type not in {"paper", "review", "multi"}:
        raise ValueError("detect_type must be one of paper/review/multi")

    payload = _ensure_dict(request_data.get("payload") or {}, "payload")

    if detect_type == "paper":
        paper_files = _ensure_list(payload.get("paper_files"), "payload.paper_files")
        images = _ensure_list(payload.get("images"), "payload.images")
        if not paper_files and not images:
            raise ValueError("paper payload has no materials: paper_files and images are both empty")

        has_text = False
        for i, item in enumerate(paper_files):
            _ensure_dict(item, f"payload.paper_files[{i}]")
            sections = _ensure_list(item.get("sections"), f"payload.paper_files[{i}].sections")
            for j, sec in enumerate(sections):
                _ensure_dict(sec, f"payload.paper_files[{i}].sections[{j}]")
                if (sec.get("text") or "").strip():
                    has_text = True

        if paper_files and not has_text:
            raise ValueError("paper payload has paper_files but no non-empty section text")

    if detect_type == "review":
        review_files = _ensure_list(payload.get("review_files"), "payload.review_files")
        review_texts = _ensure_list(payload.get("review_texts"), "payload.review_texts")
        if not review_files and not review_texts:
            raise ValueError("review payload has no materials: review_files and review_texts are both empty")

        has_file_text = False
        for i, item in enumerate(review_files):
            _ensure_dict(item, f"payload.review_files[{i}]")
            sections = _ensure_list(item.get("sections"), f"payload.review_files[{i}].sections")
            for j, sec in enumerate(sections):
                _ensure_dict(sec, f"payload.review_files[{i}].sections[{j}]")
                if (sec.get("text") or "").strip():
                    has_file_text = True

        has_direct_text = False
        for i, item in enumerate(review_texts):
            _ensure_dict(item, f"payload.review_texts[{i}]")
            raw = (item.get("raw_text") or "").strip()
            normalized = (item.get("normalized_text") or "").strip()
            if raw or normalized:
                has_direct_text = True

        if review_files and not has_file_text and not has_direct_text:
            raise ValueError("review payload has materials but no non-empty text")


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？!?\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> List[str]:
    # Supports mixed Chinese/English text with a lightweight tokenizer.
    return re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]|\d+", text.lower())


def _lexical_diversity(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    return _safe_div(len(set(tokens)), len(tokens))


def _repetition_ratio(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    freq: Dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    repeated = sum(v for v in freq.values() if v >= 3)
    return _safe_div(repeated, len(tokens))


def _bigram_duplicate_ratio(tokens: List[str]) -> float:
    if len(tokens) < 2:
        return 0.0
    bigrams = [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]
    total = len(bigrams)
    unique = len(set(bigrams))
    return _safe_div(total - unique, total)


def _sentence_length_cv(sentences: List[str]) -> float:
    if not sentences:
        return 0.0
    lengths = [len(s) for s in sentences]
    mean = _safe_div(sum(lengths), len(lengths))
    if mean <= 0:
        return 0.0
    variance = _safe_div(sum((x - mean) ** 2 for x in lengths), len(lengths))
    std = variance ** 0.5
    return _safe_div(std, mean)


def _count_keyword_hits(text: str, keywords: List[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(kw.lower()) for kw in keywords)


def _ml_enabled() -> bool:
    return ENABLE_ML and SKLEARN_AVAILABLE


def _ml_sentence_signals(text: str) -> Dict[str, float]:
    if not _ml_enabled():
        return {
            "ml_available": 0.0,
            "ml_anomaly_ratio": 0.0,
            "ml_cluster_concentration": 0.0,
            "ml_svd_energy": 0.0,
            "ml_supervised_proba": 0.0,
        }

    return ML_ENGINE.sentence_signals("paper", text)


def _numeric_anomaly_score(text: str) -> float:
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    if not numbers:
        return 0.0

    pct_hits = re.findall(r"(\d+(?:\.\d+)?)\s*%", text)
    invalid_pct = sum(1 for p in pct_hits if float(p) > 100)
    negative_hits = len(re.findall(r"-\d+(?:\.\d+)?", text))
    extreme_hits = sum(1 for x in numbers if x > 1e9)

    anomalies = invalid_pct + negative_hits + extreme_hits
    return _clamp01(_safe_div(anomalies, max(1, len(numbers))))


def _collect_text_from_sections(files: List[Dict[str, Any]]) -> str:
    blocks: List[str] = []
    for item in files:
        for sec in item.get("sections", []) or []:
            txt = (sec.get("text") or "").strip()
            if txt:
                blocks.append(txt)
    return "\n".join(blocks)


def _analyze_paper(payload: Dict[str, Any]) -> Dict[str, Any]:
    paper_files = payload.get("paper_files", []) or []
    images = payload.get("images", []) or []

    text = _collect_text_from_sections(paper_files)
    text_len = len(text)
    tokens = _tokenize(text)
    sentences = _split_sentences(text)

    lexical_div = _lexical_diversity(tokens)
    repetition = _repetition_ratio(tokens)
    bigram_dup = _bigram_duplicate_ratio(tokens)
    len_cv = _sentence_length_cv(sentences)
    ml = _ml_sentence_signals(text)

    citation_hits = len(re.findall(r"\[[0-9,\-\s]+\]", text))
    citation_words = _count_keyword_hits(text, ["参考文献", "引用", "citation", "references"])
    quote_words = _count_keyword_hits(text, ["据", "表明", "研究指出", "reported", "according to"])

    # Academic misconduct proxy: heavy repetition + suspicious quote/citation imbalance.
    citation_imbalance = _clamp01(_safe_div(max(0, quote_words - citation_hits - citation_words), 8))
    misconduct_score = _clamp01(0.55 * repetition + 0.25 * bigram_dup + 0.20 * citation_imbalance)

    # AIGC proxy: low lexical diversity + overly stable sentence lengths + repetitive pattern.
    low_div = _clamp01(1 - lexical_div)
    too_stable = _clamp01(1 - min(1.0, len_cv / 0.6))
    aigc_rule = _clamp01(0.45 * low_div + 0.30 * too_stable + 0.25 * bigram_dup)
    aigc_ml = _clamp01(0.40 * ml["ml_anomaly_ratio"] + 0.35 * ml["ml_cluster_concentration"] + 0.25 * ml["ml_svd_energy"])
    if ml["ml_available"] > 0:
        supervised = _clamp01(ml.get("ml_supervised_proba", 0.0))
        aigc_score = _clamp01(0.50 * aigc_rule + 0.35 * aigc_ml + 0.15 * supervised)
    else:
        aigc_score = aigc_rule

    # Text tampering proxy: abrupt style instability and transition inconsistency.
    transition_hits = _count_keyword_hits(text, ["因此", "综上", "然而", "但是", "therefore", "however"])
    transition_density = _safe_div(transition_hits, max(1, len(sentences)))
    tamper_rule = _clamp01(0.55 * _clamp01(len_cv / 0.8) + 0.45 * _clamp01(0.25 - transition_density))
    tamper_ml = _clamp01(0.65 * ml["ml_anomaly_ratio"] + 0.35 * _clamp01(1 - ml["ml_cluster_concentration"]))
    if ml["ml_available"] > 0:
        tamper_score = _clamp01(0.70 * tamper_rule + 0.30 * tamper_ml)
    else:
        tamper_score = tamper_rule

    # Data/chart fabrication hint proxy: numeric anomalies + chart mention without evidence.
    number_anomaly = _numeric_anomaly_score(text)
    chart_mentions = _count_keyword_hits(text, ["图", "表", "figure", "table", "chart"])
    chart_evidence_gap = _clamp01(_safe_div(max(0, chart_mentions - len(images)), 10))
    data_chart_score = _clamp01(0.65 * number_anomaly + 0.35 * chart_evidence_gap)

    overall_score = _clamp01(
        0.35 * misconduct_score
        + 0.30 * aigc_score
        + 0.20 * tamper_score
        + 0.15 * data_chart_score
    )
    is_fake = overall_score >= 0.60

    return {
        "overall": {
            "is_fake": is_fake,
            "confidence_score": round(overall_score, 4),
            "risk_level": "high" if overall_score >= 0.75 else "medium" if overall_score >= 0.45 else "low",
        },
        "summary": "paper detection finished",
        "material_summary": {
            "paper_file_count": len(paper_files),
            "image_count": len(images),
            "section_count": sum(len(item.get("sections", []) or []) for item in paper_files),
        },
        "dimensions": [
            {
                "name": "academic_misconduct",
                "score": round(misconduct_score, 4),
                "summary": "rule-based plagiarism risk estimation",
            },
            {
                "name": "aigc_generation",
                "score": round(aigc_score, 4),
                "summary": "rule-based AIGC risk estimation",
            },
            {
                "name": "text_tampering",
                "score": round(tamper_score, 4),
                "summary": "rule-based text tampering risk estimation",
            },
            {
                "name": "data_chart_fabrication_hint",
                "score": round(data_chart_score, 4),
                "summary": "rule-based data/chart consistency hint",
            },
        ],
        "evidence": {
            "text_length": text_len,
            "image_count": len(images),
            "lexical_diversity": round(lexical_div, 4),
            "repetition_ratio": round(repetition, 4),
            "sentence_length_cv": round(len_cv, 4),
            "numeric_anomaly": round(number_anomaly, 4),
            "ml_enabled": bool(_ml_enabled()),
            "ml_anomaly_ratio": round(ml["ml_anomaly_ratio"], 4),
            "ml_cluster_concentration": round(ml["ml_cluster_concentration"], 4),
            "ml_svd_energy": round(ml["ml_svd_energy"], 4),
            "ml_supervised_proba": round(ml.get("ml_supervised_proba", 0.0), 4),
        },
    }


def _ml_sentence_signals_review(text: str) -> Dict[str, float]:
    if not _ml_enabled():
        return {
            "ml_available": 0.0,
            "ml_anomaly_ratio": 0.0,
            "ml_cluster_concentration": 0.0,
            "ml_svd_energy": 0.0,
            "ml_supervised_proba": 0.0,
        }
    return ML_ENGINE.sentence_signals("review", text)


def _analyze_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    review_files = payload.get("review_files", []) or []
    review_texts = payload.get("review_texts", []) or []

    text_from_files = _collect_text_from_sections(review_files)
    text_from_paste = "\n".join((item.get("normalized_text") or item.get("raw_text") or "").strip() for item in review_texts)
    text = "\n".join([s for s in [text_from_files, text_from_paste] if s])
    text_len = len(text)
    tokens = _tokenize(text)
    sentences = _split_sentences(text)

    lexical_div = _lexical_diversity(tokens)
    repetition = _repetition_ratio(tokens)
    bigram_dup = _bigram_duplicate_ratio(tokens)
    len_cv = _sentence_length_cv(sentences)
    ml = _ml_sentence_signals_review(text)

    template_phrases = [
        "建议接收", "建议拒稿", "总体来看", "有待改进", "创新性不足", "表达清晰", "逻辑完整",
        "accept", "reject", "overall", "well written", "needs improvement",
    ]
    toxic_phrases = ["垃圾", "胡说", "荒谬", "无语", "nonsense", "stupid"]
    specificity_terms = ["实验", "方法", "数据", "结论", "对照", "指标", "ablation", "baseline", "metric"]

    template_hits = _count_keyword_hits(text, template_phrases)
    toxic_hits = _count_keyword_hits(text, toxic_phrases)
    specificity_hits = _count_keyword_hits(text, specificity_terms)

    # AIGC proxy.
    aigc_rule = _clamp01(0.45 * _clamp01(1 - lexical_div) + 0.30 * _clamp01(1 - min(1.0, len_cv / 0.7)) + 0.25 * bigram_dup)
    aigc_ml = _clamp01(0.40 * ml["ml_anomaly_ratio"] + 0.35 * ml["ml_cluster_concentration"] + 0.25 * ml["ml_svd_energy"])
    if ml["ml_available"] > 0:
        supervised = _clamp01(ml.get("ml_supervised_proba", 0.0))
        aigc_score = _clamp01(0.50 * aigc_rule + 0.35 * aigc_ml + 0.15 * supervised)
    else:
        aigc_score = aigc_rule

    # Template tendency proxy.
    template_density = _safe_div(template_hits, max(1, len(sentences)))
    template_rule = _clamp01(0.65 * _clamp01(template_density / 0.8) + 0.35 * repetition)
    template_ml = _clamp01(0.75 * ml["ml_cluster_concentration"] + 0.25 * ml["ml_svd_energy"])
    if ml["ml_available"] > 0:
        template_score = _clamp01(0.65 * template_rule + 0.35 * template_ml)
    else:
        template_score = template_rule

    # Authenticity proxy: low specificity + high generic repetition => higher risk.
    specificity_density = _safe_div(specificity_hits, max(1, len(tokens)))
    authenticity_rule = _clamp01(0.60 * _clamp01(0.08 - specificity_density) + 0.40 * bigram_dup)
    authenticity_ml = _clamp01(0.55 * ml["ml_anomaly_ratio"] + 0.45 * _clamp01(1 - ml["ml_svd_energy"]))
    if ml["ml_available"] > 0:
        authenticity_score = _clamp01(0.70 * authenticity_rule + 0.30 * authenticity_ml)
    else:
        authenticity_score = authenticity_rule

    # Compliance proxy: toxicity + extremely short content + empty actionable details.
    too_short = 1.0 if text_len < 60 else 0.0
    compliance_score = _clamp01(0.50 * _clamp01(_safe_div(toxic_hits, 2)) + 0.30 * too_short + 0.20 * _clamp01(0.06 - specificity_density))

    overall_score = _clamp01(
        0.25 * aigc_score
        + 0.20 * template_score
        + 0.35 * authenticity_score
        + 0.20 * compliance_score
    )
    is_fake = overall_score >= 0.60

    return {
        "overall": {
            "is_fake": is_fake,
            "confidence_score": round(overall_score, 4),
            "risk_level": "high" if overall_score >= 0.75 else "medium" if overall_score >= 0.45 else "low",
        },
        "summary": "review detection finished",
        "material_summary": {
            "review_file_count": len(review_files),
            "review_text_count": len(review_texts),
            "section_count": sum(len(item.get("sections", []) or []) for item in review_files),
        },
        "dimensions": [
            {
                "name": "aigc_generation",
                "score": round(aigc_score, 4),
                "summary": "rule-based AIGC risk estimation",
            },
            {
                "name": "template_tendency",
                "score": round(template_score, 4),
                "summary": "rule-based templating risk estimation",
            },
            {
                "name": "authenticity",
                "score": round(authenticity_score, 4),
                "summary": "rule-based authenticity risk estimation",
            },
            {
                "name": "compliance",
                "score": round(compliance_score, 4),
                "summary": "rule-based compliance risk estimation",
            },
        ],
        "evidence": {
            "text_length": text_len,
            "review_text_count": len(review_texts),
            "lexical_diversity": round(lexical_div, 4),
            "repetition_ratio": round(repetition, 4),
            "template_hits": template_hits,
            "specificity_hits": specificity_hits,
            "toxic_hits": toxic_hits,
            "ml_enabled": bool(_ml_enabled()),
            "ml_anomaly_ratio": round(ml["ml_anomaly_ratio"], 4),
            "ml_cluster_concentration": round(ml["ml_cluster_concentration"], 4),
            "ml_svd_energy": round(ml["ml_svd_energy"], 4),
            "ml_supervised_proba": round(ml.get("ml_supervised_proba", 0.0), 4),
        },
    }


def _run_detection(request_data: Dict[str, Any]) -> Dict[str, Any]:
    _validate_request(request_data)

    detect_type = (request_data.get("detect_type") or "").strip().lower()
    payload = request_data.get("payload") or {}

    if detect_type == "paper":
        return _analyze_paper(payload)
    if detect_type == "review":
        return _analyze_review(payload)
    if detect_type == "multi":
        raise NotImplementedError("multi detection is not implemented yet")

    raise ValueError(f"unsupported detect_type: {detect_type}")


def main() -> int:
    request_path = _resolve_request_path()
    _print_ready()

    try:
        _wait_for_request_file(request_path)
        request_data = _load_request(request_path)
        result = _run_detection(request_data)
        _print_result(result)
        return 0
    except Exception as exc:
        _stderr(f"trigger_structured failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
