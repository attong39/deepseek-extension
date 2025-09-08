from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any

from apps.backend.core.interfaces.memory_backend import MemoryBackend
from apps.backend.core.memory.backend_factory import BackendFactory, BackendType
from apps.backend.core.memory.cached_memory_service import CachedMemoryService
from apps.backend.core.memory.encrypted_memory_backend import EncryptedMemoryBackend
from apps.backend.core.memory.optimized_memory_system import OptimizedMemorySystem
from apps.backend.core.memory.streaming_memory_handler import StreamingMemoryHandler
from apps.backend.data.services.bulk_memory_adapter import BulkMemoryAdapter
from apps.backend.infra.vector_backends.pgvector_pool_backend import PGVectorPoolBackend
import bool
import classmethod
import cls
import dep
import dict
import int
import len
import self
import str
import sum
import valid

"""Dependency Injection Container cho Memory System với Ports & Adapters.
Module này cung cấp:
- Container class với type-safe dependency injection
- Factory methods cho architectural components
- Environment-based configuration
- Health monitoring và validation
"""
logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Container:
    """DI Container cho memory system dependencies với type safety."""

    backend: MemoryBackend | None = None
    cached_service: CachedMemoryService | None = None
    bulk_adapter: BulkMemoryAdapter | None = None
    streaming_handler: StreamingMemoryHandler | None = None
    optimized_system: OptimizedMemorySystem | None = None
    backend_type: BackendType = BackendType.PGVECTOR
    use_encryption: bool = True
    use_caching: bool = True
    use_streaming: bool = True
    embedding_dim: int = 1536
    encryption_key: str | None = field(
        default_factory=lambda: os.getenv("ZETA_ENCRYPTION_KEY")
    )
    cache_dir: str = field(
        default_factory=lambda: os.getenv("ZETA_CACHE_DIR", "./.cache/memory")
    )
    db_host: str = field(default_factory=lambda: os.getenv("ZETA_DB_HOST", "localhost"))
    db_port: int = field(default_factory=lambda: int(os.getenv("ZETA_DB_PORT", "5432")))
    db_name: str = field(default_factory=lambda: os.getenv("ZETA_DB_NAME", "zeta_vn"))
    db_user: str = field(default_factory=lambda: os.getenv("ZETA_DB_USER", "postgres"))
    db_password: str = field(default_factory=lambda: os.getenv("ZETA_DB_PASSWORD", ""))

    def validate_dependencies(self) -> dict[str, bool]:
        """Validate required dependencies are initialized.
        Returns:
            Dict mapping dependency names to validation status
        """
        validations = {
            "backend": self.backend is not None,
            "cached_service": self.cached_service is not None
            if self.use_caching
            else True,
            "bulk_adapter": self.bulk_adapter is not None,
            "streaming_handler": self.streaming_handler is not None
            if self.use_streaming
            else True,
            "optimized_system": self.optimized_system is not None,
        }
        failed_deps = [dep for dep, valid in validations.items() if not valid]
        if failed_deps:
            logger.warning(f"Dependencies validation failed: {failed_deps}")
        return validations

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status.
        Returns:
            System health and configuration status
        """
        validations = self.validate_dependencies()
        health_score = sum(validations.values()) / len(validations) * 100
        return {
            "health_score": health_score,
            "dependencies": validations,
            "configuration": {
                "backend_type": self.backend_type.value,
                "use_encryption": self.use_encryption,
                "use_caching": self.use_caching,
                "use_streaming": self.use_streaming,
                "embedding_dim": self.embedding_dim,
            },
            "cache_dir": self.cache_dir,
            "database": {
                "host": self.db_host,
                "port": self.db_port,
                "name": self.db_name,
                "user": self.db_user,
            },
        }

    def get_memory_backend(self) -> MemoryBackend:
        """Factory method để tạo memory backend.
        Returns:
            Configured MemoryBackend instance
        """
        if self.backend is None:
            if self.backend_type == BackendType.PGVECTOR:
                self.backend = self._create_pgvector_backend()
            elif self.backend_type == BackendType.SEMANTIC:
                self.backend = self._create_semantic_backend()
            else:
                self.backend = self._create_encrypted_backend()
        return self.backend

    def get_cached_service(self) -> CachedMemoryService:
        """Factory method để tạo cached memory service.
        Returns:
            Configured CachedMemoryService instance
        """
        if self.cached_service is None:
            backend = self.get_memory_backend()
            self.cached_service = CachedMemoryService(
                backend=backend,
                cache_dir=self.cache_dir,
                max_concurrent=int(os.getenv("ZETA_CACHE_MAX_CONCURRENT", "10")),
                cache_ttl=int(os.getenv("ZETA_CACHE_TTL", "3600")),
            )
        return self.cached_service

    def get_bulk_adapter(self) -> BulkMemoryAdapter:
        """Factory method để tạo bulk memory adapter.
        Returns:
            Configured BulkMemoryAdapter instance
        """
        if self.bulk_adapter is None:
            backend = self.get_memory_backend()
            self.bulk_adapter = BulkMemoryAdapter(
                backend=backend,
                batch_size=int(os.getenv("ZETA_BATCH_SIZE", "500")),
                max_workers=int(os.getenv("ZETA_MAX_WORKERS", "8")),
            )
        return self.bulk_adapter

    def get_streaming_handler(self) -> StreamingMemoryHandler:
        """Factory method để tạo streaming memory handler.
        Returns:
            Configured StreamingMemoryHandler instance
        """
        if self.streaming_handler is None:
            backend = self.get_memory_backend()
            self.streaming_handler = StreamingMemoryHandler(
                backend=backend,
                chunk_size=int(os.getenv("ZETA_STREAM_CHUNK_SIZE", "100")),
            )
        return self.streaming_handler

    def get_optimized_system(self) -> OptimizedMemorySystem:
        """Factory method để tạo optimized memory system.
        Returns:
            Configured OptimizedMemorySystem instance
        """
        if self.optimized_system is None:
            db_config = {
                "host": self.db_host,
                "port": self.db_port,
                "database": self.db_name,
                "user": self.db_user,
                "password": self.db_password,
            }
            self.optimized_system = OptimizedMemorySystem(
                backend_type=self.backend_type,
                use_encryption=self.use_encryption,
                use_caching=self.use_caching,
                use_streaming=self.use_streaming,
                encryption_key=self.encryption_key,
                cache_dir=self.cache_dir,
                db_config=db_config,
                embedding_dim=self.embedding_dim,
            )
        return self.optimized_system

    def _create_pgvector_backend(self) -> MemoryBackend:
        """Create PGVector backend với connection pooling."""
        dsn = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return PGVectorPoolBackend(
            dsn=dsn,
            min_conn=int(os.getenv("ZETA_DB_MIN_CONN", "2")),
            max_conn=int(os.getenv("ZETA_DB_MAX_CONN", "20")),
            embedding_dim=self.embedding_dim,
        )

    def _create_semantic_backend(self) -> MemoryBackend:
        """Create semantic search backend."""
        return BackendFactory.create(
            BackendType.SEMANTIC,
            embedding_dim=self.embedding_dim,
        )

    def _create_encrypted_backend(self) -> MemoryBackend:
        """Create encrypted memory backend."""
        return EncryptedMemoryBackend(
            encryption_key=self.encryption_key,
            embedding_dim=self.embedding_dim,
        )

    @classmethod
    def from_env(cls) -> Container:
        """Create container từ environment variables.
        Returns:
            Configured Container instance
        """
        backend_type_str = os.getenv("ZETA_BACKEND_TYPE", "PGVECTOR").upper()
        backend_type = BackendType[backend_type_str]
        return cls(
            backend_type=backend_type,
            use_encryption=os.getenv("ZETA_USE_ENCRYPTION", "true").lower() == "true",
            use_caching=os.getenv("ZETA_USE_CACHING", "true").lower() == "true",
            use_streaming=os.getenv("ZETA_USE_STREAMING", "true").lower() == "true",
            embedding_dim=int(os.getenv("ZETA_EMBEDDING_DIM", "1536")),
        )


container = Container.from_env()


def get_memory_system() -> OptimizedMemorySystem:
    """Dependency injection cho FastAPI - get optimized memory system.
    Returns:
        OptimizedMemorySystem instance
    """
    return container.get_optimized_system()


def get_memory_backend() -> MemoryBackend:
    """Dependency injection cho FastAPI - get memory backend.
    Returns:
        MemoryBackend instance
    """
    return container.get_memory_backend()


def get_cached_service() -> CachedMemoryService:
    """Dependency injection cho FastAPI - get cached service.
    Returns:
        CachedMemoryService instance
    """
    return container.get_cached_service()


def get_bulk_adapter() -> BulkMemoryAdapter:
    """Dependency injection cho FastAPI - get bulk adapter.
    Returns:
        BulkMemoryAdapter instance
    """
    return container.get_bulk_adapter()


def get_streaming_handler() -> StreamingMemoryHandler:
    """Dependency injection cho FastAPI - get streaming handler.
    Returns:
        StreamingMemoryHandler instance
    """
    return container.get_streaming_handler()


__all__ = [
    "Container",
    "backend",
    "backend_type",
    "backend_type_str",
    "container",
    "db_config",
    "dsn",
    "failed_deps",
    "from_env",
    "get_bulk_adapter",
    "get_cached_service",
    "get_memory_backend",
    "get_memory_system",
    "get_optimized_system",
    "get_streaming_handler",
    "get_system_status",
    "health_score",
    "logger",
    "validate_dependencies",
    "validations",
]
