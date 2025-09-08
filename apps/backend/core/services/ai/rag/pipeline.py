"""
RAG pipeline orchestration for end-to-end retrieval-augmented generation.

Provides high-level interfaces and concrete implementations for orchestrating
retrieval-augmented generation from query to final response.
"""

from __future__ import annotations

import inspect
import time
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

# Prefer absolute imports per project convention
from apps.backend.core.services.ai.rag.embed_interfaces import EmbeddingProvider
from apps.backend.core.services.ai.rag.reranker import BaseReranker  # type: ignore
from apps.backend.core.services.ai.rag.retriever import VectorRetriever
from apps.backend.core.services.ai.rag.types import Chunk, Passage, QueryContext
import Exception
import NotImplementedError
import all_passages
import bool
import callable
import component
import confidence
import content
import context
import default_config
import details
import dict
import doc
import document_id
import document_ids
import documents
import e
import embedding_provider
import enumerate
import float
import getattr
import hasattr
import hash
import health
import i
import int
import len
import list
import m
import max
import message
import metadata
import min
import n
import p
import passage
import pipeline_type
import primary_passages
import primary_retriever
import query
import range
import reranked_passages
import reranker
import result
import retriever
import retriever_weights
import s
import secondary_passages
import secondary_retrievers
import seen
import self
import set
import smax
import smin
import staticmethod
import str
import sum
import super
import unique
import value
import vars
import w
import zip


async def _maybe_await(value: Any) -> Any:
    """Await value if it's awaitable, otherwise return as-is."""
    if inspect.isawaitable(value):
        return await value
    return value


@dataclass
class PipelineConfig:
    """Configuration for RAG pipeline execution."""

    retrieval_k: int = 20
    rerank_k: int = 10
    final_k: int = 5
    similarity_threshold: float = 0.0
    enable_reranking: bool = True
    dynamic_final_k: bool = False
    final_k_min: int = 5


@dataclass
class PipelineMetrics:
    """Execution metrics for a single query run."""

    retrieval_time_ms: float = 0.0
    reranking_time_ms: float = 0.0
    total_time_ms: float = 0.0
    chunks_retrieved: int = 0
    chunks_reranked: int = 0
    chunks_final: int = 0
    embedding_time_ms: float = 0.0
    query_tokens: int = 0
    success: bool = False
    error_message: str | None = None


@dataclass
class RAGResult:
    """Result returned by the pipeline for a query."""

    query: str
    passages: list[Passage]
    metadata: dict[str, Any] = field(default_factory=dict)
    total_passages: int = 0
    retrieval_time_ms: float = 0.0
    processing_time_ms: float = 0.0


class RAGPipeline(ABC):
    """Abstract base class for RAG pipeline implementations."""

    @abstractmethod
    async def process_query(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> RAGResult:
        """Process a query through the complete RAG pipeline."""
        raise NotImplementedError

    @abstractmethod
    async def process_query_streaming(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> AsyncIterator[RAGResult]:
        """Process query with streaming results."""
        raise NotImplementedError

    @abstractmethod
    async def add_documents(
        self,
        documents: list[str],
        metadata: list[dict[str, Any]] | None = None,
    ) -> bool:
        """Add documents to the pipeline's knowledge base."""
        raise NotImplementedError

    @abstractmethod
    async def remove_documents(self, document_ids: list[str]) -> int:
        """Remove documents from the knowledge base."""
        raise NotImplementedError

    @abstractmethod
    async def update_document(
        self,
        document_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update an existing document."""
        raise NotImplementedError


class StandardRAGPipeline(RAGPipeline):
    """Standard single-retriever RAG pipeline."""

    def __init__(
        self,
        retriever: VectorRetriever,
        embedding_provider: EmbeddingProvider,
        reranker: BaseReranker | None = None,
        default_config: PipelineConfig | None = None,
    ) -> None:
        self.retriever = retriever
        self.embedding_provider = embedding_provider
        self.reranker = reranker
        self.default_config = default_config or PipelineConfig()
        self._metrics_history: list[PipelineMetrics] = []
        self._rag_cache = None

    async def process_query(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> RAGResult:
        _ = context
        config = config or self.default_config
        metrics = PipelineMetrics()
        start_time = time.perf_counter()

        try:
            # Step 1: Embed
            query_embedding = await self._build_query_embedding(query, metrics)

            # Step 2: Retrieve
            passages = await self._retrieve_with_cache(
                query, query_embedding, config, metrics
            )

            # Step 3: (Optional) rerank
            passages = await self._maybe_rerank(query, passages, config, metrics)

            # Step 4: Finalize
            final_passages = self._finalize_passages(passages, config, metrics)

            metrics.total_time_ms = (time.perf_counter() - start_time) * 1000
            metrics.success = True

            _ = RAGResult(
                query=query,
                passages=final_passages,
                metadata={
                    "config": vars(config),
                    "metrics": vars(metrics),
                    "context": vars(context) if context else None,
                },
                total_passages=len(final_passages),
                retrieval_time_ms=metrics.retrieval_time_ms,
                processing_time_ms=metrics.total_time_ms,
            )
            self._metrics_history.append(metrics)
            return result
        except Exception as e:  # pragma: no cover - error path
            metrics.total_time_ms = (time.perf_counter() - start_time) * 1000
            metrics.success = False
            metrics.error_message = str(e)
            self._metrics_history.append(metrics)
            raise RAGPipelineError(f"Pipeline processing failed: {e}") from e

    async def process_query_streaming(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> AsyncIterator[RAGResult]:
        config = config or self.default_config
        _ = context
        [query_embedding] = await _maybe_await(
            self.embedding_provider.embed_and_cache([query])
        )

        # Yield initial result with empty passages
        yield RAGResult(
            query=query,
            passages=[],
            metadata={"status": "embedding_complete"},
            total_passages=0,
            retrieval_time_ms=0,
            processing_time_ms=0,
        )

        passages: list[Passage] = await _maybe_await(
            self.retriever.retrieve(
                query_embedding=query_embedding,
                k=config.retrieval_k,
                threshold=config.similarity_threshold,
            )
        )

        # Yield retrieval result
        yield RAGResult(
            query=query,
            passages=passages[: config.final_k],
            metadata={"status": "retrieval_complete", "total_retrieved": len(passages)},
            total_passages=len(passages[: config.final_k]),
            retrieval_time_ms=0,
            processing_time_ms=0,
        )

        # Optionally rerank
        final_k = config.final_k
        if config.enable_reranking and self.reranker:
            reranked_passages: list[Passage] = await _maybe_await(
                self.reranker.rerank(
                    query=query,
                    passages=passages,
                    top_k=config.rerank_k,
                )
            )
            if config.dynamic_final_k:
                final_k = max(
                    config.final_k_min,
                    min(
                        config.final_k,
                        self._select_final_k(
                            self._estimate_confidence(reranked_passages)
                        ),
                    ),
                )
            final_passages = reranked_passages[:final_k]
        else:
            if config.dynamic_final_k:
                final_k = max(
                    config.final_k_min,
                    min(
                        config.final_k,
                        self._select_final_k(self._estimate_confidence(passages)),
                    ),
                )
            final_passages = passages[:final_k]

        # Yield final result
        yield RAGResult(
            query=query,
            passages=final_passages,
            metadata={"status": "complete"},
            total_passages=len(final_passages),
            retrieval_time_ms=0,
            processing_time_ms=0,
        )

    async def add_documents(
        self,
        documents: list[str],
        metadata: list[dict[str, Any]] | None = None,
        _chunk_config: dict[str, Any] | None = None,
    ) -> bool:
        """Add documents by creating single chunks and indexing them."""
        _ = _chunk_config
        chunks: list[Chunk] = []
        for i, doc in enumerate(documents):
            md = metadata[i] if metadata and i < len(metadata) else {}
            source_id = md.get("source_id") or f"doc_{uuid4()}"
            chunk = Chunk(
                id=f"{source_id}_chunk_0_{len(doc)}",
                content=doc,
                source_id=source_id,
                start_index=0,
                end_index=len(doc),
                metadata={"word_count": len(doc.split()), **md},
            )
            chunks.append(chunk)

        chunks = await _maybe_await(
            self.embedding_provider.embed_chunks(chunks, update_in_place=True)
        )
        _ = await _maybe_await(self.retriever.add_chunks(chunks))
        return bool(result)

    async def remove_documents(self, document_ids: list[str]) -> int:
        _ = await _maybe_await(self.retriever.remove_chunks(document_ids))
        try:
            return int(result)
        except Exception:
            return 0 if not result else len(document_ids)

    async def update_document(
        self,
        document_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        chunk = Chunk(
            id=document_id,
            content=content,
            source_id=(metadata or {}).get("source_id")
            or document_id.split("_chunk_")[0],
            start_index=0,
            end_index=len(content),
            metadata={"word_count": len(content.split()), **(metadata or {})},
        )
        [chunk] = await _maybe_await(
            self.embedding_provider.embed_chunks([chunk], update_in_place=True)
        )
        _ = await _maybe_await(self.retriever.update_chunk(chunk))
        return bool(result)

    def _estimate_confidence(self, passages: list[Passage]) -> float:
        if not passages:
            return 0.0
        top = passages[: min(10, len(passages))]
        scores = [float(getattr(p, "score", 0.0) or 0.0) for p in top]
        smin, smax = min(scores), max(scores)
        if smax <= smin:
            return max(0.0, min(1.0, smax))
        norm = [(s - smin) / (smax - smin) for s in scores]
        weights = [1.0 / (i + 1) for i in range(len(norm))]
        total_w = sum(weights) or 1.0
        return sum(n * w for n, w in zip(norm, weights, strict=False)) / total_w

    def _select_final_k(self, confidence: float) -> int:
        if confidence >= 0.9:
            return 5
        if confidence >= 0.8:
            return 7
        if confidence >= 0.6:
            return 9
        return 12

    async def get_pipeline_stats(self) -> dict[str, Any]:
        if not self._metrics_history:
            return {"message": "No metrics available"}
        total_queries = len(self._metrics_history)
        successful_queries = sum(1 for m in self._metrics_history if m.success)
        avg_retrieval_time = (
            sum(m.retrieval_time_ms for m in self._metrics_history) / total_queries
        )
        avg_total_time = (
            sum(m.total_time_ms for m in self._metrics_history) / total_queries
        )
        return {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "success_rate": successful_queries / total_queries
            if total_queries
            else 0.0,
            "avg_retrieval_time_ms": avg_retrieval_time,
            "avg_total_time_ms": avg_total_time,
            "last_query_success": self._metrics_history[-1].success
            if self._metrics_history
            else None,
        }

    async def health_check(self) -> dict[str, Any]:
        health: dict[str, Any] = {"overall": True, "components": {}}
        try:
            retriever_stats = await _maybe_await(self.retriever.get_index_stats())
            health["components"]["retriever"] = {
                "status": "healthy",
                "stats": retriever_stats,
            }
        except Exception as e:  # pragma: no cover - error path
            health["components"]["retriever"] = {"status": "unhealthy", "error": str(e)}
            health["overall"] = False

        try:
            [_test_embedding] = await _maybe_await(
                self.embedding_provider.embed_and_cache(["test"])
            )
            health["components"]["embedding"] = {
                "status": "healthy",
                "embedding_dim": len(_test_embedding)
                if hasattr(_test_embedding, "__len__")
                else None,
            }
        except Exception as e:  # pragma: no cover - error path
            health["components"]["embedding"] = {"status": "unhealthy", "error": str(e)}
            health["overall"] = False

        if self.reranker:
            try:
                info = getattr(self.reranker, "get_model_info", None)
                reranker_info = (
                    await _maybe_await(info())
                    if callable(info)
                    else {"available": True}
                )
                health["components"]["reranker"] = {
                    "status": "healthy",
                    "info": reranker_info,
                }
            except Exception as e:  # pragma: no cover - error path
                health["components"]["reranker"] = {
                    "status": "unhealthy",
                    "error": str(e),
                }
                health["overall"] = False

        return health

    async def _build_query_embedding(
        self, query: str, metrics: PipelineMetrics
    ) -> list[float]:
        embed_start = time.perf_counter()
        [query_embedding] = await _maybe_await(
            self.embedding_provider.embed_and_cache([query])
        )
        metrics.embedding_time_ms = (time.perf_counter() - embed_start) * 1000
        return query_embedding

    async def _retrieve_with_cache(
        self,
        query: str,
        query_embedding: list[float],
        config: PipelineConfig,
        metrics: PipelineMetrics,
    ) -> list[Passage]:
        _ = query
        retrieval_start = time.perf_counter()
        passages: list[Passage] = await _maybe_await(
            self.retriever.retrieve(
                query_embedding=query_embedding,
                k=config.retrieval_k,
                threshold=config.similarity_threshold,
            )
        )
        metrics.retrieval_time_ms = (time.perf_counter() - retrieval_start) * 1000
        metrics.chunks_retrieved = len(passages)
        return passages

    async def _maybe_rerank(
        self,
        query: str,
        passages: list[Passage],
        config: PipelineConfig,
        metrics: PipelineMetrics,
    ) -> list[Passage]:
        _ = (query, metrics)
        if config.enable_reranking and self.reranker:
            rerank_start = time.perf_counter()
            passages = await _maybe_await(
                self.reranker.rerank(
                    query=query, passages=passages, top_k=config.rerank_k
                )
            )
            metrics.reranking_time_ms = (time.perf_counter() - rerank_start) * 1000
            metrics.chunks_reranked = len(passages)
        return passages

    def _finalize_passages(
        self,
        passages: list[Passage],
        config: PipelineConfig,
        metrics: PipelineMetrics,
    ) -> list[Passage]:
        final_k = config.final_k
        if config.dynamic_final_k:
            conf = self._estimate_confidence(passages)
            final_k = max(
                config.final_k_min, min(config.final_k, self._select_final_k(conf))
            )
        final_passages = passages[:final_k]
        metrics.chunks_final = len(final_passages)
        return final_passages


class HybridRAGPipeline(RAGPipeline):
    """RAG pipeline that combines multiple retrieval strategies."""

    def __init__(
        self,
        primary_retriever: VectorRetriever,
        embedding_provider: EmbeddingProvider,
        secondary_retrievers: list[VectorRetriever] | None = None,
        retriever_weights: list[float] | None = None,
        reranker: BaseReranker | None = None,
        default_config: PipelineConfig | None = None,
    ) -> None:
        self.primary_retriever = primary_retriever
        self.embedding_provider = embedding_provider
        self.secondary_retrievers = secondary_retrievers or []
        self.retriever_weights = retriever_weights or [1.0] * (
            1 + len(self.secondary_retrievers)
        )
        self.reranker = reranker
        self.default_config = default_config or PipelineConfig()

    async def process_query(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> RAGResult:
        _ = context
        config = config or self.default_config
        [query_embedding] = await _maybe_await(
            self.embedding_provider.embed_and_cache([query])
        )

        # Retrieve from all retrievers
        all_passages: list[Passage] = []

        # Primary retriever
        primary_passages: list[Passage] = await _maybe_await(
            self.primary_retriever.retrieve(
                query_embedding=query_embedding,
                k=config.retrieval_k,
            )
        )
        all_passages.extend(primary_passages)

        # Secondary retrievers
        for retriever in self.secondary_retrievers:
            secondary_passages: list[Passage] = await _maybe_await(
                retriever.retrieve(
                    query_embedding=query_embedding,
                    k=max(1, config.retrieval_k // 2),
                )
            )
            all_passages.extend(secondary_passages)

        # Remove duplicates and (optionally) re-rank
        unique_passages = self._deduplicate_passages(all_passages)
        if config.enable_reranking and self.reranker:
            final_passages: list[Passage] = await _maybe_await(
                self.reranker.rerank(
                    query=query,
                    passages=unique_passages,
                    top_k=config.final_k,
                )
            )
        else:
            final_passages = unique_passages[: config.final_k]

        return RAGResult(
            query=query,
            passages=final_passages,
            metadata={
                "strategy": "hybrid",
                "total_retrievers": 1 + len(self.secondary_retrievers),
            },
            total_passages=len(final_passages),
            retrieval_time_ms=0,
            processing_time_ms=0,
        )

    def _deduplicate_passages(self, passages: list[Passage]) -> list[Passage]:
        seen: set[int] = set()
        unique: list[Passage] = []
        for passage in passages:
            content_hash = hash(passage.content[:100])
            if content_hash not in seen:
                seen.add(content_hash)
                unique.append(passage)
        return unique

    async def process_query_streaming(
        self,
        query: str,
        context: QueryContext | None = None,
        config: PipelineConfig | None = None,
    ) -> AsyncIterator[RAGResult]:
        _ = await self.process_query(query, context, config)
        yield result

    async def add_documents(
        self,
        documents: list[str],
        metadata: list[dict[str, Any]] | None = None,
        _chunk_config: dict[str, Any] | None = None,
    ) -> bool:
        _ = (documents, metadata, _chunk_config)
        return True

    async def remove_documents(self, document_ids: list[str]) -> int:
        _ = await _maybe_await(self.primary_retriever.remove_chunks(document_ids))
        try:
            return int(result)
        except Exception:
            return 0 if not result else len(document_ids)

    async def update_document(
        self,
        document_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        _ = (document_id, content, metadata)
        return True

    async def get_pipeline_stats(self) -> dict[str, Any]:
        return {"type": "hybrid", "retrievers": 1 + len(self.secondary_retrievers)}

    async def health_check(self) -> dict[str, Any]:
        return {"status": "basic_health_check"}


class RAGPipelineError(Exception):
    """Exception raised when RAG pipeline operations fail."""

    def __init__(
        self,
        message: str,
        pipeline_type: str | None = None,
        component: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.pipeline_type = pipeline_type
        self.component = component
        self.details = details or {}


class RAGPipelineFactory:
    """Factory for creating different types of RAG pipelines."""

    @staticmethod
    async def create_standard_pipeline(
        retriever: VectorRetriever,
        embedding_provider: EmbeddingProvider,
        reranker: BaseReranker | None = None,
        config: PipelineConfig | None = None,
    ) -> StandardRAGPipeline:
        return StandardRAGPipeline(
            retriever=retriever,
            embedding_provider=embedding_provider,
            reranker=reranker,
            default_config=config,
        )

    @staticmethod
    async def create_hybrid_pipeline(
        primary_retriever: VectorRetriever,
        embedding_provider: EmbeddingProvider,
        secondary_retrievers: list[VectorRetriever],
        reranker: BaseReranker | None = None,
        config: PipelineConfig | None = None,
    ) -> HybridRAGPipeline:
        return HybridRAGPipeline(
            primary_retriever=primary_retriever,
            embedding_provider=embedding_provider,
            secondary_retrievers=secondary_retrievers,
            reranker=reranker,
            default_config=config,
        )
