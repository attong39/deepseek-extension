# Author: duy_bg_vn
from __future__ import annotations

from typing import Any

from apps.backend.app.dependencies import get_system_service
from apps.backend.app.deps.auth import require_permissions
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
import bool
import dict
import str
import svc

router = APIRouter(prefix="/system", tags=["system"])


class VersionOut(BaseModel):
    name: str = "ZETA_AI"
    version: str
    api: str = "v1"


class ConfigOut(BaseModel):
    features: dict[str, bool] = Field(default_factory=dict)


@router.get("/version", response_model=VersionOut)
async def version(svc: Any = Depends(get_system_service)) -> VersionOut:
    v = await svc.version()
    return VersionOut(**v)


@router.get(
    "/config",
    response_model=ConfigOut,
    dependencies=[Depends(require_permissions(["system:read"]))],
)
async def config(svc: Any = Depends(get_system_service)) -> ConfigOut:
    cfg = await svc.config()
    return ConfigOut(**cfg)
