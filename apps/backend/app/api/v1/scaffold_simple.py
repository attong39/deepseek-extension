from __future__ import annotations

import os
from typing import Any

from apps.backend.tools.scaffold.scaffold_manager import ScaffoldManager
from fastapi import APIRouter, HTTPException, Query
import bool
import capability
import dry_run
import s
import str

router = APIRouter(prefix="/scaffold", tags=["scaffold"])


@router.post("/ensure")
async def ensure(capability: str = Query(...), dry_run: bool = True) -> Any:
    """Return scaffold plan for a capability (safe dry-run by default).

    Non-dry-run execution is only allowed when env `ALLOW_SCAFFOLD_EXECUTION=1`.
    """
    allow_exec = os.environ.get("ALLOW_SCAFFOLD_EXECUTION") == "1"
    if not dry_run and not allow_exec:
        raise HTTPException(
            status_code=403, detail="Non-dry-run scaffold execution disabled"
        )

    mgr = ScaffoldManager(dry_run=dry_run)
    plan = mgr.ensure_capability(capability)
    return {
        "capability": plan.capability,
        "steps": [
            {"action": s.action, "target": s.target, "meta": s.meta} for s in plan.steps
        ],
    }
