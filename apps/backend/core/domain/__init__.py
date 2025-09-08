"""Core domain package"""

# Entities
# Events
from .domain_events import DomainEvent
from .entities.agent import Agent, AgentCapability
from .entities.base import BaseEntity
from .events.agent_events import *
from .value_objects.agent import *
from .value_objects.memory import *

# Value Objects
from .value_objects.user import *

__all__ = [
    # Entities
    "BaseEntity",
    "Agent",
    "AgentCapability",
    # Events
    "DomainEvent",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "autonomy",
    "common",
    "domain_events",
    "events",
    "mixins",
    "shared_value_objects",
    "value_objects",
]

# <<< AUTO-GEN
