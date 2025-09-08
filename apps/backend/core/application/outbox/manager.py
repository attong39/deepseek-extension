from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from app.event_bus import EventBus
from app.outbox_hardened import OutboxDispatcher, OutboxRepository

from .config import DispatcherConfig, OutboxConfig
import Exception
import RuntimeError
import TimeoutError
import d
import dict
import dispatcher_config
import e
import event
import event_bus
import events
import hasattr
import i
import len
import list
import outbox_config
import partitions
import range
import repository
import self
import str
import sum

"""Unified Outbox Manager cho toàn bộ hệ thống."""
logger = logging.getLogger(__name__)


class OutboxManager:
    """Unified manager cho toàn bộ Outbox system.
    Cung cấp high-level API để:
    - Initialize và configure outbox system
    - Start/stop dispatchers
    - Monitor system health
    - Handle graceful shutdown
    """

    def __init__(
        self,
        repository: OutboxRepository,
        event_bus: EventBus,
        outbox_config: OutboxConfig | None = None,
        dispatcher_config: DispatcherConfig | None = None,
    ):
        """Initialize OutboxManager.
        Args:
            repository: Outbox repository implementation
            event_bus: Event bus cho domain events
            outbox_config: Configuration cho outbox (default nếu None)
            dispatcher_config: Configuration cho dispatcher (default nếu None)
        """
        self.repository = repository
        self.event_bus = event_bus
        self.outbox_config = outbox_config or OutboxConfig()
        self.dispatcher_config = dispatcher_config or DispatcherConfig()
        self._dispatchers: list[OutboxDispatcher] = []
        self._dispatcher_tasks: list[asyncio.Task[None]] = []
        self._shutdown_event = asyncio.Event()
        self._health_check_task: asyncio.Task[None] | None = None

    async def initialize(self) -> None:
        """Initialize outbox system components."""
        logger.info("Initializing Outbox Manager...")
        if hasattr(self.repository, "ready"):
            ready = await self.repository.ready()
            if not ready:
                raise RuntimeError("Outbox repository not ready")
        if self.dispatcher_config.enable_health_checks:
            self._health_check_task = asyncio.create_task(self._health_check_loop())
        logger.info("Outbox Manager initialized successfully")

    async def start_dispatchers(self) -> None:
        """Start tất cả outbox dispatchers."""
        logger.info(
            f"Starting {self.dispatcher_config.worker_count} outbox dispatchers..."
        )
        for i in range(self.dispatcher_config.worker_count):
            dispatcher = OutboxDispatcher(
                session_factory=self._get_session_factory(),
                event_bus=self.event_bus,
                worker_id=f"{self.dispatcher_config.worker_id_prefix}-{i}",
                shard=None,  # Will be assigned based on partitioning
                interval_sec=self.dispatcher_config.poll_interval_sec,
                batch_size=self.dispatcher_config.batch_size,
                concurrency=self.dispatcher_config.max_concurrent_batches,
            )
            self._dispatchers.append(dispatcher)
            task = asyncio.create_task(
                self._run_dispatcher(dispatcher), name=f"outbox-dispatcher-{i}"
            )
            self._dispatcher_tasks.append(task)
        logger.info(f"Started {len(self._dispatchers)} outbox dispatchers")

    async def stop_dispatchers(self) -> None:
        """Stop tất cả outbox dispatchers gracefully."""
        logger.info("Stopping outbox dispatchers...")
        self._shutdown_event.set()
        for dispatcher in self._dispatchers:
            dispatcher.stop()
        if self._dispatcher_tasks:
            await asyncio.gather(*self._dispatcher_tasks, return_exceptions=True)
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        logger.info("All outbox dispatchers stopped")

    async def publish_event(self, event: Any) -> None:
        """Publish domain event vào outbox."""
        await self.repository.add_events([event])

    async def publish_events(self, events: list[Any]) -> None:
        """Publish multiple domain events vào outbox."""
        await self.repository.add_events(events)

    async def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status."""
        try:
            queue_sizes = await self.repository.queue_sizes()
            dlq_sizes = await self.repository.dlq_sizes()
            total_queued = sum(queue_sizes.values())
            total_dlq = sum(
                sum(partitions.values()) for partitions in dlq_sizes.values()
            )
            active_dispatchers = sum(
                1 for d in self._dispatchers if not d._stop_event.is_set()
            )
            return {
                "status": "healthy" if active_dispatchers > 0 else "degraded",
                "active_dispatchers": active_dispatchers,
                "total_dispatchers": len(self._dispatchers),
                "total_queued_events": total_queued,
                "total_dlq_events": total_dlq,
                "queue_sizes_by_partition": queue_sizes,
                "dlq_sizes_by_type": dlq_sizes,
                "configuration": {
                    "worker_count": self.dispatcher_config.worker_count,
                    "batch_size": self.dispatcher_config.batch_size,
                    "poll_interval": self.dispatcher_config.poll_interval_sec,
                },
            }
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "active_dispatchers": 0,
                "total_dispatchers": len(self._dispatchers),
            }

    @asynccontextmanager
    async def lifecycle(self) -> AsyncGenerator[OutboxManager, None]:
        """Context manager cho outbox lifecycle management."""
        await self.initialize()
        await self.start_dispatchers()
        try:
            yield self
        finally:
            await self.stop_dispatchers()

    def _get_session_factory(self) -> Any:
        """Get session factory từ repository."""
        if hasattr(self.repository, "_session_factory"):
            return self.repository._session_factory
        elif hasattr(self.repository, "session"):
            return lambda: self.repository.session
        else:
            return None

    async def _run_dispatcher(self, dispatcher: OutboxDispatcher) -> None:
        """Run dispatcher với error handling."""
        try:
            await dispatcher.run_forever()
        except Exception as e:
            logger.error(f"Dispatcher error: {e}")
            raise

    async def _health_check_loop(self) -> None:
        """Periodic health check loop."""
        while not self._shutdown_event.is_set():
            try:
                status = await self.get_system_status()
                if status["status"] == "healthy":
                    logger.debug("Outbox system health check passed")
                else:
                    logger.warning(f"Outbox system health check failed: {status}")
            except Exception as e:
                logger.error(f"Health check error: {e}")
            try:
                await asyncio.wait_for(
                    self._shutdown_event.wait(),
                    timeout=self.dispatcher_config.health_check_interval,
                )
            except TimeoutError:
                continue  # Continue health check loop
            else:
                break  # Shutdown event was set


__all__ = [
    "OutboxManager",
    "active_dispatchers",
    "dispatcher",
    "dlq_sizes",
    "logger",
    "queue_sizes",
    "ready",
    "status",
    "task",
    "total_dlq",
    "total_queued",
]
