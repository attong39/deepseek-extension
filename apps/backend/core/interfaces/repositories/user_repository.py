"""User repository interface"""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.core.domain.entities.user import User


class UserRepositoryInterface(ABC):
    """Interface for user repository"""
import bool
import str

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID"""
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save user"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Delete user"""
        pass
