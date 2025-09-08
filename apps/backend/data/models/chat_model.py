"""Chat model for conversation and messaging functionality."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from apps.backend.data.models.base import Base
from apps.backend.data.models.user_model import User  # use canonical User model
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Constants for foreign key actions
CASCADE = "CASCADE"
SET_NULL = "SET NULL"

# Table name constants
CONVERSATIONS_TABLE = "conversations"
USERS_TABLE = "users"
MESSAGES_TABLE = "messages"

# Foreign key reference constants
CONVERSATIONS_ID = f"{CONVERSATIONS_TABLE}.id"
USERS_ID = f"{USERS_TABLE}.id"
MESSAGES_ID = f"{MESSAGES_TABLE}.id"


# NOTE: The canonical `User` model is defined in `user_model.py`. Import it
# here to use for relationships (avoids registering a second `users` table).


class Conversation(Base):
    """
import bool
import content
import content_type
import conversation_id
import conversation_type
import created_by
import default
import dict
import emoji
import file_size
import filename
import float
import int
import key
import kwargs
import len
import list
import max
import message_id
import original_filename
import parent_message_id
import role
import self
import sender_id
import sender_type
import storage_path
import str
import super
import title
import user_id
import value
    Conversation model for chat threads.

    Represents a conversation that can contain multiple messages and participants.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "conversations"

    # Conversation metadata
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    conversation_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="direct"
    )  # direct, group, channel

    # Status and visibility
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="active"
    )  # active, archived, deleted
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Creator information
    created_by: Mapped[str] = mapped_column(String(36), nullable=False)

    # Conversation statistics
    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    participant_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Timestamps
    last_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metadata
    settings: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default={})
    conversation_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # AI/Agent specific fields
    agent_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default={})
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    participants: Mapped[list[User]] = relationship(
        "User", secondary="conversation_participants", back_populates="conversations"
    )
    messages: Mapped[list[Message]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        created_by: str,
        title: str | None = None,
        conversation_type: str = "direct",
        **kwargs: Any,
    ) -> None:
        """
        Initialize conversation.

        Args:
            created_by: ID of user who created conversation
            title: Conversation title
            conversation_type: Type of conversation
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.created_by = created_by
        self.title = title
        self.conversation_type = conversation_type

    def add_message(self) -> None:
        """Increment message count and update last message timestamp."""
        self.message_count += 1
        self.last_message_at = datetime.now(UTC)

    def set_setting(self, key: str, value: Any) -> None:
        """Set conversation setting."""
        if self.settings is None:
            self.settings = {}
        self.settings[key] = value

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get conversation setting."""
        return self.settings.get(key, default) if self.settings else default

    def is_group_conversation(self) -> bool:
        """Check if conversation is a group conversation."""
        return self.conversation_type in ["group", "channel"]

    def __repr__(self) -> str:
        """String representation of conversation."""
        return f"<Conversation(id={self.id}, title={self.title}, type={self.conversation_type})>"


class Message(Base):
    """
    Message model for individual chat messages.

    Represents a single message within a conversation.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "messages"

    # Message content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="text"
    )  # text, markdown, html, file, image

    # Message relationships
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey(CONVERSATIONS_ID, ondelete=CASCADE), nullable=False
    )
    sender_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(USERS_ID, ondelete=SET_NULL), nullable=True
    )
    sender_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="user"
    )  # user, agent, system

    # Message threading
    parent_message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(MESSAGES_ID, ondelete=CASCADE), nullable=True
    )
    thread_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # Message status
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="sent"
    )  # sent, delivered, read, failed
    is_edited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Timestamps
    read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # AI/Agent specific fields
    agent_response_to: Mapped[UUID | None] = mapped_column(
        ForeignKey(MESSAGES_ID, ondelete=SET_NULL), nullable=True
    )
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence_score: Mapped[float | None] = mapped_column(
        Integer, nullable=True
    )  # 0.0 to 1.0

    # Metadata
    message_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    attachments: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=[]
    )  # attachment IDs
    mentions: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=[]
    )  # mentioned user IDs
    reactions: Mapped[dict[str, int]] = mapped_column(
        JSON, nullable=False, default={}
    )  # emoji -> count

    # Relationships
    conversation: Mapped[Conversation] = relationship(
        "Conversation", back_populates="messages"
    )
    sender: Mapped[User | None] = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    parent_message: Mapped[Message | None] = relationship(
        "Message",
        remote_side="Message.id",
        foreign_keys=[parent_message_id],
    )
    message_attachments: Mapped[list[MessageAttachment]] = relationship(
        "MessageAttachment", back_populates="message", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        content: str,
        conversation_id: UUID,
        sender_id: UUID | None = None,
        sender_type: str = "user",
        content_type: str = "text",
        **kwargs: Any,
    ) -> None:
        """
        Initialize message.

        Args:
            content: Message content
            conversation_id: ID of conversation
            sender_id: ID of sender user
            sender_type: Type of sender
            content_type: Content type
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.content = content
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.sender_type = sender_type
        self.content_type = content_type

    def mark_read(self) -> None:
        """Mark message as read."""
        if not self.read_at:
            self.read_at = datetime.now(UTC)
            self.status = "read"

    def mark_edited(self) -> None:
        """Mark message as edited."""
        self.is_edited = True
        self.edited_at = datetime.now(UTC)

    def mark_deleted(self) -> None:
        """Mark message as deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(UTC)
        self.status = "deleted"

    def add_reaction(self, emoji: str) -> None:
        """Add reaction to message."""
        if self.reactions is None:
            self.reactions = {}
        self.reactions[emoji] = self.reactions.get(emoji, 0) + 1

    def remove_reaction(self, emoji: str) -> None:
        """Remove reaction from message."""
        if self.reactions and emoji in self.reactions:
            self.reactions[emoji] = max(0, self.reactions[emoji] - 1)
            if self.reactions[emoji] == 0:
                del self.reactions[emoji]

    def add_mention(self, user_id: str) -> None:
        """Add user mention to message."""
        if self.mentions is None:
            self.mentions = []
        if user_id not in self.mentions:
            self.mentions.append(user_id)

    def is_from_agent(self) -> bool:
        """Check if message is from an agent."""
        return self.sender_type == "agent"

    def is_system_message(self) -> bool:
        """Check if message is a system message."""
        return self.sender_type == "system"

    def __repr__(self) -> str:
        """String representation of message."""
        content_preview = (
            self.content[:50] + "..." if len(self.content) > 50 else self.content
        )
        return f"<Message(id={self.id}, sender_type={self.sender_type}, content='{content_preview}')>"


class MessageAttachment(Base):
    """
    Message attachment model for files, images, and other media.

    Represents files and media attached to messages.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "message_attachments"

    # Attachment metadata
    message_id: Mapped[UUID] = mapped_column(
        ForeignKey(MESSAGES_ID, ondelete=CASCADE), nullable=False
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    # Storage information
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_provider: Mapped[str] = mapped_column(
        String(50), nullable=False, default="local"
    )  # local, s3, gcs

    # File metadata
    checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256
    thumbnail_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Processing status
    processing_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )  # pending, processing, completed, failed
    virus_scan_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )  # pending, clean, infected, failed

    # Metadata
    attachment_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Relationships
    message: Mapped[Message] = relationship(
        "Message", back_populates="message_attachments"
    )

    def __init__(
        self,
        message_id: UUID,
        filename: str,
        original_filename: str,
        content_type: str,
        file_size: int,
        storage_path: str,
        **kwargs: Any,
    ) -> None:
        """
        Initialize message attachment.

        Args:
            message_id: ID of parent message
            filename: Stored filename
            original_filename: Original filename
            content_type: MIME content type
            file_size: File size in bytes
            storage_path: Storage path
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.message_id = message_id
        self.filename = filename
        self.original_filename = original_filename
        self.content_type = content_type
        self.file_size = file_size
        self.storage_path = storage_path

    def is_image(self) -> bool:
        """Check if attachment is an image."""
        return self.content_type.startswith("image/")

    def is_video(self) -> bool:
        """Check if attachment is a video."""
        return self.content_type.startswith("video/")

    def is_audio(self) -> bool:
        """Check if attachment is audio."""
        return self.content_type.startswith("audio/")

    def is_document(self) -> bool:
        """Check if attachment is a document."""
        document_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "text/markdown",
        ]
        return self.content_type in document_types

    def get_file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)

    def mark_processing_completed(self) -> None:
        """Mark attachment processing as completed."""
        self.processing_status = "completed"

    def mark_virus_scan_clean(self) -> None:
        """Mark virus scan as clean."""
        self.virus_scan_status = "clean"

    def __repr__(self) -> str:
        """String representation of message attachment."""
        return f"<MessageAttachment(id={self.id}, filename={self.filename}, size={self.file_size})>"


class ConversationParticipant(Base):
    """
    Association model for conversation participants.

    Links users to conversations with additional metadata about their participation.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "conversation_participants"

    # Relationships
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey(CONVERSATIONS_ID, ondelete=CASCADE), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(USERS_ID, ondelete=CASCADE), nullable=False
    )

    # Participation metadata
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default="member"
    )  # owner, admin, moderator, member
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    left_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Participant status
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_muted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Read tracking
    last_read_message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(MESSAGES_ID, ondelete=SET_NULL), nullable=True
    )
    last_read_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    unread_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Notification preferences
    notification_settings: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    def __init__(
        self,
        conversation_id: UUID,
        user_id: UUID,
        role: str = "member",
        **kwargs: Any,
    ) -> None:
        """
        Initialize conversation participant.

        Args:
            conversation_id: ID of conversation
            user_id: ID of user
            role: Participant role
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.role = role

    def update_last_read(self, message_id: UUID) -> None:
        """Update last read message."""
        self.last_read_message_id = message_id
        self.last_read_at = datetime.now(UTC)
        self.unread_count = 0

    def increment_unread_count(self) -> None:
        """Increment unread message count."""
        self.unread_count += 1

    def leave_conversation(self) -> None:
        """Mark participant as having left the conversation."""
        self.is_active = False
        self.left_at = datetime.now(UTC)

    def mute_conversation(self) -> None:
        """Mute conversation notifications for this participant."""
        self.is_muted = True

    def unmute_conversation(self) -> None:
        """Unmute conversation notifications for this participant."""
        self.is_muted = False

    def is_admin(self) -> bool:
        """Check if participant has admin privileges."""
        return self.role in ["owner", "admin"]

    def __repr__(self) -> str:
        """String representation of conversation participant."""
        return f"<ConversationParticipant(conversation_id={self.conversation_id}, user_id={self.user_id}, role={self.role})>"
