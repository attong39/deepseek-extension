"""Production-hardened Outbox worker dispatcher.

Cung cấp distributed worker system với sharding, exponential backoff,
graceful shutdown và comprehensive error handling.
"""

from __future__ import annotations

import asyncio
import os
import random
import signal
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
import Exception
import ImportError
import NotImplementedError
import ValueError
import bool
import config_overrides
import dict
import e
import error
import event
import final_payload
import final_version
import float
import handlers
import i
import int
import list
import min
import num_workers
import print
import range
import repo
import self
import sig
import str
import type

# Import metrics - sẽ fallback nếu prometheus_client không có
try:
    from .metrics import (
        record_db_query,
        record_event_age,
        record_event_failed,
        record_event_processed,
        record_event_retried,
        record_idempotency_hit,
        record_upcaster_applied,
        record_upcaster_failed,
        set_worker_active,
        update_dlq_sizes,
        update_queue_sizes,
    )

    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False

    # Define no-op functions
    def record_event_processed(*args, **kwargs):
        pass

    def record_event_failed(*args, **kwargs):
        pass

    def record_event_retried(*args, **kwargs):
        pass

    def record_idempotency_hit(*args, **kwargs):
        pass

    def record_upcaster_applied(*args, **kwargs):
        pass

    def record_upcaster_failed(*args, **kwargs):
        pass

    def record_db_query(*args, **kwargs):
        pass

    def record_event_age(*args, **kwargs):
        pass

    def set_worker_active(*args, **kwargs):
        pass

    def update_queue_sizes(*args, **kwargs):
        pass

    def update_dlq_sizes(*args, **kwargs):
        pass


from .upcaster import registry as upcasters


@dataclass
class WorkerConfig:
    """Configuration cho Outbox worker."""

    worker_index: int
    num_workers: int
    batch_size: int = 200
    max_attempts: int = 8
    lock_timeout_sec: int = 15
    base_backoff_sec: int = 1
    max_backoff_sec: int = 120
    poll_interval_sec: float = 0.05
    metrics_interval_sec: int = 30

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.worker_index < 0 or self.worker_index >= self.num_workers:
            raise ValueError(
                f"worker_index {self.worker_index} ngoài range [0, {self.num_workers})"
            )
        if self.batch_size <= 0:
            raise ValueError("batch_size phải > 0")
        if self.max_attempts <= 0:
            raise ValueError("max_attempts phải > 0")


@dataclass
class OutboxEvent:
    """Outbox event row data."""

    id: int
    event_id: str
    event_type: str
    schema_version: str
    partition_key: int
    payload: dict[str, Any]
    attempts: int
    next_run_at: datetime
    created_at: datetime


class OutboxRepository:
    """Interface cho Outbox repository.

    Implement bằng SQLAlchemy/asyncpg ở infrastructure layer.
    """

    async def fetch_due_batch_skip_locked(
        self, partition_mod: int, worker_ix: int, batch_size: int
    ) -> list[OutboxEvent]:
        """Fetch batch events due for processing với SKIP LOCKED.

        Args:
            partition_mod: Số workers để sharding
            worker_ix: Index của worker này
            batch_size: Kích thước batch tối đa

        Returns:
            List events ready to process
        """
        raise NotImplementedError

    async def claim(self, row_id: int, owner: str, lock_timeout: int) -> bool:
        """Claim ownership của event row.

        Args:
            row_id: ID của event row
            owner: Worker identifier
            lock_timeout: Timeout in seconds

        Returns:
            True nếu claim thành công, False nếu đã có worker khác claim
        """
        raise NotImplementedError

    async def mark_done(self, row_id: int) -> None:
        """Đánh dấu event đã process xong và xóa khỏi outbox."""
        raise NotImplementedError

    async def mark_retry(
        self,
        row_id: int,
        attempts: int,
        next_run_at: datetime,
        backoff_sec: int,
        error: str,
    ) -> None:
        """Đánh dấu event cần retry với backoff."""
        raise NotImplementedError

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
        raise NotImplementedError

    async def queue_sizes(self) -> dict[int, int]:
        """Lấy queue sizes theo partition."""
        raise NotImplementedError

    async def dlq_sizes(self) -> dict[str, dict[int, int]]:
        """Lấy DLQ sizes theo event_type và partition."""
        raise NotImplementedError

    async def health_check(self) -> bool:
        """Kiểm tra DB connection health."""
        raise NotImplementedError


# Type alias cho event handler
Handler = Callable[[dict[str, Any]], Awaitable[None]]


class Dispatcher:
    """Production-hardened Outbox event dispatcher.

    Features:
    - Sharded processing với worker index
    - Exponential backoff với jitter
    - Graceful shutdown
    - Comprehensive metrics
    - Schema upcasting
    - Error handling và DLQ
    """

    def __init__(
        self, repo: OutboxRepository, handlers: dict[str, Handler], cfg: WorkerConfig
    ) -> None:
        """Initialize dispatcher.

        Args:
            repo: Outbox repository implementation
            handlers: Map từ event_type -> handler function
            cfg: Worker configuration
        """
        self.repo = repo
        self.handlers = handlers
        self.cfg = cfg
        self._shutdown = asyncio.Event()
        self._owner = f"w{cfg.worker_index}-{os.getpid()}"
        self._running = False

    def install_signal_handlers(self) -> None:
        """Install graceful shutdown signal handlers."""
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._shutdown.set)
            except NotImplementedError:
                # Windows không support add_signal_handler
                signal.signal(sig, lambda s, f: self._shutdown.set())

    async def tick_metrics(self) -> None:
        """Update metrics periodically."""
        if not METRICS_AVAILABLE:
            return

        try:
            # Update queue metrics
            queue_sizes = await self.repo.queue_sizes()
            update_queue_sizes(queue_sizes)

            dlq_sizes = await self.repo.dlq_sizes()
            update_dlq_sizes(dlq_sizes)

        except Exception:
            # Metrics không nên crash worker
            pass

    async def run(self) -> None:
        """Main worker loop.

        Runs until shutdown signal received.
        """
        self.install_signal_handlers()
        self._running = True
        set_worker_active(self.cfg.worker_index, True)

        try:
            # Background task để update metrics
            metrics_task = asyncio.create_task(self._metrics_loop())

            # Main processing loop
            while not self._shutdown.is_set():
                await self._process_batch()
                await asyncio.sleep(self.cfg.poll_interval_sec)

        except Exception as e:
            print(f"Worker {self._owner} crashed: {e}")
            raise
        finally:
            self._running = False
            set_worker_active(self.cfg.worker_index, False)
            metrics_task.cancel()
            print(f"Worker {self._owner} shutdown complete")

    async def _metrics_loop(self) -> None:
        """Background loop để update metrics."""
        while self._running and not self._shutdown.is_set():
            await self.tick_metrics()
            await asyncio.sleep(self.cfg.metrics_interval_sec)

    async def _process_batch(self) -> None:
        """Process một batch events."""
        with record_db_query("fetch", 0):
            batch = await self.repo.fetch_due_batch_skip_locked(
                self.cfg.num_workers, self.cfg.worker_index, self.cfg.batch_size
            )

        if not batch:
            return

        # Process events concurrently
        await asyncio.gather(
            *(self._process_event(event) for event in batch), return_exceptions=True
        )

    async def _process_event(self, event: OutboxEvent) -> None:
        """Process một event."""
        # Claim event row
        with record_db_query("claim", 0):
            claimed = await self.repo.claim(
                event.id, self._owner, self.cfg.lock_timeout_sec
            )

        if not claimed:
            # Another worker claimed it
            return

        start_time = datetime.now(UTC)

        try:
            # Upcast event nếu cần
            final_version, final_payload = upcasters.upcast(
                event.event_type, event.schema_version, event.payload
            )

            if final_version != event.schema_version:
                record_upcaster_applied(
                    event.event_type, event.schema_version, final_version
                )

            # Find handler
            handler = self.handlers.get(event.event_type)
            if not handler:
                await self._to_dlq(event, "no_handler")
                return

            # Prepare event payload for handler
            handler_payload = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "version": final_version,
                "payload": final_payload,
                "aggregate_id": final_payload.get("aggregate_id"),
                "occurred_at": final_payload.get("occurred_at"),
                "correlation_id": final_payload.get("correlation_id"),
            }

            # Process event
            await handler(handler_payload)

            # Mark done
            with record_db_query("mark_done", 0):
                await self.repo.mark_done(event.id)

            # Record success metrics
            duration = (datetime.now(UTC) - start_time).total_seconds()
            record_event_processed(event.event_type, "outbox_handler", duration)

            # Record event age
            age_seconds = (start_time - event.created_at).total_seconds()
            record_event_age(event.event_type, age_seconds)

        except Exception as e:
            duration = (datetime.now(UTC) - start_time).total_seconds()
            await self._handle_error(event, str(e), duration)

    async def _handle_error(
        self, event: OutboxEvent, error: str, duration: float
    ) -> None:
        """Handle processing error với retry logic."""
        attempts = event.attempts + 1

        if attempts >= self.cfg.max_attempts:
            await self._to_dlq(event, f"max_attempts_exceeded: {error}")
            return

        # Calculate backoff với jitter
        backoff = min(
            self.cfg.base_backoff_sec * (2 ** (attempts - 1)), self.cfg.max_backoff_sec
        )
        jitter = random.uniform(0, backoff * 0.1)  # 10% jitter
        total_backoff = backoff + jitter

        next_run = datetime.now(UTC) + timedelta(seconds=total_backoff)

        with record_db_query("mark_retry", 0):
            await self.repo.mark_retry(
                event.id, attempts, next_run, int(total_backoff), error
            )

        # Record retry metrics
        record_event_retried(event.event_type, "outbox_handler", attempts)
        record_event_failed(
            event.event_type, "outbox_handler", type(error).__name__, duration
        )

    async def _to_dlq(self, event: OutboxEvent, error: str) -> None:
        """Move event to Dead Letter Queue."""
        with record_db_query("to_dlq", 0):
            await self.repo.to_dlq(
                event.id,
                event.event_id,
                event.event_type,
                event.schema_version,
                event.partition_key,
                event.payload,
                event.attempts,
                error,
            )

        # Record DLQ metrics
        failure_reason = error.split(":")[0] if ":" in error else error
        from .metrics import record_dlq_written

        record_dlq_written(event.event_type, "outbox_handler", failure_reason)


async def start_dispatcher(
    repo: OutboxRepository,
    handlers: dict[str, Handler],
    num_workers: int = 2,
    **config_overrides,
) -> None:
    """Start multiple dispatcher workers.

    Args:
        repo: Repository implementation
        handlers: Event handlers map
        num_workers: Số workers chạy parallel
        **config_overrides: Override default WorkerConfig
    """
    tasks = []

    for i in range(num_workers):
        cfg = WorkerConfig(worker_index=i, num_workers=num_workers, **config_overrides)

        dispatcher = Dispatcher(repo, handlers, cfg)
        task = asyncio.create_task(dispatcher.run(), name=f"outbox-worker-{i}")
        tasks.append(task)

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("Dispatcher workers cancelled")
        raise
