from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

from apps.backend.data.services.memory_adapter import MemoryAdapter
import Exception
import RuntimeError
import batch_size
import bool
import d
import deleted
import dict
import embedding_model
import filters
import flt
import hard
import i
import ids
import int
import len
import list
import m
import namespace
import r
import records
import s
import self
import str
import t
import target_model
import top_k

# Import a real backend here (PGVector/FAISS/Pinecone) — keep import optional
try:
    from apps.backend.data.external.pgvector_backend import PGVectorBackend
except Exception:  # pragma: no cover - backend optional in tests
    PGVectorBackend = None

# NOTE: configure backend from env/settings in real deployment
_backend = None
if PGVectorBackend is not None:
    _backend = PGVectorBackend(dsn="postgres://user:pass@localhost/db")


class _Fake:
    def upsert(
        self,
        *,
        namespace: str,
        records: list[Mapping[str, Any]] | None = None,
        embedding_model: str | None = None,
    ) -> dict[str, Any]:
        return {
            "status": "noop",
            "namespace": namespace,
            "count": len(records) if records else 0,
            "model": embedding_model,
        }

    def query(
        self,
        *,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        _ = filters
        return {
            "status": "noop",
            "namespace": namespace,
            "query": query,
            "top_k": top_k,
        }

    def delete(
        self,
        *,
        namespace: str,
        ids: list[str] | None = None,
        flt: Mapping[str, Any] | None = None,
        hard: bool = False,
    ) -> dict[str, Any]:
        _ = flt
        return {
            "status": "noop",
            "namespace": namespace,
            "ids": ids or [],
            "hard": hard,
        }

    def rebuild_embeddings(
        self, *, namespace: str, target_model: str, batch_size: int = 256
    ) -> dict[str, Any]:
        return {
            "status": "noop",
            "namespace": namespace,
            "target_model": target_model,
            "batch_size": batch_size,
        }


def _semantic_shim_from_pipeline() -> Any:
    """Return a small backend object implementing the memory backend methods by delegating to MemoryPipeline.

    The import of `MemoryPipeline` is local to avoid circular imports during module import time.
    """
    from apps.backend.core.services.semantic_memory import MemoryPipeline

    class SemanticBackend:
        def __init__(self) -> None:
            self._pipe = MemoryPipeline()

        def upsert(
            self,
            *,
            namespace: str,
            records: list[Mapping[str, Any]] | None = None,
            embedding_model: str | None = None,
        ) -> dict[str, Any]:
            count = 0
            for r in records or []:
                doc_id = r.get("doc_id") or r.get("id")
                text = r.get("text")
                meta = r.get("metadata") or {}
                if doc_id and text is not None:
                    self._pipe.ingest(doc_id, text, meta)
                    count += 1
            return {"status": "ok", "namespace": namespace, "count": count}

        def query(
            self,
            *,
            namespace: str,
            query: str,
            top_k: int = 10,
            filters: Mapping[str, Any] | None = None,
        ) -> dict[str, Any]:
            # convert Mapping -> dict to satisfy MemoryPipeline typing
            fdict = dict(filters) if filters is not None else None
            raw = self._pipe.retrieve(query, top_k=top_k, filters=fdict)
            items = [
                {"id": d, "score": s, "text": t, "metadata": m} for d, s, t, m in raw
            ]
            return {"status": "ok", "namespace": namespace, "items": items}

        def delete(
            self,
            *,
            namespace: str,
            ids: list[str] | None = None,
            flt: Mapping[str, Any] | None = None,
            hard: bool = False,
        ) -> dict[str, Any]:
            deleted: list[str] = []
            if ids:
                for i in ids:
                    if i in self._pipe._vecs:
                        del self._pipe._vecs[i]
                        self._pipe._texts.pop(i, None)
                        self._pipe._meta.pop(i, None)
                        deleted.append(i)
            return {"status": "ok", "namespace": namespace, "deleted": deleted}

        def rebuild_embeddings(
            self, *, namespace: str, target_model: str, batch_size: int = 256
        ) -> dict[str, Any]:
            return {
                "status": "ok",
                "namespace": namespace,
                "target_model": target_model,
            }

    return SemanticBackend()


_memory_cache: dict[str, Any] = {}


def get_memory_service() -> Any:
    """Return a memory backend object implementing MemoryServiceProtocol.

    Behavior driven by `MEMORY_BACKEND` env var:
    - 'semantic' -> process-local `MemoryPipeline` shim (in-memory)
    - 'pgvector'  -> use PGVectorBackend via `MemoryAdapter` (if available)
    - default     -> fallback noop fake backend
    """
    choice = os.getenv("MEMORY_BACKEND", "auto").lower()
    if choice == "semantic":
        if "semantic" not in _memory_cache:
            _memory_cache["semantic"] = _semantic_shim_from_pipeline()
        return _memory_cache["semantic"]

    if choice == "pgvector" and _backend is not None:
        if "pgvector" not in _memory_cache:
            _memory_cache["pgvector"] = MemoryAdapter(_backend)
        return _memory_cache["pgvector"]

    if choice == "auto":
        if _backend is not None:
            if "pgvector" not in _memory_cache:
                _memory_cache["pgvector"] = MemoryAdapter(_backend)
            return _memory_cache["pgvector"]
        if "fake" not in _memory_cache:
            _memory_cache["fake"] = _Fake()
        return _memory_cache["fake"]

    if "fake" not in _memory_cache:
        _memory_cache["fake"] = _Fake()
    return _memory_cache["fake"]


# --- Semantic pipeline for Sprint 1 (process-local) ---

try:  # pragma: no cover - optional in some builds
    from apps.backend.core.services.semantic_memory import MemoryPipeline
except Exception:  # pragma: no cover
    MemoryPipeline = None  # type: ignore

_semantic_pipeline: MemoryPipeline | None = None


def get_semantic_memory_pipeline() -> MemoryPipeline:
    """Provide a process-local MemoryPipeline for /memory/semantic endpoints.

    Lazy-init so tests and production can opt in without affecting existing DI.
    """
    global _semantic_pipeline
    if _semantic_pipeline is None:
        if MemoryPipeline is None:  # pragma: no cover
            raise RuntimeError("semantic pipeline is unavailable")
        _semantic_pipeline = MemoryPipeline()
    return _semantic_pipeline
