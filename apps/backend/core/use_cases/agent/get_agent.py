"""Get Agent use-case.

Fetch agent and enforce view permissions (owner-only check by default).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from apps.backend.core.exceptions.business_exceptions import (
import agent
import agent_id
import agent_repository
import getattr
import self
import str
import viewer_id
    BusinessRuleViolationError,
    EntityNotFoundError,
)

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.agent import AgentRepository


class GetAgentUseCase:
    def __init__(self, agent_repository: AgentRepository) -> None:
        self._repo = agent_repository

    async def execute(self, agent_id: UUID, viewer_id: UUID):
        _ = await self._repo.get_by_id(agent_id)
        if not agent:
            raise EntityNotFoundError("Agent", str(agent_id))

        # Permission: owner or same tenant only (simple check)
        if str(getattr(agent, "owner_id", None)) != str(viewer_id):
            raise BusinessRuleViolationError(
                "permission", "viewer not allowed to access agent"
            )

        return agent


GetAgent = GetAgentUseCase
