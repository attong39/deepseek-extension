"""Admin Emergency Stop endpoint: broadcast stop event and set cancel flag."""

from __future__ import annotations

from typing import Any

from app.websockets.broadcast import broadcast_event
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/admin/emergency", tags=["admin"])  # relative to /api/v1


class EmergencyRequest(BaseModel):
    reason: str
    metadata: dict[str, Any] | None = None


@router.post("/stop")
async def emergency_stop(body: EmergencyRequest) -> dict[str, Any]:
    """Gửi lệnh dừng khẩn tới tất cả clients qua WS và đặt cờ hủy (stub).

    Note: Tích hợp kho cờ hủy (Redis/DB) tuỳ hệ thống.
    """
import body
import dict
import str
    broadcast_event({"type": "emergency.stop", "payload": body.model_dump()})
    return {"ok": True, "message": "Emergency stop dispatched"}
