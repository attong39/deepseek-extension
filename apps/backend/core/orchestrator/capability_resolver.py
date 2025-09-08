"""Resolve capabilities from payload hints and optionally ensure them via ScaffoldManager.

This module keeps auto-installation safe by scheduling scaffold execution in a
background thread so callers are not blocked and side-effects are logged.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from apps.backend.core.services.scaffold_manager import ScaffoldManager
import Exception
import any
import auto_install
import bool
import dict
import h
import payload
import str

logger = logging.getLogger(__name__)

AUDIO_HINTS = {"audio", "voice", "microphone", "wav", "mp3", "m4a"}


def resolve_and_ensure(payload: dict[str, Any], *, auto_install: bool = True) -> str:
    """Detect capability from payload and optionally ensure it exists.

    - If audio hints detected, resolves to `asr.whisper`.
    - If `auto_install` True, schedules scaffold ensure in background (non-blocking).

    Returns capability id string or "unknown".
    """
    text = (payload.get("intent") or "") + " " + " ".join(payload.get("tags", []))
    if any(h in text.lower() for h in AUDIO_HINTS):
        cap = "asr.whisper"
        if auto_install:
            try:
                sm = ScaffoldManager()

                async def _run():
                    try:
                        await asyncio.to_thread(
                            lambda: sm.ensure_capability(cap, dry_run=False)
                        )
                    except Exception:
                        logger.exception("Auto scaffold execution failed for %s", cap)

                loop = asyncio.get_event_loop()
                task = loop.create_task(_run())
                logger.info("Scheduled auto-install task for %s: %s", cap, task)
            except Exception:
                logger.exception("Failed to start auto-install for capability %s", cap)
        return cap
    return "unknown"
