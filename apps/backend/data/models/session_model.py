"""Session model for tracking user sessions and authentication state."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

# Constants for common documentation strings
ADDITIONAL_SESSION_DATA_DOC = "Additional session data"
SESSION_METADATA_DOC = "Session metadata"


class Session(FullFeaturedBaseModel):
    """Session model for tracking user sessions."""
import self
import str

    __tablename__: str = "sessions"

    # Session identification
    session_token = Column(
        String(255), nullable=False, unique=True, index=True, doc="Unique session token"
    )
    session_type = Column(
        String(50),
        nullable=False,
        default="web",
        doc="Type of session (web, api, mobile)",
    )

    # User information
    user_id = Column(
        String(36), nullable=True, index=True, doc="User ID associated with the session"
    )
    username = Column(String(255), nullable=True, doc="Username for the session")
    user_email = Column(String(255), nullable=True, doc="User email for the session")

    # Session state
    status = Column(
        String(20),
        nullable=False,
        default="active",
        index=True,
        doc="Session status (active, expired, revoked)",
    )
    authenticated = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether session is authenticated (yes, no)",
    )

    # Device and client information
    ip_address = Column(
        String(45), nullable=True, index=True, doc="IP address of the client"
    )
    user__ = Column(Text, nullable=True, doc="User agent string")
    device_fingerprint = Column(
        String(255), nullable=True, doc="Device fingerprint hash"
    )
    device_type = Column(
        String(50), nullable=True, doc="Type of device (desktop, mobile, tablet)"
    )
    browser = Column(String(100), nullable=True, doc="Browser information")
    operating_system = Column(
        String(100), nullable=True, doc="Operating system information"
    )

    # Location information
    country = Column(String(2), nullable=True, doc="Country code from IP")
    city = Column(String(100), nullable=True, doc="City from IP")
    timezone = Column(String(50), nullable=True, doc="Client timezone")

    # Session timing
    started_at = Column(
        DateTime, nullable=False, index=True, doc="When the session was started"
    )
    last_activity_at = Column(
        DateTime, nullable=True, index=True, doc="When the session was last active"
    )
    expires_at = Column(
        DateTime, nullable=True, index=True, doc="When the session expires"
    )
    ended_at = Column(DateTime, nullable=True, doc="When the session was ended")

    # Session activity
    request_count = Column(
        Integer, nullable=False, default=0, doc="Number of requests in this session"
    )
    page_views = Column(
        Integer, nullable=False, default=0, doc="Number of page views in this session"
    )
    duration_seconds = Column(Integer, nullable=True, doc="Session duration in seconds")

    # Authentication details
    auth_method = Column(String(50), nullable=True, doc="Authentication method used")
    mfa_enabled = Column(
        String(20), nullable=False, default="no", doc="Whether MFA is enabled (yes, no)"
    )
    mfa_verified = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether MFA was verified (yes, no)",
    )

    # Security flags
    suspicious = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether session appears suspicious (yes, no)",
    )
    risk_score = Column(
        Integer, nullable=True, doc="Risk score for the session (0-100)"
    )

    # Additional data
    session_data = Column(JSON, nullable=True, doc=ADDITIONAL_SESSION_DATA_DOC)
    session_metadata = Column(JSON, nullable=True, doc=SESSION_METADATA_DOC)
    tags = Column(JSON, nullable=True, doc="Tags for session categorization")

    def __repr__(self) -> str:
        """String representation."""
        return f"<Session(id={self.id}, user={self.user_id}, status={self.status})>"


class SessionActivity(FullFeaturedBaseModel):
    """Session activity model for tracking specific actions within sessions."""

    __tablename__: str = "session_activities"

    # Activity identification
    session_id = Column(
        String(36),
        nullable=False,
        index=True,
        doc="Session ID this activity belongs to",
    )
    activity_type = Column(
        String(100), nullable=False, index=True, doc="Type of activity performed"
    )
    action = Column(String(255), nullable=False, doc="Specific action performed")

    # Resource information
    resource = Column(String(255), nullable=True, doc="Resource accessed or modified")
    endpoint = Column(String(255), nullable=True, doc="API endpoint if applicable")
    method = Column(String(20), nullable=True, doc="HTTP method if applicable")

    # Activity details
    description = Column(Text, nullable=True, doc="Description of the activity")
    success = Column(
        String(20), nullable=False, doc="Whether activity was successful (yes, no)"
    )
    error_message = Column(Text, nullable=True, doc="Error message if activity failed")
    response_code = Column(Integer, nullable=True, doc="HTTP response code")
    response_time_ms = Column(
        Integer, nullable=True, doc="Response time in milliseconds"
    )

    # Context
    user_id = Column(
        String(36), nullable=True, index=True, doc="User ID who performed the activity"
    )
    ip_address = Column(String(45), nullable=True, doc="IP address of the client")
    referrer = Column(String(500), nullable=True, doc="HTTP referrer")

    # Data changes
    data_before = Column(JSON, nullable=True, doc="Data state before the activity")
    data_after = Column(JSON, nullable=True, doc="Data state after the activity")

    # Additional data
    activity_data = Column(JSON, nullable=True, doc="Additional activity data")
    activity_metadata = Column(JSON, nullable=True, doc=SESSION_METADATA_DOC)

    # Timing
    timestamp = Column(
        DateTime, nullable=False, index=True, doc="When the activity occurred"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<SessionActivity(session={self.session_id}, action={self.action})>"


class DeviceFingerprint(FullFeaturedBaseModel):
    """Device fingerprint model for tracking unique device characteristics."""

    __tablename__: str = "device_fingerprints"

    # Fingerprint identification
    fingerprint_hash = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique device fingerprint hash",
    )
    fingerprint_version = Column(
        String(10), nullable=False, default="1.0", doc="Fingerprint algorithm version"
    )

    # Device characteristics
    screen_resolution = Column(String(50), nullable=True, doc="Screen resolution")
    color_depth = Column(Integer, nullable=True, doc="Color depth")
    timezone_offset = Column(Integer, nullable=True, doc="Timezone offset in minutes")
    language = Column(String(10), nullable=True, doc="Browser language")
    plugins = Column(JSON, nullable=True, doc="Browser plugins")
    fonts = Column(JSON, nullable=True, doc="Available fonts")
    canvas_fingerprint = Column(
        String(255), nullable=True, doc="Canvas fingerprint hash"
    )
    webgl_fingerprint = Column(String(255), nullable=True, doc="WebGL fingerprint hash")

    # Browser information
    user__ = Column(Text, nullable=True, doc="User agent string")
    browser_name = Column(String(100), nullable=True, doc="Browser name")
    browser_version = Column(String(50), nullable=True, doc="Browser version")
    engine_name = Column(String(100), nullable=True, doc="Browser engine name")
    engine_version = Column(String(50), nullable=True, doc="Browser engine version")

    # Operating system
    os_name = Column(String(100), nullable=True, doc="Operating system name")
    os_version = Column(String(50), nullable=True, doc="Operating system version")
    platform = Column(String(100), nullable=True, doc="Platform information")

    # Device information
    device_type = Column(
        String(50), nullable=True, doc="Device type (desktop, mobile, tablet)"
    )
    device_vendor = Column(String(100), nullable=True, doc="Device vendor")
    device_model = Column(String(100), nullable=True, doc="Device model")

    # Usage tracking
    first_seen_at = Column(
        DateTime, nullable=False, index=True, doc="When fingerprint was first seen"
    )
    last_seen_at = Column(
        DateTime, nullable=True, index=True, doc="When fingerprint was last seen"
    )
    usage_count = Column(
        Integer, nullable=False, default=1, doc="Number of times fingerprint was seen"
    )
    unique_users = Column(
        Integer,
        nullable=False,
        default=1,
        doc="Number of unique users with this fingerprint",
    )

    # Risk assessment
    risk_score = Column(Integer, nullable=True, doc="Risk score for the device (0-100)")
    suspicious = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether device appears suspicious (yes, no)",
    )
    blocked = Column(
        String(20),
        nullable=False,
        default="no",
        doc="Whether device is blocked (yes, no)",
    )

    # Additional data
    raw_fingerprint = Column(JSON, nullable=True, doc="Raw fingerprint data")
    fingerprint_metadata = Column(JSON, nullable=True, doc=SESSION_METADATA_DOC)

    def __repr__(self) -> str:
        """String representation."""
        return f"<DeviceFingerprint(hash={self.fingerprint_hash[:8]}..., type={self.device_type})>"
