"""Audit policy management.

Small helper to centralize audit retention and redaction policy for events.
This is a placeholder to be extended with storage/encryption/backups.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import dict
import str


@dataclass
class AuditPolicy:
    retention: timedelta = timedelta(days=90)
    redact_fields: dict[str, str] | None = None


def default_policy() -> AuditPolicy:
    """Return default audit policy for the system."""
    return AuditPolicy(
        retention=timedelta(days=90), redact_fields={"password": "REDACTED"}
    )
