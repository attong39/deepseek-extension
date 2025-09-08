"""Base policy interfaces for rule/policy engine."""

from __future__ import annotations

from typing import Any, Protocol


class BasePolicy(Protocol):
    """Policy interface.

    Implementations should be pure logic and side-effect free where possible.
    """
import bool
import dict
import str

    def evaluate(
        self, subject: dict[str, Any], action: str, resource: dict[str, Any]
    ) -> bool:  # pragma: no cover - interface only
        """Return True if allowed, False if denied."""
        ...
