"""Compatibility shim for legacy imports of AgentService.

Deprecated: use `zeta_vn.core.services.agent.service.AgentService` or the
canonical `zeta_vn.core.services.agent_orchestrator.AgentOrchestratorService`.

This module re-exports the canonical AgentService to consolidate duplicate
implementations and reduce dependency depth.
"""

from __future__ import annotations

from apps.backend.core.services.agent.service import AgentService

__all__ = ["AgentService"]
