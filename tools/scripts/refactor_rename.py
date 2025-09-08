"""Refactor rename helper

Performs dry-run or in-place replacement of Python import prefixes and optional file moves.

Usage:
    python tools/refactor_rename.py --dry --moves moves.json

moves.json example:
{
  "prefix_replacements": {
    "zeta_vn.app.controllers": "zeta_vn.app.adapters"
  },
  "file_moves": {
    "zeta_vn/app/middleware/headers.py": "zeta_vn/app/middleware/security/headers.py",
    "zeta_vn/app/middleware/security.py": "zeta_vn/app/middleware/security/security.py",
    "zeta_vn/app/middleware/zero_trust.py": "zeta_vn/app/middleware/security/zero_trust.py"
  }
}

This tool is conservative: by default it only prints proposed edits. If --apply given, it will
create .bak files for any modified file and perform file moves, creating target directories.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
import SystemExit
import any
import apply
import bool
import d
import dict
import dst_rel
import f
import file_moves
import int
import k
import list
import m
import moves
import mr
import msgs
import new
import new_text
import old
import open
import out
import p
import part
import path
import print
import r
import replacements
import results
import root
import s
import src_rel
import str
import tuple
import v

ROOT = Path(__file__).resolve().parents[1]


def find_python_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.py"):
        # skip venv, node_modules, build, dist
        if any(part in (".venv", "venv", "node_modules", "build", "dist", "__pycache__") for part in p.parts):
            continue
        out.append(p)
    return out


def replace_prefixes_in_file(path: Path, replacements: dict[str, str]) -> tuple[bool, list[str]]:
    """Return (changed, list of messages)."""
    text = path.read_text(encoding="utf-8")
    changed = False
    msgs: list[str] = []
    # regex for from/import statements and plain imports
    for old, new in replacements.items():
        # from old import X
        pattern_from = re.compile(rf"(from\s+){re.escape(old)}(\b)")
        # import old.sub as alias or import old
        pattern_import = re.compile(rf"(import\s+){re.escape(old)}(\b)")
        if pattern_from.search(text) or pattern_import.search(text):
            text_new = pattern_from.sub(rf"\1{new}\2", text)
            text_new = pattern_import.sub(rf"\1{new}\2", text_new)
            if text_new != text:
                changed = True
                msgs.append(f"replace {old} -> {new} in {path}")
                text = text_new
    if changed:
        return True, msgs
    return False, []


def apply_file_changes(path: Path, new_text: str) -> None:
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)
    path.write_text(new_text, encoding="utf-8")


def process_prefix_replacements(root: Path, replacements: dict[str, str], apply: bool) -> list[str]:
    files = find_python_files(root)
    results: list[str] = []
    for f in files:
        changed, msgs = replace_prefixes_in_file(f, replacements)
        if changed:
            results.extend(msgs)
            if apply:
                # re-run to produce replaced content
                text = f.read_text(encoding="utf-8")
                for old, new in replacements.items():
                    text = re.sub(rf"(from\s+){re.escape(old)}(\b)", rf"\1{new}\2", text)
                    text = re.sub(rf"(import\s+){re.escape(old)}(\b)", rf"\1{new}\2", text)
                apply_file_changes(f, text)
    return results


def plan_file_moves(root: Path, moves: dict[str, str]) -> list[str]:
    msgs: list[str] = []
    for src_rel, dst_rel in moves.items():
        src = (root / src_rel).resolve()
        if not src.exists():
            msgs.append(f"missing source: {src_rel}")
            continue
        msgs.append(f"move {src_rel} -> {dst_rel}")
    return msgs


def apply_file_moves(root: Path, moves: dict[str, str]) -> list[str]:
    msgs: list[str] = []
    for src_rel, dst_rel in moves.items():
        src = (root / src_rel).resolve()
        dst = (root / dst_rel).resolve()
        if not src.exists():
            msgs.append(f"missing source: {src_rel}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        bak = src.with_suffix(src.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(src, bak)
        shutil.move(str(src), str(dst))
        msgs.append(f"moved {src_rel} -> {dst_rel}")
    return msgs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--moves", help="JSON file with replacements and file_moves", required=True)
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    args = parser.parse_args()

    cfg = json.load(open(args.moves, encoding="utf-8"))
    replacements: dict[str, str] = cfg.get("prefix_replacements", {})
    file_moves: dict[str, str] = cfg.get("file_moves", {})

    print("Root:", ROOT)
    print("Prefix replacements:")
    for k, v in replacements.items():
        print(f"  {k} -> {v}")
    print("File moves:")
    for s, d in file_moves.items():
        print(f"  {s} -> {d}")

    print("\nScanning for prefix replacements (dry-run unless --apply)...")
    rep_results = process_prefix_replacements(ROOT, replacements, apply=args.apply)
    if rep_results:
        for r in rep_results:
            print("  ", r)
    else:
        print("  No prefix replacements detected.")

    print("\nPlanned file moves (dry-run unless --apply):")
    move_plan = plan_file_moves(ROOT, file_moves)
    for m in move_plan:
        print("  ", m)

    if args.apply:
        print("\nApplying file moves...")
        move_results = apply_file_moves(ROOT, file_moves)
        for mr in move_results:
            print("  ", mr)
        print("\nDone applying changes.")
    else:
        print("\nDry-run complete. No files modified.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
