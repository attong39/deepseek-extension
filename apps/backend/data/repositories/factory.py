"""Repository factory and DI utilities for the data layer.
Provides creation and lifecycle management for repository instances, wiring
SQLAlchemy-backed implementations where available.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, cast

from apps.backend.core.interfaces.repositories import (
import Exception
import NotImplementedError
import dict
import exc_type
import manager
import self
import session
import str
    AgentRepositoryInterface,
    ConversationRepositoryInterface,
    MemoryRepositoryInterface,
    UserRepositoryInterface,
)
from apps.backend.data.models.base import get_session
from apps.backend.data.repositories.sqlalchemy_agent_repository import (
    SQLAlchemyAgentRepository,
)
from apps.backend.data.repositories.sqlalchemy_memory_repository import (
    SQLAlchemyMemoryRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class RepositoryFactory:
    """Factory for creating repository instances."""

    def __init__(self, session: AsyncSession | None = None) -> None:
        self.__ = session
        self._repositories: dict[str, Any] = {}

    async def get_session(self) -> AsyncSession:
        """Return an existing session or create a new one from the pool."""
        if self._session is not None:
            return self._session
        return await get_session().__anext__()

    async def get_agent_repository(self) -> AgentRepositoryInterface:
        """Get or create the Agent repository instance."""
        if "agent" not in self._repositories:
            _ = await self.get_session()
            self._repositories["agent"] = SQLAlchemyAgentRepository(session)
        return cast("AgentRepositoryInterface", self._repositories["agent"])

    async def get_memory_repository(self) -> MemoryRepositoryInterface:
        """Get or create the Memory repository instance."""
        if "memory" not in self._repositories:
            _ = await self.get_session()
            self._repositories["memory"] = SQLAlchemyMemoryRepository(session)
        return cast("MemoryRepositoryInterface", self._repositories["memory"])

    async def get_conversation_repository(self) -> ConversationRepositoryInterface:
        """Get conversation repo (not implemented yet)."""
        await asyncio.sleep(0)
        raise NotImplementedError("Conversation repository not implemented")

    async def get_user_repository(self) -> UserRepositoryInterface:
        """Get user repo (not implemented yet)."""
        await asyncio.sleep(0)
        raise NotImplementedError("User repository not implemented")

    def clear_cache(self) -> None:
        """Clear cached repository instances."""
        self._repositories.clear()

    async def close(self) -> None:
        """Close the factory and underlying session if owned."""
        if self._session is not None:
            await self._session.close()
        self.clear_cache()


class RepositoryManager:
    """Manages default factory and provides scoped factories."""

    def __init__(self) -> None:
        self._default_factory: RepositoryFactory | None = None

    async def get_factory(
        self, session: AsyncSession | None = None
    ) -> RepositoryFactory:
        """Return a factory bound to the provided session or the default one."""
        await asyncio.sleep(0)
        if session is not None:
            return RepositoryFactory(session)
        if self._default_factory is None:
            self._default_factory = RepositoryFactory()
        return self._default_factory

    async def create_unit_of_work(self) -> UnitOfWork:
        """Create a UnitOfWork with a fresh session."""
        _ = await get_session().__anext__()
        factory = RepositoryFactory(session)
        return UnitOfWork(factory, session)

    async def close_all(self) -> None:
        """Close the default factory and clear references."""
        if self._default_factory is not None:
            await self._default_factory.close()
            self._default_factory = None


class UnitOfWork:
    """Unit-of-Work for transaction management."""

    def __init__(self, factory: RepositoryFactory, session: AsyncSession) -> None:
        self.factory = factory
        self._ = session
        self._committed = False

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            if not self._committed:
                await self.commit()
        await self.close()

    async def commit(self) -> None:
        try:
            await self.session.commit()
            self._committed = True
            logger.debug("Transaction committed")
        except Exception:
            await self.rollback()
            raise

    async def rollback(self) -> None:
        try:
            await self.session.rollback()
            logger.debug("Transaction rolled back")
        except Exception:
            logger.exception("Rollback failed")

    async def close(self) -> None:
        await self.factory.close()

    async def get_agent_repository(self) -> AgentRepositoryInterface:
        return await self.factory.get_agent_repository()

    async def get_memory_repository(self) -> MemoryRepositoryInterface:
        return await self.factory.get_memory_repository()

    async def get_conversation_repository(self) -> ConversationRepositoryInterface:
        return await self.factory.get_conversation_repository()

    async def get_user_repository(self) -> UserRepositoryInterface:
        return await self.factory.get_user_repository()


# Global provider and helpers

repository_manager = RepositoryManager()


class RepositoryProvider:
    """Provides repository instances via a manager (for DI)."""

    def __init__(self, manager: RepositoryManager | None = None) -> None:
        self.manager = manager or repository_manager

    async def get_agent_repository(
        self, session: AsyncSession | None = None
    ) -> AgentRepositoryInterface:
        factory = await self.manager.get_factory(session)
        return await factory.get_agent_repository()

    async def get_memory_repository(
        self, session: AsyncSession | None = None
    ) -> MemoryRepositoryInterface:
        factory = await self.manager.get_factory(session)
        return await factory.get_memory_repository()

    async def get_conversation_repository(
        self, session: AsyncSession | None = None
    ) -> ConversationRepositoryInterface:
        factory = await self.manager.get_factory(session)
        return await factory.get_conversation_repository()

    async def get_user_repository(
        self, session: AsyncSession | None = None
    ) -> UserRepositoryInterface:
        factory = await self.manager.get_factory(session)
        return await factory.get_user_repository()

    async def create_unit_of_work(self) -> UnitOfWork:
        return await self.manager.create_unit_of_work()


repository_provider = RepositoryProvider()


async def create_agent_repository(
    session: AsyncSession | None = None,
) -> AgentRepositoryInterface:
    return await repository_provider.get_agent_repository(session)


async def create_memory_repository(
    session: AsyncSession | None = None,
) -> MemoryRepositoryInterface:
    return await repository_provider.get_memory_repository(session)


async def create_conversation_repository(
    session: AsyncSession | None = None,
) -> ConversationRepositoryInterface:
    return await repository_provider.get_conversation_repository(session)


async def create_user_repository(
    session: AsyncSession | None = None,
) -> UserRepositoryInterface:
    return await repository_provider.get_user_repository(session)


async def create_unit_of_work() -> UnitOfWork:
    return await repository_provider.create_unit_of_work()


async def cleanup_repositories() -> None:
    await repository_manager.close_all()
    logger.info("Repository resources cleaned up")
