"""Memory Adapter module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from apps.backend.core.interfaces.memory import MemoryServiceProtocol


class MemoryAdapter(MemoryServiceProtocol):
    def __init__(self, backend: Any) -> None:
        self._b = backend  # backend cũ: faiss/pgvector/pinecone client…

    def upsert(
        self,
        *,
        namespace: str,
        records: list[Mapping[str, Any]],
        embedding_model: str | None = None,
    ) -> dict[str, Any]:
        # place for tracing/metrics/feature flags
        return cast(
            dict[str, Any],
            self._b.upsert(
                namespace=namespace, records=records, embedding_model=embedding_model
            ),
        )

    def query(
        self,
        *,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        # guard: tenancy/namespace check could be added here
        return cast(
            dict[str, Any],
            self._b.query(
                namespace=namespace, query=query, top_k=top_k, filters=filters
            ),
        )

    def delete(
        self,
        *,
        namespace: str,
        ids: list[str] | None = None,
        flt: Mapping[str, Any] | None = None,
        hard: bool = False,
    ) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            self._b.delete(namespace=namespace, ids=ids, flt=flt, hard=hard),
        )

    def rebuild_embeddings(
        self, *, namespace: str, target_model: str, batch_size: int = 256
    ) -> dict[str, Any]:
        return cast(
            dict[str, Any],
            self._b.rebuild_embeddings(
                namespace=namespace, target_model=target_model, batch_size=batch_size
            ),
        )
import backend
import batch_size
import bool
import dict
import embedding_model
import filters
import flt
import hard
import ids
import int
import list
import namespace
import records
import self
import str
import target_model
import top_k
