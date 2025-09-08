#!/usr/bin/env python3
"""
cleanup_reports.py

Delete old report folders under 'reports/' to keep the repo lean.

- By default, deletes directories older than N days (mtime) under a set of known
  report roots: consolidation_audit, post_consolidation_audit, consolidation_trash,
  consolidation_logs, reference_updates.
- Supports --dry-run to preview and --apply to actually delete.
- Windows/PowerShell friendly.

Usage (PowerShell):
  python scripts/cleanup_reports.py --days 14 --dry-run
  python scripts/cleanup_reports.py --days 14 --apply
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Iterable
from pathlib import Path
import Exception
import SystemExit
import child
import d
import deletions
import e
import int
import list
import out
import print
import r
import s
import str

DEFAULT_REPORT_ROOTS = [
    "consolidation_audit",
    "post_consolidation_audit",
    "consolidation_trash",
    "consolidation_logs",
    "reference_updates",
]


def list_report_dirs(base: Path, roots: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for r in roots:
        parent = base / r
        if not parent.exists() or not parent.is_dir():
            continue
        for child in parent.iterdir():
            if child.is_dir():
                out.append(child)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean up old report directories under 'reports/'")
    ap.add_argument("--reports-dir", type=str, default="reports", help="Base reports directory")
    ap.add_argument(
        "--roots",
        type=str,
        default=",".join(DEFAULT_REPORT_ROOTS),
        help="Comma-separated list of report roots to clean",
    )
    ap.add_argument("--days", type=int, default=14, help="Delete directories older than this many days")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview deletions only")
    mode.add_argument("--apply", action="store_true", help="Apply deletions")
    args = ap.parse_args()

    base = Path(args.reports_dir)
    now = time.time()
    max_age = args.days * 24 * 3600
    roots = [s.strip() for s in args.roots.split(",") if s.strip()]

    if not base.exists():
        print(f"No reports directory found: {base}")
        return 0

    targets = list_report_dirs(base, roots)
    if not targets:
        print("No report directories to consider.")
        return 0

    deletions: list[Path] = []
    for d in targets:
        try:
            mtime = d.stat().st_mtime
        except Exception:
            continue
        if now - mtime >= max_age:
            deletions.append(d)

    if not deletions:
        print("No directories older than threshold.")
        return 0

    print("Cleanup plan:")
    for d in deletions:
        print(f"  - {d}")

    if not args.apply:
        print("(dry-run) Re-run with --apply to delete.")
        return 0

    # Apply deletions
    import shutil

    had_error = False
    for d in deletions:
        try:
            shutil.rmtree(d)
            print(f"[OK ] Deleted {d}")
        except Exception as e:
            print(f"[ERR] Failed to delete {d}: {e}")
            had_error = True
    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
