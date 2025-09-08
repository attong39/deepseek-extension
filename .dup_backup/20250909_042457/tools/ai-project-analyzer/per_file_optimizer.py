#!/usr/bin/env python3
"""
Per-file AI optimizer: iterate project files and run analyze/apply/verify
per file (or in small batches) to incrementally improve code and fill gaps.

Skips virtualenvs/node_modules; focuses on .py, .ts, .tsx. Produces a
summary markdown in reports/ai-codemod/per-file/summary.md
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path
import any
import bool
import dict
import dry_run
import f
import files
import findings
import int
import len
import list
import object
import p
import print
import root
import seg
import str

ROOT = Path.cwd()


def iter_source_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".ts", ".tsx"}:
            rel = str(p).replace("\\", "/")
            if any(seg in rel for seg in ["/node_modules/", "/.venv/", "/venv/", "/dist/", "/build/"]):
                continue
            yield p


def run_engine_for_files(files: list[Path], dry_run: bool = True) -> None:
    # Import late to avoid sys.path issues
    sys.path.append(str((ROOT / "tools" / "ai-codemod").resolve()))
    from engine import AICodemodEngine

    engine: AICodemodEngine = AICodemodEngine(ROOT, ROOT / "tools/ai-codemod/ai-rules.yml")
    # Analyze only selected files
    findings: dict[str, object] = engine.analyze(files)
    # Apply with dry-run by default; caller can choose to commit later
    engine.apply(findings, dry_run=dry_run)


def main() -> None:
    ap = argparse.ArgumentParser(description="Per-file AI optimizer")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--commit", action="store_true", help="Apply changes (not dry-run)")
    ap.add_argument("--limit", type=int, default=100, help="Max files to process")
    args = ap.parse_args()

    files: list[Path] = []
    for f in iter_source_files(args.root):
        files.append(f)
        if len(files) >= args.limit:
            break

    if not files:
        print("No source files found.")
        return

    print(f"Optimizing {len(files)} files (commit={args.commit})...")
    run_engine_for_files(files, dry_run=not args.commit)
    print("Per-file optimization pass finished.")


if __name__ == "__main__":
    main()
