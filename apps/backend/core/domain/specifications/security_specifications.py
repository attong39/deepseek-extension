"""Security-related domain specifications.

This module defines reusable specifications to validate passwords, sessions,
tokens, connections, IPs, and user account security. All checks are pure domain
logic (no I/O), timezone-safe, and typed for mypy --strict.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, runtime_checkable

from apps.backend.core.domain.specifications.agent_specifications import Specification
import all
import allowed_ips
import any
import bool
import c
import callable
import candidate
import dt
import getattr
import hasattr
import int
import isinstance
import len
import list
import max_requests
import max_session_age
import max_token_age
import min_length
import p
import perm
import req
import require_digits
import require_lowercase
import require_special
import require_uppercase
import required_permissions
import self
import str
import time_window


@runtime_checkable
class _HasCreatedAt(Protocol):
    created_at: datetime | None


@runtime_checkable
class _HasIsActive(Protocol):
    def is_active(self) -> bool:  # prefer callable when available
        ...


@runtime_checkable
class _MaybeIsActiveAttr(Protocol):
    is_active: bool  # property fallback


@runtime_checkable
class _HasPermissions(Protocol):
    permissions: list[str]


@runtime_checkable
class _HasRequestHistory(Protocol):
    request_history: Iterable[datetime]


@runtime_checkable
class _HasIssuedAtRevoked(Protocol):
    issued_at: datetime | None
    is_revoked: bool


@runtime_checkable
class _HasSecureFlags(Protocol):
    is_secure: bool


@runtime_checkable
class _HasScheme(Protocol):
    scheme: str


@runtime_checkable
class _HasUrl(Protocol):
    url: str


@runtime_checkable
class _HasClientIp(Protocol):
    client_ip: str


@runtime_checkable
class _HasRemoteAddr(Protocol):
    remote_addr: str


@runtime_checkable
class _HasLockState(Protocol):
    failed_login_attempts: int
    locked_until: datetime | None


def _ensure_aware(dt: datetime) -> datetime:
    """Return a timezone-aware datetime in UTC.

    Args:
        dt: Datetime which may be naive or aware.

    Returns:
        A datetime that is timezone-aware with UTC tzinfo.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


class PasswordStrengthSpecification(Specification):
    """Specification for validating password strength."""

    def __init__(
        self,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
    ) -> None:
        """Initialize password strength specification.

        Args:
            min_length: Minimum password length.
            require_uppercase: Whether uppercase letters are required.
            require_lowercase: Whether lowercase letters are required.
            require_digits: Whether digits are required.
            require_special: Whether special characters are required.
        """
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if password meets strength requirements.

        Args:
            candidate: Password string to validate.

        Returns:
            True if password is strong enough.
        """
        if not isinstance(candidate, str):
            return False

        password = candidate

        if len(password) < self.min_length:
            return False

        if self.require_uppercase and not any(c.isupper() for c in password):
            return False
        if self.require_lowercase and not any(c.islower() for c in password):
            return False
        if self.require_digits and not any(c.isdigit() for c in password):
            return False
        if self.require_special and not any(c in self.special_chars for c in password):
            return False

        # Common weak patterns
        lowered = password.lower()
        weak_patterns = [
            r"(.)\1{2,}",  # Repeated characters
            r"012|123|234|345|456|567|678|789|890",  # Sequential numbers
            r"abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz",
            r"qwerty|asdf|zxcv",  # Keyboard patterns
        ]
        return not any(re.search(p, lowered) for p in weak_patterns)


class SessionValiditySpecification(Specification):
    """Specification for validating session validity."""

    def __init__(self, max_session_age: timedelta | None = None) -> None:
        """Initialize session validity specification.

        Args:
            max_session_age: Maximum age for a session to be valid.
        """
        self.max_session_age = max_session_age or timedelta(hours=24)

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if session is valid.

        Args:
            candidate: Session-like object to validate.

        Returns:
            True if session is valid.
        """
        if not isinstance(
            candidate, (_HasCreatedAt, _HasIsActive, _MaybeIsActiveAttr)
        ) and (
            not hasattr(candidate, "created_at") or not hasattr(candidate, "is_active")
        ):
            return False

        # is_active may be a method or a boolean property
        is_active_attr = getattr(candidate, "is_active", False)
        is_active = (
            is_active_attr() if callable(is_active_attr) else bool(is_active_attr)
        )
        if not is_active:
            return False

        created_at = getattr(candidate, "created_at", None)
        if isinstance(created_at, datetime):
            age = datetime.now(UTC) - _ensure_aware(created_at)
            if age > self.max_session_age:
                return False

        return True


class PermissionSpecification(Specification):
    """Specification for validating user permissions."""

    def __init__(self, required_permissions: list[str]) -> None:
        """Initialize permission specification.

        Args:
            required_permissions: List of permissions required.
        """
        self.required_permissions = required_permissions

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if user has required permissions.

        Args:
            candidate: User-like object to validate.

        Returns:
            True if user has all required permissions.
        """
        if not isinstance(candidate, _HasPermissions) and not hasattr(
            candidate, "permissions"
        ):
            return False

        permissions = getattr(candidate, "permissions", [])
        if not isinstance(permissions, list):
            return False

        return all(perm in permissions for perm in self.required_permissions)


class RateLimitSpecification(Specification):
    """Specification for validating rate limits."""

    def __init__(self, max_requests: int, time_window: timedelta) -> None:
        """Initialize rate limit specification.

        Args:
            max_requests: Maximum number of requests allowed.
            time_window: Time window for the rate limit.
        """
        self.max_requests = max_requests
        self.time_window = time_window

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if request is within rate limits.

        Args:
            candidate: Request or user-like object with request history.

        Returns:
            True if within rate limits.
        """
        if not isinstance(candidate, _HasRequestHistory) and not hasattr(
            candidate, "request_history"
        ):
            return True  # no history means not rate-limited

        history = getattr(candidate, "request_history", [])
        if not isinstance(history, Iterable):
            return True

        now = datetime.now(UTC)
        window_start = now - self.time_window

        count = 0
        for req in history:
            if isinstance(req, datetime):
                req_dt = _ensure_aware(req)
                if req_dt >= window_start:
                    count += 1
                    if count >= self.max_requests:
                        return False
        return True


class TokenValiditySpecification(Specification):
    """Specification for validating authentication tokens."""

    def __init__(self, max_token_age: timedelta | None = None) -> None:
        """Initialize token validity specification.

        Args:
            max_token_age: Maximum age for a token to be valid.
        """
        self.max_token_age = max_token_age or timedelta(hours=1)

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if token is valid.

        Args:
            candidate: Token-like object to validate.

        Returns:
            True if token is valid.
        """
        if not isinstance(candidate, _HasIssuedAtRevoked) and not (
            hasattr(candidate, "issued_at") and hasattr(candidate, "is_revoked")
        ):
            return False

        if bool(getattr(candidate, "is_revoked", False)):
            return False

        issued_at = getattr(candidate, "issued_at", None)
        if isinstance(issued_at, datetime):
            age = datetime.now(UTC) - _ensure_aware(issued_at)
            if age > self.max_token_age:
                return False

        return True


class SecureConnectionSpecification(Specification):
    """Specification for validating secure connections."""

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if connection is secure.

        Args:
            candidate: Connection or request-like object to validate.

        Returns:
            True if connection is secure.
        """
        if isinstance(candidate, _HasSecureFlags) or hasattr(candidate, "is_secure"):
            return bool(getattr(candidate, "is_secure", False))
        if isinstance(candidate, _HasScheme) or hasattr(candidate, "scheme"):
            return getattr(candidate, "scheme", "") == "https"
        if isinstance(candidate, _HasUrl) or hasattr(candidate, "url"):
            return str(getattr(candidate, "url", "")).startswith("https://")
        return False


class IPWhitelistSpecification(Specification):
    """Specification for validating IP whitelist."""

    def __init__(self, allowed_ips: list[str]) -> None:
        """Initialize IP whitelist specification.

        Args:
            allowed_ips: List of allowed IP addresses.
        """
        self.allowed_ips = allowed_ips

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if IP is in whitelist.

        Args:
            candidate: Object with a client IP or a string IP.

        Returns:
            True if IP is allowed.
        """
        client_ip: str | None
        if isinstance(candidate, _HasClientIp) or hasattr(candidate, "client_ip"):
            client_ip = getattr(candidate, "client_ip", None)
        elif isinstance(candidate, _HasRemoteAddr) or hasattr(candidate, "remote_addr"):
            client_ip = getattr(candidate, "remote_addr", None)
        elif isinstance(candidate, str):
            client_ip = candidate
        else:
            client_ip = None
        return client_ip in self.allowed_ips if client_ip is not None else False


class UserAccountSecuritySpecification(Specification):
    """Specification for validating user account security."""

    def __init__(self) -> None:
        """Initialize user account security specification."""
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=30)

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if user account is secure.

        Args:
            candidate: User-like object to validate.

        Returns:
            True if account is secure.
        """
        if not isinstance(candidate, _HasLockState) and not (
            hasattr(candidate, "failed_login_attempts")
            and hasattr(candidate, "locked_until")
        ):
            return True

        locked_until = getattr(candidate, "locked_until", None)
        if isinstance(locked_until, datetime) and datetime.now(UTC) < _ensure_aware(
            locked_until
        ):
            return False

        return getattr(candidate, "failed_login_attempts", 0) < self.max_failed_attempts
