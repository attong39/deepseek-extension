"""Compatibility shim: provide lightweight stubs for historic import paths.

The real implementation lives at
``zeta_vn.core.services.agent.orchestrator``. This module exposes minimal
stub classes (and a historical misspelling alias) so that import-time access
during test collection or static analysis does not trigger circular imports.
These stubs raise if instantiated at runtime to signal callers to import the
concrete implementation when they actually need to run logic.
"""

from __future__ import annotations

from typing import Any
import RuntimeError


class AgentOrchestratorService:  # pragma: no cover - shim
    """Import-time stub for the concrete AgentOrchestratorService.

    Do not instantiate this class at import time. Import the real class from
    ``zeta_vn.core.services.agent.orchestrator`` before creating instances.
    """

    def __init__(self, *_: Any, **__: Any) -> None:
        raise RuntimeError(
            "AgentOrchestratorService is a compatibility stub. "
            "Import the real implementation from 'zeta_vn.core.services.agent.orchestrator' before instantiating."
        )


class AgentTask:  # pragma: no cover - shim
    """Import-time stub for AgentTask objects."""

    def __init__(self, *_: Any, **__: Any) -> None:
        raise RuntimeError(
            "AgentTask is a compatibility stub. Import the real implementation before instantiating."
        )


# Historical misspelling seen in the codebase; provide alias for compatibility.
AgentOrchesttratorService = AgentOrchestratorService

__all__ = ["AgentOrchestratorService", "AgentTask", "AgentOrchesttratorService"]
