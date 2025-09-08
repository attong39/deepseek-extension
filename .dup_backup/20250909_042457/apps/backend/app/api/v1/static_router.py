# zeta_vn/app/api/v1/static_router.py
"""Static router builder theo blueprint - tránh dynamic import."""

from __future__ import annotations

# Import tất cả endpoint routers một cách explicit
from apps.backend.app.api.v1 import (
    admin,
    admin_emergency,
    admin_outbox,
    agents,
    agents_demo,
    agents_simple,
    agents_v2,
    ai,
    ai_trainer,
    asr,
    assistants,
    auth,
    automation,
    dashboard,
    demo_di,
    federated,
    feedback,
    files,
    health,
    learning,
    llm,
    memory,
    memory_semantic,
    meta,
    metrics_summary,
    performance,
    planning,
    privacy,
    profiling,
    rag,
    reflexion,
    scaffold,
    scaffold_simple,
    settings,
    streaming,
    system,
    training,
    users_demo,
    voice,
)
from fastapi import APIRouter


def build_api_v1_router() -> APIRouter:
    """Build API v1 router với static imports."""
    api = APIRouter(prefix="/api/v1")

    # Register theo thứ tự logical: system → auth → business → admin
    api.include_router(health.router)
    api.include_router(meta.router)
    api.include_router(auth.router)

    # Core business features
    api.include_router(agents.router)
    api.include_router(agents_simple.router)
    api.include_router(agents_demo.router)
    api.include_router(agents_v2.router)

    api.include_router(ai.router)
    api.include_router(ai_trainer.router)
    api.include_router(asr.router)
    api.include_router(assistants.router)
    api.include_router(automation.router)
    api.include_router(dashboard.router)
    api.include_router(demo_di.router)
    api.include_router(federated.router)
    api.include_router(feedback.router)
    api.include_router(files.router)
    api.include_router(learning.router)
    api.include_router(llm.router)
    api.include_router(memory.router)
    api.include_router(memory_semantic.router)
    api.include_router(metrics_summary.router)
    api.include_router(performance.router)
    api.include_router(planning.router)
    api.include_router(privacy.router)
    api.include_router(profiling.router)
    api.include_router(rag.router)
    api.include_router(reflexion.router)
    api.include_router(settings.router)
    api.include_router(streaming.router)
    api.include_router(system.router)
    api.include_router(training.router)
    api.include_router(users_demo.router)
    api.include_router(voice.router)

    # Admin features
    api.include_router(admin.router)
    api.include_router(admin_outbox.router)
    api.include_router(admin_emergency.router)

    # Dev/Scaffold features
    api.include_router(scaffold.router)
    api.include_router(scaffold_simple.router)

    return api
