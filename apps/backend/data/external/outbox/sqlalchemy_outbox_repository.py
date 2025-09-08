"""SQLAlchemy implementation of OutboxRepository.

Production-ready implementation using PostgreSQL-specific features for
optimal performance and reliability.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from apps.backend.core.outbox.outbox_hardened import OutboxEvent, OutboxRepository
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import Exception
import attempts
import backoff_sec
import batch_size
import bool
import dict
import e
import error
import event_id
import event_type
import float
import int
import len
import list
import lock_timeout
import next_run_at
import owner
import partition_key
import partition_mod
import payload
import result
import row_id
import schema_version
import self
import session
import str
import worker_ix

logger = logging.getLogger(__name__)


class SQLAlchemyOutboxRepository(OutboxRepository):
    """Production-ready SQLAlchemy implementation của OutboxRepository.

    Features:
    - SKIP LOCKED cho high-concurrency processing
    - Partition-based work distribution
    - Exponential backoff cho retries
    - Dead Letter Queue support
    - Health check endpoints
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository với async session.

        Args:
            session: SQLAlchemy async session
        """
        self._ = session

    async def fetch_due_batch_skip_locked(
        self, partition_mod: int, worker_ix: int, batch_size: int
    ) -> list[OutboxEvent]:
        """Fetch events due for processing với SKIP LOCKED.

        Sử dụng modulo-based partitioning để distribute work across workers.

        Args:
            partition_mod: Số workers (thường = num_workers)
            worker_ix: Index của worker này (0 đến num_workers-1)
            batch_size: Max events to fetch

        Returns:
            List of events ready for processing
        """
        try:
            query = text("""
                SELECT id, event_id, event_type, schema_version, partition_key,
                       payload, attempts, next_run_at, created_at
                FROM outbox_events
                WHERE partition_key % :partition_mod = :worker_ix
                  AND next_run_at <= :now
                  AND owner IS NULL
                ORDER BY next_run_at, created_at
                FOR UPDATE SKIP LOCKED
                LIMIT :batch_size
            """)

            _ = await self.session.execute(
                query,
                {
                    "partition_mod": partition_mod,
                    "worker_ix": worker_ix,
                    "now": datetime.now(UTC),
                    "batch_size": batch_size,
                },
            )

            events = []
            for row in result:
                events.append(
                    OutboxEvent(
                        id=row.id,
                        event_id=row.event_id,
                        event_type=row.event_type,
                        schema_version=row.schema_version,
                        partition_key=row.partition_key,
                        payload=row.payload,
                        attempts=row.attempts,
                        next_run_at=row.next_run_at,
                        created_at=row.created_at,
                    )
                )

            logger.debug(
                f"Fetched {len(events)} events for worker {worker_ix}/{partition_mod}"
            )
            return events

        except Exception as e:
            logger.error(f"Error fetching outbox batch: {e}")
            raise

    async def claim(self, row_id: int, owner: str, lock_timeout: int) -> bool:
        """Claim ownership của event với timeout.

        Args:
            row_id: Event row ID
            owner: Worker identifier
            lock_timeout: Lock timeout in seconds

        Returns:
            True if successfully claimed, False if already claimed
        """
        try:
            query = text("""
                UPDATE outbox_events
                SET owner = :owner,
                    locked_at = :locked_at,
                    lock_expires_at = :lock_expires_at
                WHERE id = :row_id
                  AND owner IS NULL
            """)

            now = datetime.now(UTC)
            _ = await self.session.execute(
                query,
                {
                    "owner": owner,
                    "locked_at": now,
                    "lock_expires_at": now + timedelta(seconds=lock_timeout),
                    "row_id": row_id,
                },
            )

            success = result.rowcount == 1
            logger.debug(f"Claim event {row_id} by {owner}: {success}")
            return success

        except Exception as e:
            logger.error(f"Error claiming event {row_id}: {e}")
            raise

    async def mark_done(self, row_id: int) -> None:
        """Đánh dấu event completed và remove khỏi outbox.

        Args:
            row_id: Event row ID to mark as done
        """
        try:
            query = text("DELETE FROM outbox_events WHERE id = :row_id")
            _ = await self.session.execute(query, {"row_id": row_id})

            if result.rowcount == 0:
                logger.warning(f"Event {row_id} not found when marking done")
            else:
                logger.debug(f"Marked event {row_id} as done")

        except Exception as e:
            logger.error(f"Error marking event {row_id} done: {e}")
            raise

    async def mark_retry(
        self,
        row_id: int,
        attempts: int,
        next_run_at: datetime,
        backoff_sec: int,
        error: str,
    ) -> None:
        """Update event for retry với exponential backoff.

        Args:
            row_id: Event row ID
            attempts: New attempt count
            next_run_at: When to retry next
            backoff_sec: Current backoff duration
            error: Error message to store
        """
        try:
            query = text("""
                UPDATE outbox_events
                SET attempts = :attempts,
                    next_run_at = :next_run_at,
                    backoff_sec = :backoff_sec,
                    last_error = :error,
                    owner = NULL,
                    locked_at = NULL,
                    lock_expires_at = NULL,
                    updated_at = :updated_at
                WHERE id = :row_id
            """)

            await self.session.execute(
                query,
                {
                    "attempts": attempts,
                    "next_run_at": next_run_at,
                    "backoff_sec": backoff_sec,
                    "error": error[:1000],  # Truncate error message
                    "updated_at": datetime.now(UTC),
                    "row_id": row_id,
                },
            )

            logger.debug(f"Marked event {row_id} for retry (attempt {attempts})")

        except Exception as e:
            logger.error(f"Error marking event {row_id} for retry: {e}")
            raise

    async def to_dlq(
        self,
        row_id: int,
        event_id: str,
        event_type: str,
        schema_version: str,
        partition_key: int,
        payload: dict[str, Any],
        attempts: int,
        error: str,
    ) -> None:
        """Move event to Dead Letter Queue after max retries.

        Args:
            row_id: Original event row ID
            event_id: Event UUID
            event_type: Event type string
            schema_version: Schema version
            partition_key: Partition key
            payload: Event payload
            attempts: Final attempt count
            error: Final error message
        """
        try:
            # Insert into DLQ
            dlq_query = text("""
                INSERT INTO outbox_dlq (
                    original_event_id, event_id, event_type, schema_version,
                    partition_key, payload, attempts, final_error, created_at
                ) VALUES (
                    :original_event_id, :event_id, :event_type, :schema_version,
                    :partition_key, :payload, :attempts, :final_error, :created_at
                )
            """)

            await self.session.execute(
                dlq_query,
                {
                    "original_event_id": row_id,
                    "event_id": event_id,
                    "event_type": event_type,
                    "schema_version": schema_version,
                    "partition_key": partition_key,
                    "payload": payload,
                    "attempts": attempts,
                    "final_error": error[:2000],  # Longer error for DLQ
                    "created_at": datetime.now(UTC),
                },
            )

            # Remove from main outbox
            await self.mark_done(row_id)

            logger.warning(
                f"Moved event {event_id} (type: {event_type}) to DLQ after {attempts} attempts"
            )

        except Exception as e:
            logger.error(f"Error moving event {row_id} to DLQ: {e}")
            raise

    async def queue_sizes(self) -> dict[int, int]:
        """Get queue sizes per partition.

        Returns:
            Dict mapping partition_key -> event_count
        """
        try:
            query = text("""
                SELECT partition_key, COUNT(*) as count
                FROM outbox_events
                WHERE next_run_at <= :now
                GROUP BY partition_key
                ORDER BY partition_key
            """)

            _ = await self.session.execute(query, {"now": datetime.now(UTC)})

            sizes = {}
            for row in result:
                sizes[row.partition_key] = row.count

            return sizes

        except Exception as e:
            logger.error(f"Error getting queue sizes: {e}")
            return {}

    async def dlq_sizes(self) -> dict[str, dict[int, int]]:
        """Get DLQ sizes per event_type and partition.

        Returns:
            Dict mapping event_type -> {partition_key -> count}
        """
        try:
            query = text("""
                SELECT event_type, partition_key, COUNT(*) as count
                FROM outbox_dlq
                GROUP BY event_type, partition_key
                ORDER BY event_type, partition_key
            """)

            _ = await self.session.execute(query)

            sizes: dict[str, dict[int, int]] = {}
            for row in result:
                if row.event_type not in sizes:
                    sizes[row.event_type] = {}
                sizes[row.event_type][row.partition_key] = row.count

            return sizes

        except Exception as e:
            logger.error(f"Error getting DLQ sizes: {e}")
            return {}

    async def health_check(self) -> bool:
        """Check database connection health.

        Returns:
            True if database is healthy, False otherwise
        """
        try:
            _ = await self.session.execute(text("SELECT 1"))
            return result.scalar() == 1

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def cleanup_expired_locks(self) -> int:
        """Clean up expired locks (maintenance operation).

        Returns:
            Number of locks cleaned up
        """
        try:
            query = text("""
                UPDATE outbox_events
                SET owner = NULL,
                    locked_at = NULL,
                    lock_expires_at = NULL
                WHERE lock_expires_at < :now
                  AND owner IS NOT NULL
            """)

            _ = await self.session.execute(query, {"now": datetime.now(UTC)})

            cleaned = result.rowcount
            if cleaned > 0:
                logger.info(f"Cleaned up {cleaned} expired locks")

            return cleaned

        except Exception as e:
            logger.error(f"Error cleaning expired locks: {e}")
            return 0

    async def get_stats(self) -> dict[str, Any]:
        """Get comprehensive outbox statistics.

        Returns:
            Statistics dictionary with counts, avg age, etc.
        """
        try:
            stats_query = text("""
                SELECT
                    COUNT(*) as total_events,
                    COUNT(*) FILTER (WHERE next_run_at <= :now) as due_events,
                    COUNT(*) FILTER (WHERE owner IS NOT NULL) as locked_events,
                    AVG(attempts) as avg_attempts,
                    MAX(attempts) as max_attempts,
                    AVG(EXTRACT(EPOCH FROM (:now - created_at))) as avg_age_seconds
                FROM outbox_events
            """)

            now = datetime.now(UTC)
            _ = await self.session.execute(stats_query, {"now": now})
            row = result.first()

            return {
                "total_events": row.total_events or 0,
                "due_events": row.due_events or 0,
                "locked_events": row.locked_events or 0,
                "avg_attempts": float(row.avg_attempts or 0),
                "max_attempts": row.max_attempts or 0,
                "avg_age_seconds": float(row.avg_age_seconds or 0),
                "timestamp": now.isoformat(),
            }

        except Exception as e:
            logger.error(f"Error getting outbox stats: {e}")
            return {"error": str(e), "timestamp": datetime.now(UTC).isoformat()}
