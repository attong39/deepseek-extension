"""Test Memory Adapter And Usecases module."""

from __future__ import annotations

from apps.backend.core.use_cases.memory.query_memory import QueryMemory
from apps.backend.core.use_cases.memory.rebuild_embeddings import RebuildEmbeddings
from apps.backend.core.use_cases.memory.upsert_memory import UpsertMemory
from apps.backend.data.services.memory_adapter import MemoryAdapter


class FakeBackend:
    def __init__(self) -> None:
        self.calls = []

    def upsert(
        self, *, namespace: str, records: list[dict], embedding_model: str | None = None
    ) -> dict:
        self.calls.append(("upsert", namespace, records, embedding_model))
        return {"status": "ok", "count": len(records)}

    def query(
        self,
        *,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict | None = None,
    ) -> dict:
        self.calls.append(("query", namespace, query, top_k, filters))
        return {"status": "ok", "items": [{"id": "1", "score": 0.9}]}

    def delete(
        self,
        *,
        namespace: str,
        ids: list[str] | None = None,
        flt: dict | None = None,
        hard: bool = False,
    ) -> dict:
        self.calls.append(("delete", namespace, ids, flt, hard))
        return {"status": "ok", "deleted": ids or []}

    def rebuild_embeddings(
        self, *, namespace: str, target_model: str, batch_size: int = 256
    ) -> dict:
        self.calls.append(("rebuild_embeddings", namespace, target_model, batch_size))
        return {"status": "started", "target_model": target_model}


def test_adapter_forwarding_and_usecases():
    backend = FakeBackend()
    adapter = MemoryAdapter(backend)

    # Upsert via use-case
    up = UpsertMemory(adapter)
    res = up(
        {"namespace": "ns1", "records": [{"id": "a", "v": 1}], "embedding_model": "m1"}
    )
    assert res["status"] == "ok"
    assert backend.calls[0][0] == "upsert"

    # Query via use-case
    q = QueryMemory(adapter)
    out = q({"namespace": "ns1", "query": "hello", "top_k": 5})
    assert out["status"] == "ok"
    assert backend.calls[1][0] == "query"

    # Rebuild embeddings via use-case
    r = RebuildEmbeddings(adapter)
    out2 = r({"namespace": "ns1", "target_model": "m2", "batch_size": 128})
    assert out2["status"] == "started"
    assert backend.calls[2][0] == "rebuild_embeddings"


def test_adapter_delete_parameters():
    backend = FakeBackend()
    adapter = MemoryAdapter(backend)
    # call adapter.delete directly
    res = adapter.delete(namespace="nsx", ids=["1", "2"], flt=None, hard=True)
    assert res["status"] == "ok"
    assert backend.calls[-1][0] == "delete"
    assert backend.calls[-1][2] == ["1", "2"]


def test_rebuild_embeddings_defaults():
    backend = FakeBackend()
    adapter = MemoryAdapter(backend)
    res = adapter.rebuild_embeddings(namespace="nsx", target_model="m3")
    assert res["status"] == "started"
    assert backend.calls[-1][2] == "m3"
import batch_size
import bool
import dict
import embedding_model
import filters
import flt
import hard
import ids
import int
import len
import list
import namespace
import records
import self
import str
import target_model
import top_k
