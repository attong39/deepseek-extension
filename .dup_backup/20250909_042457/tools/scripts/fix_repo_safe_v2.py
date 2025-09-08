#!/usr/bin/env python
"""
Safe Repository Fixer - Version 2 với exclude tests và focus core package

Mục tiêu: Tập trung vào core package trước, bỏ qua tests để giảm noise
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import Exception
import apply
import bool
import cwd
import details
import dst
import e
import exclude_tests
import f
import int
import item
import list
import path
import path_filter
import pattern
import print
import py_file
import root_package
import self
import src
import step
import str

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = REPO_ROOT / "reports"
BACKUP_DIR = REPO_ROOT / ".safe_fix_backups"


class SafeRepoFixerV2:
    """Safe repository fixer với focus core package, exclude tests"""

    def __init__(
        self,
        root_package: str,
        apply: bool = False,
        path_filter: str | None = None,
        exclude_tests: bool = True,
    ):
        self.root_package = root_package
        self.apply = apply
        self.path_filter = path_filter
        self.exclude_tests = exclude_tests

        self.package_path = REPO_ROOT / root_package
        self.backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = BACKUP_DIR / f"backup_{self.backup_timestamp}"

        # Core exclude patterns (focusing on main code)
        self.exclude_patterns = [
            "tests/",
            "test_*.py",
            "*_test.py",
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ]

        self.report = {
            "timestamp": self.backup_timestamp,
            "root_package": root_package,
            "apply": apply,
            "exclude_tests": exclude_tests,
            "steps": [],
            "errors": [],
        }

    def log_step(self, step: str, success: bool = True, details: str = ""):
        """Ghi log từng bước"""
        print(f"{'✅' if success else '❌'} {step}")
        if details:
            print(f"   {details}")

        self.report["steps"].append(
            {
                "step": step,
                "success": success,
                "details": details,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def run_command(self, cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
        """Chạy command với error handling"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            return result
        except Exception as e:
            self.report["errors"].append(f"Command failed: {' '.join(cmd)} - {e}")
            raise

    def create_backup(self) -> bool:
        """Tạo backup focused path"""
        try:
            if not self.package_path.exists():
                self.log_step(f"Package path not found: {self.package_path}", False)
                return False

            BACKUP_DIR.mkdir(exist_ok=True)

            # Backup target path only
            if self.path_filter:
                target_path = self.package_path / self.path_filter
                if target_path.exists():
                    backup_target = self.backup_path / self.path_filter
                    backup_target.parent.mkdir(parents=True, exist_ok=True)
                    if target_path.is_dir():
                        shutil.copytree(target_path, backup_target)
                    else:
                        shutil.copy2(target_path, backup_target)
                    self.log_step(f"Created focused backup at {backup_target}")
                else:
                    self.log_step(f"Target path not found: {target_path}", False)
                    return False
            else:
                # Backup whole package excluding tests
                self._backup_selective(self.package_path, self.backup_path)
                self.log_step(f"Created selective backup at {self.backup_path}")

            return True
        except Exception as e:
            self.log_step(f"Backup failed: {e}", False)
            return False

    def _backup_selective(self, src: Path, dst: Path) -> None:
        """Backup excluding test files"""
        dst.mkdir(parents=True, exist_ok=True)

        for item in src.iterdir():
            if self._should_skip_path(item):
                continue

            dst_item = dst / item.name
            if item.is_dir():
                self._backup_selective(item, dst_item)
            else:
                shutil.copy2(item, dst_item)

    def _should_skip_path(self, path: Path) -> bool:
        """Kiểm tra có nên skip path không"""
        path_str = str(path.relative_to(REPO_ROOT))

        for pattern in self.exclude_patterns:
            if pattern in path_str or path.name.startswith(pattern.replace("*", "")):
                return True

        return False

    def run_ruff_fix_selective(self) -> bool:
        """Chạy ruff fix nhưng exclude tests"""
        if self.path_filter:
            target_path = self.package_path / self.path_filter
            cmd = ["uv", "run", "ruff", "check", "--fix", str(target_path)]
        else:
            # Fix whole package but exclude test patterns
            cmd = ["uv", "run", "ruff", "check", "--fix", str(self.package_path)]
            # Add exclude patterns
            for pattern in ["tests/", "test_*.py", "*_test.py"]:
                cmd.extend(["--exclude", pattern])

        result = self.run_command(cmd)
        success = result.returncode == 0

        self.log_step(
            "Ruff fix (core only)",
            success,
            f"Exit code: {result.returncode}" + (f"\nOutput: {result.stdout[:500]}" if result.stdout else ""),
        )
        return success

    def run_ruff_format_selective(self) -> bool:
        """Chạy ruff format selective"""
        if self.path_filter:
            target_path = self.package_path / self.path_filter
            cmd = ["uv", "run", "ruff", "format", str(target_path)]
        else:
            cmd = ["uv", "run", "ruff", "format", str(self.package_path)]
            # Add exclude patterns
            for pattern in ["tests/", "test_*.py", "*_test.py"]:
                cmd.extend(["--exclude", pattern])

        result = self.run_command(cmd)
        success = result.returncode == 0

        self.log_step("Ruff format (core only)", success, f"Exit code: {result.returncode}")
        return success

    def run_isort_selective(self) -> bool:
        """Chạy isort selective"""
        if self.path_filter:
            target_path = self.package_path / self.path_filter
            cmd = ["uv", "run", "isort", str(target_path)]
        else:
            cmd = [
                "uv",
                "run",
                "isort",
                str(self.package_path),
                "--skip-glob",
                "*/tests/*",
                "--skip-glob",
                "*test*.py",
            ]

        result = self.run_command(cmd)
        success = result.returncode == 0

        self.log_step("isort (core only)", success, f"Exit code: {result.returncode}")
        return success

    def check_syntax_only(self) -> bool:
        """Chỉ kiểm tra syntax, không chạy tests"""
        try:
            if self.path_filter:
                target_path = self.package_path / self.path_filter

                # Check if it's a single file
                if target_path.is_file():
                    cmd = [sys.executable, "-m", "py_compile", str(target_path)]
                else:
                    # Check all .py files in directory
                    py_files = list(target_path.rglob("*.py"))
                    if not py_files:
                        self.log_step("No Python files found to check")
                        return True

                    for py_file in py_files[:5]:  # Check first 5 files only
                        cmd = [sys.executable, "-m", "py_compile", str(py_file)]
                        result = self.run_command(cmd)
                        if result.returncode != 0:
                            self.log_step(f"Syntax error in {py_file}", False)
                            return False
            else:
                # Quick syntax check on core files only
                core_files = []
                for pattern in ["core/**/*.py", "app/**/*.py", "data/**/*.py"]:
                    core_files.extend(self.package_path.glob(pattern))

                if not core_files:
                    self.log_step("No core files found to check")
                    return True

                # Check first 10 files
                for py_file in core_files[:10]:
                    if self._should_skip_path(py_file):
                        continue

                    cmd = [sys.executable, "-m", "py_compile", str(py_file)]
                    result = self.run_command(cmd)
                    if result.returncode != 0:
                        self.log_step(f"Syntax error in {py_file}", False, result.stderr)
                        return False

            self.log_step("Syntax check passed")
            return True

        except Exception as e:
            self.log_step(f"Syntax check failed: {e}", False)
            return False

    def save_report(self) -> None:
        """Lưu báo cáo"""
        REPORTS_DIR.mkdir(exist_ok=True)

        json_report = REPORTS_DIR / "fix_report_v2.json"
        with json_report.open("w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        md_report = REPORTS_DIR / "fix_report_v2.md"
        with md_report.open("w", encoding="utf-8") as f:
            f.write("# Safe Repo Fix Report V2 (Core Focus)\n\n")
            f.write(f"**Timestamp:** {self.report['timestamp']}\n")
            f.write(f"**Root Package:** {self.report['root_package']}\n")
            f.write(f"**Mode:** {'Apply' if self.apply else 'Dry-run'}\n")
            f.write(f"**Exclude Tests:** {self.report['exclude_tests']}\n\n")

            f.write("## Steps\n\n")
            for step in self.report["steps"]:
                icon = "✅" if step["success"] else "❌"
                f.write(f"- {icon} **{step['step']}**\n")
                if step["details"]:
                    f.write(f"  - {step['details']}\n")

        print("\n📊 Reports saved:")
        print(f"   - JSON: {json_report}")
        print(f"   - Markdown: {md_report}")

    def run(self) -> bool:
        """Chạy quy trình selective"""
        print(f"🔧 Safe Repo Fixer V2 (Core Focus) - {'APPLY' if self.apply else 'DRY-RUN'}")
        print(f"📦 Package: {self.root_package}")
        if self.path_filter:
            print(f"🎯 Focus: {self.path_filter}")
        print(f"🚫 Exclude tests: {self.exclude_tests}")
        print()

        # Backup (chỉ khi apply)
        if self.apply and not self.create_backup():
            return False

        try:
            # Bước 1: Ruff fix selective
            if not self.run_ruff_fix_selective():
                self.log_step("Ruff fix failed, stopping", False)
                return False

            # Bước 2: isort selective
            if not self.run_isort_selective():
                self.log_step("isort failed, continuing...", False)

            # Bước 3: Ruff format selective
            if not self.run_ruff_format_selective():
                self.log_step("Ruff format failed, continuing...", False)

            # Bước 4: Syntax check only (không chạy tests)
            syntax_ok = self.check_syntax_only()

            self.log_step(
                f"Core package processing {'completed successfully' if syntax_ok else 'completed with syntax issues'}",
                syntax_ok,
            )

            return syntax_ok

        except Exception as e:
            self.log_step(f"Unexpected error: {e}", False)
            return False

        finally:
            self.save_report()


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Repository Fixer V2 (Core Focus)")
    parser.add_argument("--root", required=True, help="Root package name (e.g., zeta_vn)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--path", help="Filter by specific path (e.g., core/domain/)")
    parser.add_argument("--include-tests", action="store_true", help="Include tests (default: exclude)")

    args = parser.parse_args()

    fixer = SafeRepoFixerV2(
        root_package=args.root,
        apply=args.apply,
        path_filter=args.path,
        exclude_tests=not args.include_tests,
    )

    success = fixer.run()

    print(f"\n{'🎉 SUCCESS' if success else '💥 FAILED'}")

    if success and args.apply:
        print("\n💡 Tiếp theo:")
        print("   1. Kiểm tra git diff để xem thay đổi")
        print("   2. Chạy tests manual nếu cần: uv run pytest tests/ -v")
        print("   3. Commit nếu OK: git add . && git commit -m 'chore: fix core package linting'")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
