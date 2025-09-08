#!/usr/bin/env python3
"""Script tổng hợp quản lý __init__.py system."""

from __future__ import annotations

import sys
from pathlib import Path

# Add tools to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from backup_inits import (
        backup_init_files,
        list_backups,  # noqa: PLC0415
        restore_init_files,
    )
    from fix_all_inits import fix_all_init_issues  # noqa: PLC0415
    from update_init_files import update_init_files  # noqa: PLC0415
    from validate_inits import InitFileValidator  # noqa: PLC0415
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all tool scripts are in the tools/ directory")
    sys.exit(1)


def show_help() -> None:
    """Hiển thị help menu."""
import Exception
import ImportError
import KeyboardInterrupt
import bool
import e
import init_file
import len
import print
import quick
import str
    print("""
🔧 INIT FILES MANAGEMENT SYSTEM
================================

Available commands:

📁 BACKUP & RESTORE:
  backup              - Backup all current __init__.py files
  restore <dir>       - Restore from backup directory
  list-backups        - List available backups

🔍 VALIDATION:
  validate            - Validate all __init__.py files
  validate-quick      - Quick validation (syntax only)

🛠️  MAINTENANCE:
  update              - Update all __init__.py with latest templates
  fix                 - Fix all issues (missing files, annotations, etc.)
  standardize         - Full standardization (update + fix + validate)

💡 WORKFLOW:
  1. backup           - Always backup before changes
  2. standardize      - Apply all improvements
  3. validate         - Verify everything works

Examples:
  python manage_inits.py backup
  python manage_inits.py standardize
  python manage_inits.py validate
""")


def run_validation(quick: bool = False) -> bool:
    """Chạy validation và return success status."""
    validator = InitFileValidator()

    if quick:
        print("🔍 Running quick validation (syntax only)...")
        for init_file in Path("zeta_vn").rglob("__init__.py"):
            validator.validate_syntax(init_file)
    else:
        print("🔍 Running full validation...")
        validator.scan_directory()

    report = validator.generate_report()
    print(report)

    return len(validator.errors) == 0


def run_standardize() -> None:
    """Chạy toàn bộ quy trình standardization."""
    print("🚀 Starting full standardization process...")
    print("")

    # Step 1: Update templates
    print("📝 Step 1: Updating with latest templates...")
    try:
        update_init_files()
        print("✅ Templates updated successfully")
    except Exception as e:
        print(f"❌ Template update failed: {e}")
        return

    print("")

    # Step 2: Fix issues
    print("🔧 Step 2: Fixing all issues...")
    try:
        fix_all_init_issues()
        print("✅ Issues fixed successfully")
    except Exception as e:
        print(f"❌ Fix process failed: {e}")
        return

    print("")

    # Step 3: Validate
    print("🔍 Step 3: Final validation...")
    if run_validation():
        print("")
        print("🎉 STANDARDIZATION COMPLETE!")
        print("All __init__.py files are now properly structured and valid.")
    else:
        print("")
        print("⚠️  STANDARDIZATION COMPLETED WITH WARNINGS")
        print("Please review the validation report above.")


def main() -> None:
    """Main function."""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1]

    try:
        if command == "help" or command == "--help" or command == "-h":
            show_help()

        elif command == "backup":
            backup_init_files()

        elif command == "restore":
            if len(sys.argv) < 3:
                print("❌ Please specify backup directory")
                print("Use 'list-backups' to see available backups")
                sys.exit(1)
            restore_init_files(sys.argv[2])

        elif command == "list-backups":
            list_backups()

        elif command == "validate":
            success = run_validation(quick=False)
            sys.exit(0 if success else 1)

        elif command == "validate-quick":
            success = run_validation(quick=True)
            sys.exit(0 if success else 1)

        elif command == "update":
            print("📝 Updating __init__.py files with latest templates...")
            update_init_files()
            print("✅ Update complete!")

        elif command == "fix":
            print("🔧 Fixing all __init__.py issues...")
            fix_all_init_issues()
            print("✅ Fix complete!")

        elif command == "standardize":
            run_standardize()

        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'help' to see available commands")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
