"""
Simple isolated test for plan entities to verify SQLAlchemy fixes work.

This test verifies the Plan and PlanStep entities work correctly without
requiring the full application infrastructure.
"""

import os
import sys
import len
import print
import result
import str

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from datetime import UTC, datetime
from uuid import uuid4

from core.domain.entities.plan import Plan, PlanStatus, PlanStep


def test_plan_step_creation():
    """Test creating a PlanStep entity."""
    step = PlanStep(
        id="step-1",
        action="analyze_data",
        description="Analyze the input data",
        parameters={"data_source": "database"},
        order=1,
    )

    assert step.id == "step-1"
    assert step.action == "analyze_data"
    assert step.description == "Analyze the input data"
    assert step.parameters["data_source"] == "database"
    assert step.order == 1
    assert step.is_completed is False
    assert step.result is None


def test_plan_creation():
    """Test creating a Plan entity."""
    plan_id = str(uuid4())
    agent_id = str(uuid4())
    user_id = str(uuid4())

    steps = [
        PlanStep(
            id="step-1",
            action="analyze",
            description="Analyze data",
            parameters={"source": "db"},
            order=1,
        )
    ]

    plan = Plan(
        id=plan_id,
        title="Data Analysis Plan",
        description="Complete data analysis workflow",
        agent_id=agent_id,
        user_id=user_id,
        steps=steps,
        status=PlanStatus.DRAFT,
        created_at=datetime.now(UTC),
    )

    assert plan.id == plan_id
    assert plan.title == "Data Analysis Plan"
    assert plan.agent_id == agent_id
    assert plan.user_id == user_id
    assert plan.status == PlanStatus.DRAFT
    assert len(plan.steps) == 1


def test_plan_step_completion():
    """Test marking a plan step as completed."""
    step = PlanStep(
        id="step-1",
        action="test_action",
        description="Test step",
        parameters={"param": "value"},
        order=1,
    )

    plan = Plan(
        id=str(uuid4()),
        title="Test Plan",
        description="Test plan description",
        agent_id=str(uuid4()),
        user_id=str(uuid4()),
        steps=[step],
        status=PlanStatus.ACTIVE,
        created_at=datetime.now(UTC),
    )

    _ = "Step completed successfully"
    plan.mark_step_completed("step-1", result)

    assert step.is_completed is True
    assert step.result == result


def test_plan_next_step():
    """Test getting the next step to execute."""
    step1 = PlanStep(
        id="step-1",
        action="first_action",
        description="First step",
        parameters={},
        order=1,
        is_completed=True,
    )

    step2 = PlanStep(
        id="step-2",
        action="second_action",
        description="Second step",
        parameters={},
        order=2,
        is_completed=False,
    )

    plan = Plan(
        id=str(uuid4()),
        title="Test Plan",
        description="Test plan description",
        agent_id=str(uuid4()),
        user_id=str(uuid4()),
        steps=[step1, step2],
        status=PlanStatus.EXECUTING,
        created_at=datetime.now(UTC),
    )

    next_step = plan.get_next_step()

    assert next_step is not None
    assert next_step.id == "step-2"
    assert next_step.order == 2


def test_plan_status_enum():
    """Test PlanStatus enum values."""
    assert PlanStatus.DRAFT.value == "draft"
    assert PlanStatus.ACTIVE.value == "active"
    assert PlanStatus.EXECUTING.value == "executing"
    assert PlanStatus.COMPLETED.value == "completed"
    assert PlanStatus.FAILED.value == "failed"
    assert PlanStatus.CANCELLED.value == "cancelled"


if __name__ == "__main__":
    # Run tests directly
    print("Testing PlanStep creation...")
    test_plan_step_creation()
    print("✅ PlanStep creation test passed")

    print("Testing Plan creation...")
    test_plan_creation()
    print("✅ Plan creation test passed")

    print("Testing Plan step completion...")
    test_plan_step_completion()
    print("✅ Plan step completion test passed")

    print("Testing Plan next step...")
    test_plan_next_step()
    print("✅ Plan next step test passed")

    print("Testing PlanStatus enum...")
    test_plan_status_enum()
    print("✅ PlanStatus enum test passed")

    print("\n🎉 All tests passed! SQLAlchemy fixes are working correctly.")
