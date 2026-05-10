from __future__ import annotations

import os
from pathlib import Path

from service_config import SERVICE_CONFIG


SERVICE_ROOT = Path(__file__).resolve().parents[1]
SERVICE_CHECKPOINT_ROOT = SERVICE_ROOT.parent / "checkpoints"


def detect_bert_project_root() -> Path:
    env_root = os.getenv("BERT_PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    configured_root = SERVICE_CONFIG["paths"].get("bert_project_root")
    if configured_root:
        configured_path = Path(configured_root).expanduser().resolve()
        if configured_path.is_dir():
            return configured_path

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "weights").is_dir() and (parent / "checkpoints").is_dir():
            return parent

    if (SERVICE_CHECKPOINT_ROOT / "weights").is_dir() and (SERVICE_CHECKPOINT_ROOT / "checkpoints").is_dir():
        return SERVICE_CHECKPOINT_ROOT

    # Fallback to the repository layout used in this project.
    return current.parents[6]


def resolve_path(raw_path: str | None, *, base_dir: str | os.PathLike[str] | None = None) -> Path | None:
    if not raw_path:
        return None

    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path.resolve()

    if base_dir is not None:
        return (Path(base_dir) / path).resolve()

    return path.resolve()


def ensure_directory(path: str | os.PathLike[str]) -> Path:
    resolved = Path(path).resolve()
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved
