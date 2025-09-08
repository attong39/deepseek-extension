from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar
import BaseException
import Exception
import TimeoutError
import batch_size
import bool
import circuit_failure_threshold
import circuit_recovery_timeout
import dict
import e
import enable_circuit_breaker
import enable_metrics
import float
import flush_interval
import hash
import int
import item
import kwargs
import len
import list
import max_concurrent_batches
import p
import partition_count
import partition_items
import partitioned_items
import pid
import processing_time
import processor_fn
import range
import self
import set
import str
import t
import type

"""Batch Processor với tối ưu performance và advanced error handling."""
logger = logging.getLogger(__name__)
T = TypeVar("T")
R = TypeVar("R")


class BatchProcessor(Generic[T, R]):
    """Generic batch processor với tối ưu performance và monitoring."""

    def __init__(
        self,
        processor_fn: Callable[[list[T]], Awaitable[list[R]]],
        batch_size: int = 100,
        max_concurrent_batches: int = 10,
        flush_interval: float = 1.0,
        enable_metrics: bool = True,
        enable_circuit_breaker: bool = True,
        circuit_failure_threshold: int = 5,
        circuit_recovery_timeout: int = 60,
    ):
        """Initialize BatchProcessor với advanced features.
        Args:
            processor_fn: Function để process batch
            batch_size: Kích thước tối đa của batch
            max_concurrent_batches: Số batch tối đa xử lý đồng thời
            flush_interval: Thời gian tối đa chờ trước khi flush
            enable_metrics: Có enable metrics không
            enable_circuit_breaker: Có enable circuit breaker không
            circuit_failure_threshold: Ngưỡng failure cho circuit breaker
            circuit_recovery_timeout: Thời gian recovery cho circuit breaker
        """
        self.processor_fn = processor_fn
        self.batch_size = batch_size
        self.max_concurrent_batches = max_concurrent_batches
        self.flush_interval = flush_interval
        self.enable_metrics = enable_metrics
        self.enable_circuit_breaker = enable_circuit_breaker
        self.circuit_failure_threshold = circuit_failure_threshold
        self.circuit_recovery_timeout = circuit_recovery_timeout
        self._batch: list[T] = []
        self._pending_batches: dict[int, asyncio.Future[list[R]]] = {}
        self._batch_id_counter = 0
        self._flush_timer: asyncio.Task[None] | None = None
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrent_batches)
        self._active_tasks: set[asyncio.Task[None]] = set()
        self._circuit_failures = 0
        self._circuit_open_until: float = 0.0
        self._last_failure_time: float = 0.0
        self._processed_count = 0
        self._batch_count = 0
        self._avg_batch_size = 0.0
        self._avg_processing_time = 0.0
        self._error_count = 0
        self._circuit_breaker_trips = 0

    async def submit(self, item: T) -> asyncio.Future[R]:
        """Submit item để xử lý batch với circuit breaker protection."""
        if self.enable_circuit_breaker and self._is_circuit_open():
            raise CircuitBreakerOpenError("Circuit breaker is open")
        async with self._lock:
            self._batch.append(item)
            future: asyncio.Future[R] = asyncio.Future()
            batch_id = self._get_next_batch_id()
            if batch_id not in self._pending_batches:
                self._pending_batches[batch_id] = asyncio.Future()
            if len(self._batch) >= self.batch_size:
                await self._flush_batch()
            else:
                if self._flush_timer is None or self._flush_timer.done():
                    self._flush_timer = asyncio.create_task(self._delayed_flush())
            return future

    async def submit_batch(self, items: list[T]) -> list[asyncio.Future[R]]:
        """Submit batch of items với optimized processing."""
        futures = []
        for item in items:
            future = await self.submit(item)
            futures.append(future)
        return futures

    async def flush(self) -> None:
        """Force flush current batch với timeout protection."""
        async with self._lock:
            if self._batch:
                await self._flush_batch()
            if self._flush_timer and not self._flush_timer.done():
                self._flush_timer.cancel()
                try:
                    await asyncio.wait_for(self._flush_timer, timeout=5.0)
                except TimeoutError:
                    logger.warning("Flush timer cancellation timed out")
                except asyncio.CancelledError:
                    logger.warning("Flush timer was cancelled")
                    raise

    async def _flush_batch(self) -> None:
        """Flush current batch với error handling và circuit breaker."""
        if not self._batch:
            return
        batch = self._batch.copy()
        self._batch.clear()
        task = asyncio.create_task(self._process_batch_async(batch))
        self._active_tasks.add(task)
        self._active_tasks = {t for t in self._active_tasks if not t.done()}

    async def _process_batch_async(self, batch: list[T]) -> None:
        """Process batch asynchronously với comprehensive error handling."""
        async with self._semaphore:
            start_time = time.monotonic()
            try:
                if self.enable_circuit_breaker and self._is_circuit_open():
                    logger.warning("Skipping batch processing - circuit breaker open")
                    return
                await self.processor_fn(batch)
                self._record_success()
                if self.enable_metrics:
                    self._update_metrics(len(batch), time.monotonic() - start_time)
                logger.debug(f"Processed batch of {len(batch)} items successfully")
            except Exception as e:
                self._record_failure()
                self._error_count += 1
                logger.error(f"Batch processing error: {e}")

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is open."""
        if time.monotonic() > self._circuit_open_until:
            return False
        return True

    def _record_success(self) -> None:
        """Record successful operation."""
        self._circuit_failures = 0  # Reset failure count

    def _record_failure(self) -> None:
        """Record failed operation."""
        self._circuit_failures += 1
        self._last_failure_time = time.monotonic()
        if self._circuit_failures >= self.circuit_failure_threshold:
            self._circuit_open_until = time.monotonic() + self.circuit_recovery_timeout
            self._circuit_breaker_trips += 1
            logger.warning(
                f"Circuit breaker opened for {self.circuit_recovery_timeout}s"
            )

    def _update_metrics(self, batch_size: int, processing_time: float) -> None:
        """Update internal metrics với exponential moving average."""
        self._processed_count += batch_size
        self._batch_count += 1
        alpha = 0.1
        self._avg_batch_size = (1 - alpha) * self._avg_batch_size + alpha * batch_size
        self._avg_processing_time = (
            1 - alpha
        ) * self._avg_processing_time + alpha * processing_time

    def get_metrics(self) -> dict[str, Any]:
        """Get comprehensive metrics."""
        return {
            "processed_count": self._processed_count,
            "batch_count": self._batch_count,
            "avg_batch_size": self._avg_batch_size,
            "avg_processing_time": self._avg_processing_time,
            "error_count": self._error_count,
            "circuit_breaker_trips": self._circuit_breaker_trips,
            "current_batch_size": len(self._batch),
            "pending_batches": len(self._pending_batches),
            "active_tasks": len(self._active_tasks),
            "circuit_failures": self._circuit_failures,
            "circuit_open": self._is_circuit_open(),
            "circuit_open_until": self._circuit_open_until,
        }

    def _get_next_batch_id(self) -> int:
        """Get next batch ID với overflow protection."""
        self._batch_id_counter += 1
        if self._batch_id_counter > 2**31:  # Prevent overflow
            self._batch_id_counter = 1
        return self._batch_id_counter

    async def _delayed_flush(self) -> None:
        """Delayed flush với improved error handling."""
        try:
            await asyncio.sleep(self.flush_interval)
            async with self._lock:
                if self._batch:
                    await self._flush_batch()
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(f"Error in delayed flush: {e}")

    async def __aenter__(self) -> BatchProcessor[T, R]:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Async context manager exit - ensure flush và cleanup."""
        try:
            await self.flush()
        except Exception as e:
            logger.error(f"Error during batch processor cleanup: {e}")
        for task in self._active_tasks:
            if not task.done():
                task.cancel()
        if self._active_tasks:
            await asyncio.gather(*self._active_tasks, return_exceptions=True)


class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open."""


class PartitionedBatchProcessor(Generic[T, R]):
    """Batch processor với partitioning support."""

    def __init__(
        self,
        processor_fn: Callable[[int, list[T]], Awaitable[list[R]]],
        partition_count: int = 16,
        batch_size: int = 100,
        **kwargs: Any,
    ):
        """Initialize PartitionedBatchProcessor.
        Args:
            processor_fn: Function nhận (partition_id, batch) và trả về results
            partition_count: Số partitions
            batch_size: Batch size per partition
            **kwargs: Additional args cho BatchProcessor
        """
        self.processor_fn = processor_fn
        self.partition_count = partition_count
        self._processors: dict[int, BatchProcessor[T, R]] = {}
        for partition_id in range(partition_count):

            def create_processor(pid: int) -> Callable[[list[T]], Awaitable[list[R]]]:
                async def processor(batch: list[T]) -> list[R]:
                    return await self.processor_fn(pid, batch)

                return processor

            self._processors[partition_id] = BatchProcessor(
                processor_fn=create_processor(partition_id),
                batch_size=batch_size,
                **kwargs,
            )

    async def _wrap_processor_fn(self, partition_id: int, batch: list[T]) -> list[R]:
        """Wrap processor function to handle async calls."""
        return await self.processor_fn(partition_id, batch)

    def get_partition(self, item: T) -> int:
        """Get partition cho item (override để customize)."""
        return hash(str(item)) % self.partition_count

    async def submit(self, item: T) -> asyncio.Future[R]:
        """Submit item vào đúng partition."""
        partition_id = self.get_partition(item)
        processor = self._processors[partition_id]
        return await processor.submit(item)

    async def submit_batch(self, items: list[T]) -> list[asyncio.Future[R]]:
        """Submit batch items vào các partitions tương ứng."""
        partitioned_items: dict[int, list[T]] = defaultdict(list)
        for item in items:
            partition_id = self.get_partition(item)
            partitioned_items[partition_id].append(item)
        all_futures = []
        for partition_id, partition_items in partitioned_items.items():
            processor = self._processors[partition_id]
            futures = await processor.submit_batch(partition_items)
            all_futures.extend(futures)
        return all_futures

    async def flush(self) -> None:
        """Flush tất cả partitions."""
        await asyncio.gather(*(p.flush() for p in self._processors.values()))

    def get_metrics(self) -> dict[str, dict[str, Any]]:
        """Get metrics cho tất cả partitions."""
        return {
            f"partition_{pid}": processor.get_metrics()
            for pid, processor in self._processors.items()
        }

    async def __aenter__(self) -> PartitionedBatchProcessor[T, R]:
        """Async context manager entry."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Async context manager exit."""
        await self.flush()


__all__ = [
    "BatchProcessor",
    "CircuitBreakerOpenError",
    "PartitionedBatchProcessor",
    "R",
    "T",
    "all_futures",
    "alpha",
    "batch",
    "batch_id",
    "create_processor",
    "future",
    "futures",
    "get_metrics",
    "get_partition",
    "logger",
    "partition_id",
    "processor",
    "start_time",
    "task",
]
