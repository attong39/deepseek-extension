"""Chat repository interface.

Repository interface cho chat domain theo Clean Architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.chat import ChatMessage, ChatSession
import bool
import int
import list


class ChatRepository(ABC):
    """Repository interface cho chat operations."""

    @abstractmethod
    async def create_session(self, session: ChatSession) -> ChatSession:
        """Tạo chat session mới."""
        ...

    @abstractmethod
    async def get_session(self, session_id: UUID) -> ChatSession | None:
        """Lấy chat session theo ID."""
        ...

    @abstractmethod
    async def add_message(self, message: ChatMessage) -> ChatMessage:
        """Thêm message vào session."""
        ...

    @abstractmethod
    async def get_messages(
        self, session_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[ChatMessage]:
        """Lấy messages trong session."""
        ...

    @abstractmethod
    async def delete_session(self, session_id: UUID) -> bool:
        """Xóa chat session."""
        ...


__all__ = ["ChatRepository"]
