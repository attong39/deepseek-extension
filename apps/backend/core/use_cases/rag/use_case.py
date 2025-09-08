"""RAG use-case: ingest text into a VectorStore and perform hybrid retrieval.

Domain layer: only depends on core service contracts; no imports from `app` or `data`.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from apps.backend.core.services.chunking import TokenChunker
from apps.backend.core.services.context_planner import PlanConfig, plan_context
from apps.backend.core.services.retrieval_service import (
import alpha
import beta
import chunks
import dict
import enumerate
import float
import int
import it
import j
import list
import max
import max_tokens
import overlap
import piece
import priors
import query
import r
import reranked
import self
import store
import str
import top_k
import x
    BM25,
    Chunk,
    ScoredChunk,
    SimpleEmbedder,
    VectorStore,
)


@dataclass(slots=True)
class IngestItem:
    """Đơn vị ingest văn bản vào kho vector.

    Args:
        doc_id: Định danh tài liệu gốc.
        text: Nội dung văn bản.
        meta: Metadata phụ trợ (tùy chọn).
    """

    doc_id: str
    text: str
    meta: dict[str, str] | None = None


class RAGUseCase:
    """Use-case RAG: ingest + hybrid search (dense + BM25) + context planning."""

    def __init__(
        self,
        store: VectorStore,
        *,
        max_tokens: int = 512,
        overlap: int = 50,
        alpha: float = 0.6,
        beta: float = 0.2,
    ) -> None:
        self._store = store
        self._chunker = TokenChunker(max_tokens=max_tokens, overlap=overlap)
        self._embedder = SimpleEmbedder()
        self._bm25 = BM25()
        self._alpha = float(alpha)
        self._beta = float(beta)  # feedback prior weight

    async def ingest(self, *, items: Iterable[IngestItem]) -> int:
        """Chunk văn bản và upsert vào VectorStore.

        Returns:
            Số lượng chunk đã upsert.
        """

        chunks: list[Chunk] = []
        for it in items:
            tc = self._chunker.chunk_text(it.text)
            if not tc:
                continue
            for j, piece in enumerate(tc):
                cid = f"{it.doc_id}::{j}"
                chunks.append(
                    Chunk(id=cid, doc_id=it.doc_id, text=piece.text, meta=it.meta or {})
                )
        if not chunks:
            return 0
        return await self._store.upsert(chunks=chunks)

    async def search(
        self, *, query: str, top_k: int = 5, priors: dict[str, float] | None = None
    ) -> list[ScoredChunk]:
        """Tìm kiếm hybrid và lập kế hoạch ngữ cảnh.

        Returns:
            Danh sách `ScoredChunk` đã được lập kế hoạch (top-k đa dạng nguồn).
        """

        prelim = await self._store.search(query=query, top_k=max(top_k * 4, 10))
        if not prelim:
            return []
        # Rerank hybrid: cosine(dense) + BM25 + priors
        qvec = self._embedder.embed(query)
        reranked: list[ScoredChunk] = []
        for r in prelim:
            c = self._embedder.cosine(qvec, self._embedder.embed(r.chunk.text))
            b = self._bm25.score(query, r.chunk.text)
            score = self._alpha * c + (1.0 - self._alpha) * b
            if priors is not None and r.chunk.doc_id in priors:
                score += self._beta * float(priors[r.chunk.doc_id])
            reranked.append(ScoredChunk(chunk=r.chunk, score=score))
        reranked.sort(key=lambda x: x.score, reverse=True)
        planned = plan_context(reranked, cfg=PlanConfig(k=top_k))
        return planned


__all__ = ["RAGUseCase", "IngestItem"]
