"""Domain event handlers với idempotency và production features."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from app.handlers.idempotency import idempotent
from app.monitoring.metrics import METRICS
from apps.backend.core.application.event_bus import EventBus
from apps.backend.core.domain.domain_events import DomainEvent
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class DomainEventHandlers:
    """Production-ready domain event handlers với idempotency."""
import Exception
import chunking_service
import dict
import e
import embedding_service
import event
import event_bus
import float
import getattr
import hasattr
import i
import len
import list
import range
import self
import session_getter
import str
import text
import vector_store

    def __init__(
        self,
        embedding_service: Any,  # Port
        vector_store: Any,  # Port
        chunking_service: Any,  # Port
        session_getter: Callable[[], AsyncSession],
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.chunking_service = chunking_service
        self.session_getter = session_getter

    def register_handlers(self, event_bus: EventBus) -> None:
        """Register all domain event handlers với event bus."""
        # Memory processing handlers
        event_bus.subscribe("MemoryChunked", self.on_memory_chunked)
        event_bus.subscribe("MemoryIngested", self.on_memory_ingested)

        # Agent lifecycle handlers
        event_bus.subscribe("AgentCreated", self.on_agent_created)
        event_bus.subscribe("AgentActivated", self.on_agent_activated)

        logger.info("Registered domain event handlers")

    @idempotent(
        "memory_chunked_handler", session_getter=lambda: None
    )  # Will be bound at runtime
    async def on_memory_chunked(self, event: DomainEvent) -> None:
        """
        Handle memory chunked events - generate embeddings and store in vector DB.

        This handler is idempotent - if it fails partway through, it can be
        safely retried without duplicating work.
        """
        try:
            # Extract event data based on type
            if hasattr(event, "texts") and hasattr(event, "metadatas"):
                texts = event.texts
                metadatas = event.metadatas
                namespace = getattr(event, "namespace", "default")
                tenant_id = getattr(event, "tenant_id", "default")
            else:
                # Fallback to payload
                payload = getattr(event, "payload", {})
                texts = payload.get("texts", [])
                metadatas = payload.get("metadatas", [])
                namespace = payload.get("namespace", "default")
                tenant_id = payload.get("tenant_id", "default")

            if not texts:
                logger.warning(f"No texts found in memory chunked event {event.id}")
                return

            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} text chunks")
            vectors = await self.embedding_service.embed_texts(texts)

            # Store in vector database
            await self.vector_store.upsert_texts(
                tenant_id=tenant_id,
                namespace=namespace,
                texts=texts,
                vectors=vectors,
                metadatas=metadatas,
            )

            # Update metrics
            METRICS["memory_upserts"].inc(len(texts))
            METRICS["memory_chunks_processed"].inc(len(texts))

            logger.info(
                f"Successfully processed memory chunked event: {len(texts)} chunks"
            )

        except Exception as e:
            METRICS["memory_processing_errors"].inc()
            logger.error(f"Failed to process memory chunked event {event.id}: {e}")
            raise

    @idempotent(
        "memory_ingested_handler", session_getter=lambda: None
    )  # Will be bound at runtime
    async def on_memory_ingested(self, event: DomainEvent) -> None:
        """Handle memory ingested events - update metrics and trigger downstream processing."""
        try:
            payload = getattr(event, "payload", {})
            chunks_count = payload.get("chunks_count", 0)
            model = payload.get("model", "unknown")
            namespace = payload.get("namespace", "default")

            # Update metrics
            METRICS["memory_ingested_total"].inc()
            METRICS["memory_chunks_ingested"].inc(chunks_count)

            logger.info(
                f"Memory ingested: {chunks_count} chunks using {model} in {namespace}"
            )

        except Exception as e:
            logger.error(f"Failed to process memory ingested event {event.id}: {e}")
            raise

    @idempotent(
        "agent_created_handler", session_getter=lambda: None
    )  # Will be bound at runtime
    async def on_agent_created(self, event: DomainEvent) -> None:
        """Handle agent created events - setup initial agent state."""
        try:
            # Extract agent details
            if hasattr(event, "agent_id"):
                agent_id = event.agent_id
                name = getattr(event, "name", "Unknown Agent")
                model = getattr(event, "model", "unknown")
            else:
                payload = getattr(event, "payload", {})
                agent_id = payload.get("agent_id", event.aggregate_id)
                name = payload.get("name", "Unknown Agent")
                model = payload.get("model", "unknown")

            # Update metrics
            METRICS["agents_created"].inc()

            # Could trigger additional setup here:
            # - Create default memory namespace
            # - Initialize agent capabilities
            # - Send welcome message

            logger.info(f"Agent created: {name} (id={agent_id}, model={model})")

        except Exception as e:
            logger.error(f"Failed to process agent created event {event.id}: {e}")
            raise

    @idempotent(
        "agent_activated_handler", session_getter=lambda: None
    )  # Will be bound at runtime
    async def on_agent_activated(self, event: DomainEvent) -> None:
        """Handle agent activated events - enable agent capabilities."""
        try:
            # Extract agent details
            if hasattr(event, "agent_id"):
                agent_id = event.agent_id
                status = getattr(event, "status", "active")
            else:
                payload = getattr(event, "payload", {})
                agent_id = payload.get("agent_id", event.aggregate_id)
                status = payload.get("status", "active")

            # Update metrics
            METRICS["agents_activated"].inc()

            # Could trigger additional activation logic:
            # - Enable real-time processing
            # - Start background tasks
            # - Notify connected clients

            logger.info(f"Agent activated: {agent_id} (status={status})")

        except Exception as e:
            logger.error(f"Failed to process agent activated event {event.id}: {e}")
            raise


# Mock implementations for development
class MockEmbeddingService:
    """Mock embedding service cho development."""

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate mock embeddings."""
        return [[0.1, 0.2, 0.3] for _ in texts]


class MockVectorStore:
    """Mock vector store cho development."""

    async def upsert_texts(
        self,
        tenant_id: str,
        namespace: str,
        texts: list[str],
        vectors: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Mock upsert operation."""
        logger.info(f"Mock upsert: {len(texts)} texts to {tenant_id}/{namespace}")


class MockChunkingService:
    """Mock chunking service cho development."""

    async def chunk_text(self, text: str) -> list[str]:
        """Mock text chunking."""
        return [text[i : i + 100] for i in range(0, len(text), 100)]
