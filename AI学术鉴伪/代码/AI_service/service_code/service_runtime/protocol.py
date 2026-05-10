from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

from .pathing import SERVICE_ROOT


READY_MARKER = os.getenv("UNIFIED_AI_READY_MARKER", "ai service ready")
RESULT_MARKER = os.getenv("UNIFIED_AI_RESULT_MARKER", "ai service result")
DEFAULT_REQUEST_DIR = SERVICE_ROOT / "requests"
REQUEST_FILENAME = "request.json"


def print_ready() -> None:
    print(READY_MARKER, flush=True)


def print_result(payload: Dict[str, Any]) -> None:
    encoded = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode("utf-8")).decode("utf-8")
    print(RESULT_MARKER, flush=True)
    print(encoded, flush=True)


def print_error(exc: Exception, request_id: Any = None) -> None:
    payload = {
        "success": False,
        "request_id": request_id,
        "error": {
            "type": exc.__class__.__name__,
            "message": str(exc),
        },
    }
    print_result(payload)
    print(f"unified ai service failed: {exc}", file=sys.stderr, flush=True)


def resolve_request_path() -> Path:
    explicit = os.getenv("UNIFIED_AI_REQUEST_FILE")
    if explicit:
        return Path(explicit).expanduser().resolve()

    request_dir = os.getenv("UNIFIED_AI_REQUEST_DIR")
    if request_dir:
        return (Path(request_dir).expanduser() / REQUEST_FILENAME).resolve()

    return (DEFAULT_REQUEST_DIR / REQUEST_FILENAME).resolve()


def wait_for_request_file(path: Path, timeout_sec: float = 120.0, poll_interval: float = 0.2) -> None:
    deadline = time.time() + timeout_sec
    last_size = -1
    stable_count = 0

    while time.time() < deadline:
        if path.exists():
            try:
                size = path.stat().st_size
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


def load_request(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("request.json must be a JSON object")
    return data

