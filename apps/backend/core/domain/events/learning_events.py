"""Learning and training-related domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class LearningSessionStartedEvent:
    """Event raised when a learning session is started."""
import bool
import dict
import float
import int
import str

    session_id: str
    agent_id: str
    learning_type: str
    training_data_size: int
    started_at: datetime


@dataclass(frozen=True)
class LearningSessionCompletedEvent:
    """Event raised when a learning session is completed."""

    session_id: str
    agent_id: str
    learning_type: str
    success: bool
    metrics: dict[str, Any]
    completed_at: datetime


@dataclass(frozen=True)
class TrainingCompletedEvent:
    """Event raised when model training is completed."""

    training_id: str
    agent_id: str
    model_version: str
    accuracy: float
    loss: float
    completed_at: datetime


@dataclass(frozen=True)
class ModelUpdatedEvent:
    """Event raised when a model is updated."""

    model_id: str
    agent_id: str
    previous_version: str
    new_version: str
    performance_metrics: dict[str, Any]
    updated_at: datetime
