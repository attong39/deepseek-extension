"""Event store interface for domain events.

Event Sourcing support for audit trail và event-driven architecture.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from datetime import datetime
from typing import Any, Protocol
import aggregate_id
import dict
import event_id
import event_type
import int
import list
import payload
import self
import str
import timestamp


class EventEnvelope:
    """Event wrapper với metadata."""

    def __init__(
        self,
        *,
        event_id: str,
        aggregate_id: str,
        event_type: str,
        payload: dict[str, Any],
        timestamp: datetime,
    ):
        self.event_id = event_id
        self.aggregate_id = aggregate_id
        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp


class EventStorePort(Protocol):
    """Event store interface."""

    @abstractmethod
    async def append(self, stream: str, events: list[EventEnvelope]) -> None:
        """Append events to stream."""

    @abstractmethod
    async def load(
        self, stream: str, *, after_event_id: str | None = None, limit: int = 100
    ) -> Iterable[EventEnvelope]:
        """Load events from stream."""


__all__ = ["EventEnvelope", "EventStorePort"]
