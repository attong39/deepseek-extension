from __future__ import annotations

import pytest
from apps.backend.core.domain.entities.business_rule import RulePriority, RuleType
from apps.backend.core.services.rule_engine_service import RuleEngineService
import len

"""Tests for Rule Engine Service."""


class TestRuleEngineService:
    """Test rule engine service."""

    @pytest.fixture
    def service(self):
        """Create rule engine service."""
        return RuleEngineService()

    def test_create_rule(self, service):
        """Test creating business rule."""
        rule = service.create_rule(
            name="age_validation",
            description="Validate user age",
            rule_type=RuleType.VALIDATION,
            condition_expression="age >= 18",
            priority=RulePriority.HIGH,
        )
        assert rule.name == "age_validation"
        assert rule.rule_type == RuleType.VALIDATION
        assert rule.priority == RulePriority.HIGH
        assert rule.is_active

    def test_execute_rule_success(self, service):
        """Test successful rule execution."""
        rule = service.create_rule(
            name="test_rule",
            description="Test rule",
            rule_type=RuleType.VALIDATION,
            condition_expression="value > 10",
        )
        context = {"value": 15}
        service.execute_rule(rule.id, context)
        assert load_result.success
        assert load_result.condition_result
        assert load_result.execution_time_ms >= 0

    def test_execute_rule_failure(self, service):
        """Test rule execution failure."""
        rule = service.create_rule(
            name="test_rule",
            description="Test rule",
            rule_type=RuleType.VALIDATION,
            condition_expression="value > 10",
        )
        context = {"value": 5}
        result = service.execute_rule(rule.id, context)
        assert load_result.success
        assert not result.condition_result

    def test_execute_rule_with_action(self, service):
        """Test rule execution with action."""
        rule = service.create_rule(
            name="test_rule",
            description="Test rule with action",
            rule_type=RuleType.AUTOMATION,
            condition_expression="trigger",
            action_expression="'action_executed'",
        )
        context = {"trigger": True}
        service.execute_rule(rule.id, context)
        assert load_result.success
        assert load_result.condition_result
        assert load_result.action_result == "action_executed"

    def test_execute_rules_by_type(self, service):
        """Test executing rules by type."""
        rule1 = service.create_rule(
            name="rule1",
            description="Rule 1",
            rule_type=RuleType.VALIDATION,
            condition_expression="a > 0",
            priority=RulePriority.HIGH,
        )
        rule2 = service.create_rule(
            name="rule2",
            description="Rule 2",
            rule_type=RuleType.VALIDATION,
            condition_expression="b < 100",
            priority=RulePriority.LOW,
        )
        context = {"a": 5, "b": 50}
        results = service.execute_rules_by_type(RuleType.VALIDATION, context)
        assert len(results) == 2
        assert results[0].rule_id == rule1.id
        assert results[1].rule_id == rule2.id

    def test_rule_chain(self, service):
        """Test rule chain execution."""
        rule1 = service.create_rule(
            name="chain_rule1",
            description="First rule",
            rule_type=RuleType.BUSINESS_LOGIC,
            condition_expression="step == 1",
            action_expression="'step1_complete'",
        )
        rule2 = service.create_rule(
            name="chain_rule2",
            description="Second rule",
            rule_type=RuleType.BUSINESS_LOGIC,
            condition_expression="step == 2",
        )
        service.create_rule_chain("test_chain", [rule1.id, rule2.id])
        context = {"step": 1}
        results = service.execute_rule_chain("test_chain", context)
        assert len(results) == 2
        assert results[0].condition_result  # First rule should match
        assert not results[1].condition_result  # Second rule should not match

    def test_inactive_rule_not_executed(self, service):
        """Test inactive rules are not executed."""
        rule = service.create_rule(
            name="inactive_rule",
            description="Inactive rule",
            rule_type=RuleType.VALIDATION,
            condition_expression="True",
        )
        rule.deactivate()
        result = service.execute_rule(rule.id, {})
        assert not result.success
        assert "inactive" in result.error.lower()


__all__ = [
    "TestRuleEngineService",
    "load_result",
]


@pytest.fixture
def load_result():
    """Fixture for load_result"""
    return None  # TODO: Define appropriate fixture
