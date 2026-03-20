"""
ML Classifier — TF-IDF + Random Forest for Python error classification.
Classifies error messages into categories and suggests fix strategies.
Self-retrains from SQLite feedback.
"""
from __future__ import annotations
import os
import json
import pickle
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import numpy as np

logger = logging.getLogger(__name__)

# Path to the bundled model and training data
_PKG_DIR = Path(__file__).parent.parent
_MODEL_PATH = _PKG_DIR / "models" / "classifier.pkl"
_VECTORIZER_PATH = _PKG_DIR / "models" / "vectorizer.pkl"
_DATA_PATH = _PKG_DIR / "data" / "error_patterns.json"

# Lazy imports to avoid hard dependency at startup
try:
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False


class MLClassifier:
    """
    TF-IDF + Random Forest classifier for Python error messages.
    Falls back gracefully if sklearn is not installed.
    """

    def __init__(self):
        self._pipeline: Optional[object] = None
        self._label_encoder: Optional[object] = None
        self._loaded = False
        self._load_model()

    def _load_model(self):
        """Load pre-trained model from disk if available."""
        if not _SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not installed. ML classifier disabled.")
            return

        if _MODEL_PATH.exists() and _VECTORIZER_PATH.exists():
            try:
                with open(_MODEL_PATH, "rb") as f:
                    self._pipeline = pickle.load(f)
                with open(_VECTORIZER_PATH, "rb") as f:
                    self._label_encoder = pickle.load(f)
                self._loaded = True
                logger.debug("ML classifier loaded from disk.")
                return
            except Exception as e:
                logger.warning(f"Failed to load ML model: {e}")

        # If no pre-trained model exists, train from bundled data
        self._train_from_data()

    def _train_from_data(self):
        """Train classifier from the bundled error_patterns.json dataset."""
        if not _SKLEARN_AVAILABLE:
            return

        if not _DATA_PATH.exists():
            logger.warning(f"Training data not found at {_DATA_PATH}. ML classifier disabled.")
            return

        try:
            with open(_DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            texts = [item["error_message"] for item in data]
            labels = [item["category"] for item in data]

            if len(texts) < 10:
                return

            le = LabelEncoder()
            y = le.fit_transform(labels)

            pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(
                    analyzer="char_wb", ngram_range=(2, 5),
                    max_features=5000, sublinear_tf=True,
                )),
                ("clf", RandomForestClassifier(
                    n_estimators=200, max_depth=12,
                    random_state=42, n_jobs=-1,
                    class_weight="balanced",
                )),
            ])

            X_train, X_test, y_train, y_test = train_test_split(
                texts, y, test_size=0.2, random_state=42, stratify=y
            )
            pipeline.fit(X_train, y_train)
            acc = accuracy_score(y_test, pipeline.predict(X_test))
            logger.info(f"ML classifier trained. Accuracy: {acc:.2%}")

            # Save model
            _MODEL_PATH.parent.mkdir(exist_ok=True, parents=True)
            with open(_MODEL_PATH, "wb") as f:
                pickle.dump(pipeline, f)
            with open(_VECTORIZER_PATH, "wb") as f:
                pickle.dump(le, f)

            self._pipeline = pipeline
            self._label_encoder = le
            self._loaded = True

        except Exception as e:
            logger.warning(f"Failed to train ML classifier: {e}")

    def predict(self, error_message: str) -> List[Tuple[str, float]]:
        """
        Predict error category from error message.
        Returns list of (category_name, confidence) tuples sorted by confidence.
        """
        if not self._loaded or not _SKLEARN_AVAILABLE:
            return []

        try:
            pipeline = self._pipeline
            le = self._label_encoder

            probas = pipeline.predict_proba([error_message])[0]
            classes = le.classes_

            results = sorted(
                zip(classes, probas.tolist()),
                key=lambda x: x[1], reverse=True
            )
            # Return top-3
            return results[:3]
        except Exception as e:
            logger.warning(f"ML prediction failed: {e}")
            return []

    def retrain(self, extra_samples: List[Dict]):
        """
        Retrain the model by merging stored feedback with original data.
        extra_samples: list of {"error_message": str, "category": str}
        """
        if not _SKLEARN_AVAILABLE or not extra_samples:
            return

        try:
            existing = []
            if _DATA_PATH.exists():
                with open(_DATA_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)

            merged = existing + extra_samples

            # Write merged data and retrain
            tmp_path = _DATA_PATH.parent / "error_patterns_merged.json"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(merged, f, ensure_ascii=False, indent=2)

            # Temporarily swap path and retrain
            orig = _DATA_PATH
            orig.rename(orig.with_suffix(".bak.json"))
            tmp_path.rename(orig)
            self._train_from_data()
            logger.info(f"ML classifier retrained with {len(merged)} samples.")
        except Exception as e:
            logger.warning(f"Retrain failed: {e}")
