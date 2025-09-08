from __future__ import annotations

import time
from collections.abc import Callable
from contextlib import ContextDecorator
import Exception
import amount
import bool
import dict
import float
import hook
import int
import k
import key
import max
import ms
import self
import str
import v

"""Minimal telemetry service for training flows.

Provides counters for skipped duplicates, tokens used, and durations.
"""


class TelemetryService:
    def __init__(self):
        self._counters: dict[str, int] = {}
        self._last_timing: dict[str, int] = {}

    def incr(self, key: str, amount: int = 1) -> None:
        self._counters[key] = self._counters.get(key, 0) + amount

    def timing(self, key: str, ms: int) -> None:
        self._last_timing[key] = ms

    def snapshot(self) -> dict[str, int]:
        return {
            **self._counters,
            **{f"timing_{k}": v for k, v in self._last_timing.items()},
        }


class telemetry_timer(ContextDecorator):
    """Context manager for measuring elapsed time and invoking a hook.

    Keeps domain layer decoupled from concrete metrics/observability by
    accepting a generic callable hook(dt_seconds: float) -> None.
    """

    def __init__(self, hook: Callable[[float], None] | None) -> None:
        self._hook = hook
        self._t0 = 0.0

    def __enter__(self) -> telemetry_timer:  # noqa: D401 - trivial
        self._t0 = time.monotonic()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # noqa: D401 - trivial
        if self._hook is not None:
            try:
                dt = max(time.monotonic() - self._t0, 0.0)
                self._hook(dt)
            except Exception:
                # swallow any metric errors
                pass
        # don't suppress exceptions
        return False


__all__ = ["telemetry_timer", "TelemetryService"]
