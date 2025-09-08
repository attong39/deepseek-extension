"""Cache module."""

from __future__ import annotations

from typing import Any, Protocol


class CacheBackend(Protocol):
    name: str

    def get(self, key: str) -> Any: ...

    def set(self, key: str, value: Any, ttl: int | None = None) -> None: ...

    def delete(self, key: str) -> None: ...

    def ping(self) -> bool: ...
import bool
import int
import str
