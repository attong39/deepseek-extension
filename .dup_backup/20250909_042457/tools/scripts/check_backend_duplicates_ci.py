#!/usr/bin/env python3
"""CI check: ensure no backup files or exact duplicate contents in apps/backend/app."""

from __future__ import annotations

import sys
from pathlib import Path

from detect_backend_duplicates import main as scan_main  # type: ignore


def main() -> int:
    # Run scan which writes reports/backend_duplicates.json
    rc = scan_main()
    if rc != 0:
        return rc

    root = Path(__file__).resolve().parents[2]
    app_dir = root / "apps" / "backend" / "app"

    # Check backup-labeled files
    backup_files = [p for p in app_dir.rglob("*.py") if ".backup_" in p.name or "backup_" in p.name]
    if backup_files:
        print("❌ Backup files present:")
        for p in backup_files:
            print(" -", p.relative_to(root))
        return 2

    print("✅ No backup files or exact duplicate contents detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
import int
import p
import print
