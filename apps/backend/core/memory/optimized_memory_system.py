from __future__ import annotations

import logging
from typing import Any

from apps.backend.core.memory.backend_factory import BackendFactory, BackendType
from apps.backend.core.memory.cached_memory_service import CachedMemoryService
from apps.backend.core.memory.encrypted_memory_backend import EncryptedMemoryBackend
from apps.backend.core.memory.streaming_memory_handler import StreamingMemoryHandler
from apps.backend.data.services.bulk_memory_adapter import BulkMemoryAdapter
from apps.backend.infra.vector_backends.pgvector_pool_backend import PGVectorPoolBackend
from fastapi import Request
from fastapi.responses import StreamingResponse
import ValueError
import backend_type
import batch_size
import bool
import cache_dir
import db_config
import dict
import embedding_dim
import encryption_key
import filters
import hasattr
import ids
import int
import isinstance
import len
import list
import namespace
import records
import request
import self
import str
import target_model
import top_k
import use_bulk
import use_cache
import use_caching
import use_encryption
import use_streaming

"""Memory System Integration với tất cả optimizations.
Module này tích hợp:
- EncryptedMemoryBackend với Fernet encryption
- CachedMemoryService với diskcache
- StreamingMemoryHandler với FastAPI
- PGVectorPoolBackend với connection pooling
- BulkMemoryAdapter với rate limiting
"""
logger = logging.getLogger(__name__)


class OptimizedMemorySystem:
    """Tích hợp tất cả memory optimizations."""

    def __init__(
        self,
        backend_type: BackendType = BackendType.PGVECTOR,
        use_encryption: bool = True,
        use_caching: bool = True,
        use_streaming: bool = True,
        encryption_key: str | None = None,
        cache_dir: str = "./.cache/memory",
        db_config: dict[str, Any] | None = None,
        embedding_dim: int = 1536,
    ):
        """Initialize optimized memory system.
        Args:
            backend_type: Type of backend to use
            use_encryption: Whether to use encryption
            use_caching: Whether to use caching
            use_streaming: Whether to use streaming
            encryption_key: Encryption key for Fernet
            cache_dir: Cache directory path
            db_config: Database configuration
            embedding_dim: Vector embedding dimension
        """
        self.backend_type = backend_type
        self.use_encryption = use_encryption
        self.use_caching = use_caching
        self.use_streaming = use_streaming
        self.backend = self._create_backend(
            backend_type=backend_type,
            use_encryption=use_encryption,
            encryption_key=encryption_key,
            db_config=db_config,
            embedding_dim=embedding_dim,
        )
        if use_caching:
            self.cached_service = CachedMemoryService(
                backend=self.backend, cache_dir=cache_dir
            )
        else:
            self.cached_service: CachedMemoryService | None = None
        self.bulk_adapter = BulkMemoryAdapter(backend=self.backend)
        if use_streaming:
            self.streaming_handler = StreamingMemoryHandler(backend=self.backend)
        else:
            self.streaming_handler: StreamingMemoryHandler | None = None
        logger.info(
            f"Initialized optimized memory system with backend: {backend_type.value}"
        )

    def _create_backend(
        self,
        backend_type: BackendType,
        use_encryption: bool,
        encryption_key: str | None,
        db_config: dict[str, Any] | None,
        embedding_dim: int,
    ) -> Any:
        """Create appropriate backend based on type."""
        if backend_type == BackendType.PGVECTOR:
            if not db_config:
                raise ValueError("db_config required for PGVector backend")
            dsn = f"postgresql://{db_config.get('user', 'postgres')}:{db_config.get('password', '')}@{db_config.get('host', 'localhost')}:{db_config.get('port', 5432)}/{db_config.get('database', 'zeta_vn')}"
            backend = PGVectorPoolBackend(
                dsn=dsn,
                min_conn=db_config.get("min_pool_size", 5),
                max_conn=db_config.get("max_pool_size", 20),
                embedding_dim=embedding_dim,
            )
        elif backend_type == BackendType.SQLITE:
            if use_encryption:
                backend = EncryptedMemoryBackend(
                    encryption_key=encryption_key,
                    db_path=db_config.get("db_path", ":memory:")
                    if db_config
                    else ":memory:",
                    embedding_dim=embedding_dim,
                )
            else:
                backend = BackendFactory.create(
                    backend_type=backend_type, config={"embedding_dim": embedding_dim}
                )
        else:
            backend = BackendFactory.create(
                backend_type=backend_type, config={"embedding_dim": embedding_dim}
            )
        return backend

    async def upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        use_bulk: bool = True,
        use_cache: bool = True,
    ) -> Any:
        """Upsert records với optimizations.
        Args:
            namespace: Target namespace
            records: Records to upsert
            use_bulk: Whether to use bulk processing
            use_cache: Whether to use caching
        Returns:
            Upsert result
        """
        if use_bulk and len(records) > 10:
            return await self.bulk_adapter.bulk_upsert(namespace, records)
        else:
            if use_cache and self.cached_service:
                return await self.cached_service.upsert(namespace, records)
            else:
                return await self.backend.upsert(namespace, records)

    async def query(
        self,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
        use_cache: bool = True,
    ) -> Any:
        """Query records với optimizations.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters
            use_cache: Whether to use caching
        Returns:
            Query results
        """
        if use_cache and self.cached_service:
            return await self.cached_service.query(namespace, query, top_k, filters)
        else:
            return await self.backend.query(namespace, query, top_k, filters)

    def stream_query_results(
        self,
        namespace: str,
        query: str,
        top_k: int = 1000,
        filters: dict[str, Any] | None = None,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream query results.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Maximum results
            filters: Optional filters
            request: FastAPI request
        Returns:
            Streaming response
        """
        if not self.streaming_handler:
            raise ValueError("Streaming not enabled")
        return self.streaming_handler.stream_query_results(
            namespace, query, top_k, filters, request
        )

    def stream_bulk_upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        batch_size: int = 50,
        request: Request | None = None,
    ) -> StreamingResponse:
        """Stream bulk upsert progress.
        Args:
            namespace: Target namespace
            records: Records to upsert
            batch_size: Batch size
            request: FastAPI request
        Returns:
            Streaming response
        """
        if not self.streaming_handler:
            raise ValueError("Streaming not enabled")
        return self.streaming_handler.stream_bulk_upsert(
            namespace, records, batch_size, request
        )

    async def delete(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> Any:
        """Delete records.
        Args:
            namespace: Target namespace
            ids: Record IDs to delete
            filters: Optional filters
        Returns:
            Delete result
        """
        if self.cached_service:
            await self.cached_service.invalidate_namespace(namespace)
        return await self.backend.delete(namespace, ids, filters)

    async def rebuild_embeddings(self, namespace: str, target_model: str) -> Any:
        """Rebuild embeddings.
        Args:
            namespace: Target namespace
            target_model: Target embedding model
        Returns:
            Rebuild result
        """
        if self.cached_service:
            await self.cached_service.invalidate_namespace(namespace)
        return await self.backend.rebuild_embeddings(namespace, target_model)

    async def get_stats(self) -> dict[str, Any]:
        """Get system statistics.
        Returns:
            Statistics dictionary
        """
        stats = {
            "backend_type": self.backend_type.value,
            "use_encryption": self.use_encryption,
            "use_caching": self.use_caching,
            "use_streaming": self.use_streaming,
        }
        if hasattr(self.backend, "get_stats"):
            backend_stats = await self.backend.get_stats()
            stats.update(backend_stats)
        if self.cached_service:
            cache_stats = await self.cached_service.get_cache_stats()
            stats["cache"] = cache_stats
        return stats

    def get_encryption_key(self) -> str | None:
        """Get encryption key if using encrypted backend.
        Returns:
            Encryption key or None
        """
        if isinstance(self.backend, EncryptedMemoryBackend):
            return self.backend.get_encryption_key()
        return None


__all__ = [
    "OptimizedMemorySystem",
    "backend",
    "backend_stats",
    "cache_stats",
    "dsn",
    "get_encryption_key",
    "logger",
    "stats",
    "stream_bulk_upsert",
    "stream_query_results",
]
