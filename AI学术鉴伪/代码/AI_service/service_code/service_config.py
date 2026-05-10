from __future__ import annotations

from pathlib import Path
from typing import Any


SERVICE_CODE_ROOT = Path(__file__).resolve().parent
SERVICE_ROOT = SERVICE_CODE_ROOT.parent
CHECKPOINT_ROOT = SERVICE_ROOT / "checkpoints"


SERVICE_CONFIG: dict[str, Any] = {
    "paths": {
        "service_code_root": str(SERVICE_CODE_ROOT),
        "service_root": str(SERVICE_ROOT),
        "checkpoint_root": str(CHECKPOINT_ROOT),
        "image_forgery_root": str(CHECKPOINT_ROOT / "image_forgery"),
        "bert_project_root": str(CHECKPOINT_ROOT),
        "structured_models_root": str(SERVICE_CODE_ROOT / "structured_models"),
        "llm_weight_root": str(CHECKPOINT_ROOT / "llm" / "fakeshield-v1-22b"),
    },
    "image_pipeline": {
        "defaults": {
            "cmd_block_size": 64,
            "urn_k": 0.3,
            "if_use_llm": False,
        },
    },
    "model_devices": {
        "urn_coarse_v2": 0,
        "urn_blurring": 0,
        "urn_brute_force": 0,
        "urn_contrast": 0,
        "urn_inpainting": 0,
        "bert_text": 5,
        "llm_image": 6,
    },
    "image_forgery_models": {
        "urn_coarse_v2": "image_forgery/urn_coarse_v2/checkpoint_99.pkl",
        "urn_blurring": "image_forgery/urn_blurring/checkpoint_99.pkl",
        "urn_brute_force": "image_forgery/urn_brute_force/checkpoint_99.pkl",
        "urn_contrast": "image_forgery/urn_contrast/checkpoint_99.pkl",
        "urn_inpainting": "image_forgery/urn_inpainting/checkpoint_99.pkl",
    },
    "bert_text": {
        "default_lang": "chinese",
        "default_model_dir": "checkpoints/hc3_classifier/QiDeBERTa-base/chinese/final",
        "max_length": 256,
        "dropout": 0.1,
    },
    "llm_image": {
        "venv_python": "/root/miniconda3/envs/llm/bin/python",
        "venv_pip": "/root/miniconda3/envs/llm/bin/pip",
    },
}


def resolve_config_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    return (CHECKPOINT_ROOT / raw_path).resolve()
