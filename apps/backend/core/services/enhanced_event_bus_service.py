"""
Enhanced Event Bus Service với real-time messaging.

Features:
- Async event publishing/subscribing
- Redis Streams for persistence
- WebSocket broadcasting
- Event filtering & routing
- Dead letter queues
- Performance monitoring
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4
from weakref import WeakSet
import Exception
import ImportError
import ValueError
import bool
import callback
import correlation_id
import data
import details
import dict
import e
import end_time
import error
import event_type
import event_types
import expected_value
import fields
import float
import handler
import hasattr
import int
import key
import len
import limit
import list
import max
import max_stream_length
import metadata
import metric_name
import model_id
import redis_url
import self
import session_id
import source
import str
import stream_name
import sum
import tags
import task_type
import tuple
import unit
import user_id
import value
import websocket
import ws

logger = logging.getLogger(__name__)

# Optional dependencies
try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False

try:
    import websockets

    WEBSOCKETS_AVAILABLE = True
except ImportError:
    websockets = None
    WEBSOCKETS_AVAILABLE = False


class EventType(Enum):
    """Types of events."""

    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"

    # AI events
    MODEL_SELECTED = "ai.model.selected"
    INFERENCE_STARTED = "ai.inference.started"
    INFERENCE_COMPLETED = "ai.inference.completed"
    INFERENCE_FAILED = "ai.inference.failed"

    # RAG events
    DOCUMENT_INDEXED = "rag.document.indexed"
    QUERY_EXECUTED = "rag.query.executed"
    CHUNK_PROCESSED = "rag.chunk.processed"

    # Knowledge Graph events
    NODE_ADDED = "kg.node.added"
    EDGE_ADDED = "kg.edge.added"
    GRAPH_UPDATED = "kg.graph.updated"

    # ASR events
    TRANSCRIPTION_STARTED = "asr.transcription.started"
    TRANSCRIPTION_COMPLETED = "asr.transcription.completed"

    # User events
    USER_ACTION = "user.action"
    USER_FEEDBACK = "user.feedback"

    # Performance events
    PERFORMANCE_METRIC = "performance.metric"
    HEALTH_CHECK = "health.check"

    # Custom events
    CUSTOM = "custom"


@dataclass
class Event:
    """Event data structure."""

    id: str = field(default_factory=lambda: str(uuid4()))
    type: EventType = EventType.CUSTOM
    source: str = ""
    timestamp: float = field(default_factory=time.time)
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: str | None = None
    user_id: str | None = None
    session_id: str | None = None


@dataclass
class EventSubscription:
    """Event subscription."""

    id: str
    event_types: list[EventType]
    callback: Callable[[Event], None]
    filters: dict[str, Any] = field(default_factory=dict)
    active: bool = True


@dataclass
class EventMetrics:
    """Event metrics."""

    total_published: int = 0
    total_processed: int = 0
    total_failed: int = 0
    avg_processing_time_ms: float = 0.0
    last_event_time: float = 0.0
    active_subscriptions: int = 0


class EnhancedEventBusService:
    """
    Enhanced Event Bus Service với real-time messaging.

    Features:
    - Async pub/sub pattern
    - Redis Streams persistence
    - WebSocket broadcasting
    - Event filtering
    - Dead letter handling
    - Performance monitoring
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        stream_name: str = "zeta_events",
        max_stream_length: int = 10000,
    ) -> None:
        """Initialize event bus service."""
        self.redis_url = redis_url
        self.stream_name = stream_name
        self.max_stream_length = max_stream_length

        # Redis connection
        self.redis: redis.Redis | None = None

        # In-memory subscriptions
        self.subscriptions: dict[str, EventSubscription] = {}
        self.event_handlers: dict[EventType, list[Callable[[Event], None]]] = {}

        # WebSocket connections
        self.websocket_connections: WeakSet[Any] = WeakSet()

        # Event queue for processing
        self.event_queue: list[Event] = []
        self.processing_events = False

        # Metrics
        self.metrics = EventMetrics()

        # Dead letter queue
        self.dead_letter_queue: list[tuple[Event, Exception]] = []
        self.max_dead_letters = 1000

    async def initialize(self) -> None:
        """Initialize event bus service."""
        # Initialize Redis
        if REDIS_AVAILABLE:
            try:
                self.redis = redis.from_url(self.redis_url)
                await self.redis.ping()
                logger.info("Connected to Redis for event persistence")

                # Create consumer group if needed
                try:
                    await self.redis.xgroup_create(
                        self.stream_name, "event_processors", id="0", mkstream=True
                    )
                except redis.ResponseError:
                    # Group already exists
                    pass

            except Exception as e:
                logger.warning(f"Redis connection failed: {e}")
                self.redis = None

        # Start event processing
        await self._start_event_processor()

    async def shutdown(self) -> None:
        """Shutdown event bus service."""
        # Process remaining events
        if self.event_queue:
            await self._process_event_queue()

        # Close Redis connection
        if self.redis:
            await self.redis.close()

    async def publish(
        self,
        event_type: EventType,
        data: dict[str, Any] | None = None,
        source: str = "",
        correlation_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Event:
        """
        Publish event to bus.

        Args:
            event_type: Type of event
            data: Event data
            source: Event source
            correlation_id: Correlation ID for tracing
            user_id: User ID
            session_id: Session ID
            metadata: Additional metadata

        Returns:
            Published event
        """
        event = Event(
            type=event_type,
            source=source,
            data=data or {},
            metadata=metadata or {},
            correlation_id=correlation_id,
            user_id=user_id,
            session_id=session_id,
        )

        # Add to processing queue
        self.event_queue.append(event)

        # Persist to Redis Stream
        await self._persist_event(event)

        # Broadcast to WebSocket connections
        await self._broadcast_to_websockets(event)

        # Update metrics
        self.metrics.total_published += 1
        self.metrics.last_event_time = time.time()

        logger.debug(f"Published event: {event_type.value} from {source}")
        return event

    async def subscribe(
        self,
        event_types: list[EventType],
        callback: Callable[[Event], None],
        filters: dict[str, Any] | None = None,
        subscription_id: str | None = None,
    ) -> str:
        """
        Subscribe to events.

        Args:
            event_types: List of event types to subscribe to
            callback: Callback function for events
            filters: Optional filters for events
            subscription_id: Optional custom subscription ID

        Returns:
            Subscription ID
        """
        subscription_id = subscription_id or str(uuid4())
        filters = filters or {}

        subscription = EventSubscription(
            id=subscription_id,
            event_types=event_types,
            callback=callback,
            filters=filters,
        )

        self.subscriptions[subscription_id] = subscription

        # Add to event handlers
        for event_type in event_types:
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
            self.event_handlers[event_type].append(callback)

        # Update metrics
        self.metrics.active_subscriptions = len(self.subscriptions)

        logger.info(
            f"Added subscription {subscription_id} for {len(event_types)} event types"
        )
        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.

        Args:
            subscription_id: Subscription ID to remove

        Returns:
            True if subscription was removed
        """
        if subscription_id not in self.subscriptions:
            return False

        subscription = self.subscriptions[subscription_id]

        # Remove from event handlers
        for event_type in subscription.event_types:
            if event_type in self.event_handlers:
                try:
                    self.event_handlers[event_type].remove(subscription.callback)
                    if not self.event_handlers[event_type]:
                        del self.event_handlers[event_type]
                except ValueError:
                    pass  # Callback not in list

        # Remove subscription
        del self.subscriptions[subscription_id]

        # Update metrics
        self.metrics.active_subscriptions = len(self.subscriptions)

        logger.info(f"Removed subscription {subscription_id}")
        return True

    async def add_websocket_connection(self, websocket: Any) -> None:
        """Add WebSocket connection for real-time events."""
        if WEBSOCKETS_AVAILABLE:
            self.websocket_connections.add(websocket)
            logger.info("Added WebSocket connection for real-time events")

    async def remove_websocket_connection(self, websocket: Any) -> None:
        """Remove WebSocket connection."""
        if websocket in self.websocket_connections:
            self.websocket_connections.discard(websocket)
            logger.info("Removed WebSocket connection")

    async def get_events_history(
        self,
        event_types: list[EventType] | None = None,
        start_time: float | None = None,
        end_time: float | None = None,
        limit: int = 100,
    ) -> list[Event]:
        """
        Get events history from Redis Stream.

        Args:
            event_types: Filter by event types
            start_time: Start timestamp
            end_time: End timestamp
            limit: Maximum number of events

        Returns:
            List of historical events
        """
        if not self.redis:
            return []

        try:
            # Read from Redis Stream
            events = []
            stream_entries = await self.redis.xrevrange(
                self.stream_name, max="+", min="-", count=limit
            )

            for _entry_id, fields in stream_entries:
                try:
                    event_data = json.loads(fields.get("data", "{}"))
                    event = Event(
                        id=event_data.get("id", ""),
                        type=EventType(event_data.get("type", "custom")),
                        source=event_data.get("source", ""),
                        timestamp=float(event_data.get("timestamp", 0)),
                        data=event_data.get("data", {}),
                        metadata=event_data.get("metadata", {}),
                        correlation_id=event_data.get("correlation_id"),
                        user_id=event_data.get("user_id"),
                        session_id=event_data.get("session_id"),
                    )

                    # Apply filters
                    if event_types and event.type not in event_types:
                        continue

                    if start_time and event.timestamp < start_time:
                        continue

                    if end_time and event.timestamp > end_time:
                        continue

                    events.append(event)

                except Exception as e:
                    logger.warning(f"Failed to parse event from stream: {e}")

            return events

        except Exception as e:
            logger.error(f"Failed to get events history: {e}")
            return []

    async def _start_event_processor(self) -> None:
        """Start background event processor."""
        if not self.processing_events:
            self.processing_events = True
            # In a real implementation, this would be a background task
            # For now, we'll process events synchronously when they're published

    async def _process_event_queue(self) -> None:
        """Process events in the queue."""
        while self.event_queue:
            event = self.event_queue.pop(0)
            await self._process_event(event)

    async def _process_event(self, event: Event) -> None:
        """Process a single event."""
        start_time = time.perf_counter()

        try:
            # Get handlers for this event type
            handlers = self.event_handlers.get(event.type, [])

            for handler in handlers:
                try:
                    # Check if this handler is from an active subscription
                    active_handler = False
                    for subscription in self.subscriptions.values():
                        if subscription.active and handler == subscription.callback:
                            # Apply filters
                            if self._event_matches_filters(event, subscription.filters):
                                active_handler = True
                                break

                    if active_handler:
                        # Call handler
                        if hasattr(handler, "__await__"):
                            await handler(event)
                        else:
                            handler(event)

                except Exception as e:
                    logger.error(f"Event handler failed for {event.type.value}: {e}")
                    self._add_to_dead_letter_queue(event, e)

            # Update metrics
            processing_time = (time.perf_counter() - start_time) * 1000
            self.metrics.total_processed += 1

            # Update average processing time
            if self.metrics.total_processed == 1:
                self.metrics.avg_processing_time_ms = processing_time
            else:
                alpha = 0.1  # Exponential moving average
                self.metrics.avg_processing_time_ms = (
                    alpha * processing_time
                    + (1 - alpha) * self.metrics.avg_processing_time_ms
                )

        except Exception as e:
            logger.error(f"Failed to process event {event.id}: {e}")
            self.metrics.total_failed += 1
            self._add_to_dead_letter_queue(event, e)

    def _event_matches_filters(self, event: Event, filters: dict[str, Any]) -> bool:
        """Check if event matches subscription filters."""
        if not filters:
            return True

        for key, expected_value in filters.items():
            if key == "source" and event.source != expected_value:
                return False
            elif key == "user_id" and event.user_id != expected_value:
                return False
            elif key == "session_id" and event.session_id != expected_value:
                return False
            elif key in event.data and event.data[key] != expected_value:
                return False
            elif key in event.metadata and event.metadata[key] != expected_value:
                return False

        return True

    async def _persist_event(self, event: Event) -> None:
        """Persist event to Redis Stream."""
        if not self.redis:
            return

        try:
            event_data = {
                "id": event.id,
                "type": event.type.value,
                "source": event.source,
                "timestamp": event.timestamp,
                "data": event.data,
                "metadata": event.metadata,
                "correlation_id": event.correlation_id,
                "user_id": event.user_id,
                "session_id": event.session_id,
            }

            await self.redis.xadd(
                self.stream_name,
                {"data": json.dumps(event_data)},
                maxlen=self.max_stream_length,
                approximate=True,
            )

        except Exception as e:
            logger.error(f"Failed to persist event {event.id}: {e}")

    async def _broadcast_to_websockets(self, event: Event) -> None:
        """Broadcast event to WebSocket connections."""
        if not self.websocket_connections or not WEBSOCKETS_AVAILABLE:
            return

        message = {
            "type": "event",
            "event": {
                "id": event.id,
                "type": event.type.value,
                "source": event.source,
                "timestamp": event.timestamp,
                "data": event.data,
                "metadata": event.metadata,
            },
        }

        # Send to all active connections
        disconnected_connections = []
        for ws in list(self.websocket_connections):
            try:
                await ws.send(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send WebSocket message: {e}")
                disconnected_connections.append(ws)

        # Remove disconnected connections
        for ws in disconnected_connections:
            self.websocket_connections.discard(ws)

    def _add_to_dead_letter_queue(self, event: Event, error: Exception) -> None:
        """Add failed event to dead letter queue."""
        if len(self.dead_letter_queue) >= self.max_dead_letters:
            self.dead_letter_queue.pop(0)  # Remove oldest

        self.dead_letter_queue.append((event, error))
        logger.warning(f"Added event {event.id} to dead letter queue: {error}")

    def get_metrics(self) -> dict[str, Any]:
        """Get event bus metrics."""
        return {
            "total_published": self.metrics.total_published,
            "total_processed": self.metrics.total_processed,
            "total_failed": self.metrics.total_failed,
            "success_rate": (
                (self.metrics.total_processed / max(self.metrics.total_published, 1))
                * 100
            ),
            "avg_processing_time_ms": self.metrics.avg_processing_time_ms,
            "active_subscriptions": self.metrics.active_subscriptions,
            "websocket_connections": len(self.websocket_connections),
            "queue_size": len(self.event_queue),
            "dead_letter_count": len(self.dead_letter_queue),
            "last_event_time": self.metrics.last_event_time,
            "event_handlers_count": sum(
                len(handlers) for handlers in self.event_handlers.values()
            ),
        }

    def get_dead_letter_events(self) -> list[tuple[Event, str]]:
        """Get events from dead letter queue."""
        return [(event, str(error)) for event, error in self.dead_letter_queue]

    def clear_dead_letter_queue(self) -> int:
        """Clear dead letter queue and return number of cleared events."""
        count = len(self.dead_letter_queue)
        self.dead_letter_queue.clear()
        return count

    async def replay_dead_letter_events(self) -> int:
        """Replay events from dead letter queue."""
        replayed = 0

        for event, error in list(self.dead_letter_queue):
            try:
                await self._process_event(event)
                self.dead_letter_queue.remove((event, error))
                replayed += 1
            except Exception as e:
                logger.error(f"Failed to replay event {event.id}: {e}")

        return replayed

    # Convenience methods for common events
    async def publish_system_event(
        self,
        event_type: EventType,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> Event:
        """Publish system event."""
        return await self.publish(
            event_type=event_type,
            data={"message": message, "details": details or {}},
            source="system",
        )

    async def publish_ai_event(
        self,
        event_type: EventType,
        model_id: str,
        task_type: str,
        details: dict[str, Any] | None = None,
        user_id: str | None = None,
    ) -> Event:
        """Publish AI-related event."""
        return await self.publish(
            event_type=event_type,
            data={
                "model_id": model_id,
                "task_type": task_type,
                "details": details or {},
            },
            source="ai_service",
            user_id=user_id,
        )

    async def publish_performance_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "ms",
        tags: dict[str, str] | None = None,
    ) -> Event:
        """Publish performance metric."""
        return await self.publish(
            event_type=EventType.PERFORMANCE_METRIC,
            data={
                "metric_name": metric_name,
                "value": value,
                "unit": unit,
                "tags": tags or {},
            },
            source="metrics",
        )


# Global event bus instance
_event_bus_instance: EnhancedEventBusService | None = None


def get_event_bus() -> EnhancedEventBusService:
    """Get global event bus instance."""
    global _event_bus_instance
    if _event_bus_instance is None:
        _event_bus_instance = EnhancedEventBusService()
    return _event_bus_instance


__all__ = [
    "EnhancedEventBusService",
    "Event",
    "EventType",
    "EventSubscription",
    "EventMetrics",
    "get_event_bus",
]
