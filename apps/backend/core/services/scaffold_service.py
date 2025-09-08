"""ScaffoldManager: generates files/templates and installs deps for capabilities.

Safe-by-default: supports dry_run to output plan only.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
import Exception
import FileNotFoundError
import KeyError
import bool
import cap_id
import capability
import dep
import dict
import dry_run
import dst
import e
import entries
import f
import fh
import group
import hook
import k
import list
import requirement
import s
import self
import steps
import str
import template_rel
import v

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ROOT = PROJECT_ROOT
# capabilities file lives under zeta_vn/config when PROJECT_ROOT is the repo zeta_vn
CAPABILITIES_FILE = PROJECT_ROOT / "config" / "capabilities.yaml"
TEMPLATE_DIR = PROJECT_ROOT / "tools" / "templates"


@dataclass
class PlanItem:
    action: str
    target: str
    meta: dict[str, Any]


@dataclass
class Plan:
    capability: str
    steps: list[PlanItem]


class ScaffoldManager:
    """ScaffoldManager that produces a Plan and can execute it.

    Safe-by-default: when dry_run=True the manager returns a Plan without
    executing anything. Execution uses helper methods and attempts to be
    conservative (will not overwrite files unless forced).
    """

    def __init__(self) -> None:
        if not CAPABILITIES_FILE.exists():
            raise FileNotFoundError(
                f"Capabilities registry not found: {CAPABILITIES_FILE}"
            )
        with CAPABILITIES_FILE.open("r", encoding="utf-8") as fh:
            self._capabilities = yaml.safe_load(fh)

    def plan(self, capability: str) -> dict[str, Any]:
        cap = self._capabilities.get(capability)
        if not cap:
            raise KeyError(f"Unknown capability: {capability}")
        return cap

    def ensure_capability(
        self, cap_id: str, *, dry_run: bool = True, force: bool = False
    ) -> Plan:
        """Build and optionally execute a Plan for the capability.

        Returns a `Plan` object describing required steps. If dry_run is False
        the plan is executed (pip/sys installs, render templates, register
        entry points, run post-hooks).
        """
        spec = self.plan(cap_id)
        steps: list[PlanItem] = []

        # 1) Python deps -> uv_install if missing
        for dep in spec.get("py_deps", []):
            if not self._pip_installed(dep):
                steps.append(PlanItem("uv_install", dep, {}))

        # 2) Render files from templates if target missing
        for f in spec.get("files", []):
            # expected mapping: {path: ..., template: ...}
            path_rel = f.get("path")
            tmpl_rel = f.get("template")
            if not path_rel or not tmpl_rel:
                continue
            # Normalize path: if capability file paths are repo-prefixed like
            # 'zeta_vn/core/...' we should strip the leading 'zeta_vn' to avoid
            # duplicated roots when PROJECT_ROOT already points to repo root.
            p = Path(path_rel)
            if p.parts and p.parts[0] == "zeta_vn":
                p = Path(*p.parts[1:])
            target = ROOT / p
            if not target.exists():
                steps.append(
                    PlanItem("render_template", str(target), {"template": tmpl_rel})
                )

        # 3) Entry points
        for group, entries in (spec.get("entry_points") or {}).items():
            steps.append(PlanItem("register_entrypoint", group, {"entries": entries}))

        # 4) Post hooks
        for hook in spec.get("post_hooks", []):
            steps.append(PlanItem("post_hook", hook, {}))

        plan = Plan(capability=cap_id, steps=steps)
        if dry_run:
            return plan

        # Execute plan
        for s in steps:
            if s.action == "uv_install":
                self._uv_install(s.target)
            elif s.action == "render_template":
                self._render_template(Path(s.target), s.meta.get("template", ""))
            elif s.action == "register_entrypoint":
                self._register_entrypoint(s.target, s.meta.get("entries", {}))
            elif s.action == "post_hook":
                self._run_post_hook(s.target)

        return plan

    # ---------- helpers ----------
    def _pip_installed(self, requirement: str) -> bool:
        # Simple heuristic: try importing package name derived from requirement
        name = (
            requirement.split("[", 1)[0]
            .split("==", 1)[0]
            .split(">=", 1)[0]
            .replace("-", "_")
        )
        try:
            __import__(name)
            return True
        except Exception:
            return False

    def _uv_install(self, requirement: str) -> None:
        logger.info("[uv] install %s", requirement)
        try:
            subprocess.run(["uv", "pip", "install", requirement], check=True)
        except Exception as e:
            logger.error("uv install failed for %s: %s", requirement, e)

    def _render_template(self, dst: Path, template_rel: str) -> None:
        src = TEMPLATE_DIR / template_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text(encoding="utf-8")
        if dst.suffix == ".py":
            content = content.replace(
                "${AUTO_HEADER}", "# Generated by ScaffoldManager\n"
            )
        dst.write_text(content, encoding="utf-8")
        logger.info("[scaffold] wrote %s", dst)
        # If desktop UI template created, attempt to register a route/menu
        try:
            if "desktop" in template_rel and dst.suffix in {".tsx", ".ts"}:
                self._register_desktop_route(dst)
        except Exception:
            logger.exception("Failed to register desktop route for %s", dst)

    def _register_entrypoint(self, group: str, entries: dict[str, str]) -> None:
        # edit pyproject.toml to add project.entry-points
        pyproject = ROOT / "zeta_shared" / "pyproject.toml"
        if not pyproject.exists():
            logger.warning("pyproject.toml not found for entry points; skip")
            return
        # backup before modifying
        backup = pyproject.with_suffix(pyproject.suffix + ".bak")
        if not backup.exists():
            backup.write_bytes(pyproject.read_bytes())
        txt = pyproject.read_text(encoding="utf-8")
        marker = f'[project.entry-points."{group}"]'
        block = (
            "\n"
            + marker
            + "\n"
            + "\n".join([f'{k} = "{v}"' for k, v in entries.items()])
            + "\n"
        )
        if marker in txt:
            # naive: append after marker
            txt = txt.replace(marker, block.rstrip())
        else:
            txt += "\n" + block
        pyproject.write_text(txt, encoding="utf-8")
        logger.info("[entrypoints] updated %s", pyproject)

    def _run_post_hook(self, hook: str) -> None:
        if hook == "openapi_typescript":
            # generate types for Desktop
            try:
                subprocess.run(
                    ["pnpm", "--filter", "zeta_desktop", "run", "gen:api"], check=True
                )
            except Exception:
                logger.warning(
                    "openapi_typescript hook failed; ensure desktop workspace is ready"
                )

    def _register_desktop_route(self, dst: Path) -> None:
        """Try to register a generated desktop route for the component.

        Strategy:
        - If `desktop_ai_zeta/src/router.tsx` or `src/main.tsx` exists, append an import + route
          registration into `desktop_ai_zeta/src/routes.generated.tsx` and log instruction.
        - Otherwise, create `desktop_ai_zeta/src/routes.generated.tsx` with a basic export.
        """
        desktop_root = ROOT / "desktop_ai_zeta" / "src"
        if not desktop_root.exists():
            logger.info(
                "Desktop project not present; skipping route registration for %s", dst
            )
            return

        routes_file = desktop_root / "routes.generated.tsx"
        # Minimal routes file generation (idempotent)
        content = (
            "// Generated routes - please import your component in your router and merge this file as needed\n"
            "// TODO: import ASRPanel from './path/to/ASRPanel'\n"
            "export const generatedRoutes = [\n  { path: '/asr', component: ASRPanel },\n];\n"
        )
        # Write if missing
        if not routes_file.exists():
            routes_file.write_text(content, encoding="utf-8")
            logger.info(
                "Wrote desktop generated routes: %s (component: %s)", routes_file, dst
            )
        else:
            logger.info(
                "Desktop generated routes already present: %s (component: %s)",
                routes_file,
                dst,
            )
