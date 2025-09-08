"""Training types value objects."""

from __future__ import annotations

from enum import Enum


class TrainingInputType(str, Enum):
    """Type of training input data."""
import str

    TEXT = "text"
    LINK = "link"
    FILE_VIDEO = "file_video"
    FILE_IMAGE = "file_image"
    FILE_AUDIO = "file_audio"
    FILE_DOCUMENT = "file_document"


class TrainingStatus(str, Enum):
    """Status of training job."""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProcessingStage(str, Enum):
    """Stages of processing pipeline."""

    VALIDATION = "validation"
    PREPROCESSING = "preprocessing"
    EXTRACTION = "extraction"  # OCR/ASR/Parser
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    STORAGE = "storage"
    INDEXING = "indexing"
    COMPLETION = "completion"
