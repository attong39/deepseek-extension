"""
Logs API - Quản lý system logs
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.api.v1._schemas import LogItem
from fastapi import APIRouter, Query
import LOGS
import component
import dict
import int
import job_id
import level
import limit
import list
import msg
import offset
import str

router = APIRouter(prefix="/v1/logs", tags=["logs"])

# In-memory logs storage cho demo
LOGS: dict[str, LogItem] = {}


def _add_log(
    level: str, msg: str, component: str = "system", job_id: str | None = None
) -> None:
    """Thêm log entry"""
    log_id = f"log_{uuid.uuid4().hex[:8]}"
    log = LogItem(
        ts=datetime.now(UTC),
        level=level,  # type: ignore[arg-type]
        msg=msg,
        component=component,
        job_id=job_id,
    )
    LOGS[log_id] = log


# Seed some demo logs
_add_log("INFO", "ZETA_VN server started", "main")
_add_log("INFO", "Event bus initialized", "events")
_add_log("DEBUG", "Training service ready", "training")


@router.get("", response_model=list[LogItem])
async def get_logs(
    level: str | None = Query(None, description="Filter by log level"),
    limit: int = Query(50, ge=1, le=1000, description="Max number of logs"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    component: str | None = Query(None, description="Filter by component"),
    job_id: str | None = Query(None, description="Filter by job ID"),
) -> list[LogItem]:
    """Lấy danh sách logs với filters"""
    logs = list(LOGS.values())

    # Apply filters
    if level:
        logs = [log for log in logs if log.level == level]

    if component:
        logs = [log for log in logs if log.component == component]

    if job_id:
        logs = [log for log in logs if log.job_id == job_id]

    # Sort by timestamp descending (newest first)
    logs.sort(key=lambda log: log.ts, reverse=True)

    # Apply pagination
    return logs[offset : offset + limit]


@router.post("/add")
async def add_log_entry(
    level: str, msg: str, component: str = "system", job_id: str | None = None
) -> dict[str, str]:
    """Thêm log entry mới (for testing)"""
    _add_log(level, msg, component, job_id)
    return {"message": "Log added successfully"}


@router.delete("/clear")
async def clear_logs() -> dict[str, str]:
    """Xóa tất cả logs (for testing)"""
    LOGS.clear()
    # Re-seed basic logs
    _add_log("INFO", "ZETA_VN server started", "main")
    _add_log("INFO", "Event bus initialized", "events")
    _add_log("DEBUG", "Training service ready", "training")

    return {"message": "Logs cleared and re-seeded"}
