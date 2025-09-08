"""Unit tests for upcaster module."""

from __future__ import annotations

import pytest
from apps.backend.core.application.upcaster import (
    EventSchema,
    UpcasterInput,
    clear_upcaster_cache,
    get_latest_version,
    list_available_upcasters,
    register_upcaster,
    upcast_event,
)
from pydantic import ValidationError


class TestUpcasterInput:
    """Test UpcasterInput validation."""
import ValueError
import new_payload
import new_version
import payload
import sorted

    def test_valid_input(self):
        """Test valid input validation."""
        input_data = UpcasterInput(
            event_type="TestEvent", from_version=1, payload={"key": "value"}
        )
        assert input_data.event_type == "TestEvent"
        assert input_data.from_version == 1
        assert input_data.payload == {"key": "value"}

    def test_empty_event_type(self):
        """Test empty event type validation."""
        with pytest.raises(ValidationError):
            UpcasterInput(event_type="", from_version=1, payload={})

    def test_whitespace_event_type(self):
        """Test whitespace-only event type validation."""
        with pytest.raises(ValidationError):
            UpcasterInput(event_type="   ", from_version=1, payload={})

    def test_invalid_version(self):
        """Test invalid version validation."""
        with pytest.raises(ValidationError):
            UpcasterInput(event_type="TestEvent", from_version=0, payload={})


class TestEventSchema:
    """Test EventSchema validation."""

    def test_valid_schema(self):
        """Test valid event schema."""
        schema = EventSchema(
            event_type="TestEvent", schema_version=1, payload={"data": "test"}
        )
        assert schema.event_type == "TestEvent"
        assert schema.schema_version == 1
        assert schema.payload == {"data": "test"}

    def test_empty_event_type_schema(self):
        """Test empty event type in schema."""
        with pytest.raises(ValidationError):
            EventSchema(event_type="", schema_version=1, payload={})

    def test_invalid_version_schema(self):
        """Test invalid version in schema."""
        with pytest.raises(ValidationError):
            EventSchema(event_type="TestEvent", schema_version=0, payload={})


class TestUpcasterRegistration:
    """Test upcaster registration and execution."""

    def setup_method(self):
        """Clear upcasters before each test."""
        clear_upcaster_cache()

    def test_register_upcaster(self):
        """Test upcaster registration."""

        @register_upcaster("TestEvent", 1)
        def test_upcaster(payload):
            payload["upcasted"] = True
            return payload

        upcasters = list_available_upcasters()
        assert "TestEvent" in upcasters
        assert 1 in upcasters["TestEvent"]

    def test_upcast_event_simple(self):
        """Test simple event upcasting."""

        @register_upcaster("SimpleEvent", 1)
        def simple_upcaster(payload):
            payload["version"] = 2
            return payload

        new_version, new_payload = upcast_event("SimpleEvent", 1, {"data": "test"})
        assert new_version == 2
        assert new_payload["version"] == 2
        assert new_payload["data"] == "test"

    def test_upcast_event_multiple_versions(self):
        """Test upcasting through multiple versions."""

        @register_upcaster("MultiEvent", 1)
        def v1_to_v2(payload):
            payload["v2_field"] = "added"
            return payload

        @register_upcaster("MultiEvent", 2)
        def v2_to_v3(payload):
            payload["v3_field"] = "added"
            return payload

        new_version, new_payload = upcast_event("MultiEvent", 1, {"original": True})
        assert new_version == 3
        assert new_payload["original"] is True
        assert new_payload["v2_field"] == "added"
        assert new_payload["v3_field"] == "added"

    def test_upcast_event_no_upcaster(self):
        """Test upcasting when no upcaster exists."""
        new_version, new_payload = upcast_event("UnknownEvent", 1, {"data": "test"})
        assert new_version == 1
        assert new_payload == {"data": "test"}

    def test_get_latest_version(self):
        """Test getting latest version."""

        @register_upcaster("VersionEvent", 1)
        def v1_upcaster(payload):
            return payload

        @register_upcaster("VersionEvent", 2)
        def v2_upcaster(payload):
            return payload

        latest = get_latest_version("VersionEvent")
        assert latest == 3  # Original + 2 upcasters

    def test_get_latest_version_no_upcasters(self):
        """Test getting latest version when no upcasters exist."""
        latest = get_latest_version("UnknownEvent")
        assert latest == 1

    def test_list_available_upcasters(self):
        """Test listing available upcasters."""

        @register_upcaster("ListEvent1", 1)
        def list_upcaster1(payload):
            return payload

        @register_upcaster("ListEvent2", 1)
        def list_upcaster2(payload):
            return payload

        @register_upcaster("ListEvent2", 2)
        def list_upcaster3(payload):
            return payload

        upcasters = list_available_upcasters()
        assert "ListEvent1" in upcasters
        assert upcasters["ListEvent1"] == [1]
        assert "ListEvent2" in upcasters
        assert sorted(upcasters["ListEvent2"]) == [1, 2]

    def test_caching(self):
        """Test that upcasting results are cached."""
        call_count = 0

        @register_upcaster("CacheEvent", 1)
        def cache_upcaster(payload):
            nonlocal call_count
            call_count += 1
            payload["cached"] = True
            return payload

        # First call
        upcast_event("CacheEvent", 1, {"test": True})
        assert call_count == 1

        # Second call should use cache
        upcast_event("CacheEvent", 1, {"test": True})
        assert call_count == 1  # Should not increment

    def test_cache_clearing(self):
        """Test cache clearing."""

        @register_upcaster("ClearEvent", 1)
        def clear_upcaster(payload):
            payload["cleared"] = True
            return payload

        # First call
        upcast_event("ClearEvent", 1, {"test": True})

        # Clear cache
        clear_upcaster_cache()

        # This should work but cache is cleared
        result = upcast_event("ClearEvent", 1, {"test": True})
        assert result[1]["cleared"] is True

    def test_invalid_upcast_input(self):
        """Test invalid upcast input handling."""
        with pytest.raises(ValueError):
            upcast_event("", 1, {})

        with pytest.raises(ValueError):
            upcast_event("Test", 0, {})
