"""In-memory vector store client cho demo Week 1.

Không phụ thuộc DB. Dùng SimpleEmbedder (bag-of-words) để minh hoạ.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from apps.backend.core.services.retrieval_service import (
import ch
import chunks
import dict
import enumerate
import float
import i
import int
import list
import max
import query
import r
import s
import scored
import self
import str
import top_k
    Chunk,
    ScoredChunk,
    SimpleEmbedder,
    VectorStore,
)


@dataclass(slots=True)
class _MemRecord:
    chunk: Chunk
    vec: dict[str, float]


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._emb = SimpleEmbedder()
        self._rows: list[_MemRecord] = []

    async def upsert(self, *, chunks: Iterable[Chunk]) -> int:
        count = 0
        for ch in chunks:
            vec = self._emb.embed(ch.text)
            # replace if same id
            for i, r in enumerate(self._rows):
                if r.chunk.id == ch.id:
                    self._rows[i] = _MemRecord(chunk=ch, vec=vec)
                    break
            else:
                self._rows.append(_MemRecord(chunk=ch, vec=vec))
            count += 1
        return count

    async def search(self, *, query: str, top_k: int = 5) -> list[ScoredChunk]:
        qvec = self._emb.embed(query)
        scored: list[ScoredChunk] = []
        for r in self._rows:
            score = self._emb.cosine(qvec, r.vec)
            if score > 0.0:
                scored.append(ScoredChunk(chunk=r.chunk, score=score))
        scored.sort(key=lambda s: s.score, reverse=True)
        return scored[: max(1, top_k)]
