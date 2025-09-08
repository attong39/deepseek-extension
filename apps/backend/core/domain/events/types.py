"""Event payload types - no inheritance conflicts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import register_event


@register_event("AgentCreated")
@dataclass(frozen=True)
class AgentCreated:
    agent_id: str
    name: str
    tags: list[str] = field(default_factory=list)


@register_event("AgentActivated")
@dataclass(frozen=True)
class AgentActivated:
    agent_id: str
    status: str = "ACTIVE"


@register_event("AgentDeactivated")
@dataclass(frozen=True)
class AgentDeactivated:
    agent_id: str
    status: str = "INACTIVE"


@register_event("MemoryCreated")
@dataclass(frozen=True)
class MemoryCreated:
    memory_id: str
    owner_agent_id: str
    content_length: int = 0


@register_event("MemoryChunked")
@dataclass(frozen=True)
class MemoryChunked:
    tenant_id: str
    namespace: str
    texts: list[str]
    metadatas: list[dict[str, Any]] = field(default_factory=list)


@register_event("PlanCreated")
@dataclass(frozen=True)
class PlanCreated:
    plan_id: str
    owner_agent_id: str
    goal: str
    steps_count: int = 0


@register_event("PlanProposed")
@dataclass(frozen=True)
class PlanProposed:
    plan_id: str
    agent_id: str
    steps: list[dict[str, Any]]
    summary: str | None = None


__all__ = [
    "AgentCreated",
    "AgentActivated",
    "AgentDeactivated",
    "MemoryCreated",
    "MemoryChunked",
    "PlanCreated",
    "PlanProposed",
]
import dict
import int
import list
import str
