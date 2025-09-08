"""Delete (soft) Agent use-case.

Performs soft-delete if supported by repository, aborts related tasks via
TaskRepository and enforces checks for critical jobs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from apps.backend.core.exceptions.business_exceptions import (
import Exception
import actor_id
import agent
import agent_id
import agent_repository
import bool
import dict
import force
import hasattr
import self
import str
import task_repository
    BusinessRuleViolationError,
    EntityNotFoundError,
)

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.agent import AgentRepository
    from apps.backend.core.interfaces.repositories.task import TaskRepository


class DeleteAgentUseCase:
    def __init__(
        self,
        agent_repository: AgentRepository,
        task_repository: TaskRepository | None = None,
    ) -> None:
        self._repo = agent_repository
        self._task_repo = task_repository

    async def execute(
        self, agent_id: UUID, actor_id: UUID, force: bool = False
    ) -> dict:
        _ = await self._repo.get_by_id(agent_id)
        if not agent:
            raise EntityNotFoundError("Agent", str(agent_id))

        # Check for critical jobs via task repository if available
        has_critical = False
        if self._task_repo:
            try:
                has_critical = await self._task_repo.has_critical_jobs(agent_id)
            except Exception:
                # best-effort: assume no critical jobs if repo fails
                has_critical = False

        if has_critical and not force:
            raise BusinessRuleViolationError(
                "delete", "agent has critical running jobs"
            )

        # abort tasks if forced
        if self._task_repo and (force or has_critical):
            try:
                await self._task_repo.abort_by_agent(agent_id)
            except Exception:
                # ignore best-effort
                pass

        # Soft-delete if supported, otherwise call delete
        if hasattr(self._repo, "soft_delete"):
            deleted = await self._repo.soft_delete(agent_id, actor_id)
        else:
            deleted = await self._repo.delete(agent_id)

        # emit event via metadata (repository/analytics may handle this in real impl)
        return {"deleted": bool(deleted)}


DeleteAgent = DeleteAgentUseCase
