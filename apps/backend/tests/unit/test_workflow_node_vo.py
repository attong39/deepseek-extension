"""
Test WorkflowNodeVO Value Object - ZETA AI Server
================================================

Tests for WorkflowNodeVO value object.
Covers immutability, validation, and helper methods.
"""

from uuid import uuid4

import pytest

from core.domain.value_objects.workflow_node import NodeStatus, NodeType, WorkflowNodeVO
import AttributeError
import ValueError
import node_type


class TestWorkflowNodeVO:
    """Test cases for WorkflowNodeVO value object."""

    def test_create_valid_workflow_node(self) -> None:
        """Test creating a valid workflow node."""
        node_id = uuid4()
        task_id = uuid4()

        node = WorkflowNodeVO(
            id=node_id,
            name="Process Data",
            description="Process the input data",
            node_type=NodeType.TASK,
            task_id=task_id,
            task_type="data_processing",
            timeout_seconds=600,
            max_retries=5,
        )

        assert node.id == node_id
        assert node.name == "Process Data"
        assert node.description == "Process the input data"
        assert node.node_type == NodeType.TASK
        assert node.status == NodeStatus.PENDING
        assert node.task_id == task_id
        assert node.task_type == "data_processing"
        assert node.timeout_seconds == 600
        assert node.max_retries == 5

    def test_workflow_node_validation(self) -> None:
        """Test workflow node validation."""
        node_id = uuid4()

        # Empty name should fail
        with pytest.raises(ValueError, match="WorkflowNode phải có name"):
            WorkflowNodeVO(id=node_id, name="")

        # Name too long should fail
        with pytest.raises(
            ValueError, match="WorkflowNode name không được vượt quá 100 ký tự"
        ):
            WorkflowNodeVO(id=node_id, name="x" * 101)

        # Invalid timeout should fail
        with pytest.raises(ValueError, match="timeout_seconds phải > 0"):
            WorkflowNodeVO(id=node_id, name="Valid Name", timeout_seconds=0)

        # Invalid max_retries should fail
        with pytest.raises(ValueError, match="max_retries phải >= 0"):
            WorkflowNodeVO(id=node_id, name="Valid Name", max_retries=-1)

        # Invalid retry_delay should fail
        with pytest.raises(ValueError, match="retry_delay_seconds phải >= 0"):
            WorkflowNodeVO(id=node_id, name="Valid Name", retry_delay_seconds=-1)

    def test_workflow_node_helper_methods(self) -> None:
        """Test workflow node helper methods."""
        node_id = uuid4()
        task_id = uuid4()

        # Create ready node
        node = WorkflowNodeVO(
            id=node_id,
            name="Test Node",
            status=NodeStatus.READY,
            node_type=NodeType.TASK,
            task_id=task_id,
            depends_on=[uuid4()],
            condition="status == 'completed'",
        )

        # Test helper methods
        assert node.is_ready() is True
        assert node.is_terminal() is False
        assert node.has_dependencies() is True
        assert node.has_condition() is True
        assert node.is_task_node() is True

        # Test terminal node
        completed_node = node.with_status(NodeStatus.COMPLETED)
        assert completed_node.is_terminal() is True

        # Test non-task node
        decision_node = WorkflowNodeVO(
            id=uuid4(),
            name="Decision Node",
            node_type=NodeType.DECISION,
        )
        assert decision_node.is_task_node() is False

    def test_workflow_node_with_status(self) -> None:
        """Test creating new instance with updated status."""
        node_id = uuid4()
        original_node = WorkflowNodeVO(
            id=node_id,
            name="Test Node",
            status=NodeStatus.PENDING,
            config={"key": "value"},
        )

        # Create new instance with different status
        running_node = original_node.with_status(NodeStatus.RUNNING)

        # Original should be unchanged
        assert original_node.status == NodeStatus.PENDING
        # New instance should have updated status
        assert running_node.status == NodeStatus.RUNNING
        # Other fields should be the same
        assert running_node.id == node_id
        assert running_node.name == "Test Node"
        assert running_node.config == {"key": "value"}

    def test_workflow_node_with_outputs(self) -> None:
        """Test creating new instance with updated outputs."""
        node_id = uuid4()
        original_node = WorkflowNodeVO(
            id=node_id,
            name="Test Node",
            outputs={"initial": "data"},
        )

        # Create new instance with additional outputs
        updated_node = original_node.with_outputs({"result": "success", "count": 42})

        # Original should be unchanged
        assert original_node.outputs == {"initial": "data"}
        # New instance should have merged outputs
        expected_outputs = {"initial": "data", "result": "success", "count": 42}
        assert updated_node.outputs == expected_outputs
        # Other fields should be the same
        assert updated_node.id == node_id
        assert updated_node.name == "Test Node"

    def test_workflow_node_types(self) -> None:
        """Test different workflow node types."""
        node_id = uuid4()

        # Test each node type
        for node_type in NodeType:
            node = WorkflowNodeVO(
                id=node_id,
                name=f"{node_type.value} Node",
                node_type=node_type,
            )
            assert node.node_type == node_type

    def test_workflow_node_immutability(self) -> None:
        """Test that WorkflowNodeVO is immutable."""
        node_id = uuid4()
        node = WorkflowNodeVO(
            id=node_id,
            name="Immutable Node",
            config={"initial": "value"},
        )

        # Should not be able to modify fields directly
        with pytest.raises(AttributeError):
            node.name = "Modified Name"  # type: ignore

        with pytest.raises(AttributeError):
            node.status = NodeStatus.RUNNING  # type: ignore

    def test_workflow_node_defaults(self) -> None:
        """Test workflow node default values."""
        node_id = uuid4()
        node = WorkflowNodeVO(
            id=node_id,
            name="Default Node",
        )

        # Check defaults
        assert node.node_type == NodeType.TASK
        assert node.status == NodeStatus.PENDING
        assert node.timeout_seconds == 300
        assert node.max_retries == 3
        assert node.retry_delay_seconds == 60
        assert node.config is None
        assert node.inputs is None
        assert node.outputs is None
        assert node.depends_on is None
        assert node.condition is None
        assert node.tags is None
        assert node.metadata is None

    def test_workflow_node_with_all_fields(self) -> None:
        """Test workflow node with all fields populated."""
        node_id = uuid4()
        task_id = uuid4()
        depends_on = [uuid4(), uuid4()]

        node = WorkflowNodeVO(
            id=node_id,
            name="Complete Node",
            description="A node with all fields",
            node_type=NodeType.PARALLEL,
            status=NodeStatus.RUNNING,
            task_id=task_id,
            task_type="complex_task",
            config={"setting1": "value1", "setting2": True},
            inputs={"input1": "data1", "input2": 42},
            outputs={"output1": "result1"},
            depends_on=depends_on,
            condition="input1 != null",
            timeout_seconds=1800,
            max_retries=2,
            retry_delay_seconds=120,
            tags=["important", "parallel"],
            metadata={"owner": "system", "priority": "high"},
        )

        # Verify all fields
        assert node.id == node_id
        assert node.name == "Complete Node"
        assert node.description == "A node with all fields"
        assert node.node_type == NodeType.PARALLEL
        assert node.status == NodeStatus.RUNNING
        assert node.task_id == task_id
        assert node.task_type == "complex_task"
        assert node.config == {"setting1": "value1", "setting2": True}
        assert node.inputs == {"input1": "data1", "input2": 42}
        assert node.outputs == {"output1": "result1"}
        assert node.depends_on == depends_on
        assert node.condition == "input1 != null"
        assert node.timeout_seconds == 1800
        assert node.max_retries == 2
        assert node.retry_delay_seconds == 120
        assert node.tags == ["important", "parallel"]
        assert node.metadata == {"owner": "system", "priority": "high"}
