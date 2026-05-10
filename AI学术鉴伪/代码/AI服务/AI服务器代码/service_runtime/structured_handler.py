from __future__ import annotations

from typing import Any, Dict

from trigger_structured import run_detection


def run_structured_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    if "detect_type" in request_data and "payload" in request_data:
        structured_request = {
            "detect_type": request_data.get("detect_type"),
            "payload": payload,
        }
    else:
        detect_type = payload.get("detect_type") or request_data.get("detect_type")
        if not detect_type:
            raise ValueError("structured pipeline requires detect_type")
        structured_request = {
            "detect_type": detect_type,
            "payload": payload,
        }

    return run_detection(structured_request)

