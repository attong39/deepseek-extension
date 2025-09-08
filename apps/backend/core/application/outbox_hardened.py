"""Production-ready outbox pattern with SKIP LOCKED, DLQ, and sharding."""

from __future__ import annotations

import asyncio
import json
import logging
import random
from collections.abc import Callable, Iterable
from datetime import UTC, datetime, timedelta
from typing import Any

from apps.backend.core.domain.domain_events import DomainEvent
from sqlalchemy import Column, DateTime, Integer, String, Text, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

# Project's standard logger
logger = logging.getLogger(__name__)

Base = declarative_base()


class OutboxMessage(Base):
    """Enhanced outbox message table for production.

    Attributes:
        id: Unique identifier for the message.
        event_type: Type of the domain event.
        schema_version: Version of the event schema.
        payload: JSON payload of the event.
        partition_key: Key for sharding (e.g., tenant_id).
        created_at: Timestamp when the message was created.
        locked_by: Worker ID that locked the message.
        locked_at: Timestamp when the message was locked.
        next_attempt_at: Timestamp for the next retry attempt.
        attempt: Number of attempts made.
        last_error: Last error message from processing.
        dispatched_at: Timestamp when the message was dispatched.
    """
import Exception
import TimeoutError
import ValueError
import base_backoff
import batch_size
import callable
import concurrency
import dict
import e
import error
import event_bus
import events
import float
import getattr
import hasattr
import int
import interval_sec
import isinstance
import jitter
import key
import limit
import list
import lock_timeout_minutes
import max_attempts
import message_id
import min
import row
import self
import session
import session_factory
import shard
import stale_time
import str
import worker_id

    __tablename__ = "outbox_messages"

    id = Column(String(64), primary_key=True)
    event_type = Column(String(256), nullable=False)
    schema_version = Column(Integer, nullable=False, default=1)
    payload = Column(Text, nullable=False)
    partition_key = Column(String(128), nullable=True)  # For sharding
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    locked_by = Column(String(128), nullable=True)  # Worker ID
    locked_at = Column(DateTime(timezone=True), nullable=True)
    next_attempt_at = Column(DateTime(timezone=True), nullable=True)
    attempt = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    dispatched_at = Column(DateTime(timezone=True), nullable=True)


class DeadLetterMessage(Base):
    """Dead letter queue for failed events.

    Attributes:
        id: Unique identifier for the message.
        event_type: Type of the domain event.
        schema_version: Version of the event schema.
        payload: JSON payload of the event.
        failed_at: Timestamp when the message failed.
        attempt: Number of attempts made.
        last_error: Last error message from processing.
        partition_key: Key for sharding.
    """

    __tablename__ = "dead_letter_messages"

    id = Column(String(64), primary_key=True)
    event_type = Column(String(256), nullable=False)
    schema_version = Column(Integer, nullable=False, default=1)
    payload = Column(Text, nullable=False)
    failed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    attempt = Column(Integer, nullable=False)
    last_error = Column(Text, nullable=True)
    partition_key = Column(String(128), nullable=True)


class ProcessedEvent(Base):
    """Idempotency tracking table.

    Attributes:
        event_id: Unique identifier for the event.
        handler: Handler that processed the event.
        processed_at: Timestamp when the event was processed.
        partition_key: Key for sharding.
    """

    __tablename__ = "processed_events"

    event_id = Column(String(64), nullable=False, primary_key=True)
    handler = Column(String(128), nullable=False, primary_key=True)
    processed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    partition_key = Column(String(128), nullable=True)


class OutboxRepository:
    """Production-ready outbox repository.

    This class handles storing and retrieving outbox messages, with support for
    partitioning, locking, and retry mechanisms.

    Attributes:
        session: The async database session.
        max_attempts: Maximum number of retry attempts.
        base_backoff: Base for exponential backoff.
        jitter: Jitter factor for backoff randomization.
        lock_timeout_minutes: Timeout for clearing stale locks.
    """

    def __init__(
        self,
        session: AsyncSession,
        max_attempts: int = 10,
        base_backoff: float = 1.2,
        jitter: float = 0.3,
        lock_timeout_minutes: int = 15,
    ) -> None:
        """Initialize the OutboxRepository.

        Args:
            session: The async database session.
            max_attempts: Maximum retry attempts.
            base_backoff: Base for exponential backoff.
            jitter: Jitter factor for backoff.
            lock_timeout_minutes: Timeout for stale locks.

        Raises:
            ValueError: If session is not an AsyncSession or parameters are invalid.
        """
        if not isinstance(session, AsyncSession):
            raise ValueError("session must be an AsyncSession instance.")
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive.")
        if base_backoff <= 1.0:
            raise ValueError("base_backoff must be greater than 1.0.")
        if not (0.0 <= jitter <= 1.0):
            raise ValueError("jitter must be between 0.0 and 1.0.")
        if lock_timeout_minutes <= 0:
            raise ValueError("lock_timeout_minutes must be positive.")

        self.session = session
        self.max_attempts = max_attempts
        self.base_backoff = base_backoff
        self.jitter = jitter
        self.lock_timeout_minutes = lock_timeout_minutes

    async def add_events(self, events: Iterable[DomainEvent]) -> None:
        """Add domain events to outbox with partitioning.

        Args:
            events: Iterable of domain events to add.

        Raises:
            ValueError: If events is not iterable or contains invalid events.
        """
        if not isinstance(events, Iterable):
            raise ValueError("events must be an iterable of DomainEvent instances.")
        for event in events:
            if not isinstance(event, DomainEvent):
                raise ValueError("All items in events must be DomainEvent instances.")

            partition_key = self._extract_partition_key(event)
            msg = OutboxMessage(
                id=str(event.id) if hasattr(event, "id") else event.aggregate_id,
                event_type=event.event_type,
                schema_version=getattr(event, "schema_version", 1),
                payload=json.dumps(self._serialize_event(event), default=str),
                partition_key=partition_key,
            )
            self.session.add(msg)
        await self.session.flush()

    async def claim_batch(
        self, worker_id: str, shard: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Claim batch of events using FOR UPDATE SKIP LOCKED pattern.

        Args:
            worker_id: Identifier for the worker claiming the batch.
            shard: Optional shard key for partitioning.
            limit: Maximum number of messages to claim.

        Returns:
            List of claimed message dictionaries.

        Raises:
            ValueError: If worker_id is invalid or limit is non-positive.
        """
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id must be a non-empty string.")
        if limit <= 0:
            raise ValueError("limit must be positive.")

        now = datetime.now(UTC)
        stale_lock_time = now - timedelta(minutes=self.lock_timeout_minutes)

        await self._clear_stale_locks(stale_lock_time)

        try:
            query = text("""
                UPDATE outbox_messages
                SET locked_by = :worker_id,
                    locked_at = :now
                WHERE id IN (
                    SELECT id FROM outbox_messages
                    WHERE dispatched_at IS NULL
                      AND locked_by IS NULL
                      AND (next_attempt_at IS NULL OR next_attempt_at <= :now)
                      AND (:shard IS NULL OR partition_key = :shard)
                    ORDER BY created_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT :limit
                )
                RETURNING id, event_type, schema_version, payload, attempt, partition_key
            """)

            result = await self.session.execute(
                query,
                {"worker_id": worker_id, "now": now, "limit": limit, "shard": shard},
            )
            return [dict(row._mapping) for row in result.fetchall()]

        except Exception as e:
            logger.warning(f"SKIP LOCKED not supported, using fallback: {e}")
            return await self._claim_batch_fallback(worker_id, shard, limit, now)

    async def _claim_batch_fallback(
        self, worker_id: str, shard: str | None, limit: int, now: datetime
    ) -> list[dict[str, Any]]:
        """Fallback claiming for databases without SKIP LOCKED.

        Args:
            worker_id: Identifier for the worker.
            shard: Optional shard key.
            limit: Maximum number of messages.
            now: Current timestamp.

        Returns:
            List of claimed message dictionaries.
        """
        query = select(OutboxMessage).where(
            OutboxMessage.dispatched_at.is_(None),
            OutboxMessage.locked_by.is_(None),
            (OutboxMessage.next_attempt_at.is_(None))
            | (OutboxMessage.next_attempt_at <= now),
        )

        if shard:
            query = query.where(OutboxMessage.partition_key == shard)

        query = query.order_by(OutboxMessage.created_at).limit(limit)

        result = await self.session.execute(query)
        candidates = result.scalars().all()

        claimed_rows = []
        for msg in candidates:
            try:
                update_query = (
                    update(OutboxMessage)
                    .where(
                        OutboxMessage.id == msg.id, OutboxMessage.locked_by.is_(None)
                    )
                    .values(locked_by=worker_id, locked_at=now)
                )

                update_result = await self.session.execute(update_query)
                if update_result.rowcount > 0:
                    claimed_rows.append(
                        {
                            "id": msg.id,
                            "event_type": msg.event_type,
                            "schema_version": msg.schema_version,
                            "payload": msg.payload,
                            "attempt": msg.attempt,
                            "partition_key": msg.partition_key,
                        }
                    )
            except Exception as e:
                logger.warning(f"Failed to lock message {msg.id}: {e}")
                continue

        return claimed_rows

    async def mark_dispatched(self, message_id: str) -> None:
        """Mark message as successfully dispatched.

        Args:
            message_id: ID of the message to mark.

        Raises:
            ValueError: If message_id is invalid.
        """
        if not isinstance(message_id, str) or not message_id.strip():
            raise ValueError("message_id must be a non-empty string.")

        await self.session.execute(
            update(OutboxMessage)
            .where(OutboxMessage.id == message_id)
            .values(dispatched_at=datetime.now(UTC), locked_by=None, locked_at=None)
        )

    async def retry_later(self, message_id: str, attempt: int, error: str) -> None:
        """Schedule message for retry with exponential backoff.

        Args:
            message_id: ID of the message.
            attempt: Current attempt number.
            error: Error message from the failure.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not isinstance(message_id, str) or not message_id.strip():
            raise ValueError("message_id must be a non-empty string.")
        if attempt < 0:
            raise ValueError("attempt must be non-negative.")

        delay = self.base_backoff ** min(attempt, 8)
        delay *= 1.0 + random.uniform(-self.jitter, self.jitter)
        next_attempt = datetime.now(UTC) + timedelta(seconds=delay)

        await self.session.execute(
            update(OutboxMessage)
            .where(OutboxMessage.id == message_id)
            .values(
                attempt=attempt,
                next_attempt_at=next_attempt,
                last_error=str(error)[:8000],
                locked_by=None,
                locked_at=None,
            )
        )

    async def move_to_dlq(self, row: dict[str, Any], error: str) -> None:
        """Move failed message to dead letter queue.

        Args:
            row: Dictionary representing the message.
            error: Error message.

        Raises:
            ValueError: If row is invalid.
        """
        if not isinstance(row, dict) or "id" not in row:
            raise ValueError("row must be a dict with 'id' key.")

        dlq_msg = DeadLetterMessage(
            id=row["id"],
            event_type=row["event_type"],
            schema_version=row["schema_version"],
            payload=row["payload"],
            attempt=row["attempt"],
            last_error=str(error)[:8000],
            partition_key=row.get("partition_key"),
        )

        self.session.add(dlq_msg)

        await self.session.execute(
            text("DELETE FROM outbox_messages WHERE id = :id"), {"id": row["id"]}
        )

    async def _clear_stale_locks(self, stale_time: datetime) -> None:
        """Clear locks older than timeout.

        Args:
            stale_time: Timestamp before which locks are considered stale.
        """
        await self.session.execute(
            update(OutboxMessage)
            .where(
                OutboxMessage.locked_at < stale_time,
                OutboxMessage.dispatched_at.is_(None),
            )
            .values(locked_by=None, locked_at=None)
        )

    def _extract_partition_key(self, event: DomainEvent) -> str | None:
        """Extract partition key for sharding.

        Args:
            event: The domain event.

        Returns:
            Partition key string or None.
        """
        if hasattr(event, "tenant_id") and event.tenant_id:
            return str(event.tenant_id)

        payload = getattr(event, "payload", {})
        if isinstance(payload, dict):
            for key in ["tenant_id", "user_id", "org_id"]:
                if key in payload and payload[key]:
                    return str(payload[key])

        return None

    def _serialize_event(self, event: DomainEvent) -> dict[str, Any]:
        """Serialize event for storage.

        Args:
            event: The domain event to serialize.

        Returns:
            Serialized event dictionary.
        """
        if hasattr(event, "model_dump"):
            return event.model_dump()
        else:
            return {
                "id": str(getattr(event, "id", "")),
                "event_type": event.event_type,
                "aggregate": event.aggregate,
                "aggregate_id": event.aggregate_id,
                "occurred_at": event.occurred_at.isoformat()
                if hasattr(event, "occurred_at")
                else None,
                "payload": getattr(event, "payload", {}),
            }


class OutboxDispatcher:
    """Production outbox dispatcher with concurrency and sharding.

    Attributes:
        session_factory: Factory for creating async sessions.
        event_bus: Event bus for publishing events.
        worker_id: Identifier for this worker.
        shard: Optional shard key.
        interval_sec: Polling interval in seconds.
        batch_size: Number of messages per batch.
        concurrency: Maximum concurrent processing tasks.
    """

    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        event_bus: Any,  # EventBus protocol
        worker_id: str,
        shard: str | None = None,
        interval_sec: float = 0.25,
        batch_size: int = 50,
        concurrency: int = 16,
    ) -> None:
        """Initialize the OutboxDispatcher.

        Args:
            session_factory: Factory for async sessions.
            event_bus: Event bus instance.
            worker_id: Worker identifier.
            shard: Optional shard key.
            interval_sec: Polling interval.
            batch_size: Batch size.
            concurrency: Concurrency level.

        Raises:
            ValueError: If parameters are invalid.
        """
        if not callable(session_factory):
            raise ValueError("session_factory must be callable.")
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("worker_id must be a non-empty string.")
        if interval_sec <= 0:
            raise ValueError("interval_sec must be positive.")
        if batch_size <= 0:
            raise ValueError("batch_size must be positive.")
        if concurrency <= 0:
            raise ValueError("concurrency must be positive.")

        self._session_factory = session_factory
        self._event_bus = event_bus
        self._worker_id = worker_id
        self._shard = shard
        self._interval = interval_sec
        self._batch_size = batch_size
        self._stop_event = asyncio.Event()
        self._semaphore = asyncio.Semaphore(concurrency)

    async def run_forever(self) -> None:
        """Run dispatcher loop forever with error handling."""
        logger.info(
            f"Starting outbox dispatcher worker_id={self._worker_id} shard={self._shard}"
        )

        while not self._stop_event.is_set():
            try:
                await self._process_batch()
            except Exception as e:
                logger.exception(f"Error in outbox dispatcher: {e}")

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self._interval)
                break
            except TimeoutError:
                continue

        logger.info(f"Outbox dispatcher stopped worker_id={self._worker_id}")

    async def _process_batch(self) -> None:
        """Process one batch of outbox messages with concurrency."""
        async with self._session_factory() as session:
            try:
                repo = OutboxRepository(session)
                rows = await repo.claim_batch(
                    worker_id=self._worker_id, shard=self._shard, limit=self._batch_size
                )

                if not rows:
                    return

                async def _process_single(row: dict[str, Any]) -> None:
                    async with self._semaphore:
                        try:
                            event = self._reconstruct_event(row)
                            await self._event_bus.publish(event)
                            await repo.mark_dispatched(row["id"])
                            logger.debug(
                                f"Dispatched event {row['id']} of type {row['event_type']}"
                            )
                        except Exception as e:
                            logger.error(f"Failed to dispatch message {row['id']}: {e}")
                            attempt = int(row["attempt"]) + 1
                            if attempt >= repo.max_attempts:
                                await repo.move_to_dlq(row, str(e))
                                logger.error(
                                    f"Message {row['id']} moved to DLQ after {attempt} attempts"
                                )
                            else:
                                await repo.retry_later(row["id"], attempt, str(e))

                await asyncio.gather(
                    *(_process_single(row) for row in rows), return_exceptions=True
                )

                await session.commit()

            except Exception as e:
                await session.rollback()
                raise e

    def _reconstruct_event(self, row: dict[str, Any]) -> DomainEvent:
        """Reconstruct domain event from outbox message.

        Args:
            row: Dictionary representing the message.

        Returns:
            Reconstructed DomainEvent.

        Raises:
            ValueError: If row is invalid.
        """
        if not isinstance(row, dict) or "payload" not in row:
            raise ValueError("row must be a dict with 'payload' key.")

        payload_data = json.loads(row["payload"])

        return DomainEvent(
            id=payload_data.get("id", row["id"]),
            event_type=row["event_type"],
            aggregate=payload_data.get("aggregate", "unknown"),
            aggregate_id=payload_data.get("aggregate_id", ""),
            occurred_at=payload_data.get("occurred_at", datetime.now(UTC)),
            payload=payload_data.get("payload", {}),
        )

    def stop(self) -> None:
        """Stop the dispatcher."""
        self._stop_event.set()
