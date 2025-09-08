#!/usr/bin/env python3
"""Apply refactor plan manifest: move/merge/delete/create with git and import fixups.

Usage:
  python scripts/apply_refactor_plan.py --plan tools/refactor/refactor_plan.yaml --dry-run

Notes:
- Requires git in PATH; runs `git mv` for moves when possible to preserve history.
- Updates Python imports for moved files (best-effort): rewrites occurrences of old module paths to new ones.
- Supports globbing for `from` using pathlib.rglob semantics when `from` points to a directory or glob pattern.
- This is conservative: it won't attempt AST merges; for `merge`, it will append a file's content into `into` with
  separators and a header marker.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import Exception
import ValueError
import act
import action
import actions
import any
import argv
import bool
import c
import ch
import cmd
import cwd
import d
import dict
import dry
import e
import fh
import int
import isinstance
import len
import list
import m
import merge
import mv
import p
import pat
import path
import print
import raw
import results
import rewrite_rules
import rewritten
import rule
import rules
import s
import set
import sorted
import str
import tuple
import x

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    print("PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]

IMPORT_RE = re.compile(r"\bfrom\s+([\w.]+)\s+import\b|\bimport\s+([\w.]+)")


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd or ROOT, text=True, capture_output=True, shell=False, check=False)


@dataclass
class Action:
    op: str
    src: str | None
    dst: str | None
    into: str | None
    content: str | None
    note: str | None


def load_plan(path: Path) -> tuple[list[Action], list[tuple[str, str]], dict[str, Any]]:
    """Load plan manifest.

    Supports two schemas:
    - Legacy: { version: 1, actions: [ { op, from, to, into, content } ] }
    - Extended: { version: 1, moves, merges, deletes, creates, rewrite_rules, safety }

    Returns:
        actions: flattened list of executable actions for move/delete/create/merge
        rewrite_rules: list of (find, replace) pairs to apply as regex substitutions
        safety: dict with optional blocklist_dirs and allow_extensions
    """
    data = yaml.safe_load(path.read_text()) or {}
    actions: list[Action] = []
    rewrite_rules: list[tuple[str, str]] = []
    safety: dict[str, Any] = {}

    legacy_actions = data.get("actions", []) or []
    if legacy_actions:
        for raw in legacy_actions:
            actions.append(
                Action(
                    op=str(raw.get("op", "")).strip(),
                    src=raw.get("from"),
                    dst=raw.get("to"),
                    into=raw.get("into"),
                    content=raw.get("content"),
                    note=raw.get("note"),
                )
            )
    else:
        # Extended schema parsing
        for mv in data.get("moves", []) or []:
            actions.append(
                Action(
                    op="move",
                    src=mv.get("src") or mv.get("from"),
                    dst=mv.get("dst") or mv.get("to"),
                    into=None,
                    content=None,
                    note=mv.get("note"),
                )
            )
        for merge in data.get("merges", []) or []:
            dst = merge.get("dst") or merge.get("to") or merge.get("into")
            srcs = merge.get("srcs") or []
            # Only append strategy supported; other strategies can be added later
            for s in srcs:
                actions.append(Action(op="merge", src=s, dst=None, into=dst, content=None, note=None))
        for d in data.get("deletes", []) or []:
            actions.append(Action(op="delete", src=d, dst=None, into=None, content=None, note=None))
        for c in data.get("creates", []) or []:
            actions.append(
                Action(
                    op="create",
                    src=None,
                    dst=c.get("path") or c.get("to"),
                    into=None,
                    content=c.get("content", ""),
                    note=None,
                )
            )
        for rule in data.get("rewrite_rules", []) or []:
            find = rule.get("find")
            repl = rule.get("replace")
            if isinstance(find, str) and isinstance(repl, str):
                rewrite_rules.append((find, repl))
        safety = data.get("safety", {}) or {}

    return actions, rewrite_rules, safety


def git_mv(src: Path, dst: Path, dry: bool) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry:
        print(f"DRY git mv {src} -> {dst}")
        return
    # Prefer git mv when inside a git repo, using repo-relative paths; fallback to shutil.move
    try:
        in_git = run(["git", "rev-parse", "--is-inside-work-tree"]).returncode == 0
    except Exception:
        in_git = False
    if in_git:
        rel_src = str(src.relative_to(ROOT)) if src.is_absolute() else str(src)
        rel_dst = str(dst.relative_to(ROOT)) if dst.is_absolute() else str(dst)
        res = run(["git", "mv", rel_src, rel_dst])
        if res.returncode == 0:
            return
        # Fall through to shutil if git mv fails
    shutil.move(str(src), str(dst))


def apply_move(action: Action, dry: bool, rewritten: list[tuple[str, str]]) -> list[tuple[str, str]]:
    assert action.src and action.dst
    src_path = ROOT / action.src
    # Glob support
    if any(ch in action.src for ch in "*?[]"):
        matches = [Path(p) for p in fnmatch.filter([str(p.relative_to(ROOT)) for p in ROOT.rglob("*")], action.src)]
    else:
        matches = [src_path] if src_path.exists() else []
    for m in matches:
        old = str(m.relative_to(ROOT)).replace(os.sep, "/")
        dst_path = ROOT / (action.dst if not action.dst.endswith("/") else (action.dst + m.name))
        new = str(dst_path.relative_to(ROOT)).replace(os.sep, "/")
        print(f"MOVE {old} -> {new}")
        git_mv(m, dst_path, dry)
        # Track import rewrite mapping (module path form)
        old_mod = old[:-3].replace("/", ".") if old.endswith(".py") else old.replace("/", ".")
        new_mod = new[:-3].replace("/", ".") if new.endswith(".py") else new.replace("/", ".")
        rewritten.append((old_mod, new_mod))
    return rewritten


def apply_delete(action: Action, dry: bool) -> None:
    assert action.src
    target = ROOT / action.src
    # Glob delete
    if any(ch in action.src for ch in "*?[]"):
        paths = [Path(p) for p in fnmatch.filter([str(p.relative_to(ROOT)) for p in ROOT.rglob("*")], action.src)]
    else:
        paths = [target] if target.exists() else []
    for p in paths:
        print(f"DELETE {p.relative_to(ROOT)}")
        if dry:
            continue
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        else:
            try:
                run(["git", "rm", "-f", str(p)])
            except Exception:
                p.unlink(missing_ok=True)


def apply_create(action: Action, dry: bool) -> None:
    assert action.dst is not None
    dst = ROOT / action.dst
    print(f"CREATE {dst.relative_to(ROOT)}")
    if dry:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    content = action.content or ""
    dst.write_text(content, encoding="utf-8")


def apply_merge(action: Action, dry: bool) -> None:
    assert action.src and action.into
    src = ROOT / action.src
    into = ROOT / action.into
    if not src.exists():
        print(f"SKIP MERGE (source missing): {action.src}")
        return
    print(f"MERGE {src.relative_to(ROOT)} -> {into.relative_to(ROOT)}")
    if dry:
        return
    into.parent.mkdir(parents=True, exist_ok=True)
    src_txt = src.read_text(encoding="utf-8")
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    sep = f"\n\n# ==== MERGED FROM: {action.src} at {ts} ====\n\n"
    with Path(into).open("a", encoding="utf-8") as fh:
        fh.write(sep)
        fh.write(src_txt)


def _iter_files(allow_exts: list[str] | None = None, blocklist_dirs: list[str] | None = None) -> list[Path]:
    allow_exts = allow_exts or [".py"]
    blocked = {d.strip("/") for d in (blocklist_dirs or [])}
    results: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in allow_exts:
            continue
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue
        parts = set(str(rel).replace("\\", "/").split("/"))
        if parts & blocked:
            continue
        results.append(path)
    return results


def rewrite_imports(mappings: list[tuple[str, str]], dry: bool, blocklist_dirs: list[str] | None = None) -> None:
    if not mappings:
        return
    # Build regex map patterns to avoid partial replacements
    compiled = [(re.compile(rf"\b{re.escape(old)}\b"), new) for old, new in sorted(mappings, key=lambda x: -len(x[0]))]
    py_files = _iter_files([".py"], blocklist_dirs)
    for path in py_files:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        orig = txt
        for pat, new in compiled:
            # Replace in both import forms and general occurrences of module path
            txt = re.sub(rf"(from\s+){pat.pattern}(\s+import)", rf"\1{new}\2", txt)
            txt = re.sub(rf"(import\s+){pat.pattern}(\b)", rf"\1{new}\2", txt)
            txt = pat.sub(new, txt)
        if txt != orig:
            print(f"REWRITE imports in {path.relative_to(ROOT)}")
            if not dry:
                path.write_text(txt, encoding="utf-8")


def apply_rewrite_rules(
    rules: list[tuple[str, str]],
    dry: bool,
    allow_exts: list[str],
    blocklist_dirs: list[str],
) -> None:
    if not rules:
        return
    compiled = [(re.compile(find), repl) for find, repl in rules]
    files = _iter_files(allow_exts, blocklist_dirs)
    for path in files:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        orig = txt
        for pat, repl in compiled:
            txt = pat.sub(repl, txt)
        if txt != orig:
            print(f"REWRITE rules in {path.relative_to(ROOT)}")
            if not dry:
                path.write_text(txt, encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Apply refactor plan manifest")
    ap.add_argument("--plan", default=str(ROOT / "tools/refactor/refactor_plan.yaml"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path
    if not plan_path.exists():
        print(f"Plan not found: {plan_path}", file=sys.stderr)
        return 2

    actions, rewrite_rules, safety = load_plan(plan_path)
    if not actions and not rewrite_rules:
        print("No actions in plan; nothing to do.")
        return 0

    mappings: list[tuple[str, str]] = []
    for act in actions:
        if act.op == "move":
            mappings = apply_move(act, args.dry_run, mappings)
        elif act.op == "delete":
            apply_delete(act, args.dry_run)
        elif act.op == "create":
            apply_create(act, args.dry_run)
        elif act.op == "merge":
            apply_merge(act, args.dry_run)
        else:
            print(f"Unknown op: {act.op}", file=sys.stderr)

    # Rewrite imports after moves (module path changes)
    blocklist_dirs = [str(d) for d in (safety.get("blocklist_dirs") or [])]
    rewrite_imports(mappings, args.dry_run, blocklist_dirs)

    # Apply explicit rewrite rules (regex literal)
    allow_exts = [str(e) for e in (safety.get("allow_extensions") or [".py", ".md", ".yaml", ".yml"])]
    apply_rewrite_rules(rewrite_rules, args.dry_run, allow_exts, blocklist_dirs)

    if not args.dry_run:
        run(["git", "add", "-A"])  # stage changes
    print("\nDONE. Next:\n  - ruff check .\n  - pytest -q\n  - fix any broken imports (should be minimal)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
