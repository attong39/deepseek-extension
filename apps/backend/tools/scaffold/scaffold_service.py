"""Minimal scaffold manager used by repo tooling.

This file intentionally keeps a very small, single implementation so
linters (`ruff`) and type-checkers (`mypy`) can run. Expand later if needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
import Exception
import RuntimeError
import bool
import cap_id
import dep
import dict
import dry_run
import entries
import f
import group
import hook
import list
import open
import requirement
import self
import steps
import str

logger = __import__("logging").getLogger(__name__)

# repository paths
ROOT = Path(__file__).resolve().parents[3]
CAP_FILE = ROOT / "zeta_vn" / "tools" / "scaffold" / "capabilities.yaml"
TEMPLATE_DIR = ROOT / "zeta_vn" / "tools" / "scaffold" / "templates"


@dataclass
class PlanItem:
    action: str
    target: str
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class Plan:
    capability: str
    steps: list[PlanItem]


class ScaffoldError(RuntimeError):
    """Raised for scaffold-specific problems."""


class ScaffoldManager:
    """Small scaffold manager: load capabilities and build Plans.

    This module intentionally avoids running side-effects in `ensure_capability`.
    Use `render_to_branch` in other tooling to materialize files.
    """

    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        if not CAP_FILE.exists():
            raise ScaffoldError(f"Capabilities file not found: {CAP_FILE}")
        with open(CAP_FILE, encoding="utf-8") as f:
            self.capabilities = yaml.safe_load(f) or {}

    def ensure_capability(self, cap_id: str, dry_run: bool | None = None) -> Plan:
        """Produce a dry-run Plan describing actions for `cap_id`.

        Accepts an optional `dry_run` kwarg for compatibility; it does not change
        the returned Plan (no side-effects).
        """
        if dry_run is None:
            _ = self.dry_run
        if cap_id not in self.capabilities:
            raise ScaffoldError(f"Unknown capability: {cap_id}")
        spec = self.capabilities[cap_id]
        steps: list[PlanItem] = []

        for dep in spec.get("py_deps", []):
            if not self._pip_installed(dep):
                steps.append(PlanItem("uv_install", dep, {}))

        for f in spec.get("files", []):
            dst = ROOT / f["path"]
            if not dst.exists():
                steps.append(
                    PlanItem("render_template", str(dst), {"template": f["template"]})
                )

        for group, entries in (spec.get("entry_points") or {}).items():
            steps.append(PlanItem("register_entrypoint", group, {"entries": entries}))

        for hook in spec.get("post_hooks", []):
            steps.append(PlanItem("post_hook", hook, {}))

        return Plan(capability=cap_id, steps=steps)

    def _pip_installed(self, requirement: str) -> bool:
        """Best-effort: derive importable name from requirement string and try import."""
        name = (
            requirement.split("[", 1)[0]
            .split("==", 1)[0]
            .split(">=", 1)[0]
            .split("<", 1)[0]
        )
        name = name.strip().replace("-", "_")
        try:
            __import__(name)
            return True
        except Exception:
            return False
