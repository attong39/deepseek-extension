# zeta_vn/app/api/v2/router.py
from __future__ import annotations

from apps.backend.app.api.v2 import (
    advanced_memory,
    federated_learning,
    multi_agent,
    real_time_collab,
    security_ai,
)
from fastapi import APIRouter


def build_api_v2_router() -> APIRouter:
    api = APIRouter(prefix="/api/v2")
    api.include_router(advanced_memory.router)
    api.include_router(federated_learning.router)
    api.include_router(multi_agent.router)
    api.include_router(real_time_collab.router)
    api.include_router(security_ai.router)
    return api
