"""Storage interfaces.





This module defines abstract interfaces for storage operations


including file storage, blob storage, and data persistence.


"""

from __future__ import annotations

import io
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any
import bool
import bytes
import dict
import float
import int
import list
import str
import tuple


class FileStorageInterface(ABC):
    """Interface for file storage operations."""

    @abstractmethod
    async def save_file(
        self,
        file_data: bytes | io.BytesIO,
        file_path: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Save file to storage.





        Args:


            file_data: File content as bytes or BytesIO.


            file_path: Target file path.


            metadata: Optional file metadata.





        Returns:


            File information including path, size, etc.


        """

    @abstractmethod
    async def get_file(self, file_path: str) -> bytes:
        """Retrieve file content.





        Args:


            file_path: File path to retrieve.





        Returns:


            File content as bytes.


        """

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage.





        Args:


            file_path: File path to delete.





        Returns:


            True if deletion was successful.


        """

    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """Check if file exists.





        Args:


            file_path: File path to check.





        Returns:


            True if file exists.


        """

    @abstractmethod
    async def get_file_info(self, file_path: str) -> dict[str, Any]:
        """Get file metadata and information.





        Args:


            file_path: File path to get info for.





        Returns:


            File information including size, modified time, etc.


        """

    @abstractmethod
    async def list_files(
        self,
        directory: str = "",
        pattern: str | None = None,
        recursive: bool = False,
    ) -> list[dict[str, Any]]:
        """List files in directory.





        Args:


            directory: Directory path to list.


            pattern: Optional filename pattern.


            recursive: Whether to list recursively.





        Returns:


            List of file information dictionaries.


        """


class BlobStorageInterface(ABC):
    """Interface for blob storage operations (e.g., AWS S3, Azure Blob)."""

    @abstractmethod
    async def upload_blob(
        self,
        container: str,
        blob_name: str,
        data: bytes | io.BytesIO,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Upload blob to storage.





        Args:


            container: Container/bucket name.


            blob_name: Blob identifier.


            data: Blob content.


            content_type: MIME content type.


            metadata: Optional metadata.





        Returns:


            Upload result with blob URL and metadata.


        """

    @abstractmethod
    async def download_blob(
        self,
        container: str,
        blob_name: str,
    ) -> bytes:
        """Download blob from storage.





        Args:


            container: Container/bucket name.


            blob_name: Blob identifier.





        Returns:


            Blob content as bytes.


        """

    @abstractmethod
    async def delete_blob(
        self,
        container: str,
        blob_name: str,
    ) -> bool:
        """Delete blob from storage.





        Args:


            container: Container/bucket name.


            blob_name: Blob identifier.





        Returns:


            True if deletion was successful.


        """

    @abstractmethod
    async def blob_exists(
        self,
        container: str,
        blob_name: str,
    ) -> bool:
        """Check if blob exists.





        Args:


            container: Container/bucket name.


            blob_name: Blob identifier.





        Returns:


            True if blob exists.


        """

    @abstractmethod
    async def get_blob_url(
        self,
        container: str,
        blob_name: str,
        expires_in: int | None = None,
    ) -> str:
        """Get blob access URL.





        Args:


            container: Container/bucket name.


            blob_name: Blob identifier.


            expires_in: Optional expiration time in seconds.





        Returns:


            Blob access URL.


        """

    @abstractmethod
    async def list_blobs(
        self,
        container: str,
        prefix: str = "",
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """List blobs in container.





        Args:


            container: Container/bucket name.


            prefix: Optional blob name prefix.


            limit: Optional result limit.





        Returns:


            List of blob information.


        """


class CacheStorageInterface(ABC):
    """Interface for cache storage operations."""

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get value from cache.





        Args:


            key: Cache key.





        Returns:


            Cached value or None if not found.


        """

    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> bool:
        """Set value in cache.





        Args:


            key: Cache key.


            value: Value to cache.


            ttl: Time to live in seconds.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete key from cache.





        Args:


            key: Cache key to delete.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.





        Args:


            key: Cache key to check.





        Returns:


            True if key exists.


        """

    @abstractmethod
    async def clear(self, pattern: str | None = None) -> bool:
        """Clear cache entries.





        Args:


            pattern: Optional key pattern to match.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.





        Returns:


            Cache statistics including hit rate, memory usage, etc.


        """


class DocumentStorageInterface(ABC):
    """Interface for document storage operations."""

    @abstractmethod
    async def create_document(
        self,
        collection: str,
        document: dict[str, Any],
        document_id: str | None = None,
    ) -> str:
        """Create new document.





        Args:


            collection: Collection name.


            document: Document data.


            document_id: Optional document ID.





        Returns:


            Created document ID.


        """

    @abstractmethod
    async def get_document(
        self,
        collection: str,
        document_id: str,
    ) -> dict[str, Any] | None:
        """Get document by ID.





        Args:


            collection: Collection name.


            document_id: Document ID.





        Returns:


            Document data or None if not found.


        """

    @abstractmethod
    async def update_document(
        self,
        collection: str,
        document_id: str,
        updates: dict[str, Any],
    ) -> bool:
        """Update document.





        Args:


            collection: Collection name.


            document_id: Document ID.


            updates: Update data.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def delete_document(
        self,
        collection: str,
        document_id: str,
    ) -> bool:
        """Delete document.





        Args:


            collection: Collection name.


            document_id: Document ID.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def query_documents(
        self,
        collection: str,
        query: dict[str, Any],
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Query documents.





        Args:


            collection: Collection name.


            query: Query criteria.


            limit: Optional result limit.


            offset: Result offset.





        Returns:


            List of matching documents.


        """

    @abstractmethod
    async def count_documents(
        self,
        collection: str,
        query: dict[str, Any] | None = None,
    ) -> int:
        """Count documents matching query.





        Args:


            collection: Collection name.


            query: Optional query criteria.





        Returns:


            Document count.


        """


class VectorStorageInterface(ABC):
    """Interface for vector storage operations."""

    @abstractmethod
    async def add_vectors(
        self,
        vectors: list[tuple[str, list[float], dict[str, Any]]],
        namespace: str = "default",
    ) -> bool:
        """Add vectors to storage.





        Args:


            vectors: List of (id, vector, metadata) tuples.


            namespace: Storage namespace.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def search_vectors(
        self,
        query_vector: list[float],
        top_k: int = 10,
        namespace: str = "default",
        filter_: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for similar vectors.





        Args:


            query_vector: Query vector.


            top_k: Number of results.


            namespace: Storage namespace.


            filter_: Optional metadata filter.





        Returns:


            List of similar vectors with scores.


        """

    @abstractmethod
    async def get_vector(
        self,
        vector_id: str,
        namespace: str = "default",
    ) -> dict[str, Any] | None:
        """Get vector by ID.





        Args:


            vector_id: Vector identifier.


            namespace: Storage namespace.





        Returns:


            Vector data or None if not found.


        """

    @abstractmethod
    async def delete_vectors(
        self,
        vector_ids: list[str],
        namespace: str = "default",
    ) -> bool:
        """Delete vectors by IDs.





        Args:


            vector_ids: List of vector IDs.


            namespace: Storage namespace.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def update_vector_metadata(
        self,
        vector_id: str,
        metadata: dict[str, Any],
        namespace: str = "default",
    ) -> bool:
        """Update vector metadata.





        Args:


            vector_id: Vector identifier.


            metadata: New metadata.


            namespace: Storage namespace.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def get_namespace_stats(self, namespace: str = "default") -> dict[str, Any]:
        """Get namespace statistics.





        Args:


            namespace: Storage namespace.





        Returns:


            Namespace statistics.


        """


class StreamStorageInterface(ABC):
    """Interface for streaming data storage operations."""

    @abstractmethod
    async def create_stream(
        self,
        stream_name: str,
        config: dict[str, Any] | None = None,
    ) -> bool:
        """Create data stream.





        Args:


            stream_name: Stream identifier.


            config: Optional stream configuration.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def write_to_stream(
        self,
        stream_name: str,
        data: dict[str, Any],
        partition_key: str | None = None,
    ) -> str:
        """Write data to stream.





        Args:


            stream_name: Stream identifier.


            data: Data to write.


            partition_key: Optional partition key.





        Returns:


            Record ID or sequence number.


        """

    @abstractmethod
    async def read_from_stream(
        self,
        stream_name: str,
        limit: int = 100,
        start_position: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Read data from stream.





        Args:


            stream_name: Stream identifier.


            limit: Maximum records to read.


            start_position: Optional starting position.





        Yields:


            Stream records.


        """

    @abstractmethod
    async def delete_stream(self, stream_name: str) -> bool:
        """Delete data stream.





        Args:


            stream_name: Stream identifier.





        Returns:


            True if successful.


        """

    @abstractmethod
    async def get_stream_info(self, stream_name: str) -> dict[str, Any]:
        """Get stream information.





        Args:


            stream_name: Stream identifier.





        Returns:


            Stream information and statistics.


        """
