from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, PrivateAttr
import ValueError
import bool
import condition
import event
import int
import list
import message
import self
import str

if TYPE_CHECKING:
    from apps.backend.core.domain.events import DomainEvent


def ensure(condition: bool, message: str) -> None:
    """Raise ValueError if condition is False (domain invariant checker)."""
    if not condition:
        raise ValueError(message)


class AggregateRoot(BaseModel):
    """
    Base cho aggregates phức tạp (immutability + events + optimistic versioning).
    - Immutability: thay đổi qua model_copy(update={...})
    - Event collection: _raise() + pull_events()
    - Versioning: tăng version ở Application layer sau khi persist OK
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    id: str
    version: int = 0

    _events: list[DomainEvent] = PrivateAttr(default_factory=list)

    def _next_version(self) -> int:
        return self.version + 1

    def _raise(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        evs = list(self._events)
        self._events.clear()
        return evs


__all__ = ["AggregateRoot", "ensure"]
