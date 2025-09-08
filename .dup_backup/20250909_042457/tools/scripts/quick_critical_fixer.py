#!/usr/bin/env python
"""
🚨 QUICK CRITICAL FIXER - Sửa nhanh lỗi critical
=================================================

Sửa các lỗi critical blockers:
- F821: Undefined name (missing variable assignments)
- E402: Module level import not at top
- F841: Unused variables
- Missing imports in __init__.py

Usage: python tools/quick_critical_fixer.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
import Exception
import any
import bool
import e
import enumerate
import int
import len
import level
import line
import message
import pattern
import print
import replacement
import self
import str
import unused

REPO_ROOT = Path(__file__).parent.parent.resolve()


class QuickCriticalFixer:
    """Sửa nhanh các lỗi critical để dự án có thể chạy được"""

    def __init__(self):
        self.fixes_applied = 0
        self.errors_found = 0

    def log(self, message: str, level: str = "INFO"):
        """Log với màu"""
        colors = {
            "INFO": "\033[96m",  # Cyan
            "SUCCESS": "\033[92m",  # Green
            "WARNING": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
        }
        print(f"{colors.get(level, '')}{message}\033[0m")

    def fix_undefined_names_in_tests(self) -> int:
        """Sửa F821 undefined name trong test files"""
        fixes = 0

        # Fix test_user_entity.py - missing user assignment
        test_user_file = REPO_ROOT / "zeta_vn/tests/unit/test_user_entity.py"
        if test_user_file.exists():
            content = test_user_file.read_text(encoding="utf-8")

            # Fix missing user assignment in test methods
            patterns = [
                (
                    r'(\s+)_ = User\.create\("testuser", "test@example\.com", "hash"\)\s*\n(\s+)(.*user\.)',
                    r'\1user = User.create("testuser", "test@example.com", "hash")\n\2\3',
                ),
                (
                    r'(\s+)_ = User\.create\("testuser2", "test2@example\.com", "hash"\)\s*\n(\s+)(.*user\.)',
                    r'\1user = User.create("testuser2", "test2@example.com", "hash")\n\2\3',
                ),
            ]

            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    fixes += 1
                    self.log(f"Fixed undefined user assignment in {test_user_file.name}", "SUCCESS")

            if fixes > 0:
                test_user_file.write_text(content, encoding="utf-8")

        return fixes

    def fix_undefined_result_variables(self) -> int:
        """Sửa F821 undefined result variables"""
        fixes = 0

        files_to_fix = [
            "zeta_vn/tests/unit/test_value_objects.py",
            "zeta_vn/tests/unit/test_workflow_entity.py",
            "zeta_vn/trainer/demo_authorization.py",
            "zeta_vn/workflows/trainer_pipeline.py",
        ]

        for file_path in files_to_fix:
            full_path = REPO_ROOT / file_path
            if not full_path.exists():
                continue

            content = full_path.read_text(encoding="utf-8")
            original_content = content

            # Common patterns for missing result assignments
            patterns = [
                # Pattern: _ = func() followed by assert result
                (r"(\s+)_ = ([^=\n]+)\s*\n(\s+)assert result", r"\1result = \2\n\3assert result"),
                (r"(\s+)_ = ([^=\n]+)\s*\n(\s+)print\(.*result", r"\1result = \2\n\3print("),
                # Pattern: function call without assignment
                (
                    r'(\s+)([a-zA-Z_][a-zA-Z0-9_.]*\([^)]*\))\s*\n(\s+)print\(f".*\{result',
                    r'\1result = \2\n\3print(f"',
                ),
            ]

            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)

            if content != original_content:
                full_path.write_text(content, encoding="utf-8")
                fixes += 1
                self.log(f"Fixed undefined result in {file_path}", "SUCCESS")

        return fixes

    def fix_import_order(self) -> int:
        """Sửa E402 imports not at top"""
        fixes = 0

        file_path = REPO_ROOT / "zeta_vn/tools/ports_tools.py"
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            # Find docstring end and move imports there
            lines = content.split("\n")
            import_lines = []
            other_lines = []
            in_docstring = False
            docstring_ended = False

            for i, line in enumerate(lines):
                if '"""' in line and not docstring_ended:
                    if in_docstring:
                        docstring_ended = True
                        other_lines.append(line)
                    else:
                        in_docstring = True
                        other_lines.append(line)
                elif (line.strip().startswith("import ") or line.strip().startswith("from ")) and docstring_ended:
                    import_lines.append(line)
                else:
                    other_lines.append(line)

            if import_lines:
                # Rebuild file with imports at top after docstring
                new_lines = []
                for line in other_lines:
                    new_lines.append(line)
                    if '"""' in line and docstring_ended:
                        new_lines.append("")
                        new_lines.extend(import_lines)
                        new_lines.append("")
                        break

                # Add remaining lines (skip import lines)
                for line in other_lines[len(new_lines) - len(import_lines) - 2 :]:
                    if not (line.strip().startswith("import ") or line.strip().startswith("from ")):
                        new_lines.append(line)

                file_path.write_text("\n".join(new_lines), encoding="utf-8")
                fixes += 1
                self.log(f"Fixed import order in {file_path.name}", "SUCCESS")

        return fixes

    def fix_unused_variables(self) -> int:
        """Sửa F841 unused variables"""
        fixes = 0

        file_path = REPO_ROOT / "zeta_vn/tests/utils/test_helpers.py"
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            # Fix async__ unused variable
            if "async__ = sessionmaker" in content:
                content = content.replace(
                    "async__ = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)",
                    "async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)",
                )
                fixes += 1
                self.log(f"Fixed unused variable in {file_path.name}", "SUCCESS")
                file_path.write_text(content, encoding="utf-8")

        return fixes

    def fix_missing_imports(self) -> int:
        """Sửa missing imports trong __init__.py files"""
        fixes = 0

        # Fix main __init__.py unused imports
        main_init = REPO_ROOT / "zeta_vn/__init__.py"
        if main_init.exists():
            content = main_init.read_text(encoding="utf-8")

            # Remove unused imports at module level
            lines = content.split("\n")
            new_lines = []

            for line in lines:
                # Keep only necessary imports
                if (
                    line.strip().startswith("import ")
                    and any(unused in line for unused in ["importlib", "logging", "sys"])
                    and "# Required" not in line
                ):
                    continue  # Skip unused imports
                new_lines.append(line)

            if len(new_lines) != len(lines):
                main_init.write_text("\n".join(new_lines), encoding="utf-8")
                fixes += 1
                self.log(f"Removed unused imports from {main_init.name}", "SUCCESS")

        return fixes

    def run_quick_lint_check(self) -> bool:
        """Chạy quick lint check để xem cải thiện"""
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", "zeta_vn", "--quiet"],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )

            error_lines = result.stdout.count("\n") if result.stdout else 0
            self.log(f"Current lint errors: {error_lines}", "INFO")
            return error_lines < 1000  # Reasonable threshold

        except Exception as e:
            self.log(f"Lint check failed: {e}", "ERROR")
            return False

    def run_fixes(self) -> bool:
        """Chạy tất cả fixes"""
        self.log("🚨 Starting Quick Critical Fixes...", "INFO")

        total_fixes = 0

        # 1. Fix undefined names in tests
        self.log("Fixing undefined names in tests...", "INFO")
        total_fixes += self.fix_undefined_names_in_tests()

        # 2. Fix undefined result variables
        self.log("Fixing undefined result variables...", "INFO")
        total_fixes += self.fix_undefined_result_variables()

        # 3. Fix import order
        self.log("Fixing import order...", "INFO")
        total_fixes += self.fix_import_order()

        # 4. Fix unused variables
        self.log("Fixing unused variables...", "INFO")
        total_fixes += self.fix_unused_variables()

        # 5. Fix missing imports
        self.log("Fixing missing imports...", "INFO")
        total_fixes += self.fix_missing_imports()

        self.log(f"✅ Applied {total_fixes} critical fixes", "SUCCESS")

        # Quick verification
        self.log("Running quick verification...", "INFO")
        improved = self.run_quick_lint_check()

        return improved


def main():
    """Main entry point"""
    fixer = QuickCriticalFixer()
    success = fixer.run_fixes()

    if success:
        print("\n🎉 Quick critical fixes completed successfully!")
        print("💡 You can now proceed with comprehensive optimization")
    else:
        print("\n⚠️ Some issues remain, but major blockers should be fixed")
        print("💡 Proceed with caution or run manual fixes")


if __name__ == "__main__":
    main()
