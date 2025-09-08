# zeta_vn/app/api/v1/_common_audit.py
from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any
import actor
import dict
import event
import payload
import str

logger = logging.getLogger("zeta.audit")


def audit(event: str, actor: str | None, payload: dict[str, Any] | None = None) -> None:
    doc = {
        "ts": datetime.now(UTC).isoformat(),
        "event": event,
        "actor": actor,
        "payload": payload or {},
    }
    logger.info(json.dumps(doc, ensure_ascii=False))
