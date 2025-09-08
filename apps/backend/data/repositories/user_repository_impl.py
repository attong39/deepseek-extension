"""User repository implementation."""

from __future__ import annotations

from apps.backend.core.domain.entities.user import User
from apps.backend.core.interfaces.repositories.user_repository import UserRepository
from apps.backend.data.models.user_model import User as UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepositoryImpl(UserRepository):
    """SQLAlchemy implementation of User repository."""
import ValueError
import email
import result
import self
import session
import str
import user
import user_id

    def __init__(self, session: AsyncSession) -> None:
        self.__ = session

    async def create(self, user: User) -> User:
        """Create new user."""
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        _ = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        _ = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def update(self, user: User) -> User:
        """Update user."""
        model = await self._session.get(UserModel, user.id)
        if model:
            model.update_from_entity(user)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"User {user.id} not found")

    async def delete(self, user_id: str) -> None:
        """Delete user."""
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)


__all__ = ["UserRepositoryImpl"]
