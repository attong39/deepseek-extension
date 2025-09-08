"""Logs model for storing application logs and audit trails."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text


class LogEntry(FullFeaturedBaseModel):
    """Log entry model for storing application logs."""
import self
import str

    __tablename__: str = "log_entries"

    # Log identification
    level = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    logger_name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Name of the logger that created this entry",
    )
    module = Column(
        String(255), nullable=True, index=True, doc="Module where the log originated"
    )
    function = Column(
        String(255), nullable=True, doc="Function where the log originated"
    )
    line_number = Column(
        Integer, nullable=True, doc="Line number where the log originated"
    )

    # Log content
    message = Column(Text, nullable=False, doc="Log message content")
    formatted_message = Column(
        Text, nullable=True, doc="Formatted log message with context"
    )

    # Context information
    user_id = Column(
        String(36), nullable=True, index=True, doc="User ID if log is user-specific"
    )
    session_id = Column(
        String(36),
        nullable=True,
        index=True,
        doc="Session ID if log is session-specific",
    )
    request_id = Column(
        String(36), nullable=True, index=True, doc="Request ID for tracing"
    )
    trace_id = Column(String(64), nullable=True, index=True, doc="Distributed trace ID")

    # Exception information
    exception_type = Column(
        String(255), nullable=True, doc="Exception type if log is from an exception"
    )
    exception_message = Column(Text, nullable=True, doc="Exception message")
    stack_trace = Column(Text, nullable=True, doc="Full stack trace")

    # Additional data
    extra_data = Column(JSON, nullable=True, doc="Additional structured data")
    tags = Column(JSON, nullable=True, doc="Tags for log categorization")

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the log entry was created"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<LogEntry(level={self.level}, logger={self.logger_name}, message={self.message[:50]}...)>"


class AuditLog(FullFeaturedBaseModel):
    """Audit log model for tracking user actions and system changes."""

    __tablename__: str = "audit_logs"

    # Action identification
    action = Column(
        String(100), nullable=False, index=True, doc="Action that was performed"
    )
    entity_type = Column(
        String(100), nullable=False, index=True, doc="Type of entity that was affected"
    )
    entity_id = Column(
        String(36), nullable=True, index=True, doc="ID of the entity that was affected"
    )

    # Actor information
    user_id = Column(
        String(36), nullable=True, index=True, doc="User who performed the action"
    )
    user_email = Column(
        String(255), nullable=True, doc="Email of the user who performed the action"
    )
    actor_type = Column(
        String(50),
        nullable=False,
        default="user",
        doc="Type of actor (user, system, service)",
    )

    # Context
    session_id = Column(
        String(36),
        nullable=True,
        index=True,
        doc="Session ID when action was performed",
    )
    ip_address = Column(String(45), nullable=True, doc="IP address of the actor")
    user__ = Column(Text, nullable=True, doc="User agent string")

    # Change details
    old_values = Column(JSON, nullable=True, doc="Previous values before the change")
    new_values = Column(JSON, nullable=True, doc="New values after the change")
    changes_summary = Column(
        Text, nullable=True, doc="Human-readable summary of changes"
    )

    # Result
    success = Column(
        String(20),
        nullable=False,
        default="success",
        doc="Result of the action (success, failure, partial)",
    )
    error_message = Column(Text, nullable=True, doc="Error message if action failed")

    # Additional audit_metadata
    audit_metadata = Column(JSON, nullable=True, doc="Additional audit metadata")
    tags = Column(JSON, nullable=True, doc="Tags for audit log categorization")

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the action was performed"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<AuditLog(action={self.action}, entity={self.entity_type}, user={self.user_id})>"


class SystemEvent(FullFeaturedBaseModel):
    """System event model for tracking system-level events."""

    __tablename__: str = "system_events"

    # Event identification
    event_type = Column(
        String(100), nullable=False, index=True, doc="Type of system event"
    )
    event_name = Column(
        String(255), nullable=False, index=True, doc="Name of the specific event"
    )
    severity = Column(
        String(20),
        nullable=False,
        default="info",
        doc="Event severity (info, warning, error, critical)",
    )

    # Event details
    description = Column(Text, nullable=False, doc="Description of the event")
    component = Column(
        String(100),
        nullable=True,
        index=True,
        doc="System component that generated the event",
    )
    service = Column(
        String(100), nullable=True, index=True, doc="Service that generated the event"
    )

    # Event data
    event_data = Column(JSON, nullable=True, doc="Structured event data")
    error_details = Column(
        JSON, nullable=True, doc="Error details if event represents an error"
    )

    # Context
    environment = Column(
        String(50),
        nullable=True,
        doc="Environment where event occurred (dev, staging, prod)",
    )
    version = Column(
        String(50), nullable=True, doc="Application version when event occurred"
    )

    # Resolution
    resolved = Column(
        String(20),
        nullable=False,
        default="open",
        doc="Resolution status (open, resolved, ignored)",
    )
    resolution_notes = Column(
        Text, nullable=True, doc="Notes about how the event was resolved"
    )
    resolved_at = Column(DateTime, nullable=True, doc="When the event was resolved")
    resolved_by = Column(String(36), nullable=True, doc="Who resolved the event")

    # Additional metadata
    tags = Column(JSON, nullable=True, doc="Tags for event categorization")

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the event occurred"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<SystemEvent(type={self.event_type}, name={self.event_name}, severity={self.severity})>"
