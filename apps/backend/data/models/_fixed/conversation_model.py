"""
Conversation Database Model - SQLAlchemy 2.x Fixed Version.

Represents conversations between users and agents with proper type safety.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
import TypeError
import attachments
import context
import dict
import feedback
import float
import int
import isinstance
import list
import metadata
import rating
import self
import settings
import str


class Conversation(BaseModel):
    """Conversation model for tracking chat sessions."""

    # Basic Information
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active", index=True
    )

    # Participants
    user_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)

    # Conversation Settings
    context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    settings_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Statistics
    message_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # User Feedback
    user_rating: Mapped[str | None] = mapped_column(String(10), nullable=True)
    user_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    satisfaction_score: Mapped[str | None] = mapped_column(String(20), nullable=True)

    def get_context(self) -> dict[str, Any]:
        """Get conversation context from JSON."""
        if not self.context_json:
            return {}
        try:
            parsed = json.loads(self.context_json)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_context(self, context: dict[str, Any]) -> None:
        """Set conversation context as JSON."""
        self.context_json = json.dumps(context)

    def get_settings(self) -> dict[str, Any]:
        """Get conversation settings from JSON."""
        if not self.settings_json:
            return {}
        try:
            raw = str(self.settings_json)
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_settings(self, settings: dict[str, Any]) -> None:
        """Set conversation settings as JSON."""
        self.settings_json = json.dumps(settings)

    def start_conversation(self) -> None:
        """Start the conversation."""
        now = datetime.now(UTC)
        self.started_at = now
        self.last_activity_at = now
        self.status = "active"

    def end_conversation(self) -> None:
        """End the conversation."""
        now = datetime.now(UTC)
        self.ended_at = now
        self.last_activity_at = now
        self.status = "ended"

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

    def set_user_feedback(
        self, rating: int | None = None, feedback: str | None = None
    ) -> None:
        """Set user feedback and rating."""
        if rating is not None:
            self.user_rating = str(rating)
            self.user_feedback = feedback

            # Auto-calculate satisfaction score
            if rating >= 4:
                self.satisfaction_score = "high"
            elif rating >= 3:
                self.satisfaction_score = "medium"
            else:
                self.satisfaction_score = "low"


class ConversationMessage(BaseModel):
    """Individual message in a conversation."""

    # Message Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    message_type: Mapped[str] = mapped_column(
        String(50), default="text", nullable=False
    )

    # References
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id"), nullable=False, index=True
    )
    parent_message_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # Message Metadata
    message_metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    attachments_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Processing
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Quality
    confidence_score: Mapped[float | None] = mapped_column(nullable=True)
    relevance_score: Mapped[float | None] = mapped_column(nullable=True)

    def get_metadata(self) -> dict[str, Any]:
        """Get message metadata from JSON."""
        if not self.message_metadata_json:
            return {}
        try:
            parsed = json.loads(self.message_metadata_json)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set message metadata as JSON."""
        self.message_metadata_json = json.dumps(metadata)

    def get_attachments(self) -> list[dict[str, Any]]:
        """Get message attachments from JSON."""
        if not self.attachments_json:
            return []
        try:
            parsed = json.loads(self.attachments_json)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def set_attachments(self, attachments: list[dict[str, Any]]) -> None:
        """Set message attachments as JSON."""
        self.attachments_json = json.dumps(attachments)


__all__ = ["Conversation", "ConversationMessage"]
