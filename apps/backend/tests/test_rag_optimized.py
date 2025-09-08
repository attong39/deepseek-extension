"""Unit tests for OptimizedRAG pipeline using simple fakes.

Validates multi-query rewrite + parallel retrieval + rerank hook path.
"""

from __future__ import annotations

from typing import Any

import pytest
from apps.backend.core.services.ai.rag.embed_interfaces import EmbeddingProvider
from apps.backend.core.services.ai.rag.optimized import (
    OptimizedRAG,
    OptimizedRetrievalTargets,
)
from apps.backend.core.services.ai.rag.retriever import VectorRetriever
from apps.backend.core.services.ai.rag.types import Chunk, Passage, QueryContext


class FakeEmbeddingProvider(EmbeddingProvider):
    async def embed_and_cache(
        self,
        texts: list[str],
        cache_key_prefix: str | None = None,
        force_refresh: bool = False,
    ) -> list[list[float]]:
        return [[float(i)] * 4 for i, _ in enumerate(texts)]

    async def embed_chunks(
        self, chunks: list[Chunk], update_in_place: bool = True
    ) -> list[Chunk]:
        for i, c in enumerate(chunks):
            c.embedding = [float(i)] * 4
        return chunks

    async def get_model_info(self) -> dict[str, Any]:
        return {"name": "fake", "dim": 4}

    async def health_check(self) -> dict[str, Any]:
        return {"ok": True}


class FakeVectorRetriever(VectorRetriever):
    async def retrieve(
        self,
        query_embedding: list[float],
        k: int = 10,
        filters: dict[str, Any] | None = None,
        threshold: float | None = None,
    ) -> list[Passage]:
        # Produce k dummy passages with decreasing scores
        res: list[Passage] = []
        for i in range(min(k, 5)):
            ch = Chunk(
                id=f"c{i}",
                content=f"content {i}",
                source_id="s",
                start_index=0,
                end_index=1,
                metadata={},
            )
            res.append(Passage(chunk=ch, score=1.0 - i * 0.1, rank=i))
        return res

    async def add_chunks(
        self, chunks: list[Chunk]
    ) -> bool:  # pragma: no cover - not used
        return True

    async def remove_chunks(
        self, chunk_ids: list[str]
    ) -> int:  # pragma: no cover - not used
        return len(chunk_ids)

    async def update_chunk(self, chunk: Chunk) -> bool:  # pragma: no cover - not used
        return True

    async def get_index_stats(self) -> dict[str, Any]:  # pragma: no cover - not used
        return {"count": 0}


@pytest.mark.asyncio
async def test_optimized_rag_enhanced_retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval() -> None:
    emb = FakeEmbeddingProvider()
    vec = FakeVectorRetriever()
    key = FakeVectorRetriever()  # reuse for keyword path
    rag = OptimizedRAG(
        embedding_provider=emb,
        vector_retriever=vec,
        keyword_retriever=key,
        targets=OptimizedRetrievalTargets(top_k_vectors=3, top_k_keywords=2, final_k=4),
        max_concurrency=2,
    )

    passages = await rag.enhanced_retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval("test query", context=QueryContext())
    # Expect at most final_k, and non-empty
    assert 0 < len(passages) <= 4
    # Ensure dedup returns unique by content prefix
    seen = set()
    for p in passages:
        sig = p.content[:10]
        assert sig not in seen
        seen.add(sig)
