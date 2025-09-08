"""Security model for tracking authentication, authorization, and security events."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

# Constants for common documentation strings
ADDITIONAL_METADATA_DOC = "Additional metadata"
THREAT_CATEGORIZATION_DOC = "Tags for threat categorization"
EVENT_CATEGORIZATION_DOC = "Tags for event categorization"


class SecurityEvent(FullFeaturedBaseModel):
    """Security event model for tracking security-related events."""
import self
import str

    __tablename__: str = "security_events"

    # Event identification
    event_type = Column(
        String(100), nullable=False, index=True, doc="Type of security event"
    )
    event_name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Name of the specific security event",
    )
    severity = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Event severity (low, medium, high, critical)",
    )
    category = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Event category (authentication, authorization, intrusion)",
    )

    # Actor information
    user_id = Column(
        String(36), nullable=True, index=True, doc="User ID if event is user-related"
    )
    username = Column(
        String(255), nullable=True, index=True, doc="Username if available"
    )
    user_email = Column(String(255), nullable=True, doc="User email if available")
    actor_type = Column(
        String(50),
        nullable=False,
        default="user",
        doc="Type of actor (user, system, service, unknown)",
    )

    # Source information
    ip_address = Column(String(45), nullable=True, index=True, doc="Source IP address")
    user__ = Column(Text, nullable=True, doc="User agent string")
    location = Column(JSON, nullable=True, doc="Geographical location data")

    # Event details
    description = Column(Text, nullable=False, doc="Description of the security event")
    action_attempted = Column(
        String(255), nullable=True, doc="Action that was attempted"
    )
    resource = Column(
        String(255), nullable=True, doc="Resource that was accessed or attempted"
    )
    method = Column(String(20), nullable=True, doc="HTTP method if applicable")
    endpoint = Column(String(255), nullable=True, doc="API endpoint if applicable")

    # Result
    _ = Column(
        String(20),
        nullable=False,
        doc="Result of the action (success, failure, blocked)",
    )
    failure_reason = Column(
        String(255), nullable=True, doc="Reason for failure if applicable"
    )

    # Risk assessment
    risk_score = Column(Integer, nullable=True, doc="Risk score (0-100)")
    threat_indicators = Column(JSON, nullable=True, doc="Threat indicators detected")

    # Context
    session_id = Column(
        String(36), nullable=True, index=True, doc="Session ID if applicable"
    )
    request_id = Column(
        String(36), nullable=True, index=True, doc="Request ID for tracing"
    )
    correlation_id = Column(
        String(36), nullable=True, index=True, doc="Correlation ID for related events"
    )

    # Additional data
    event_data = Column(JSON, nullable=True, doc="Additional security event data")
    security_metadata = Column(JSON, nullable=True, doc=ADDITIONAL_METADATA_DOC)
    tags = Column(JSON, nullable=True, doc=EVENT_CATEGORIZATION_DOC)

    # Investigation
    investigated = Column(
        String(20),
        nullable=False,
        default="pending",
        doc="Investigation status (pending, in_progress, completed)",
    )
    investigated_by = Column(
        String(36), nullable=True, doc="Who investigated the event"
    )
    investigation_notes = Column(Text, nullable=True, doc="Investigation notes")

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the security event occurred"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<SecurityEvent(type={self.event_type}, severity={self.severity}, result={self.result})>"


class AccessAttempt(FullFeaturedBaseModel):
    """Access attempt model for tracking authentication and authorization attempts."""

    __tablename__: str = "access_attempts"

    # Attempt identification
    attempt_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of access attempt (login, api_access, resource_access)",
    )
    authentication_method = Column(
        String(50), nullable=True, doc="Authentication method used"
    )

    # User information
    user_id = Column(String(36), nullable=True, index=True, doc="User ID if known")
    username = Column(String(255), nullable=True, index=True, doc="Username attempted")
    email = Column(String(255), nullable=True, index=True, doc="Email attempted")

    # Source information
    ip_address = Column(String(45), nullable=True, index=True, doc="Source IP address")
    user__ = Column(Text, nullable=True, doc="User agent string")
    country = Column(String(2), nullable=True, doc="Country code from IP")
    city = Column(String(100), nullable=True, doc="City from IP")

    # Access details
    resource = Column(String(255), nullable=True, doc="Resource being accessed")
    action = Column(String(100), nullable=True, doc="Action being performed")
    permissions_required = Column(
        JSON, nullable=True, doc="Permissions required for the action"
    )

    # Result
    success = Column(
        String(20),
        nullable=False,
        doc="Result of the attempt (success, failure, blocked)",
    )
    failure_reason = Column(String(255), nullable=True, doc="Reason for failure")
    response_time_ms = Column(
        Integer, nullable=True, doc="Response time in milliseconds"
    )

    # Security flags
    suspicious = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether attempt is suspicious (yes, no, maybe)",
    )
    blocked = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether attempt was blocked (yes, no)",
    )
    requires_mfa = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether MFA was required (yes, no)",
    )
    mfa_success = Column(
        String(20), nullable=True, doc="MFA result if applicable (success, failure)"
    )

    # Context
    session_id = Column(
        String(36), nullable=True, index=True, doc="Session ID if applicable"
    )
    device_fingerprint = Column(
        String(255), nullable=True, doc="Device fingerprint hash"
    )

    # Additional data
    headers = Column(JSON, nullable=True, doc="Request headers")
    access_metadata = Column(JSON, nullable=True, doc=ADDITIONAL_METADATA_DOC)

    # Timing
    attempted_at = Column(
        DateTime, nullable=False, index=True, doc="When the access was attempted"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<AccessAttempt(type={self.attempt_type}, user={self.username}, success={self.success})>"


class ThreatDetection(FullFeaturedBaseModel):
    """Threat detection model for tracking detected security threats."""

    __tablename__: str = "threat_detections"

    # Threat identification
    threat_type = Column(
        String(100), nullable=False, index=True, doc="Type of threat detected"
    )
    threat_name = Column(
        String(255), nullable=False, index=True, doc="Name of the specific threat"
    )
    severity = Column(
        String(20),
        nullable=False,
        index=True,
        doc="Threat severity (low, medium, high, critical)",
    )
    confidence = Column(Integer, nullable=False, doc="Confidence level (0-100)")

    # Source information
    source_ip = Column(
        String(45), nullable=True, index=True, doc="Source IP address of the threat"
    )
    source__ = Column(
        String(36), nullable=True, index=True, doc="User associated with the threat"
    )
    source_country = Column(String(2), nullable=True, doc="Country of origin")

    # Detection details
    description = Column(Text, nullable=False, doc="Description of the threat")
    detection_method = Column(
        String(100), nullable=False, doc="Method used to detect the threat"
    )
    indicators = Column(
        JSON, nullable=False, doc="Threat indicators that triggered detection"
    )
    evidence = Column(
        JSON, nullable=True, doc="Evidence supporting the threat detection"
    )

    # Impact assessment
    potential_impact = Column(
        String(20),
        nullable=True,
        doc="Potential impact level (low, medium, high, critical)",
    )
    affected_resources = Column(
        JSON, nullable=True, doc="Resources potentially affected"
    )
    attack_vector = Column(String(100), nullable=True, doc="Attack vector used")

    # Response
    status = Column(
        String(20),
        nullable=False,
        default="detected",
        doc="Status (detected, investigating, mitigated, false_positive)",
    )
    action_taken = Column(String(255), nullable=True, doc="Action taken in response")
    mitigated_at = Column(DateTime, nullable=True, doc="When threat was mitigated")
    mitigated_by = Column(String(36), nullable=True, doc="Who mitigated the threat")

    # Classification
    false_positive = Column(
        String(20),
        nullable=False,
        default="unknown",
        doc="Whether detection is false positive (yes, no, unknown)",
    )
    analyst_notes = Column(Text, nullable=True, doc="Security analyst notes")

    # Additional data
    raw_data = Column(JSON, nullable=True, doc="Raw detection data")
    threat_metadata = Column(JSON, nullable=True, doc=ADDITIONAL_METADATA_DOC)
    tags = Column(JSON, nullable=True, doc=THREAT_CATEGORIZATION_DOC)

    # Timing
    detected_at = Column(
        DateTime, nullable=False, index=True, doc="When the threat was detected"
    )
    first_seen_at = Column(
        DateTime, nullable=True, doc="When threat activity was first observed"
    )
    last_seen_at = Column(
        DateTime, nullable=True, doc="When threat activity was last observed"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<ThreatDetection(type={self.threat_type}, severity={self.severity}, status={self.status})>"
