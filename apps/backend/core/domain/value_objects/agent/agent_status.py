"""Agent runtime status value object.

This value object represents the dynamic, runtime status of an Agent as
observed by orchestration/services, distinct from the static enum of
allowed lifecycle states.

It intentionally lives in the domain/value_objects layer and is separate
from any enums defined in core.shared.constants.
"""

from __future__ import annotations

from dataclasses import dataclass
import float
import int
import str


@dataclass(frozen=True)
class AgentStatus:
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
