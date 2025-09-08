"""Audit model for compliance and security tracking."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from apps.backend.data.models.base import Base
from sqlalchemy import JSON as JSONType
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class AuditLog(Base):
    """
import action
import bool
import dict
import flag
import float
import int
import key
import kwargs
import list
import operation
import resource_type
import self
import status
import str
import super
import tag
import value
    Audit log model for tracking user actions and system events.

    Provides comprehensive audit trail for compliance (GDPR, CCPA, SOX),
    security monitoring, and operational transparency.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "audit_logs"

    # Override base id to use string instead of UUID for this table
    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # User context
    user_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Action details
    action: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    resource_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    operation: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # CREATE, READ, UPDATE, DELETE
    status: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # SUCCESS, FAILURE, PARTIAL

    # Request context
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    api_endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    http_method: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Payload data
    request_payload: Mapped[dict[str, Any] | None] = mapped_column(
        JSONType, nullable=True
    )
    response_payload: Mapped[dict[str, Any] | None] = mapped_column(
        JSONType, nullable=True
    )
    before_state: Mapped[dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    after_state: Mapped[dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    changes: Mapped[dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    # Metadata and classification
    meta_data: Mapped[dict[str, Any]] = mapped_column(
        JSONType, nullable=False, default={}
    )
    tags: Mapped[list[str]] = mapped_column(JSONType, nullable=False, default=[])
    risk_level: Mapped[str] = mapped_column(
        String(50), nullable=False, default="low"
    )  # low, medium, high, critical
    compliance_flags: Mapped[list[str]] = mapped_column(
        JSONType, nullable=False, default=[]
    )

    # Performance metrics
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Override base timestamps to remove onupdate for audit logs (immutable)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __init__(
        self,
        action: str,
        resource_type: str,
        operation: str,
        status: str,
        **kwargs: Any,
    ) -> None:
        """
        Initialize audit log entry.

        Args:
            action: Description of the action performed
            resource_type: Type of resource being accessed
            operation: CRUD operation type
            status: Success/failure status
            **kwargs: Additional model arguments including all optional fields
        """
        super().__init__(**kwargs)
        self.action = action
        self.resource_type = resource_type
        self.operation = operation
        self.status = status

    def add_tag(self, tag: str) -> None:
        """Add a classification tag."""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)

    def add_compliance_flag(self, flag: str) -> None:
        """Add a compliance requirement flag."""
        if self.compliance_flags is None:
            self.compliance_flags = []
        if flag not in self.compliance_flags:
            self.compliance_flags.append(flag)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        if self.meta_data is None:
            self.meta_data = {}
        self.meta_data[key] = value

    def is_high_risk(self) -> bool:
        """Check if audit entry is high risk."""
        return self.risk_level in ["high", "critical"]

    def is_failure(self) -> bool:
        """Check if operation failed."""
        return self.status in ["FAILURE", "PARTIAL"]

    def has_compliance_requirements(self) -> bool:
        """Check if entry has compliance flags."""
        return bool(self.compliance_flags)

    def get_duration_seconds(self) -> float | None:
        """Get operation duration in seconds."""
        if self.duration_ms is not None:
            return self.duration_ms / 1000.0
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert audit log to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "resource_name": self.resource_name,
            "operation": self.operation,
            "status": self.status,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_id": self.request_id,
            "api_endpoint": self.api_endpoint,
            "http_method": self.http_method,
            "request_payload": self.request_payload,
            "response_payload": self.response_payload,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "changes": self.changes,
            "metadata": self.meta_data,
            "tags": self.tags,
            "risk_level": self.risk_level,
            "compliance_flags": self.compliance_flags,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        """String representation of audit log."""
        return (
            f"<AuditLog(id={self.id}, action={self.action}, "
            f"resource_type={self.resource_type}, status={self.status})>"
        )
