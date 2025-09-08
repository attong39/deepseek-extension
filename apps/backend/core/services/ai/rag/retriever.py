"""Retrieval interfaces for RAG pipeline.

Defines abstract interfaces for document retrieval without vendor lock-in.
Implementations will be provided in data layer adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any
import Exception
import bool
import details
import dict
import float
import int
import list
import message
import retriever_name
import self
import str
import super

if TYPE_CHECKING:
    from apps.backend.core.services.ai.rag.types import (
        Chunk,
        Passage,
        QueryContext,
        RetrievalResult,
    )


class VectorRetriever(ABC):
    """Abstract interface for vector-based retrieval."""

    @abstractmethod
    async def retrieve(
        self,
        query_embedding: list[float],
        k: int = 10,
        filters: dict[str, Any] | None = None,
        threshold: float | None = None,
    ) -> list[Passage]:
        """Retrieve most similar passages using vector similarity.

        Args:
            query_embedding: Query embedding vector
            k: Number of passages to retrieve
            filters: Optional metadata filters
            threshold: Optional similarity threshold

        Returns:
            List of retrieved passages with scores

        Raises:
            RetrievalError: If retrieval fails
        """

    @abstractmethod
    async def add_chunks(self, chunks: list[Chunk]) -> bool:
        """Add chunks to the retrieval index.

        Args:
            chunks: List of chunks to index

        Returns:
            True if successful

        Raises:
            RetrievalError: If indexing fails
        """

    @abstractmethod
    async def remove_chunks(self, chunk_ids: list[str]) -> int:
        """Remove chunks from the retrieval index.

        Args:
            chunk_ids: List of chunk IDs to remove

        Returns:
            Number of chunks removed
        """

    @abstractmethod
    async def update_chunk(self, chunk: Chunk) -> bool:
        """Update an existing chunk in the index.

        Args:
            chunk: Updated chunk

        Returns:
            True if successful
        """

    @abstractmethod
    async def get_index_stats(self) -> dict[str, Any]:
        """Get statistics about the retrieval index.

        Returns:
            Index statistics dictionary
        """


class HybridRetriever(ABC):
    """Interface for hybrid retrieval combining multiple strategies."""

    @abstractmethod
    async def retrieve_hybrid(
        self,
        query: str,
        query_embedding: list[float],
        k: int = 10,
        vector_weight: float = 0.7,
        keyword_weight: float = 0.3,
        filters: dict[str, Any] | None = None,
    ) -> list[Passage]:
        """Retrieve using hybrid vector + keyword search.

        Args:
            query: Original query text
            query_embedding: Query embedding vector
            k: Number of passages to retrieve
            vector_weight: Weight for vector similarity scores
            keyword_weight: Weight for keyword match scores
            filters: Optional metadata filters

        Returns:
            List of retrieved passages with combined scores
        """

    @abstractmethod
    async def retrieve_keywords(
        self,
        query: str,
        k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[Passage]:
        """Retrieve using keyword/BM25 search only.

        Args:
            query: Query text
            k: Number of passages to retrieve
            filters: Optional metadata filters

        Returns:
            List of retrieved passages with BM25 scores
        """


class ContextualRetriever(ABC):
    """Interface for context-aware retrieval."""

    @abstractmethod
    async def retrieve_with_context(
        self,
        query: str,
        context: QueryContext,
        k: int = 10,
    ) -> RetrievalResult:
        """Retrieve passages considering user context and history.

        Args:
            query: Query text
            context: Query context including user info and history
            k: Number of passages to retrieve

        Returns:
            Complete retrieval result with context
        """

    @abstractmethod
    async def expand_context(
        self,
        passages: list[Passage],
        expansion_window: int = 1,
    ) -> list[Passage]:
        """Expand retrieved passages with surrounding context.

        Args:
            passages: Initial retrieved passages
            expansion_window: Number of neighboring chunks to include

        Returns:
            Passages with expanded context
        """


class MultiModalRetriever(ABC):
    """Interface for multi-modal retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(text, images, etc.)."""

    @abstractmethod
    async def retrieve_text(
        self,
        query: str,
        k: int = 10,
        modalities: list[str] | None = None,
    ) -> list[Passage]:
        """Retrieve text passages that may reference other modalities.

        Args:
            query: Text query
            k: Number of passages to retrieve
            modalities: Optional modality filters (text, image, audio)

        Returns:
            List of retrieved text passages
        """

    @abstractmethod
    async def retrieve_by_image(
        self,
        image_embedding: list[float],
        k: int = 10,
    ) -> list[Passage]:
        """Retrieve passages using image similarity.

        Args:
            image_embedding: Image embedding vector
            k: Number of passages to retrieve

        Returns:
            List of retrieved passages related to the image
        """


class FilteredRetriever(ABC):
    """Interface for retrieval with advanced filtering."""

    @abstractmethod
    async def retrieve_with_filters(
        self,
        query_embedding: list[float],
        filters: dict[str, Any],
        k: int = 10,
    ) -> list[Passage]:
        """Retrieve with complex metadata filtering.

        Args:
            query_embedding: Query embedding vector
            filters: Complex filter dictionary
            k: Number of passages to retrieve

        Returns:
            Filtered retrieval results
        """

    @abstractmethod
    async def retrieve_by_date_range(
        self,
        query_embedding: list[float],
        start_date: str,
        end_date: str,
        k: int = 10,
    ) -> list[Passage]:
        """Retrieve passages within a date range.

        Args:
            query_embedding: Query embedding vector
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            k: Number of passages to retrieve

        Returns:
            Date-filtered retrieval results
        """

    @abstractmethod
    async def retrieve_by_source(
        self,
        query_embedding: list[float],
        source_ids: list[str],
        k: int = 10,
    ) -> list[Passage]:
        """Retrieve passages from specific sources only.

        Args:
            query_embedding: Query embedding vector
            source_ids: List of allowed source IDs
            k: Number of passages to retrieve

        Returns:
            Source-filtered retrieval results
        """


class RetrieverPool(ABC):
    """Interface for managing multiple retrievers."""

    @abstractmethod
    async def retrieve_from_multiple(
        self,
        query_embedding: list[float],
        retriever_names: list[str],
        k_per_retriever: int = 5,
        merge_strategy: str = "round_robin",
    ) -> list[Passage]:
        """Retrieve from multiple retrievers and merge results.

        Args:
            query_embedding: Query embedding vector
            retriever_names: Names of retrievers to use
            k_per_retriever: Results per retriever
            merge_strategy: How to merge results (round_robin, score_based)

        Returns:
            Merged retrieval results
        """

    @abstractmethod
    async def get_retriever(self, name: str) -> VectorRetriever:
        """Get a specific retriever by name.

        Args:
            name: Retriever name

        Returns:
            Retriever instance

        Raises:
            KeyError: If retriever not found
        """

    @abstractmethod
    async def list_retrievers(self) -> list[str]:
        """List available retriever names.

        Returns:
            List of retriever names
        """


class RetrievalError(Exception):
    """Exception raised when retrieval operations fail."""

    def __init__(
        self,
        message: str,
        retriever_name: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """Initialize retrieval error.

        Args:
            message: Error message
            retriever_name: Optional retriever name that failed
            details: Optional error details
        """
        super().__init__(message)
        self.retriever_name = retriever_name
        self.details = details or {}


class RetrieverFactory(ABC):
    """Factory for creating different types of retrievers."""

    @abstractmethod
    async def create_vector_retriever(
        self,
        index_name: str,
        embedding_dimension: int,
        similarity_metric: str = "cosine",
        **kwargs: Any,
    ) -> VectorRetriever:
        """Create a vector retriever.

        Args:
            index_name: Name for the retrieval index
            embedding_dimension: Dimension of embedding vectors
            similarity_metric: Similarity metric to use
            **kwargs: Additional retriever-specific parameters

        Returns:
            Configured vector retriever
        """

    @abstractmethod
    async def create_hybrid_retriever(
        self,
        vector_retriever: VectorRetriever,
        keyword_index_name: str,
        **kwargs: Any,
    ) -> HybridRetriever:
        """Create a hybrid retriever.

        Args:
            vector_retriever: Vector retriever instance
            keyword_index_name: Name for keyword index
            **kwargs: Additional parameters

        Returns:
            Configured hybrid retriever
        """

    @abstractmethod
    async def create_contextual_retriever(
        self,
        base_retriever: VectorRetriever,
        context_window: int = 3,
        **kwargs: Any,
    ) -> ContextualRetriever:
        """Create a contextual retriever.

        Args:
            base_retriever: Base retriever to wrap
            context_window: Context expansion window
            **kwargs: Additional parameters

        Returns:
            Configured contextual retriever
        """
