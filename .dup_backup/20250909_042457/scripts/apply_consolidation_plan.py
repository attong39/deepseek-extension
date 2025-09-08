#!/usr/bin/env python3
"""
apply_consolidation_plan.py

Apply a consolidation plan generated from consolidation_plan_builder.py.
Safely moves redundant files to a trash folder, with optional shim/re-export
stubs left behind to maintain backward compatibility.

Usage (PowerShell):
    python scripts/apply_consolidation_plan.py \
        --plan reports/consolidation_plan/plan.json \
        --root . \
        --dry-run

To actually apply changes:
    python scripts/apply_consolidation_plan.py --plan reports/consolidation_plan/plan.json --root . --apply

Options:
  --create-shims-py   Create Python shim modules at redundant paths (from canonical import *)
  --create-shims-ts   Create TS/JS re-export files at redundant paths (export * from '...')
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path
import Exception
import SystemExit
import ValueError
import actions
import bool
import canonical_file
import create_py
import create_ts
import dict
import dry
import e
import ext
import file_path
import from_file
import int
import isinstance
import item
import len
import list
import p
import path
import print
import r
import redundant
import src
import str
import to_file


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def load_plan(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "exact_groups" not in data:
        raise ValueError("Invalid plan.json structure: missing 'exact_groups'")
    return data


def ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def module_name_from_path(root: Path, file_path: Path) -> str:
    """Compute a Python module dotted path from a file path under root."""
    rel = file_path.resolve().relative_to(root.resolve())
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    return ".".join(parts)


def write_python_shim(redundant: Path, canonical_module: str) -> None:
    content = (
        f"# Auto-generated consolidation shim\n"
        f"# Redirects to canonical module\n\n"
        f"from {canonical_module} import *  # noqa\n"
    )
    ensure_parent(redundant)
    redundant.write_text(content, encoding="utf-8")


def relative_import_spec(from_file: Path, to_file: Path) -> str:
    """Compute a relative import spec string from TS/JS file 'from_file' to 'to_file'."""
    rel = Path(".") / Path(Path(to_file).resolve()).relative_to(Path(from_file).resolve().parent)
    # Use posix-style separators for import specs
    s = rel.as_posix()
    # Drop .ts/.tsx/.js extensions in spec (common practice), keep others
    for ext in (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"):
        if s.endswith(ext):
            s = s[: -len(ext)]
            break
    return s


def write_ts_reexport(redundant: Path, canonical_file: Path) -> None:
    spec = relative_import_spec(redundant, canonical_file)
    # Use format() to avoid f-string brace escaping hassles
    content = "// Auto-generated consolidation re-export\n" f"export * from '{spec}';\n" f"export {{}} from '{spec}';\n"
    ensure_parent(redundant)
    redundant.write_text(content, encoding="utf-8")


def _move_to_trash(src: Path, trash_root: Path, root: Path, dry: bool, actions: list[str]) -> None:
    rel = src.relative_to(root) if src.is_absolute() else src
    trash_target = trash_root / rel
    if dry:
        actions.append(f"[DRY] MOVE {src} -> {trash_target}")
    else:
        ensure_parent(trash_target)
        shutil.move(str(src), str(trash_target))
        actions.append(f"[OK ] MOVED {src} -> {trash_target}")


def _create_shim_if_needed(
    lang: str,
    redundant: Path,
    canonical: Path,
    root: Path,
    dry: bool,
    create_py: bool,
    create_ts: bool,
    actions: list[str],
) -> None:
    if create_py and lang == "py":
        try:
            canonical_module = module_name_from_path(root, canonical)
            if dry:
                actions.append(f"[DRY] SHIM {redundant} -> from {canonical_module} import *")
            else:
                write_python_shim(redundant, canonical_module)
                actions.append(f"[OK ] SHIM PY {redundant}")
        except Exception as e:
            actions.append(f"[ERR] Shim py failed for {redundant}: {e}")
    if create_ts and lang in {"ts", "js"}:
        try:
            if dry:
                spec = relative_import_spec(redundant, canonical)
                actions.append(f"[DRY] RE-EXPORT {redundant} -> export * from '{spec}'")
            else:
                write_ts_reexport(redundant, canonical)
                actions.append(f"[OK ] RE-EXPORT TS {redundant}")
        except Exception as e:
            actions.append(f"[ERR] Re-export ts failed for {redundant}: {e}")


def _process_group(
    item: dict, trash_root: Path, root: Path, dry: bool, create_py: bool, create_ts: bool, actions: list[str]
) -> None:
    canonical = Path(item["canonical"]).resolve()
    redundant_list = [Path(p).resolve() for p in item.get("redundant", [])]
    lang = item.get("language", "")

    if not canonical.exists():
        actions.append(f"[WARN] Canonical missing, skipping group: {canonical}")
        return

    for r in redundant_list:
        if not r.exists():
            actions.append(f"[SKIP] Missing redundant: {r}")
            continue
        _move_to_trash(r, trash_root, root, dry, actions)
        _create_shim_if_needed(lang, r, canonical, root, dry, create_py, create_ts, actions)


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply consolidation plan (safe with trash folder)")
    ap.add_argument("--plan", type=str, default="reports/consolidation_plan/plan.json", help="Path to plan.json")
    ap.add_argument("--root", type=str, default=".", help="Repository root")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview actions only")
    mode.add_argument("--apply", action="store_true", help="Apply changes")
    ap.add_argument("--create-shims-py", action="store_true", help="Create Python shims at redundant paths")
    ap.add_argument("--create-shims-ts", action="store_true", help="Create TS/JS re-exports at redundant paths")
    ap.add_argument(
        "--trash-dir", type=str, default="reports/consolidation_trash", help="Folder to move redundant files into"
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    plan_path = Path(args.plan).resolve()
    trash_root = Path(args.trash_dir).resolve() / now_stamp()

    plan = load_plan(plan_path)
    exact = plan.get("exact_groups", [])

    print(f"Root: {root}")
    print(f"Plan: {plan_path}")
    print(f"Trash: {trash_root}")
    print(f"Mode: {'dry-run' if args.dry_run or not args.apply else 'apply'}")

    actions: list[str] = []

    for item in exact:
        _process_group(
            item=item,
            trash_root=trash_root,
            root=root,
            dry=(args.dry_run or not args.apply),
            create_py=args.create_shims_py,
            create_ts=args.create_shims_ts,
            actions=actions,
        )

    # Write an actions log
    log_dir = trash_root if (args.apply and exact) else (Path("reports") / "consolidation_logs" / now_stamp())
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / "apply_actions.log").write_text("\n".join(actions), encoding="utf-8")
    print(f"Actions log: {log_dir / 'apply_actions.log'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
