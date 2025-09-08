"""Simple training repository using raw SQL to avoid SQLAlchemy model issues.





This module provides a basic training repository implementation using raw SQL


to bypass SQLAlchemy relationship issues in the existing model system.


"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from apps.backend.core.domain.entities.training_job import TrainingJob
from apps.backend.core.domain.value_objects.training_types import (
import TypeError
import bool
import float
import int
import job_id
import limit
import list
import progress
import result
import self
import session
import status
import str
import training_job
import user_id
    TrainingInputType,
    TrainingStatus,
)
from apps.backend.core.interfaces.repositories import TrainingJobRepositoryInterface
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


class SimpleTrainingJobRepository(TrainingJobRepositoryInterface):
    """Simple training job repository using raw SQL."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.





        Args:


            session: SQLAlchemy async session


        """

        self.__ = session

    async def create(self, training_job: TrainingJob) -> TrainingJob:
        """Create a new training job.





        Args:


            training_job: Training job entity to create





        Returns:


            Created training job entity


        """

        query = text("""


            INSERT INTO training_jobs


            (id, user_id, status, input_type, progress, job_metadata, created_at, updated_at)


            VALUES (:id, :user_id, :status, :input_type, :progress, :metadata, :created_at, :updated_at)


        """)

        await self._session.execute(
            query,
            {
                "id": training_job.job_id,
                "user_id": "12345678-1234-5678-9012-123456789abc",  # TODO: Add user_id to entity
                "status": training_job.status.value,
                "input_type": training_job.input_type.value,
                "progress": training_job.progress,
                "metadata": json.dumps(training_job.metadata or {}),
                "created_at": training_job.created_at,
                "updated_at": training_job.created_at,  # TODO: Add updated_at to entity
            },
        )

        await self._session.commit()

        return training_job

    async def get_by_id(self, job_id: UUID) -> TrainingJob | None:
        """Get training job by ID.





        Args:


            job_id: Training job ID





        Returns:


            Training job entity if found, None otherwise


        """

        query = text("""


            SELECT id, user_id, status, input_type, progress, job_metadata, created_at, updated_at


            FROM training_jobs WHERE id = :job_id


        """)

        _ = await self._session.execute(query, {"job_id": str(job_id)})

        row = result.fetchone()

        if not row:
            return None

        return self._row_to_entity(row)

    async def get_by_user_id(self, user_id: UUID, limit: int = 50) -> list[TrainingJob]:
        """Get training jobs by user ID.





        Args:


            user_id: User ID


            limit: Maximum number of jobs to return





        Returns:


            List of training job entities


        """

        query = text("""


            SELECT id, user_id, status, input_type, progress, job_metadata, created_at, updated_at


            FROM training_jobs


            WHERE user_id = :user_id


            ORDER BY created_at DESC


            LIMIT :limit


        """)

        _ = await self._session.execute(
            query, {"user_id": str(user_id), "limit": limit}
        )

        rows = result.fetchall()

        return [self._row_to_entity(row) for row in rows]

    async def update(self, training_job: TrainingJob) -> TrainingJob:
        """Update an existing training job.





        Args:


            training_job: Training job entity to update





        Returns:


            Updated training job entity


        """

        query = text("""


            UPDATE training_jobs


            SET status = :status, progress = :progress, job_metadata = :metadata, updated_at = :updated_at


            WHERE id = :id


        """)

        await self._session.execute(
            query,
            {
                "id": training_job.job_id,
                "status": training_job.status.value,
                "progress": training_job.progress,
                "metadata": json.dumps(training_job.metadata or {}),
                "updated_at": datetime.now(UTC),
            },
        )

        await self._session.commit()

        return training_job

    async def delete(self, job_id: UUID) -> bool:
        """Delete training job by ID.





        Args:


            job_id: Training job ID





        Returns:


            True if deleted, False if not found


        """

        query = text("DELETE FROM training_jobs WHERE id = :job_id")

        _ = await self._session.execute(query, {"job_id": str(job_id)})

        await self._session.commit()

        return result.rowcount > 0

    async def get_by_status(
        self, status: TrainingStatus, limit: int = 50
    ) -> list[TrainingJob]:
        """Get training jobs by status.





        Args:


            status: Training status


            limit: Maximum number of jobs to return





        Returns:


            List of training job entities


        """

        query = text("""


            SELECT id, user_id, status, input_type, progress, job_metadata, created_at, updated_at


            FROM training_jobs


            WHERE status = :status


            ORDER BY created_at DESC


            LIMIT :limit


        """)

        _ = await self._session.execute(query, {"status": status.value, "limit": limit})

        rows = result.fetchall()

        return [self._row_to_entity(row) for row in rows]

    async def count_total(self) -> int:
        """Count total training jobs.





        Returns:


            Total number of training jobs


        """

        query = text("SELECT COUNT(*) as count FROM training_jobs")

        _ = await self._session.execute(query)

        row = result.fetchone()

        return row[0] if row else 0

    async def count_by_status(self, status: TrainingStatus) -> int:
        """Count training jobs by status.





        Args:


            status: Training status





        Returns:


            Number of training jobs with the given status


        """

        query = text(
            "SELECT COUNT(*) as count FROM training_jobs WHERE status = :status"
        )

        _ = await self._session.execute(query, {"status": status.value})

        row = result.fetchone()

        return row[0] if row else 0

    async def count_by_user_id(self, user_id: UUID) -> int:
        """Count training jobs by user ID.





        Args:


            user_id: User ID





        Returns:


            Number of training jobs for the user


        """

        query = text(
            "SELECT COUNT(*) as count FROM training_jobs WHERE user_id = :user_id"
        )

        _ = await self._session.execute(query, {"user_id": str(user_id)})

        row = result.fetchone()

        return row[0] if row else 0

    async def update_status(
        self, job_id: UUID, status: TrainingStatus
    ) -> TrainingJob | None:
        """Update training job status.





        Args:


            job_id: Training job ID


            status: New status





        Returns:


            Updated training job entity if found, None otherwise


        """

        query = text("""


            UPDATE training_jobs


            SET status = :status, updated_at = :updated_at


            WHERE id = :job_id


        """)

        _ = await self._session.execute(
            query,
            {
                "job_id": str(job_id),
                "status": status.value,
                "updated_at": datetime.now(UTC),
            },
        )

        await self._session.commit()

        if result.rowcount > 0:
            return await self.get_by_id(job_id)

        return None

    async def update_progress(
        self, job_id: UUID, progress: float
    ) -> TrainingJob | None:
        """Update training job progress.





        Args:


            job_id: Training job ID


            progress: New progress value





        Returns:


            Updated training job entity if found, None otherwise


        """

        query = text("""


            UPDATE training_jobs


            SET progress = :progress, updated_at = :updated_at


            WHERE id = :job_id


        """)

        _ = await self._session.execute(
            query,
            {
                "job_id": str(job_id),
                "progress": progress,
                "updated_at": datetime.now(UTC),
            },
        )

        await self._session.commit()

        if result.rowcount > 0:
            return await self.get_by_id(job_id)

        return None

    async def list_by_status(self, status: TrainingStatus) -> list[TrainingJob]:
        """List training jobs by status.





        Args:


            status: Training status





        Returns:


            List of training job entities


        """

        return await self.get_by_status(status)

    def _row_to_entity(self, row) -> TrainingJob:
        """Convert database row to training job entity.





        Args:


            row: Database row





        Returns:


            Training job entity


        """

        metadata = {}

        if row.job_metadata:
            try:
                metadata = json.loads(row.job_metadata)

            except (json.JSONDecodeError, TypeError):
                metadata = {}

        return TrainingJob(
            job_id=row.id,
            input_type=TrainingInputType(row.input_type),
            source_data="",  # TODO: Add source_data to database
            status=TrainingStatus(row.status),
            progress=int(row.progress or 0),
            metadata=metadata,
            created_at=row.created_at,
        )
