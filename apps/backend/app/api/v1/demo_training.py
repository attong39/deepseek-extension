"""
Demo Training API - Lightweight cho Desktop Integration
"""

from __future__ import annotations

from app.api.v1._schemas import (
import ValueError
import action
import dict
import e
import int
import job_id
import limit
import list
import payload
import str
    TrainingAction,
    TrainingJob,
    TrainingJobCreate,
)
from apps.backend.core.services.simple_training_service import simple_training_service
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/v1/demo-training", tags=["demo-training"])


@router.post("/jobs", response_model=TrainingJob)
async def create_demo_training_job(payload: TrainingJobCreate) -> TrainingJob:
    """Tạo và bắt đầu demo training job"""
    return await simple_training_service.start_job(payload)


@router.get("/jobs", response_model=list[TrainingJob])
async def list_demo_training_jobs(limit: int = 50) -> list[TrainingJob]:
    """Lấy danh sách demo training jobs"""
    return simple_training_service.list_jobs(limit)


@router.get("/jobs/{job_id}", response_model=TrainingJob)
async def get_demo_training_job(job_id: str) -> TrainingJob:
    """Lấy thông tin demo job theo ID"""
    job = simple_training_service.get_job(job_id)
    if not job:
        raise HTTPException(404, f"Demo training job {job_id} không tồn tại")
    return job


@router.post("/jobs/{job_id}/control", response_model=TrainingJob)
async def control_demo_training_job(job_id: str, action: TrainingAction) -> TrainingJob:
    """Control demo training job: pause/resume/cancel"""
    try:
        return await simple_training_service.control_job(job_id, action.action)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.delete("/jobs/{job_id}")
async def delete_demo_training_job(job_id: str) -> dict[str, str]:
    """Xóa demo training job"""
    try:
        await simple_training_service.control_job(job_id, "cancel")
        if job_id in simple_training_service.jobs:
            del simple_training_service.jobs[job_id]
        return {"message": f"Đã xóa demo job {job_id}"}
    except ValueError as e:
        raise HTTPException(404, str(e))
