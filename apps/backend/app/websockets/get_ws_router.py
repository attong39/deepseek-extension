from __future__ import annotations

from fastapi import APIRouter
import dict
import str

"""Auto-generated router skeleton."""

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
