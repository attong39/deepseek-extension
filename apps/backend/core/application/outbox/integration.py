from __future__ import annotations

import logging
from typing import Any

from app.event_bus import InMemoryEventBus
from app.outbox_hardened import OutboxRepository

from .config import DispatcherConfig, OutboxConfig
from .manager import OutboxManager
import Exception
import RuntimeError
import app_event
import app_repo
import app_row
import attempt
import bool
import core_event
import core_repo
import dict
import e
import error
import event_bus
import hasattr
import int
import isinstance
import limit
import list
import message_id
import repository
import row
import self
import shard
import staticmethod
import str
import use_app_for_writes
import use_core_for_reads
import worker_count
import worker_id

"""Integration layer giữa application và core outbox systems."""
logger = logging.getLogger(__name__)


class UnifiedOutboxRepository:
    """Unified repository that bridges application and core outbox systems.
    Provides consistent interface while leveraging optimizations from both layers.
    """

    __outbox_repository__: bool = True

    def __init__(
        self,
        app_repo: OutboxRepository | None = None,
        core_repo: OutboxRepository | None = None,
        use_core_for_reads: bool = True,
        use_app_for_writes: bool = True,
    ):
        """Initialize unified repository.
        Args:
            app_repo: Application layer repository
            core_repo: Core layer repository
            use_core_for_reads: Use core repo for read operations (better performance)
            use_app_for_writes: Use app repo for write operations (better consistency)
        """
        self.app_repo = app_repo
        self.core_repo = core_repo
        self.use_core_for_reads = use_core_for_reads
        self.use_app_for_writes = use_app_for_writes

    async def add_events(self, events: list[Any]) -> None:
        """Add events using the configured write repository."""
        if self.use_app_for_writes and self.app_repo:
            await self.app_repo.add_events(events)
        elif self.core_repo:
            core_events = [self._convert_to_core_event(e) for e in events]
            await self.core_repo.add_events(core_events)
        else:
            raise RuntimeError("No repository configured for writes")

    async def claim_batch(
        self, worker_id: str, shard: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Claim batch using the configured read repository."""
        if self.use_core_for_reads and self.core_repo:
            events = await self.core_repo.claim_batch(worker_id, shard, limit)
            return [self._convert_from_core_event(e) for e in events]
        elif self.app_repo:
            result = await self.app_repo.claim_batch(worker_id, shard, limit)
            return result if isinstance(result, list) else []
        else:
            raise RuntimeError("No repository configured for reads")

    async def mark_dispatched(self, message_id: str) -> None:
        """Mark message as dispatched."""
        if self.app_repo:
            try:
                await self.app_repo.mark_dispatched(message_id)
                return
            except Exception as e:
                logger.warning(f"App repo mark_dispatched failed: {e}")
        if self.core_repo:
            try:
                await self.core_repo.mark_dispatched(message_id)
                return
            except Exception as e:
                logger.warning(f"Core repo mark_dispatched failed: {e}")
        raise RuntimeError(f"Failed to mark message {message_id} as dispatched")

    async def retry_later(self, message_id: str, attempt: int, error: str) -> None:
        """Schedule message for retry."""
        if self.app_repo:
            try:
                await self.app_repo.retry_later(message_id, attempt, error)
                return
            except Exception as e:
                logger.warning(f"App repo retry_later failed: {e}")
        if self.core_repo:
            try:
                await self.core_repo.retry_later(message_id, attempt, error)
                return
            except Exception as e:
                logger.warning(f"Core repo retry_later failed: {e}")
        raise RuntimeError(f"Failed to retry message {message_id}")

    async def move_to_dlq(self, row: dict[str, Any], error: str) -> None:
        """Move message to dead letter queue."""
        if self.app_repo:
            try:
                await self.app_repo.move_to_dlq(row, error)
                return
            except Exception as e:
                logger.warning(f"App repo move_to_dlq failed: {e}")
        if self.core_repo:
            try:
                core_row = self._convert_to_core_row(row)
                await self.core_repo.move_to_dlq(core_row, error)
                return
            except Exception as e:
                logger.warning(f"Core repo move_to_dlq failed: {e}")
        raise RuntimeError(f"Failed to move message to DLQ: {row.get('id', 'unknown')}")

    async def queue_sizes(self) -> dict[int, int]:
        """Get queue sizes."""
        if self.use_core_for_reads and self.core_repo:
            result = await self.core_repo.queue_sizes()
            return result if isinstance(result, dict) else {}
        elif self.app_repo:
            result = await self.app_repo.queue_sizes()
            return result if isinstance(result, dict) else {}
        else:
            return {}

    async def dlq_sizes(self) -> dict[str, dict[int, int]]:
        """Get DLQ sizes."""
        if self.use_core_for_reads and self.core_repo:
            result = await self.core_repo.dlq_sizes()
            return result if isinstance(result, dict) else {}
        elif self.app_repo:
            result = await self.app_repo.dlq_sizes()
            return result if isinstance(result, dict) else {}
        else:
            return {}

    def _convert_to_core_event(self, app_event: Any) -> Any:
        """Convert application event to core event format."""
        return app_event

    def _convert_from_core_event(self, core_event: Any) -> dict[str, Any]:
        """Convert core event to application format."""
        if hasattr(core_event, "__dict__"):
            result = core_event.__dict__
            return result if isinstance(result, dict) else {"data": result}
        return (
            dict(core_event)
            if hasattr(core_event, "keys")
            else {"data": str(core_event)}
        )

    def _convert_to_core_row(self, app_row: dict[str, Any]) -> dict[str, Any]:
        """Convert application row to core format."""
        return app_row


class OutboxSystemFactory:
    """Factory for creating optimized outbox system components."""

    @staticmethod
    def create_unified_repository(
        app_repo: OutboxRepository | None = None,
        core_repo: OutboxRepository | None = None,
    ) -> UnifiedOutboxRepository:
        """Create unified repository with optimal settings."""
        return UnifiedOutboxRepository(
            app_repo=app_repo,
            core_repo=core_repo,
            use_core_for_reads=True,  # Core has better read performance
            use_app_for_writes=True,  # App has better consistency
        )

    @staticmethod
    def create_optimized_event_bus() -> Any:
        """Create optimized event bus with performance monitoring."""
        return InMemoryEventBus()

    @staticmethod
    def create_production_ready_system(
        repository: UnifiedOutboxRepository,
        event_bus: Any,
        worker_count: int = 4,
    ) -> Any:
        """Create production-ready outbox system."""
        outbox_config = OutboxConfig(
            max_connections=50,
            enable_partitioning=True,
            partition_count=32,
            enable_metrics=True,
        )
        dispatcher_config = DispatcherConfig(
            worker_count=worker_count,
            batch_size=100,
            max_concurrent_batches=20,
            enable_health_checks=True,
            enable_detailed_metrics=True,
        )
        return OutboxManager(
            repository=repository,  # type: ignore
            event_bus=event_bus,
            outbox_config=outbox_config,
            dispatcher_config=dispatcher_config,
        )


__all__ = [
    "OutboxSystemFactory",
    "UnifiedOutboxRepository",
]
