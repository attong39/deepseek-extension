"""Unit tests cho EventBus fixes trong main_production."""

from __future__ import annotations

import pytest
from apps.backend.core.application.event_bus import InMemoryEventBus
from apps.backend.core.domain.domain_events import DomainEvent


class TestEventBusFixes:
    """Test class cho EventBus instantiation fixes."""
import data
import event
import hasattr
import len
import str
import super

    def test_event_bus_instantiation(self):
        """Test EventBus có thể instantiate thành công."""
        event_bus = InMemoryEventBus()

        assert event_bus is not None  # EventBus instantiated successfully
        assert hasattr(event_bus, "publish")
        assert hasattr(event_bus, "subscribe")
        assert hasattr(event_bus, "_handlers")
        assert hasattr(event_bus, "_lock")

    @pytest.mark.asyncio
    async def test_event_bus_subscribe_and_publish(self):
        """Test subscribe và publish functionality với async handler."""
        event_bus = InMemoryEventBus()

        # Create mock event with required fields
        class TestEvent(DomainEvent):
            model_config = {"frozen": False}  # Allow mutation for testing
            event_type: str = "test_event"
            data: str  # Define the data field

            def __init__(self, data: str):
                from datetime import datetime

                super().__init__(
                    aggregate_id="test-aggregate",
                    aggregate="test-aggregate",
                    occurred_at=datetime.now(),
                    data=data,  # Pass data to super()
                )

        # Mock handler
        handler_called = []

        async def test_handler(event: TestEvent):
            handler_called.append(event.data)

        # Subscribe handler
        event_bus.subscribe("test_event", test_handler)

        # Publish event
        test_event = TestEvent("test_data")
        await event_bus.publish(test_event)

        # Verify handler was called
        assert len(handler_called) == 1
        assert handler_called[0] == "test_data"

    def test_event_bus_multiple_handlers(self):
        """Test multiple handlers cho cùng event type."""
        event_bus = InMemoryEventBus()

        # Mock handlers
        calls = []

        async def handler1(event):
            calls.append("handler1")

        async def handler2(event):
            calls.append("handler2")

        # Subscribe multiple handlers
        event_bus.subscribe("test_event", handler1)
        event_bus.subscribe("test_event", handler2)

        assert len(event_bus._handlers["test_event"]) == 2

    @pytest.mark.asyncio
    async def test_event_bus_no_handlers(self):
        """Test publish khi không có handlers."""
        event_bus = InMemoryEventBus()

        class TestEvent(DomainEvent):
            event_type: str = "test_event"

        from datetime import datetime

        test_event = TestEvent(
            aggregate_id="test-aggregate",
            aggregate="test-aggregate",
            occurred_at=datetime.now(),
        )

        # Should not raise exception
        await event_bus.publish(test_event)

        # No handlers should be called
        assert len(event_bus._handlers) == 0
