"""
zeta_vn.core.domain.events package.

Core domain events cho ZETA AI System
"""

from __future__ import annotations

# Import từ base module (không phải base_event để tránh cycle)
from .agent_events import AgentActivated, AgentCreated, AgentDeactivated
from .base import DomainEvent, EventMeta, make_event, register_event

__all__ = [
    "DomainEvent",
    "EventMeta",
    "make_event",
    "register_event",
    "AgentCreated",
    "AgentActivated",
    "AgentDeactivated",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "agent_events",
    "base",
    "base_event",
    "chat_events",
    "learning_events",
    "memory_events",
    "rule_events",
    "rule_events_old",
    "system_events",
    "types",
]

# <<< AUTO-GEN
