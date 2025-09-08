"""Unit tests for event_bus module.

This module contains comprehensive unit tests for the InMemoryEventBus
implementation, covering async operations, concurrency limits, metrics,
and circuit breaker functionality.
"""

from __future__ import annotations

import asyncio
import time
from unittest.mock import AsyncMock

import pytest
from apps.backend.core.application.event_bus import InMemoryEventBus
from apps.backend.core.domain.domain_events import DomainEvent
import Exception
import RuntimeError
import data
import dict
import event_type
import i
import range
import self
import str
import super


class TestEvent(DomainEvent):
    """Test domain event for testing purposes."""

    def __init__(self, event_type: str, data: dict | None = None) -> None:
        super().__init__(event_type=event_type, trace_id="test-trace-123")
        self.data = data or {}


class TestInMemoryEventBus:
    """Test suite for InMemoryEventBus."""

    @pytest.fixture
    def event_bus(self) -> InMemoryEventBus:
        """Fixture for event bus instance."""
        return InMemoryEventBus(
            max_queue_size=10,
            failure_threshold=2,
            recovery_timeout=1.0,
            max_concurrent_handlers=3,
        )

    @pytest.fixture
    def test_event(self) -> TestEvent:
        """Fixture for test event."""
        return TestEvent("TestEvent", {"key": "value"})

    @pytest.mark.asyncio
    async def test_subscribe_and_publish(
        self, event_bus: InMemoryEventBus, test_event: TestEvent
    ) -> None:
        """Test basic subscribe and publish functionality."""
        handler = AsyncMock()
        event_bus.subscribe("TestEvent", handler)

        await event_bus.publish(test_event)

        # Wait for processing
        await asyncio.sleep(0.1)

        handler.assert_called_once_with(test_event)

    @pytest.mark.asyncio
    async def test_concurrency_limit(self, event_bus: InMemoryEventBus) -> None:
        """Test that semaphore limits concurrent handler invocations."""
        slow_handler = AsyncMock(side_effect=lambda e: asyncio.sleep(0.1))

        # Subscribe multiple handlers
        for _ in range(5):
            event_bus.subscribe("TestEvent", slow_handler)

        event = TestEvent("TestEvent")

        start_time = time.time()
        await event_bus.publish(event)
        await asyncio.sleep(0.3)  # Wait for all to complete
        end_time = time.time()

        # With concurrency limit of 3, should take at least 2 batches * 0.1s
        assert end_time - start_time >= 0.2
        assert slow_handler.call_count == 5

    @pytest.mark.asyncio
    async def test_metrics_tracking(
        self, event_bus: InMemoryEventBus, test_event: TestEvent
    ) -> None:
        """Test that metrics are properly tracked."""
        handler = AsyncMock()
        event_bus.subscribe("TestEvent", handler)

        await event_bus.publish(test_event)
        await asyncio.sleep(0.1)

        metrics = event_bus.get_metrics()
        assert metrics["events_published"] == 1
        assert metrics["events_processed"] == 1
        assert metrics["handler_invocations"] == 1
        assert metrics["handler_failure_rate"] == pytest.approx(0.0)
        assert "avg_latency" in metrics

    @pytest.mark.asyncio
    async def test_handler_failure_tracking(
        self, event_bus: InMemoryEventBus, test_event: TestEvent
    ) -> None:
        """Test that handler failures are tracked in metrics."""
        failing_handler = AsyncMock(side_effect=Exception("Handler failed"))
        event_bus.subscribe("TestEvent", failing_handler)

        await event_bus.publish(test_event)
        await asyncio.sleep(0.1)

        metrics = event_bus.get_metrics()
        assert metrics["handler_failures"] == 1
        assert metrics["handler_failure_rate"] == pytest.approx(1.0)

    @pytest.mark.asyncio
    async def test_circuit_breaker_open_on_failures(
        self, event_bus: InMemoryEventBus
    ) -> None:
        """Test circuit breaker opens after threshold failures."""
        failing_handler = AsyncMock(side_effect=Exception("Handler failed"))
        event_bus.subscribe("TestEvent", failing_handler)

        # Trigger failures
        for _ in range(3):
            try:
                await event_bus.publish(TestEvent("TestEvent"))
                await asyncio.sleep(0.1)
            except RuntimeError:
                pass  # Expected when circuit opens

        metrics = event_bus.get_metrics()
        assert metrics["circuit_breaker_state"] == "open"

    @pytest.mark.asyncio
    async def test_circuit_breaker_recovery(self, event_bus: InMemoryEventBus) -> None:
        """Test circuit breaker recovery after timeout."""
        failing_handler = AsyncMock(side_effect=Exception("Handler failed"))
        event_bus.subscribe("TestEvent", failing_handler)

        # Open circuit
        for _ in range(3):
            try:
                await event_bus.publish(TestEvent("TestEvent"))
                await asyncio.sleep(0.1)
            except RuntimeError:
                pass

        # Wait for recovery timeout
        await asyncio.sleep(1.1)

        # Should allow publish again (half-open)
        success_handler = AsyncMock()
        event_bus.subscribe("TestEvent", success_handler)

        await event_bus.publish(TestEvent("TestEvent"))
        await asyncio.sleep(0.1)

        metrics = event_bus.get_metrics()
        assert metrics["circuit_breaker_state"] == "closed"
        success_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_publish_many(self, event_bus: InMemoryEventBus) -> None:
        """Test publishing multiple events."""
        handler = AsyncMock()
        event_bus.subscribe("TestEvent", handler)

        events = [TestEvent("TestEvent", {"id": i}) for i in range(3)]
        await event_bus.publish_many(events)

        await asyncio.sleep(0.1)

        assert handler.call_count == 3

    def test_get_handler_count(self, event_bus: InMemoryEventBus) -> None:
        """Test getting handler count."""
        assert event_bus.get_handler_count("TestEvent") == 0

        event_bus.subscribe("TestEvent", AsyncMock())
        assert event_bus.get_handler_count("TestEvent") == 1

    @pytest.mark.asyncio
    async def test_queue_full_handling(self, event_bus: InMemoryEventBus) -> None:
        """Test handling when queue is full."""
        # Create bus with small queue
        small_bus = InMemoryEventBus(max_queue_size=1)

        # Fill queue
        await small_bus._queue.put(TestEvent("TestEvent"))
        # This should fail due to queue full
        await small_bus.publish(TestEvent("TestEvent"))

        # Should record failure
        assert small_bus._circuit_breaker["failures"] > 0

    @pytest.mark.asyncio
    async def test_shutdown(self, event_bus: InMemoryEventBus) -> None:
        """Test graceful shutdown."""
        handler = AsyncMock()
        event_bus.subscribe("TestEvent", handler)

        await event_bus.publish(TestEvent("TestEvent"))
        await event_bus.shutdown()

        # Processing task should be cancelled
        assert (
            event_bus._processing_task is None or event_bus._processing_task.cancelled()
        )
