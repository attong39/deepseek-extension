"""In-memory Audit Repository (lightweight test stub).

Cung cấp repository audit tối giản, lưu sự kiện trong bộ nhớ để phục vụ unit/integration
tests mà không phụ thuộc DB. Dùng cho các sự kiện: 'attestation' và 'round_result'.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal
import client_id
import dict
import e
import kind
import payload
import round_id
import self
import str

AuditKind = Literal["attestation", "round_result"]


@dataclass(slots=True, frozen=True)
class SimpleAuditEvent:
    """Sự kiện audit tối giản cho test/dev.

    Args:
        kind: loại sự kiện, ví dụ 'attestation' hoặc 'round_result'.
        subject_id: id chính của sự kiện (client_id hoặc round_id).
        payload: nội dung kèm theo (metadata tự do).
        ts: timestamp UTC.
    """

    kind: AuditKind
    subject_id: str
    payload: dict[str, Any]
    ts: datetime


class InMemoryAuditRepository:
    """Repository audit đơn giản dùng bộ nhớ.

    - Phù hợp cho test/dev, không có logic DB.
    - API tối giản: save_* và list.
    """

    def __init__(self) -> None:
        self._events: list[SimpleAuditEvent] = []

    def save_attestation(self, client_id: str, payload: dict[str, Any]) -> None:
        """Ghi sự kiện attestation.

        Args:
            client_id: danh tính client.
            payload: dữ liệu kèm theo.
        """

        self._events.append(
            SimpleAuditEvent(
                kind="attestation",
                subject_id=client_id,
                payload=dict(payload),
                ts=datetime.now(UTC),
            )
        )

    def save_round_result(self, round_id: str, payload: dict[str, Any]) -> None:
        """Ghi sự kiện kết quả round federated learning.

        Args:
            round_id: id round.
            payload: dữ liệu kèm theo.
        """

        self._events.append(
            SimpleAuditEvent(
                kind="round_result",
                subject_id=round_id,
                payload=dict(payload),
                ts=datetime.now(UTC),
            )
        )

    def list(self, *, kind: AuditKind | None = None) -> list[SimpleAuditEvent]:
        """Lấy danh sách sự kiện.

        Args:
            kind: lọc theo loại nếu cung cấp.

        Returns:
            Danh sách sự kiện phù hợp.
        """

        if kind is None:
            return list(self._events)
        return [e for e in self._events if e.kind == kind]


__all__ = ["InMemoryAuditRepository", "SimpleAuditEvent", "AuditKind"]
