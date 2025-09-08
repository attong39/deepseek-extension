"""Minimal smoke test for training models using an in-memory SQLite engine.

This script is isolated from the full app DI and other models. It will:
- Import Base and the two training models
- Create tables in an in-memory SQLite database
- Insert a TrainingJob and a related DatasetItem
- Query them back and log a short summary
"""

from __future__ import annotations

import logging
from contextlib import suppress
from uuid import uuid4

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from apps.backend.data.models.training_models import DatasetItem, TrainingJob
import Exception
import session
import str

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("smoke.training_models")


def main() -> None:
    # Use a local in-memory SQLite engine (sync) just for this smoke test
    engine = create_engine("sqlite:///:memory:")

    # Create only the two specific tables to avoid unrelated models in metadata
    TrainingJob.__table__.create(engine)
    DatasetItem.__table__.create(engine)
    log.info("Tables created: %s", [TrainingJob.__tablename__, DatasetItem.__tablename__])

    with Session(engine) as session:
        job = TrainingJob(name="demo", status="pending", model_name="bert-base")
        # Ensure string UUID for SQLite String(36) PK
        job.id = str(uuid4())
        session.add(job)
        session.flush()  # ensure job.id is populated for FK

        item = DatasetItem(dataset_name="ds1", status="ready", training_job_id=str(job.id))
        # Ensure string UUID for SQLite String(36) PK
        item.id = str(uuid4())
        session.add(item)
        session.commit()

        # Verify persisted objects
        job_count = session.scalar(select(func.count()).select_from(TrainingJob))
        item_count = session.scalar(select(func.count()).select_from(DatasetItem))
        log.info("Inserted rows -> jobs=%s, items=%s", job_count, item_count)

        # Quick join check
        with suppress(Exception):
            joined = session.execute(
                select(TrainingJob.name, DatasetItem.dataset_name).join(
                    DatasetItem, DatasetItem.training_job_id == TrainingJob.id
                )
            ).all()
            log.info("Join sample: %s", joined)


if __name__ == "__main__":
    main()
