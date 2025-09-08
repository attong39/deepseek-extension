"""
Unit tests for planning functionality.

Tests the planning domain entities, value objects, and use cases.
"""

from datetime import UTC, datetime
from uuid import uuid4

from core.domain.entities.plan import Plan, PlanStatus, PlanStep
import len
import result
import str


class TestPlanStep:
    """Test cases for PlanStep entity."""

    def test_create_plan_step(self):
        """Test creating a new plan step."""
        step = PlanStep(
            id="step-1",
            action="analyze_data",
            description="Analyze the input data",
            parameters={"data_source": "database", "format": "json"},
            order=1,
        )

        assert step.id == "step-1"
        assert step.action == "analyze_data"
        assert step.description == "Analyze the input data"
        assert step.parameters["data_source"] == "database"
        assert step.order == 1
        assert step.is_completed is False
        assert step.result is None

    def test_plan_step_with_result(self):
        """Test creating a plan step with result."""
        step = PlanStep(
            id="step-2",
            action="generate_report",
            description="Generate analysis report",
            parameters={"format": "pdf"},
            order=2,
            is_completed=True,
            result="Report generated successfully",
        )

        assert step.is_completed is True
        assert step.result == "Report generated successfully"


class TestPlan:
    """Test cases for Plan entity."""

    def test_create_plan(self):
        """Test creating a new plan."""
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
        assert plan.completed_at is None

    def test_add_step_to_plan(self):
        """Test adding a step to a plan."""
        plan = Plan(
            id=str(uuid4()),
            title="Test Plan",
            description="Test plan description",
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            steps=[],
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        step = PlanStep(
            id="step-1",
            action="test_action",
            description="Test step",
            parameters={"param": "value"},
            order=1,
        )

        plan.add_step(step)

        assert len(plan.steps) == 1
        assert plan.steps[0] == step

    def test_mark_step_completed(self):
        """Test marking a step as completed."""
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

    def test_get_next_step(self):
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

        step3 = PlanStep(
            id="step-3",
            action="third_action",
            description="Third step",
            parameters={},
            order=3,
            is_completed=False,
        )

        plan = Plan(
            id=str(uuid4()),
            title="Test Plan",
            description="Test plan description",
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            steps=[step1, step2, step3],
            status=PlanStatus.EXECUTING,
            created_at=datetime.now(UTC),
        )

        next_step = plan.get_next_step()

        assert next_step is not None
        assert next_step.id == "step-2"
        assert next_step.order == 2

    def test_get_next_step_when_all_completed(self):
        """Test getting next step when all steps are completed."""
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
            is_completed=True,
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

        assert next_step is None

    def test_is_plan_completed(self):
        """Test checking if plan is completed."""
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

        # Plan should not be completed with incomplete steps
        assert plan.is_completed() is False

        # Complete the remaining step
        plan.mark_step_completed("step-2", "Step 2 completed")

        # Now plan should be completed
        assert plan.is_completed() is True


class TestPlanStatus:
    """Test cases for PlanStatus enum."""

    def test_plan_status_values(self):
        """Test PlanStatus enum values."""
        assert PlanStatus.DRAFT.value == "draft"
        assert PlanStatus.ACTIVE.value == "active"
        assert PlanStatus.EXECUTING.value == "executing"
        assert PlanStatus.COMPLETED.value == "completed"
        assert PlanStatus.FAILED.value == "failed"
        assert PlanStatus.CANCELLED.value == "cancelled"


class TestPlanBusinessLogic:
    """Test cases for plan business logic and workflows."""

    def test_plan_execution_workflow(self):
        """Test complete plan execution workflow."""
        # Create a plan with multiple steps
        steps = [
            PlanStep(
                id="step-1",
                action="initialize",
                description="Initialize the process",
                parameters={"config": "default"},
                order=1,
            ),
            PlanStep(
                id="step-2",
                action="process_data",
                description="Process the input data",
                parameters={"batch_size": 100},
                order=2,
            ),
            PlanStep(
                id="step-3",
                action="finalize",
                description="Finalize the process",
                parameters={"output_format": "json"},
                order=3,
            ),
        ]

        plan = Plan(
            id=str(uuid4()),
            title="Data Processing Plan",
            description="Complete data processing workflow",
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            steps=steps,
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        # Initially, plan should not be completed
        assert plan.is_completed() is False

        # First step should be the next to execute
        next_step = plan.get_next_step()
        assert next_step is not None
        assert next_step.id == "step-1"

        # Complete first step
        plan.mark_step_completed("step-1", "Initialization completed")

        # Second step should now be next
        next_step = plan.get_next_step()
        assert next_step is not None
        assert next_step.id == "step-2"

        # Complete second step
        plan.mark_step_completed("step-2", "Data processing completed")

        # Third step should now be next
        next_step = plan.get_next_step()
        assert next_step is not None
        assert next_step.id == "step-3"

        # Complete final step
        plan.mark_step_completed("step-3", "Process finalized")

        # Plan should now be completed
        assert plan.is_completed() is True

        # No next step should be available
        next_step = plan.get_next_step()
        assert next_step is None

    def test_plan_with_unordered_steps(self):
        """Test plan execution with steps added in wrong order."""
        # Add steps in wrong order
        steps = [
            PlanStep(
                id="step-3",
                action="finalize",
                description="Finalize the process",
                parameters={},
                order=3,
            ),
            PlanStep(
                id="step-1",
                action="initialize",
                description="Initialize the process",
                parameters={},
                order=1,
            ),
            PlanStep(
                id="step-2",
                action="process",
                description="Process the data",
                parameters={},
                order=2,
            ),
        ]

        plan = Plan(
            id=str(uuid4()),
            title="Unordered Plan",
            description="Plan with unordered steps",
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            steps=steps,
            status=PlanStatus.ACTIVE,
            created_at=datetime.now(UTC),
        )

        # Should still get steps in correct order
        next_step = plan.get_next_step()
        assert next_step is not None
        assert next_step.id == "step-1"  # Should be first by order, not by addition
        assert next_step.order == 1

    def test_empty_plan(self):
        """Test plan with no steps."""
        plan = Plan(
            id=str(uuid4()),
            title="Empty Plan",
            description="Plan with no steps",
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            steps=[],
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        # Empty plan should be considered completed
        assert plan.is_completed() is True

        # No next step should be available
        next_step = plan.get_next_step()
        assert next_step is None

    def test_mark_nonexistent_step_completed(self):
        """Test marking a non-existent step as completed."""
        step = PlanStep(
            id="step-1",
            action="test_action",
            description="Test step",
            parameters={},
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

        # Mark non-existent step as completed (should not raise error)
        plan.mark_step_completed("non-existent", "Some result")

        # Original step should remain unchanged
        assert step.is_completed is False
        assert step.result is None
