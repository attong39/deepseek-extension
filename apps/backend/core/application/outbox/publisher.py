from __future__ import annotations

import asyncio
import logging
from typing import Any, Protocol

from app.event_bus import EventBus
from app.outbox_hardened import OutboxRepository
import BaseException
import Exception
import batch_size
import dict
import e
import event
import event_bus
import events
import field
import float
import flush_interval
import getattr
import hasattr
import hash
import int
import isinstance
import len
import list
import outbox_repo
import self
import serializer
import str
import type

"""Event Publisher với advanced features."""
logger = logging.getLogger(__name__)


class EventSerializer(Protocol):
    """Protocol cho event serialization."""

    def serialize(self, event: Any) -> dict[str, Any]:
        """Serialize event thành dict."""
        ...

    def get_event_type(self, event: Any) -> str:
        """Get event type từ event object."""
        ...

    def get_partition_key(self, event: Any) -> int | None:
        """Get partition key từ event (optional)."""
        ...


class DefaultEventSerializer:
    """Default event serializer."""

    def serialize(self, event: Any) -> dict[str, Any]:
        """Serialize event using model_dump hoặc dict conversion."""
        if hasattr(event, "model_dump"):
            result = event.model_dump()
            return result if isinstance(result, dict) else {"data": result}
        elif hasattr(event, "__dict__"):
            result = event.__dict__
            return result if isinstance(result, dict) else {"data": result}
        else:
            return dict(event) if hasattr(event, "keys") else {"data": str(event)}

    def get_event_type(self, event: Any) -> str:
        """Get event type từ event."""
        if hasattr(event, "event_type"):
            result = event.event_type
            return str(result) if result is not None else "UnknownEvent"
        elif hasattr(event, "__class__"):
            result = event.__class__.__name__
            return str(result) if result else "UnknownEvent"
        else:
            return "UnknownEvent"

    def get_partition_key(self, event: Any) -> int | None:
        """Get partition key từ event."""
        for field in ["tenant_id", "user_id", "organization_id", "partition_key"]:
            if hasattr(event, field):
                value = getattr(event, field)
                if value is not None:
                    return hash(str(value)) % 16
        return None


class EventPublisher:
    """Advanced event publisher với batching và error handling."""

    def __init__(
        self,
        outbox_repo: OutboxRepository,
        event_bus: EventBus | None = None,
        serializer: EventSerializer | None = None,
        batch_size: int = 50,
        flush_interval: float = 1.0,
    ):
        """Initialize EventPublisher.
        Args:
            outbox_repo: Repository để lưu events
            event_bus: Optional event bus để publish immediately
            serializer: Event serializer (default: DefaultEventSerializer)
            batch_size: Kích thước batch trước khi flush
            flush_interval: Thời gian tối đa chờ trước khi flush
        """
        self.outbox_repo = outbox_repo
        self.event_bus = event_bus
        self.serializer = serializer or DefaultEventSerializer()
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._batch: list[Any] = []
        self._flush_timer: asyncio.Task[None] | None = None
        self._lock = asyncio.Lock()

    async def publish(self, event: Any) -> None:
        """Publish single event."""
        await self.publish_batch([event])

    async def publish_batch(self, events: list[Any]) -> None:
        """Publish batch of events."""
        async with self._lock:
            self._batch.extend(events)
            if len(self._batch) >= self.batch_size:
                await self._flush_batch()
            else:
                if self._flush_timer is None or self._flush_timer.done():
                    self._flush_timer = asyncio.create_task(self._delayed_flush())

    async def flush(self) -> None:
        """Force flush current batch."""
        async with self._lock:
            if self._batch:
                await self._flush_batch()
            if self._flush_timer and not self._flush_timer.done():
                self._flush_timer.cancel()
                try:
                    await self._flush_timer
                except asyncio.CancelledError:
                    logger.warning("Flush timer was cancelled")
                    raise

    async def _flush_batch(self) -> None:
        """Flush current batch to outbox."""
        if not self._batch:
            return
        batch = self._batch.copy()
        self._batch.clear()
        try:
            await self.outbox_repo.add_events(batch)
            if self.event_bus:
                await self.event_bus.publish_many(batch)
            logger.debug(f"Published batch of {len(batch)} events")
        except Exception as e:
            logger.error(f"Failed to publish batch: {e}")
            self._batch.extend(batch)
            raise

    async def _delayed_flush(self) -> None:
        """Delayed flush after timeout."""
        try:
            await asyncio.sleep(self.flush_interval)
            async with self._lock:
                if self._batch:
                    await self._flush_batch()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(f"Error in delayed flush: {e}")

    async def __aenter__(self) -> EventPublisher:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Async context manager exit - ensure flush."""
        await self.flush()


__all__ = [
    "DefaultEventSerializer",
    "EventPublisher",
    "EventSerializer",
    "batch",
    "get_event_type",
    "get_partition_key",
    "logger",
    "result",
    "serialize",
    "value",
]
