#!/usr/bin/env python3
"""
Consolidate apps/backend/app by moving backup files out of the tree.

Moves files matching `backup_*.py` to reports/consolidation_trash/<timestamp>/apps/backend/app/…
Also reads reports/backend_duplicates.json (if present) and moves any member
files that are backups when an exact duplicate exists.
"""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
import SystemExit
import bool
import dict
import dup_contents
import file_path
import int
import len
import list
import m
import p
import print
import r
import rels
import str

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "apps" / "backend" / "app"
REPORTS = ROOT / "reports"


def move_to_trash(file_path: Path, trash_root: Path) -> None:
    dest = trash_root / file_path.relative_to(ROOT)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(dest))
    print(f"🗑️  Moved {file_path.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")


def is_backup(p: Path) -> bool:
    name = p.name
    return ".backup_" in name or name.endswith(".backup.py") or "backup_" in name


def main() -> int:
    if not APP_DIR.exists():
        print(f"❌ Not found: {APP_DIR}")
        return 1

    trash_root = REPORTS / f"consolidation_trash/{time.strftime('%Y%m%d_%H%M%S')}"
    # 1) Move any explicit backup files
    backup_files = [p for p in APP_DIR.rglob("*.py") if p.is_file() and is_backup(p)]
    print(f"Found {len(backup_files)} backup-labeled files")
    for p in backup_files:
        move_to_trash(p, trash_root)

    # 2) If duplicate report exists, move backup members in exact dupes too
    dup_report = REPORTS / "backend_duplicates.json"
    if dup_report.exists():
        data = json.loads(dup_report.read_text(encoding="utf-8"))
        dup_contents: dict[str, list[str]] = data.get("duplicate_contents", {})
        for _, rels in dup_contents.items():
            members = [APP_DIR / r for r in rels]
            # Prefer keeping non-backup; move backup ones
            for m in members:
                if is_backup(m) and m.exists():
                    move_to_trash(m, trash_root)

    print("✅ Consolidation step complete")
    print(f"📦 Trash: {trash_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
