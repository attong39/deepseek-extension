import Exception
import bool
import client_data
import config
import deploy_data
import dict
import e
import float
import int
import list
import round_data
import round_id
import str
import svc
import update_data
# zeta_vn/app/api/v2/federated_learning.py
"""
Federated Learning API v2

Mục tiêu & phạm vi:
Điều phối Federated Learning nâng cao: lập kế hoạch round, phát plan, nhận cập nhật cục bộ,
tổng hợp (FedAvg/FedProx/Median), theo dõi tiến độ, audit & rollback, privacy-preserving,
differential privacy, secure aggregation.
Tích hợp với core/domain/aggregates/federated_round.py & model.py.

Năng lực chính:
- Client management: registration, capability assessment, selection
- Round orchestration: planning, execution, monitoring, completion
- Model aggregation: FedAvg, FedProx, weighted aggregation, robust methods
- Privacy protection: differential privacy, secure aggregation
- Quality assurance: validation, rollback, audit trails
"""

from __future__ import annotations

from typing import Annotated, Any

from apps.backend.app.dependencies import get_federated_service
from apps.backend.app.deps.auth import get_current_user, require_permissions
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field


# Schemas for Federated Learning
class ClientRegisterIn(BaseModel):
    """Schema cho đăng ký client FL."""

    client_id: str = Field(..., description="ID client duy nhất")
    client_name: str = Field(..., description="Tên client")
    capabilities: dict[str, Any] = Field(..., description="Khả năng của client")
    compute_resources: dict[str, Any] = Field(
        default_factory=dict, description="Tài nguyên compute"
    )
    data_stats: dict[str, Any] = Field(
        default_factory=dict, description="Thống kê data (không sensitive)"
    )
    model_version: str = Field(..., description="Phiên bản model hỗ trợ")
    privacy_level: str = Field(
        "standard", description="Mức privacy: basic/standard/high"
    )
    location: str | None = Field(None, description="Location/region")


class RoundCreateIn(BaseModel):
    """Schema cho tạo training round."""

    round_name: str = Field(..., description="Tên round")
    model_configuration: dict[str, Any] = Field(..., description="Cấu hình model")
    aggregation_method: str = Field(
        "fedavg", description="Method: fedavg/fedprox/median/secure"
    )
    target_clients: int = Field(10, description="Số client mục tiêu")
    min_clients: int = Field(5, description="Số client tối thiểu")
    max_rounds: int = Field(10, description="Số rounds tối đa")
    client_epochs: int = Field(5, description="Số epochs trên client")
    convergence_threshold: float = Field(0.01, description="Ngưỡng convergence")
    privacy_budget: float | None = Field(None, description="Privacy budget (DP)")
    timeout_minutes: int = Field(60, description="Timeout cho mỗi round")
    client_selection_strategy: str = Field(
        "random", description="Strategy: random/performance/balanced"
    )


class ClientUpdateIn(BaseModel):
    """Schema cho client gửi model update."""

    client_id: str = Field(..., description="ID client")
    round_id: str = Field(..., description="ID round")
    model_weights: dict[str, Any] = Field(..., description="Model weights (encrypted)")
    training_stats: dict[str, Any] = Field(..., description="Training statistics")
    data_size: int = Field(..., description="Số samples đã train")
    training_time: float = Field(..., description="Thời gian training (seconds)")
    validation_accuracy: float | None = Field(None, description="Validation accuracy")
    privacy_noise_level: float | None = Field(None, description="Noise level applied")


class ModelDeployIn(BaseModel):
    """Schema cho deploy global model."""

    round_id: str = Field(..., description="ID round completed")
    deployment_strategy: str = Field(
        "gradual", description="Strategy: immediate/gradual/canary"
    )
    target_environments: list[str] = Field(..., description="Target environments")
    validation_requirements: dict[str, Any] = Field(
        default_factory=dict, description="Validation requirements"
    )
    rollback_threshold: float = Field(
        0.8, description="Performance threshold cho rollback"
    )


class AggregationConfigIn(BaseModel):
    """Schema cho cấu hình aggregation."""

    round_id: str = Field(..., description="ID round")
    method: str = Field(..., description="Aggregation method")
    weighted_by: str = Field(
        "data_size", description="Weighting: data_size/performance/equal"
    )
    outlier_detection: bool = Field(True, description="Enable outlier detection")
    byzantine_tolerance: bool = Field(False, description="Enable Byzantine tolerance")
    differential_privacy: bool = Field(False, description="Enable DP")
    privacy_epsilon: float | None = Field(None, description="Privacy epsilon")
    secure_aggregation: bool = Field(False, description="Enable secure aggregation")


# Response Schemas
class ClientRegisterOut(BaseModel):
    """Schema cho response đăng ký client."""

    client_id: str = Field(..., description="ID client")
    registration_token: str = Field(..., description="Token xác thực")
    status: str = Field(..., description="Status: registered/pending/rejected")
    capabilities_score: float = Field(..., description="Điểm capabilities (0.0-1.0)")
    assigned_tier: str = Field(..., description="Tier: bronze/silver/gold/platinum")
    next_round_eligibility: bool = Field(
        ..., description="Eligible cho round tiếp theo"
    )
    privacy_compliance: bool = Field(
        ..., description="Compliant với privacy requirements"
    )


class RoundCreateOut(BaseModel):
    """Schema cho response tạo round."""

    round_id: str = Field(..., description="ID round")
    round_name: str = Field(..., description="Tên round")
    status: str = Field(
        ..., description="Status: created/recruiting/training/aggregating/completed"
    )
    global_model_version: str = Field(..., description="Phiên bản global model")
    target_clients: int = Field(..., description="Số client target")
    estimated_duration: int = Field(..., description="Thời gian ước tính (minutes)")
    created_at: str = Field(..., description="Thời gian tạo")
    recruitment_deadline: str = Field(..., description="Deadline tuyển client")


class ClientUpdateOut(BaseModel):
    """Schema cho response client update."""

    update_id: str = Field(..., description="ID update")
    client_id: str = Field(..., description="ID client")
    round_id: str = Field(..., description="ID round")
    status: str = Field(..., description="Status: received/validated/accepted/rejected")
    validation_score: float | None = Field(None, description="Điểm validation")
    contribution_weight: float | None = Field(None, description="Trọng số contribution")
    privacy_compliance: bool = Field(..., description="Tuân thủ privacy")
    received_at: str = Field(..., description="Thời gian nhận")


class AggregationResultOut(BaseModel):
    """Schema cho kết quả aggregation."""

    aggregation_id: str = Field(..., description="ID aggregation")
    round_id: str = Field(..., description="ID round")
    method_used: str = Field(..., description="Method đã sử dụng")
    participating_clients: int = Field(..., description="Số clients tham gia")
    global_model_accuracy: float | None = Field(
        None, description="Accuracy global model"
    )
    convergence_achieved: bool = Field(..., description="Đã convergence chưa")
    privacy_budget_consumed: float | None = Field(
        None, description="Privacy budget đã dùng"
    )
    byzantine_clients_detected: int = Field(
        0, description="Số Byzantine clients detected"
    )
    aggregation_time: float = Field(..., description="Thời gian aggregation (seconds)")
    quality_metrics: dict[str, Any] = Field(..., description="Metrics chất lượng")


class ModelDeployOut(BaseModel):
    """Schema cho response deployment."""

    deployment_id: str = Field(..., description="ID deployment")
    round_id: str = Field(..., description="ID round")
    global_model_version: str = Field(..., description="Phiên bản model deployed")
    deployment_status: str = Field(..., description="Status deployment")
    target_environments: list[str] = Field(..., description="Environments deployed")
    rollback_plan: dict[str, Any] = Field(..., description="Kế hoạch rollback")
    deployed_at: str = Field(..., description="Thời gian deploy")


class RoundStatusOut(BaseModel):
    """Schema cho status round."""

    round_id: str = Field(..., description="ID round")
    round_name: str = Field(..., description="Tên round")
    status: str = Field(..., description="Status hiện tại")
    progress: float = Field(..., description="Progress % (0.0-1.0)")
    participating_clients: int = Field(..., description="Số clients tham gia")
    completed_updates: int = Field(..., description="Số updates đã hoàn thành")
    current_round_number: int = Field(..., description="Round number hiện tại")
    convergence_progress: float = Field(..., description="Progress convergence")
    estimated_completion: str | None = Field(None, description="Ước tính hoàn thành")
    performance_metrics: dict[str, Any] = Field(..., description="Performance metrics")


class FederatedOpOut(BaseModel):
    """Schema cho các operations."""

    success: bool = Field(..., description="Thành công hay không")
    message: str = Field(..., description="Thông báo")
    affected_count: int | None = Field(None, description="Số entities bị ảnh hưởng")


# Router
router = APIRouter()


@router.post(
    "/clients/register",
    response_model=ClientRegisterOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register FL client",
    description="Đăng ký client cho federated learning với capability assessment",
    dependencies=[Depends(require_permissions(["learning:participate"]))],
)
async def register_client(
    client_data: ClientRegisterIn,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> ClientRegisterOut:
    """
    Register client cho federated learning.

    Luồng:
    1. Validate client capabilities
    2. Assess compute resources
    3. Check privacy compliance
    4. Assign tier và eligibility
    5. Generate registration token
    """
    try:
        result_data = await svc.register_client(client_data)
        return ClientRegisterOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register client: {e!s}",
        ) from e


@router.post(
    "/rounds",
    response_model=RoundCreateOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create training round",
    description="Tạo round federated learning với configuration và strategy",
    dependencies=[Depends(require_permissions(["learning:orchestrate"]))],
)
async def create_round(
    round_data: RoundCreateIn,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> RoundCreateOut:
    """
    Tạo federated learning round.

    Luồng:
    1. Validate model configuration
    2. Setup aggregation method
    3. Initialize privacy parameters
    4. Create FederatedRoundAggregate
    5. Emit round.created event
    """
    try:
        result_data = await svc.create_round(round_data)
        return RoundCreateOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create round: {e!s}",
        ) from e


@router.post(
    "/rounds/{round_id}/updates",
    response_model=ClientUpdateOut,
    summary="Submit client update",
    description="Client gửi model update với privacy protection",
    dependencies=[Depends(require_permissions(["learning:participate"]))],
)
async def submit_client_update(
    round_id: str,
    update_data: ClientUpdateIn,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> ClientUpdateOut:
    """
    Submit encrypted model update từ client.

    Security:
    - Model weights encryption
    - Differential privacy noise
    - Byzantine detection
    - Update validation
    """
    update_data.round_id = round_id
    try:
        result_data = await svc.submit_update(update_data)
        return ClientUpdateOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit update: {e!s}",
        ) from e


@router.post(
    "/rounds/{round_id}/aggregate",
    response_model=AggregationResultOut,
    summary="Aggregate round",
    description="Aggregate client updates với privacy-preserving methods",
    dependencies=[Depends(require_permissions(["learning:orchestrate"]))],
)
async def aggregate_round(
    round_id: str,
    config: AggregationConfigIn,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> AggregationResultOut:
    """
    Aggregate model updates từ clients.

    Methods:
    - FedAvg: weighted averaging
    - FedProx: proximal term for heterogeneity
    - Median: robust to outliers
    - Secure: cryptographic aggregation
    """
    config.round_id = round_id
    try:
        result_data = await svc.aggregate_round(config)
        return AggregationResultOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to aggregate round: {e!s}",
        ) from e


@router.post(
    "/models/deploy",
    response_model=ModelDeployOut,
    summary="Deploy global model",
    description="Deploy aggregated global model với rollback strategy",
    dependencies=[Depends(require_permissions(["learning:orchestrate"]))],
)
async def deploy_global_model(
    deploy_data: ModelDeployIn,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> ModelDeployOut:
    """
    Deploy global model sau aggregation.

    Strategies:
    - Immediate: deploy ngay lập tức
    - Gradual: phased rollout
    - Canary: test với subset
    """
    try:
        result_data = await svc.deploy_model(deploy_data)
        return ModelDeployOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to deploy model: {e!s}",
        ) from e


@router.get(
    "/rounds/{round_id}/status",
    response_model=RoundStatusOut,
    summary="Get round status",
    description="Lấy real-time status của federated learning round",
    dependencies=[Depends(require_permissions(["learning:read"]))],
)
async def get_round_status(
    round_id: str,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> RoundStatusOut:
    """
    Lấy detailed status của FL round.

    Returns:
    - Participation metrics
    - Convergence progress
    - Performance indicators
    - Privacy budget usage
    """
    try:
        result_data = await svc.get_round_status(round_id)
        return RoundStatusOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get round status: {e!s}",
        ) from e


@router.post(
    "/rounds/{round_id}/pause",
    response_model=FederatedOpOut,
    summary="Pause round",
    description="Pause federated learning round",
    dependencies=[Depends(require_permissions(["learning:orchestrate"]))],
)
async def pause_round(
    round_id: str,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> FederatedOpOut:
    """Pause federated learning round."""
    try:
        result_data = await svc.pause_round(round_id)
        return FederatedOpOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause round: {e!s}",
        ) from e


@router.delete(
    "/rounds/{round_id}",
    response_model=FederatedOpOut,
    summary="Cancel round",
    description="Cancel federated learning round",
    dependencies=[Depends(require_permissions(["learning:orchestrate"]))],
)
async def cancel_round(
    round_id: str,
    svc: Annotated[Any, Depends(get_federated_service)],
    current_user: Annotated[Any, Depends(get_current_user)] = None,  # noqa: ARG001
) -> FederatedOpOut:
    """Cancel federated learning round."""
    try:
        result_data = await svc.cancel_round(round_id)
        return FederatedOpOut(**result_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel round: {e!s}",
        ) from e
