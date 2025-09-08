"""Event bus for domain events with async handlers."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any, List, Protocol

from apps.backend.core.domain.domain_events import DomainEvent

# Project's standard logger
logger = logging.getLogger(__name__)

Handler = Callable[[DomainEvent], Awaitable[None]]


class EventBus(Protocol):
    """Protocol for event bus implementations.

    This protocol defines the interface for publishing and subscribing to domain events.
    """
import Exception
import TypeError
import ValueError
import callable
import dict
import e
import enumerate
import event
import events
import handler
import i
import int
import isinstance
import len
import list
import result
import self
import str

    async def publish(self, event: DomainEvent) -> None:
        """Publish a domain event to all subscribed handlers.

        Args:
            event: The domain event to publish.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        ...

    def subscribe(self, event_type: str, handler: Handler) -> None:
        """Subscribe a handler to a specific event type.

        Args:
            event_type: The type of event to subscribe to.
            handler: The async handler function to call when the event is published.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        ...


class InMemoryEventBus:
    """In-memory implementation of the EventBus protocol.

    This class provides a simple, in-memory event bus for handling domain events
    asynchronously. It supports subscribing handlers to event types and publishing
    events to trigger those handlers.

    Attributes:
        _handlers: A dictionary mapping event types to lists of handlers.
        _lock: An asyncio lock to ensure thread-safe access to handlers.
    """

    def __init__(self) -> None:
        """Initialize the InMemoryEventBus with empty handlers and a lock."""
        self._handlers: dict[str, List[Handler]] = {}
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: str, handler: Handler) -> None:
        """Subscribe a handler to a specific event type.

        Args:
            event_type: The type of event to subscribe to. Must be a non-empty string.
            handler: The async handler function. Must be callable and awaitable.

        Raises:
            ValueError: If event_type is empty or handler is not callable.
            TypeError: If handler does not match the expected signature.
        """
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type must be a non-empty string.")
        if not callable(handler):
            raise ValueError("handler must be callable.")
        # Additional check: Ensure handler is awaitable (basic check)
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError("handler must be an async function (coroutine).")

        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        logger.info(f"Subscribed handler to event type: {event_type}")

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to all registered handlers asynchronously.

        Args:
            event: The domain event to publish. Must be an instance of DomainEvent.

        Raises:
            ValueError: If event is not a valid DomainEvent instance.
        """
        if not isinstance(event, DomainEvent):
            raise ValueError("event must be an instance of DomainEvent.")

        event_type = event.event_type

        # Get handlers under lock for thread safety
        async with self._lock:
            handlers = self._handlers.get(event_type, []).copy()

        if not handlers:
            logger.debug(f"No handlers registered for event type: {event_type}")
            return

        # Execute handlers concurrently outside the lock to avoid deadlocks
        results = await asyncio.gather(
            *(self._safe_handler_call(handler, event) for handler in handlers),
            return_exceptions=True,
        )

        # Log any exceptions that occurred
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(
                    f"Handler {i} for event {event_type} failed: {result}",
                    exc_info=result,
                )

    async def _safe_handler_call(self, handler: Handler, event: DomainEvent) -> None:
        """Safely call a handler, catching and logging exceptions.

        Args:
            handler: The handler to call.
            event: The event to pass to the handler.
        """
        try:
            await handler(event)
        except Exception as e:
            logger.error(f"Error in handler for event {event.event_type}: {e}", exc_info=e)
            raise  # Re-raise to propagate to gather

    async def publish_many(self, events: List[DomainEvent]) -> None:
        """Publish multiple events concurrently.

        Args:
            events: A list of domain events to publish.

        Raises:
            ValueError: If events is not a list or contains invalid events.
        """
        if not isinstance(events, list):
            raise ValueError("events must be a list of DomainEvent instances.")
        for event in events:
            if not isinstance(event, DomainEvent):
                raise ValueError("All items in events must be DomainEvent instances.")

        await asyncio.gather(
            *(self.publish(event) for event in events),
            return_exceptions=True,
        )
        logger.info(f"Published {len(events)} events.")

    def get_handler_count(self, event_type: str) -> int:
        """Get the number of handlers registered for an event type.

        This method is primarily for testing purposes.

        Args:
            event_type: The event type to query.

        Returns:
            The number of handlers for the given event type.
        """
        return len(self._handlers.get(event_type, []))
