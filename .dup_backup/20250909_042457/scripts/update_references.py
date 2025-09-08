#!/usr/bin/env python3
"""
update_references.py

Update Python and TS/JS import references based on consolidation plan exact duplicates.
For each redundant -> canonical mapping, update references in files under --root.

Usage (PowerShell):
  python scripts/update_references.py --plan reports/consolidation_plan/plan.json --root . --dry-run
  python scripts/update_references.py --plan reports/consolidation_plan/plan.json --root . --apply

Notes:
- Python: converts imports that reference redundant module path to canonical.
- TS/JS: updates relative imports pointing to redundant to point to canonical.
- This is a heuristic search/replace with safeguards. Always run with --dry-run first.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
import Exception
import SystemExit
import ValueError
import changes
import d
import dict
import dirnames
import dirpath
import dst_mod
import e
import exact_groups
import ext
import file_path
import filenames
import fn
import fp
import from_file
import int
import isinstance
import item
import len
import list
import m
import n
import n1
import n2
import pat
import path
import print
import py_map
import r
import rep
import set
import sorted
import src_mod
import str
import to_file
import ts_map
import tuple
import v

CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
TS_EXTS = ("", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")


def load_plan(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "exact_groups" not in data:
        raise ValueError("Invalid plan.json structure: missing 'exact_groups'")
    return data


EXCLUDE_DIRS_DEFAULT = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "out",
    "__pycache__",
    "reports",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
}


def gather_files(root: Path, exclude_dirs: set[str] | None = None) -> list[Path]:
    files: list[Path] = []
    exclude = set(EXCLUDE_DIRS_DEFAULT)
    if exclude_dirs:
        exclude |= set(exclude_dirs)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in CODE_EXTS:
                files.append(p)
    return files


def python_module_from_path(root: Path, file_path: Path) -> str:
    rel = file_path.resolve().relative_to(root.resolve())
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    return ".".join(parts)


def ts_relative_spec(from_file: Path, to_file: Path) -> str:
    rel = Path(".") / Path(to_file.resolve()).relative_to(from_file.resolve().parent)
    s = rel.as_posix()
    for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"):
        if s.endswith(ext):
            s = s[: -len(ext)]
            break
    return s


def _strip_known_ts_ext(spec: str) -> str:
    for e in TS_EXTS[1:]:  # skip empty string
        if spec.endswith(e):
            return spec[: -len(e)]
    return spec


def _build_py_map(root: Path, exact_groups: list[dict]) -> dict[str, str]:
    py_map: dict[str, str] = {}
    for item in exact_groups:
        if item.get("language") != "py":
            continue
        canonical = Path(item["canonical"]).resolve()
        redundant_list = [Path(p).resolve() for p in item.get("redundant", [])]
        canon_mod = python_module_from_path(root, canonical)
        for r in redundant_list:
            try:
                r_mod = python_module_from_path(root, r)
                if r_mod and canon_mod and r_mod != canon_mod:
                    py_map[r_mod] = canon_mod
            except Exception:
                # Skip paths that cannot be converted to modules
                continue
    return py_map


def _build_ts_map(exact_groups: list[dict]) -> dict[str, str]:
    ts_map: dict[str, str] = {}
    for item in exact_groups:
        if item.get("language") not in {"ts", "js"}:
            continue
        canonical = Path(item["canonical"]).resolve()
        redundant_list = [Path(p).resolve() for p in item.get("redundant", [])]
        canon_noext = canonical.with_suffix("")
        for r in redundant_list:
            r_noext = r.with_suffix("")
            ts_map[r_noext.as_posix()] = canon_noext.as_posix()
    return ts_map


def build_mappings(root: Path, plan: dict) -> tuple[dict[str, str], dict[str, str]]:
    """Return (py_map, ts_map). Keys are what to replace, values are canonical targets.
    - py_map: module path string (e.g., 'apps.backend.core.x') -> 'apps.backend.core.y'
    - ts_map: file path posix (e.g., 'apps/desktop/src/a') -> 'apps/desktop/src/b' (no extension)
    """
    exact = plan.get("exact_groups", [])
    return _build_py_map(root, exact), _build_ts_map(exact)


def update_python_imports(text: str, py_map: dict[str, str]) -> tuple[str, int]:
    count = 0
    for src_mod, dst_mod in py_map.items():
        # replace in 'import x' and 'from x import'
        patterns = [
            (re.compile(rf"(^|\n)\s*import\s+{re.escape(src_mod)}(\s|$|,)"), rf"\1import {dst_mod}\2"),
            (re.compile(rf"(^|\n)\s*from\s+{re.escape(src_mod)}\s+import\s"), rf"\1from {dst_mod} import "),
        ]
        for pat, rep in patterns:
            new_text, n = pat.subn(rep, text)
            if n:
                count += n
                text = new_text
    return text, count


def update_ts_imports(file_path: Path, text: str, ts_map: dict[str, str]) -> tuple[str, int]:
    count = 0

    def find_canonical(target: Path) -> Path | None:
        key = target.as_posix()
        for ext in TS_EXTS:
            k = (target.with_suffix(ext)).as_posix() if ext else key
            if k in ts_map:
                return Path(ts_map[k])
        return None

    def compute_new_spec(abs_from: Path, spec: str) -> str | None:
        if not spec.startswith("."):
            return None
        target = (abs_from.parent / spec).resolve()
        new_abs = find_canonical(target)
        if new_abs is None:
            return None
        rel = Path(".") / new_abs.relative_to(abs_from.parent)
        return _strip_known_ts_ext(rel.as_posix())

    def repl(m: re.Match) -> str:
        nonlocal count
        spec = m.group(2)
        abs_from = file_path.resolve()
        new_spec = compute_new_spec(abs_from, spec)
        if new_spec is None:
            return m.group(0)
        count += 1
        return m.group(0).replace(spec, new_spec)

    pattern = re.compile(r"(['\"])([^'\"]+)(\1)")
    return pattern.sub(repl, text), count


def main() -> int:
    ap = argparse.ArgumentParser(description="Update references based on consolidation plan")
    ap.add_argument("--plan", type=str, default="reports/consolidation_plan/plan.json", help="Path to plan.json")
    ap.add_argument("--root", type=str, default=".", help="Repository root")
    ap.add_argument(
        "--report-dir", type=str, default="reports/reference_updates", help="Where to write change logs (JSON)"
    )
    ap.add_argument(
        "--exclude-dirs",
        type=str,
        default=",".join(sorted(EXCLUDE_DIRS_DEFAULT)),
        help="Comma-separated folders to exclude",
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview changes only")
    mode.add_argument("--apply", action="store_true", help="Apply file edits")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    plan = load_plan(Path(args.plan))
    py_map, ts_map = build_mappings(root, plan)

    exclude_dirs = {e.strip() for e in args.exclude_dirs.split(",") if e.strip()}
    files = gather_files(root, exclude_dirs=exclude_dirs)
    changes: dict[str, int] = {}

    for fp in files:
        text = fp.read_text(encoding="utf-8", errors="ignore")
        new_text = text
        cnt = 0
        if fp.suffix.lower() == ".py":
            new_text, n1 = update_python_imports(new_text, py_map)
            cnt += n1
        elif fp.suffix.lower() in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
            new_text, n2 = update_ts_imports(fp, new_text, ts_map)
            cnt += n2
        if cnt > 0:
            changes[str(fp)] = cnt
            if args.apply:
                fp.write_text(new_text, encoding="utf-8")

    print("Reference update summary:")
    for k, v in sorted(changes.items()):
        print(f"  {k}: {v} replacements")
    if not changes:
        print("  No changes.")

    if not args.apply:
        print("(dry-run) Re-run with --apply to modify files.")

    # Write a machine-readable log of changes
    try:
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(args.report_dir) / stamp
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "changes.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Changes log: {out_dir / 'changes.json'}")
    except Exception as e:
        print(f"Warning: failed to write changes log: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
