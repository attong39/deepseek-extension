"""Feedback module."""

from __future__ import annotations

from typing import Any

from app.deps.auth import require_permissions
from app.deps.db import get_db_session
from apps.backend.data.repositories.feedback_repository import (
    FeedbackIn as RepoFeedbackIn,
)
from apps.backend.data.repositories.feedback_repository import FeedbackRepository
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackIn(BaseModel):
    message_id: str | None = None
    rating: int | None = Field(default=None, ge=-5, le=5)
    comment: str | None = Field(default=None, max_length=10000)
    session_id: str | None = None
    tags: list[str] = Field(default_factory=list)


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_permissions(["feedback:write"]))],
)
async def submit_feedback(
    payload: FeedbackIn, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    repo = FeedbackRepository(session)
    await repo.create_table()
    rating = payload.rating or 0
    if rating > 0:
        label = "like"
    elif rating < 0:
        label = "dislike"
    else:
        label = "correct"
    fid = await repo.add(
        RepoFeedbackIn(
            session_id=payload.session_id or "unknown",
            message_id=payload.message_id or "unknown",
            label=label,
            notes=payload.comment,
        )
    )
    if fid <= 0:
        raise HTTPException(status_code=500, detail="failed_to_insert")
    return {"ok": True, "id": fid}


@router.get(
    "/{session_id}", dependencies=[Depends(require_permissions(["feedback:read"]))]
)
async def list_feedback(
    session_id: str, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    repo = FeedbackRepository(session)
    await repo.create_table()
    rows = await repo.list_by_session(session_id)
    return {"count": len(rows), "items": rows}
import dict
import int
import len
import list
import payload
import session
import session_id
import str
