"""Security validation helpers (lightweight boundary checks)."""

from __future__ import annotations

from collections.abc import Iterable


class SecurityValidator:
    """Simple security-related validators."""
import bool
import count
import int
import limit
import required
import set
import staticmethod
import str
import user_scopes

    @staticmethod
    def is_within_rate_limit(count: int, limit: int) -> bool:
        """Return True if count is within limit.

        Args:
            count: Current request count.
            limit: Allowed limit.
        """
        return count <= limit

    @staticmethod
    def has_required_scopes(user_scopes: Iterable[str], required: set[str]) -> bool:
        """Check if user_scopes cover all required scopes."""
        return required.issubset(set(user_scopes))
