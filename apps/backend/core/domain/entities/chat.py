"""Chat domain entities.

Chat entities theo Clean Architecture principles.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from apps.backend.core.domain.common import DomainModel, Timestamped, Versioned
from pydantic import Field
import dict
import int
import str


class MessageRole(str, Enum):
    """Vai trò của message trong chat."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Loại message."""

    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"


class ChatMessage(DomainModel, Timestamped):
    """Chat message entity."""

    id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    role: MessageRole
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: dict[str, str] = Field(default_factory=dict)
    parent_message_id: UUID | None = None


class SessionStatus(str, Enum):
    """Trạng thái chat session."""

    ACTIVE = "active"
    ENDED = "ended"
    ARCHIVED = "archived"


class ChatSession(DomainModel, Timestamped, Versioned):
    """Chat session entity."""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    title: str | None = None
    status: SessionStatus = SessionStatus.ACTIVE
    agent_id: UUID | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    message_count: int = 0
    last_activity: datetime = Field(default_factory=datetime.utcnow)


__all__ = ["ChatMessage", "ChatSession", "MessageRole", "MessageType", "SessionStatus"]
