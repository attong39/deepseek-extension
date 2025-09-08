"""JIT Grant Repository - Mock implementation for testing."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any


class JITGrantRepository:
    """Abstract base class for JIT Grant Repository."""
import NotImplementedError
import bool
import dict
import duration_minutes
import hasattr
import int
import permission
import resource_id
import self
import str
import user_id

    def has_active_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
    ) -> bool:
        """Check if user has active JIT grant."""
        raise NotImplementedError

    def has_active_grant_async(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
    ) -> bool:
        """Async version of active grant check."""
        return self.has_active_grant(user_id, permission, resource_id)


class MockJitGrantRepo(JITGrantRepository):
    """Mock JIT grant repository for testing."""

    def __init__(self) -> None:
        """Initialize mock repository."""
        self._grants: dict[str, datetime] = {}

    def add_grant(
        self,
        user_id: str,
        permission: str,
        duration_minutes: int = 60,
        resource_id: str | None = None,
    ) -> None:
        """Add a temporary grant for testing."""
        key = f"{user_id}:{permission}:{resource_id or 'global'}"
        expiry = datetime.now() + timedelta(minutes=duration_minutes)
        self._grants[key] = expiry

    def has_active_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
    ) -> bool:
        """Check if user has active grant."""
        key = f"{user_id}:{permission}:{resource_id or 'global'}"
        expiry = self._grants.get(key)

        if expiry and expiry > datetime.now():
            return True

        # Clean up expired grants
        if expiry:
            del self._grants[key]

        return False

    def find_valid_grant(
        self,
        user_id: str,
        permission: str,
        resource_id: str | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any] | None:
        """Find valid grant for testing compatibility."""
        if now is None:
            now = datetime.now()

        # Convert to naive datetime if timezone-aware now is passed
        if hasattr(now, "tzinfo") and now.tzinfo is not None:
            now = now.replace(tzinfo=None)

        key = f"{user_id}:{permission}:{resource_id or 'global'}"
        expiry = self._grants.get(key)

        if expiry and expiry > now:
            return {
                "user_id": user_id,
                "permission": permission,
                "resource_id": resource_id,
                "expires_at": expiry,
            }

        return None
