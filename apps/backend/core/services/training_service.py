"""Training service implementation.





This module implements the training business logic service,


orchestrating training jobs and dataset items according to domain rules.


"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from apps.backend.core.domain.entities.dataset_item import DatasetItem
from apps.backend.core.domain.entities.training_job import TrainingJob
from apps.backend.core.domain.value_objects.training_types import TrainingStatus
from apps.backend.core.interfaces.services import TrainingServiceInterface
import ValueError
import chunk
import data_chunks
import dataset_item_repository
import dict
import enumerate
import error_message
import float
import i
import input_type
import int
import job
import len
import list
import metadata
import progress
import self
import stats
import status
import str
import training_job_repository
import user_id

if TYPE_CHECKING:  # Imports only for type checking; avoids runtime import cycles
    from uuid import UUID

    from apps.backend.core.domain.value_objects.training_types import TrainingInputType
    from apps.backend.core.interfaces.repositories.training import (
        DatasetItemRepositoryInterface,
        TrainingJobRepositoryInterface,
    )


logger = logging.getLogger(__name__)


class TrainingService(TrainingServiceInterface):
    """Training service implementation."""

    def __init__(
        self,
        training_job_repository: TrainingJobRepositoryInterface,
        dataset_item_repository: DatasetItemRepositoryInterface,
    ) -> None:
        """Initialize training service with repositories.





        Args:


            training_job_repository: Repository for training jobs


            dataset_item_repository: Repository for dataset items


        """

        self._training_job_repository = training_job_repository

        self._dataset_item_repository = dataset_item_repository

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

        job_id = uuid4()

        # Create training job

        training_job = TrainingJob(
            id=job_id,
            user_id=user_id,
            status=TrainingStatus.PENDING,
            input_type=input_type,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )

        # Save training job

        created_job = await self._training_job_repository.create(training_job)

        # Create dataset items from chunks

        for i, chunk in enumerate(data_chunks):
            dataset_item = DatasetItem(
                id=uuid4(),
                training_job_id=job_id,
                chunk_index=i,
                content=chunk,
                input_type=input_type,
                created_at=datetime.utcnow(),
            )

            await self._dataset_item_repository.create(dataset_item)

        logger.info(f"Created training job {job_id} with {len(data_chunks)} chunks")

        return created_job

    async def start_training(self, job_id: UUID) -> TrainingJob:
        """Start training job execution.





        Args:


            job_id: ID of the training job





        Returns:


            Updated training job


        """

        updated_job = await self._training_job_repository.update_status(
            job_id, TrainingStatus.RUNNING
        )

        if updated_job is None:
            raise ValueError(f"Training job {job_id} not found")

        logger.info(f"Started training job {job_id}")

        return updated_job

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

        if not 0.0 <= progress <= 1.0:
            raise ValueError("Progress must be between 0.0 and 1.0")

        updated_job = await self._training_job_repository.update_progress(
            job_id, progress
        )

        if updated_job is None:
            raise ValueError(f"Training job {job_id} not found")

        logger.debug(f"Updated training job {job_id} progress to {progress:.2%}")

        return updated_job

    async def complete_training(self, job_id: UUID) -> TrainingJob:
        """Mark training job as completed.





        Args:


            job_id: ID of the training job





        Returns:


            Updated training job


        """

        updated_job = await self._training_job_repository.update_status(
            job_id, TrainingStatus.COMPLETED
        )

        if updated_job is None:
            raise ValueError(f"Training job {job_id} not found")

        # Update progress to 100%

        await self._training_job_repository.update_progress(job_id, 1.0)

        logger.info(f"Completed training job {job_id}")

        return updated_job

    async def fail_training(self, job_id: UUID, error_message: str) -> TrainingJob:
        """Mark training job as failed.





        Args:


            job_id: ID of the training job


            error_message: Error message describing the failure





        Returns:


            Updated training job


        """

        updated_job = await self._training_job_repository.update_status(
            job_id, TrainingStatus.FAILED
        )

        if updated_job is None:
            raise ValueError(f"Training job {job_id} not found")

        logger.error(f"Training job {job_id} failed: {error_message}")

        return updated_job

    async def get_user_training_jobs(self, user_id: UUID) -> list[TrainingJob]:
        """Get all training jobs for a user.





        Args:


            user_id: ID of the user





        Returns:


            List of user's training jobs


        """

        return await self._training_job_repository.get_by_user_id(user_id)

    async def get_training_job_stats(
        self, user_id: UUID | None = None
    ) -> dict[str, int]:
        """Get training job statistics.





        Args:


            user_id: Optional user ID to filter stats





        Returns:


            Dictionary with training job counts by status


        """

        stats: dict[str, int] = {
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
        }

        if user_id:
            # Get stats for specific user

            user_jobs = await self._training_job_repository.get_by_user_id(user_id)

            for job in user_jobs:
                status_key = job.status.value.lower()

                if status_key in stats:
                    stats[status_key] += 1

        else:
            # Get global stats by querying each status

            for status in TrainingStatus:
                status_key = status.value.lower()

                if status_key in stats:
                    jobs = await self._training_job_repository.list_by_status(status)

                    stats[status_key] = len(jobs)

        return stats
