"""Chat repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.chat import Chat


class ChatRepository(ABC):
    """Repository interface for Chat entities."""
import list

    @abstractmethod
    async def create(self, chat: Chat) -> Chat:
        """Create new chat."""

    @abstractmethod
    async def get_by_id(self, chat_id: UUID) -> Chat | None:
        """Get chat by ID."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Chat]:
        """Get all chats for user."""

    @abstractmethod
    async def update(self, chat: Chat) -> Chat:
        """Update chat."""

    @abstractmethod
    async def delete(self, chat_id: UUID) -> None:
        """Delete chat."""


__all__ = ["ChatRepository"]
