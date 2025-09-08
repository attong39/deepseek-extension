"""
Session Entity - Standard Domain Model
======================================

Đại diện cho user session trong hệ thống
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from app._base_model import DomainModel
from pydantic import Field, field_validator
import ValueError
import bool
import classmethod
import dict
import hours
import int
import new_context
import self
import str
import v


class SessionStatus(str, Enum):
    """Trạng thái session"""

    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class SessionType(str, Enum):
    """Loại session"""

    CONVERSATION = "conversation"
    API = "api"
    ADMIN = "admin"
    SYSTEM = "system"


class Session(DomainModel):
    """
    Session Entity

    Represents a user session with lifecycle management
    """

    # === Core Identity ===
    id: UUID = Field(default_factory=uuid4, description="Unique session ID")
    user_id: UUID = Field(description="User ID who owns this session")

    # === Core Properties ===
    title: str = Field(min_length=1, max_length=200, description="Session title")
    session_type: SessionType = Field(
        default=SessionType.CONVERSATION, description="Type of session"
    )

    # === Status & Lifecycle ===
    status: SessionStatus = Field(
        default=SessionStatus.ACTIVE, description="Session status"
    )

    # === Context & Configuration ===
    context: dict[str, Any] = Field(
        default_factory=dict, description="Session context data"
    )

    # === Timestamps ===
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    expires_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate session title"""
        if not v or not v.strip():
            raise ValueError("Session title cannot be empty")
        return v.strip()

    def update_context(self, new_context: dict[str, Any]) -> Session:
        """Update session context"""
        updated_context = {**self.context, **new_context}
        return self.model_copy(
            update={"context": updated_context, "updated_at": datetime.now(UTC)}
        )

    def expire(self) -> Session:
        """Expire session"""
        return self.model_copy(
            update={
                "status": SessionStatus.EXPIRED,
                "updated_at": datetime.now(UTC),
                "expires_at": datetime.now(UTC),
            }
        )

    def terminate(self) -> Session:
        """Terminate session"""
        return self.model_copy(
            update={"status": SessionStatus.TERMINATED, "updated_at": datetime.now(UTC)}
        )

    def is_active(self) -> bool:
        """Check if session is active"""
        if self.status != SessionStatus.ACTIVE:
            return False

        if self.expires_at and datetime.now(UTC) > self.expires_at:
            return False

        return True

    def extend_expiry(self, hours: int = 24) -> Session:
        """Extend session expiry"""
        from datetime import timedelta

        new_expiry = datetime.now(UTC) + timedelta(hours=hours)
        return self.model_copy(
            update={"expires_at": new_expiry, "updated_at": datetime.now(UTC)}
        )
