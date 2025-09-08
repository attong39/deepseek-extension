"""
API v1 endpoints package.
"""

from apps.backend.app.api.v1.endpoints.agents_example import (
    router as agents_example_router,
)
from apps.backend.app.api.v1.endpoints.mentor import router as mentor_router
from apps.backend.app.api.v1.endpoints.plans_example import (
    router as plans_example_router,
)
from fastapi import APIRouter

# Compose a single package-level router to avoid name redefinition
router = APIRouter()
router.include_router(agents_example_router)
router.include_router(mentor_router)
router.include_router(plans_example_router)