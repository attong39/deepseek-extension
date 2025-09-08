"""Service interfaces for business logic.

This module defines abstract interfaces for core business services that orchestrate
domain entities and use cases. Keep these interfaces simple and framework-agnostic
to comply with Clean Architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import dict
import float
import int
import list
import str

if TYPE_CHECKING:  # Imports only for type checking; avoids runtime import cycles
    from uuid import UUID

    from apps.backend.core.domain.entities.training_job import TrainingJob
    from apps.backend.core.domain.value_objects.training_types import TrainingInputType


class TrainingServiceInterface(ABC):
    """Abstract interface for training business logic."""

    @abstractmethod
    async def create_training_job(
        self,
        user_id: UUID,
        input_type: TrainingInputType,
        data_chunks: list[str],
        metadata: dict[str, str] | None = None,
    ) -> TrainingJob:
        """Create a new training job with dataset items.

        Args:
            user_id: ID of the user creating the job
            input_type: Type of training input (document, dataset, etc.)
            data_chunks: List of data chunks to process
            metadata: Optional metadata for the job

        Returns:
            Created training job
        """

    @abstractmethod
    async def start_training(self, job_id: UUID) -> TrainingJob:
        """Start training job execution.

        Args:
            job_id: ID of the training job

        Returns:
            Updated training job
        """

    @abstractmethod
    async def update_training_progress(
        self, job_id: UUID, progress: float
    ) -> TrainingJob:
        """Update training job progress.

        Args:
            job_id: ID of the training job
            progress: Progress percentage (0.0-1.0)

        Returns:
            Updated training job
        """

    @abstractmethod
    async def complete_training(self, job_id: UUID) -> TrainingJob:
        """Mark training job as completed.

        Args:
            job_id: ID of the training job

        Returns:
            Updated training job
        """

    @abstractmethod
    async def fail_training(self, job_id: UUID, error_message: str) -> TrainingJob:
        """Mark training job as failed.

        Args:
            job_id: ID of the training job
            error_message: Error message describing the failure

        Returns:
            Updated training job
        """

    @abstractmethod
    async def get_user_training_jobs(self, user_id: UUID) -> list[TrainingJob]:
        """Get all training jobs for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of user's training jobs
        """

    @abstractmethod
    async def get_training_job_stats(
        self, user_id: UUID | None = None
    ) -> dict[str, int]:
        """Get training job statistics.

        Args:
            user_id: Optional user ID to filter stats

        Returns:
            Dictionary with training job counts by status
        """


class DashboardServiceInterface(ABC):
    """Abstract interface for dashboard business logic."""

    @abstractmethod
    async def get_dashboard_stats(self, user_id: UUID) -> dict[str, int]:
        """Get dashboard statistics for a user.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with dashboard statistics
        """

    @abstractmethod
    async def get_recent_activities(
        self, user_id: UUID, limit: int = 10
    ) -> list[dict[str, str]]:
        """Get recent activities for a user.

        Args:
            user_id: ID of the user
            limit: Maximum number of activities to return

        Returns:
            List of recent activities
        """


# Alias for DI typing convenience (matches usage across codebase)
TrainingService = TrainingServiceInterface
DashboardService = DashboardServiceInterface
