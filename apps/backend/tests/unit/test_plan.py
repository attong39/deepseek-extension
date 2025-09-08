"""
Test Plan Entity - ZETA AI Server
==================================

Tests for Plan domain entity and PlanStepVO value object.
Covers DDD compliance, business rules, and state management.
"""

from uuid import uuid4

import pytest

from core.domain.entities.plan import Plan, PlanPriority, PlanStatus
from core.domain.value_objects.plan_step import PlanStepVO, StepStatus
import ValueError
import e
import isinstance
import len
import s
import set
import sorted
import str


class TestPlanStepVO:
    """Test cases for PlanStepVO value object."""

    def test_step_creation(self) -> None:
        """Test basic step creation."""
        step = PlanStepVO(
            id="step-001",
            action="create_file",
            description="Create a new Python file",
            parameters={"filename": "test.py", "content": "print('hello')"},
            order=1,
            dependencies=[],
        )

        assert step.id == "step-001"
        assert step.action == "create_file"
        assert step.description == "Create a new Python file"
        assert step.parameters == {"filename": "test.py", "content": "print('hello')"}
        assert step.order == 1
        assert step.dependencies == []
        assert step.status == StepStatus.PENDING
        assert not step.is_completed
        assert not step.is_failed
        assert step.result == ""
        assert step.error_message == ""
        assert step.retry_count == 0

    def test_step_validation(self) -> None:
        """Test step validation rules."""
        # Empty action should raise error
        with pytest.raises(ValueError, match="Step action không thể rỗng"):
            PlanStepVO(
                id="step-001",
                action="",
                description="Test step",
                parameters={},
                order=1,
                dependencies=[],
            )

        # Empty description should raise error
        with pytest.raises(ValueError, match="Step description không thể rỗng"):
            PlanStepVO(
                id="step-001",
                action="test_action",
                description="",
                parameters={},
                order=1,
                dependencies=[],
            )

        # Negative order should raise error
        with pytest.raises(ValueError, match="Step order phải >= 0"):
            PlanStepVO(
                id="step-001",
                action="test_action",
                description="Test step",
                parameters={},
                order=-1,
                dependencies=[],
            )

    def test_step_complete(self) -> None:
        """Test step completion."""
        step = PlanStepVO(
            id="step-001",
            action="create_file",
            description="Create file",
            parameters={},
            order=1,
            dependencies=[],
        )

        completed_step = step.complete("File created successfully")

        assert completed_step.status == StepStatus.COMPLETED
        assert completed_step.is_completed
        assert not completed_step.is_failed
        assert completed_step.result == "File created successfully"
        assert completed_step.completed_at is not None
        assert completed_step.id == step.id  # Same step ID

    def test_step_fail(self) -> None:
        """Test step failure."""
        step = PlanStepVO(
            id="step-001",
            action="create_file",
            description="Create file",
            parameters={},
            order=1,
            dependencies=[],
        )

        failed_step = step.fail("Permission denied")

        assert failed_step.status == StepStatus.FAILED
        assert not failed_step.is_completed
        assert failed_step.is_failed
        assert failed_step.error_message == "Permission denied"
        assert failed_step.retry_count == step.retry_count + 1
        assert failed_step.completed_at is not None

    def test_step_dependencies(self) -> None:
        """Test step dependency checking."""
        step = PlanStepVO(
            id="step-002",
            action="process_file",
            description="Process created file",
            parameters={},
            order=2,
            dependencies=["step-001"],
        )

        # Should not execute without dependencies
        assert not step.can_execute(set())
        assert not step.can_execute({"other-step"})

        # Should execute with dependencies met
        assert step.can_execute({"step-001"})
        assert step.can_execute({"step-001", "step-003"})

    def test_step_serialization(self) -> None:
        """Test step to_dict/from_dict."""
        original_step = PlanStepVO(
            id="step-001",
            action="create_file",
            description="Create file",
            parameters={"filename": "test.py"},
            order=1,
            dependencies=["dep-001"],
        )

        # Convert to dict
        step_dict = original_step.to_dict()

        # Convert back to object
        restored_step = PlanStepVO.from_dict(step_dict)

        assert restored_step.id == original_step.id
        assert restored_step.action == original_step.action
        assert restored_step.description == original_step.description
        assert restored_step.parameters == original_step.parameters
        assert restored_step.order == original_step.order
        assert restored_step.dependencies == original_step.dependencies
        assert restored_step.status == original_step.status


class TestPlanEntity:
    """Test cases for Plan entity."""

    def test_plan_creation(self) -> None:
        """Test basic plan creation."""
        agent_id = str(uuid4())
        user_id = str(uuid4())
        session_id = str(uuid4())

        plan = Plan(
            agent_id=agent_id,
            user_id=user_id,
            session_id=session_id,
            title="Test Automation Plan",
            description="Automate testing workflow",
        )

        assert plan.agent_id == agent_id
        assert plan.user_id == user_id
        assert plan.session_id == session_id
        assert plan.title == "Test Automation Plan"
        assert plan.description == "Automate testing workflow"
        assert plan.status == PlanStatus.DRAFT
        assert plan.priority == PlanPriority.MEDIUM
        assert not plan.approved_by_user
        assert plan.steps == []
        assert plan.current_step_index == 0
        assert isinstance(plan.id, str)
        assert len(plan.id) > 0

    def test_plan_validation(self) -> None:
        """Test plan validation invariants."""
        # Missing agent_id
        with pytest.raises(ValueError, match="Plan phải có agent_id"):
            Plan(agent_id="", user_id=str(uuid4()), title="Test Plan")

        # Missing user_id
        with pytest.raises(ValueError, match="Plan phải có user_id"):
            Plan(agent_id=str(uuid4()), user_id="", title="Test Plan")

        # Empty title
        with pytest.raises(ValueError, match="Plan phải có title"):
            Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="")

    def test_add_step(self) -> None:
        """Test adding steps to plan."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        # Add first step
        step1 = plan.add_step(
            action="create_file",
            description="Create initial file",
            parameters={"filename": "main.py"},
        )

        assert len(plan.steps) == 1
        assert step1.order == 0
        assert step1.action == "create_file"
        assert step1.description == "Create initial file"
        assert step1.parameters == {"filename": "main.py"}

        # Add second step with dependencies
        step2 = plan.add_step(
            action="run_tests", description="Run unit tests", dependencies=[step1.id]
        )

        assert len(plan.steps) == 2
        assert step2.order == 1
        assert step2.dependencies == [step1.id]

    def test_plan_approval_workflow(self) -> None:
        """Test plan approval workflow."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        # Add a step first
        plan.add_step("create_file", "Create file")

        # Approve plan
        approver_id = str(uuid4())
        plan.approve(approver_id)

        assert plan.approved_by_user
        assert plan.approved_by == approver_id
        assert plan.approved_at is not None
        assert plan.status == PlanStatus.APPROVED

        # Should not approve twice
        with pytest.raises(ValueError, match="Plan đã được approved"):
            plan.approve("someone-else")

    def test_plan_execution_lifecycle(self) -> None:
        """Test complete plan execution lifecycle."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        # Add steps
        step1 = plan.add_step("action1", "First action")
        step2 = plan.add_step("action2", "Second action", dependencies=[step1.id])

        # Approve and start execution
        plan.approve("user-123")
        plan.start_execution()

        assert plan.status == PlanStatus.EXECUTING
        assert plan.started_at is not None
        assert plan.current_step_index == 0

        # Complete first step
        plan.complete_step(step1.id, "Step 1 completed")

        # Check step completion
        completed_step = plan._find_step(step1.id)
        assert completed_step.is_completed
        assert completed_step.result == "Step 1 completed"

        # Complete second step (should complete plan)
        plan.complete_step(step2.id, "Step 2 completed")

        assert plan.status == PlanStatus.COMPLETED
        assert plan.completed_at is not None
        assert plan.is_completed()

    def test_step_failure_handling(self) -> None:
        """Test step failure and retry logic."""
        plan = Plan(
            agent_id=str(uuid4()),
            user_id=str(uuid4()),
            title="Test Plan",
            max_retries=2,
        )

        # Add step and start execution
        step = plan.add_step("failing_action", "Action that fails")
        plan.approve("user-123")
        plan.start_execution()

        # Fail step multiple times
        plan.fail_step(step.id, "First failure")
        assert plan.status == PlanStatus.EXECUTING  # Still executing (retry available)
        assert plan.retry_count == 1

        plan.fail_step(step.id, "Second failure")
        assert plan.status == PlanStatus.FAILED  # Failed after max retries
        assert plan.retry_count == 2
        assert "Second failure" in plan.failure_reason

    def test_plan_reordering(self) -> None:
        """Test step reordering."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        # Add multiple steps
        step1 = plan.add_step("action1", "First action")
        step2 = plan.add_step("action2", "Second action")
        step3 = plan.add_step("action3", "Third action")

        assert [s.order for s in plan.steps] == [0, 1, 2]

        # Reorder steps
        plan.reorder_steps({step1.id: 2, step2.id: 0, step3.id: 1})

        # Check new order
        sorted_steps = sorted(plan.steps, key=lambda s: s.order)
        assert sorted_steps[0].id == step2.id  # order 0
        assert sorted_steps[1].id == step3.id  # order 1
        assert sorted_steps[2].id == step1.id  # order 2

    def test_plan_cancellation(self) -> None:
        """Test plan cancellation."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        plan.add_step("action1", "First action")
        plan.approve("user-123")
        plan.start_execution()

        # Cancel plan
        plan.cancel("User requested cancellation")

        assert plan.status == PlanStatus.CANCELLED
        assert plan.failure_reason == "User requested cancellation"

    def test_plan_progress_tracking(self) -> None:
        """Test plan progress calculation."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        # Add 4 steps
        step1 = plan.add_step("action1", "Action 1")
        step2 = plan.add_step("action2", "Action 2")
        step3 = plan.add_step("action3", "Action 3")
        step4 = plan.add_step("action4", "Action 4")

        plan.approve("user-123")
        plan.start_execution()

        # Initial progress
        assert plan.get_progress_percentage() == 0.0

        # Complete 2 out of 4 steps
        plan.complete_step(step1.id, "Done")
        plan.complete_step(step2.id, "Done")

        assert plan.get_progress_percentage() == 50.0

        # Complete all steps
        plan.complete_step(step3.id, "Done")
        plan.complete_step(step4.id, "Done")

        assert plan.get_progress_percentage() == 100.0

    def test_domain_events(self) -> None:
        """Test domain event generation."""
        plan = Plan(agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan")

        step = plan.add_step("action1", "Test action")
        plan.approve("user-123")

        # Should have approval event
        events = plan.clear_events()
        assert len(events) == 1
        assert events[0].__class__.__name__ == "PlanApprovedEvent"

        # Start execution
        plan.start_execution()
        events = plan.clear_events()
        assert len(events) == 1
        assert events[0].__class__.__name__ == "PlanStatusChangedEvent"

        # Complete step
        plan.complete_step(step.id, "Done")
        events = plan.clear_events()
        assert len(events) >= 1
        step_events = [
            e for e in events if e.__class__.__name__ == "PlanStepCompletedEvent"
        ]
        assert len(step_events) == 1

    def test_execution_summary(self) -> None:
        """Test execution summary generation."""
        plan = Plan(
            agent_id=str(uuid4()), user_id=str(uuid4()), title="Test Plan Summary"
        )

        plan.add_step("action1", "Action 1")
        plan.add_step("action2", "Action 2")

        summary = plan.get_execution_summary()

        assert summary["id"] == plan.id
        assert summary["title"] == "Test Plan Summary"
        assert summary["status"] == "draft"
        assert summary["total_steps"] == 2
        assert summary["completed_steps"] == 0
        assert summary["failed_steps"] == 0
        assert summary["progress"] == 0.0
        assert not summary["approved_by_user"]
