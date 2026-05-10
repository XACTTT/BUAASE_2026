from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel, AutoTokenizer, PreTrainedModel
from transformers.modeling_outputs import SequenceClassifierOutput

from service_config import SERVICE_CONFIG
from .pathing import detect_bert_project_root, resolve_path


class QiDeBERTaForSequenceClassification(PreTrainedModel):
    config_class = AutoConfig
    base_model_prefix = "qideberta"

    def _init_weights(self, module):
        std = getattr(self.config, "initializer_range", 0.02)
        if isinstance(module, nn.Linear):
            module.weight.data.normal_(mean=0.0, std=std)
            if module.bias is not None:
                module.bias.data.zero_()
        elif isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=std)
            padding_idx = getattr(module, "padding_idx", None)
            if padding_idx is not None:
                module.weight.data[padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)

    def __init__(self, config, num_labels: int = 2, dropout: float = 0.1):
        super().__init__(config)
        self.num_labels = num_labels
        self.config.num_labels = num_labels
        self.dropout = nn.Dropout(dropout)

        base_path = getattr(config, "base_model_name_or_path", None) or getattr(config, "_name_or_path", None)
        if not base_path:
            raise ValueError("missing base_model_name_or_path for QiDeBERTa classifier")
        self.qideberta = AutoModel.from_pretrained(base_path, trust_remote_code=True, local_files_only=True)

        hidden_size = getattr(config, "d_model", getattr(config, "hidden_size", 768))
        self.classifier = nn.Linear(hidden_size, self.num_labels)
        self.post_init()

    def forward(self, input_ids, attention_mask=None, labels=None, **kwargs):
        outputs = self.qideberta(input_ids=input_ids, attention_mask=attention_mask, output_attentions=False)
        pooled = outputs.last_hidden_state[:, 0, :]
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled)
        loss = nn.functional.cross_entropy(logits.float(), labels.long()) if labels is not None else None
        return SequenceClassifierOutput(loss=loss, logits=logits)


def _available_weight_dirs(weights_root: Path) -> list[str]:
    if not weights_root.is_dir():
        return []
    return sorted(
        child.name for child in weights_root.iterdir()
        if child.is_dir()
    )


def resolve_base_weights_dir(model_dir: Path, explicit_base_model: str | None, repo_root: Path) -> Path:
    if explicit_base_model:
        resolved = resolve_path(explicit_base_model, base_dir=repo_root)
        if resolved is None or not resolved.is_dir():
            raise FileNotFoundError(f"base model directory not found: {explicit_base_model}")
        return resolved

    weights_root = repo_root / "weights"
    candidates = _available_weight_dirs(weights_root)
    model_dir_norm = os.path.normpath(str(model_dir))
    for candidate in candidates:
        if candidate in model_dir_norm:
            return weights_root / candidate

    checkpoint_config = model_dir / "config.json"
    if checkpoint_config.is_file():
        config = AutoConfig.from_pretrained(str(model_dir), trust_remote_code=True, local_files_only=True)
        name_or_path = getattr(config, "_name_or_path", None)
        if isinstance(name_or_path, str) and name_or_path:
            candidate = os.path.basename(os.path.normpath(name_or_path))
            candidate_dir = weights_root / candidate
            if candidate_dir.is_dir():
                return candidate_dir

    if len(candidates) == 1:
        return weights_root / candidates[0]

    raise ValueError(
        f"unable to infer base model directory for {model_dir}; "
        f"available weights: {', '.join(candidates) if candidates else '(none)'}"
    )


def resolve_model_dir(payload: Dict[str, Any], repo_root: Path, lang: str) -> Path:
    explicit = payload.get("model_dir")
    if explicit:
        resolved = resolve_path(explicit, base_dir=repo_root)
        if resolved is None or not resolved.is_dir():
            raise FileNotFoundError(f"model directory not found: {explicit}")
        return resolved

    env_model = os.getenv("BERT_TEXT_MODEL_DIR")
    if env_model:
        resolved = resolve_path(env_model, base_dir=repo_root)
        if resolved is not None and resolved.is_dir():
            return resolved

    configured_default = SERVICE_CONFIG["bert_text"].get("default_model_dir")
    if configured_default:
        resolved = resolve_path(str(configured_default), base_dir=repo_root)
        if resolved is not None and resolved.is_dir():
            return resolved

    preferred = [
        repo_root / "checkpoints" / "hc3_classifier" / "QiDeBERTa-base" / lang / "final",
        repo_root / "checkpoints" / "hc3_classifier" / "QiDeBERTa-large" / lang / "final",
    ]
    for candidate in preferred:
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError("no default Bert text classifier checkpoint found")


def _extract_text_inputs(payload: Dict[str, Any]) -> tuple[str | None, str]:
    question = payload.get("question")
    answer = payload.get("answer")
    text = payload.get("text")

    if answer:
        return question if isinstance(question, str) else None, str(answer)
    if text:
        return question if isinstance(question, str) else None, str(text)

    raise ValueError("bert_text pipeline requires payload.answer or payload.text")


def run_bert_text_pipeline(request_data: Dict[str, Any]) -> Dict[str, Any]:
    payload = request_data.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")

    lang = str(payload.get("lang") or request_data.get("lang") or SERVICE_CONFIG["bert_text"].get("default_lang", "chinese"))
    pair_mode = bool(payload.get("pair_mode", False))
    max_length = int(payload.get("max_length", SERVICE_CONFIG["bert_text"].get("max_length", 256)))
    dropout = float(payload.get("dropout", SERVICE_CONFIG["bert_text"].get("dropout", 0.1)))

    repo_root = detect_bert_project_root()
    model_dir = resolve_model_dir(payload, repo_root, lang)
    base_model_dir = resolve_base_weights_dir(model_dir, payload.get("base_model_dir"), repo_root)

    tokenizer_dir = model_dir if (model_dir / "tokenizer_config.json").is_file() else base_model_dir
    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_dir), trust_remote_code=True, local_files_only=True)

    config = AutoConfig.from_pretrained(str(model_dir), trust_remote_code=True, local_files_only=True)
    config.base_model_name_or_path = str(base_model_dir)

    model = QiDeBERTaForSequenceClassification.from_pretrained(
        str(model_dir),
        config=config,
        num_labels=2,
        dropout=dropout,
        trust_remote_code=True,
        local_files_only=True,
    )

    bert_gpu = int(payload.get("gpu", SERVICE_CONFIG["model_devices"].get("bert_text", 0)))
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{bert_gpu}")
    else:
        device = torch.device("cpu")
    model.to(device)
    model.eval()

    question, answer = _extract_text_inputs(payload)
    if pair_mode and question:
        encoded = tokenizer(
            question,
            answer,
            max_length=max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
    else:
        encoded = tokenizer(
            answer,
            max_length=max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

    encoded = {k: v.to(device) for k, v in encoded.items()}
    with torch.no_grad():
        logits = model(**encoded).logits
        probs = torch.softmax(logits, dim=-1)[0].detach().cpu().tolist()

    pred_label = int(torch.argmax(logits, dim=-1).item())
    pred_score = float(probs[pred_label])
    human_prob = float(probs[0]) if len(probs) > 0 else 0.0
    aigc_prob = float(probs[1]) if len(probs) > 1 else 0.0

    return {
        "model_dir": str(model_dir),
        "base_model_dir": str(base_model_dir),
        "lang": lang,
        "is_aigc": pred_label == 1,
        "label": pred_label,
        "label_name": "aigc" if pred_label == 1 else "human",
        "confidence_score": pred_score,
        "probabilities": {
            "human": human_prob,
            "aigc": aigc_prob,
        },
        "input_summary": {
            "pair_mode": pair_mode and question is not None,
            "question_length": len(question) if question else 0,
            "text_length": len(answer),
            "max_length": max_length,
        },
    }
