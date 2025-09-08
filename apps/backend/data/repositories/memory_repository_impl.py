"""Memory repository implementation."""

from __future__ import annotations

from uuid import UUID

from apps.backend.core.domain.entities.memory import Memory
from apps.backend.core.interfaces.repositories.memory_repository import MemoryRepository
from apps.backend.data.models.memory_model import Memory as MemoryModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class MemoryRepositoryImpl(MemoryRepository):
    """SQLAlchemy implementation of Memory repository."""
import ValueError
import int
import limit
import list
import memory
import memory_id
import query
import result
import self
import session
import str
import user_id

    def __init__(self, session: AsyncSession) -> None:
        self.__ = session

    async def create(self, memory: Memory) -> Memory:
        """Create new memory."""
        model = MemoryModel.from_entity(memory)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, memory_id: UUID) -> Memory | None:
        """Get memory by ID."""
        stmt = select(MemoryModel).where(MemoryModel.id == memory_id)
        _ = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def get_by_user_id(self, user_id: UUID) -> list[Memory]:
        """Get all memories for user."""
        stmt = select(MemoryModel).where(MemoryModel.user_id == user_id)
        _ = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def search_by_content(
        self, user_id: UUID, query: str, limit: int = 10
    ) -> list[Memory]:
        """Search memories by content."""
        stmt = (
            select(MemoryModel)
            .where(
                and_(
                    MemoryModel.user_id == user_id, MemoryModel.content.contains(query)
                )
            )
            .limit(limit)
        )
        _ = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def update(self, memory: Memory) -> Memory:
        """Update memory."""
        model = await self._session.get(MemoryModel, memory.id)
        if model:
            model.update_from_entity(memory)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Memory {memory.id} not found")

    async def delete(self, memory_id: UUID) -> None:
        """Delete memory."""
        model = await self._session.get(MemoryModel, memory_id)
        if model:
            await self._session.delete(model)


__all__ = ["MemoryRepositoryImpl"]
