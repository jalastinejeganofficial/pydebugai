"""
Transformer Model — CodeBERT-based semantic fix suggestion engine.
Uses microsoft/codebert-base embeddings to find similar known errors and their fixes.
Cosine similarity retrieval over pre-encoded knowledge base.
Lazy-loaded to avoid slow startup times.
"""
from __future__ import annotations
import json
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any
import numpy as np
from ..models import ErrorCategory, Suggestion

logger = logging.getLogger(__name__)

_PKG_DIR = Path(__file__).parent.parent
_KB_PATH = _PKG_DIR / "data" / "codebert_kb.json"     # knowledge base
_EMBED_CACHE = _PKG_DIR / "models" / "kb_embeddings.npy"  # cached embeddings

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    _TRANSFORMERS_AVAILABLE = False


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


class TransformerModel:
    """
    CodeBERT-based semantic retrieval engine.
    Embeds the error + code context, then retrieves top-K similar
    known fixes from the knowledge base via cosine similarity.

    Falls back gracefully if transformers / torch are not installed.
    """

    MODEL_NAME = "microsoft/codebert-base"
    MAX_TOKEN_LEN = 128

    def __init__(self, lazy: bool = True):
        self._tokenizer = None
        self._model = None
        self._kb: List[Dict[str, Any]] = []
        self._kb_embeddings: Optional[np.ndarray] = None
        self._ready = False

        if not lazy:
            self._initialize()

    def _initialize(self):
        """Load model and knowledge base. Call once before first use."""
        if self._ready:
            return

        if not _TRANSFORMERS_AVAILABLE:
            logger.warning("transformers/torch not installed. CodeBERT engine disabled.")
            return

        try:
            logger.info("Loading CodeBERT model (first use may take a moment)...")
            self._tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
            self._model = AutoModel.from_pretrained(self.MODEL_NAME)
            self._model.eval()
            self._load_knowledge_base()
            self._ready = True
            logger.info("CodeBERT model ready.")
        except Exception as e:
            logger.warning(f"Failed to load CodeBERT: {e}")

    def _load_knowledge_base(self):
        """Load knowledge base and embeddings from disk."""
        if not _KB_PATH.exists():
            logger.warning(f"CodeBERT knowledge base not found at {_KB_PATH}")
            return

        with open(_KB_PATH, "r", encoding="utf-8") as f:
            self._kb = json.load(f)

        # Load or build embeddings cache
        if _EMBED_CACHE.exists():
            self._kb_embeddings = np.load(str(_EMBED_CACHE))
        else:
            logger.info("Building CodeBERT embedding cache for knowledge base...")
            texts = [f"{item['error_message']} {item.get('code_context', '')}"
                     for item in self._kb]
            self._kb_embeddings = np.stack([self._embed(t) for t in texts])
            _EMBED_CACHE.parent.mkdir(exist_ok=True, parents=True)
            np.save(str(_EMBED_CACHE), self._kb_embeddings)
            logger.info(f"Cached {len(self._kb)} embeddings.")

    def _embed(self, text: str) -> np.ndarray:
        """Encode text to a fixed-size embedding vector using CodeBERT."""
        if not self._ready and not _TRANSFORMERS_AVAILABLE:
            return np.zeros(768)

        inputs = self._tokenizer(
            text, return_tensors="pt",
            truncation=True, max_length=self.MAX_TOKEN_LEN,
            padding="max_length",
        )
        with torch.no_grad():
            outputs = self._model(**inputs)
        # Use [CLS] token embedding as sentence representation
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()

    def suggest(self, error_message: str, code_context: str = "",
                line: Optional[int] = None, top_k: int = 3) -> List[Suggestion]:
        """
        Embed the query (error + code) and retrieve top-K similar fixes.
        Returns list of Suggestion objects.
        """
        if not self._ready:
            self._initialize()
        if not self._ready or self._kb_embeddings is None:
            return []

        query_text = f"{error_message} {code_context}".strip()
        if not query_text:
            return []

        try:
            query_vec = self._embed(query_text)
            scores = [
                _cosine_similarity(query_vec, self._kb_embeddings[i])
                for i in range(len(self._kb))
            ]
            top_indices = np.argsort(scores)[-top_k:][::-1]

            suggestions = []
            for idx in top_indices:
                item = self._kb[idx]
                sim = scores[int(idx)]
                if sim < 0.3:   # skip very low similarity results
                    continue
                category = ErrorCategory.__members__.get(
                    item.get("category", "UNKNOWN"), ErrorCategory.UNKNOWN
                )
                suggestions.append(Suggestion(
                    title=item.get("title", "Semantic Fix Suggestion"),
                    explanation=item.get("explanation", ""),
                    fix_code=item.get("fix_code"),
                    line=line,
                    confidence=round(sim * 0.95, 3),  # slight penalty vs exact match
                    source="codebert",
                    category=category,
                    references=item.get("references", []),
                ))
            return suggestions
        except Exception as e:
            logger.warning(f"CodeBERT suggestion failed: {e}")
            return []
