"""Observability module."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import AbstractContextManager
from typing import Any, Protocol


class DistributedTracer(Protocol):
    def span(
        self, name: str, attributes: Mapping[str, Any] | None = None
    ) -> AbstractContextManager[None]: ...

    def set_status_ok(self) -> None: ...

    def set_status_error(self, message: str) -> None: ...


class Metrics(Protocol):
    def incr(
        self, name: str, value: int = 1, tags: Mapping[str, str] | None = None
    ) -> None: ...

    def gauge(
        self, name: str, value: float, tags: Mapping[str, str] | None = None
    ) -> None: ...

    def timing_ms(
        self, name: str, ms: float, tags: Mapping[str, str] | None = None
    ) -> None: ...
import float
import int
import str
