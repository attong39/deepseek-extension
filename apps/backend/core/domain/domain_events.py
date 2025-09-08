"""Domain events cho Event Sourcing và Outbox pattern."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _now() -> datetime:
    """UTC timestamp hiện tại."""
import aggregate
import aggregate_id
import classmethod
import cls
import data
import dict
import event_type
import int
import list
import payload
import print
import str
import super
import type
    return datetime.now(UTC)


class DomainEvent(BaseModel):
    """Base class cho tất cả domain events."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    aggregate: str
    aggregate_id: str
    occurred_at: datetime = Field(default_factory=_now)
    payload: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def make(
        cls, event_type: str, aggregate: str, aggregate_id: str, **payload: Any
    ) -> DomainEvent:
        """Factory method cho domain events."""
        return cls(
            event_type=event_type,
            aggregate=aggregate,
            aggregate_id=aggregate_id,
            payload=payload or {},
        )


# Specific domain events
class AgentCreated(DomainEvent):
    """Agent created event."""

    agent_id: str
    name: str
    model: str
    tenant_id: str = ""

    def __init__(self, **data: Any) -> None:
        data.setdefault("event_type", "AgentCreated")
        data.setdefault("aggregate", "agent")
        data.setdefault("aggregate_id", data.get("agent_id", ""))
        super().__init__(**data)


class AgentActivated(DomainEvent):
    """Agent activated event."""

    agent_id: str
    status: str

    def __init__(self, **data: Any) -> None:
        data.setdefault("event_type", "AgentActivated")
        data.setdefault("aggregate", "agent")
        data.setdefault("aggregate_id", data.get("agent_id", ""))
        super().__init__(**data)


class MemoryChunked(DomainEvent):
    """Memory chunked và ready for vectorization."""

    memory_id: str
    tenant_id: str
    namespace: str
    texts: list[str]
    metadatas: list[dict[str, Any]]

    def __init__(self, **data: Any) -> None:
        data.setdefault("event_type", "MemoryChunked")
        data.setdefault("aggregate", "memory")
        data.setdefault("aggregate_id", data.get("memory_id", ""))
        super().__init__(**data)


class MemoryIngested(DomainEvent):
    """Memory ingested into vector store."""

    memory_id: str
    chunks_count: int
    model: str
    namespace: str

    def __init__(self, **data: Any) -> None:
        data.setdefault("event_type", "MemoryIngested")
        data.setdefault("aggregate", "memory")
        data.setdefault("aggregate_id", data.get("memory_id", ""))
        super().__init__(**data)


# Event registry for type resolution
EVENT_REGISTRY: dict[str, type[DomainEvent]] = {
    "DomainEvent": DomainEvent,
    "AgentCreated": AgentCreated,
    "AgentActivated": AgentActivated,
    "MemoryChunked": MemoryChunked,
    "MemoryIngested": MemoryIngested,
}


if __name__ == "__main__":
    # Test domain events
    print("🚀 DOMAIN EVENTS TEST")

    # Create base event
    event = DomainEvent(
        event_type="TestEvent",
        aggregate="test",
        aggregate_id="test-123",
        payload={"message": "hello world"},
    )

    print(f"✅ Base event: {event.event_type}")
    print(f"✅ Event ID: {event.id}")
    print(f"✅ Occurred at: {event.occurred_at}")

    # Create specific event
    agent_event = AgentCreated(
        agent_id="agent-456", name="Test Agent", model="gpt-4o-mini"
    )

    print(f"✅ Agent event: {agent_event.event_type}")
    print(f"✅ Agent ID: {agent_event.agent_id}")
    print(f"✅ Agent name: {agent_event.name}")

    print("🎉 DOMAIN EVENTS WORKING!")
