"""Unit tests for InMemoryAlerts adapter.

This module contains comprehensive unit tests for the InMemoryAlerts
adapter, covering all public methods and edge cases.
"""

from __future__ import annotations

import pytest
from apps.backend.core.adapters.inmemory_alerts import Alert, InMemoryAlerts
import AttributeError
import ValueError
import len
import level
import str


class TestAlert:
    """Test cases for the Alert dataclass."""

    def test_alert_creation(self) -> None:
        """Test creating an alert with valid data."""
        alert = Alert(
            level="warning",
            message="Test message",
            context={"key": "value"},
        )
        assert alert.level == "warning"
        assert alert.message == "Test message"
        assert alert.context == {"key": "value"}

    def test_alert_immutable(self) -> None:
        """Test that Alert instances are immutable."""
        alert = Alert(level="info", message="test", context={})
        with pytest.raises(AttributeError):
            alert.level = "error"  # type: ignore


class TestInMemoryAlerts:
    """Test cases for the InMemoryAlerts adapter."""

    def test_initialization(self) -> None:
        """Test adapter initialization."""
        adapter = InMemoryAlerts()
        assert adapter.list() == []
        assert adapter.count_by_level("info") == 0

    def test_add_valid_alert(self) -> None:
        """Test adding a valid alert."""
        adapter = InMemoryAlerts()
        adapter.add("info", "Test message", key="value")

        alerts = adapter.list()
        assert len(alerts) == 1
        assert alerts[0].level == "info"
        assert alerts[0].message == "Test message"
        assert alerts[0].context == {"key": "value"}

    def test_add_alert_with_empty_level(self) -> None:
        """Test adding alert with empty level raises ValueError."""
        adapter = InMemoryAlerts()
        with pytest.raises(ValueError, match="Alert level must be a non-empty string"):
            adapter.add("", "message")

    def test_add_alert_with_empty_message(self) -> None:
        """Test adding alert with empty message raises ValueError."""
        adapter = InMemoryAlerts()
        with pytest.raises(
            ValueError, match="Alert message must be a non-empty string"
        ):
            adapter.add("info", "")

    def test_add_multiple_alerts(self) -> None:
        """Test adding multiple alerts."""
        adapter = InMemoryAlerts()
        adapter.add("info", "First message")
        adapter.add("warning", "Second message")
        adapter.add("error", "Third message")

        alerts = adapter.list()
        assert len(alerts) == 3
        assert {alert.level for alert in alerts} == {"info", "warning", "error"}

    def test_list_returns_copy(self) -> None:
        """Test that list() returns a copy, not the original list."""
        adapter = InMemoryAlerts()
        adapter.add("info", "test")

        alerts = adapter.list()
        alerts.clear()  # Modify the returned list

        # Original should still have the alert
        assert len(adapter.list()) == 1

    def test_clear_alerts(self) -> None:
        """Test clearing all alerts."""
        adapter = InMemoryAlerts()
        adapter.add("info", "test1")
        adapter.add("warning", "test2")

        assert len(adapter.list()) == 2

        adapter.clear()
        assert len(adapter.list()) == 0

    def test_count_by_level(self) -> None:
        """Test counting alerts by level."""
        adapter = InMemoryAlerts()
        adapter.add("info", "msg1")
        adapter.add("info", "msg2")
        adapter.add("warning", "msg3")

        assert adapter.count_by_level("info") == 2
        assert adapter.count_by_level("warning") == 1
        assert adapter.count_by_level("error") == 0

    def test_count_by_level_with_no_alerts(self) -> None:
        """Test counting by level when no alerts exist."""
        adapter = InMemoryAlerts()
        assert adapter.count_by_level("any_level") == 0

    @pytest.mark.parametrize("level", ["info", "warning", "error", "debug"])
    def test_add_various_levels(self, level: str) -> None:
        """Test adding alerts with various valid levels."""
        adapter = InMemoryAlerts()
        adapter.add(level, f"Message for {level}")
        assert adapter.count_by_level(level) == 1

    def test_context_preservation(self) -> None:
        """Test that context dictionaries are properly preserved."""
        context = {"user_id": 123, "action": "login", "ip": "192.168.1.1"}
        adapter = InMemoryAlerts()
        adapter.add("security", "Login attempt", **context)

        alerts = adapter.list()
        assert alerts[0].context == context

    def test_empty_context(self) -> None:
        """Test adding alert with no additional context."""
        adapter = InMemoryAlerts()
        adapter.add("info", "Simple message")

        alerts = adapter.list()
        assert alerts[0].context == {}
