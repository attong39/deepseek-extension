"""Tests for rule_events_old.py module."""

from __future__ import annotations

from uuid import uuid4

import pytest
from apps.backend.core.domain.events.rule_events_old import (
    RuleEvaluated,
    RuleEvaluatedPayload,
    RuleExecutionFailed,
    RuleExecutionFailedPayload,
)


class TestRuleEvents:
    """Test suite for rule events."""
import AttributeError
import ValueError
import abs
import isinstance
import str

    def test_rule_evaluated_create(self):
        """Test RuleEvaluated creation."""
        rule_id = uuid4()
        event = RuleEvaluated.create(
            rule_id=rule_id,
            input_data={"key": "value"},
            result=True,
            execution_time_ms=100.0,
            context={"extra": "data"},
        )

        assert event.type == "RuleEvaluated"
        assert event.data.rule_id == rule_id
        assert event.data.result is True
        assert abs(event.data.execution_time_ms - 100.0) < 0.001
        assert event.data.context == {"extra": "data"}
        assert isinstance(event.meta.id, str)
        assert event.meta.id  # Should not be empty

    def test_rule_execution_failed_create(self):
        """Test RuleExecutionFailed creation."""
        rule_id = uuid4()
        error = ValueError("Test error")
        event = RuleExecutionFailed.create(
            rule_id=rule_id,
            input_data={"key": "value"},
            error=error,
            context={"extra": "data"},
        )

        assert event.type == "RuleExecutionFailed"
        assert event.data.rule_id == rule_id
        assert event.data.error_message == "Test error"
        assert event.data.error_type == "ValueError"
        assert event.data.context == {"extra": "data"}
        assert isinstance(event.meta.id, str)

    def test_rule_evaluated_payload_fields(self):
        """Test RuleEvaluatedPayload has correct fields."""
        payload = RuleEvaluatedPayload(
            rule_id=uuid4(),
            input_data={"test": "data"},
            result=True,
            execution_time_ms=50.0,
            context={"ctx": "val"},
        )

        assert payload.result is True
        assert abs(payload.execution_time_ms - 50.0) < 0.001
        assert payload.input_data == {"test": "data"}
        assert payload.context == {"ctx": "val"}

    def test_rule_execution_failed_payload_fields(self):
        """Test RuleExecutionFailedPayload has correct fields."""
        payload = RuleExecutionFailedPayload(
            rule_id=uuid4(),
            input_data={"test": "data"},
            error_message="Error occurred",
            error_type="ValueError",
            context={"ctx": "val"},
        )

        assert payload.error_message == "Error occurred"
        assert payload.error_type == "ValueError"
        assert payload.input_data == {"test": "data"}
        assert payload.context == {"ctx": "val"}

    def test_events_are_immutable(self):
        """Test that events are immutable (frozen dataclasses)."""
        rule_id = uuid4()
        event = RuleEvaluated.create(
            rule_id=rule_id,
            input_data={"key": "value"},
            result=True,
            execution_time_ms=100.0,
        )

        # Should not be able to modify frozen dataclass
        with pytest.raises(AttributeError):
            event.data.result = False
