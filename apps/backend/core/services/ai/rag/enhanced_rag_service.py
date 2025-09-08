"""Enhanced RAG service for ZETA_AI 2025 with hybrid retrieval and reranking.

This module provides the complete RAG pipeline combining:
- Hybrid retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(vector + lexical search)
- Cross-encoder reranking for precision
- Two-tier caching (LRU + Redis)
- Performance monitoring and observability
- Graceful fallback handling

Architecture:
Query → Cache Check → Hybrid Retrieval → Reranking → Cache Store → Results
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from apps.backend.core.services.ai.rag.cross_encoder_reranker import (
import Exception
import ValueError
import bool
import bypass_cache
import cached_result
import config
import dict
import doc
import documents
import e
import embedder
import enumerate
import float
import i
import int
import len
import list
import print
import property
import r
import result
import self
import str
import sum
import vector_index
    CrossEncoderReranker,
)
from apps.backend.core.services.ai.rag.enhanced_cache import create_rag_cache
from apps.backend.core.services.ai.rag.hybrid_retriever import HybridRetriever
from apps.backend.core.services.ai.rag.types import (
    EmbedderInterface,
    RerankingResult,
    VectorIndexInterface,
)


@dataclass
class RAGServiceConfig:
    """Configuration for enhanced RAG service."""

    # Retrieval settings
    max_candidates: int = 100
    final_results: int = 10
    vector_weight: float = 0.6
    lexical_weight: float = 0.4

    # Reranking settings
    enable_reranking: bool = True
    rerank_top_k: int = 20

    # Caching settings
    cache_capacity: int = 512
    cache_ttl_seconds: int = 3600
    redis_url: str | None = None

    # Performance settings
    max_query_length: int = 512
    timeout_seconds: float = 30.0

    # Observability
    enable_metrics: bool = True
    log_slow_queries: bool = True
    slow_query_threshold: float = 1.0


@dataclass
class RAGMetrics:
    """RAG service performance metrics."""

    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_retrieval_time: float = 0.0
    avg_rerank_time: float = 0.0
    avg_total_time: float = 0.0
    slow_queries: int = 0
    error_count: int = 0

    # Detailed timing
    retrieval_times: list[float] = field(default_factory=list)
    rerank_times: list[float] = field(default_factory=list)
    total_times: list[float] = field(default_factory=list)

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        return self.cache_hits / total if total > 0 else 0.0

    def update_timing(
        self,
        retrieval_time: float,
        rerank_time: float,
        total_time: float,
        is_slow: bool = False,
    ) -> None:
        """Update timing metrics with new measurements."""
        self.retrieval_times.append(retrieval_time)
        self.rerank_times.append(rerank_time)
        self.total_times.append(total_time)

        # Keep only last 1000 measurements for rolling averages
        if len(self.retrieval_times) > 1000:
            self.retrieval_times = self.retrieval_times[-1000:]
            self.rerank_times = self.rerank_times[-1000:]
            self.total_times = self.total_times[-1000:]

        # Update averages
        self.avg_retrieval_time = sum(self.retrieval_times) / len(self.retrieval_times)
        self.avg_rerank_time = sum(self.rerank_times) / len(self.rerank_times)
        self.avg_total_time = sum(self.total_times) / len(self.total_times)

        if is_slow:
            self.slow_queries += 1


@dataclass
class RAGResponse:
    """Response from enhanced RAG service."""

    query: str
    results: list[RerankingResult]
    total_time: float
    retrieval_time: float
    rerank_time: float
    cache_hit: bool
    num_candidates: int
    num_reranked: int

    # Metadata
    config_hash: str | None = None
    timestamp: float | None = None


class EnhancedRAGService:
    """
    Enhanced RAG service with hybrid retrieval and reranking for ZETA_AI 2025.

    This service provides:
    - Hybrid retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(vector + lexical search)
    - Cross-encoder reranking for improved precision
    - Two-tier caching for performance
    - Comprehensive metrics and monitoring
    - Graceful error handling and timeouts
    """

    def __init__(
        self,
        hybrid_retriever: HybridRetriever,
        reranker: CrossEncoderReranker | None = None,
        config: RAGServiceConfig | None = None,
    ):
        """
        Initialize enhanced RAG service.

        Args:
            hybrid_retriever: Hybrid retrieval implementation
            reranker: Optional cross-encoder reranker
            config: Service configuration
        """
        self.config = config or RAGServiceConfig()
        self.hybrid_retriever = hybrid_retriever
        self.reranker = reranker or CrossEncoderReranker()

        # Initialize cache
        self.cache = create_rag_cache(
            redis_url=self.config.redis_url,
            capacity=self.config.cache_capacity,
            ttl_seconds=self.config.cache_ttl_seconds,
        )

        # Metrics
        self.metrics = RAGMetrics()
        self._start_time = time.time()

    def _make_cache_key(self, query: str) -> str:
        """Generate cache key for query."""
        # Include config parameters that affect results
        config_params = {
            "max_candidates": self.config.max_candidates,
            "final_results": self.config.final_results,
            "vector_weight": self.config.vector_weight,
            "lexical_weight": self.config.lexical_weight,
            "enable_reranking": self.config.enable_reranking,
            "rerank_top_k": self.config.rerank_top_k,
        }

        # Create deterministic key
        import hashlib
        import json

        cache_data = {"query": query.strip().lower(), "config": config_params}

        cache_str = json.dumps(cache_data, sort_keys=True)
        cache_hash = hashlib.sha256(cache_str.encode()).hexdigest()[:16]

        return f"rag_query:{cache_hash}"

    async def search(
        self,
        query: str,
        max_results: int | None = None,
        bypass_cache: bool = False,
        timeout: float | None = None,
    ) -> RAGResponse:
        """
        Execute RAG search with hybrid retrieval and reranking.

        Args:
            query: Search query
            max_results: Maximum number of results to return
            bypass_cache: Whether to bypass cache lookup
            timeout: Query timeout in seconds

        Returns:
            RAG response with results and metadata
        """
        start_time = time.time()
        timeout = timeout or self.config.timeout_seconds
        max_results = max_results or self.config.final_results

        # Validate query
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if len(query) > self.config.max_query_length:
            raise ValueError(
                f"Query too long: {len(query)} > {self.config.max_query_length}"
            )

        query = query.strip()
        self.metrics.total_queries += 1

        # Check cache first
        cache_key = self._make_cache_key(query)

        if not bypass_cache:
            try:
                self.cache.get(cache_key)
                if cached_result:
                    self.metrics.cache_hits += 1

                    # Reconstruct response from cache
                    return RAGResponse(
                        query=query,
                        results=cached_result["results"],
                        total_time=time.time() - start_time,
                        retrieval_time=cached_result.get("retrieval_time", 0.0),
                        rerank_time=cached_result.get("rerank_time", 0.0),
                        cache_hit=True,
                        num_candidates=cached_result.get("num_candidates", 0),
                        num_reranked=cached_result.get("num_reranked", 0),
                        config_hash=cache_key,
                        timestamp=start_time,
                    )
            except Exception as e:
                print(f"Cache lookup error: {e}")

        self.metrics.cache_misses += 1

        try:
            # Step 1: Hybrid retrieval
            retrieval_start = time.time()

            # Create query object for hybrid retriever
            from apps.backend.core.services.ai.rag.types import Query

            query_obj = Query(text=query, top_k=self.config.max_candidates)

            retrieval_results = self.hybrid_retriever.retrieve(query_obj)

            retrieval_time = time.time() - retrieval_start

            # Step 2: Reranking (if enabled)
            rerank_start = time.time()
            final_results = []

            if self.config.enable_reranking and self.reranker:
                # Select top candidates for reranking
                rerank_candidates = retrieval_results[: self.config.rerank_top_k]

                try:
                    # Create query object for reranker
                    query_obj_rerank = Query(text=query, top_k=max_results)

                    reranked_results = self.reranker.rerank(
                        query=query_obj_rerank,
                        items=rerank_candidates,
                        top_k=max_results,
                    )

                    # Convert to RerankingResult format
                    final_results = []
                    for i, result in enumerate(reranked_results):
                        final_results.append(
                            RerankingResult(
                                index=i,
                                score=result.score,
                                content=result.text,
                                source=result.doc_id,
                                metadata=result.meta,
                            )
                        )

                except Exception as e:
                    print(f"Reranking failed, using retrieval results: {e}")
                    # Fallback to retrieval results
                    final_results = [
                        RerankingResult(
                            index=i,
                            score=r.score,
                            content=r.text,
                            source=r.doc_id,
                            metadata=r.meta,
                        )
                        for i, r in enumerate(retrieval_results[:max_results])
                    ]
            else:
                # No reranking, use retrieval results directly
                final_results = [
                    RerankingResult(
                        index=i,
                        score=r.score,
                        content=r.text,
                        source=r.doc_id,
                        metadata=r.meta,
                    )
                    for i, r in enumerate(retrieval_results[:max_results])
                ]

            rerank_time = time.time() - rerank_start
            total_time = time.time() - start_time

            # Check for slow query
            is_slow = total_time > self.config.slow_query_threshold
            if is_slow and self.config.log_slow_queries:
                print(f"Slow RAG query ({total_time:.2f}s): {query[:100]}...")

            # Update metrics
            if self.config.enable_metrics:
                self.metrics.update_timing(
                    retrieval_time=retrieval_time,
                    rerank_time=rerank_time,
                    total_time=total_time,
                    is_slow=is_slow,
                )

            # Cache result
            try:
                cache_data = {
                    "results": final_results,
                    "retrieval_time": retrieval_time,
                    "rerank_time": rerank_time,
                    "num_candidates": len(retrieval_results),
                    "num_reranked": len(final_results),
                }
                self.cache.put(cache_key, cache_data)
            except Exception as e:
                print(f"Cache store error: {e}")

            return RAGResponse(
                query=query,
                results=final_results,
                total_time=total_time,
                retrieval_time=retrieval_time,
                rerank_time=rerank_time,
                cache_hit=False,
                num_candidates=len(retrieval_results),
                num_reranked=len(final_results),
                config_hash=cache_key,
                timestamp=start_time,
            )

        except Exception as e:
            self.metrics.error_count += 1
            print(f"RAG search error: {e}")
            raise

    def get_metrics(self) -> dict[str, Any]:
        """Get comprehensive service metrics."""
        cache_stats = self.cache.get_stats()

        return {
            "rag_metrics": {
                "total_queries": self.metrics.total_queries,
                "cache_hit_rate": self.metrics.cache_hit_rate,
                "avg_retrieval_time": self.metrics.avg_retrieval_time,
                "avg_rerank_time": self.metrics.avg_rerank_time,
                "avg_total_time": self.metrics.avg_total_time,
                "slow_queries": self.metrics.slow_queries,
                "error_count": self.metrics.error_count,
                "uptime_seconds": time.time() - self._start_time,
            },
            "cache_metrics": {
                "memory_hits": cache_stats.memory_hits,
                "memory_misses": cache_stats.memory_misses,
                "redis_hits": cache_stats.redis_hits,
                "redis_misses": cache_stats.redis_misses,
                "memory_size": cache_stats.memory_size,
                "memory_capacity": cache_stats.memory_capacity,
                "hit_rate": cache_stats.hit_rate,
                "redis_hit_rate": cache_stats.redis_hit_rate,
            },
            "config": {
                "max_candidates": self.config.max_candidates,
                "final_results": self.config.final_results,
                "vector_weight": self.config.vector_weight,
                "lexical_weight": self.config.lexical_weight,
                "enable_reranking": self.config.enable_reranking,
                "rerank_top_k": self.config.rerank_top_k,
            },
        }

    def health_check(self) -> dict[str, Any]:
        """Check service health status."""
        cache_health = self.cache.health_check()

        health = {
            "status": "healthy",
            "cache": cache_health,
            "metrics": {
                "total_queries": self.metrics.total_queries,
                "error_rate": (
                    self.metrics.error_count / self.metrics.total_queries
                    if self.metrics.total_queries > 0
                    else 0.0
                ),
                "avg_response_time": self.metrics.avg_total_time,
            },
        }

        # Determine overall health
        if cache_health.get("redis_cache") == "unhealthy":
            health["status"] = "degraded"

        error_rate = health["metrics"]["error_rate"]
        if error_rate > 0.1:  # > 10% error rate
            health["status"] = "unhealthy"

        return health

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.metrics = RAGMetrics()
        self.cache.reset_stats()
        self._start_time = time.time()


# === Factory Function ===


async def create_enhanced_rag_service(
    vector_index: VectorIndexInterface,
    embedder: EmbedderInterface,
    documents: list[str],
    config: RAGServiceConfig | None = None,
) -> EnhancedRAGService:
    """
    Create an enhanced RAG service with all components.

    Args:
        vector_index: Vector index implementation
        embedder: Embedding model
        documents: Documents to index
        config: Service configuration

    Returns:
        Configured RAG service ready for production use
    """
    from apps.backend.core.services.ai.rag.lexical_index import LexicalIndex

    # Create lexical index
    lexical_index = LexicalIndex()

    # Create hybrid retriever with correct parameters
    hybrid_retriever = HybridRetriever(
        embedder=embedder, index=vector_index, lexical_index=lexical_index
    )

    # Build indices (simplified for demo)
    # In production, this would be more sophisticated
    embeddings = await embedder.embed_batch(documents)
    await vector_index.add_documents(documents, embeddings)

    # Add documents to lexical index
    from apps.backend.core.services.ai.rag.types import Chunk

    chunks = [
        Chunk(doc_id=f"doc_{i}", idx=0, text=doc, meta={})
        for i, doc in enumerate(documents)
    ]
    hybrid_retriever.add_chunks_to_lexical(chunks)

    # Create reranker
    reranker = CrossEncoderReranker()

    # Create service
    return EnhancedRAGService(
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
        config=config or RAGServiceConfig(),
    )
