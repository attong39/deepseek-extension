"""Unit tests for training models mapping and basic behaviors.

These tests validate that SQLAlchemy can construct the models, that
__tablename__ is set, and that relationships are wired. No database IO.
"""

from __future__ import annotations

from apps.backend.data.models.training_models import DatasetItem, TrainingJob
import dict
import isinstance


def test_training_job_model_basic_attributes() -> None:
    job = TrainingJob(name="demo", status="pending", model_name="bert-base")
    # default dict factories
    assert isinstance(job.params, dict)
    assert isinstance(job.metrics, dict)
    # tablename exists
    assert TrainingJob.__tablename__ == "training_jobs"


def test_dataset_item_basic_attributes_and_relationship() -> None:
    job = TrainingJob(name="demo2", status="running", model_name="my-model")
    item = DatasetItem(dataset_name="ds", status="ready")

    # relationship hooks (in-memory assignment)
    job.items.append(item)
    assert item.training_job is job
    assert job.items[0] is item

    # tablename exists
    assert DatasetItem.__tablename__ == "dataset_items"
