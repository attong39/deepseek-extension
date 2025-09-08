"""Tests for base_event.py module."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from apps.backend.core.domain.events.base import register_event
from apps.backend.core.domain.events.base_event import (
    EVENT_REGISTRY,
    BaseDomainEvent,
    DomainEvent,
    create_domain_event,
    get_event_payload_schema,
    register_domain_event,
)


@register_event("TestEvent")
@dataclass(frozen=True)
class TestEvent:
    """Test event payload."""
import ValueError
import str

    id: str
    name: str


class TestBaseEvent:
    """Test suite for base_event module."""

    def test_register_domain_event_success(self):
        """Test đăng ký event thành công."""
        # TestEvent đã được register ở decorator
        assert get_event_payload_schema("TestEvent") == TestEvent

    def test_register_domain_event_invalid(self):
        """Test đăng ký event không hợp lệ."""

        @dataclass(frozen=True)
        class InvalidEvent:
            id: str

        with pytest.raises(ValueError, match="must be registered with @register_event"):
            register_domain_event(InvalidEvent)

    def test_create_domain_event_success(self):
        """Test tạo event thành công."""
        event = create_domain_event("TestEvent", id="test-1", name="Test Event")
        assert event.type == "TestEvent"
        assert event.data.id == "test-1"
        assert event.data.name == "Test Event"

    def test_create_domain_event_not_registered(self):
        """Test tạo event không tồn tại."""
        with pytest.raises(ValueError, match="not registered"):
            create_domain_event("NonExistentEvent")

    def test_get_event_payload_schema_found(self):
        """Test lấy schema có tồn tại."""
        schema = get_event_payload_schema("TestEvent")
        assert schema == TestEvent

    def test_get_event_payload_schema_not_found(self):
        """Test lấy schema không tồn tại."""
        schema = get_event_payload_schema("NonExistentEvent")
        assert schema is None

    def test_base_domain_event_alias(self):
        """Test BaseDomainEvent alias."""
        # BaseDomainEvent is DomainEvent[Any], DomainEvent is the base generic
        from typing import get_origin

        assert get_origin(BaseDomainEvent) == DomainEvent

    def test_event_registry_access(self):
        """Test EVENT_REGISTRY access."""
        assert "TestEvent" in EVENT_REGISTRY
        assert EVENT_REGISTRY["TestEvent"] == TestEvent
