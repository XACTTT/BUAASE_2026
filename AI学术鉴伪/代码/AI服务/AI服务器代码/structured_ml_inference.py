import os
import re
from typing import Dict, List

try:
    import joblib
except Exception:  # pragma: no cover - optional dependency
    joblib = None

try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import TruncatedSVD
    from sklearn.ensemble import IsolationForest

    SKLEARN_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    SKLEARN_AVAILABLE = False


def _safe_div(n: float, d: float) -> float:
    if d == 0:
        return 0.0
    return n / d


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。！？!?\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def tokenize(text: str) -> List[str]:
    return re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]|\d+", text.lower())


def lexical_diversity(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    return _safe_div(len(set(tokens)), len(tokens))


def repetition_ratio(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    freq: Dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    repeated = sum(v for v in freq.values() if v >= 3)
    return _safe_div(repeated, len(tokens))


def bigram_duplicate_ratio(tokens: List[str]) -> float:
    if len(tokens) < 2:
        return 0.0
    bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
    total = len(bigrams)
    return _safe_div(total - len(set(bigrams)), total)


def sentence_length_cv(sentences: List[str]) -> float:
    if not sentences:
        return 0.0
    lengths = [len(s) for s in sentences]
    mean = _safe_div(sum(lengths), len(lengths))
    if mean <= 0:
        return 0.0
    var = _safe_div(sum((x - mean) ** 2 for x in lengths), len(lengths))
    return _safe_div(var ** 0.5, mean)


def extract_handcrafted_features(text: str) -> Dict[str, float]:
    sentences = split_sentences(text)
    tokens = tokenize(text)
    return {
        "text_len": float(len(text)),
        "sentence_count": float(len(sentences)),
        "token_count": float(len(tokens)),
        "lexical_diversity": lexical_diversity(tokens),
        "repetition_ratio": repetition_ratio(tokens),
        "bigram_duplicate_ratio": bigram_duplicate_ratio(tokens),
        "sentence_length_cv": sentence_length_cv(sentences),
    }


class TraditionalMLEngine:
    """
    Concrete ML implementation layer:
    - If trained artifacts exist, uses supervised model probability.
    - Otherwise uses unsupervised sentence-level ML signals.
    """

    def __init__(self, model_dir: str | None = None):
        self.model_dir = model_dir or os.getenv("STRUCTURED_AI_MODEL_DIR", "./structured_models")
        self.paper_model = None
        self.review_model = None
        self.paper_vectorizer = None
        self.review_vectorizer = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        if not joblib:
            return
        try:
            pm = os.path.join(self.model_dir, "paper_overall_model.joblib")
            pv = os.path.join(self.model_dir, "paper_vectorizer.joblib")
            rm = os.path.join(self.model_dir, "review_overall_model.joblib")
            rv = os.path.join(self.model_dir, "review_vectorizer.joblib")
            if os.path.exists(pm) and os.path.exists(pv):
                self.paper_model = joblib.load(pm)
                self.paper_vectorizer = joblib.load(pv)
            if os.path.exists(rm) and os.path.exists(rv):
                self.review_model = joblib.load(rm)
                self.review_vectorizer = joblib.load(rv)
        except Exception:
            self.paper_model = None
            self.review_model = None
            self.paper_vectorizer = None
            self.review_vectorizer = None

    def _unsupervised_signals(self, text: str) -> Dict[str, float]:
        if not SKLEARN_AVAILABLE:
            return {
                "ml_available": 0.0,
                "ml_anomaly_ratio": 0.0,
                "ml_cluster_concentration": 0.0,
                "ml_svd_energy": 0.0,
                "ml_supervised_proba": 0.0,
            }

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            sents = split_sentences(text)
            if len(sents) < 3:
                return {
                    "ml_available": 1.0,
                    "ml_anomaly_ratio": 0.0,
                    "ml_cluster_concentration": 0.0,
                    "ml_svd_energy": 0.0,
                    "ml_supervised_proba": 0.0,
                }

            vec = TfidfVectorizer(analyzer="char", ngram_range=(2, 4), min_df=1)
            x = vec.fit_transform(sents)
            if x.shape[0] < 3 or x.shape[1] < 2:
                return {
                    "ml_available": 1.0,
                    "ml_anomaly_ratio": 0.0,
                    "ml_cluster_concentration": 0.0,
                    "ml_svd_energy": 0.0,
                    "ml_supervised_proba": 0.0,
                }

            iso = IsolationForest(n_estimators=64, contamination="auto", random_state=42)
            pred = iso.fit_predict(x.toarray())
            anomaly_ratio = _safe_div(sum(1 for p in pred if p == -1), len(pred))

            n_clusters = min(3, x.shape[0])
            km = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
            labels = km.fit_predict(x)
            counts: Dict[int, int] = {}
            for lb in labels:
                counts[int(lb)] = counts.get(int(lb), 0) + 1
            max_cluster = max(counts.values()) if counts else 0
            cluster_concentration = _safe_div(max_cluster, len(labels))

            n_comp = min(2, max(1, x.shape[1] - 1), x.shape[0] - 1)
            if n_comp >= 1:
                svd = TruncatedSVD(n_components=n_comp, random_state=42)
                svd.fit(x)
                energy = float(svd.explained_variance_ratio_[0])
            else:
                energy = 0.0

            return {
                "ml_available": 1.0,
                "ml_anomaly_ratio": _clamp01(anomaly_ratio),
                "ml_cluster_concentration": _clamp01(cluster_concentration),
                "ml_svd_energy": _clamp01(energy),
                "ml_supervised_proba": 0.0,
            }
        except Exception:
            return {
                "ml_available": 1.0,
                "ml_anomaly_ratio": 0.0,
                "ml_cluster_concentration": 0.0,
                "ml_svd_energy": 0.0,
                "ml_supervised_proba": 0.0,
            }

    def _supervised_proba(self, detect_type: str, text: str) -> float:
        if not joblib:
            return 0.0

        try:
            if detect_type == "paper" and self.paper_model is not None and self.paper_vectorizer is not None:
                x = self.paper_vectorizer.transform([text])
                proba = float(self.paper_model.predict_proba(x)[0][1])
                return _clamp01(proba)

            if detect_type == "review" and self.review_model is not None and self.review_vectorizer is not None:
                x = self.review_vectorizer.transform([text])
                proba = float(self.review_model.predict_proba(x)[0][1])
                return _clamp01(proba)
        except Exception:
            return 0.0

        return 0.0

    def sentence_signals(self, detect_type: str, text: str) -> Dict[str, float]:
        sig = self._unsupervised_signals(text)
        proba = self._supervised_proba(detect_type, text)
        sig["ml_supervised_proba"] = proba
        return sig
