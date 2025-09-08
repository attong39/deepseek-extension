import Exception
import aggregation
import assignment
import bool
import capability
import dict
import e
import execution
import execution_id
import float
import int
import list
import payload
import str
import svc
import workflow_id
# zeta_vn/app/api/v2/multi_agent.py
"""
Multi-Agent Orchestration API v2

Mục tiêu & phạm vi:
Orchestrator đa agent nâng cao: lập kế hoạch, phân vai, hand-off theo rule-based/LLM-planner,
workflow automation, agent capability matching, result aggregation, conflict resolution.
Tích hợp với core/domain/aggregates/agent.py & workflow.py.

Năng lực chính:
- Workflow orchestration: định nghĩa flow, assign tasks, track progress
- Agent coordination: capability matching, load balancing, failover
- Result aggregation: combine outputs từ multiple agents
- Conflict resolution: khi agents có kết quả khác nhau
- Session management: multi-agent collaboration sessions
"""

from __future__ import annotations

from typing import Annotated, Any

from apps.backend.app.dependencies import get_orchestration_service
from apps.backend.app.deps.auth import get_current_user, require_permissions
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field


# Schemas for Multi-Agent Orchestration
class WorkflowCreateIn(BaseModel):
    """Schema cho tạo workflow orchestration."""

    name: str = Field(..., description="Tên workflow")
    description: str = Field(..., description="Mô tả mục tiêu workflow")
    tasks: list[dict[str, Any]] = Field(..., description="Danh sách tasks")
    agent_requirements: dict[str, Any] = Field(
        default_factory=dict, description="Yêu cầu capabilities của agents"
    )
    execution_mode: str = Field(
        "sequential", description="Mode: sequential/parallel/conditional"
    )
    timeout_seconds: int = Field(3600, description="Timeout workflow")
    priority: str = Field("normal", description="Priority: low/normal/high/urgent")


class TaskAssignmentIn(BaseModel):
    """Schema cho assign task cho agent."""

    workflow_id: str = Field(..., description="ID workflow")
    task_id: str = Field(..., description="ID task")
    agent_id: str = Field(..., description="ID agent được assign")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Parameters cho task"
    )
    deadline: str | None = Field(None, description="Deadline cho task")


class AgentCapabilityIn(BaseModel):
    """Schema cho register agent capabilities."""

    agent_id: str = Field(..., description="ID agent")
    capabilities: list[str] = Field(..., description="Danh sách capabilities")
    performance_metrics: dict[str, float] = Field(
        default_factory=dict, description="Metrics hiệu suất"
    )
    max_concurrent_tasks: int = Field(1, description="Số task tối đa đồng thời")
    availability_schedule: dict[str, Any] = Field(
        default_factory=dict, description="Lịch trình available"
    )


class WorkflowExecuteIn(BaseModel):
    """Schema cho execute workflow."""

    workflow_id: str = Field(..., description="ID workflow")
    input_data: dict[str, Any] = Field(..., description="Input data cho workflow")
    agent_preferences: dict[str, str] = Field(
        default_factory=dict, description="Preferred agents cho specific tasks"
    )
    override_timeouts: dict[str, int] = Field(
        default_factory=dict, description="Override timeouts cho specific tasks"
    )


class ResultAggregationIn(BaseModel):
    """Schema cho aggregate results từ multiple agents."""

    execution_id: str = Field(..., description="ID execution")
    aggregation_method: str = Field(
        "consensus", description="Method: consensus/voting/weighted/custom"
    )
    conflict_resolution: str = Field(
        "expert_review", description="Strategy khi có conflict"
    )
    quality_threshold: float = Field(0.8, description="Ngưỡng quality để accept result")


# Response Schemas
class WorkflowCreateOut(BaseModel):
    """Schema cho response tạo workflow."""

    workflow_id: str = Field(..., description="ID workflow")
    name: str = Field(..., description="Tên workflow")
    status: str = Field(..., description="Status: draft/active/paused/completed")
    tasks_count: int = Field(..., description="Số lượng tasks")
    created_at: str = Field(..., description="Thời gian tạo")
    estimated_duration: int = Field(..., description="Thời gian ước tính (seconds)")


class TaskAssignmentOut(BaseModel):
    """Schema cho response assignment."""

    assignment_id: str = Field(..., description="ID assignment")
    workflow_id: str = Field(..., description="ID workflow")
    task_id: str = Field(..., description="ID task")
    agent_id: str = Field(..., description="ID agent")
    status: str = Field(
        ..., description="Status: assigned/in_progress/completed/failed"
    )
    assigned_at: str = Field(..., description="Thời gian assign")
    estimated_completion: str | None = Field(None, description="Ước tính hoàn thành")


class WorkflowExecuteOut(BaseModel):
    """Schema cho response execute workflow."""

    execution_id: str = Field(..., description="ID execution")
    workflow_id: str = Field(..., description="ID workflow")
    status: str = Field(..., description="Status execution")
    progress: float = Field(..., description="Progress % (0.0-1.0)")
    started_at: str = Field(..., description="Thời gian bắt đầu")
    estimated_completion: str | None = Field(None, description="Ước tính hoàn thành")
    assigned_agents: list[str] = Field(..., description="Danh sách agents được assign")


class AgentCapabilityOut(BaseModel):
    """Schema cho response capability registration."""

    agent_id: str = Field(..., description="ID agent")
    status: str = Field(..., description="Status registration")
    capabilities_registered: list[str] = Field(
        ..., description="Capabilities đã register"
    )
    availability_score: float = Field(..., description="Điểm availability (0.0-1.0)")
    performance_rating: float = Field(..., description="Rating hiệu suất (0.0-5.0)")


class ResultAggregationOut(BaseModel):
    """Schema cho response aggregation."""

    aggregation_id: str = Field(..., description="ID aggregation")
    execution_id: str = Field(..., description="ID execution")
    final_result: dict[str, Any] = Field(..., description="Kết quả cuối cùng")
    confidence_score: float = Field(..., description="Confidence score (0.0-1.0)")
    method_used: str = Field(..., description="Method đã sử dụng")
    conflicts_detected: int = Field(..., description="Số conflicts detected")
    resolution_strategy: str = Field(..., description="Strategy đã dùng resolve")


class WorkflowStatusOut(BaseModel):
    """Schema cho workflow status."""

    workflow_id: str = Field(..., description="ID workflow")
    name: str = Field(..., description="Tên workflow")
    status: str = Field(..., description="Status hiện tại")
    progress: float = Field(..., description="Progress % (0.0-1.0)")
    total_tasks: int = Field(..., description="Tổng số tasks")
    completed_tasks: int = Field(..., description="Số tasks đã hoàn thành")
    failed_tasks: int = Field(..., description="Số tasks failed")
    active_agents: list[str] = Field(..., description="Agents đang active")
    estimated_remaining: int | None = Field(
        None, description="Thời gian còn lại (seconds)"
    )


class OrchestrationOpOut(BaseModel):
    """Schema cho các operations."""

    success: bool = Field(..., description="Thành công hay không")
    message: str = Field(..., description="Thông báo")
    affected_count: int | None = Field(None, description="Số entities bị ảnh hưởng")


# Router
router = APIRouter()


@router.post(
    "/workflows",
    response_model=WorkflowCreateOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create workflow",
    description="Tạo workflow multi-agent với task definitions và requirements",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def create_workflow(
    payload: WorkflowCreateIn,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> WorkflowCreateOut:
    """
    Tạo workflow multi-agent orchestration.

    Luồng:
    1. Validate workflow definition
    2. Analyze task dependencies
    3. Create workflow trong WorkflowAggregate
    4. Emit workflow.created event
    """
    try:
        result_data = await svc.create_workflow(payload)
        return WorkflowCreateOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workflow: {e!s}",
        ) from e


@router.post(
    "/workflows/{workflow_id}/execute",
    response_model=WorkflowExecuteOut,
    summary="Execute workflow",
    description="Execute workflow với agent assignment và task orchestration",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def execute_workflow(
    workflow_id: str,
    execution: WorkflowExecuteIn,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> WorkflowExecuteOut:
    """
    Execute workflow với automatic agent assignment.

    Luồng:
    1. Load workflow definition
    2. Match agents với task requirements
    3. Create execution plan
    4. Start task orchestration
    5. Emit workflow.started event
    """
    execution.workflow_id = workflow_id
    try:
        result_data = await svc.execute_workflow(execution)
        return WorkflowExecuteOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute workflow: {e!s}",
        ) from e


@router.post(
    "/tasks/assign",
    response_model=TaskAssignmentOut,
    summary="Assign task",
    description="Assign specific task cho agent với manual override",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def assign_task(
    assignment: TaskAssignmentIn,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> TaskAssignmentOut:
    """
    Manual task assignment với agent capability check.

    Supports:
    - Capability matching validation
    - Load balancing considerations
    - Deadline tracking
    """
    try:
        result_data = await svc.assign_task(assignment)
        return TaskAssignmentOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assign task: {e!s}",
        ) from e


@router.post(
    "/agents/capabilities",
    response_model=AgentCapabilityOut,
    summary="Register agent capabilities",
    description="Register agent capabilities và performance metrics",
    dependencies=[Depends(require_permissions(["agent:register"]))],
)
async def register_agent_capability(
    capability: AgentCapabilityIn,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> AgentCapabilityOut:
    """
    Register agent capabilities cho orchestration.

    Updates:
    - Agent capability registry
    - Performance metrics
    - Availability scheduling
    """
    try:
        result_data = await svc.register_capability(capability)
        return AgentCapabilityOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register capability: {e!s}",
        ) from e


@router.post(
    "/executions/{execution_id}/aggregate",
    response_model=ResultAggregationOut,
    summary="Aggregate results",
    description="Aggregate results từ multiple agents với conflict resolution",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def aggregate_execution_results(
    execution_id: str,
    aggregation: ResultAggregationIn,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> ResultAggregationOut:
    """
    Aggregate và resolve conflicts trong results.

    Methods:
    - Consensus: majority voting
    - Weighted: based on agent performance
    - Expert: human review for conflicts
    """
    aggregation.execution_id = execution_id
    try:
        result_data = await svc.aggregate_results(aggregation)
        return ResultAggregationOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to aggregate results: {e!s}",
        ) from e


@router.get(
    "/workflows/{workflow_id}/status",
    response_model=WorkflowStatusOut,
    summary="Get workflow status",
    description="Lấy trạng thái chi tiết của workflow execution",
    dependencies=[Depends(require_permissions(["agent:read"]))],
)
async def get_workflow_status(
    workflow_id: str,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> WorkflowStatusOut:
    """
    Lấy real-time status của workflow execution.

    Returns:
    - Progress tracking
    - Task completion status
    - Active agents
    - Performance metrics
    """
    try:
        result_data = await svc.get_workflow_status(workflow_id)
        return WorkflowStatusOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow status: {e!s}",
        ) from e


@router.post(
    "/workflows/{workflow_id}/pause",
    response_model=OrchestrationOpOut,
    summary="Pause workflow",
    description="Pause workflow execution",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def pause_workflow(
    workflow_id: str,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> OrchestrationOpOut:
    """Pause workflow execution."""
    try:
        result_data = await svc.pause_workflow(workflow_id)
        return OrchestrationOpOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause workflow: {e!s}",
        ) from e


@router.post(
    "/workflows/{workflow_id}/resume",
    response_model=OrchestrationOpOut,
    summary="Resume workflow",
    description="Resume paused workflow execution",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def resume_workflow(
    workflow_id: str,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> OrchestrationOpOut:
    """Resume paused workflow execution."""
    try:
        result_data = await svc.resume_workflow(workflow_id)
        return OrchestrationOpOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume workflow: {e!s}",
        ) from e


@router.delete(
    "/workflows/{workflow_id}",
    response_model=OrchestrationOpOut,
    summary="Cancel workflow",
    description="Cancel workflow execution",
    dependencies=[Depends(require_permissions(["agent:orchestrate"]))],
)
async def cancel_workflow(
    workflow_id: str,
    svc: Annotated[Any, Depends(get_orchestration_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> OrchestrationOpOut:
    """Cancel workflow execution."""
    try:
        result_data = await svc.cancel_workflow(workflow_id)
        return OrchestrationOpOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel workflow: {e!s}",
        ) from e
