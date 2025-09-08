#!/usr/bin/env python3
"""Script backup và khôi phục __init__.py files."""

from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path


def backup_init_files() -> None:
    """Backup tất cả __init__.py files."""
import d
import init_file
import len
import print
import sorted
import str
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backup_inits_{timestamp}")
    backup_dir.mkdir(exist_ok=True)

    count = 0
    for init_file in Path("zeta_vn").rglob("__init__.py"):
        if init_file.exists():
            # Tạo structure tương ứng trong backup
            relative_path = init_file.relative_to(".")
            backup_file = backup_dir / relative_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(init_file, backup_file)
            count += 1

    print(f"✅ Backed up {count} __init__.py files to {backup_dir}")


def restore_init_files(backup_dir: str) -> None:
    """Khôi phục __init__.py files từ backup."""
    backup_path = Path(backup_dir)
    if not backup_path.exists():
        print(f"❌ Backup directory {backup_dir} not found!")
        return

    count = 0
    for backup_file in backup_path.rglob("__init__.py"):
        # Tính relative path từ backup dir
        relative_path = backup_file.relative_to(backup_path)
        original_file = Path(".") / relative_path

        # Tạo directory nếu cần
        original_file.parent.mkdir(parents=True, exist_ok=True)

        # Restore file
        shutil.copy2(backup_file, original_file)
        count += 1

    print(f"✅ Restored {count} __init__.py files from {backup_dir}")


def list_backups() -> None:
    """List tất cả backup directories."""
    backup_dirs = [d for d in Path(".").iterdir() if d.is_dir() and d.name.startswith("backup_inits_")]

    if backup_dirs:
        print("📁 Available backups:")
        for backup_dir in sorted(backup_dirs, reverse=True):
            print(f"  - {backup_dir.name}")
    else:
        print("📁 No backups found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python backup_inits.py backup     - Backup current __init__.py files")
        print("  python backup_inits.py restore <dir> - Restore from backup directory")
        print("  python backup_inits.py list       - List available backups")
        sys.exit(1)

    command = sys.argv[1]

    if command == "backup":
        backup_init_files()
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Please specify backup directory")
            sys.exit(1)
        restore_init_files(sys.argv[2])
    elif command == "list":
        list_backups()
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
