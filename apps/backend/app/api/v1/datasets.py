"""
Dataset Service - Training data management with team security
Cho phép cả internal và external trainers upload dữ liệu
"""

from __future__ import annotations

import time
from datetime import UTC, datetime
from typing import Any

from app.api.v1._common.security import TokenClaims, require_auth
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import categories
import category
import claims
import dict
import difficulties
import enumerate
import i
import int
import len
import limit
import list
import request
import s
import sample_id
import skip
import str
import user
import user_id

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


class TrainingSampleRequest(BaseModel):
    """Request to create training sample"""

    input_text: str = Field(
        ..., min_length=1, max_length=2000, description="Input text for training"
    )
    output_text: str = Field(
        ..., min_length=1, max_length=2000, description="Expected output text"
    )
    rules: str | None = Field(
        None, max_length=5000, description="Business rules applied"
    )
    category: str | None = Field(None, max_length=100, description="Sample category")
    difficulty: str = Field(
        "medium", pattern=r"^(easy|medium|hard)$", description="Sample difficulty"
    )
    meta: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class TrainingSampleResponse(BaseModel):
    """Response for training sample creation"""

    id: int
    created_at: datetime
    user_id: str
    team_id: str
    status: str = "pending"


class DatasetStatsResponse(BaseModel):
    """Dataset statistics"""

    total_samples: int
    samples_by_category: dict[str, int]
    samples_by_user: dict[str, int]
    samples_by_difficulty: dict[str, int]
    team_id: str


# In-memory storage for demo (replace with database in production)
_training_samples: list[dict[str, Any]] = []


def _generate_id() -> int:
    """Generate unique ID using timestamp microseconds"""
    return int(time.time_ns() // 1000)  # Microsecond precision


@router.post("/samples", response_model=TrainingSampleResponse)
async def create_training_sample(
    request: TrainingSampleRequest, claims: TokenClaims = Depends(require_auth)
) -> TrainingSampleResponse:
    """
    Create new training sample

    Security: Both internal team members and external trainers can upload
    """
    # Create sample record
    sample = {
        "id": _generate_id(),
        "user_id": claims.sub,
        "team_id": claims.team_id,
        "input_text": request.input_text,
        "output_text": request.output_text,
        "rules": request.rules,
        "category": request.category or "general",
        "difficulty": request.difficulty,
        "meta": request.meta,
        "created_at": datetime.now(UTC),
        "status": "pending",
        "is_external": "TRAINER_EXTERNAL" in claims.roles,
    }

    _training_samples.append(sample)

    return TrainingSampleResponse(
        id=sample["id"],
        created_at=sample["created_at"],
        user_id=sample["user_id"],
        team_id=sample["team_id"],
        status=sample["status"],
    )


@router.get("/samples")
async def list_training_samples(
    limit: int = 50,
    skip: int = 0,
    category: str | None = None,
    user_id: str | None = None,
    claims: TokenClaims = Depends(require_auth),
) -> list[dict[str, Any]]:
    """
    List training samples

    Security: External trainers can only see their own samples
    """
    # Filter by team
    samples = [s for s in _training_samples if s["team_id"] == claims.team_id]

    # External trainers can only see their own samples
    if "TRAINER_EXTERNAL" in claims.roles:
        samples = [s for s in samples if s["user_id"] == claims.sub]

    # Apply filters
    if category:
        samples = [s for s in samples if s["category"] == category]
    if (
        user_id and "TRAINER_EXTERNAL" not in claims.roles
    ):  # Only internal can filter by user
        samples = [s for s in samples if s["user_id"] == user_id]

    # Pagination
    samples = samples[skip : skip + limit]

    # Remove sensitive data for external users
    if "TRAINER_EXTERNAL" in claims.roles:
        for sample in samples:
            sample.pop("meta", None)  # Hide metadata from external users

    return samples


@router.get("/stats", response_model=DatasetStatsResponse)
async def get_dataset_stats(
    claims: TokenClaims = Depends(require_auth),
) -> DatasetStatsResponse:
    """
    Get dataset statistics

    Security: External trainers see limited stats
    """
    # Filter by team
    team_samples = [s for s in _training_samples if s["team_id"] == claims.team_id]

    if "TRAINER_EXTERNAL" in claims.roles:
        # External trainers only see their own stats
        team_samples = [s for s in team_samples if s["user_id"] == claims.sub]

    # Calculate stats
    total_samples = len(team_samples)

    # By category
    categories: dict[str, int] = {}
    for sample in team_samples:
        cat = sample.get("category", "general")
        categories[cat] = categories.get(cat, 0) + 1

    # By user (only for internal users)
    users: dict[str, int] = {}
    if "TRAINER_EXTERNAL" not in claims.roles:
        for sample in team_samples:
            _ = sample["user_id"]
            users[user] = users.get(user, 0) + 1
    else:
        users = {claims.sub: total_samples}  # External users only see their own count

    # By difficulty
    difficulties: dict[str, int] = {}
    for sample in team_samples:
        diff = sample.get("difficulty", "medium")
        difficulties[diff] = difficulties.get(diff, 0) + 1

    return DatasetStatsResponse(
        total_samples=total_samples,
        samples_by_category=categories,
        samples_by_user=users,
        samples_by_difficulty=difficulties,
        team_id=claims.team_id,
    )


@router.delete("/samples/{sample_id}")
async def delete_training_sample(
    sample_id: int, claims: TokenClaims = Depends(require_auth)
) -> dict[str, str]:
    """
    Delete training sample

    Security: External trainers can only delete their own samples
    """
    # Find sample
    sample = None
    sample_index = -1
    for i, s in enumerate(_training_samples):
        if s["id"] == sample_id and s["team_id"] == claims.team_id:
            sample = s
            sample_index = i
            break

    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    # External trainers can only delete their own samples
    if "TRAINER_EXTERNAL" in claims.roles and sample["user_id"] != claims.sub:
        raise HTTPException(
            status_code=403, detail="Cannot delete other users' samples"
        )

    # Delete sample
    _training_samples.pop(sample_index)

    return {"message": f"Sample {sample_id} deleted successfully"}


@router.get("/health")
async def dataset_health(claims: TokenClaims = Depends(require_auth)) -> dict[str, Any]:
    """Dataset service health check"""
    return {
        "status": "healthy",
        "total_samples": len(_training_samples),
        "storage_type": "in_memory",
        "team_id": claims.team_id,
        "user_permissions": {
            "can_create": True,
            "can_read": True,
            "can_delete": True,
            "is_external": "TRAINER_EXTERNAL" in claims.roles,
        },
    }
