"""Training API endpoints for training job management.

Contains both trainer-only endpoints (e.g. `/learn`) and job management
endpoints that enqueue processing pipelines. Trainer endpoints must not call
ChatService and should be wired to trainer/Kb DI bindings.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from app.dependencies import get_file_service, get_training_service
from app.deps.auth import get_current_user, require_permissions
from app.di_container import get_service
from app.serializers.training_serializers import (
import Exception
import actor_id
import allowed_exts
import allowed_mimes
import artifact_key
import bool
import current_user
import description
import dict
import e
import f
import feedback
import file
import file_svc
import files
import hasattr
import ids
import int
import isinstance
import kb
import len
import list
import rating
import request
import rlhf
import s
import set
import str
import svc
import topic
import trainer
import training_service
import tuple
    IngestIn,
    JobOut,
    StatusOut,
    TrainingJobList,
)
from apps.backend.core.domain.entities.user import User
from apps.backend.core.domain.value_objects.training_types import TrainingInputType
from apps.backend.data.external.worker.tasks.training_tasks import enqueue_training_job
from apps.backend.data.external.worker.tasks.training_tasks import (
    get_job_status as _get_job_status,
)
from apps.backend.training.gpt4o_trainer import GPT4oTrainerService
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

# FastAPI DI helpers for trainers/rlhf
GetTrainerService = get_service("trainer_service")
GetRLHFStore = get_service("rlhf_store")
GetTelemetry = get_service("telemetry_service")
GetKBStore = get_service("kb_store")

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/training", tags=["training"])


# Dependency placeholders: prefer DI container shortcuts
def get_trainer_service(
    trainer: GPT4oTrainerService = Depends(GetTrainerService),
) -> GPT4oTrainerService:
    return trainer


def get_kb_store(kb: Any = Depends(GetKBStore)) -> Any:
    return kb


def get_rlhf_store(rlhf: Any = Depends(GetRLHFStore)) -> Any:
    return rlhf


async def _save_files(files: list[UploadFile] | None, file_svc: Any) -> list[str]:
    ids: list[str] = []
    if not files or not hasattr(file_svc, "save"):
        return ids
    for f in files:
        try:
            meta = await file_svc.save(f)
            if isinstance(meta, dict):
                fid = meta.get("id")
                if isinstance(fid, str):
                    ids.append(fid)
        except Exception:
            continue
    return ids


@router.post("/learn")
async def learn_topic(
    topic: str,
    svc: GPT4oTrainerService = Depends(get_trainer_service),
    kb: Any = Depends(get_kb_store),
) -> Any:
    """Trainer-only endpoint that builds & persists a learning artifact.

    Important: this route must not call ChatService. Wire `get_trainer_service`
    and `get_kb_store` via DI in `app.di_container`.
    """
    res = await svc.learn_and_persist(
        topic,
        store=kb,
        limit=5,
        rules=[
            "Safety: red-team outputs. No user-facing answers.",
            "Keep artifacts concise and testable.",
        ],
    )
    return res


@router.post(
    "/feedback",
    dependencies=[
        Depends(require_permissions(["training:write", "admin:users:write"]))
    ],
)
async def ingest_feedback(
    artifact_key: str,
    rating: int | None = None,
    feedback: str | None = None,
    actor_id: str | None = None,
    rlhf: Any = Depends(get_rlhf_store),
) -> dict[str, Any]:
    """Ingest feedback from desktop/agents to update RLHF signals.

    This endpoint is intentionally small and returns success True/False.
    """
    ok = await rlhf.ingest_feedback(
        artifact_key=artifact_key, rating=rating, feedback=feedback, actor_id=actor_id
    )
    return {"ok": bool(ok)}


def _parse_env_limits() -> tuple[set[str], set[str], int | None]:
    mimes = {
        s.strip().lower()
        for s in os.getenv("TRAINING_ALLOWED_MIME", "").split(",")
        if s.strip()
    }
    exts = {
        s.strip().lower().lstrip(".")
        for s in os.getenv("TRAINING_ALLOWED_EXTS", "").split(",")
        if s.strip()
    }
    max_mb = os.getenv("TRAINING_MAX_FILE_SIZE_MB")
    try:
        max_bytes: int | None = int(max_mb) * 1024 * 1024 if max_mb else None
    except Exception:
        max_bytes = None
    return mimes, exts, max_bytes


def _validate_file_basic(
    file: UploadFile, allowed_mimes: set[str], allowed_exts: set[str]
) -> None:
    # MIME
    if allowed_mimes and (file.content_type or "").lower() not in allowed_mimes:
        raise HTTPException(
            status_code=400, detail=f"MIME type not allowed: {file.content_type}"
        )
    # Extension
    name = (file.filename or "").lower()
    ext = name.rsplit(".", 1)[-1] if "." in name else ""
    if allowed_exts and ext not in allowed_exts:
        raise HTTPException(
            status_code=400, detail=f"File extension not allowed: .{ext}"
        )


def _validate_file_size_header(file: UploadFile, max_bytes: int | None) -> None:
    if max_bytes is None:
        return
    try:
        # Per-part header if client sends it
        hdr = file.headers.get("content-length") if hasattr(file, "headers") else None
        if hdr is not None:
            size = int(hdr)
            if size > max_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"File exceeds max size: {size} > {max_bytes}",
                )
    except HTTPException:
        raise
    except Exception:
        # If header absent or invalid, skip; storage layer will enforce limits
        return


@router.post(
    "",
    response_model=JobOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["training:create"]))],
)
async def start_training_upload(
    description: str | None = Form(default=None),
    files: list[UploadFile] | None = File(default=None),
    file_svc: Any = Depends(get_file_service),
) -> JobOut:
    """Start a training job via multipart upload (description + files[]).

    Lưu ý: Hiện tại pipeline mô phỏng, file chưa được xử lý nội dung.
    Trả về job_id để client poll trạng thái.
    """
    try:
        # Đánh dấu có file để pipeline mô phỏng chạy các stage tương ứng
        has_file = bool(files and len(files) > 0)
        allowed_mimes, allowed_exts, max_bytes = _parse_env_limits()
        # Validate per-file theo env (nếu set)
        if has_file:
            for f in files or []:
                _validate_file_basic(f, allowed_mimes, allowed_exts)
                _validate_file_size_header(f, max_bytes)
        saved_ids = await _save_files(files if has_file else None, file_svc)
        job_id = enqueue_training_job(
            file=True if has_file else None,
            text=description or None,
            link=None,
            tags=[],
            file_ids=saved_ids,
        )
        return JobOut(job_id=job_id, status="queued")
    except Exception as e:
        logger.error(f"Failed to start training (multipart): {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start training job",
        ) from e


@router.get(
    "/jobs",
    response_model=TrainingJobList,
    dependencies=[Depends(require_permissions(["training:read"]))],
)
async def list_training_jobs(
    training_service: Any = Depends(get_training_service),
    current_user: User = Depends(get_current_user),
) -> TrainingJobList:
    """List all training jobs for the current user."""
    try:
        jobs = await training_service.get_user_training_jobs(current_user.id)
        status_jobs = [
            StatusOut(
                job_id=job.job_id,
                status=job.status.value,
                progress=int(job.progress),
                message=f"Training {job.status.value}",
                started_at=job.created_at.isoformat() if job.created_at else None,
                completed_at=(
                    job.updated_at.isoformat()
                    if job.status.value == "completed"
                    else None
                ),
            )
            for job in jobs
        ]
        return TrainingJobList(
            jobs=status_jobs, total=len(status_jobs), page=1, per_page=10
        )
    except Exception as e:
        logger.error(f"Failed to list training jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve training jobs",
        ) from e


@router.post(
    "/jobs",
    response_model=JobOut,
    dependencies=[Depends(require_permissions(["training:create"]))],
)
async def create_training_job(
    request: IngestIn,
    training_service: Any = Depends(get_training_service),
    current_user: User = Depends(get_current_user),
) -> JobOut:
    """Create a new training job."""
    try:
        input_type = TrainingInputType.TEXT if request.text else TrainingInputType.LINK
        job = await training_service.create_training_job(
            user_id=current_user.id,
            input_type=input_type,
            data_chunks=[request.text or str(request.link)],
            metadata={"tags": request.tags or []},
        )
        return JobOut(job_id=job.job_id, status=job.status.value)
    except Exception as e:
        logger.error(f"Failed to create training job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create training job",
        ) from e


@router.get("/{job_id}", response_model=StatusOut)
async def get_training_job(job_id: str) -> StatusOut:
    """Get a specific training job by ID (Celery-backed mock store)."""
    data = _get_job_status(job_id)
    return StatusOut(
        job_id=job_id,
        status=str(data.get("status", "unknown")),
        progress=int(data.get("progress", 0)),
        message=str(data.get("message", "")) or None,
        started_at=None,
        completed_at=None,
    )


@router.get("/{job_id}/status", response_model=StatusOut)
async def get_training_job_status(job_id: str) -> StatusOut:
    """Get status of a training job (Celery-backed mock store)."""
    data = _get_job_status(job_id)
    return StatusOut(
        job_id=job_id,
        status=str(data.get("status", "unknown")),
        progress=int(data.get("progress", 0)),
        message=str(data.get("message", "")) or None,
        started_at=None,
        completed_at=None,
    )
