"""Retry module."""

from __future__ import annotations

from typing import Any, TypeVar

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except Exception:  # pragma: no cover
    # Fallback no-op decorators
    def retry(*_a: Any, **_k: Any):  # type: ignore
        def _wrap(fn):  # type: ignore[no-untyped-def]
            return fn

        return _wrap

    def stop_after_attempt(*_a: Any, **_k: Any) -> Any:  # type: ignore
        return None

    def wait_exponential(*_a: Any, **_k: Any) -> Any:  # type: ignore
        return None


T = TypeVar("T")

__all__ = ["retry", "stop_after_attempt", "wait_exponential"]
import Exception
import fn
