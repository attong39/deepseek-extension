"""


Conversation Database Model.





Represents conversations between users and agents.


"""

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
import TypeError
import ValueError
import attachments
import bool
import context
import context_update
import dict
import feedback
import float
import int
import isinstance
import len
import list
import metadata
import rating
import raw_s
import self
import settings
import str


class Conversation(BaseModel, SoftDeleteMixin):
    """Conversation model for tracking chat sessions."""

    # Basic Information

    title = Column(String(255), nullable=True, doc="Conversation title")

    summary = Column(Text, nullable=True, doc="Conversation summary")

    status = Column(
        String(20),
        nullable=False,
        default="active",
        index=True,
        doc="Conversation status (active, archived, ended)",
    )

    # Participants

    user_id = Column(
        String(36),
        nullable=False,
        index=True,
        doc="User ID participating in conversation",
    )

    agent_id = Column(
        String(36),
        ForeignKey("agents.id"),
        nullable=False,
        index=True,
        doc="Agent ID in conversation",
    )

    # Session Information

    session_id = Column(String(36), nullable=True, index=True, doc="Session identifier")

    channel = Column(
        String(50),
        nullable=False,
        default="chat",
        doc="Communication channel (chat, voice, api, etc.)",
    )

    # Metrics

    message_count = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Total number of messages in conversation",
    )

    duration_seconds = Column(
        Integer, nullable=True, doc="Conversation duration in seconds"
    )

    # Timestamps

    started_at = Column(
        DateTime(timezone=True), nullable=True, doc="Conversation start time"
    )

    ended_at = Column(
        DateTime(timezone=True), nullable=True, doc="Conversation end time"
    )

    last_activity_at = Column(
        DateTime(timezone=True), nullable=True, doc="Last activity timestamp"
    )

    # Context and Configuration

    context_json = Column(
        Text, nullable=True, doc="Conversation context in JSON format"
    )

    settings_json = Column(
        Text, nullable=True, doc="Conversation settings in JSON format"
    )

    # Ratings and Feedback

    user_rating = Column(String(10), nullable=True, doc="User rating (1-5 stars)")

    user_feedback = Column(Text, nullable=True, doc="User feedback text")

    satisfaction_score = Column(
        String(10), nullable=True, doc="Overall satisfaction score"
    )

    # Privacy and Security

    is_private = Column(
        Boolean, nullable=False, default=True, doc="Whether conversation is private"
    )

    encryption_enabled = Column(
        Boolean, nullable=False, default=False, doc="Whether conversation is encrypted"
    )

    # Relationships

    _ = relationship("Agent", back_populates="conversations")

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    # Helper Methods

    def get_context(self) -> dict[str, Any]:
        """Get conversation context."""

        if self.context_json is None:
            return {}

        try:
            return json.loads(str(self.context_json))

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_context(self, context: dict[str, Any]) -> None:
        """Set conversation context."""

        self.context_json = json.dumps(context)

    def update_context(self, context_update: dict[str, Any]) -> None:
        """Update conversation context."""

        current = self.get_context()

        current.update(context_update)

        self.set_context(current)

    def get_settings(self) -> dict[str, Any]:
        """Get conversation settings."""

        # Tránh dùng trực tiếp Column trong điều kiện/JSON parse
        if self.settings_json is None:
            return {}

        try:
            raw = (
                self.settings_json
                if isinstance(self.settings_json, str)
                else str(self.settings_json)
            )
            return json.loads(raw)

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_settings(self, settings: dict[str, Any]) -> None:
        """Set conversation settings."""

        self.settings_json = json.dumps(settings)

    def start_conversation(self) -> None:
        """Mark conversation as started."""

        now = datetime.now(UTC)

        self.started_at = now

        self.last_activity_at = now

        self.status = "active"

    def end_conversation(self) -> None:
        """Mark conversation as ended."""

        now = datetime.now(UTC)

        self.ended_at = now

        self.last_activity_at = now

        self.status = "ended"

        # Calculate duration

        # Bảo vệ kiểu: chỉ tính khi started_at là datetime thật sự
        if isinstance(self.started_at, datetime):
            duration = now - self.started_at
            self.duration_seconds = int(duration.total_seconds())

    def archive_conversation(self) -> None:
        """Archive the conversation."""

        self.status = "archived"

        self.last_activity_at = datetime.now(UTC)

    def update_activity(self) -> None:
        """Update last activity timestamp."""

        self.last_activity_at = datetime.now(UTC)

    def increment_message_count(self) -> None:
        """Increment message count."""

        self.message_count += 1

        self.update_activity()

    def set_rating(self, rating: int, feedback: str | None = None) -> None:
        """Set user rating and feedback."""

        if 1 <= rating <= 5:
            self.user_rating = str(rating)

            self.user_feedback = feedback

            # Calculate satisfaction score (basic implementation)

            if rating >= 4:
                self.satisfaction_score = "high"

            elif rating >= 3:
                self.satisfaction_score = "medium"

            else:
                self.satisfaction_score = "low"

    def get_duration_human(self) -> str:
        """Get human-readable duration."""

        seconds_val = (
            self.duration_seconds if isinstance(self.duration_seconds, int) else None
        )
        if seconds_val is None:
            return "Unknown"

        seconds = int(seconds_val)

        if seconds < 60:
            return f"{seconds} seconds"

        elif seconds < 3600:
            minutes = seconds // 60

            return f"{minutes} minutes"

        else:
            hours = seconds // 3600

            minutes = (seconds % 3600) // 60

            return f"{hours}h {minutes}m"

    def is_active(self) -> bool:
        """Check if conversation is active."""

        return str(self.status) == "active"

    def is_ended(self) -> bool:
        """Check if conversation is ended."""

        return str(self.status) == "ended"

    def can_user_access(self, user_id: str) -> bool:
        """Check if user can access this conversation."""

        # Owner always has access

        if str(self.user_id) == str(user_id):
            return True

        # Public conversations are accessible to all
        is_private_val = self.is_private if isinstance(self.is_private, bool) else True
        if not is_private_val:
            return True

        return False

    def to_dict_summary(self) -> dict[str, Any]:
        """Get conversation summary."""

        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "message_count": self.message_count,
            "duration": self.get_duration_human(),
            "channel": self.channel,
            "user_rating": self.user_rating,
            "satisfaction_score": self.satisfaction_score,
            "started_at": self.started_at.isoformat()
            if isinstance(self.started_at, datetime)
            else None,
            "ended_at": self.ended_at.isoformat()
            if isinstance(self.ended_at, datetime)
            else None,
            "last_activity_at": self.last_activity_at.isoformat()
            if isinstance(self.last_activity_at, datetime)
            else None,
            "created_at": self.created_at.isoformat()
            if isinstance(self.created_at, datetime)
            else None,
        }

    def to_dict_detailed(self) -> dict[str, Any]:
        """Get detailed conversation information."""

        summary = self.to_dict_summary()

        summary.update(
            {
                "summary": self.summary,
                "user_id": self.user_id,
                "agent_id": self.agent_id,
                "session_id": self.session_id,
                "context": self.get_context(),
                "settings": self.get_settings(),
                "user_feedback": self.user_feedback,
                "is_private": self.is_private,
                "encryption_enabled": self.encryption_enabled,
                "duration_seconds": self.duration_seconds,
            }
        )

        return summary

    def __repr__(self) -> str:
        """String representation."""

        return f"<Conversation(id={self.id}, user={self.user_id}, agent={self.agent_id}, status={self.status})>"


class Message(BaseModel):
    """Message model for individual messages in conversations."""

    # Message Content

    content = Column(Text, nullable=False, doc="Message content")

    content_type = Column(
        String(50),
        nullable=False,
        default="text",
        doc="Content type (text, image, file, etc.)",
    )

    # Message Metadata

    role = Column(
        String(20), nullable=False, doc="Message role (user, assistant, system)"
    )

    sequence_number = Column(
        Integer, nullable=False, doc="Message sequence number in conversation"
    )

    # Relationships

    conversation_id = Column(
        String(36),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
        doc="Conversation ID",
    )

    parent_message_id = Column(
        String(36),
        ForeignKey("messages.id"),
        nullable=True,
        doc="Parent message ID for threading",
    )

    # Sender Information

    sender_id = Column(
        String(36), nullable=True, doc="ID of the sender (user or agent)"
    )

    sender_type = Column(
        String(20), nullable=False, doc="Type of sender (user, agent, system)"
    )

    # Processing Information

    processing_time_ms = Column(
        String(20), nullable=True, doc="Time taken to process/generate message"
    )

    tokens_used = Column(
        Integer, nullable=True, doc="Number of tokens used for this message"
    )

    model_used = Column(
        String(100), nullable=True, doc="AI model used to generate response"
    )

    # Status and Flags

    is_edited = Column(
        Boolean, nullable=False, default=False, doc="Whether message has been edited"
    )

    is_flagged = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether message is flagged for review",
    )

    # Additional Data

    metadata_json = Column(
        Text, nullable=True, doc="Additional message metadata in JSON"
    )

    attachments_json = Column(
        Text, nullable=True, doc="Message attachments in JSON format"
    )

    # Relationships

    conversation = relationship("Conversation", back_populates="messages")

    parent_message = relationship(
        "Message",
        remote_side="Message.id",
        foreign_keys=[parent_message_id],
    )

    child_messages = relationship("Message", back_populates="parent_message")

    # Helper Methods

    def get_metadata(self) -> dict[str, Any]:
        """Get message metadata."""

        raw = self.metadata_json if isinstance(self.metadata_json, str) else None
        if raw is None:
            return {}
        raw_s: str = raw
        if len(raw_s) == 0:
            return {}

        try:
            return json.loads(raw)

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set message metadata."""

        self.metadata_json = json.dumps(metadata)

    def get_attachments(self) -> list[dict[str, Any]]:
        """Get message attachments."""

        raw = self.attachments_json if isinstance(self.attachments_json, str) else None
        if raw is None:
            return []
        raw_s: str = raw
        if len(raw_s) == 0:
            return []

        try:
            return json.loads(raw)

        except (json.JSONDecodeError, TypeError):
            return []

    def set_attachments(self, attachments: list[dict[str, Any]]) -> None:
        """Set message attachments."""

        self.attachments_json = json.dumps(attachments)

    def is_from_user(self) -> bool:
        """Check if message is from user."""

        return str(self.role) == "user"

    def is_from_assistant(self) -> bool:
        """Check if message is from assistant."""

        return str(self.role) == "assistant"

    def is_system_message(self) -> bool:
        """Check if message is system message."""

        return str(self.role) == "system"

    def get_processing_time_human(self) -> str:
        """Get human-readable processing time."""
        raw = (
            self.processing_time_ms
            if isinstance(self.processing_time_ms, str)
            else None
        )
        if raw is None:
            return "Unknown"
        raw_s: str = raw
        if len(raw_s) == 0:
            return "Unknown"

        try:
            ms = float(raw)

            if ms < 1000:
                return f"{ms:.0f}ms"

            else:
                return f"{ms / 1000:.1f}s"

        except (ValueError, TypeError):
            return "Unknown"

    def to_dict_public(self) -> dict[str, Any]:
        """Get public message representation."""

        return {
            "id": self.id,
            "content": self.content,
            "content_type": self.content_type,
            "role": self.role,
            "sequence_number": self.sequence_number,
            "sender_type": self.sender_type,
            "is_edited": self.is_edited,
            "attachments": self.get_attachments(),
            "created_at": self.created_at.isoformat()
            if isinstance(self.created_at, datetime)
            else None,
        }

    def to_dict_detailed(self) -> dict[str, Any]:
        """Get detailed message representation."""

        public = self.to_dict_public()

        public.update(
            {
                "conversation_id": self.conversation_id,
                "parent_message_id": self.parent_message_id,
                "sender_id": self.sender_id,
                "processing_time": self.get_processing_time_human(),
                "tokens_used": self.tokens_used,
                "model_used": self.model_used,
                "is_flagged": self.is_flagged,
                "metadata": self.get_metadata(),
            }
        )

        return public

    def __repr__(self) -> str:
        """String representation."""

        content_text = self.content if isinstance(self.content, str) else ""
        content_preview = (
            content_text[:50] + "..." if len(content_text) > 50 else content_text
        )

        return f"<Message(id={self.id}, role={self.role}, content='{content_preview}')>"
