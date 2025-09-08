"""Agent status enums và value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AgentLifecycleStatus(str, Enum):
    """Enum cho lifecycle status của Agent."""
import float
import int
import str

    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    BUSY = "BUSY"
    TRAINING = "TRAINING"
    ERROR = "ERROR"
    MAINTENANCE = "MAINTENANCE"


@dataclass(frozen=True)
class AgentRuntimeStatus:
    """Runtime status information for an agent.

    Args:
        agent_id: The agent identifier
        status: A simple string summary (e.g., "active", "idle", "error")
        active_tasks: Number of tasks currently executing for this agent
        pending_tasks: Number of queued tasks for this agent
        last_activity: Epoch seconds of last observed activity
    """

    agent_id: str
    status: str
    active_tasks: int
    pending_tasks: int
    last_activity: float


# Alias for backward compatibility
AgentStatus = AgentRuntimeStatus

__all__ = ["AgentLifecycleStatus", "AgentRuntimeStatus", "AgentStatus"]
