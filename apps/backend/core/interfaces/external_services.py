"""External services interfaces.

This module defines abstract interfaces for external service integrations
that the system depends on. These interfaces provide abstraction layers
for external APIs and services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any
import bool
import dict
import float
import int
import list
import str
import tuple


class OpenAIClientInterface(ABC):
    """Interface for OpenAI client interactions."""

    @abstractmethod
    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        """Generate chat completion.

        Args:
            messages: List of chat messages.
            model: Model name to use.
            temperature: Sampling temperature.
            max_tokens: Maximum tokens to generate.

        Returns:
            Completion response.
        """

    @abstractmethod
    async def generate_embedding(
        self,
        text: str,
        model: str = "text-embedding-ada-002",
    ) -> list[float]:
        """Generate text embedding.

        Args:
            text: Text to embed.
            model: Embedding model name.

        Returns:
            Embedding vector.
        """

    @abstractmethod
    async def stream_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream chat completion.

        Args:
            messages: List of chat messages.
            model: Model name to use.
            temperature: Sampling temperature.

        Yields:
            Completion chunks.
        """


class AnthropicClientInterface(ABC):
    """Interface for Anthropic Claude client interactions."""

    @abstractmethod
    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        """Generate chat completion.

        Args:
            messages: List of chat messages.
            model: Model name to use.
            max_tokens: Maximum tokens to generate.

        Returns:
            Completion response.
        """

    @abstractmethod
    async def stream_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 4096,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream chat completion.

        Args:
            messages: List of chat messages.
            model: Model name to use.
            max_tokens: Maximum tokens to generate.

        Yields:
            Completion chunks.
        """


class PostgreSQLClientInterface(ABC):
    """Interface for PostgreSQL database interactions."""

    @abstractmethod
    async def execute_query(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute SQL query.

        Args:
            query: SQL query string.
            params: Query parameters.

        Returns:
            Query results.
        """

    @abstractmethod
    async def execute_transaction(
        self,
        queries: list[tuple[str, dict[str, Any] | None]],
    ) -> bool:
        """Execute multiple queries in transaction.

        Args:
            queries: List of (query, params) tuples.

        Returns:
            True if transaction succeeded.
        """

    @abstractmethod
    async def get_connection_info(self) -> dict[str, Any]:
        """Get database connection information.

        Returns:
            Connection details.
        """


class RedisClientInterface(ABC):
    """Interface for Redis cache interactions."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Get value by key.

        Args:
            key: Cache key.

        Returns:
            Cached value or None.
        """

    @abstractmethod
    async def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
    ) -> bool:
        """Set key-value pair.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Time to live in seconds.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete key.

        Args:
            key: Cache key to delete.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: Cache key to check.

        Returns:
            True if key exists.
        """


class ElasticsearchClientInterface(ABC):
    """Interface for Elasticsearch interactions."""

    @abstractmethod
    async def index_document(
        self,
        index: str,
        document: dict[str, Any],
        doc_id: str | None = None,
    ) -> dict[str, Any]:
        """Index a document.

        Args:
            index: Index name.
            document: Document to index.
            doc_id: Optional document ID.

        Returns:
            Indexing result.
        """

    @abstractmethod
    async def search_documents(
        self,
        index: str,
        query: dict[str, Any],
        size: int = 10,
        from_: int = 0,
    ) -> dict[str, Any]:
        """Search documents.

        Args:
            index: Index name.
            query: Search query.
            size: Number of results.
            from_: Offset for pagination.

        Returns:
            Search results.
        """

    @abstractmethod
    async def delete_document(
        self,
        index: str,
        doc_id: str,
    ) -> dict[str, Any]:
        """Delete a document.

        Args:
            index: Index name.
            doc_id: Document ID to delete.

        Returns:
            Deletion result.
        """


class PineconeClientInterface(ABC):
    """Interface for Pinecone vector database interactions."""

    @abstractmethod
    async def upsert_vectors(
        self,
        vectors: list[tuple[str, list[float], dict[str, Any]]],
        namespace: str = "",
    ) -> dict[str, Any]:
        """Upsert vectors to index.

        Args:
            vectors: List of (id, vector, metadata) tuples.
            namespace: Optional namespace.

        Returns:
            Upsert result.
        """

    @abstractmethod
    async def query_vectors(
        self,
        vector: list[float],
        top_k: int = 10,
        namespace: str = "",
        filter_: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Query similar vectors.

        Args:
            vector: Query vector.
            top_k: Number of results.
            namespace: Optional namespace.
            filter_: Optional metadata filter.

        Returns:
            Query results.
        """

    @abstractmethod
    async def delete_vectors(
        self,
        ids: list[str],
        namespace: str = "",
    ) -> dict[str, Any]:
        """Delete vectors by IDs.

        Args:
            ids: Vector IDs to delete.
            namespace: Optional namespace.

        Returns:
            Deletion result.
        """


class S3ClientInterface(ABC):
    """Interface for AWS S3 storage interactions."""

    @abstractmethod
    async def upload_file(
        self,
        file_path: str,
        bucket: str,
        key: str,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Upload file to S3.

        Args:
            file_path: Local file path.
            bucket: S3 bucket name.
            key: S3 object key.
            metadata: Optional metadata.

        Returns:
            Upload result.
        """

    @abstractmethod
    async def download_file(
        self,
        bucket: str,
        key: str,
        file_path: str,
    ) -> bool:
        """Download file from S3.

        Args:
            bucket: S3 bucket name.
            key: S3 object key.
            file_path: Local file path.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def delete_file(
        self,
        bucket: str,
        key: str,
    ) -> bool:
        """Delete file from S3.

        Args:
            bucket: S3 bucket name.
            key: S3 object key.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
    ) -> list[dict[str, Any]]:
        """List files in S3 bucket.

        Args:
            bucket: S3 bucket name.
            prefix: Optional key prefix.

        Returns:
            List of file objects.
        """


class HuggingFaceClientInterface(ABC):
    """Interface for Hugging Face model interactions."""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        model: str,
        max_length: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """Generate text using model.

        Args:
            prompt: Input prompt.
            model: Model name or path.
            max_length: Maximum length.
            temperature: Sampling temperature.

        Returns:
            Generated text.
        """

    @abstractmethod
    async def get_embeddings(
        self,
        texts: list[str],
        model: str,
    ) -> list[list[float]]:
        """Get embeddings for texts.

        Args:
            texts: List of input texts.
            model: Model name or path.

        Returns:
            List of embedding vectors.
        """

    @abstractmethod
    async def classify_text(
        self,
        text: str,
        model: str,
        labels: list[str] | None = None,
    ) -> dict[str, float]:
        """Classify text.

        Args:
            text: Input text.
            model: Model name or path.
            labels: Optional label candidates.

        Returns:
            Classification scores.
        """


class MonitoringClientInterface(ABC):
    """Interface for monitoring and observability services."""

    @abstractmethod
    async def send_metric(
        self,
        name: str,
        value: float,
        tags: dict[str, str] | None = None,
        timestamp: float | None = None,
    ) -> bool:
        """Send metric data.

        Args:
            name: Metric name.
            value: Metric value.
            tags: Optional tags.
            timestamp: Optional timestamp.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def send_log(
        self,
        level: str,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """Send log entry.

        Args:
            level: Log level.
            message: Log message.
            context: Optional context data.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def send_trace(
        self,
        trace_id: str,
        span_id: str,
        operation: str,
        duration: float,
        tags: dict[str, str] | None = None,
    ) -> bool:
        """Send trace data.

        Args:
            trace_id: Trace identifier.
            span_id: Span identifier.
            operation: Operation name.
            duration: Operation duration.
            tags: Optional tags.

        Returns:
            True if successful.
        """
