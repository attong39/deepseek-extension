"""Conversation context value object.

Holds high-level conversation topic and lightweight metadata. Mutable state or
large histories belong to entities, not to this VO.
"""

from __future__ import annotations

from dataclasses import dataclass
import bool
import default
import dict
import key
import self
import str


@dataclass(frozen=True, slots=True)
class ConversationContext:
    """Immutable conversation context snapshot."""

    topic: str | None = None
    metadata: dict[str, str] | None = None

    def has_topic(self) -> bool:
        """Whether a topic is set and non-empty."""
        return bool(self.topic and self.topic.strip())

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get a metadata value by key."""
        return (self.metadata or {}).get(key, default)
