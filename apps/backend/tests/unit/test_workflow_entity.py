"""
Test Workflow Entity - ZETA AI Server
====================================

Tests for Workflow domain entity.
Covers DDD compliance, business rules, DAG validation, and state management.
"""

from uuid import uuid4

import pytest

from core.domain.entities.workflow import (
import ValueError
import a_id
import b_id
import c_id
import d_id
import isinstance
import len
import name
import type
    Workflow,
    WorkflowStatus,
    WorkflowTrigger,
    WorkflowTriggerType,
)
from core.domain.value_objects.workflow_node import NodeType, WorkflowNodeVO


class TestWorkflowEntity:
    """Test cases for Workflow entity."""

    def test_workflow_creation(self) -> None:
        """Test basic workflow creation."""
        owner_id = uuid4()
        workflow = Workflow(
            name="Test Workflow",
            description="A workflow for testing",
            owner_id=owner_id,
        )

        assert workflow.name == "Test Workflow"
        assert workflow.description == "A workflow for testing"
        assert workflow.owner_id == owner_id
        assert workflow.status == WorkflowStatus.DRAFT
        assert workflow.version == "1.0.0"
        assert workflow.nodes == []
        assert workflow.edges == []
        assert workflow.triggers == []
        assert isinstance(workflow.id, type(uuid4()))

    def test_add_node_to_workflow(self) -> None:
        """Test adding nodes to workflow."""
        owner_id = uuid4()
        workflow = Workflow(name="Node Test", owner_id=owner_id)

        # Create node
        node = WorkflowNodeVO(
            id=uuid4(),
            name="Test Node",
            node_type=NodeType.TASK,
        )

        # Add node
        workflow.add_node(node)

        assert len(workflow.nodes) == 1
        assert workflow.nodes[0] == node

    def test_add_duplicate_node_fails(self) -> None:
        """Test adding duplicate node IDs fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Duplicate Test", owner_id=owner_id)

        node_id = uuid4()
        node1 = WorkflowNodeVO(id=node_id, name="Node 1")
        node2 = WorkflowNodeVO(id=node_id, name="Node 2")

        workflow.add_node(node1)

        with pytest.raises(
            ValueError, match="Node với ID .* đã tồn tại trong workflow"
        ):
            workflow.add_node(node2)

    def test_remove_node_from_workflow(self) -> None:
        """Test removing nodes from workflow."""
        owner_id = uuid4()
        workflow = Workflow(name="Remove Test", owner_id=owner_id)

        # Add nodes
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Node 1")
        node2 = WorkflowNodeVO(id=node2_id, name="Node 2")

        workflow.add_node(node1)
        workflow.add_node(node2)

        # Add edge between nodes
        workflow.connect(node1_id, node2_id)

        assert len(workflow.nodes) == 2
        assert len(workflow.edges) == 1

        # Remove node1
        result = workflow.remove_node(node1_id)
        assert result is True
        assert len(workflow.nodes) == 1
        assert workflow.nodes[0].id == node2_id
        assert len(workflow.edges) == 0  # Edge should be removed too

    def test_connect_nodes(self) -> None:
        """Test connecting nodes with edges."""
        owner_id = uuid4()
        workflow = Workflow(name="Connect Test", owner_id=owner_id)

        # Add nodes
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Node 1")
        node2 = WorkflowNodeVO(id=node2_id, name="Node 2")

        workflow.add_node(node1)
        workflow.add_node(node2)

        # Connect nodes
        workflow.connect(node1_id, node2_id, condition="status == 'completed'")

        assert len(workflow.edges) == 1
        edge = workflow.edges[0]
        assert edge["from"] == node1_id
        assert edge["to"] == node2_id
        assert edge["condition"] == "status == 'completed'"

    def test_connect_nonexistent_nodes_fails(self) -> None:
        """Test connecting non-existent nodes fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Connect Fail Test", owner_id=owner_id)

        node1_id = uuid4()
        node2_id = uuid4()
        node3_id = uuid4()

        # Add only one node
        node1 = WorkflowNodeVO(id=node1_id, name="Node 1")
        workflow.add_node(node1)

        # Try to connect to non-existent node
        with pytest.raises(ValueError, match="Node .* không tồn tại"):
            workflow.connect(node1_id, node2_id)

        # Try to connect from non-existent node
        with pytest.raises(ValueError, match="Node .* không tồn tại"):
            workflow.connect(node3_id, node1_id)

    def test_connect_duplicate_edge_fails(self) -> None:
        """Test connecting same nodes twice fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Duplicate Edge Test", owner_id=owner_id)

        # Add nodes
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Node 1")
        node2 = WorkflowNodeVO(id=node2_id, name="Node 2")

        workflow.add_node(node1)
        workflow.add_node(node2)

        # Connect nodes
        workflow.connect(node1_id, node2_id)

        # Try to connect again
        with pytest.raises(ValueError, match="Edge từ .* đến .* đã tồn tại"):
            workflow.connect(node1_id, node2_id)

    def test_disconnect_nodes(self) -> None:
        """Test disconnecting nodes."""
        owner_id = uuid4()
        workflow = Workflow(name="Disconnect Test", owner_id=owner_id)

        # Add nodes and connect
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Node 1")
        node2 = WorkflowNodeVO(id=node2_id, name="Node 2")

        workflow.add_node(node1)
        workflow.add_node(node2)
        workflow.connect(node1_id, node2_id)

        assert len(workflow.edges) == 1

        # Disconnect
        result = workflow.disconnect(node1_id, node2_id)
        assert result is True
        assert len(workflow.edges) == 0

        # Try to disconnect again
        result = workflow.disconnect(node1_id, node2_id)
        assert result is False

    def test_workflow_activation(self) -> None:
        """Test workflow activation."""
        owner_id = uuid4()
        workflow = Workflow(name="Activation Test", owner_id=owner_id)

        # Add valid DAG
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Start")
        node2 = WorkflowNodeVO(id=node2_id, name="End")

        workflow.add_node(node1)
        workflow.add_node(node2)
        workflow.connect(node1_id, node2_id)

        # Activate workflow
        workflow.activate("manual_trigger")

        assert workflow.status == WorkflowStatus.ACTIVE
        assert workflow.metadata["last_trigger"] == "manual_trigger"
        assert "activated_at" in workflow.metadata

    def test_workflow_activation_invalid_dag_fails(self) -> None:
        """Test workflow activation with invalid DAG fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Invalid DAG Test", owner_id=owner_id)

        # Create cycle: A -> B -> A
        node1_id = uuid4()
        node2_id = uuid4()
        node1 = WorkflowNodeVO(id=node1_id, name="Node A")
        node2 = WorkflowNodeVO(id=node2_id, name="Node B")

        workflow.add_node(node1)
        workflow.add_node(node2)
        workflow.connect(node1_id, node2_id)
        workflow.connect(node2_id, node1_id)  # Creates cycle

        # Try to activate
        with pytest.raises(ValueError, match="Workflow DAG không hợp lệ"):
            workflow.activate()

    def test_workflow_pause_resume(self) -> None:
        """Test workflow pause and resume."""
        owner_id = uuid4()
        workflow = Workflow(name="Pause Test", owner_id=owner_id)

        # Set status to active
        workflow.status = WorkflowStatus.ACTIVE

        # Pause workflow
        workflow.pause()
        assert workflow.status == WorkflowStatus.PAUSED

        # Resume workflow
        workflow.resume()
        assert workflow.status == WorkflowStatus.ACTIVE

    def test_workflow_pause_invalid_status_fails(self) -> None:
        """Test pausing workflow in invalid status fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Pause Fail Test", owner_id=owner_id)

        # Try to pause draft workflow
        with pytest.raises(ValueError, match="Không thể pause workflow ở trạng thái"):
            workflow.pause()

    def test_workflow_resume_invalid_status_fails(self) -> None:
        """Test resuming workflow in invalid status fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Resume Fail Test", owner_id=owner_id)

        # Try to resume non-paused workflow
        with pytest.raises(ValueError, match="Không thể resume workflow ở trạng thái"):
            workflow.resume()

    def test_workflow_cancel(self) -> None:
        """Test workflow cancellation."""
        owner_id = uuid4()
        workflow = Workflow(name="Cancel Test", owner_id=owner_id)

        # Set to running status
        workflow.status = WorkflowStatus.RUNNING

        # Cancel workflow
        workflow.cancel()
        assert workflow.status == WorkflowStatus.CANCELLED

    def test_workflow_cancel_invalid_status_fails(self) -> None:
        """Test cancelling workflow in invalid status fails."""
        owner_id = uuid4()
        workflow = Workflow(name="Cancel Fail Test", owner_id=owner_id)

        # Set to completed status
        workflow.status = WorkflowStatus.COMPLETED

        # Try to cancel
        with pytest.raises(ValueError, match="Không thể cancel workflow ở trạng thái"):
            workflow.cancel()

    def test_workflow_triggers(self) -> None:
        """Test adding and removing triggers."""
        owner_id = uuid4()
        workflow = Workflow(name="Trigger Test", owner_id=owner_id)

        # Add trigger
        trigger = WorkflowTrigger(
            type=WorkflowTriggerType.SCHEDULED,
            schedule="0 9 * * *",
            config={"timezone": "UTC"},
        )
        workflow.add_trigger(trigger)

        assert len(workflow.triggers) == 1
        assert workflow.triggers[0] == trigger

        # Remove trigger
        result = workflow.remove_trigger(WorkflowTriggerType.SCHEDULED)
        assert result is True
        assert len(workflow.triggers) == 0

        # Try to remove non-existent trigger
        result = workflow.remove_trigger(WorkflowTriggerType.MANUAL)
        assert result is False

    def test_workflow_execution_lifecycle(self) -> None:
        """Test workflow execution lifecycle."""
        owner_id = uuid4()
        workflow = Workflow(name="Execution Test", owner_id=owner_id)

        execution_id = uuid4()

        # Start execution
        workflow.start_execution(execution_id)

        assert workflow.status == WorkflowStatus.RUNNING
        assert workflow.last_execution_id == execution_id
        assert workflow.execution_count == 1
        assert workflow.last_executed_at is not None

        # Complete execution
        workflow.complete_execution("completed")

        assert workflow.status == WorkflowStatus.COMPLETED
        assert workflow.last_execution_status == "completed"

    def test_workflow_dag_helper_methods(self) -> None:
        """Test DAG helper methods."""
        owner_id = uuid4()
        workflow = Workflow(name="DAG Helper Test", owner_id=owner_id)

        # Create DAG: start -> middle -> end
        start_id = uuid4()
        middle_id = uuid4()
        end_id = uuid4()

        start_node = WorkflowNodeVO(id=start_id, name="Start")
        middle_node = WorkflowNodeVO(id=middle_id, name="Middle")
        end_node = WorkflowNodeVO(id=end_id, name="End")

        workflow.add_node(start_node)
        workflow.add_node(middle_node)
        workflow.add_node(end_node)

        workflow.connect(start_id, middle_id)
        workflow.connect(middle_id, end_id)

        # Test root nodes (no incoming edges)
        root_nodes = workflow.get_root_nodes()
        assert len(root_nodes) == 1
        assert root_nodes[0].id == start_id

        # Test leaf nodes (no outgoing edges)
        leaf_nodes = workflow.get_leaf_nodes()
        assert len(leaf_nodes) == 1
        assert leaf_nodes[0].id == end_id

        # Test dependencies
        middle_deps = workflow.get_dependencies(middle_id)
        assert middle_deps == [start_id]

        # Test dependents
        start_dependents = workflow.get_dependents(start_id)
        assert start_dependents == [middle_id]

    def test_workflow_permissions(self) -> None:
        """Test workflow permission system."""
        owner_id = uuid4()
        user1_id = uuid4()
        user2_id = uuid4()

        workflow = Workflow(name="Permission Test", owner_id=owner_id)

        # Owner should have access
        assert workflow.is_accessible_by(owner_id) is True

        # Other users should not have access initially
        assert workflow.is_accessible_by(user1_id) is False

        # Add allowed user
        workflow.add_allowed_user(user1_id)
        assert workflow.is_accessible_by(user1_id) is True

        # Remove allowed user
        workflow.remove_allowed_user(user1_id)
        assert workflow.is_accessible_by(user1_id) is False

        # Test public workflow
        workflow.is_public = True
        assert workflow.is_accessible_by(user1_id) is True
        assert workflow.is_accessible_by(user2_id) is True

    def test_workflow_validation_complex_dag(self) -> None:
        """Test DAG validation with complex workflow."""
        owner_id = uuid4()
        workflow = Workflow(name="Complex DAG Test", owner_id=owner_id)

        # Create diamond DAG: A -> B, A -> C, B -> D, C -> D
        a_id, b_id, c_id, d_id = uuid4(), uuid4(), uuid4(), uuid4()

        for node_id, name in [(a_id, "A"), (b_id, "B"), (c_id, "C"), (d_id, "D")]:
            workflow.add_node(WorkflowNodeVO(id=node_id, name=name))

        workflow.connect(a_id, b_id)
        workflow.connect(a_id, c_id)
        workflow.connect(b_id, d_id)
        workflow.connect(c_id, d_id)

        # Should be valid DAG
        assert workflow._validate_dag() is True

        # Should be able to activate
        workflow.activate()
        assert workflow.status == WorkflowStatus.ACTIVE

    def test_workflow_tags(self) -> None:
        """Test workflow tag management."""
        owner_id = uuid4()
        workflow = Workflow(name="Tag Test", owner_id=owner_id)

        # Add tags
        workflow.add_tag("production")
        workflow.add_tag("critical")

        assert "production" in workflow.tags
        assert "critical" in workflow.tags

        # Add duplicate tag (should not duplicate)
        workflow.add_tag("production")
        assert workflow.tags.count("production") == 1

        # Remove tag
        workflow.remove_tag("production")
        assert "production" not in workflow.tags
        assert "critical" in workflow.tags
