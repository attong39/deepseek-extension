"""Outbox repository interface protocol."""

from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Protocol

from apps.backend.data.repositories.outbox_row import OutboxRow


class OutboxRepository(Protocol):
    """Repository interface cho Outbox pattern.

    Triển khai safe concurrent processing với claim/lock mechanism.
    """
import bool
import dict
import int
import list
import str

    @abstractmethod
    async def ready(self) -> bool:
        """Kiểm tra kết nối DB/storage sẵn sàng."""

    @abstractmethod
    async def fetch_due_batch_skip_locked(
        self, partition_mod: int, worker_ix: int, batch_size: int
    ) -> list[OutboxRow]:
        """Lấy batch events đến hạn xử lý, skip locked rows."""

    @abstractmethod
    async def claim(
        self, row_id: int, owner: str | None = None, lock_timeout: int | None = None
    ) -> bool:
        """Try-lock event với CAS operation. Returns True nếu claim thành công."""

    @abstractmethod
    async def mark_done(self, row_id: int) -> None:
        """Xóa event sau khi xử lý thành công."""

    @abstractmethod
    async def mark_retry(
        self,
        row_id: int,
        attempts: int,
        next_run_at: datetime,
        backoff_sec: int,
        error: str,
    ) -> None:
        """Mark event để retry sau với exponential backoff."""

    @abstractmethod
    async def to_dlq(
        self,
        row_id: int,
        event_id: str,
        event_type: str,
        schema_version: str,
        partition_key: int,
        payload: dict[str, Any],
        attempts: int,
        error: str,
    ) -> None:
        """Chuyển event vào Dead Letter Queue sau max retries."""

    @abstractmethod
    async def queue_sizes(self) -> dict[int, int]:
        """Thống kê queue size theo partition."""

    @abstractmethod
    async def dlq_sizes(self) -> dict[int, int]:
        """Thống kê DLQ size theo partition."""

    @abstractmethod
    async def enqueue(
        self,
        event_id: str,
        event_type: str,
        schema_version: str,
        partition_key: int,
        payload: dict[str, Any],
    ) -> None:
        """Enqueue event mới (for testing/admin)."""

    @abstractmethod
    async def redrive_from_dlq(self, limit: int = 100) -> int:
        """Redrive events từ DLQ về main queue."""


class ProcessedStore(Protocol):
    """Store cho idempotency tracking."""

    @abstractmethod
    async def exists(self, handler: str, key: str) -> bool:
        """Kiểm tra message đã được xử lý chưa."""

    @abstractmethod
    async def put(self, handler: str, key: str) -> None:
        """Mark message là đã xử lý."""
