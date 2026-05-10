from __future__ import annotations

import base64
import io
import json
import pickle
import zipfile
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from PIL import Image

from .pathing import resolve_path


def _read_images_from_zip(zip_path: Path) -> List[np.ndarray]:
    images: List[np.ndarray] = []
    with zipfile.ZipFile(zip_path) as zip_file:
        for zip_info in zip_file.infolist():
            if "/" in zip_info.filename:
                continue
            if not zip_info.filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                continue
            data = zip_file.read(zip_info)
            img = Image.open(io.BytesIO(data)).convert("RGB")
            images.append(np.array(img))
    return images


def _extract_method_names(raw_results: Any) -> List[str]:
    method_names: List[str] = []
    if isinstance(raw_results, list):
        for item in raw_results:
            if isinstance(item, tuple) and len(item) >= 1 and isinstance(item[0], str):
                method_names.append(item[0])
    return method_names


def run_image_pipeline(request_data: Dict[str, Any], *, request_path: Path) -> Dict[str, Any]:
    from pipeline.pipeline_single_image import PipelineSingleImage

    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    request_dir = request_path.parent
    zip_path = resolve_path(
        payload.get("image_zip")
        or payload.get("images_zip")
        or payload.get("image_archive")
        or "test/img.zip",
        base_dir=request_dir,
    )
    if zip_path is None or not zip_path.is_file():
        raise FileNotFoundError(f"image zip not found: {zip_path}")

    config = payload.get("config")
    if config is None:
        config_path = resolve_path(
            payload.get("config_path")
            or payload.get("data_json")
            or payload.get("params_file")
            or "test/data.json",
            base_dir=request_dir,
        )
        if config_path and config_path.is_file():
            with config_path.open("r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {"cmd_block_size": 64, "urn_k": 0.3, "if_use_llm": False}
    elif not isinstance(config, dict):
        raise ValueError("payload.config must be an object")

    images = _read_images_from_zip(zip_path)
    if not images:
        raise ValueError(f"no images found in zip: {zip_path}")

    pipeline = PipelineSingleImage()
    pipeline.clear_images()
    pipeline.set_method_parameters(config)
    pipeline.run_multi_images(images)
    raw_results = pipeline.get_results()
    result_bytes = pickle.dumps(raw_results)
    result_base64 = base64.b64encode(result_bytes).decode("utf-8")

    return {
        "summary": {
            "image_count": len(images),
            "zip_path": str(zip_path),
            "config": config,
            "method_names": _extract_method_names(raw_results),
        },
        "transport": {
            "format": "pickle_base64",
            "consumer_hint": "decode base64 then pickle.loads to recover the original image-detection result payload",
            "data": result_base64,
        },
    }
