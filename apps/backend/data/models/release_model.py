"""Release model for self-upgrade records.

This is a minimal model stub. Add proper ORM mapping (SQLAlchemy) per project conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import str


@dataclass
class ReleaseRecord:
    release_id: str
    image: str
    checksum: str | None
    status: str = "planned"
    started_at: datetime | None = None
    finished_at: datetime | None = None
