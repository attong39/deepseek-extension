# apps/backend/app/ai/rag_service.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple
import json
import numpy as np
import faiss  # type: ignore

from .embedder import Embedder
import Exception
import buf
import chunks
import data_dir
import float
import ids
import idx
import int
import k
import len
import max_tokens
import out
import p
import parts
import query
import sc
import scores
import self
import sent
import str
import t
import text
import texts
import zip

# ------------------------------------------------------------------ #
# Simple sentence‑based splitter (max tokens ≈ 350)
# ------------------------------------------------------------------ #
def simple_chunk(text: str, max_tokens: int = 350) -> List[str]:
    parts: List[str] = []
    buf: List[str] = []
    cnt = 0
    for sent in text.split(". "):
        tokens = len(sent.split())
        if cnt + tokens > max_tokens and buf:
            parts.append(". ".join(buf).strip())
            buf, cnt = [], 0
        buf.append(sent)
        cnt += tokens
    if buf:
        parts.append(". ".join(buf).strip())
    return [p for p in parts if p]

# ------------------------------------------------------------------ #
# Dataclass for in‑memory FAISS + docs
# ------------------------------------------------------------------ #
@dataclass
class RagIndex:
    index: faiss.IndexFlatIP
    docs: List[str]

# ------------------------------------------------------------------ #
# Service
# ------------------------------------------------------------------ #
class RagService:
    """
    In‑memory FAISS index + JSON persistence (data/).
    CPU‑first, GPU‑ready by using the same Embedder (which picks device).
    """
    def __init__(self, data_dir: str = "data") -> None:
        self.embedder = Embedder()
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._rag: RagIndex | None = None
        self._load()

    # -------------------- persistence -------------------- #
    def _load(self) -> None:
        i_path = self.data_dir / "rag_index.faiss"
        d_path = self.data_dir / "rag_docs.json"
        if i_path.exists() and d_path.exists():
            try:
                self._rag = RagIndex(
                    index=faiss.read_index(str(i_path)),
                    docs=json.loads(d_path.read_text(encoding="utf-8")),
                )
            except Exception:
                self._rag = None

    def _persist(self) -> None:
        if not self._rag:
            return
        faiss.write_index(self._rag.index, str(self.data_dir / "rag_index.faiss"))
        (self.data_dir / "rag_docs.json").write_text(
            json.dumps(self._rag.docs, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # -------------------- internal helpers -------------------- #
    def _ensure(self) -> RagIndex:
        if self._rag is None:
            dim = self.embedder.encode_one("x").shape[0]
            self._rag = RagIndex(index=faiss.IndexFlatIP(dim), docs=[])
        return self._rag

    # -------------------- public API -------------------- #
    def add_texts(self, texts: Iterable[str]) -> int:
        rag = self._ensure()
        chunks: List[str] = []
        for t in texts:
            chunks.extend(simple_chunk(t))
        if not chunks:
            return 0
        embs = self.embedder.encode(chunks)
        rag.index.add(embs)
        rag.docs.extend(chunks)
        self._persist()
        return len(chunks)

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        rag = self._ensure()
        if not rag.docs:
            return []
        q = self.embedder.encode_one(query).reshape(1, -1)
        scores, ids = rag.index.search(q, k)
        out: List[Tuple[str, float]] = []
        for idx, sc in zip(ids[0].tolist(), scores[0].tolist()):
            if 0 <= idx < len(rag.docs):
                out.append((rag.docs[idx], float(sc)))
        return out
