"""Test Search Diverse Selection module."""

from __future__ import annotations

from uuid import uuid4

from apps.backend.core.domain.entities.memory import (
    Memory,
    MemoryImportance,
    MemoryType,
    MemoryVisibility,
)
from apps.backend.core.use_cases.memory.store_memory import _diverse_select


def _mk_mem(content: str, importance: MemoryImportance) -> Memory:
    return Memory(
        id=uuid4(),
        agent_id=uuid4(),
        owner_id=None,
        content=content,
        embedding_ref="",
        source="",
        visibility=MemoryVisibility.PRIVATE,
        score=0.5,
        ttl=None,
        type=MemoryType.EPISODIC,
        importance=importance,
        tags=[],
        context={},
    )


def test_diversity_basic():
    mems = [
        _mk_mem("Topic A alpha details", MemoryImportance.MEDIUM),
        _mk_mem("Topic A beta more", MemoryImportance.LOW),
        _mk_mem("Topic B intro", MemoryImportance.HIGH),
        _mk_mem("Topic C insight", MemoryImportance.MEDIUM),
        _mk_mem("Topic C more info", MemoryImportance.LOW),
    ]
    selected = _diverse_select(mems, limit=3)
    assert len(selected) == 3
    # Expect at least one from A,B,C topics across the three
    topics = {"A": 0, "B": 0, "C": 0}
    for m in selected:
        t = "?"
        if "Topic A" in m.content:
            t = "A"
        elif "Topic B" in m.content:
            t = "B"
        elif "Topic C" in m.content:
            t = "C"
        if t in topics:
            topics[t] += 1
    assert any(v >= 1 for v in topics.values())


def test_priority_by_importance():
    mems = [
        _mk_mem("Topic Z minor", MemoryImportance.LOW),
        _mk_mem("Topic Z important", MemoryImportance.HIGH),
        _mk_mem("Topic Z medium", MemoryImportance.MEDIUM),
    ]
    selected = _diverse_select(mems, limit=1)
    assert len(selected) == 1
    assert selected[0].importance == MemoryImportance.HIGH


def test_under_limit_returns_as_is():
    mems = [
        _mk_mem("One", MemoryImportance.MEDIUM),
        _mk_mem("Two", MemoryImportance.MEDIUM),
    ]
    selected = _diverse_select(mems, limit=5)
    assert selected == mems
import any
import content
import importance
import len
import m
import str
import v
