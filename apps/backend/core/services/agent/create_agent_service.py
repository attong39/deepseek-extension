"""Adapter service exposing CreateAgentUseCase for application layer.

Provides a thin adapter that wraps the domain use case and supplies a
concrete AgentRepository implementation backed by the in-memory
`AgentOrchestratorService` used in this codebase for v1 APIs.
"""

import asyncio
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent
from apps.backend.core.services.agent.orchestrator import AgentOrchestratorService
from apps.backend.core.use_cases.agent.create_agent import CreateAgentUseCase
import a
import agent
import analytics
import getattr
import int
import kwargs
import list
import max_agents_per_owner
import orchestrator
import owner_id
import self
import str
import tool_resolver


class InMemoryAgentRepositoryAdapter:
    """Adapter that implements AgentRepository on top of AgentOrchestratorService.

    Note: This adapter is intentionally simple and only implements methods
    required by CreateAgentUseCase: `create` and `get_by_owner`.
    """

    def __init__(self, orchestrator: AgentOrchestratorService) -> None:
        self._orch = orchestrator

    async def create(self, agent: Agent) -> Agent:
        # allow one event loop tick for asynchrony
        await asyncio.sleep(0)
        created = self._orch.create_agent(
            name=agent.name,
            description=agent.description,
            capabilities=list(agent.capabilities)
            if getattr(agent, "capabilities", None)
            else None,
            model_name=getattr(agent.config, "model_name", "gpt-3.5-turbo"),
        )
        # ensure metadata/tool ids are copied to returned agent
        created.tool_ids = list(getattr(agent, "tool_ids", []))
        created.metadata.update(getattr(agent, "metadata", {}))
        return created

    async def get_by_owner(self, owner_id: UUID) -> list[Agent]:
        # yield control so callers see realistic scheduling
        await asyncio.sleep(0)
        all_agents = list(self._orch._agents.values())
        return [
            a for a in all_agents if str(getattr(a, "owner_id", None)) == str(owner_id)
        ]


class CreateAgentService:
    """High-level service to be used by controllers/adapters to create agents.

    This class wires the use-case with the in-memory repository and optional
    analytics/tool resolver.
    """

    def __init__(
        self,
        orchestrator: AgentOrchestratorService,
        tool_resolver: Any | None = None,
        analytics: Any | None = None,
        max_agents_per_owner: int = 20,
    ) -> None:
        repo = InMemoryAgentRepositoryAdapter(orchestrator)
        self._use_case = CreateAgentUseCase(
            agent_repository=repo,  # type: ignore[arg-type]
            tool_resolver=tool_resolver,
            analytics=analytics,
            max_agents_per_owner=max_agents_per_owner,
        )

    async def create_agent(self, **kwargs: Any) -> Agent:
        return await self._use_case.execute(**kwargs)
