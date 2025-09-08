"""PostgreSQL implementation của OutboxRepository."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

from apps.backend.data.outbox_tables import outbox_dlq, outbox_events, processed_message
from apps.backend.data.repositories.outbox_row import OutboxRow
from sqlalchemy import delete, func, insert, select, text, update
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


class PostgresOutboxRepository:
    """PostgreSQL implementation của OutboxRepository với safe concurrent processing."""
import Exception
import RuntimeError
import attempts
import backoff_sec
import batch_size
import bool
import classmethod
import cls
import conn
import dict
import error
import event_id
import event_type
import handler
import int
import item
import key
import limit
import list
import lock_timeout_sec
import next_run_at
import partition_key
import partition_mod
import payload
import pk
import result
import row_id
import schema_version
import self
import session
import str
import worker_ix

    def __init__(self, engine: AsyncEngine, owner: str, lock_timeout_sec: int = 15):
        self.engine = engine
        self.Session = async_sessionmaker(engine, expire_on_commit=False)
        self.owner = owner
        self.lock_timeout_sec = lock_timeout_sec

    @classmethod
    def from_env(
        cls, owner: str, lock_timeout_sec: int = 15
    ) -> PostgresOutboxRepository:
        """Tạo instance từ DATABASE_URL env var."""
        url = os.getenv("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL environment variable not set")
        engine = create_async_engine(url, pool_pre_ping=True)
        return cls(engine, owner, lock_timeout_sec)

    async def ready(self) -> bool:
        """Kiểm tra kết nối DB sẵn sàng."""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception:
            return False

    def _now(self) -> datetime:
        """Current UTC timestamp."""
        return datetime.now(UTC)

    async def fetch_due_batch_skip_locked(
        self, partition_mod: int, worker_ix: int, batch_size: int
    ) -> list[OutboxRow]:
        """Lấy events đến hạn xử lý cho worker này.

        Args:
            partition_mod: Tổng số workers (để partition)
            worker_ix: Index của worker này (0-based)
            batch_size: Số lượng events tối đa

        Returns:
            List OutboxRow candidates (chưa claim)
        """
        now = self._now()
        async with self.Session() as session:
            query = (
                select(
                    outbox_events.c.id,
                    outbox_events.c.event_id,
                    outbox_events.c.event_type,
                    outbox_events.c.schema_version,
                    outbox_events.c.partition_key,
                    outbox_events.c.payload,
                    outbox_events.c.attempts,
                )
                .where(outbox_events.c.next_run_at <= now)
                .where((outbox_events.c.partition_key % partition_mod) == worker_ix)
                .order_by(outbox_events.c.next_run_at.asc())
                .limit(batch_size * 3)  # Over-select để giảm lock contention
            )
            rows = (await session.execute(query)).all()

        return [
            OutboxRow(
                id=row.id,
                event_id=row.event_id,
                event_type=row.event_type,
                schema_version=row.schema_version,
                partition_key=row.partition_key,
                payload=row.payload,
                attempts=row.attempts,
            )
            for row in rows
        ]

    async def claim(
        self, row_id: int, owner: str | None = None, lock_timeout: int | None = None
    ) -> bool:
        """Try-lock event với Compare-And-Swap operation.

        Args:
            row_id: ID của event cần claim
            owner: Owner của lock (default: self.owner)
            lock_timeout: Timeout seconds (default: self.lock_timeout_sec)

        Returns:
            True nếu claim thành công, False nếu đã bị lock
        """
        owner = owner or self.owner
        lock_timeout = lock_timeout or self.lock_timeout_sec
        expire_before = self._now() - timedelta(seconds=lock_timeout)

        async with self.Session.begin() as session:
            query = (
                update(outbox_events)
                .where(outbox_events.c.id == row_id)
                .where(
                    (outbox_events.c.locked_at.is_(None))
                    | (outbox_events.c.locked_at < expire_before)
                )
                .values(locked_at=self._now(), lock_owner=owner)
            )
            _ = await session.execute(query)
            return result.rowcount == 1

    async def mark_done(self, row_id: int) -> None:
        """Xóa event sau khi xử lý thành công."""
        async with self.Session.begin() as session:
            await session.execute(
                delete(outbox_events).where(outbox_events.c.id == row_id)
            )

    async def mark_retry(
        self,
        row_id: int,
        attempts: int,
        next_run_at: datetime,
        backoff_sec: int,
        error: str,
    ) -> None:
        """Mark event để retry sau với backoff."""
        async with self.Session.begin() as session:
            query = (
                update(outbox_events)
                .where(outbox_events.c.id == row_id)
                .values(
                    attempts=attempts,
                    next_run_at=next_run_at,
                    backoff_sec=backoff_sec,
                    locked_at=None,
                    lock_owner=None,
                    updated_at=self._now(),
                )
            )
            await session.execute(query)

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
        """Chuyển event vào Dead Letter Queue."""
        async with self.Session.begin() as session:
            # Insert vào DLQ
            await session.execute(
                insert(outbox_dlq).values(
                    event_id=event_id,
                    event_type=event_type,
                    schema_version=schema_version,
                    partition_key=partition_key,
                    payload=payload,
                    error=error,
                    attempts=attempts,
                )
            )
            # Xóa khỏi main queue
            await session.execute(
                delete(outbox_events).where(outbox_events.c.id == row_id)
            )

    async def queue_sizes(self) -> dict[int, int]:
        """Thống kê queue size theo partition."""
        async with self.Session() as session:
            query = select(outbox_events.c.partition_key, func.count()).group_by(
                outbox_events.c.partition_key
            )
            _ = (await session.execute(query)).all()
        return {int(pk): int(count) for pk, count in result}

    async def dlq_sizes(self) -> dict[int, int]:
        """Thống kê DLQ size theo partition."""
        async with self.Session() as session:
            query = select(outbox_dlq.c.partition_key, func.count()).group_by(
                outbox_dlq.c.partition_key
            )
            _ = (await session.execute(query)).all()
        return {int(pk): int(count) for pk, count in result}

    async def enqueue(
        self,
        event_id: str,
        event_type: str,
        schema_version: str,
        partition_key: int,
        payload: dict[str, Any],
    ) -> None:
        """Enqueue event mới (for testing/admin)."""
        async with self.Session.begin() as session:
            await session.execute(
                insert(outbox_events).values(
                    event_id=event_id,
                    event_type=event_type,
                    schema_version=schema_version,
                    partition_key=partition_key,
                    payload=payload,
                    next_run_at=self._now(),
                    attempts=0,
                    backoff_sec=0,
                )
            )

    async def redrive_from_dlq(self, limit: int = 100) -> int:
        """Redrive events từ DLQ về main queue."""
        async with self.Session() as session:
            # Lấy items từ DLQ
            query = select(outbox_dlq).limit(limit)
            items = (await session.execute(query)).mappings().all()

        count = 0
        for item in items:
            await self._redrive_one_item(item)
            count += 1

        return count

    async def _redrive_one_item(self, item: dict[str, Any] | RowMapping) -> None:
        """Redrive một DLQ item về main queue."""
        async with self.Session.begin() as session:
            # Insert về main queue
            await session.execute(
                insert(outbox_events).values(
                    event_id=item["event_id"],
                    event_type=item["event_type"],
                    schema_version=item["schema_version"],
                    partition_key=item["partition_key"],
                    payload=item["payload"],
                    next_run_at=self._now(),
                    attempts=0,
                    backoff_sec=0,
                )
            )
            # Xóa khỏi DLQ
            await session.execute(
                delete(outbox_dlq).where(outbox_dlq.c.id == item["id"])
            )


class SQLProcessedStore:
    """SQL-backed ProcessedStore cho idempotency."""

    def __init__(self, engine: AsyncEngine):
        self.Session = async_sessionmaker(engine, expire_on_commit=False)

    async def exists(self, handler: str, key: str) -> bool:
        """Kiểm tra message đã được xử lý chưa."""
        async with self.Session() as session:
            query = select(processed_message.c.id).where(
                processed_message.c.handler == handler,
                processed_message.c.message_key == key,
            )
            row = (await session.execute(query)).first()
            return row is not None

    async def put(self, handler: str, key: str) -> None:
        """Mark message là đã xử lý."""
        async with self.Session.begin() as session:
            stmt = insert(processed_message).values(handler=handler, message_key=key)
            # PostgreSQL ON CONFLICT DO NOTHING - cast to Any để bypass mypy
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["handler", "message_key"]
            )  # type: ignore[attr-defined]
            await session.execute(stmt)
