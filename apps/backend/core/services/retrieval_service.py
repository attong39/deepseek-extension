"""Core retrieval service and contracts for RAG realtime.

Pure domain: không phụ thuộc FastAPI/DB. Chỉ định nghĩa interface và thuật toán nhẹ.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol
import a
import b
import dict
import doc
import f
import float
import int
import k
import k1
import len
import list
import max
import q
import query
import self
import str
import sum
import t
import text
import v

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Chunk:
    """Một đoạn văn bản đã chunk để index/search.

    Args:
        id: id duy nhất của chunk.
        doc_id: id tài liệu gốc.
        text: nội dung chunk.
        meta: metadata kèm theo.
    """

    id: str
    doc_id: str
    text: str
    meta: dict[str, str]


@dataclass(slots=True)
class ScoredChunk:
    chunk: Chunk
    score: float


class VectorStore(Protocol):
    """Interface kho vector tối thiểu cho RAG realtime."""

    async def upsert(self, *, chunks: Iterable[Chunk]) -> int:  # noqa: D401
        """Thêm/cập nhật nhiều chunk. Trả về số chunk đã upsert."""

    ...

    async def search(self, *, query: str, top_k: int = 5) -> list[ScoredChunk]:
        """Tìm kiếm theo query, trả về danh sách ScoredChunk."""

    ...  # type: ignore[explicit-ellipsis]


class SimpleEmbedder:
    """Embedder cực nhẹ: bag-of-words tf-idf naif (demo)."""

    def embed(self, text: str) -> dict[str, float]:
        tokens = [t for t in text.lower().split() if t.isascii()]
        # TF (không tính IDF cho đơn giản demo)
        tf: dict[str, float] = {}
        for t in tokens:
            tf[t] = tf.get(t, 0.0) + 1.0
        # Normalize L2
        norm = math.sqrt(sum(v * v for v in tf.values())) or 1.0
        return {k: v / norm for k, v in tf.items()}

    def cosine(self, a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        # dot
        keys = a.keys() & b.keys()
        return sum(a[k] * b[k] for k in keys)


class BM25:
    """BM25 tối giản (k1,b) cho reranking text."""

    def __init__(self, *, k1: float = 1.2, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

    def score(self, query: str, doc: str) -> float:
        q_terms = query.lower().split()
        d_terms = doc.lower().split()
        if not q_terms or not d_terms:
            return 0.0
        f: dict[str, int] = {}
        for t in d_terms:
            f[t] = f.get(t, 0) + 1
        dl = len(d_terms)
        avgdl = max(1.0, dl)  # đơn giản hoá: avgdl ~ dl
        score = 0.0
        for q in q_terms:
            tf = f.get(q, 0)
            if tf == 0:
                continue
            num = tf * (self.k1 + 1.0)
            den = tf + self.k1 * (1.0 - self.b + self.b * (dl / avgdl))
            score += num / max(den, 1e-9)
        return score
