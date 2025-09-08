"""Agent service layer với business logic."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.agent_v2 import Agent, AgentStatus
from apps.backend.core.domain.ports.repositories import NotFoundError
from apps.backend.data.repositories.sql_agent_repository import SqlAgentRepository


class AgentService:
    """Agent business service."""
import agent_id
import capabilities
import configuration
import dict
import int
import limit
import name
import name_query
import new_caps
import offset
import owner_user_id
import repo
import repo_factory
import self
import set
import str
import tags
import tuple
import uow
import uow_factory

    def __init__(self, repo_factory, uow_factory):
        """
        Args:
            repo_factory: (session) -> SqlAgentRepository
            uow_factory: () -> UnitOfWork
        """
        self._repo_factory = repo_factory
        self._uow_factory = uow_factory

    async def create(
        self,
        *,
        owner_user_id: str,
        name: str,
        capabilities: Iterable[str] = (),
        tags: Iterable[str] = (),
        configuration: dict | None = None,
    ) -> Agent:
        """Create new agent với business validation."""
        now = datetime.now(UTC)

        agent = Agent(
            id=uuid4(),
            owner_user_id=owner_user_id,
            name=name,
            capabilities=tuple(capabilities),
            tags=tuple(tags),
            configuration=configuration or {},
            status=AgentStatus.INACTIVE,
            created_at=now,
            updated_at=now,
        )

        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore[attr-defined]
            await repo.insert(agent)
            await uow.commit()
            return agent

    async def activate(self, agent_id: UUID) -> Agent:
        """Activate agent (business rule enforcement)."""
        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore
            fetched = await repo.get(agent_id)
            if not fetched:
                raise NotFoundError(f"Agent {agent_id} not found")

            # Business logic: activate
            activated = fetched.activate()

            # Save với optimistic locking
            saved = await repo.update(activated)
            await uow.commit()
            return saved

    async def add_capabilities(self, agent_id: UUID, new_caps: Iterable[str]) -> Agent:
        """Add capabilities to agent."""
        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore
            fetched = await repo.get(agent_id)
            if not fetched:
                raise NotFoundError(f"Agent {agent_id} not found")

            # Merge capabilities
            all_caps = set(fetched.capabilities) | set(new_caps)
            updated = fetched.with_capabilities(all_caps)

            saved = await repo.update(updated)
            await uow.commit()
            return saved

    async def set_busy(self, agent_id: UUID) -> Agent:
        """Set agent to BUSY status (với validation)."""
        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore
            fetched = await repo.get(agent_id)
            if not fetched:
                raise NotFoundError(f"Agent {agent_id} not found")

            # Business method with validation
            busy_agent = fetched.assign_task()

            saved = await repo.update(busy_agent)
            await uow.commit()
            return saved

    async def list_agents(
        self,
        *,
        owner_user_id: str | None = None,
        name_query: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Agent]:
        """List agents với filtering."""
        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore
            return await repo.list(
                owner_user_id=owner_user_id,
                name_query=name_query,
                limit=limit,
                offset=offset,
            )

    async def get_agent(self, agent_id: UUID) -> Agent:
        """Get single agent by ID."""
        async with self._uow_factory() as uow:
            repo: SqlAgentRepository = self._repo_factory(uow.session)  # type: ignore
            agent = await repo.get(agent_id)
            if not agent:
                raise NotFoundError(f"Agent {agent_id} not found")
            return agent
