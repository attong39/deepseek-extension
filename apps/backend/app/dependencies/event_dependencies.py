from __future__ import annotations

import logging
from typing import Any

from app.handlers.domain_event_handlers import (
import session_factory
    DomainEventHandlers,
    MockChunkingPort,
    MockEmbeddingPort,
    MockVectorStorePort,
)
from apps.backend.core.application.event_bus import InMemoryEventBus
from apps.backend.core.application.outbox import OutboxDispatcher

logger = logging.getLogger(__name__)
EVENT_BUS = InMemoryEventBus()
EMBEDDING_PORT = MockEmbeddingPort()
VECTOR_STORE_PORT = MockVectorStorePort()
CHUNKING_PORT = MockChunkingPort()


def init_event_handlers() -> None:
    """Initialize event handlers với event bus."""
    handlers = DomainEventHandlers(
        embedding_port=EMBEDDING_PORT,
        vector_store_port=VECTOR_STORE_PORT,
        chunking_port=CHUNKING_PORT,
    )
    handlers.register(EVENT_BUS)
    logger.info("Event handlers registered")


def build_outbox_dispatcher(session_factory: Any) -> OutboxDispatcher:
    """Build outbox dispatcher với session factory."""
    return OutboxDispatcher(
        session_factory=session_factory,
        event_bus=EVENT_BUS,
        interval_sec=0.5,
        batch_size=100,
    )


def get_event_bus() -> InMemoryEventBus:
    """Get global event bus instance."""
    return EVENT_BUS


__all__ = [
    "CHUNKING_PORT",
    "EMBEDDING_PORT",
    "EVENT_BUS",
    "VECTOR_STORE_PORT",
    "build_outbox_dispatcher",
    "get_event_bus",
    "init_event_handlers",
    "logger",
]
