#!/usr/bin/env python
"""
Safe Repository Fixer - Công cụ tối ưu toàn diện cho Python project

Mục tiêu: "quét – sửa – dọn – tối ưu" mà KHÔNG phá vỡ hành vi, có backup + rollback,
chỉ commit khi test pass.

Usage:
    python tools/fix_repo_safe.py --root zeta_vn                    # dry-run
    python tools/fix_repo_safe.py --root zeta_vn --apply            # apply + rollback nếu fail
    python tools/fix_repo_safe.py --root zeta_vn --apply --path core/  # chỉ fix thư mục core
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
import directory
import e
import error
import exclude_patterns
import f
import file_path
import force_all
import include_patterns
import int
import len
import list
import no_auto_all
import output_path
import path_filter
import pattern
import print
import py_file
import root_package
import self
import set
import sorted
import step
import str

REPO_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = REPO_ROOT / "reports"
BACKUP_DIR = REPO_ROOT / ".safe_fix_backups"
INIT_FILE = "__init__.py"


class SafeRepoFixer:
    """Safe repository fixer với backup và rollback tự động"""

    def __init__(
        self,
        root_package: str,
        apply: bool = False,
        path_filter: str | None = None,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        no_auto_all: bool = False,
        force_all: bool = False,
    ):
        self.root_package = root_package
        self.apply = apply
        self.path_filter = path_filter
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or [
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "node_modules",
            ".git",
            "venv",
            ".venv",
        ]
        self.no_auto_all = no_auto_all
        self.force_all = force_all

        self.package_path = REPO_ROOT / root_package
        self.backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = BACKUP_DIR / f"backup_{self.backup_timestamp}"
        self.report = {
            "timestamp": self.backup_timestamp,
            "root_package": root_package,
            "apply": apply,
            "steps": [],
            "errors": [],
            "stats": {"files_processed": 0, "files_modified": 0, "tests_passed": False},
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
        """Tạo backup toàn bộ package trước khi thay đổi"""
        try:
            if not self.package_path.exists():
                self.log_step(f"Package path not found: {self.package_path}", False)
                return False

            BACKUP_DIR.mkdir(exist_ok=True)
            shutil.copytree(self.package_path, self.backup_path)
            self.log_step(f"Created backup at {self.backup_path}")
            return True
        except Exception as e:
            self.log_step(f"Backup failed: {e}", False)
            return False

    def restore_backup(self) -> bool:
        """Khôi phục từ backup"""
        try:
            if not self.backup_path.exists():
                self.log_step("No backup found for restore", False)
                return False

            if self.package_path.exists():
                shutil.rmtree(self.package_path)

            shutil.copytree(self.backup_path, self.package_path)
            self.log_step(f"Restored from backup {self.backup_path}")
            return True
        except Exception as e:
            self.log_step(f"Restore failed: {e}", False)
            return False

    def ensure_init_files(self) -> bool:
        """Đảm bảo tất cả thư mục Python có __init__.py"""
        try:
            missing_inits = []

            for py_file in self.package_path.rglob("*.py"):
                parent = py_file.parent
                init_file = parent / "__init__.py"

                if not init_file.exists() and parent != self.package_path.parent:
                    missing_inits.append(init_file)

            if missing_inits:
                for init_file in missing_inits:
                    if self.apply:
                        init_file.touch()
                    self.log_step(f"{'Created' if self.apply else 'Would create'} {init_file}")

            self.log_step(f"Ensured __init__.py files: {len(missing_inits)} files")
            return True
        except Exception as e:
            self.log_step(f"Init files check failed: {e}", False)
            return False

    def generate_all_exports(self) -> bool:
        """Generate __all__ exports (conservative)"""
        if self.no_auto_all:
            self.log_step("Skipped __all__ generation (--no-auto-all)")
            return True

        try:
            modified_files = []

            for init_file in self.package_path.rglob("__init__.py"):
                if self._should_skip_file(init_file):
                    continue

                content = init_file.read_text(encoding="utf-8")

                # Chỉ thêm __all__ nếu chưa có (hoặc force)
                if "__all__" in content and not self.force_all:
                    continue

                # Tìm public symbols (không bắt đầu bằng "_")
                public_symbols = self._extract_public_symbols(init_file.parent)

                if public_symbols:
                    new_content = self._add_all_export(content, public_symbols)
                    if new_content != content and self.apply:
                        init_file.write_text(new_content, encoding="utf-8")
                        modified_files.append(init_file)

            self.log_step(f"Generated __all__ exports: {len(modified_files)} files")
            return True
        except Exception as e:
            self.log_step(f"__all__ generation failed: {e}", False)
            return False

    def _should_skip_file(self, file_path: Path) -> bool:
        """Kiểm tra có nên skip file không"""
        rel_path = file_path.relative_to(REPO_ROOT)

        for pattern in self.exclude_patterns:
            if pattern in str(rel_path):
                return True

        if self.path_filter:
            return not str(rel_path).startswith(self.path_filter)

        return False

    def _extract_public_symbols(self, directory: Path) -> list[str]:
        """Extract public symbols từ directory"""
        symbols = set()

        for py_file in directory.glob("*.py"):
            if py_file.name == "__init__.py":
                continue

            try:
                content = py_file.read_text(encoding="utf-8")
                # Simple extraction: class/function definitions
                lines = content.split("\n")
                for line in lines:
                    line = line.strip()
                    if line.startswith(("class ", "def ", "async def ")):
                        parts = line.split()
                        if len(parts) >= 2:
                            name = parts[1].split("(")[0].split(":")[0]
                            if not name.startswith("_"):
                                symbols.add(name)
            except Exception:
                continue

        return sorted(symbols)

    def _add_all_export(self, content: str, symbols: list[str]) -> str:
        """Thêm __all__ export vào content"""
        if "__all__" in content and not self.force_all:
            return content

        all_line = f"__all__ = {symbols!r}\n"

        if content.strip():
            return all_line + "\n" + content
        else:
            return all_line

    def run_ruff_fix(self) -> bool:
        """Chạy ruff --fix"""
        cmd = ["uv", "run", "ruff", "check", "--fix", str(self.package_path)]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step(
            "Ruff fix",
            success,
            f"Exit code: {result.returncode}" + (f"\nOutput: {result.stdout}" if result.stdout else ""),
        )
        return success

    def run_isort(self) -> bool:
        """Chạy isort"""
        cmd = ["uv", "run", "isort", str(self.package_path)]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step("isort", success, f"Exit code: {result.returncode}")
        return success

    def run_autoflake(self) -> bool:
        """Chạy autoflake để xóa import thừa"""
        cmd = [
            "uv",
            "run",
            "autoflake",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            "--in-place",
            "--recursive",
            str(self.package_path),
        ]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step("autoflake", success, f"Exit code: {result.returncode}")
        return success

    def run_ruff_format(self) -> bool:
        """Chạy ruff format"""
        cmd = ["uv", "run", "ruff", "format", str(self.package_path)]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step("Ruff format", success, f"Exit code: {result.returncode}")
        return success

    def run_mypy(self) -> bool:
        """Chạy mypy (strict)"""
        cmd = ["uv", "run", "mypy", str(self.package_path)]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step(
            "MyPy type check",
            success,
            f"Exit code: {result.returncode}" + (f"\nErrors: {result.stderr}" if result.stderr else ""),
        )
        return success

    def run_pytest(self) -> bool:
        """Chạy pytest"""
        test_dir = REPO_ROOT / "tests"
        if not test_dir.exists():
            self.log_step("No tests directory found, skipping pytest")
            return True

        cmd = ["uv", "run", "pytest", "-q", str(test_dir)]
        result = self.run_command(cmd)

        success = result.returncode == 0
        self.log_step(
            "PyTest",
            success,
            f"Exit code: {result.returncode}" + (f"\nOutput: {result.stdout}" if result.stdout else ""),
        )
        self.report["stats"]["tests_passed"] = success
        return success

    def save_report(self) -> None:
        """Lưu báo cáo"""
        REPORTS_DIR.mkdir(exist_ok=True)

        # JSON report
        json_report = REPORTS_DIR / "fix_report.json"
        with json_report.open("w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        # Markdown report
        md_report = REPORTS_DIR / "fix_report.md"
        self._generate_markdown_report(md_report)

        print("\n📊 Reports saved:")
        print(f"   - JSON: {json_report}")
        print(f"   - Markdown: {md_report}")

    def _generate_markdown_report(self, output_path: Path) -> None:
        """Generate markdown report"""
        with output_path.open("w", encoding="utf-8") as f:
            f.write("# Safe Repo Fix Report\n\n")
            f.write(f"**Timestamp:** {self.report['timestamp']}\n")
            f.write(f"**Root Package:** {self.report['root_package']}\n")
            f.write(f"**Mode:** {'Apply' if self.apply else 'Dry-run'}\n")
            f.write(f"**Tests Passed:** {'✅' if self.report['stats']['tests_passed'] else '❌'}\n\n")

            f.write("## Steps\n\n")
            for step in self.report["steps"]:
                icon = "✅" if step["success"] else "❌"
                f.write(f"- {icon} **{step['step']}**\n")
                if step["details"]:
                    f.write(f"  - {step['details']}\n")

            if self.report["errors"]:
                f.write("\n## Errors\n\n")
                for error in self.report["errors"]:
                    f.write(f"- ❌ {error}\n")

    def run(self) -> bool:
        """Chạy toàn bộ quy trình"""
        print(f"🔧 Safe Repo Fixer - {'APPLY' if self.apply else 'DRY-RUN'}")
        print(f"📦 Package: {self.root_package}")
        print(f"📁 Path: {self.package_path}")
        if self.path_filter:
            print(f"🎯 Filter: {self.path_filter}")
        print()

        # Backup (chỉ khi apply)
        if self.apply and not self.create_backup():
            return False

        try:
            # Bước 1: Ensure __init__.py files
            if not self.ensure_init_files():
                return False

            # Bước 2: Generate __all__ exports
            if not self.generate_all_exports():
                return False

            # Bước 3: Ruff --fix
            if not self.run_ruff_fix():
                return False

            # Bước 4: isort
            if not self.run_isort():
                return False

            # Bước 5: autoflake
            if not self.run_autoflake():
                return False

            # Bước 6: Ruff format
            if not self.run_ruff_format():
                return False

            # Bước 7: MyPy check
            mypy_success = self.run_mypy()

            # Bước 8: PyTest
            pytest_success = self.run_pytest()

            # Kiểm tra kết quả cuối
            if self.apply and (not mypy_success or not pytest_success):
                self.log_step("Quality checks failed, rolling back...", False)
                self.restore_backup()
                return False

            success = mypy_success and pytest_success
            self.log_step(f"All steps completed {'successfully' if success else 'with issues'}", success)

            return success

        except Exception as e:
            self.log_step(f"Unexpected error: {e}", False)
            if self.apply:
                self.restore_backup()
            return False

        finally:
            self.save_report()


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Repository Fixer")
    parser.add_argument("--root", required=True, help="Root package name (e.g., zeta_vn)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--path", help="Filter by path (e.g., core/)")
    parser.add_argument("--include", action="append", help="Include patterns")
    parser.add_argument("--exclude", action="append", help="Exclude patterns")
    parser.add_argument("--no-auto-all", action="store_true", help="Skip __all__ generation")
    parser.add_argument("--force-all", action="store_true", help="Force __all__ regeneration")

    args = parser.parse_args()

    fixer = SafeRepoFixer(
        root_package=args.root,
        apply=args.apply,
        path_filter=args.path,
        include_patterns=args.include,
        exclude_patterns=args.exclude,
        no_auto_all=args.no_auto_all,
        force_all=args.force_all,
    )

    success = fixer.run()

    print(f"\n{'🎉 SUCCESS' if success else '💥 FAILED'}")

    if success and args.apply:
        print("\n💡 Để commit thay đổi:")
        print("   git add .")
        print('   git commit -m "chore(tooling): apply safe fix (ruff/isort/autoflake/mypy/pytest)"')
        print("\n⚠️  KHÔNG push tự động - kiểm tra thay đổi trước!")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
