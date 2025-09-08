"""Optimizer module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import libcst as cst  # type: ignore
except Exception:  # pragma: no cover
    cst = None  # type: ignore

from typing import cast

from .duplicate_detector import DuplicateDetector
from .import_optimizer import ImportOptimizer


class AICodeOptimizer:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        # Load YAML optimizer config (may be empty)
        self.config = self._load_config(config_path)

    def optimize_project(self, root: Path) -> dict[str, Any]:
        files = self._get_source_files(root)
        print(f"[optimizer] Found {len(files)} Python files to process under {root}", flush=True)
        results: dict[str, Any] = {
            "import_optimizations": [],
            "duplicate_removals": [],
            "structure_enforcements": [],
        }

        # Imports
        if cst is not None:
            imp = ImportOptimizer()
            for idx, f in enumerate(files, 1):
                if idx % 25 == 0 or idx == 1:
                    print(f"[optimizer] Import pass {idx}/{len(files)}: {f}", flush=True)
                r = imp.optimize_file(f)
                results["import_optimizations"].append(r)

        # Duplicates
        dup = DuplicateDetector()
        dups = dup.find_duplicates([Path(f) for f in files])
        results["duplicate_removals"] = dups
        print(f"[optimizer] Duplicate scan complete: {len(dups)} groups", flush=True)

        # Structure
        if cst is not None:
            # Import only when libcst is available to avoid hard dependency
            from .structure_enforcer import StructureEnforcer  # type: ignore

            enforcer = StructureEnforcer(self.config_path)
            for idx, f in enumerate(files, 1):
                if Path(f).suffix == ".py":
                    changed = enforcer.enforce_structure(Path(f))
                    if changed:
                        results["structure_enforcements"].append({"file": f, "changes": "structure_enforced"})
                if idx % 25 == 0 or idx == len(files):
                    print(f"[optimizer] Structure pass {idx}/{len(files)}", flush=True)

        return results

    def _get_source_files(self, root: Path) -> list[str]:
        include_exts = {".py"}
        # Configurable scopes
        include_dirs = set(self.config.get("include_dirs", []))
        exclude_dirs = set(
            self.config.get(
                "exclude_dirs",
                [
                    "node_modules",
                    "dist",
                    "build",
                    "__pycache__",
                    ".git",
                    ".venv",
                    "venv",
                    "env",
                    ".env",
                    "site-packages",
                ],
            )
        )
        max_files = int(self.config.get("max_files", 0) or 0)
        out: list[str] = []
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix not in include_exts:
                continue
            parts = set(p.parts)
            if any(seg in exclude_dirs for seg in parts):
                continue
            if include_dirs and not any(seg in include_dirs for seg in parts):
                continue
            out.append(str(p))
            if max_files and len(out) >= max_files:
                break
        return out

    def _load_config(self, path: Path) -> dict[str, Any]:
        try:
            import yaml  # type: ignore
        except Exception:
            return {}
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return cast(dict[str, Any], data)
            return {}
        except Exception:
            return {}
import Exception
import any
import config_path
import dict
import enumerate
import f
import idx
import int
import isinstance
import len
import list
import out
import p
import path
import print
import results
import root
import seg
import self
import set
import str
