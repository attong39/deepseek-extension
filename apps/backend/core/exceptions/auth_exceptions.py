"""
Authentication and Authorization Exception Classes
Handles all security-related errors in ZETA AI Server
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
import Exception
import action
import dict
import error_code
import int
import kwargs
import limit
import metadata
import resource
import self
import str
import super
import user_id
import window

logger = logging.getLogger(__name__)


class BaseAuthError(Exception):
    """Base authentication/authorization error class."""

    def __init__(
        self,
        message: str,
        error_code: str,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.user_id = user_id
        self.metadata = metadata or {}
        self.timestamp = datetime.now(UTC)

        # Auto-log security events with structured context
        logger.warning(
            "Auth Error: %s - %s",
            error_code,
            message,
            extra={
                "user_id": user_id,
                "error_code": error_code,
                "metadata": self.metadata,
            },
        )

        super().__init__(message)


class AuthenticationError(BaseAuthError):
    """Raised when user authentication fails."""

    def __init__(self, message: str = "Authentication failed", **kwargs: Any) -> None:
        super().__init__(message, "AUTH_001", **kwargs)


class AuthorizationError(BaseAuthError):
    """Raised when user lacks required permissions."""

    def __init__(
        self, message: str = "Insufficient permissions", **kwargs: Any
    ) -> None:
        super().__init__(message, "AUTH_002", **kwargs)


class JWTTokenError(BaseAuthError):
    """Raised for JWT token-related errors."""

    def __init__(
        self, message: str = "Invalid or expired token", **kwargs: Any
    ) -> None:
        super().__init__(message, "AUTH_003", **kwargs)


class MFARequiredError(BaseAuthError):
    """Raised when Multi-Factor Authentication is required."""

    def __init__(
        self, message: str = "Multi-factor authentication required", **kwargs: Any
    ) -> None:
        super().__init__(message, "AUTH_004", **kwargs)


class SessionExpiredError(BaseAuthError):
    """Raised when user session has expired."""

    def __init__(self, message: str = "Session expired", **kwargs: Any) -> None:
        super().__init__(message, "AUTH_005", **kwargs)


class PermissionDeniedError(BaseAuthError):
    """Raised when access to resource is denied."""

    def __init__(self, resource: str, action: str, **kwargs: Any) -> None:
        message = f"Permission denied: {action} on {resource}"
        super().__init__(message, "AUTH_006", **kwargs)
        self.resource = resource
        self.action = action


class RateLimitExceededError(BaseAuthError):
    """Raised when rate limit is exceeded."""

    def __init__(self, limit: int, window: int, **kwargs: Any) -> None:
        message = f"Rate limit exceeded: {limit} requests per {window} seconds"
        super().__init__(message, "AUTH_007", **kwargs)
        self.limit = limit
        self.window = window


# Backward-compatibility aliases for existing names used elsewhere
class InvalidCredentialsError(AuthenticationError):
    """Legacy: Invalid user credentials provided."""

    def __init__(self, message: str = "Invalid credentials", **kwargs: Any) -> None:
        super().__init__(message=message, **kwargs)


class InvalidTokenError(JWTTokenError):
    """Legacy: Invalid or expired authentication token."""


class UserAlreadyExistsError(AuthenticationError):
    """Legacy: User with given identifier already exists."""


__all__ = [
    "BaseAuthError",
    "AuthenticationError",
    "AuthorizationError",
    "JWTTokenError",
    "MFARequiredError",
    "SessionExpiredError",
    "PermissionDeniedError",
    "RateLimitExceededError",
    # Legacy aliases
    "InvalidCredentialsError",
    "InvalidTokenError",
    "UserAlreadyExistsError",
]
