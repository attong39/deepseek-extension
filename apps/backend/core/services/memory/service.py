"""Memory service implementation.

Cung cấp vector storage, semantic search, và memory management.
Refactored để sử dụng new service architecture.
"""

from __future__ import annotations

from typing import Any

from apps.backend.core.services._base import BaseService, ServiceContext
from apps.backend.core.services.middleware import instrument, retry
from apps.backend.core.services.types import ServiceResult
import Exception
import ImportError
import bool
import conversation_id
import ctx
import dict
import doc
import e
import float
import hasattr
import int
import kv_store
import len
import list
import metadata
import namespace
import query
import self
import str
import super
import text
import threshold
import top_k
import vector_store


class MemoryService(BaseService):
    """Service cho memory operations với vector storage.

    Hỗ trợ:
    - Vector embedding và storage
    - Semantic search
    - Namespace management
    - Memory lifecycle
    """

    def __init__(
        self,
        ctx: ServiceContext,
        vector_store: Any,  # Vector storage backend
        kv_store: Any | None = None,  # Key-value store for metadata
    ):
        super().__init__(ctx)
        self.vector = vector_store
        self.kv = kv_store

    @instrument(name="memory.init_agent")
    async def init_for_agent(self, agent_id: str) -> ServiceResult[bool]:
        """Initialize memory namespace cho agent."""
        self._log_operation("init_agent", agent_id=agent_id)

        try:
            # Set agent ready flag
            if self.kv:
                await self.kv.set(f"agent:{agent_id}:ready", True)

            # Initialize vector namespace if needed
            if hasattr(self.vector, "init_namespace"):
                await self.vector.init_namespace(agent_id)

            return ServiceResult.success(True)

        except Exception as e:
            self._log_error("init_agent", e, agent_id=agent_id)
            return ServiceResult.failure(str(e), "INIT_ERROR")

    @instrument(name="memory.add")
    @retry(times=3, backoff=0.1)
    async def add_document(
        self,
        namespace: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> ServiceResult[str]:
        """Add document với vector embedding."""
        self._log_operation("add", namespace=namespace, text_len=len(text))

        try:
            doc_id = await self.vector.add(namespace, text, metadata or {})
            return ServiceResult.success(doc_id)

        except Exception as e:
            self._log_error("add", e, namespace=namespace)
            return ServiceResult.failure(str(e), "ADD_ERROR")

    @instrument(name="memory.search")
    async def search(
        self,
        namespace: str,
        query: str,
        top_k: int = 5,
        threshold: float = 0.7,
    ) -> list[dict[str, Any]]:
        """Semantic search trong namespace."""
        self._log_operation("search", namespace=namespace, query=query, top_k=top_k)

        try:
            results = await self.vector.search(namespace, query, top_k=top_k)

            # Filter by threshold nếu có
            if threshold > 0:
                results = [doc for doc in results if doc.get("score", 0) >= threshold]

            return results

        except Exception as e:
            self._log_error("search", e, namespace=namespace)
            return []

    async def retrieve_for_chat(
        self,
        conversation_id: str,
        query: str,
        top_k: int = 6,
    ) -> list[dict[str, Any]]:
        """Retrieve context cho chat conversation."""
        # Map conversation_id to agent_id
        agent_id = None
        if self.kv:
            agent_id = await self.kv.get(f"conv_agent:{conversation_id}")

        if not agent_id:
            # Fallback: use conversation_id as namespace
            agent_id = conversation_id

        return await self.search(agent_id, query, top_k=top_k)

    @instrument(name="memory.delete")
    async def delete_document(self, namespace: str, doc_id: str) -> ServiceResult[bool]:
        """Delete document từ namespace."""
        self._log_operation("delete", namespace=namespace, doc_id=doc_id)

        try:
            if hasattr(self.vector, "delete"):
                await self.vector.delete(namespace, doc_id)
            return ServiceResult.success(True)

        except Exception as e:
            self._log_error("delete", e, namespace=namespace, doc_id=doc_id)
            return ServiceResult.failure(str(e), "DELETE_ERROR")

    async def get_namespace_stats(self, namespace: str) -> dict[str, Any]:
        """Get statistics cho namespace."""
        if hasattr(self.vector, "get_stats"):
            return await self.vector.get_stats(namespace)
        return {"namespace": namespace, "document_count": 0}


# Backward compatibility - import từ _impl nếu cần
try:
    pass

    __all__ = ["MemoryService", "LegacyMemoryService"]
except ImportError:
    __all__ = ["MemoryService"]
