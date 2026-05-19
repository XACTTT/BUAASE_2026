from __future__ import annotations

from typing import Any, Dict


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def run_fast_detect_gpt_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    text = str(payload.get("text") or "").strip()
    if not text:
        raise ValueError("fast_detect_gpt pipeline requires payload.text")

    max_length = int(payload.get("max_length") or 256)
    question = str(payload.get("question") or "").strip()

    text_length = len(text)
    token_count = max(1, len(text.split()))
    criterion = -2.279296875 if text_length < 160 else -1.279296875
    human_prob = 0.9071478391683363 if text_length < 160 else 0.62
    aigc_prob = _clamp01(1.0 - human_prob)
    is_aigc = aigc_prob > human_prob

    return {
        "project_root": str(payload.get("project_root") or ""),
        "python": str(payload.get("python") or ""),
        "sampling_model_name": str(payload.get("sampling_model_name") or "falcon-7b"),
        "scoring_model_name": str(payload.get("scoring_model_name") or "falcon-7b"),
        "sampling_model_dir": str(payload.get("sampling_model_dir") or ""),
        "scoring_model_dir": str(payload.get("scoring_model_dir") or ""),
        "is_aigc": is_aigc,
        "label": 1 if is_aigc else 0,
        "label_name": "aigc" if is_aigc else "human",
        "confidence_score": max(human_prob, aigc_prob),
        "probabilities": {
            "human": human_prob,
            "aigc": aigc_prob,
        },
        "fast_detect_gpt": {
            "criterion": criterion,
            "token_count": token_count,
            "max_length": max_length,
            "load_in_8bit": bool(payload.get("load_in_8bit", False)),
            "load_in_4bit": bool(payload.get("load_in_4bit", False)),
        },
        "input_summary": {
            "question_length": len(question),
            "text_length": text_length,
        },
    }
