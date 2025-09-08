import pytest
from apps.backend.core.domain.aggregates.workflow_aggregate import (
import len
import str
import valid_status
    WorkflowAggregate,
    WorkflowStatus,
    WorkflowStep,
)
from pydantic import ValidationError


class TestWorkflowStep:
    """Test cases for WorkflowStep model."""

    def test_valid_step_creation(self):
        """Test creating a valid workflow step."""
        step = WorkflowStep(
            id="step-1", name="Test Step", status="pending", metadata={"key": "value"}
        )
        assert step.id == "step-1"
        assert step.name == "Test Step"
        assert step.status == "pending"
        assert step.metadata == {"key": "value"}
        assert step.started_at is None
        assert step.ended_at is None

    def test_invalid_status_validation(self):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Status must be one of"):
            WorkflowStep(id="step-1", name="Test", status="invalid")

    @pytest.mark.parametrize(
        "valid_status", ["pending", "running", "done", "failed", "skipped"]
    )
    def test_valid_statuses(self, valid_status: str):
        """Test all valid statuses."""
        step = WorkflowStep(id="step-1", name="Test", status=valid_status)
        assert step.status == valid_status


class TestWorkflowAggregate:
    """Test cases for WorkflowAggregate class."""

    def test_create_workflow(self):
        """Test creating a new workflow."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        assert workflow.id == "wf-123"
        assert workflow.name == "Test Workflow"
        assert workflow.status == WorkflowStatus.CREATED
        assert workflow.context == {}
        assert workflow.steps == []
        assert workflow.started_at is None
        assert workflow.ended_at is None

    def test_create_workflow_with_context(self):
        """Test creating workflow with initial context."""
        context = {"env": "test", "version": "1.0"}
        workflow = WorkflowAggregate.create(
            id="wf-123", name="Test Workflow", context=context
        )
        assert workflow.context == context

    def test_create_workflow_validation(self):
        """Test workflow creation validation."""
        with pytest.raises(ValidationError):
            WorkflowAggregate.create(id="wf-123", name="")
        with pytest.raises(ValueError, match="Workflow name cannot be empty"):
            WorkflowAggregate.create(id="wf-123", name="   ")

    def test_add_step(self):
        """Test adding steps to workflow."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        assert len(workflow.steps) == 1
        step = workflow.steps[0]
        assert step.id == "step-1"
        assert step.name == "First Step"
        assert step.status == "pending"
        assert step.metadata == {}

    def test_add_step_with_metadata(self):
        """Test adding step with metadata."""
        metadata = {"priority": "high", "timeout": 30}
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step", metadata)
        assert workflow.steps[0].metadata == metadata

    def test_add_step_validation(self):
        """Test step addition validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        with pytest.raises(ValueError, match="Step ID cannot be empty"):
            workflow.add_step("", "Test Step")
        with pytest.raises(ValueError, match="Step name cannot be empty"):
            workflow.add_step("step-1", "")
        workflow = workflow.add_step("step-1", "First Step")
        with pytest.raises(ValueError, match="Step with ID 'step-1' already exists"):
            workflow.add_step("step-1", "Another Step")

    def test_start_workflow(self):
        """Test starting workflow execution."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        assert workflow.status == WorkflowStatus.RUNNING
        assert workflow.started_at is not None
        assert workflow.ended_at is None

    def test_start_workflow_validation(self):
        """Test workflow start validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        with pytest.raises(ValueError, match="Workflow must have at least one step"):
            workflow.start()
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        with pytest.raises(ValueError, match="Workflow must be in created state"):
            workflow.start()

    def test_advance_step(self):
        """Test advancing a step to running status."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.add_step("step-2", "Second Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        assert workflow.steps[0].status == "running"
        assert workflow.steps[0].started_at is not None
        assert workflow.steps[1].status == "pending"

    def test_advance_step_validation(self):
        """Test step advancement validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        with pytest.raises(ValueError, match="Step 'non-existent' not found"):
            workflow.advance_step("non-existent")
        stopped_workflow = workflow.model_copy(
            update={"status": WorkflowStatus.COMPLETED}
        )
        with pytest.raises(
            ValueError, match="Workflow must be running to advance steps"
        ):
            stopped_workflow.advance_step("step-1")

    def test_complete_step(self):
        """Test completing a running step."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        outputs = {"result": "success", "data": [1, 2, 3]}
        workflow = workflow.complete_step("step-1", outputs)
        step = workflow.steps[0]
        assert step.status == "done"
        assert step.ended_at is not None
        assert step.metadata["outputs"] == outputs

    def test_complete_step_validation(self):
        """Test step completion validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        with pytest.raises(ValueError, match="Step step-1 must be running"):
            workflow.complete_step("step-1")
        with pytest.raises(ValueError, match="Step 'non-existent' not found"):
            workflow.complete_step("non-existent")

    def test_fail_step(self):
        """Test failing a step."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.fail_step("step-1", "Network timeout")
        step = workflow.steps[0]
        assert step.status == "failed"
        assert step.ended_at is not None
        assert step.metadata["error"] == "Network timeout"
        assert workflow.status == WorkflowStatus.FAILED
        assert workflow.ended_at is not None

    def test_fail_step_validation(self):
        """Test step failure validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        with pytest.raises(ValueError, match="Failure reason cannot be empty"):
            workflow.fail_step("step-1", "")
        with pytest.raises(ValueError, match="Step 'non-existent' not found"):
            workflow.fail_step("non-existent", "Error")

    def test_workflow_completion(self):
        """Test complete workflow execution."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.add_step("step-2", "Second Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.complete_step("step-1")
        workflow = workflow.advance_step("step-2")
        workflow = workflow.complete_step("step-2")
        assert workflow.status == WorkflowStatus.COMPLETED
        assert workflow.ended_at is not None
        assert all(step.status == "done" for step in workflow.steps)

    def test_cancel_workflow(self):
        """Test cancelling a running workflow."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.start()
        workflow = workflow.cancel("User requested cancellation")
        assert workflow.status == WorkflowStatus.CANCELLED
        assert workflow.ended_at is not None

    def test_cancel_workflow_validation(self):
        """Test workflow cancellation validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        with pytest.raises(ValueError, match="Workflow must be running"):
            workflow.cancel()

    def test_parallel_execution_limit(self):
        """Test maximum parallel steps limit."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.add_step("step-2", "Second Step")
        workflow = workflow.start()
        workflow = workflow.model_copy(update={"max_parallel_steps": 1})
        workflow = workflow.advance_step("step-1")
        with pytest.raises(ValueError, match="Maximum parallel steps limit reached"):
            workflow.advance_step("step-2")

    def test_get_step_methods(self):
        """Test step retrieval methods."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.add_step("step-2", "Second Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.complete_step("step-1")
        step = workflow.get_step("step-1")
        assert step is not None
        assert step.status == "done"
        assert workflow.get_step("non-existent") is None
        assert len(workflow.get_pending_steps()) == 1
        assert len(workflow.get_running_steps()) == 0
        assert len(workflow.get_completed_steps()) == 1
        assert len(workflow.get_failed_steps()) == 0

    def test_workflow_summary(self):
        """Test workflow summary generation."""
        workflow = WorkflowAggregate.create(
            id="wf-123", name="Test Workflow", context={"env": "prod"}
        )
        workflow = workflow.add_step("step-1", "First Step")
        workflow = workflow.add_step("step-2", "Second Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.complete_step("step-1")
        summary = workflow.get_workflow_summary()
        assert summary["workflow_id"] == "wf-123"
        assert summary["name"] == "Test Workflow"
        assert summary["status"] == WorkflowStatus.RUNNING
        assert summary["step_counts"]["total"] == 2
        assert summary["step_counts"]["completed"] == 1
        assert summary["step_counts"]["pending"] == 1
        assert summary["context_keys"] == ["env"]
        assert summary["max_parallel_steps"] == 1

    def test_invariant_validation(self):
        """Test aggregate invariant validation."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        workflow.validate_invariants()  # Should not raise
        invalid_workflow = workflow.model_copy(update={"name": ""})
        with pytest.raises(ValueError, match="Workflow name cannot be empty"):
            invalid_workflow.validate_invariants()
        workflow = workflow.add_step("step-1", "First")
        with pytest.raises(ValueError, match="Step with ID 'step-1' already exists"):
            workflow.add_step("step-1", "Duplicate")

    def test_domain_events(self):
        """Test that domain events are raised correctly."""
        workflow = WorkflowAggregate.create(id="wf-123", name="Test Workflow")
        events = workflow.pull_events()
        assert len(events) == 0  # No events should be raised
        workflow = workflow.add_step("step-1", "First Step")
        events = workflow.pull_events()
        assert len(events) >= 1
        assert any(e.event_type == "WorkflowStepAdded" for e in events)


class TestWorkflowAggregateIntegration:
    """Integration tests for complex workflow scenarios."""

    def test_complex_workflow_execution(self):
        """Test a complex workflow with multiple steps and failures."""
        workflow = WorkflowAggregate.create(
            id="wf-complex", name="Complex Processing Pipeline"
        )
        steps = [
            ("extract", "Data Extraction"),
            ("validate", "Data Validation"),
            ("transform", "Data Transformation"),
            ("load", "Data Loading"),
        ]
        for step_id, name in steps:
            workflow = workflow.add_step(step_id, name)
        workflow = workflow.start()
        workflow = workflow.advance_step("extract")
        workflow = workflow.complete_step("extract", {"records": 1000})
        workflow = workflow.advance_step("validate")
        workflow = workflow.fail_step(
            "validate", "Validation failed: missing required fields"
        )
        assert workflow.status == WorkflowStatus.FAILED
        assert workflow.get_failed_steps()[0].id == "validate"

    def test_workflow_with_parallel_steps(self):
        """Test workflow with parallel step execution."""
        workflow = WorkflowAggregate.create(
            id="wf-parallel", name="Parallel Processing"
        )
        workflow = workflow.model_copy(update={"max_parallel_steps": 2})
        workflow = workflow.add_step("step-1", "Parallel Step 1")
        workflow = workflow.add_step("step-2", "Parallel Step 2")
        workflow = workflow.add_step("step-3", "Sequential Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.advance_step("step-2")
        assert len(workflow.get_running_steps()) == 2
        workflow = workflow.complete_step("step-1")
        workflow = workflow.advance_step("step-3")
        assert len(workflow.get_running_steps()) == 2

    def test_workflow_cancellation_mid_execution(self):
        """Test cancelling workflow during execution."""
        workflow = WorkflowAggregate.create(id="wf-cancel", name="Cancellable Workflow")
        workflow = workflow.add_step("step-1", "Long Running Step")
        workflow = workflow.start()
        workflow = workflow.advance_step("step-1")
        workflow = workflow.cancel("Emergency stop required")
        assert workflow.status == WorkflowStatus.CANCELLED
        assert workflow.ended_at is not None


if __name__ == "__main__":
    pytest.main([__file__])


@pytest.fixture
def ValueError():
    """Fixture for ValueError"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def all():
    """Fixture for all"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def any():
    """Fixture for any"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def e():
    """Fixture for e"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def name():
    """Fixture for name"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def step():
    """Fixture for step"""
    return None  # TODO: Define appropriate fixture


@pytest.fixture
def step_id():
    """Fixture for step_id"""
    return None  # TODO: Define appropriate fixture
