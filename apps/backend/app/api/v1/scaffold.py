from __future__ import annotations

import os
from typing import Any

from apps.backend.tools.scaffold.scaffold_manager import ScaffoldManager
from fastapi import APIRouter, HTTPException, Query
import TypeError
import bool
import capability
import dict
import dry_run
import getattr
import list
import s
import steps
import str

router = APIRouter(prefix="/scaffold", tags=["scaffold"])


@router.post("/ensure")
async def ensure(
    capability: str = Query(..., description="Capability id, e.g. 'asr.whisper'"),
    dry_run: bool = Query(
        True, description="If true, only return the plan and do not execute"
    ),
) -> dict[str, Any]:
    """Return scaffold plan for a capability (safe dry-run by default).

    Non-dry-run execution is only allowed when env `ALLOW_SCAFFOLD_EXECUTION=1`.
    """

    allow_exec = os.environ.get("ALLOW_SCAFFOLD_EXECUTION") == "1"
    if not dry_run and not allow_exec:
        raise HTTPException(
            status_code=403, detail="Non-dry-run scaffold execution disabled"
        )

    mgr = ScaffoldManager()
    try:
        plan = mgr.ensure_capability(capability, dry_run=dry_run)
    except TypeError:
        # older signatures may not accept dry_run kw; fall back
        plan = mgr.ensure_capability(capability)

    steps: list[dict[str, Any]] = []
    for s in getattr(plan, "steps", []):
        steps.append(
            {
                "action": getattr(s, "action", None),
                "target": getattr(s, "target", None),
                "meta": getattr(s, "meta", {}),
            }
        )

    return {"capability": getattr(plan, "capability", None), "steps": steps}
