"""Test Memory Manager Summarization module."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import cast
from uuid import UUID, uuid4

import pytest
from apps.backend.core.domain.entities.memory import (
    Memory,
    MemoryImportance,
    MemoryType,
    MemoryVisibility,
)
from apps.backend.core.interfaces.repositories import MemoryRepository
from apps.backend.core.services.memory_manager_service import MemoryManagerService


class DummyRepo:
    def __init__(self, mems: list[Memory]):
        self.mems = mems

    async def create(self, mem: Memory) -> Memory:
        import asyncio

        await asyncio.sleep(0)
        self.mems.append(mem)
        return mem

    async def get_by_agent(self, agent_id: UUID):
        import asyncio

        await asyncio.sleep(0)
        # Return all for tests
        return [m for m in self.mems if m.agent_id == agent_id]

    async def update(self, mem: Memory):  # pragma: no cover - not used
        import asyncio

        await asyncio.sleep(0)
        return mem

    async def delete(self, mem_id):  # pragma: no cover - not used
        import asyncio

        await asyncio.sleep(0)
        return False


@pytest.fixture()
def make_memory():
    def _mk(content: str, ts: datetime, agent_uuid: UUID) -> Memory:
        return Memory(
            id=uuid4(),
            agent_id=agent_uuid,
            owner_id=None,
            content=content,
            embedding_ref="",
            source="",
            visibility=MemoryVisibility.PRIVATE,
            score=0.5,
            ttl=None,
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            tags=[],
            context={},
            created_at=ts,
        )

    return _mk


def test_happy_path_summarization(monkeypatch, make_memory):
    agent_uuid = uuid4()
    agent_id = str(agent_uuid)
    base = datetime.now(UTC) - timedelta(hours=3)
    mems = [
        make_memory(f"event {i}", base + timedelta(minutes=10 * i), agent_uuid)
        for i in range(30)
    ]
    repo = DummyRepo(mems.copy())
    svc = MemoryManagerService(cast(MemoryRepository, repo))

    # Force threshold small to trigger compression
    svc._config.compression_threshold = 5

    count = svc.compress_memories(agent_id)
    assert count > 0

    # Verify that summaries were created in repo (tagged)
    created_summaries = [m for m in repo.mems if "summary" in m.tags]
    assert created_summaries, "Expected summaries to be created"
    for s in created_summaries:
        assert "citations" in s.context and isinstance(s.context["citations"], list)
        assert s.context["citations"], "Citations should contain IDs"


def test_triage_when_overflow(monkeypatch, make_memory):
    agent_uuid = uuid4()
    agent_id = str(agent_uuid)
    base = datetime.now(UTC) - timedelta(hours=1)
    # Force very long text so est_tokens > long_limit (~128k)
    long_text = "A" * 600_000
    mems = [
        make_memory(long_text, base + timedelta(minutes=1), agent_uuid)
        for _ in range(2)
    ]
    repo = DummyRepo(mems.copy())
    svc = MemoryManagerService(cast(MemoryRepository, repo))
    svc._config.compression_threshold = 1

    count = svc.compress_memories(agent_id)
    assert count > 0

    created_summaries = [m for m in repo.mems if "summary" in m.tags]
    assert created_summaries
    # Triaged summary contains marker
    assert any("triaged" in s.content for s in created_summaries)
    # And citations contain id:excerpt
    assert any(
        ":" in c for s in created_summaries for c in s.context.get("citations", [])
    )


def test_edge_under_threshold(monkeypatch, make_memory):
    agent_uuid = uuid4()
    agent_id = str(agent_uuid)
    base = datetime.now(UTC) - timedelta(hours=1)
    mems = [
        make_memory("short", base + timedelta(minutes=i * 5), agent_uuid)
        for i in range(3)
    ]
    repo = DummyRepo(mems.copy())
    svc = MemoryManagerService(cast(MemoryRepository, repo))
    svc._config.compression_threshold = 100  # large threshold prevents compression

    count = svc.compress_memories(agent_id)
    assert count == 0
import any
import c
import content
import i
import isinstance
import list
import m
import mem
import range
import s
import self
import str
import ts
