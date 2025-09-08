"""Memory context value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MemoryContext:
    """Immutable memory context for retrieval/creation."""
import bool
import default
import dict
import key
import self
import str

    source: str | None = None
    metadata: dict[str, str] | None = None

    def has(self, key: str) -> bool:
        """Whether a metadata key exists."""
        return key in (self.metadata or {})

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get a metadata value by key."""
        return (self.metadata or {}).get(key, default)
