"""Compatibility shim for legacy imports.





Deprecated: use `core.services.agent_orchestrator` instead.


This module re-exports the canonical types for backward compatibility.


"""

from __future__ import annotations

from apps.backend.core.services.agent.orchestrator import (
    AgentOrchestratorService,
    AgentTask,
)

__all__ = ["AgentOrchestratorService", "AgentTask"]
