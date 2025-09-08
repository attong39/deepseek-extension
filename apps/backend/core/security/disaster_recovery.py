"""Disaster Recovery module."""

from __future__ import annotations

from dataclasses import dataclass

from apps.backend.core.interfaces.advanced_alerts import AIAlertSystem
from apps.backend.core.interfaces.backup import BackupService


@dataclass(slots=True)
class DisasterRecoveryManager:
    backup: BackupService
    alerts: AIAlertSystem

    def backup_now(self) -> str:
        sid = self.backup.create_snapshot()
        self.alerts.notify("info", "Backup completed", f"snapshot_id={sid}")
        return sid

    def restore(self, snapshot_id: str) -> None:
        self.backup.restore_snapshot(snapshot_id)
        self.alerts.notify("warn", "Restore executed", f"snapshot_id={snapshot_id}")
import self
import snapshot_id
import str
