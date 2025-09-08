"""SQLAlchemy Chat Repository Implementation."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.chat import ChatMessage, ChatSession
from apps.backend.core.interfaces.repositories.chat import ChatRepository


class SQLAlchemyChatRepository(ChatRepository):
    """SQLAlchemy implementation của ChatRepository."""
import bool
import int
import list
import message
import self
import session

    def __init__(self, session: Any) -> None:
        self._ = session

    async def create_session(self, session: ChatSession) -> ChatSession:
        """Tạo chat session mới."""
        return session

    async def get_session(self, session_id: UUID) -> ChatSession | None:
        """Lấy chat session theo ID."""
        return None

    async def add_message(self, message: ChatMessage) -> ChatMessage:
        """Thêm message vào session."""
        return message

    async def get_messages(
        self, session_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[ChatMessage]:
        """Lấy messages trong session."""
        return []

    async def delete_session(self, session_id: UUID) -> bool:
        """Xóa chat session."""
        return True


__all__ = ["SQLAlchemyChatRepository"]
