"""RAG pipeline types and core data structures.

Defines the core types used throughout the RAG pipeline without any
vendor-specific implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
from uuid import UUID, uuid4
import bool
import c
import dict
import float
import int
import len
import list
import property
import self
import str


class ChunkingStrategy(Enum):
    """Text chunking strategies."""

    FIXED_SIZE = "fixed_size"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"


class SimilarityMetric(Enum):
    """Similarity measurement metrics."""

    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"
    MANHATTAN = "manhattan"


@dataclass
class Chunk:
    """Text chunk with metadata."""

    id: str
    content: str
    source_id: str
    start_index: int
    end_index: int
    metadata: dict[str, Any]
    embedding: list[float] | None = None

    def __post_init__(self) -> None:
        """Initialize chunk with UUID if not provided."""
        if not self.id:
            self.id = str(uuid4())


@dataclass
class Passage:
    """Retrieved passage from knowledge base."""

    chunk: Chunk
    score: float
    rank: int
    context_chunks: list[Chunk] | None = None

    @property
    def content(self) -> str:
        """Get passage content."""
        return self.chunk.content

    @property
    def metadata(self) -> dict[str, Any]:
        """Get passage metadata."""
        return self.chunk.metadata


@dataclass
class ScoredPassage:
    """Passage with relevance score."""

    passage: Passage
    relevance_score: float
    confidence: float
    reasoning: str | None = None


@dataclass
class Citation:
    """Citation for retrieved information."""

    source_id: str
    source_title: str | None
    chunk_id: str
    content_snippet: str
    page_number: int | None = None
    url: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class QueryContext:
    """Context for RAG query processing."""

    user_id: UUID | None = None
    session_id: str | None = None
    conversation_history: list[str] | None = None
    domain_filters: dict[str, Any] | None = None
    language: str = "en"
    max_context_length: int = 4000


@dataclass
class RetrievalResult:
    """Result from retrieval stage."""

    query: str
    passages: list[Passage]
    total_found: int
    search_time_ms: float
    context: QueryContext

    @property
    def top_passage(self) -> Passage | None:
        """Get the highest-scoring passage."""
        return self.passages[0] if self.passages else None


@dataclass
class RerankingResult:
    """Result from reranking stage."""

    original_passages: list[Passage]
    reranked_passages: list[ScoredPassage]
    reranking_time_ms: float
    model_used: str | None = None


@dataclass
class GenerationContext:
    """Context for answer generation."""

    query: str
    passages: list[ScoredPassage]
    system_prompt: str | None = None
    temperature: float = 0.7
    max_tokens: int = 1000
    include_citations: bool = True


@dataclass
class AnswerWithCitations:
    """Generated answer with supporting citations."""

    answer: str
    citations: list[Citation]
    confidence_score: float
    generation_time_ms: float
    model_used: str | None = None
    metadata: dict[str, Any] | None = None

    @property
    def has_citations(self) -> bool:
        """Check if answer has citations."""
        return len(self.citations) > 0


@dataclass
class RAGMetrics:
    """Performance metrics for RAG pipeline."""

    total_time_ms: float
    retrieval_time_ms: float
    reranking_time_ms: float
    generation_time_ms: float
    chunks_retrieved: int
    chunks_used: int
    confidence_score: float

    @property
    def retrieval_efficiency(self) -> float:
        """Calculate retrieval efficiency (chunks used / chunks retrieved)."""
        if self.chunks_retrieved == 0:
            return 0.0
        return self.chunks_used / self.chunks_retrieved


@dataclass
class RAGResponse:
    """Complete RAG pipeline response."""

    query: str
    answer: AnswerWithCitations
    retrieval_result: RetrievalResult
    reranking_result: RerankingResult | None
    metrics: RAGMetrics
    context: QueryContext

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "query": self.query,
            "answer": self.answer.answer,
            "citations": [
                {
                    "source_id": c.source_id,
                    "source_title": c.source_title,
                    "content_snippet": c.content_snippet,
                    "page_number": c.page_number,
                    "url": c.url,
                    "metadata": c.metadata,
                }
                for c in self.answer.citations
            ],
            "confidence": self.answer.confidence_score,
            "metrics": {
                "total_time_ms": self.metrics.total_time_ms,
                "retrieval_time_ms": self.metrics.retrieval_time_ms,
                "reranking_time_ms": self.metrics.reranking_time_ms,
                "generation_time_ms": self.metrics.generation_time_ms,
                "chunks_retrieved": self.metrics.chunks_retrieved,
                "chunks_used": self.metrics.chunks_used,
                "retrieval_efficiency": self.metrics.retrieval_efficiency,
            },
        }
