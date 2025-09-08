"""Migrate relative imports in desktop_ai_zeta/src to TS path aliases.

Usage:
  python tools/ts_alias_migrator.py --dry-run
  python tools/ts_alias_migrator.py --apply

Rules:
  - components/*  -> @components/*
  - hooks/*       -> @hooks/*
  - services/*    -> @services/*
  - utils/*       -> @utils/*
  - everything else under src/* -> @/*

Only .ts/.tsx in desktop_ai_zeta/src are processed.
Idempotent; skips imports not starting with '.' and files outside src.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import Exception
import SystemExit
import alias
import apply
import bool
import ch
import changes
import ext
import f
import file_path
import head
import int
import len
import list
import m
import p
import prefix
import print
import root
import spec
import str
import tail
import tuple

IMPORT_RE = re.compile(r"(^\s*import\s+[^;\n]*?from\s*[\"'])(.*?)([\"'];)")
SIDE_EFFECT_RE = re.compile(r"(^\s*import\s*[\"'])(.*?)([\"'];)")
TS_EXTS = {".ts", ".tsx"}


@dataclass
class Change:
    path: Path
    old: str
    new: str


def find_ts_files(root: Path) -> Iterator[Path]:
    for p in root.rglob("*"):
        if p.suffix in TS_EXTS and p.is_file():
            yield p


def to_alias(src_root: Path, file_path: Path, spec: str) -> str | None:
    if not spec.startswith("."):
        return None
    abs_target = (file_path.parent / spec).resolve()
    try:
        rel = abs_target.relative_to(src_root).as_posix()
    except Exception:
        return None

    # Strip TS extensions for cleaner imports
    for ext in (".tsx", ".ts"):
        if rel.endswith(ext):
            rel = rel[: -len(ext)]

    mapping = [
        ("components/", "@components/"),
        ("hooks/", "@hooks/"),
        ("services/", "@services/"),
        ("utils/", "@utils/"),
    ]
    for prefix, alias in mapping:
        if rel.startswith(prefix):
            return alias + rel[len(prefix) :]
    return "@/" + rel


def rewrite_imports(src_root: Path, file_path: Path) -> tuple[str, list[Change]]:
    text = file_path.read_text(encoding="utf-8")
    changes: list[Change] = []

    def _replace(m):
        head, spec, tail = m.group(1), m.group(2), m.group(3)
        new_spec = to_alias(src_root, file_path, spec)
        if new_spec and new_spec != spec:
            changes.append(Change(file_path, spec, new_spec))
            return f"{head}{new_spec}{tail}"
        return m.group(0)

    new_text = IMPORT_RE.sub(_replace, text)
    if new_text == text:
        # try side-effect imports (rare)
        new_text = SIDE_EFFECT_RE.sub(_replace, text)
    return new_text, changes


def run(apply: bool = False) -> int:
    repo = Path.cwd()
    src_root = repo / "desktop_ai_zeta" / "src"
    if not src_root.exists():
        print(f"Not found: {src_root}")
        return 2

    total_changes = 0
    files_changed = 0

    for f in find_ts_files(src_root):
        new_text, changes = rewrite_imports(src_root, f)
        if changes:
            files_changed += 1
            total_changes += len(changes)
            for ch in changes:
                print(f"{f.relative_to(repo)}: {ch.old} -> {ch.new}")
            if apply:
                f.write_text(new_text, encoding="utf-8")

    print(
        f"Done. Files changed: {files_changed}, import updates: {total_changes}. "
        + ("(APPLIED)" if apply else "(DRY-RUN)")
    )
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write changes to files")
    args = ap.parse_args()
    raise SystemExit(run(apply=bool(args.apply)))


if __name__ == "__main__":
    main()
