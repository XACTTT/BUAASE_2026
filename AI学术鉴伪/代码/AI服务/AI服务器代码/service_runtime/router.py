from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


PIPELINE_ALIASES = {
    "image": "image",
    "image_forgery": "image",
    "vision": "image",
    "structured": "structured",
    "structured_text": "structured",
    "paper_review": "structured",
    "bert": "bert_text",
    "bert_text": "bert_text",
    "text": "bert_text",
    "text_aigc": "bert_text",
}


def _normalize_pipeline_name(raw: Any) -> str | None:
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise ValueError("pipeline must be a string")
    lowered = raw.strip().lower()
    if not lowered:
        return None
    if lowered == "auto":
        return "auto"
    return PIPELINE_ALIASES.get(lowered, lowered)


def _infer_pipeline(request_data: Dict[str, Any]) -> str:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    if any(key in payload for key in ("image_zip", "images_zip", "image_archive", "image_paths")):
        return "image"

    detect_type = request_data.get("detect_type") or payload.get("detect_type")
    if isinstance(detect_type, str) and detect_type.strip().lower() in {"paper", "review", "multi"}:
        return "structured"

    if any(key in payload for key in ("paper_files", "review_files", "review_texts", "images")):
        return "structured"

    if any(key in payload for key in ("text", "answer", "question")):
        return "bert_text"

    raise ValueError("unable to infer pipeline from request payload")


def resolve_pipeline(request_data: Dict[str, Any]) -> str:
    explicit = _normalize_pipeline_name(request_data.get("pipeline"))
    if explicit and explicit != "auto":
        return explicit
    return _infer_pipeline(request_data)


def dispatch_request(request_data: Dict[str, Any], *, request_path: Path) -> Dict[str, Any]:
    pipeline = resolve_pipeline(request_data)

    if pipeline == "image":
        from .image_handler import run_image_pipeline

        result = run_image_pipeline(request_data, request_path=request_path)
    elif pipeline == "structured":
        from .structured_handler import run_structured_pipeline

        result = run_structured_pipeline(request_data)
    elif pipeline == "bert_text":
        from .bert_text_handler import run_bert_text_pipeline

        result = run_bert_text_pipeline(request_data)
    else:
        raise ValueError(f"unsupported pipeline: {pipeline}")

    return {
        "success": True,
        "request_id": request_data.get("request_id") or request_data.get("task_id"),
        "pipeline": pipeline,
        "result": result,
    }

