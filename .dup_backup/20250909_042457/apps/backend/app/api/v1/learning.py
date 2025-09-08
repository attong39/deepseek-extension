# Author: duy_bg_vn
from __future__ import annotations

from typing import Any, Literal

from apps.backend.app.dependencies import get_learning_service
from apps.backend.app.deps.auth import require_permissions
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
import bool
import dict
import e
import getattr
import int
import it
import job_id
import len
import list
import max
import ok
import page
import page_items
import page_size
import payload
import response
import status_filter
import str
import svc
import total
import u

# ---- Schemas ----

JobStatus = Literal["queued", "running", "completed", "failed", "canceled"]
DATASET_NAME_PATTERN = r"^[\w\-]{1,64}$"


class LearningJob(BaseModel):
    id: str
    status: JobStatus
    message: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    dataset: str | None = None


class DatasetInfo(BaseModel):
    id: str
    name: str
    description: str | None = None
    created_at: str | None = None
    size: int | None = None


class IngestUrlsIn(BaseModel):
    urls: list[str] = Field(min_length=1)
    dataset: str | None = Field(default=None, pattern=DATASET_NAME_PATTERN)


class IngestTextIn(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    dataset: str | None = Field(default=None, pattern=DATASET_NAME_PATTERN)


class JobOut(BaseModel):
    job: LearningJob


class StartJobIn(BaseModel):
    config: dict[str, Any] = Field(default_factory=dict)
    dataset: str | None = Field(default=None, pattern=DATASET_NAME_PATTERN)


class InteractionEvent(BaseModel):
    session_id: str
    agent_id: str | None = None
    user_text: str = ""
    ai_text: str = ""
    rating: int | None = None
    comment: str | None = None
    meta: dict[str, Any] | None = None
    ts: int


class InteractionBatchIn(BaseModel):
    events: list[InteractionEvent] = Field(min_length=1)


router = APIRouter(prefix="/learning", tags=["learning"])


class TrainIn(BaseModel):
    agent_id: str
    dataset_id: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)


class TrainOut(BaseModel):
    job_id: str
    status: str


@router.post(
    "/train",
    response_model=TrainOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["learning:train"]))],
)
async def train(payload: TrainIn, svc: Any = Depends(get_learning_service)) -> TrainOut:
    job: dict[str, Any] = await svc.train(**payload.model_dump())
    return TrainOut(**job)


# ---- Ingest endpoints ----


@router.post(
    "/ingest/urls",
    response_model=JobOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["learning:ingest"]))],
)
async def ingest_urls(
    payload: IngestUrlsIn, svc: Any = Depends(get_learning_service)
) -> JobOut:
    # Server-side URL validation (basic)
    valid = []
    for u in payload.urls:
        if u.startswith("http://") or u.startswith("https://"):
            valid.append(u)
    if not valid:
        return JobOut(job=LearningJob(id="", status="failed", message="no valid url"))
    job = await svc.ingest_urls(urls=valid, dataset=payload.dataset)
    return JobOut(job=LearningJob(**job))


@router.post(
    "/ingest/text",
    response_model=JobOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["learning:ingest"]))],
)
async def ingest_text(
    payload: IngestTextIn, svc: Any = Depends(get_learning_service)
) -> JobOut:
    job = await svc.ingest_text(text=payload.text, dataset=payload.dataset)
    return JobOut(job=LearningJob(**job))


# ---- Datasets ----


@router.get(
    "/datasets",
    response_model=list[DatasetInfo],
    dependencies=[Depends(require_permissions(["learning:read"]))],
)
async def list_datasets(svc: Any = Depends(get_learning_service)) -> list[DatasetInfo]:
    items = await svc.list_datasets()
    return [DatasetInfo(**it) for it in items]


# ---- Jobs ----


@router.post(
    "/jobs",
    response_model=LearningJob,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["learning:jobs"]))],
)
async def start_job(
    payload: StartJobIn, svc: Any = Depends(get_learning_service)
) -> LearningJob:
    job = await svc.start_job(config=payload.config, dataset=payload.dataset)
    return LearningJob(**job)


@router.get(
    "/jobs",
    response_model=list[LearningJob],
    dependencies=[Depends(require_permissions(["learning:read"]))],
)
async def list_jobs(
    response: Response,
    status_filter: JobStatus | None = None,
    page: int = 1,
    page_size: int = 50,
    svc: Any = Depends(get_learning_service),
) -> list[LearningJob]:
    """List jobs with optional server-side pagination.

    Backward-compatible: returns a plain list. Pagination metadata exposed via headers:
    - X-Total-Count
    - X-Page
    - X-Page-Size
    """
    page_items, total = await getattr(svc, "list_jobs_paged", svc.list_jobs)(
        status=status_filter, page=page, page_size=page_size
    )
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Page"] = str(page)
    response.headers["X-Page-Size"] = str(page_size)
    return [LearningJob(**it) for it in page_items]


@router.get(
    "/jobs/{job_id}",
    response_model=LearningJob,
    dependencies=[Depends(require_permissions(["learning:read"]))],
)
async def get_job(job_id: str, svc: Any = Depends(get_learning_service)) -> LearningJob:
    job = await svc.get_job(job_id)
    return LearningJob(**job)


@router.post(
    "/jobs/{job_id}/cancel",
    response_model=dict,
    dependencies=[Depends(require_permissions(["learning:jobs"]))],
)
async def cancel_job(
    job_id: str, svc: Any = Depends(get_learning_service)
) -> dict[str, bool]:
    ok: bool = await svc.cancel_job(job_id)
    return {"ok": ok}


# ---- Interactions ----


@router.post(
    "/interactions",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_permissions(["learning:interactions:write"]))],
)
async def record_interactions(
    payload: InteractionBatchIn,
    response: Response,
    svc: Any = Depends(get_learning_service),
) -> dict[str, Any]:
    requested = len(payload.events)
    accepted = await svc.record_interactions([e.model_dump() for e in payload.events])
    dropped = max(0, requested - accepted)
    if dropped > 0:
        response.headers["X-Interactions-Dropped"] = str(dropped)
    # Strict throttle mode: return 429 if nothing accepted
    import os  # noqa: PLC0415

    strict = (
        os.getenv("LEARNING_INTERACTIONS_STRICT_THROTTLE", "false").lower() == "true"
    )
    if strict and accepted == 0:
        # Cho client biết nên retry sau bao lâu (mặc định 1s; có thể override qua env)
        retry_after = os.getenv("LEARNING_INTERACTIONS_RETRY_AFTER", "1")
        response.headers["Retry-After"] = retry_after
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"accepted": 0, "dropped": requested},
        )
    return {"accepted": accepted}
