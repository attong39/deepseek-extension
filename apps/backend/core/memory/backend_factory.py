from __future__ import annotations

from enum import Enum, auto
from typing import Any, Dict
import logging

from importlib import import_module

    from apps.backend.data.external.pinecone_client import PineconeClient
    from apps.backend.data.external.semantic_backend import SemanticBackend
    from apps.backend.infra.vector_backends.faiss_backend import FAISSBackend
    from apps.backend.infra.vector_backends.pgvector_backend import PGVectorBackend
from apps.backend.core.interfaces.memory_backend import BaseMemoryBackend, MemoryResult
from apps.backend.core.interfaces.memory_backend import MemoryBackend

"""Factory Pattern cho Memory Backends với Type Hints và Enum.
Module này cung cấp:
- BackendType Enum cho type safety
- BackendFactory với pattern matching
- Type-safe backend creation
"""
logger = logging.getLogger(__name__)
class BackendType(Enum):
    """Enum cho memory backend types với type safety."""
    SEMANTIC = auto()
    PGVECTOR = auto()
    PINECONE = auto()
    FAISS = auto()
    SQLITE = auto()
    FAKE = auto()
class BackendFactory:
    """Factory class để tạo memory backends với type safety."""
    @classmethod
    def create(cls, backend_type: BackendType, **kwargs: Any) -> MemoryBackend:
        """Tạo memory backend dựa trên type.
        Args:
            backend_type: Loại backend cần tạo
            **kwargs: Configuration parameters
        Returns:
            MemoryBackend instance
        Raises:
            RuntimeError: Nếu backend không available
            ValueError: Nếu config invalid
        """
        match backend_type:
            case BackendType.SEMANTIC:
                return cls._create_semantic_backend(**kwargs)
            case BackendType.PGVECTOR:
                return cls._create_pgvector_backend(**kwargs)
            case BackendType.PINECONE:
                return cls._create_pinecone_backend(**kwargs)
            case BackendType.FAISS:
                return cls._create_faiss_backend(**kwargs)
            case BackendType.FAKE:
                return cls._create_fake_backend(**kwargs)
            case _:
                raise ValueError(f"Unsupported backend type: {backend_type}")
    @staticmethod
    def _create_semantic_backend(**kwargs: Any) -> MemoryBackend:
        """Tạo semantic search backend."""
        try:
            return SemanticBackend(**kwargs)
        except ImportError:
            raise RuntimeError("Semantic backend not available")
    @staticmethod
    def _create_pgvector_backend(**kwargs: Any) -> MemoryBackend:
        """Tạo PGVector backend với connection pooling."""
        dsn = kwargs.get("dsn")
        if not dsn:
            raise ValueError("DSN required for PGVector backend")
        try:
            return PGVectorBackend(dsn=dsn, **kwargs)
        except ImportError:
            raise RuntimeError("PGVector backend not available")
    @staticmethod
    def _create_pinecone_backend(**kwargs: Any) -> MemoryBackend:
        """Tạo Pinecone backend."""
        api_key = kwargs.get("api_key")
        if not api_key:
            raise ValueError("API key required for Pinecone backend")
        try:
            return PineconeClient(**kwargs)
        except ImportError:
            raise RuntimeError("Pinecone backend not available")
    @staticmethod
    def _create_faiss_backend(**kwargs: Any) -> MemoryBackend:
        """Tạo FAISS backend."""
        try:
            return FAISSBackend(**kwargs)
        except ImportError:
            raise RuntimeError("FAISS backend not available")
    @staticmethod
    def _create_fake_backend(**kwargs: Any) -> MemoryBackend:
        """Tạo fake backend cho testing."""
        class FakeBackend(BaseMemoryBackend):
            """Fake backend implementation cho testing."""
            def upsert(
                self,
                namespace: str,
                records: List[Dict[str, Any]],
                embedding_model: Optional[str] = None,
            ) -> MemoryResult:
                self._validate_namespace(namespace)
                self._validate_records(records)
                return self._create_result(
                    status="success",
                    namespace=namespace,
                    operation="upsert",
                    count=len(records),
                    metadata={"fake": True},
                )
            def query(
                self,
                namespace: str,
                query: str,
                top_k: int = 10,
                filters: Optional[Dict[str, Any]] = None,
            ) -> MemoryResult:
                self._validate_namespace(namespace)
                return self._create_result(
                    status="success",
                    namespace=namespace,
                    operation="query",
                    count=top_k,
                    data={"results": []},
                    metadata={"fake": True},
                )
            def delete(
                self,
                namespace: str,
                ids: list[str] | None = None,
                filters: dict | None = None,
                hard: bool = False,
            ) -> MemoryResult:
                self._validate_namespace(namespace)
                return self._create_result(
                    status="success",
                    namespace=namespace,
                    operation="delete",
                    count=len(ids) if ids else 0,
                    metadata={"fake": True},
                )
            def rebuild_embeddings(
                self, namespace: str, target_model: str, batch_size: int = 256
            ) -> MemoryResult:
                self._validate_namespace(namespace)
                return self._create_result(
                    status="success",
                    namespace=namespace,
                    operation="rebuild",
                    metadata={"fake": True, "target_model": target_model},
                )
        return FakeBackend()
    @classmethod
    def get_available_backends(cls) -> Dict[BackendType, bool]:
        """Kiểm tra available backends.
        Returns:
            Dict mapping backend type to availability status
        """
        availability = {}
        for backend_type in BackendType:
            try:
                if backend_type == BackendType.FAKE:
                    availability[backend_type] = True
                elif backend_type == BackendType.PGVECTOR:
                    import_module("pgvector")
                    availability[backend_type] = True
                elif backend_type == BackendType.PINECONE:
                    import_module("pinecone")
                    availability[backend_type] = True
                else:
                    availability[backend_type] = True
            except ImportError:
                availability[backend_type] = False
            except Exception as e:
                logger.warning(f"Error checking {backend_type}: {e}")
                availability[backend_type] = False
        return availability
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> MemoryBackend:
        """Tạo backend từ configuration dict.
        Args:
            config: Configuration dictionary với 'type' và các parameters khác
        Returns:
            MemoryBackend instance
        Raises:
            ValueError: Nếu config invalid
        """
        backend_type_str = config.get("type", "").upper()
        if not backend_type_str:
            raise ValueError("Backend type must be specified in config")
        try:
            backend_type = BackendType[backend_type_str]
        except KeyError:
            available = [bt.name for bt in BackendType]
            raise ValueError(f"Unknown backend type '{backend_type_str}'. Available: {available}")
        kwargs = {k: v for k, v in config.items() if k != "type"}
        return cls.create(backend_type, **kwargs)
__all__ = [
    "BackendFactory",
    "BackendType",
    "FAISS",
    "FAKE",
    "FakeBackend",
    "PGVECTOR",
    "PINECONE",
    "SEMANTIC",
    "SQLITE",
    "api_key",
    "availability",
    "available",
    "backend_type",
    "backend_type_str",
    "create",
    "create_from_config",
    "delete",
    "dsn",
    "get_available_backends",
    "kwargs",
    "logger",
    "query",
    "rebuild_embeddings",
    "upsert",
]
