"""Embedding interfaces for RAG pipeline.

Defines abstract interfaces for text embedding without vendor lock-in.
Implementations will be provided in data layer adapters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.backend.core.services.ai.rag.types import Chunk
import Exception
import bool
import details
import dict
import float
import int
import list
import message
import property
import self
import str
import super


class EmbeddingModel(ABC):
    """Abstract interface for text embedding models."""

    @abstractmethod
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            EmbeddingError: If embedding generation fails
        """

    @abstractmethod
    async def embed_query(self, query: str) -> list[float]:
        """Generate embedding for a single query.

        Args:
            query: Query text to embed

        Returns:
            Query embedding vector

        Raises:
            EmbeddingError: If embedding generation fails
        """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the model name/identifier."""

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """Get the embedding vector dimension."""

    @property
    @abstractmethod
    def max_sequence_length(self) -> int:
        """Get maximum supported sequence length."""


class BatchEmbedder(ABC):
    """Interface for efficient batch embedding processing."""

    @abstractmethod
    async def embed_chunks_batch(
        self,
        chunks: list[Chunk],
        batch_size: int = 32,
    ) -> list[Chunk]:
        """Embed multiple chunks in batches.

        Args:
            chunks: List of chunks to embed
            batch_size: Number of chunks per batch
            show_progress: Whether to show progress indicator

        Returns:
            Chunks with embeddings populated

        Raises:
            EmbeddingError: If batch embedding fails
        """

    @abstractmethod
    async def estimate_cost(
        self,
        texts: list[str],
        model_name: str | None = None,
    ) -> dict[str, Any]:
        """Estimate embedding cost for given texts.

        Args:
            texts: Texts to estimate cost for
            model_name: Optional specific model name

        Returns:
            Cost estimation details
        """


class EmbeddingCache(ABC):
    """Interface for caching embeddings to avoid recomputation."""

    @abstractmethod
    async def get_embedding(self, text_hash: str) -> list[float] | None:
        """Get cached embedding by text hash.

        Args:
            text_hash: Hash of the text

        Returns:
            Cached embedding vector or None if not found
        """

    @abstractmethod
    async def set_embedding(
        self,
        text_hash: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Cache an embedding.

        Args:
            text_hash: Hash of the text
            embedding: Embedding vector to cache
            metadata: Optional metadata about the embedding
        """

    @abstractmethod
    async def get_embeddings_batch(
        self, text_hashes: list[str]
    ) -> dict[str, list[float]]:
        """Get multiple cached embeddings.

        Args:
            text_hashes: List of text hashes

        Returns:
            Dictionary mapping hashes to embedding vectors
        """

    @abstractmethod
    async def set_embeddings_batch(
        self,
        embeddings: dict[str, list[float]],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Cache multiple embeddings.

        Args:
            embeddings: Dictionary mapping text hashes to embeddings
            metadata: Optional metadata about the embeddings
        """

    @abstractmethod
    async def clear_cache(self, pattern: str | None = None) -> int:
        """Clear cached embeddings.

        Args:
            pattern: Optional pattern to match for selective clearing

        Returns:
            Number of embeddings cleared
        """


class SimilarityCalculator(ABC):
    """Interface for calculating similarity between embeddings."""

    @abstractmethod
    def calculate_similarity(
        self,
        query_embedding: list[float],
        document_embeddings: list[list[float]],
    ) -> list[float]:
        """Calculate similarity scores between query and documents.

        Args:
            query_embedding: Query embedding vector
            document_embeddings: List of document embedding vectors

        Returns:
            List of similarity scores
        """

    @abstractmethod
    def calculate_pairwise_similarity(
        self,
        embeddings1: list[list[float]],
        embeddings2: list[list[float]],
    ) -> list[list[float]]:
        """Calculate pairwise similarity matrix.

        Args:
            embeddings1: First set of embeddings
            embeddings2: Second set of embeddings

        Returns:
            2D similarity matrix
        """

    @property
    @abstractmethod
    def metric_name(self) -> str:
        """Get the similarity metric name."""


class EmbeddingError(Exception):
    """Exception raised when embedding operations fail."""

    def __init__(
        self,
        message: str,
        model_name: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        """Initialize embedding error.

        Args:
            message: Error message
            model_name: Optional model name that failed
            details: Optional error details
        """
        super().__init__(message)
        self.model_name = model_name
        self.details = details or {}


class EmbeddingProvider(ABC):
    """High-level interface combining embedding model and caching."""

    @abstractmethod
    async def embed_and_cache(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Embed texts with caching support.

        Args:
            texts: Texts to embed
            cache_key_prefix: Optional prefix for cache keys
            force_refresh: Whether to bypass cache and regenerate

        Returns:
            List of embedding vectors
        """

    @abstractmethod
    async def embed_chunks(
        self,
        chunks: list[Chunk],
        update_in_place: bool = True,
    ) -> list[Chunk]:
        """Embed text chunks with caching.

        Args:
            chunks: Chunks to embed
            update_in_place: Whether to update chunk objects in place

        Returns:
            Chunks with embeddings populated
        """

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        """Get information about the embedding model.

        Returns:
            Model information dictionary
        """

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """Check if embedding service is healthy.

        Returns:
            Health status information
        """
