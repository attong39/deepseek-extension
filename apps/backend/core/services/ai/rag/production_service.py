"""
Production RAG Service - Enhanced RAG pipeline for production use.

Integrates with core adapters to provide a robust, scalable RAG implementation
with advanced features like query optimization, result ranking, and caching.
"""

from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from apps.backend.core.observability.logging import get_logger
from apps.backend.core.performance.smart_cache import smart_cache
from apps.backend.core.services.ai.orchestrator import (
import Exception
import ValueError
import any
import bool
import chunk
import chunking_service
import dict
import document
import e
import embedding_adapter
import enumerate
import float
import i
import int
import len
import list
import min
import property
import request
import result
import results
import self
import set
import sorted
import source
import str
import super
import tuple
import vector_store
import word
import x
    AIRequest,
    AIResponse,
    BaseAIService,
)
from apps.backend.core.services.ai.registry import CapabilityProvider
from apps.backend.data.adapters.vector import (
    ChunkingService,
    MemoryVectorStoreAdapter,
    OpenAIEmbeddingAdapter,
)

logger = get_logger(__name__)


@dataclass
class RAGQuery:
    """RAG query structure."""

    query: str
    max_results: int = 5
    similarity_threshold: float = 0.7
    filters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RAGDocument:
    """Document structure for RAG indexing."""

    id: str
    content: str
    title: str = ""
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    indexed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class RAGResult:
    """RAG search result."""

    document_id: str
    content: str
    title: str
    source: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "document_id": self.document_id,
            "content": self.content,
            "title": self.title,
            "source": self.source,
            "score": self.score,
            "metadata": self.metadata,
        }


@dataclass
class RAGResponse:
    """RAG response with retrieved documents and generated answer."""

    query: str
    answer: str
    sources: list[RAGResult]
    confidence: float
    processing_time_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)


class QueryOptimizer:
    """Optimizes queries for better retrieval performance."""

    def __init__(self) -> None:
        self._expansion_terms = {
            "AI": ["artificial intelligence", "machine learning", "neural networks"],
            "software": ["application", "program", "code", "development"],
            "data": ["information", "dataset", "records", "database"],
            "user": ["customer", "client", "person", "individual"],
            "system": ["platform", "infrastructure", "architecture", "framework"],
        }

    async def optimize_query(self, query: str) -> str:
        """Optimize query for better retrieval."""
        # Simple query expansion
        words = query.lower().split()
        expanded_terms = []

        for word in words:
            expanded_terms.append(word)
            if word in self._expansion_terms:
                expanded_terms.extend(
                    self._expansion_terms[word][:2]
                )  # Add top 2 synonyms

        # Remove duplicates while preserving order
        seen = set()
        optimized_words = []
        for word in expanded_terms:
            if word not in seen:
                optimized_words.append(word)
                seen.add(word)

        return " ".join(optimized_words)


class ResultRanker:
    """Ranks and filters search results."""

    def __init__(self) -> None:
        self._boost_factors = {
            "title_match": 1.5,
            "recent_document": 1.2,
            "high_quality_source": 1.3,
        }

    async def rank_results(
        self, results: list[RAGResult], query: str, max_results: int = 5
    ) -> list[RAGResult]:
        """Rank and filter results."""
        query_lower = query.lower()

        # Apply ranking boosts
        for result in results:
            # Title match boost
            if query_lower in result.title.lower():
                result.score *= self._boost_factors["title_match"]

            # Recent document boost (placeholder logic)
            if "recent" in result.metadata:
                result.score *= self._boost_factors["recent_document"]

            # High quality source boost
            if result.source in ["documentation", "official", "authoritative"]:
                result.score *= self._boost_factors["high_quality_source"]

        # Sort by score descending
        ranked_results = sorted(results, key=lambda x: x.score, reverse=True)

        return ranked_results[:max_results]


class AnswerGenerator:
    """Generates answers from retrieved context."""

    def __init__(self) -> None:
        self._answer_templates = {
            "factual": "Based on the information provided: {context}",
            "procedural": "Here's how to {query}: {context}",
            "definition": "{query} refers to: {context}",
            "comparison": "Comparing the options: {context}",
            "default": "According to the available information: {context}",
        }

    async def generate_answer(
        self, query: str, results: list[RAGResult]
    ) -> tuple[str, float]:
        """Generate answer from retrieved results."""
        if not results:
            return "I couldn't find relevant information to answer your question.", 0.0

        # Combine context from top results
        context_parts = []
        total_score = 0.0

        for result in results[:3]:  # Use top 3 results
            context_parts.append(f"From {result.source}: {result.content}")
            total_score += result.score

        context = " ".join(context_parts)

        # Simple answer generation (placeholder for real LLM integration)
        query_type = self._classify_query_type(query)
        template = self._answer_templates.get(
            query_type, self._answer_templates["default"]
        )

        answer = template.format(
            query=query, context=context[:500]
        )  # Limit context length
        confidence = min(total_score / len(results), 1.0)

        return answer, confidence

    def _classify_query_type(self, query: str) -> str:
        """Classify query type for answer generation."""
        query_lower = query.lower()

        if any(word in query_lower for word in ["what is", "define", "definition"]):
            return "definition"
        elif any(word in query_lower for word in ["how to", "how do", "step"]):
            return "procedural"
        elif any(word in query_lower for word in ["compare", "difference", "vs"]):
            return "comparison"
        elif any(word in query_lower for word in ["who", "when", "where", "which"]):
            return "factual"
        else:
            return "default"


class ProductionRAGService(BaseAIService, CapabilityProvider):
    """
    Production-ready RAG service with advanced features.

    Integrates with core adapters for embedding, chunking, and vector storage.
    Provides query optimization, result ranking, and answer generation.
    """

    def __init__(
        self,
        embedding_adapter: OpenAIEmbeddingAdapter | None = None,
        vector_store: MemoryVectorStoreAdapter | None = None,
        chunking_service: ChunkingService | None = None,
    ) -> None:
        super().__init__("production_rag_service")

        # Use provided adapters or create defaults
        self._embedding_adapter = embedding_adapter or OpenAIEmbeddingAdapter()
        self._vector_store = vector_store or MemoryVectorStoreAdapter()
        self._chunking_service = chunking_service or ChunkingService()

        # RAG components
        self._query_optimizer = QueryOptimizer()
        self._result_ranker = ResultRanker()
        self._answer_generator = AnswerGenerator()

        # Document storage
        self._documents: dict[str, RAGDocument] = {}
        self._query_cache: dict[str, RAGResponse] = {}
        self._cache_ttl = 3600  # 1 hour

    @property
    def capability_name(self) -> str:
        """Capability name."""
        return "rag"

    @property
    def capability_version(self) -> str:
        """Capability version."""
        return "1.0.0"

    async def _start_service(self) -> None:
        """Start the RAG service."""
        # Core adapters don't need explicit initialization in this case
        # Just validate they exist
        if not self._embedding_adapter:
            raise ValueError("Embedding adapter required")
        if not self._vector_store:
            raise ValueError("Vector store required")
        if not self._chunking_service:
            raise ValueError("Chunking service required")

        logger.info("Production RAG service started")

    async def _stop_service(self) -> None:
        """Stop the RAG service."""
        # Cleanup if needed
        logger.info("Production RAG service stopped")

    async def initialize(self) -> None:
        """Initialize the capability."""
        await self.start()

    async def shutdown(self) -> None:
        """Shutdown the capability."""
        await self.stop()

    async def index_document(self, document: RAGDocument) -> bool:
        """Index a document for retrieval."""
        try:
            # Chunk the document using sync method
            chunks = self._chunking_service.chunk(
                document.content, chunk_size=500, chunk_overlap=50
            )

            # Generate embeddings and store chunks
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document.id}_chunk_{i}"

                # Generate embedding using correct method
                embedding = await self._embedding_adapter.embed_query(chunk)

                # Store in vector store
                await self._vector_store.store_vector(
                    vector_id=chunk_id,
                    vector=embedding,
                    metadata={
                        "document_id": document.id,
                        "chunk_index": i,
                        "title": document.title,
                        "source": document.source,
                        "content": chunk,  # chunk is string, not object
                        **document.metadata,
                    },
                )

            # Store document metadata
            self._documents[document.id] = document

            logger.info(f"Indexed document {document.id} with {len(chunks)} chunks")
            return True

        except Exception as e:
            logger.error(f"Error indexing document {document.id}: {e}")
            return False

    @smart_cache(ttl=300, max_size=1000, cache_key_prefix="rag_search")
    async def search(self, query: RAGQuery) -> list[RAGResult]:
        """Search for relevant documents."""
        try:
            # Optimize query
            optimized_query = await self._query_optimizer.optimize_query(query.query)

            # Generate query embedding
            query_embedding = await self._embedding_adapter.embed_query(optimized_query)

            # Search vector store
            search_results = await self._vector_store.search_similar(
                query_vector=query_embedding,
                top_k=query.max_results * 2,  # Get more for ranking
                threshold=query.similarity_threshold,
            )

            # Convert to RAG results
            rag_results = []
            for result in search_results:
                metadata = result.get("metadata", {})
                rag_results.append(
                    RAGResult(
                        document_id=metadata.get("document_id", ""),
                        content=metadata.get("content", ""),
                        title=metadata.get("title", ""),
                        source=metadata.get("source", ""),
                        score=result.get("score", 0.0),
                        metadata=metadata,
                    )
                )

            # Rank and filter results
            ranked_results = await self._result_ranker.rank_results(
                rag_results, query.query, query.max_results
            )

            return ranked_results

        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

    @smart_cache(ttl=600, max_size=500, cache_key_prefix="rag_query")
    async def query(self, query: RAGQuery) -> RAGResponse:
        """Execute RAG query with answer generation."""
        start_time = asyncio.get_event_loop().time()

        try:
            # Check cache
            cache_key = self._get_cache_key(query)
            if cache_key in self._query_cache:
                cached_response = self._query_cache[cache_key]
                # Simple TTL check (real implementation would be more sophisticated)
                return cached_response

            # Search for relevant documents
            search_results = await self.search(query)

            # Generate answer
            answer, confidence = await self._answer_generator.generate_answer(
                query.query, search_results
            )

            processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

            # Create response
            response = RAGResponse(
                query=query.query,
                answer=answer,
                sources=search_results,
                confidence=confidence,
                processing_time_ms=processing_time,
                metadata={
                    "optimized_query": await self._query_optimizer.optimize_query(
                        query.query
                    ),
                    "num_sources": len(search_results),
                    "cached": False,
                },
            )

            # Cache response
            self._query_cache[cache_key] = response

            return response

        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

            return RAGResponse(
                query=query.query,
                answer="I'm sorry, I encountered an error while processing your query.",
                sources=[],
                confidence=0.0,
                processing_time_ms=processing_time,
                metadata={"error": str(e)},
            )

    async def process(self, request: AIRequest) -> AIResponse:
        """Process RAG request."""
        try:
            # Extract query parameters
            query_text = request.payload.get("query", "")
            max_results = request.payload.get("max_results", 5)
            similarity_threshold = request.payload.get("similarity_threshold", 0.7)

            if not query_text:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error="No query provided",
                )

            # Create RAG query
            rag_query = RAGQuery(
                query=query_text,
                max_results=max_results,
                similarity_threshold=similarity_threshold,
                metadata=request.context or {},
            )

            # Execute query
            rag_response = await self.query(rag_query)

            return AIResponse(
                request_id=request.request_id,
                success=True,
                result={
                    "answer": rag_response.answer,
                    "sources": [source.to_dict() for source in rag_response.sources],
                    "confidence": rag_response.confidence,
                    "metadata": rag_response.metadata,
                },
                metadata={
                    "processing_time_ms": rag_response.processing_time_ms,
                    "num_sources": len(rag_response.sources),
                },
            )

        except Exception as e:
            logger.error(f"Error processing RAG request: {e}")
            return AIResponse(
                request_id=request.request_id,
                success=False,
                error=f"RAG processing error: {str(e)}",
            )

    async def get_document_stats(self) -> dict[str, Any]:
        """Get document indexing statistics."""
        return {
            "total_documents": len(self._documents),
            "total_vectors": await self._vector_store.get_vector_count(),
            "cache_entries": len(self._query_cache),
            "service_status": self.status.value,
        }

    def _get_cache_key(self, query: RAGQuery) -> str:
        """Generate cache key for query."""
        key_data = f"{query.query}_{query.max_results}_{query.similarity_threshold}"
        return hashlib.sha256(key_data.encode()).hexdigest()
