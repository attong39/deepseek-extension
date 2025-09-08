"""Backup module."""

from __future__ import annotations

from typing import Protocol


class BackupService(Protocol):
    def create_snapshot(self) -> str: ...

    def restore_snapshot(self, snapshot_id: str) -> None: ...
import str
