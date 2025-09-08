"""Repository-facing training models compatibility layer.

This module re-exports the canonical SQLAlchemy models from
``zeta_vn.data.models.training_models`` with the names expected by repository
implementations (``TrainingJobModel``, ``DatasetItemModel``). It also exposes
``Base`` for tests that import it via this path.
"""

from __future__ import annotations

from apps.backend.data.models.base import Base
from apps.backend.data.models.training_models import DatasetItem as DatasetItemModel
from apps.backend.data.models.training_models import TrainingJob as TrainingJobModel

__all__ = [
    "Base",
    "TrainingJobModel",
    "DatasetItemModel",
]
