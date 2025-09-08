#!/usr/bin/env python3
"""
Batch Error Fixing Script - Sửa lỗi một cách an toàn từng phase

Chiến lược:
1. Sửa import issues (F401, E402)
2. Sửa unused variables (ARG002, B007)
3. Sửa naming issues (N999)
4. Sửa undefined names (F821)
5. Sửa line length (E501)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any
import Exception
import OSError
import UnicodeDecodeError
import bool
import dict
import dir_name
import e
import enumerate
import file_path
import i
import int
import len
import line
import pattern
import phase
import print
import py_file
import replacement
import root_path
import self
import str


class ErrorFixer:
    """Tool để sửa lỗi batch một cách an toàn."""

    def __init__(self, root_path: Path):
        self.root = root_path
        self.dry_run = True

    def run_ruff_check(self) -> dict[str, Any]:
        """Chạy ruff check và parse kết quả."""
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", ".", "--format", "json"],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.stdout:
                import json

                return json.loads(result.stdout)
            return {"errors": []}
        except Exception as e:
            print(f"Error running ruff: {e}")
            return {"errors": []}

    def fix_imports(self, file_path: Path) -> bool:
        """Sửa các lỗi import cơ bản."""
        if not file_path.exists():
            return False

        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return False

        original = content

        # Fix F401: Remove unused imports (safe patterns only)
        unused_patterns = [
            r"^from\s+.*\s+import\s+AgentCapability.*$",  # Specific unused
        ]

        for pattern in unused_patterns:
            content = re.sub(pattern, "", content, flags=re.MULTILINE)

        if content != original:
            if not self.dry_run:
                file_path.write_text(content, encoding="utf-8")
            print(f"✓ Fixed imports in {file_path}")
            return True
        return False

    def fix_unused_args(self, file_path: Path) -> bool:
        """Prefix unused arguments với underscore."""
        if not file_path.exists():
            return False

        content = file_path.read_text(encoding="utf-8")
        original = content

        # Pattern cho unused arguments - safe replacements only
        patterns = [
            (r"\bdef\s+\w+\([^)]*\b(mock_\w+)", r"_\1"),  # mock args
            (r"\bdef\s+\w+\([^)]*\b(query|limit|skip)", r"_\1"),  # common unused
        ]

        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)

        if content != original:
            if not self.dry_run:
                file_path.write_text(content, encoding="utf-8")
            print(f"✓ Fixed unused args in {file_path}")
            return True
        return False

    def fix_naming(self, file_path: Path) -> bool:
        """Sửa tên module không hợp lệ."""
        if not file_path.exists():
            return False

        # N999: Invalid module name - rename files
        if file_path.stem[0].isupper():
            new_name = file_path.with_stem(file_path.stem.lower())
            if not self.dry_run:
                file_path.rename(new_name)
            print(f"✓ Renamed {file_path} -> {new_name}")
            return True
        return False

    def fix_line_length(self, file_path: Path) -> bool:
        """Sửa dòng quá dài (basic cases)."""
        if not file_path.exists():
            return False

        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        changed = False

        for i, line in enumerate(lines):
            if len(line) > 100:
                # Simple line breaking cho strings
                if "# " in line and len(line) > 100:
                    # Break comment lines
                    comment_start = line.find("# ")
                    if comment_start > 80:
                        lines[i] = line[:comment_start] + "\n    " + line[comment_start:]
                        changed = True

        if changed:
            content = "\n".join(lines)
            if not self.dry_run:
                file_path.write_text(content, encoding="utf-8")
            print(f"✓ Fixed line length in {file_path}")
            return True
        return False

    def run_phase(self, phase: str) -> int:
        """Chạy một phase sửa lỗi."""
        print(f"\n🔧 Phase: {phase}")
        fixed_count = 0

        # Chỉ sửa source code của dự án (bỏ qua .venv, __pycache__, etc.)
        source_dirs = ["zeta_vn", "tests", "tools", "scripts"]
        py_files = []

        for dir_name in source_dirs:
            dir_path = self.root / dir_name
            if dir_path.exists():
                py_files.extend(dir_path.rglob("*.py"))

        if phase == "imports":
            for py_file in py_files:
                if self.fix_imports(py_file):
                    fixed_count += 1

        elif phase == "unused_args":
            for py_file in py_files:
                if self.fix_unused_args(py_file):
                    fixed_count += 1

        elif phase == "naming":
            for py_file in py_files:
                if self.fix_naming(py_file):
                    fixed_count += 1

        elif phase == "line_length":
            for py_file in py_files:
                if self.fix_line_length(py_file):
                    fixed_count += 1

        print(f"Fixed {fixed_count} files in phase: {phase}")
        return fixed_count


def main():
    """Main entry point."""
    root = Path(__file__).parent.parent
    fixer = ErrorFixer(root)

    # Dry run first
    print("🧪 DRY RUN MODE - No changes will be made")
    phases = ["imports", "unused_args", "naming", "line_length"]

    for phase in phases:
        fixer.run_phase(phase)

    print("\n" + "=" * 50)
    print("Dry run complete. Run with --apply to make changes:")
    print("python tools/batch_fix_errors.py --apply")

    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        print("\n🔨 APPLYING FIXES...")
        fixer.dry_run = False

        for phase in phases:
            fixer.run_phase(phase)

        print("\n✅ Batch fixes applied!")
        print("Run 'uv run ruff check .' to see remaining errors.")


if __name__ == "__main__":
    main()
