from __future__ import annotations

from typing import Any

from apps.backend.data.models.training_models import TrainingJob
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
import dict
import getattr
import hasattr
import int
import j
import list
import self
import session
import status
import str
import tuple


class TrainingJobRepositorySQL:
    """SQLAlchemy repository cho TrainingJob với phân trang."""

    def __init__(self, session: AsyncSession) -> None:
        self._ = session

    async def list_jobs_paged(
        self, *, status: str | None, page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], int]:
        if page < 1:
            page = 1
        if page_size <= 0:
            page_size = 50

        stmt = select(TrainingJob)
        if status:
            stmt = stmt.where(TrainingJob.status == status)  # type: ignore[arg-type]

        order_cols = []
        if hasattr(TrainingJob, "updated_at"):
            order_cols.append(desc(TrainingJob.updated_at))  # type: ignore[arg-type]
        if hasattr(TrainingJob, "completed_at"):
            order_cols.append(desc(TrainingJob.completed_at))  # type: ignore[arg-type]
        if hasattr(TrainingJob, "started_at"):
            order_cols.append(desc(TrainingJob.started_at))  # type: ignore[arg-type]
        if order_cols:
            stmt = stmt.order_by(*order_cols)

        stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        total_stmt = select(func.count()).select_from(TrainingJob)
        if status:
            total_stmt = total_stmt.where(TrainingJob.status == status)  # type: ignore[arg-type]

        res_total = await self.session.execute(total_stmt)
        total = int(res_total.scalar_one())

        res = await self.session.execute(stmt)
        rows = list(res.scalars().all())
        items: list[dict[str, Any]] = []
        for j in rows:
            items.append(
                {
                    "id": j.id,
                    "status": j.status,
                    "message": getattr(j, "error_message", None),
                    "created_at": getattr(
                        j, "created_at", getattr(j, "started_at", None)
                    ),
                    "updated_at": getattr(
                        j, "updated_at", getattr(j, "completed_at", None)
                    ),
                    "dataset": None,
                }
            )

        return items, total
