#!/usr/bin/env python3
"""
🧹 AUTO CLEANUP SCRIPT - Safe Repository Maintenance

Tự động cleanup và maintain code quality một cách an toàn.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
import Exception
import bool
import cmd
import description
import e
import file
import file_path
import len
import list
import path
import pattern
import print
import project_root
import required_file
import self
import str


class SafeCleanup:
    """Safe repository cleanup manager."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        self.project_root = project_root
        self.backup_dir = project_root / ".cleanup_backups" / datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def backup_file(self, file_path: Path) -> Path:
        """Backup file before modification."""
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path

    def run_safe_command(self, cmd: list[str], description: str) -> bool:
        """Run command safely with logging."""
        print(f"🔧 {description}...")
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                print(f"✅ {description} completed successfully")
                return True
            else:
                print(f"❌ {description} failed:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ {description} error: {e}")
            return False

    def auto_format_code(self) -> bool:
        """Auto format code with ruff."""
        return self.run_safe_command(["uv", "run", "ruff", "format", "."], "Code formatting")

    def auto_fix_linting(self) -> bool:
        """Auto fix safe linting issues."""
        return self.run_safe_command(
            ["uv", "run", "ruff", "check", ".", "--fix", "--select", "F401,I001,W291"],
            "Auto-fix safe linting issues",
        )

    def cleanup_cache_files(self) -> None:
        """Remove cache and temporary files."""
        print("🗑️  Cleaning cache files...")

        patterns_to_remove = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/.pytest_cache",
            "**/.mypy_cache",
            "**/.ruff_cache",
            "**/node_modules",
            "**/.DS_Store",
            "**/Thumbs.db",
            "**/*.tmp",
        ]

        removed_count = 0
        for pattern in patterns_to_remove:
            for path in self.project_root.glob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                        removed_count += 1
                    elif path.is_dir():
                        shutil.rmtree(path)
                        removed_count += 1
                except Exception as e:
                    print(f"⚠️  Could not remove {path}: {e}")

        print(f"✅ Removed {removed_count} cache files/directories")

    def organize_imports(self) -> bool:
        """Organize imports safely."""
        return self.run_safe_command(
            ["uv", "run", "ruff", "check", ".", "--fix", "--select", "I"], "Import organization"
        )

    def remove_unused_imports(self) -> bool:
        """Remove unused imports safely."""
        return self.run_safe_command(
            ["uv", "run", "ruff", "check", ".", "--fix", "--select", "F401"],
            "Unused import removal",
        )

    def check_large_files(self) -> None:
        """Check for large files that should be removed."""
        print("📏 Checking for large files...")

        large_files = []
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    # Files larger than 10MB
                    if size > 10 * 1024 * 1024:
                        large_files.append((file_path, size))
                except Exception:
                    continue

        if large_files:
            print("⚠️  Found large files:")
            for file_path, size in large_files:
                size_mb = size / (1024 * 1024)
                print(f"  📁 {file_path.relative_to(self.project_root)}: {size_mb:.1f}MB")
        else:
            print("✅ No large files found")

    def validate_structure(self) -> bool:
        """Validate project structure."""
        print("🏗️  Validating project structure...")

        required_files = ["pyproject.toml", "README.md", ".gitignore", "zeta_vn/__init__.py"]

        missing_files = []
        for required_file in required_files:
            if not (self.project_root / required_file).exists():
                missing_files.append(required_file)

        if missing_files:
            print("❌ Missing required files:")
            for file in missing_files:
                print(f"  📄 {file}")
            return False
        else:
            print("✅ Project structure is valid")
            return True

    def run_full_cleanup(self) -> bool:
        """Run complete safe cleanup."""
        print("🚀 Starting safe repository cleanup...")
        print(f"📦 Backup directory: {self.backup_dir}")

        success = True

        # Step 1: Validate structure first
        if not self.validate_structure():
            print("❌ Project structure validation failed")
            return False

        # Step 2: Cache cleanup (safe)
        self.cleanup_cache_files()

        # Step 3: Check for large files
        self.check_large_files()

        # Step 4: Code formatting
        if not self.auto_format_code():
            success = False

        # Step 5: Safe auto-fixes
        if not self.auto_fix_linting():
            success = False

        # Step 6: Import organization
        if not self.organize_imports():
            success = False

        # Step 7: Remove unused imports
        if not self.remove_unused_imports():
            success = False

        if success:
            print("✅ Safe cleanup completed successfully!")
        else:
            print("⚠️  Some cleanup operations failed. Check logs above.")

        return success


def main() -> None:
    """Main entry point."""
    cleanup = SafeCleanup()

    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("🔍 Dry run mode - no changes will be made")
        # In dry run, just check structure and large files
        cleanup.validate_structure()
        cleanup.check_large_files()
    else:
        success = cleanup.run_full_cleanup()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
