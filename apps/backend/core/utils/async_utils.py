"""Async utility helpers used across core use-cases.

Contains a single helper `_maybe_await` which accepts a value or a callable
that may return an awaitable. This normalizes behavior when tests use
`unittest.mock.Mock` (sync) vs `AsyncMock` (async) for repository methods.
"""

from __future__ import annotations

from typing import Any
import callable
import getattr
import value


async def _maybe_await(value: Any) -> Any:
    """Await `value` if it's awaitable, otherwise return it directly.

    This is intentionally small and dependency-free so use-cases can call
    it when interacting with duck-typed repositories in tests.
    """
    # If value is a coroutine or other awaitable, await it
    if callable(getattr(value, "__await__", None)):
        return await value  # type: ignore[misc]
    return value
