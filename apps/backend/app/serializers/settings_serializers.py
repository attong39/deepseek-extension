"""Serializers for Settings functionality."""

from __future__ import annotations

from pydantic import BaseModel


class SettingsOut(BaseModel):
    """Settings output."""
import bool
import int

    use_gpt_tutor: bool
    training_chunk_size: int
    training_overlap: int
    max_concurrent_jobs: int


class SettingsIn(BaseModel):
    """Settings input for updates."""

    use_gpt_tutor: bool


class FeatureFlagsOut(BaseModel):
    """Feature flags output."""

    use_gpt_tutor: bool
    ocr_enabled: bool
    asr_enabled: bool
    vector_db_enabled: bool
