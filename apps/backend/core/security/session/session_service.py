from datetime import datetime
import any
import attr1
import attr2
import bool
import bot
import config
import current_device_data
import device_data
import dict
import exclude_session
import extend_lifetime
import float
import fp1
import fp2
import int
import ip_address
import isinstance
import kwargs
import len
import list
import min
import mobile
import reason
import remember_me
import secret_key
import self
import session
import set
import stored_fingerprint
import str
import tablet
import user_agent
import user_id
import weight
import x

"""Session management and security for ZETA AI.





This module provides comprehensive session management including:


- Secure session creation and validation


- Session timeout and cleanup


- Concurrent session limiting


- Device fingerprinting and tracking


- Session hijacking protection


"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class SessionStatus(str, Enum):
    """Session status values."""

    ACTIVE = "active"

    EXPIRED = "expired"

    TERMINATED = "terminated"

    SUSPENDED = "suspended"


class DeviceType(str, Enum):
    """Device types."""

    DESKTOP = "desktop"

    MOBILE = "mobile"

    TABLET = "tablet"

    BOT = "bot"

    UNKNOWN = "unknown"


class SessionTerminationReason(str, Enum):
    """Session termination reasons."""

    LOGOUT = "logout"

    TIMEOUT = "timeout"

    SECURITY_VIOLATION = "security_violation"

    CONCURRENT_LIMIT = "concurrent_limit"

    ADMIN_TERMINATION = "admin_termination"

    DEVICE_CHANGE = "device_change"


class DeviceFingerprint(BaseModel):
    """Device fingerprint for session tracking."""

    fingerprint_id: str = Field(default_factory=lambda: str(uuid4()))

    user_agent: str | None = None

    screen_resolution: str | None = None

    timezone: str | None = None

    language: str | None = None

    platform: str | None = None

    device_type: DeviceType = Field(default=DeviceType.UNKNOWN)

    ip_address: str | None = None

    fingerprint_hash: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    last_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))

    trust_score: float = Field(default=0.0, ge=0.0, le=1.0)


class SessionInfo(BaseModel):
    """Session information."""

    session_id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str | None = None

    device_fingerprint: DeviceFingerprint | None = None

    ip_address: str | None = None

    user_agent: str | None = None

    status: SessionStatus = Field(default=SessionStatus.ACTIVE)

    # Timestamps

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    last_activity: datetime = Field(default_factory=lambda: datetime.now(UTC))

    expires_at: datetime | None = None

    terminated_at: datetime | None = None

    # Security attributes

    csrf_token: str | None = None

    is_secure: bool = Field(default=False)

    is_authenticated: bool = Field(default=False)

    authentication_level: str = Field(default="none")  # none, basic, mfa

    # Session metadata

    metadata: dict[str, Any] = Field(default_factory=dict)

    permissions: set[str] = Field(default_factory=set)

    roles: set[str] = Field(default_factory=set)

    # Tracking

    login_count: int = Field(default=0)

    termination_reason: SessionTerminationReason | None = None


class SessionConfig(BaseModel):
    """Session configuration."""

    # Timeout settings (in seconds)

    idle_timeout: int = Field(default=1800)  # 30 minutes

    absolute_timeout: int = Field(default=28800)  # 8 hours

    remember_me_timeout: int = Field(default=2592000)  # 30 days

    # Security settings

    secure_cookies: bool = Field(default=True)

    httponly_cookies: bool = Field(default=True)

    samesite_strict: bool = Field(default=True)

    max_concurrent_sessions: int = Field(default=5)

    # Device fingerprinting

    enable_fingerprinting: bool = Field(default=True)

    fingerprint_change_threshold: float = Field(default=0.3)

    require_device_verification: bool = Field(default=False)

    # Session rotation

    rotate_on_auth: bool = Field(default=True)

    rotate_on_privilege_change: bool = Field(default=True)

    rotation_interval: int = Field(default=3600)  # 1 hour


class SessionManager:
    """Advanced session management system."""

    def __init__(
        self, config: SessionConfig | None = None, secret_key: str | None = None
    ):
        """Initialize session manager.





        Args:


            config: Session configuration


            secret_key: Secret key for session signing


        """

        self.config = config or SessionConfig()

        self.secret_key = secret_key or secrets.token_urlsafe(32)

        # Active sessions storage

        self._sessions: dict[str, SessionInfo] = {}

        self._user_sessions: dict[str, set[str]] = {}  # user_id -> session_ids

        self._device_fingerprints: dict[str, DeviceFingerprint] = {}

        # Security tracking

        self._suspicious_ips: set[str] = set()

        self._blocked_devices: set[str] = set()

    def create_session(
        self,
        user_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        device_data: dict[str, Any] | None = None,
        remember_me: bool = False,
    ) -> SessionInfo:
        """Create a new session.





        Args:


            user_id: User ID for authenticated sessions


            ip_address: Client IP address


            user_agent: Client user agent


            device_data: Device fingerprinting data


            remember_me: Whether to extend session lifetime





        Returns:


            Created session info


        """

        # Generate secure session ID

        session_id = self._generate_session_id()

        # Create device fingerprint if enabled

        device_fingerprint = None

        if self.config.enable_fingerprinting and device_data:
            device_fingerprint = self._create_device_fingerprint(
                device_data, ip_address
            )

        # Calculate expiration time

        if remember_me:
            expires_at = datetime.now(UTC) + timedelta(
                seconds=self.config.remember_me_timeout
            )

        else:
            expires_at = datetime.now(UTC) + timedelta(
                seconds=self.config.absolute_timeout
            )

        # Create session

        _ = SessionInfo(
            session_id=session_id,
            user_id=user_id,
            device_fingerprint=device_fingerprint,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            csrf_token=self._generate_csrf_token(),
            is_secure=True,
            is_authenticated=user_id is not None,
        )

        # Check concurrent session limits

        if user_id and self._check_concurrent_limit(user_id):
            self._enforce_concurrent_limit(user_id)

        # Store session

        self._sessions[session_id] = session

        if user_id:
            if user_id not in self._user_sessions:
                self._user_sessions[user_id] = set()

            self._user_sessions[user_id].add(session_id)

        return session

    def get_session(self, session_id: str) -> SessionInfo | None:
        """Get session by ID.





        Args:


            session_id: Session ID





        Returns:


            Session info if found and valid


        """

        _ = self._sessions.get(session_id)

        if not session:
            return None

        # Check if session is expired

        if self._is_session_expired(session):
            self.terminate_session(session_id, SessionTerminationReason.TIMEOUT)

            return None

        return session

    def validate_session(
        self,
        session_id: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        device_data: dict[str, Any] | None = None,
    ) -> bool:
        """Validate session and update activity.





        Args:


            session_id: Session ID to validate


            ip_address: Current IP address


            user_agent: Current user agent


            device_data: Current device data





        Returns:


            True if session is valid


        """

        _ = self.get_session(session_id)

        if not session:
            return False

        # Check IP address consistency

        if (
            ip_address
            and session.ip_address
            and ip_address != session.ip_address
            and ip_address in self._suspicious_ips
        ):
            # Log potential session hijacking
            self.terminate_session(
                session_id, SessionTerminationReason.SECURITY_VIOLATION
            )

            return False

        # Check device fingerprint if enabled

        if (
            self.config.enable_fingerprinting
            and device_data
            and session.device_fingerprint
            and not self._validate_device_fingerprint(
                session.device_fingerprint, device_data
            )
            and self.config.require_device_verification
        ):
            self.terminate_session(session_id, SessionTerminationReason.DEVICE_CHANGE)

            return False

        # Update session activity

        session.last_activity = datetime.now(UTC)

        session.ip_address = ip_address or session.ip_address

        session.user__ = user_agent or session.user_agent

        return True

    def terminate_session(
        self,
        session_id: str,
        reason: SessionTerminationReason = SessionTerminationReason.LOGOUT,
    ) -> bool:
        """Terminate a session.





        Args:


            session_id: Session ID to terminate


            reason: Termination reason





        Returns:


            True if session was terminated


        """

        _ = self._sessions.get(session_id)

        if not session:
            return False

        # Update session status

        session.status = SessionStatus.TERMINATED

        session.terminated_at = datetime.now(UTC)

        session.termination_reason = reason

        # Remove from active sessions

        del self._sessions[session_id]

        # Remove from user sessions

        if session.user_id and session.user_id in self._user_sessions:
            self._user_sessions[session.user_id].discard(session_id)

            if not self._user_sessions[session.user_id]:
                del self._user_sessions[session.user_id]

        return True

    def terminate_user_sessions(
        self,
        user_id: str,
        exclude_session: str | None = None,
        reason: SessionTerminationReason = SessionTerminationReason.ADMIN_TERMINATION,
    ) -> int:
        """Terminate all sessions for a user.





        Args:


            user_id: User ID


            exclude_session: Session ID to exclude from termination


            reason: Termination reason





        Returns:


            Number of sessions terminated


        """

        if user_id not in self._user_sessions:
            return 0

        session_ids = list(self._user_sessions[user_id])

        terminated_count = 0

        for session_id in session_ids:
            if session_id != exclude_session and self.terminate_session(
                session_id, reason
            ):
                terminated_count += 1

        return terminated_count

    def refresh_session(self, session_id: str, extend_lifetime: bool = False) -> bool:
        """Refresh session to prevent timeout.





        Args:


            session_id: Session ID to refresh


            extend_lifetime: Whether to extend session lifetime





        Returns:


            True if session was refreshed


        """

        _ = self.get_session(session_id)

        if not session:
            return False

        session.last_activity = datetime.now(UTC)

        if extend_lifetime and session.expires_at:
            session.expires_at = datetime.now(UTC) + timedelta(
                seconds=self.config.absolute_timeout
            )

        return True

    def get_user_sessions(self, user_id: str) -> list[SessionInfo]:
        """Get all active sessions for a user.





        Args:


            user_id: User ID





        Returns:


            List of active sessions


        """

        if user_id not in self._user_sessions:
            return []

        sessions = []

        for session_id in self._user_sessions[user_id]:
            _ = self.get_session(session_id)

            if session:
                sessions.append(session)

        return sessions

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions.





        Returns:


            Number of sessions cleaned up


        """

        expired_sessions = []

        for session_id, session in self._sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            self.terminate_session(session_id, SessionTerminationReason.TIMEOUT)

        return len(expired_sessions)

    def _generate_session_id(self) -> str:
        """Generate secure session ID."""

        # Generate cryptographically secure random session ID

        random_bytes = secrets.token_bytes(32)

        # Add timestamp for uniqueness

        timestamp = str(datetime.now(UTC).timestamp())

        # Create HMAC signature

        signature = hmac.new(
            self.secret_key.encode(), random_bytes + timestamp.encode(), hashlib.sha256
        ).hexdigest()

        return f"{secrets.token_urlsafe(32)}_{signature[:16]}"

    def _generate_csrf_token(self) -> str:
        """Generate CSRF token."""

        return secrets.token_urlsafe(32)

    def _create_device_fingerprint(
        self, device_data: dict[str, Any], ip_address: str | None
    ) -> DeviceFingerprint:
        """Create device fingerprint from device data.





        Args:


            device_data: Device data dictionary


            ip_address: IP address





        Returns:


            Device fingerprint


        """

        # Extract device information

        device_data.get("user_agent")

        screen_resolution = device_data.get("screen_resolution")

        timezone = device_data.get("timezone")

        language = device_data.get("language")

        platform = device_data.get("platform")

        # Determine device type

        device_type = self._detect_device_type(user_agent)

        # Create fingerprint hash

        fingerprint_data = (
            f"{user_agent}:{screen_resolution}:{timezone}:{language}:{platform}"
        )

        fingerprint_hash = hashlib.sha256(fingerprint_data.encode()).hexdigest()

        # Check if we've seen this device before

        existing_fingerprint = self._device_fingerprints.get(fingerprint_hash)

        if existing_fingerprint:
            existing_fingerprint.last_seen = datetime.now(UTC)

            existing_fingerprint.trust_score = min(
                1.0, existing_fingerprint.trust_score + 0.1
            )

            return existing_fingerprint

        # Create new fingerprint

        fingerprint = DeviceFingerprint(
            user_agent=user_agent,
            screen_resolution=screen_resolution,
            timezone=timezone,
            language=language,
            platform=platform,
            device_type=device_type,
            ip_address=ip_address,
            fingerprint_hash=fingerprint_hash,
            trust_score=0.5,  # Start with neutral trust
        )

        self._device_fingerprints[fingerprint_hash] = fingerprint

        return fingerprint

    def _detect_device_type(self, user_agent: str | None) -> DeviceType:
        """Detect device type from user agent.





        Args:


            user_agent: User agent string





        Returns:


            Detected device type


        """

        if not user_agent:
            return DeviceType.UNKNOWN

        user_agent_lower = user_agent.lower()

        if any(
            mobile in user_agent_lower for mobile in ["mobile", "android", "iphone"]
        ):
            return DeviceType.MOBILE

        elif any(tablet in user_agent_lower for tablet in ["tablet", "ipad"]):
            return DeviceType.TABLET

        elif any(bot in user_agent_lower for bot in ["bot", "crawler", "spider"]):
            return DeviceType.BOT

        else:
            return DeviceType.DESKTOP

    def _validate_device_fingerprint(
        self, stored_fingerprint: DeviceFingerprint, current_device_data: dict[str, Any]
    ) -> bool:
        """Validate device fingerprint against current device data.





        Args:


            stored_fingerprint: Stored device fingerprint


            current_device_data: Current device data





        Returns:


            True if fingerprint is valid


        """

        # Create temporary fingerprint for comparison

        temp_fingerprint = self._create_device_fingerprint(
            current_device_data, stored_fingerprint.ip_address
        )

        # Calculate similarity score

        similarity = self._calculate_fingerprint_similarity(
            stored_fingerprint, temp_fingerprint
        )

        # Check if similarity is above threshold

        return similarity >= (1.0 - self.config.fingerprint_change_threshold)

    def _calculate_fingerprint_similarity(
        self, fp1: DeviceFingerprint, fp2: DeviceFingerprint
    ) -> float:
        """Calculate similarity between two device fingerprints.





        Args:


            fp1: First fingerprint


            fp2: Second fingerprint





        Returns:


            Similarity score (0.0 to 1.0)


        """

        score = 0.0

        total_weight = 0.0

        # Compare attributes with different weights

        comparisons = [
            (fp1.user_agent, fp2.user_agent, 0.3),
            (fp1.screen_resolution, fp2.screen_resolution, 0.2),
            (fp1.timezone, fp2.timezone, 0.15),
            (fp1.language, fp2.language, 0.15),
            (fp1.platform, fp2.platform, 0.2),
        ]

        for attr1, attr2, weight in comparisons:
            total_weight += weight

            if attr1 == attr2:
                score += weight

            elif attr1 and attr2 and isinstance(attr1, str) and isinstance(attr2, str):
                # Partial match for some attributes
                common_chars = len(set(attr1.lower()) & set(attr2.lower()))

                total_chars = len(set(attr1.lower()) | set(attr2.lower()))

                if total_chars > 0:
                    partial_score = common_chars / total_chars

                    score += weight * partial_score

        return score / total_weight if total_weight > 0 else 0.0

    def _is_session_expired(self, session: SessionInfo) -> bool:
        """Check if session is expired.

        Args:
            session: Session to check.

        Returns:
            True if the session is expired, otherwise False.
        """

        current_time = datetime.now(UTC)

        # Check absolute timeout
        if session.expires_at and current_time > session.expires_at:
            return True

        # Check idle timeout
        idle_limit = session.last_activity + timedelta(seconds=self.config.idle_timeout)
        return current_time > idle_limit

    def _check_concurrent_limit(self, user_id: str) -> bool:
        """Check if user has reached concurrent session limit.





        Args:


            user_id: User ID to check





        Returns:


            True if limit is reached


        """

        if user_id not in self._user_sessions:
            return False

        active_count = len(self._user_sessions[user_id])

        return active_count >= self.config.max_concurrent_sessions

    def _enforce_concurrent_limit(self, user_id: str) -> None:
        """Enforce concurrent session limit by terminating oldest sessions.





        Args:


            user_id: User ID to enforce limit for


        """

        if user_id not in self._user_sessions:
            return

        session_ids = list(self._user_sessions[user_id])

        # Get sessions with timestamps

        sessions_with_time = []

        for session_id in session_ids:
            _ = self._sessions.get(session_id)

            if session:
                sessions_with_time.append((session_id, session.created_at))

        # Sort by creation time (oldest first)

        sessions_with_time.sort(key=lambda x: x[1])

        # Terminate oldest sessions to make room

        while len(sessions_with_time) >= self.config.max_concurrent_sessions:
            oldest_session_id = sessions_with_time.pop(0)[0]

            self.terminate_session(
                oldest_session_id, SessionTerminationReason.CONCURRENT_LIMIT
            )


# Factory functions


def create_session_manager(
    config: SessionConfig | None = None, secret_key: str | None = None
) -> SessionManager:
    """Create session manager instance.





    Args:


        config: Session configuration


        secret_key: Secret key





    Returns:


        SessionManager instance


    """

    return SessionManager(config, secret_key)


def create_session_config(**kwargs) -> SessionConfig:
    """Create session configuration.





    Args:


        **kwargs: Configuration parameters





    Returns:


        Session configuration


    """

    return SessionConfig(**kwargs)
