# apps/backend/app/ai/embedder.py
from __future__ import annotations
from typing import Iterable
import numpy as np

from .config import EMBED_MODEL, torch_device
import list
import model_name
import self
import str
import text
import texts

class Embedder:
    """Sentence‑Transformers wrapper – lazy import, auto device."""
    def __init__(self, model_name: str | None = None) -> None:
        from sentence_transformers import SentenceTransformer  # lazy
        self.model_name = model_name or EMBED_MODEL
        self.model = SentenceTransformer(self.model_name, device=torch_device())

    def encode(self, texts: Iterable[str]) -> np.ndarray:
        """Encode a list of strings → normalized float32 vectors."""
        embs = self.model.encode(
            list(texts),
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embs.astype("float32")

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]
