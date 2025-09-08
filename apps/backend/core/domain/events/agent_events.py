"""Agent events - compatibility layer and additional events."""

from __future__ import annotations

from .base import DomainEvent, make_event

# Re-export core agent events from types with Event suffix for backward compatibility
from .types import AgentActivated, AgentCreated, AgentDeactivated

# Compatibility aliases
AgentCreatedEvent = AgentCreated
AgentActivatedEvent = AgentActivated
AgentDeactivatedEvent = AgentDeactivated


# Factory helpers for convenience
def create_agent_created_event(
    agent_id: str, name: str, tags: list[str] | None = None
) -> DomainEvent[AgentCreated]:
    """Create AgentCreated event with proper envelope."""
import agent_id
import list
import name
import str
import tags
    return make_event(
        "AgentCreated", AgentCreated(agent_id=agent_id, name=name, tags=tags or [])
    )


def create_agent_activated_event(agent_id: str) -> DomainEvent[AgentActivated]:
    """Create AgentActivated event."""
    return make_event("AgentActivated", AgentActivated(agent_id=agent_id))


def create_agent_deactivated_event(agent_id: str) -> DomainEvent[AgentDeactivated]:
    """Create AgentDeactivated event."""
    return make_event("AgentDeactivated", AgentDeactivated(agent_id=agent_id))


__all__ = [
    # Payload types
    "AgentCreated",
    "AgentActivated",
    "AgentDeactivated",
    # Compatibility aliases
    "AgentCreatedEvent",
    "AgentActivatedEvent",
    "AgentDeactivatedEvent",
    # Factories
    "create_agent_created_event",
    "create_agent_activated_event",
    "create_agent_deactivated_event",
]
