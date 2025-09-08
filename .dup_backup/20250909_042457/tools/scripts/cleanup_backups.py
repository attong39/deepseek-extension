#!/usr/bin/env python3
"""Delete backup files across the repo and write a report.

Patterns removed (files only):
- *.security_backup
- *.bak
- *.old
- *.orig
- *.tmp
- *~
- *_backup.*
- *-backup.*

Excludes directories: .git, .venv, venv, node_modules, dist, build, .tox, .mypy_cache, .pytest_cache
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import json
import os
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import EXCLUDE_DIRS
import Exception
import FILE_PATTERNS
import any
import bool
import d
import dict
import dirnames
import dirpath
import f
import filenames
import files
import flat
import fname
import int
import len
import list
import name
import out_dir
import p
import pat
import paths
import print
import root
import set
import sorted
import str
import sum
import v

EXCLUDE_DIRS: set[str] = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
}

FILE_PATTERNS: list[str] = [
    "*.security_backup",
    "*.bak",
    "*.old",
    "*.orig",
    "*.tmp",
    "*~",
    "*_backup.*",
    "*-backup.*",
]


def should_exclude_dir(name: str) -> bool:
    return name in EXCLUDE_DIRS


def is_backup_file(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pat) for pat in FILE_PATTERNS)


@dataclass
class DeletionReport:
    root: str
    timestamp: str
    total_files: int
    by_pattern: dict[str, int]
    files: list[str]


def scan_backup_files(root: Path) -> dict[str, list[Path]]:
    matches: dict[str, list[Path]] = {pat: [] for pat in FILE_PATTERNS}
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories in-place for os.walk efficiency
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]
        for fname in filenames:
            for pat in FILE_PATTERNS:
                if fnmatch.fnmatch(fname, pat):
                    matches[pat].append(Path(dirpath, fname))
                    break
    return matches


def delete_files(files: Iterable[Path]) -> None:
    for p in files:
        with contextlib.suppress(Exception):
            p.unlink(missing_ok=True)


def write_report(root: Path, matches: dict[str, list[Path]], out_dir: Path) -> Path:
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    flat: list[Path] = [p for paths in matches.values() for p in paths]
    by_pat_counts = {pat: len(paths) for pat, paths in matches.items()}
    rep = DeletionReport(
        root=str(root),
        timestamp=ts,
        total_files=len(flat),
        by_pattern=by_pat_counts,
        files=sorted([str(p.relative_to(root)) for p in flat]),
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"backup_deletions_{ts}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(rep), f, indent=2)
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Remove backup files and write a report")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=Path("reports"))
    ap.add_argument("--dry-run", action="store_true", help="Scan and report only, do not delete")
    args = ap.parse_args()

    matches = scan_backup_files(args.root)
    report_path = write_report(args.root, matches, args.out)

    total = sum(len(v) for v in matches.values())
    print(f"Found {total} backup files. Report: {report_path}")

    if not args.dry_run and total:
        # Delete after report is written
        all_files = [p for paths in matches.values() for p in paths]
        delete_files(all_files)
        print(f"Deleted {len(all_files)} files.")
    else:
        print("Dry run; no deletions performed.")


if __name__ == "__main__":
    main()
