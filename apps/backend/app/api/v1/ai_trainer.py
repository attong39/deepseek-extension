"""API endpoints cho hệ thống AI trainer 24/7.

Module này expose các endpoints để quản lý và monitor
hệ thống training tự động.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.trainer.datasets.registry import DatasetStage, registry
from apps.backend.trainer.distill_gpt5 import RawExample, distill_examples
from apps.backend.trainer.evaluators.gpt5_verifier import evaluate_model_quick
from apps.backend.trainer.model_matrix import model_matrix
from apps.backend.trainer.workflows.trainer_workflow import (
import Exception
import dict
import e
import ex_data
import float
import int
import len
import list
import m
import min_quality
import model
import passes_gate
import report
import request
import set
import source_type
import stage
import str
import task
    get_learning_status,
    orchestrator,
)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai-trainer", tags=["AI Trainer"])


# Request/Response models
class DatasetCreateRequest(BaseModel):
    """Request để tạo dataset mới."""

    name: str = Field(..., description="Tên dataset")
    description: str = Field(default="", description="Mô tả dataset")
    source_type: str = Field(default="manual", description="Loại nguồn dữ liệu")
    examples: list[dict[str, Any]] = Field(
        default_factory=list, description="Raw examples"
    )


class DatasetResponse(BaseModel):
    """Response thông tin dataset."""

    dataset_id: str
    name: str
    stage: str
    sample_count: int
    quality_score: float
    created_at: str


class TrainingRequest(BaseModel):
    """Request để start training."""

    dataset_id: str = Field(..., description="ID dataset để train")
    model_name: str = Field(default="llama4-custom", description="Tên model output")
    config: dict[str, Any] = Field(default_factory=dict, description="Training config")


class EvaluationRequest(BaseModel):
    """Request để evaluate model."""

    model_name: str = Field(..., description="Tên model")
    model_path: str = Field(default="", description="Đường dẫn model")
    threshold: float = Field(default=0.75, description="Quality threshold")


class WorkflowControlRequest(BaseModel):
    """Request để control workflow."""

    action: str = Field(..., description="start | stop | restart")
    config: dict[str, Any] = Field(default_factory=dict, description="Workflow config")


# Dataset management endpoints
@router.post("/datasets", response_model=DatasetResponse)
async def create_dataset(request: DatasetCreateRequest) -> DatasetResponse:
    """Tạo dataset mới và optionally distill examples."""
    try:
        # Register dataset
        dataset_id = registry.register_dataset(
            name=request.name,
            description=request.description,
            source_type=request.source_type,
        )

        # Convert examples và distill nếu có
        if request.examples:
            raw_examples = []
            for ex_data in request.examples:
                example = RawExample(
                    prompt=ex_data.get("prompt", ""),
                    context=ex_data.get("context", ""),
                    refs=ex_data.get("refs", []),
                    meta=ex_data.get("meta", {}),
                    source_url=ex_data.get("source_url"),
                )
                raw_examples.append(example)

            # Distill với teacher model
            await distill_examples(
                examples=raw_examples,
                dataset_name=request.name,
                description=request.description,
            )

        # Get dataset info
        dataset_lineage = registry.get_dataset(dataset_id)
        if not dataset_lineage:
            raise HTTPException(
                status_code=404, detail="Dataset not found after creation"
            )

        return DatasetResponse(
            dataset_id=dataset_id,
            name=dataset_lineage.name,
            stage=dataset_lineage.stage.value,
            sample_count=dataset_lineage.sample_count,
            quality_score=dataset_lineage.quality.overall_score
            if dataset_lineage.quality
            else 0.0,
            created_at=dataset_lineage.created_at.isoformat(),
        )

    except Exception as e:
        logger.error(f"Failed to create dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets", response_model=list[DatasetResponse])
async def list_datasets(
    stage: str | None = None,
    source_type: str | None = None,
    min_quality: float = 0.0,
) -> list[DatasetResponse]:
    """Liệt kê datasets với filters."""
    try:
        stage_enum = DatasetStage(stage) if stage else None
        datasets = registry.list_datasets(
            stage=stage_enum,
            source_type=source_type,
            min_quality=min_quality,
        )

        responses = []
        for dataset_lineage in datasets:
            response = DatasetResponse(
                dataset_id=dataset_lineage.dataset_id,
                name=dataset_lineage.name,
                stage=dataset_lineage.stage.value,
                sample_count=dataset_lineage.sample_count,
                quality_score=dataset_lineage.quality.overall_score
                if dataset_lineage.quality
                else 0.0,
                created_at=dataset_lineage.created_at.isoformat(),
            )
            responses.append(response)

        return responses

    except Exception as e:
        logger.error(f"Failed to list datasets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_id}", response_model=dict[str, Any])
async def get_dataset(dataset_id: str) -> dict[str, Any]:
    """Lấy thông tin chi tiết dataset."""
    dataset_lineage = registry.get_dataset(dataset_id)
    if not dataset_lineage:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Convert to dict
    return {
        "dataset_id": dataset_lineage.dataset_id,
        "name": dataset_lineage.name,
        "description": dataset_lineage.description,
        "stage": dataset_lineage.stage.value,
        "source_url": dataset_lineage.source_url,
        "source_type": dataset_lineage.source_type,
        "sample_count": dataset_lineage.sample_count,
        "token_count_estimate": dataset_lineage.token_count_estimate,
        "quality": dataset_lineage.quality.model_dump()
        if dataset_lineage.quality
        else None,
        "created_at": dataset_lineage.created_at.isoformat(),
        "processed_at": dataset_lineage.processed_at.isoformat()
        if dataset_lineage.processed_at
        else None,
        "used_in_jobs": dataset_lineage.used_in_jobs,
        "performance_impact": dataset_lineage.performance_impact,
    }


# Training endpoints
@router.post("/training/start")
async def start_training(request: TrainingRequest) -> dict[str, Any]:
    """Bắt đầu training job."""
    try:
        # Validate dataset exists và ready
        dataset_lineage = registry.get_dataset(request.dataset_id)
        if not dataset_lineage:
            raise HTTPException(status_code=404, detail="Dataset not found")

        if dataset_lineage.stage != DatasetStage.LABELED:
            raise HTTPException(
                status_code=400,
                detail=f"Dataset not ready for training (stage: {dataset_lineage.stage})",
            )

        # TODO: Submit actual training job to Celery
        # For now, return mock response
        job_id = f"train_{request.dataset_id[:8]}"

        return {
            "job_id": job_id,
            "status": "submitted",
            "dataset_id": request.dataset_id,
            "model_name": request.model_name,
            "message": "Training job submitted successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start training: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training/jobs")
async def list_training_jobs() -> dict[str, Any]:
    """Liệt kê training jobs hiện tại."""
    # TODO: Integrate với actual job tracking
    return {
        "active_jobs": [],
        "recent_jobs": [],
        "total_completed": 0,
    }


# Evaluation endpoints
@router.post("/evaluation/start")
async def start_evaluation(request: EvaluationRequest) -> dict[str, Any]:
    """Bắt đầu evaluation model."""
    try:
        passes_gate, report = await evaluate_model_quick(
            model_name=request.model_name,
            model_path=request.model_path,
            threshold=request.threshold,
        )

        return {
            "evaluation_id": report.evaluation_id,
            "model_name": request.model_name,
            "passes_quality_gate": passes_gate,
            "overall_score": report.avg_overall,
            "safety_score": report.avg_safety,
            "recommendation": report.recommendation,
            "detailed_report": report.model_dump(),
        }

    except Exception as e:
        logger.error(f"Failed to start evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Model Matrix endpoints
@router.get("/models/matrix")
async def get_model_matrix() -> dict[str, Any]:
    """Lấy thông tin model matrix."""
    try:
        models = model_matrix.list_models()

        matrix_data = {
            "total_models": len(models),
            "by_role": {},
            "by_provider": {},
            "models": [],
        }

        for model in models:
            # Group by role
            role_key = model.role.value
            if role_key not in matrix_data["by_role"]:
                matrix_data["by_role"][role_key] = []
            matrix_data["by_role"][role_key].append(model.name)

            # Group by provider
            provider_key = model.provider
            if provider_key not in matrix_data["by_provider"]:
                matrix_data["by_provider"][provider_key] = []
            matrix_data["by_provider"][provider_key].append(model.name)

            # Model details
            model_data = {
                "name": model.name,
                "provider": model.provider,
                "role": model.role.value,
                "supported_tasks": [task.value for task in model.supported_tasks],
                "cost_tier": model.cost_tier.value,
                "max_context_tokens": model.max_context_tokens,
                "benchmark_score": model.benchmark_score,
                "can_run_local": model.can_run_local,
            }
            matrix_data["models"].append(model_data)

        return matrix_data

    except Exception as e:
        logger.error(f"Failed to get model matrix: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Workflow control endpoints
@router.post("/workflow/control")
async def control_workflow(request: WorkflowControlRequest) -> dict[str, Any]:
    """Control workflow 24/7."""
    try:
        if request.action == "start":
            if orchestrator.status.is_running:
                return {"message": "Workflow already running", "status": "running"}

            # TODO: Start workflow in background
            # await orchestrator.start_workflow()
            return {"message": "Workflow start requested", "status": "starting"}

        elif request.action == "stop":
            if not orchestrator.status.is_running:
                return {"message": "Workflow not running", "status": "stopped"}

            await orchestrator.stop_workflow()
            return {"message": "Workflow stopped", "status": "stopped"}

        elif request.action == "restart":
            if orchestrator.status.is_running:
                await orchestrator.stop_workflow()
            # TODO: Start workflow
            return {"message": "Workflow restarted", "status": "restarting"}

        else:
            raise HTTPException(
                status_code=400, detail=f"Invalid action: {request.action}"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to control workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflow/status")
async def get_workflow_status() -> dict[str, Any]:
    """Lấy trạng thái workflow hiện tại."""
    try:
        return get_learning_status()
    except Exception as e:
        logger.error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Statistics endpoints
@router.get("/stats/overview")
async def get_stats_overview() -> dict[str, Any]:
    """Thống kê tổng quan hệ thống trainer."""
    try:
        # Registry stats
        registry_stats = registry.get_stats()

        # Workflow stats
        workflow_status = get_learning_status()

        # Model matrix stats
        models = model_matrix.list_models()

        return {
            "datasets": {
                "total": registry_stats["total_datasets"],
                "by_stage": registry_stats["by_stage"],
                "average_quality": registry_stats["average_quality"],
                "total_samples": registry_stats["total_samples"],
            },
            "models": {
                "total_available": len(models),
                "by_role": len(set(m.role for m in models)),
                "local_models": len([m for m in models if m.can_run_local]),
            },
            "workflow": {
                "is_running": workflow_status["workflow"]["is_running"],
                "total_ingested": workflow_status["workflow"]["total_ingested"],
                "total_labeled": workflow_status["workflow"]["total_labeled"],
                "total_trained": workflow_status["workflow"]["total_trained"],
                "active_tasks": len(workflow_status["workflow"]["active_tasks"]),
            },
            "system_health": {
                "status": "healthy"
                if workflow_status["workflow"]["error_count"] < 5
                else "degraded",
                "error_count": workflow_status["workflow"]["error_count"],
                "last_activity": workflow_status["workflow"]["last_ingest"]
                or workflow_status["workflow"]["started_at"],
            },
        }

    except Exception as e:
        logger.error(f"Failed to get stats overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))
