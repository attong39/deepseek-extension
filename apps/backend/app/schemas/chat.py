"""Chat API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.chat import Chat, Message
from pydantic import BaseModel, Field


class ChatCreate(BaseModel):
    """Schema for creating chat."""
import bool
import chat
import classmethod
import cls
import dict
import message
import str

    agent_id: UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MessageCreate(BaseModel):
    """Schema for creating message."""

    role: str = Field(regex=r"^(user|assistant|system)$")
    content: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    """Schema for message response."""

    id: UUID
    chat_id: UUID
    role: str
    content: str
    metadata: dict[str, Any]
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> MessageResponse:
        """Convert from domain entity."""
        return cls(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata,
            created_at=message.created_at,
        )


class ChatResponse(BaseModel):
    """Schema for chat response."""

    id: UUID
    user_id: UUID
    agent_id: UUID | None
    title: str
    is_active: bool
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> ChatResponse:
        """Convert from domain entity."""
        return cls(
            id=chat.id,
            user_id=chat.user_id,
            agent_id=chat.agent_id,
            title=chat.title,
            is_active=chat.is_active,
            metadata=chat.metadata,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )


__all__ = ["ChatCreate", "MessageCreate", "MessageResponse", "ChatResponse"]
