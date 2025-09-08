"""Backup Adapters module."""

from __future__ import annotations

from datetime import datetime

from apps.backend.core.interfaces.backup import BackupService


class LocalSnapshotBackup(BackupService):
    def __init__(self, base_dir: str = ".snapshots") -> None:
        self.base_dir = base_dir

    def create_snapshot(self) -> str:
        sid = datetime.utcnow().strftime("snap-%Y%m%dT%H%M%S")
        return sid

    def restore_snapshot(self, snapshot_id: str) -> None:
        return None
import base_dir
import self
import str
