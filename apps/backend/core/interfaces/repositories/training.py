"""Training module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.domain.entities.dataset_item import DatasetItem
    from apps.backend.core.domain.entities.training_job import TrainingJob
    from apps.backend.core.domain.value_objects.training_types import (
        TrainingInputType,
        TrainingStatus,
    )


class TrainingJobRepository(ABC):
    @abstractmethod
    async def create(self, training_job: TrainingJob) -> TrainingJob: ...

    @abstractmethod
    async def get_by_id(self, job_id: UUID) -> TrainingJob | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[TrainingJob]: ...

    @abstractmethod
    async def update_status(
        self, job_id: UUID, status: TrainingStatus
    ) -> TrainingJob | None: ...

    @abstractmethod
    async def update_progress(
        self, job_id: UUID, progress: float
    ) -> TrainingJob | None: ...

    @abstractmethod
    async def list_by_status(self, status: TrainingStatus) -> list[TrainingJob]: ...

    @abstractmethod
    async def delete(self, job_id: UUID) -> bool: ...


class DatasetItemRepository(ABC):
    @abstractmethod
    async def create(self, dataset_item: DatasetItem) -> DatasetItem: ...

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> DatasetItem | None: ...

    @abstractmethod
    async def get_by_job_id(self, job_id: UUID) -> list[DatasetItem]: ...

    @abstractmethod
    async def list_by_type(
        self, input_type: TrainingInputType
    ) -> list[DatasetItem]: ...

    @abstractmethod
    async def delete(self, item_id: UUID) -> bool: ...
import bool
import float
import list
