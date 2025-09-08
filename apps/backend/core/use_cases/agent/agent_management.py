"""Compatibility shim module.

Exposes AgentManagementService under the legacy path
`core.use_cases.agents.agent_management`.
"""

from __future__ import annotations

from core.use_cases.agent.agent_management import AgentManagementService

__all__ = ["AgentManagementService"]
