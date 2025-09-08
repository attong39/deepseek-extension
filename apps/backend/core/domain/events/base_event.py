"""
Base Domain Event - ZETA AI Server
Domain-Driven Design (DDD) Compliant
====================================

Compatibility layer - imports từ base.py mới
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Import new composition-based events system
from .base import EVENT_REGISTRY, DomainEvent

# Import event payloads - use TYPE_CHECKING to avoid cycle
if TYPE_CHECKING:
    pass

# Legacy aliases for backward compatibility
# AgentCreatedEvent = AgentCreated
# AgentActivatedEvent = AgentActivated
# MemoryCreatedEvent = MemoryCreated
# PlanCreatedEvent = PlanCreated

__all__ = [
    "DomainEvent",
    "EVENT_REGISTRY",
]
