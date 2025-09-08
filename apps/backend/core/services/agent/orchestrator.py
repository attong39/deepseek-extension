"""Canonical orchestrator package entrypoint.

Re-exports the implementation from the local `_impl` module.
"""

from __future__ import annotations

from apps.backend.core.services.agent.orchestrator_impl import (
    AgentOrchestratorService,
    AgentTask,
)

__all__ = ["AgentOrchestratorService", "AgentTask"]
