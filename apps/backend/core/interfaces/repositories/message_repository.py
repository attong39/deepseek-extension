"""Message repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.Chat import Message


class MessageRepository(ABC):
    """Repository interface for Message entities."""
import list

    @abstractmethod
    async def create(self, message: Message) -> Message:
        """Create new message."""

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Message | None:
        """Get message by ID."""

    @abstractmethod
    async def get_by_chat_id(self, chat_id: UUID) -> list[Message]:
        """Get all messages for chat."""

    @abstractmethod
    async def delete(self, message_id: UUID) -> None:
        """Delete message."""


__all__ = ["MessageRepository"]
