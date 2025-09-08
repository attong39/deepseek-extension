"""Message SQLAlchemy model."""

from __future__ import annotations

from datetime import datetime

from apps.backend.core.domain.entities.chat import Message
from apps.backend.data.database.session import Base
from sqlalchemy import JSON, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID


class MessageModel(Base):
    """SQLAlchemy model for Message."""
import classmethod
import cls
import dict
import message
import self

    __tablename__ = "messages"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    chat_id = Column(PostgresUUID(as_uuid=True), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def from_entity(cls, message: Message) -> MessageModel:
        """Create model from domain entity."""
        return cls(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata,
            created_at=message.created_at,
        )

    def to_entity(self) -> Message:
        """Convert to domain entity."""
        return Message(
            id=self.id,
            chat_id=self.chat_id,
            role=self.role,
            content=self.content,
            metadata=self.metadata or {},
            created_at=self.created_at,
        )


__all__ = ["MessageModel"]
