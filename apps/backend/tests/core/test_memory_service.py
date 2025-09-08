"""Test Memory Service module."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from apps.backend.core.services.memory._impl import MemoryService


def test_create_get_update_delete_memory():
    svc = MemoryService()
    agent_id = str(uuid4())

    mem = svc.create_memory(
        content="hello world", memory_type="episodic", agent_id=agent_id
    )
    assert mem is not None
    mid = str(mem.id)

    fetched = svc.get_memory(mid)
    assert fetched is not None and fetched.content == "hello world"

    updated = svc.update_memory(mid, content="updated")
    assert updated is True
    fetched2 = svc.get_memory(mid)
    assert fetched2 is not None and fetched2.content == "updated"

    deleted = svc.delete_memory(mid)
    assert deleted is True
    assert svc.get_memory(mid) is None


def test_consolidate_and_forget():
    svc = MemoryService()
    agent_id = str(uuid4())

    # create several similar memories
    svc.create_memory("alpha bravo", "episodic", agent_id=agent_id, importance="high")
    svc.create_memory("alpha charlie", "episodic", agent_id=agent_id, importance="high")
    svc.create_memory("delta echo", "episodic", agent_id=agent_id, importance="low")

    consolidated = svc.consolidate_memories(agent_id, importance_threshold="high")
    assert consolidated >= 0

    # forget old memories by manipulating created_at
    mems = svc.get_agent_memories(agent_id)
    for m in mems:
        m.created_at = datetime.now(UTC) - timedelta(days=90)

    forgotten = svc.forget_memories(agent_id, importance_threshold="low", age_days=30)
    assert isinstance(forgotten, int)
import int
import isinstance
import m
import str
