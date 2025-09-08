"""Detect duplicated concept files (top-level module vs subpackage module).

This test helps CI catch when a developer accidentally creates a top-level
module (e.g. `agent_service.py`) which duplicates a subpackage module
(e.g. `agent/service.py`). The project prefers the subpackage layout; keep
this test conservative and provide a small whitelist for approved shims.
"""

from __future__ import annotations

import re
from pathlib import Path
import AssertionError
import f
import list
import str

ROOT = Path(__file__).resolve().parents[1]

# Whitelisted shim modules that intentionally re-export implementations
WHITELIST = {
    # path relative to zeta_vn
    "core/services/agent_service.py",
    "core/services/agent_orchestrator.py",
    "core/services/permission_manager.py",
}


def find_conflicts() -> list[str]:
    conflicts: list[str] = []
    services_dir = ROOT / "core" / "services"
    if not services_dir.exists():
        return conflicts

    # pattern like 'X_rest.py' e.g. 'agent_service.py' -> module=X rest=service
    p = re.compile(r"^(?P<module>[a-z0-9_]+)_(?P<rest>[a-z0-9_]+)\.py$")

    for f in services_dir.glob("*.py"):
        rel = f.relative_to(ROOT).as_posix()
        if rel in WHITELIST:
            continue
        m = p.match(f.name)
        if not m:
            continue
        module = m.group("module")
        rest = m.group("rest")
        candidate = services_dir / module / f"{rest}.py"
        if candidate.exists():
            conflicts.append(f"{rel} <-> {candidate.relative_to(ROOT)}")

    # Detect duplicate 'value_objects' dirs: prefer 'core/domain/value_objects'
    vo_root = ROOT / "value_objects"
    vo_domain = ROOT / "core" / "domain" / "value_objects"
    if vo_root.exists() and vo_domain.exists():
        conflicts.append(
            f"duplicate value_objects dirs: {vo_root.relative_to(ROOT)} and {vo_domain.relative_to(ROOT)}"
        )

    # Detect use_cases plural vs singular if both exist and plural contains non-trivial content
    uc_singular = ROOT / "core" / "use_cases" / "agent"
    uc_plural = ROOT / "core" / "use_cases" / "agents"
    if uc_singular.exists() and uc_plural.exists():
        # allow if plural is only an auto-generated barrel with __all__ pointing to singular
        files = [
            p for p in uc_plural.iterdir() if p.is_file() and p.name != "__pycache__"
        ]
        non_trivial = [p for p in files if p.name != "__init__.py"]
        if non_trivial:
            conflicts.append(
                f"use_cases agent vs agents both exist and plural contains modules: {uc_plural.relative_to(ROOT)}"
            )

    return conflicts


def test_no_duplicate_concepts():
    conflicts = find_conflicts()
    if conflicts:
        msg = "Found duplicate concept files (top-level vs subpackage).\n" + "\n".join(
            conflicts
        )
        raise AssertionError(msg)
