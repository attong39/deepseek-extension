"""
API schemas cho ZETA_VN v1.0
Chuẩn Pydantic v2, camelCase FE ↔ snake_case BE
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field
import bool
import dict
import float
import int
import list
import str


class UploadResp(BaseModel):
    """Response sau khi upload file thành công"""

    file_id: str
    kind: Literal["text", "image", "video", "audio", "other"]
    path: str
    size_bytes: int
    original_name: str


class TrainingJobCreate(BaseModel):
    """Request tạo training job mới"""

    name: str = Field(min_length=1, max_length=200)
    dataset_file_ids: list[str] = Field(default_factory=list)
    model: str = Field(default="zeta-mini")
    lr: float = Field(default=1e-4, ge=1e-6, le=1e-1)
    epochs: int = Field(default=1, ge=1, le=100)
    batch_size: int = Field(default=32, ge=1, le=512)


class TrainingJob(BaseModel):
    """Training job state"""

    id: str
    name: str
    status: Literal["PENDING", "RUNNING", "PAUSED", "CANCELLED", "FAILED", "SUCCEEDED"]
    progress: float = Field(ge=0.0, le=1.0)
    created_at: datetime
    updated_at: datetime
    model: str
    lr: float
    epochs: int
    current_epoch: int = 0
    loss: float | None = None
    dataset_file_ids: list[str]


class TrainingAction(BaseModel):
    """Control action cho training job"""

    action: Literal["pause", "resume", "cancel"]


class RuleUpsert(BaseModel):
    """Upsert nguyên tắc AI"""

    text: str = Field(min_length=1, max_length=2000)
    category: str = Field(default="general", max_length=50)
    priority: int = Field(default=1, ge=1, le=10)


class RuleResp(BaseModel):
    """Rule response"""

    id: str
    text: str
    category: str
    priority: int
    created_at: datetime
    is_active: bool = True


class LogItem(BaseModel):
    """Log entry"""

    ts: datetime
    level: Literal["DEBUG", "INFO", "WARN", "ERROR"]
    msg: str
    component: str = "system"
    job_id: str | None = None


class LogsQuery(BaseModel):
    """Query params cho logs"""

    level: Literal["DEBUG", "INFO", "WARN", "ERROR"] | None = None
    limit: int = Field(default=50, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
    component: str | None = None
    job_id: str | None = None


class HealthResp(BaseModel):
    """Health check response"""

    ok: bool
    version: str = "1.0.0"
    uptime_seconds: float
    components: dict[str, bool]


class NotificationMessage(BaseModel):
    """WebSocket notification"""

    type: Literal["info", "warning", "error", "success"]
    title: str
    message: str
    timestamp: datetime
    auto_dismiss: bool = True


class TrainingProgress(BaseModel):
    """Training progress event"""

    type: Literal["progress", "status", "log", "done", "error"]
    job_id: str
    status: str | None = None
    progress: float | None = None
    current_epoch: int | None = None
    loss: float | None = None
    message: str | None = None
    timestamp: datetime
