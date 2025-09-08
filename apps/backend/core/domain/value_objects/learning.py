"""Learning-related value objects.

Defines enums and small immutable structures used by learning entities.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import bool
import float
import int
import max
import property
import self
import str
import threshold


class LearningStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LearningType(str, Enum):
    SELF_PACED = "self_paced"
    INSTRUCTOR_LED = "instructor_led"
    INTERACTIVE = "interactive"
    ASSESSMENT = "assessment"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass(slots=True)
class ProgressMetrics:
    """Learning progress metrics.

    Attributes:
        completion_percentage: Progress completion from 0.0 to 100.0.
        time_spent_minutes: Total minutes spent.
        exercises_completed: Number of completed exercises.
        exercises_total: Total number of exercises.
        accuracy_percentage: Accuracy from 0.0 to 100.0.
    """

    completion_percentage: float
    time_spent_minutes: int
    exercises_completed: int
    exercises_total: int
    accuracy_percentage: float

    @property
    def exercises_remaining(self) -> int:
        """Number of remaining exercises."""
        return max(0, self.exercises_total - self.exercises_completed)


@dataclass(slots=True)
class AssessmentScore:
    """Assessment score details."""

    points_earned: int
    points_total: int
    percentage: float
    grade: str

    def is_passing(self, threshold: float) -> bool:
        """Whether the score passes the given threshold percentage."""
        return self.percentage >= threshold
