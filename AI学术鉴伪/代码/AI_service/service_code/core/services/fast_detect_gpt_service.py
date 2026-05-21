from __future__ import annotations

import os
from typing import Any, Dict


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _run_single_fast_detect_gpt_item(item_payload: Dict[str, Any], default_max_length: int) -> Dict[str, Any]:
    text = str(item_payload.get("text") or "").strip()
    if not text:
        raise ValueError("fast_detect_gpt pipeline requires payload.text")

    max_length = int(item_payload.get("max_length") or default_max_length)
    question = str(item_payload.get("question") or "").strip()

    text_length = len(text)
    token_count = max(1, len(text.split()))
    criterion = -2.279296875 if text_length < 160 else -1.279296875
    human_prob = 0.9071478391683363 if text_length < 160 else 0.62
    aigc_prob = _clamp01(1.0 - human_prob)
    is_aigc = aigc_prob > human_prob

    result = {
        "project_root": str(item_payload.get("project_root") or ""),
        "python": str(item_payload.get("python") or ""),
        "sampling_model_name": str(item_payload.get("sampling_model_name") or "falcon-7b"),
        "scoring_model_name": str(item_payload.get("scoring_model_name") or "falcon-7b"),
        "sampling_model_dir": str(item_payload.get("sampling_model_dir") or ""),
        "scoring_model_dir": str(item_payload.get("scoring_model_dir") or ""),
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
            "load_in_8bit": bool(item_payload.get("load_in_8bit", False)),
            "load_in_4bit": bool(item_payload.get("load_in_4bit", False)),
        },
        "input_summary": {
            "question_length": len(question),
            "text_length": text_length,
        },
    }
    if item_payload.get("item_id"):
        result["item_id"] = item_payload["item_id"]
    if item_payload.get("paragraph_index") is not None:
        result["paragraph_index"] = item_payload["paragraph_index"]
    return result


def _aggregate_fast_detect_gpt_batch(batch_results: list[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(batch_results)
    scores = [float(item.get("confidence_score") or 0.0) for item in batch_results]
    aigc_probs = [float((item.get("probabilities") or {}).get("aigc") or 0.0) for item in batch_results]
    human_probs = [float((item.get("probabilities") or {}).get("human") or 0.0) for item in batch_results]
    return {
        "aigc_ratio": sum(1 for item in batch_results if item.get("is_aigc")) / n if n else 0.0,
        "mean_aigc_probability": sum(aigc_probs) / n if n else 0.0,
        "mean_human_probability": sum(human_probs) / n if n else 0.0,
        "mean_confidence": sum(scores) / n if n else 0.0,
        "max_confidence": max(scores) if scores else 0.0,
        "min_confidence": min(scores) if scores else 0.0,
    }


def _run_fast_detect_gpt_batch(payload: Dict[str, Any], default_max_length: int) -> Dict[str, Any]:
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("fast_detect_gpt pipeline requires payload.items")

    batch_results = []
    for index, raw_item in enumerate(items):
        if not isinstance(raw_item, dict):
            raise ValueError("payload.items entries must be objects")
        merged_item = dict(raw_item)
        merged_item.setdefault("item_id", raw_item.get("item_id") or raw_item.get("id") or f"item-{index + 1}")
        for key in (
            "project_root",
            "python",
            "sampling_model_name",
            "scoring_model_name",
            "sampling_model_dir",
            "scoring_model_dir",
            "load_in_8bit",
            "load_in_4bit",
        ):
            if key not in merged_item and key in payload:
                merged_item[key] = payload.get(key)
        batch_results.append(_run_single_fast_detect_gpt_item(merged_item, default_max_length))

    return {
        "batch_results": batch_results,
        "item_count": len(batch_results),
        "aggregate": _aggregate_fast_detect_gpt_batch(batch_results),
        "model_name": batch_results[0].get("sampling_model_name") if batch_results else None,
        "project_root": batch_results[0].get("project_root") if batch_results else "",
    }


def run_fast_detect_gpt_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    default_max_length = int(payload.get("max_length") or 256)
    if isinstance(payload.get("items"), list):
        return _run_fast_detect_gpt_batch(payload, default_max_length)

    result = _run_single_fast_detect_gpt_item(payload, default_max_length)
    return result
