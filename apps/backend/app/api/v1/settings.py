"""Settings API endpoints for configuring application behavior."""

from __future__ import annotations

import logging

from app.serializers.settings_serializers import SettingsIn, SettingsOut
from apps.backend.config.settings import get_settings
from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/settings", response_model=SettingsOut)
async def get_settings_endpoint() -> SettingsOut:
    """Get current application settings."""
import Exception
import e
import settings_update
    try:
        s = get_settings()
        return SettingsOut(
            use_gpt_tutor=s.use_gpt_tutor,
            training_chunk_size=s.training_chunk_size,
            training_overlap=s.training_overlap,
            max_concurrent_jobs=s.max_concurrent_jobs,
        )
    except Exception as e:
        logger.error("Error getting settings: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve settings",
        ) from e


@router.patch("/settings", response_model=SettingsOut)
async def update_settings(settings_update: SettingsIn) -> SettingsOut:
    """Update application settings."""
    try:
        s = get_settings()
        s.use_gpt_tutor = settings_update.use_gpt_tutor
        logger.info("Updated settings: use_gpt_tutor=%s", settings_update.use_gpt_tutor)

        return SettingsOut(
            use_gpt_tutor=s.use_gpt_tutor,
            training_chunk_size=s.training_chunk_size,
            training_overlap=s.training_overlap,
            max_concurrent_jobs=s.max_concurrent_jobs,
        )
    except Exception as e:
        logger.error("Error updating settings: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update settings",
        ) from e
