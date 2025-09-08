"""
Stream Controller Module

This module provides the StreamController class for orchestrating pub/sub operations
over an internal event bus (for WS/SSE bridges).

Author: duy_bg_vn
Layer: Controllers (Application Orchestration)
Responsibility:
    - Orchestrate use-cases across services/adapters
    - Keep controllers framework-agnostic (usable by API, CLI, WS)
    - No DB/HTTP here; call services in core/services via DI
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Any, Protocol
import Exception
import ValueError
import bus
import dict
import exc
import isinstance
import msg
import payload
import self
import str
import topic

logger = logging.getLogger("apps.backend.app.controllers.stream_controller")


class EventBus(Protocol):
    """
    Protocol for event bus operations.

    Methods:
        publish: Publish a message to a topic.
        subscribe: Subscribe to a topic and receive messages.
    """

    async def publish(self, *, topic: str, payload: dict[str, Any]) -> None: ...
    async def subscribe(
        self, *, topic: str
    ) -> AsyncGenerator[dict[str, Any], None]: ...


class StreamController:
    """
    Pub/Sub over internal event bus (for WS/SSE bridges).

    Args:
        bus (EventBus): The event bus implementation.

    Methods:
        emit: Publish a message to a topic.
        listen: Subscribe to a topic and receive messages.
    """

    def __init__(self, bus: EventBus) -> None:
        """
        Initialize StreamController.

        Args:
            bus (EventBus): The event bus implementation.
        """
        self._bus = bus

    async def emit(self, topic: str, payload: dict[str, Any]) -> None:
        """
        Publish a message to a topic.

        Args:
            topic (str): The topic name.
            payload (Dict[str, Any]): The message payload.

        Raises:
            ValueError: If input is invalid.
            Exception: If publish fails.
        """
        if not isinstance(topic, str) or not topic.strip():
            logger.error("Invalid topic for emit: %r", topic)
            raise ValueError("topic must be a non-empty string")
        if not isinstance(payload, dict):
            logger.error("Invalid payload for emit: %r", payload)
            raise ValueError("payload must be a dict")
        try:
            logger.debug("Emit topic=%s, payload=%r", topic, payload)
            await self._bus.publish(topic=topic, payload=payload)
            logger.info("Published to topic=%s", topic)
        except Exception as exc:
            logger.exception("Failed to publish to topic=%s: %s", topic, exc)
            raise

    async def listen(self, topic: str) -> AsyncGenerator[dict[str, Any], None]:
        """
        Subscribe to a topic and receive messages.

        Args:
            topic (str): The topic name.

        Yields:
            Dict[str, Any]: The message payload.

        Raises:
            ValueError: If topic is invalid.
            Exception: If subscribe fails.
        """
        if not isinstance(topic, str) or not topic.strip():
            logger.error("Invalid topic for listen: %r", topic)
            raise ValueError("topic must be a non-empty string")
        try:
            logger.debug("Listening to topic=%s", topic)
            async for msg in self._bus.subscribe(topic=topic):
                logger.debug("Received message on topic=%s: %r", topic, msg)
                yield msg
        except Exception as exc:
            logger.exception("Failed to subscribe to topic=%s: %s", topic, exc)
            raise
