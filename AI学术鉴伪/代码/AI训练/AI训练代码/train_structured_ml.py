import argparse
import json
import os
import re
from typing import Dict, List

try:
    import joblib
    import numpy as np
    from scipy.sparse import csr_matrix, hstack
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"missing dependency for training: {exc}")


def _safe_div(n: float, d: float) -> float:
    if d == 0:
        return 0.0
    return n / d


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？!?\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]|\d+", text.lower())


def _extract_handcrafted_features(text: str) -> Dict[str, float]:
    sentences = _split_sentences(text)
    tokens = _tokenize(text)

    freq: Dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    lexical_diversity = _safe_div(len(set(tokens)), len(tokens)) if tokens else 0.0
    repetition_ratio = _safe_div(sum(v for v in freq.values() if v >= 3), len(tokens)) if tokens else 0.0

    if len(tokens) >= 2:
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        bigram_duplicate_ratio = _safe_div(len(bigrams) - len(set(bigrams)), len(bigrams))
    else:
        bigram_duplicate_ratio = 0.0

    if sentences:
        lengths = [len(s) for s in sentences]
        mean_len = _safe_div(sum(lengths), len(lengths))
        if mean_len > 0:
            variance = _safe_div(sum((x - mean_len) ** 2 for x in lengths), len(lengths))
            sentence_length_cv = _safe_div(variance ** 0.5, mean_len)
        else:
            sentence_length_cv = 0.0
    else:
        sentence_length_cv = 0.0

    return {
        "text_len": float(len(text)),
        "sentence_count": float(len(sentences)),
        "token_count": float(len(tokens)),
        "lexical_diversity": lexical_diversity,
        "repetition_ratio": repetition_ratio,
        "bigram_duplicate_ratio": bigram_duplicate_ratio,
        "sentence_length_cv": sentence_length_cv,
    }


def _load_jsonl(path: str) -> List[Dict]:
    rows: List[Dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _rows_for_type(rows: List[Dict], detect_type: str) -> List[Dict]:
    return [r for r in rows if (r.get("detect_type") or "").strip().lower() == detect_type]


def _build_sparse_features(texts: List[str]):
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=1, max_features=50000)
    x_tfidf = vectorizer.fit_transform(texts)

    hand = []
    for text in texts:
        feat = _extract_handcrafted_features(text)
        hand.append([
            feat["text_len"],
            feat["sentence_count"],
            feat["token_count"],
            feat["lexical_diversity"],
            feat["repetition_ratio"],
            feat["bigram_duplicate_ratio"],
            feat["sentence_length_cv"],
        ])

    x_hand = csr_matrix(np.asarray(hand, dtype=np.float32))
    x = hstack([x_tfidf, x_hand], format="csr")
    return vectorizer, x


def _train_binary(texts: List[str], labels: List[int]):
    vectorizer, x = _build_sparse_features(texts)
    y = np.asarray(labels, dtype=np.int32)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(x, y)
    return vectorizer, model


def _save(model_dir: str, prefix: str, vectorizer, model):
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(model_dir, f"{prefix}_vectorizer.joblib"))
    joblib.dump(model, os.path.join(model_dir, f"{prefix}_overall_model.joblib"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Train traditional ML models for structured paper/review detection")
    parser.add_argument("--data", required=True, help="Path to JSONL dataset")
    parser.add_argument("--model-dir", default="./structured_models", help="Output directory for joblib models")
    args = parser.parse_args()

    rows = _load_jsonl(args.data)
    if not rows:
        raise SystemExit("dataset is empty")

    for detect_type, prefix in [("paper", "paper"), ("review", "review")]:
        subset = _rows_for_type(rows, detect_type)
        if not subset:
            print(f"skip {detect_type}: no rows")
            continue

        texts: List[str] = []
        labels: List[int] = []
        for item in subset:
            text = (item.get("text") or "").strip()
            if not text:
                continue
            label = int(item.get("overall_label", 0))
            texts.append(text)
            labels.append(1 if label > 0 else 0)

        if len(texts) < 10 or len(set(labels)) < 2:
            print(f"skip {detect_type}: need >=10 samples and both classes")
            continue

        vectorizer, model = _train_binary(texts, labels)
        _save(args.model_dir, prefix, vectorizer, model)
        print(f"trained {detect_type}: samples={len(texts)} saved_to={args.model_dir}")

    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
