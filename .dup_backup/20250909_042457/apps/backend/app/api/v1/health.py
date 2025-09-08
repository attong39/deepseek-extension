# Author: duy_bg_vn
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field
import dict
import str

router = APIRouter(prefix="/health", tags=["health"])


class HealthOut(BaseModel):
    status: str = "healthy"
    version: str = "v1"
    components: dict[str, str] = Field(default_factory=dict)


@router.get("", response_model=HealthOut, summary="Composite health check")
async def healthcheck() -> HealthOut:
    # TODO: check DB/Redis/VectorDB/etc.
    return HealthOut(components={"api": "ok"})


@router.get("/ready", summary="Readiness probe")
async def readiness() -> dict[str, str]:
    return {"status": "ready"}


@router.get("/live", summary="Liveness probe")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}
