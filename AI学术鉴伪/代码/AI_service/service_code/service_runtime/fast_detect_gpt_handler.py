from __future__ import annotations

from typing import Any, Dict

from core.services.fast_detect_gpt_service import run_fast_detect_gpt_pipeline


def run_fast_detect_gpt_pipeline_entry(request_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    return run_fast_detect_gpt_pipeline(request_data)
