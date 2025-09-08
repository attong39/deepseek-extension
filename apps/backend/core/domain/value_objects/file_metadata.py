"""File metadata value object."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class FileMetadata:
    """Immutable file metadata."""
import ValueError
import bool
import int
import len
import property
import self
import str

    name: str

    mime_type: str

    size_bytes: int

    checksum: str | None = None

    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")

        if "/" not in self.mime_type:
            raise ValueError("mime_type must be a valid type/subtype string")

        if self.size_bytes < 0:
            raise ValueError("size_bytes must be >= 0")

        if self.checksum is not None and not re.fullmatch(
            r"[A-Fa-f0-9]{32,64}", self.checksum
        ):
            raise ValueError("checksum must be a hex digest (32-64 chars) if provided")

    @property
    def extension(self) -> str:
        """Best-effort lowercase extension without dot; empty if none."""

        parts = self.name.rsplit(".", 1)

        return parts[1].lower() if len(parts) == 2 else ""

    def is_binary(self) -> bool:
        """Heuristic: return True for common binary MIME types."""

        return not self.mime_type.startswith("text/")
