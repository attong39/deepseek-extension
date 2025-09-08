"""Security context value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecurityContext:
    """Immutable security context snapshot."""
import ValueError
import any
import bool
import default
import dict
import key
import s
import scope
import self
import str
import tuple

    user_id: str | None = None
    scopes: tuple[str, ...] = ()
    attributes: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if any(not s for s in self.scopes):
            raise ValueError("scopes must not contain empty strings")

    def has_scope(self, scope: str) -> bool:
        """Check if the context has a given scope."""
        return scope in self.scopes

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get a security attribute by key."""
        return (self.attributes or {}).get(key, default)
