import os
import isinstance
import len
import result

"""Basic unit tests for automation value objects and factory.

This test ensures that all automation components can be instantiated
and basic functionality works as expected.
"""

from datetime import datetime
from uuid import UUID

import pytest
from apps.backend.core.domain.value_objects.automation import (
    ActionType,
    AutomationPlan,
    AutomationStep,
    BBox,
    Point,
    SafetyConfig,
    SafetyResult,
    StepResult,
)

from data.factories.automation_factory import AutomationFactory


class TestAutomationValueObjects:
    """Test automation value objects."""

    def test_point_creation(self) -> None:
        """Test Point value object creation."""
        point = Point(x=100, y=200)
        assert point.x == 100
        assert point.y == 200

    def test_bbox_creation(self) -> None:
        """Test BBox value object creation."""
        bbox = BBox(x=10, y=20, w=100, h=50)
        assert bbox.x == 10
        assert bbox.y == 20
        assert bbox.w == 100
        assert bbox.h == 50

    def test_bbox_center(self) -> None:
        """Test BBox center calculation."""
        bbox = BBox(x=10, y=20, w=100, h=50)
        center = bbox.center()
        assert center.x == 60  # 10 + 100/2
        assert center.y == 45  # 20 + 50/2

    def test_automation_step_creation(self) -> None:
        """Test AutomationStep creation."""
        step = AutomationStep(
            action=ActionType.CLICK,
            target_text="Login",
            coords=Point(100, 200),
        )
        assert step.action == ActionType.CLICK
        assert step.target_text == "Login"
        assert step.coords is not None
        assert step.coords.x == 100
        assert step.coords.y == 200

    def test_automation_plan_creation(self) -> None:
        """Test AutomationPlan creation."""
        plan = AutomationPlan.create(
            goal="Login to application",
            context="Test environment",
        )
        assert plan.goal == "Login to application"
        assert plan.context == "Test environment"
        assert isinstance(plan.id, UUID)
        assert isinstance(plan.created_at, datetime)
        assert plan.steps == []

    def test_step_result_success(self) -> None:
        """Test successful StepResult creation."""
        _ = StepResult.success_result(
            step_id=1,
            message="Click successful",
            execution_time_ms=250,
        )
        assert result.step_id == 1
        assert result.success is True
        assert result.message == "Click successful"
        assert result.execution_time_ms == 250

    def test_step_result_failure(self) -> None:
        """Test failed StepResult creation."""
        _ = StepResult.failure_result(
            step_id=2,
            message="Element not found",
            error_details="Target text 'Login' not visible",
        )
        assert result.step_id == 2
        assert result.success is False
        assert result.message == "Element not found"
        assert result.error_details == "Target text 'Login' not visible"

    def test_safety_config_creation(self) -> None:
        """Test SafetyConfig creation."""
        config = SafetyConfig(
            allowed_apps=["notepad.exe", "calculator.exe"],
            danger_zones=[BBox(0, 0, 100, 100)],
            max_actions_per_minute=20,
        )
        assert len(config.allowed_apps) == 2
        assert config.max_actions_per_minute == 20

    def test_safety_result_safe(self) -> None:
        """Test SafetyResult safe creation."""
        _ = SafetyResult.safe(warnings=["Minor delay detected"])
        assert result.is_safe is True
        assert len(result.warnings) == 1
        assert result.recommended_action == "proceed"

    def test_safety_result_unsafe(self) -> None:
        """Test SafetyResult unsafe creation."""
        _ = SafetyResult.unsafe(
            violations=["Danger zone detected"],
            recommended_action="stop immediately",
        )
        assert result.is_safe is False
        assert len(result.violations) == 1
        assert result.recommended_action == "stop immediately"


class TestAutomationFactory:
    """Test automation factory."""

    def test_factory_creation(self) -> None:
        """Test factory creation requires OpenAI API key."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        assert factory is not None

    def test_factory_creates_screen_perception(self) -> None:
        """Test factory creates screen perception service."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        perception = factory.create_screen_perception()
        assert perception is not None

    def test_factory_creates_input_controller(self) -> None:
        """Test factory creates input controller."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        input_ctrl = factory.create_input_controller()
        assert input_ctrl is not None

    def test_factory_creates_planner(self) -> None:
        """Test factory creates automation planner."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        planner = factory.create_automation_planner()
        assert planner is not None

    def test_factory_creates_executor(self) -> None:
        """Test factory creates automation executor."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        executor = factory.create_automation_executor()
        assert executor is not None

    def test_factory_creates_safety_engine(self) -> None:
        """Test factory creates safety engine."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        safety = factory.create_safety_engine()
        assert safety is not None

    def test_factory_creates_automation_service(self) -> None:
        """Test factory creates complete automation service."""
        factory = AutomationFactory(openai_api_key=os.getenv("API_KEY"))
        service = factory.create_automation_service()
        assert service is not None


if __name__ == "__main__":
    pytest.main([__file__])
