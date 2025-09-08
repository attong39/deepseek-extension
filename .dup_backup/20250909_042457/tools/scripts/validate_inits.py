#!/usr/bin/env python3
"""Script validation tổng thể cho __init__.py files."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


class InitFileValidator:
    """Validator cho __init__.py files."""
import Exception
import SyntaxError
import bool
import dict
import e
import enumerate
import error
import f
import file_path
import int
import len
import line
import list
import open
import path
import print
import py_file
import self
import set
import sorted
import str
import warning

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict[str, int] = {
            "total_files": 0,
            "valid_files": 0,
            "files_with_errors": 0,
            "files_with_warnings": 0,
        }

    def validate_syntax(self, file_path: Path) -> bool:
        """Kiểm tra syntax của __init__.py file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            ast.parse(content)
            return True
        except SyntaxError as e:
            self.errors.append(f"{file_path}: Syntax error - {e}")
            return False
        except Exception as e:
            self.errors.append(f"{file_path}: Parse error - {e}")
            return False

    def check_imports(self, file_path: Path) -> None:
        """Kiểm tra imports trong __init__.py."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check for relative imports
            if "from ." in content:
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    if line.strip().startswith("from .") and "import" in line:
                        # Valid relative import
                        continue

            # Check for __future__ imports
            if "from __future__" not in content:
                self.warnings.append(f"{file_path}: Missing __future__ annotations import")

        except Exception as e:
            self.errors.append(f"{file_path}: Import check failed - {e}")

    def check_structure(self, file_path: Path) -> None:
        """Kiểm tra cấu trúc chuẩn của __init__.py."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check for docstring
            if '"""' not in content and "'''" not in content:
                self.warnings.append(f"{file_path}: Missing module docstring")

            # Check for __all__ if there are exports
            if "def " in content or "class " in content:
                if "__all__" not in content:
                    self.warnings.append(f"{file_path}: Missing __all__ declaration")

        except Exception as e:
            self.errors.append(f"{file_path}: Structure check failed - {e}")

    def validate_file(self, file_path: Path) -> None:
        """Validate một __init__.py file."""
        self.stats["total_files"] += 1

        if not self.validate_syntax(file_path):
            self.stats["files_with_errors"] += 1
            return

        initial_warnings = len(self.warnings)

        self.check_imports(file_path)
        self.check_structure(file_path)

        if len(self.warnings) > initial_warnings:
            self.stats["files_with_warnings"] += 1
        else:
            self.stats["valid_files"] += 1

    def scan_directory(self, root_dir: Path = None) -> None:
        """Scan tất cả __init__.py files trong directory."""
        if root_dir is None:
            root_dir = Path("zeta_vn")

        for init_file in root_dir.rglob("__init__.py"):
            self.validate_file(init_file)

    def find_missing_inits(self, root_dir: Path = None) -> set[Path]:
        """Tìm directories thiếu __init__.py."""
        if root_dir is None:
            root_dir = Path("zeta_vn")

        missing = set()

        for py_file in root_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            parent = py_file.parent
            init_file = parent / "__init__.py"

            if not init_file.exists():
                missing.add(parent)

        return missing

    def generate_report(self) -> str:
        """Generate validation report."""
        lines = [
            "=" * 60,
            "🔍 INIT FILES VALIDATION REPORT",
            "=" * 60,
            "",
            "📊 STATISTICS:",
            f"  Total files scanned: {self.stats['total_files']}",
            f"  Valid files: {self.stats['valid_files']}",
            f"  Files with warnings: {self.stats['files_with_warnings']}",
            f"  Files with errors: {self.stats['files_with_errors']}",
            "",
        ]

        if self.errors:
            lines.extend(
                [
                    "❌ ERRORS:",
                    "",
                ]
            )
            for error in self.errors:
                lines.append(f"  - {error}")
            lines.append("")

        if self.warnings:
            lines.extend(
                [
                    "⚠️  WARNINGS:",
                    "",
                ]
            )
            for warning in self.warnings:
                lines.append(f"  - {warning}")
            lines.append("")

        # Check for missing init files
        missing = self.find_missing_inits()
        if missing:
            lines.extend(
                [
                    "📁 MISSING __init__.py FILES:",
                    "",
                ]
            )
            for path in sorted(missing):
                lines.append(f"  - {path}")
            lines.append("")

        if not self.errors and not self.warnings and not missing:
            lines.extend(
                [
                    "✅ ALL CHECKS PASSED!",
                    "All __init__.py files are properly structured and valid.",
                    "",
                ]
            )

        lines.append("=" * 60)

        return "\n".join(lines)


def main() -> None:
    """Main validation function."""
    validator = InitFileValidator()

    print("🔍 Scanning __init__.py files...")
    validator.scan_directory()

    report = validator.generate_report()
    print(report)

    # Exit with error code if there are errors
    if validator.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
