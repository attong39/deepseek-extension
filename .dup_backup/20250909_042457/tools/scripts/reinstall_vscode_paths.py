#!/usr/bin/env python3
"""
Script cài lại và cấu hình đường dẫn VS Code cho ZETA project
Đảm bảo Python interpreter, PYTHONPATH, và environment variables được setup đúng
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
import Exception
import ImportError
import KeyboardInterrupt
import bool
import dict
import e
import f
import int
import issue
import message
import open
import print
import self
import str

# Rich imports cho UI đẹp
try:
    from rich import print as rprint
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False


def print_info(message: str) -> None:
    """In thông báo với formatting"""
    if RICH_AVAILABLE:
        rprint(f"[blue]ℹ️ {message}[/blue]")
    else:
        print(f"ℹ️ {message}")


def print_success(message: str) -> None:
    """In thông báo thành công"""
    if RICH_AVAILABLE:
        rprint(f"[green]✅ {message}[/green]")
    else:
        print(f"✅ {message}")


def print_warning(message: str) -> None:
    """In cảnh báo"""
    if RICH_AVAILABLE:
        rprint(f"[yellow]⚠️ {message}[/yellow]")
    else:
        print(f"⚠️ {message}")


def print_error(message: str) -> None:
    """In lỗi"""
    if RICH_AVAILABLE:
        rprint(f"[red]❌ {message}[/red]")
    else:
        print(f"❌ {message}")


class VSCodePathInstaller:
    """Cài lại và cấu hình đường dẫn VS Code"""

    def __init__(self) -> None:
        self.workspace_root = Path.cwd()
        self.vscode_dir = self.workspace_root / ".vscode"
        self.venv_dir = self.workspace_root / ".venv"
        self.settings_file = self.vscode_dir / "settings.json"

        # Python paths
        if os.name == "nt":  # Windows
            self.python_exe = self.venv_dir / "Scripts" / "python.exe"
        else:  # Unix
            self.python_exe = self.venv_dir / "bin" / "python"

    def check_prerequisites(self) -> bool:
        """Kiểm tra điều kiện tiên quyết"""
        if RICH_AVAILABLE:
            rprint("\n[bold blue]🔍 KIỂM TRA ĐIỀU KIỆN TIÊN QUYẾT[/bold blue]")
        else:
            print("\n🔍 KIỂM TRA ĐIỀU KIỆN TIÊN QUYẾT")

        issues = []

        # Kiểm tra workspace
        if not self.workspace_root.exists():
            issues.append("Workspace root không tồn tại")
        else:
            print_success(f"Workspace root: {self.workspace_root}")

        # Kiểm tra .vscode directory
        if not self.vscode_dir.exists():
            print_warning(".vscode directory không tồn tại - sẽ tạo mới")
            self.vscode_dir.mkdir(exist_ok=True)
        else:
            print_success(f".vscode directory: {self.vscode_dir}")

        # Kiểm tra virtual environment
        if not self.venv_dir.exists():
            issues.append("Virtual environment (.venv) không tồn tại")
        elif not self.python_exe.exists():
            issues.append(f"Python executable không tồn tại: {self.python_exe}")
        else:
            print_success(f"Virtual environment: {self.venv_dir}")
            print_success(f"Python executable: {self.python_exe}")

        if issues:
            for issue in issues:
                print_error(issue)
            return False

        return True

    def get_current_python_info(self) -> dict[str, Any]:
        """Lấy thông tin Python hiện tại"""
        try:
            result = subprocess.run(
                [
                    str(self.python_exe),
                    "-c",
                    "import sys; print(sys.executable); print(sys.version); print(sys.prefix); print(sys.base_prefix)",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            lines = result.stdout.strip().split("\n")
            return {
                "executable": lines[0],
                "version": lines[1],
                "prefix": lines[2],
                "base_prefix": lines[3],
                "in_venv": lines[2] != lines[3],
            }
        except Exception as e:
            print_error(f"Không thể lấy thông tin Python: {e}")
            return {}

    def create_optimal_settings(self) -> dict[str, Any]:
        """Tạo cấu hình VS Code tối ưu"""
        # Đường dẫn Python paths cho PYTHONPATH
        python_paths = [
            "${workspaceFolder}/zeta_vn",
            "${workspaceFolder}/zeta_vn/app",
            "${workspaceFolder}/zeta_vn/core",
            "${workspaceFolder}/zeta_vn/data",
        ]

        # Cấu hình tối ưu
        settings = {
            # Python Configuration
            "python.languageServer": "Pylance",
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.terminal.activateEnvironment": True,
            "python.analysis.autoSearchPaths": True,
            "python.analysis.autoImportCompletions": True,
            "python.analysis.typeCheckingMode": "strict",
            "python.analysis.extraPaths": python_paths,
            "python.linting.enabled": False,  # Sử dụng Ruff thay vì pylint
            # Testing Configuration
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "python.testing.cwd": "${workspaceFolder}",
            "python.testing.autoTestDiscoverOnSaveEnabled": True,
            # Ruff Configuration (thay thế flake8, black, isort)
            "ruff.enable": True,
            "ruff.importStrategy": "useBundled",
            "ruff.lint.enable": True,
            "ruff.format.enable": True,
            "ruff.organizeImports": True,
            "ruff.fixAll": True,
            "ruff.showSyntaxErrors": True,
            "ruff.nativeServer": True,
            # Terminal Environment - Cross-platform
            "terminal.integrated.env.linux": {
                "PYTHONPATH": ":".join(python_paths).replace("${workspaceFolder}", str(self.workspace_root))
            },
            "terminal.integrated.env.osx": {
                "PYTHONPATH": ":".join(python_paths).replace("${workspaceFolder}", str(self.workspace_root))
            },
            "terminal.integrated.env.windows": {
                "PYTHONPATH": ";".join(python_paths).replace("${workspaceFolder}", str(self.workspace_root))
            },
            # Language-specific settings
            "[python]": {
                "editor.defaultFormatter": None,  # Dùng Ruff
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.organizeImports": "explicit",
                    "source.fixAll.ruff": "explicit",
                },
            },
            # Editor Configuration
            "editor.fontFamily": "'Cascadia Code', Consolas, monospace",
            "editor.fontSize": 14,
            "editor.fontLigatures": True,
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "editor.rulers": [88, 120],
            "editor.wordWrap": "bounded",
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll": "explicit",
                "source.organizeImports": "explicit",
            },
            # File exclusions - Tối ưu hiệu năng
            "files.exclude": {
                "**/.git": True,
                "**/.venv": True,
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/.mypy_cache": True,
                "**/.ruff_cache": True,
                "**/*.pyc": True,
            },
            # Watcher exclude để nhẹ CPU
            "files.watcherExclude": {
                "**/node_modules/**": True,
                "**/dist/**": True,
                "**/build/**": True,
                "**/.venv/**": True,
            },
            # Search exclusions
            "search.exclude": {
                "**/node_modules": True,
                "**/.venv": True,
                "**/venv": True,
                "**/.git": True,
                "**/dist": True,
                "**/build": True,
                "**/*.pyc": True,
                "**/__pycache__": True,
            },
            # Copilot Configuration
            "github.copilot.inlineSuggest.enable": True,
            "github.copilot.editor.enableAutoCompletions": True,
            "chat.extensionTools.enabled": True,
            "chat.implicitContext.suggestedContext": True,
            "chat.promptFiles": True,
            # Git configuration
            "git.ignoreLimitWarning": True,
        }

        return settings

    def backup_current_settings(self) -> Path | None:
        """Backup cấu hình hiện tại"""
        if self.settings_file.exists():
            backup_file = self.settings_file.parent / f"settings.json.backup_{os.getpid()}"
            try:
                backup_file.write_text(self.settings_file.read_text(encoding="utf-8"), encoding="utf-8")
                print_success(f"Backup created: {backup_file}")
                return backup_file
            except Exception as e:
                print_error(f"Không thể tạo backup: {e}")
        return None

    def write_settings(self, settings: dict[str, Any]) -> bool:
        """Ghi cấu hình vào file"""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print_success(f"Settings written to: {self.settings_file}")
            return True
        except Exception as e:
            print_error(f"Không thể ghi settings: {e}")
            return False

    def verify_configuration(self) -> bool:
        """Xác minh cấu hình đã được áp dụng"""
        print_info("Đang xác minh cấu hình...")

        # Test Python import
        try:
            result = subprocess.run(
                [
                    str(self.python_exe),
                    "-c",
                    "import sys; print('Python OK'); import zeta_vn; print('Import OK')",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print_success("Python interpreter và imports hoạt động")
                return True
            else:
                print_error(f"Import test failed: {result.stderr}")
                return False
        except Exception as e:
            print_error(f"Verification failed: {e}")
            return False

    def show_summary(self, python_info: dict[str, Any]) -> None:
        """Hiển thị tổng kết"""
        if RICH_AVAILABLE:
            table = Table(title="🎯 VS Code Configuration Summary")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Workspace", str(self.workspace_root))
            table.add_row("Python Executable", str(self.python_exe))
            table.add_row("Python Version", python_info.get("version", "Unknown"))
            table.add_row("Virtual Env Active", str(python_info.get("in_venv", False)))
            table.add_row("Settings File", str(self.settings_file))

            console.print(table)
        else:
            print("\n🎯 VS Code Configuration Summary:")
            print(f"  Workspace: {self.workspace_root}")
            print(f"  Python Executable: {self.python_exe}")
            print(f"  Python Version: {python_info.get('version', 'Unknown')}")
            print(f"  Virtual Env Active: {python_info.get('in_venv', False)}")
            print(f"  Settings File: {self.settings_file}")

    def run(self) -> bool:
        """Chạy quá trình cài lại đường dẫn VS Code"""
        if RICH_AVAILABLE:
            rprint("\n[bold green]🔧 VS CODE PATH INSTALLER FOR ZETA[/bold green]")
        else:
            print("\n🔧 VS CODE PATH INSTALLER FOR ZETA")

        # 1. Kiểm tra điều kiện tiên quyết
        if not self.check_prerequisites():
            print_error("Điều kiện tiên quyết không đạt. Vui lòng sửa các vấn đề trên.")
            return False

        # 2. Lấy thông tin Python hiện tại
        python_info = self.get_current_python_info()
        if not python_info:
            return False

        # 3. Backup cấu hình hiện tại
        self.backup_current_settings()

        # 4. Tạo cấu hình tối ưu
        print_info("Đang tạo cấu hình VS Code tối ưu...")
        optimal_settings = self.create_optimal_settings()

        # 5. Ghi cấu hình
        if not self.write_settings(optimal_settings):
            return False

        # 6. Xác minh
        if not self.verify_configuration():
            print_warning("Xác minh có vấn đề - có thể cần restart VS Code")

        # 7. Hiển thị tổng kết
        self.show_summary(python_info)

        # 8. Hướng dẫn tiếp theo
        if RICH_AVAILABLE:
            panel = Panel(
                "[bold green]✅ CÀI ĐẶT HOÀN THÀNH![/bold green]\n\n"
                "📋 Các bước tiếp theo:\n"
                "1. Restart VS Code hoàn toàn\n"
                "2. Ctrl+Shift+P → 'Python: Select Interpreter'\n"
                f"3. Chọn: {self.python_exe}\n"
                "4. Mở terminal mới và verify môi trường\n"
                "5. Test: python --version && python -c 'import zeta_vn'",
                title="🎉 Success",
                border_style="green",
            )
            console.print(panel)
        else:
            print("\n✅ CÀI ĐẶT HOÀN THÀNH!")
            print("\n📋 Các bước tiếp theo:")
            print("1. Restart VS Code hoàn toàn")
            print("2. Ctrl+Shift+P → 'Python: Select Interpreter'")
            print(f"3. Chọn: {self.python_exe}")
            print("4. Mở terminal mới và verify môi trường")
            print("5. Test: python --version && python -c 'import zeta_vn'")

        return True


def main() -> int:
    """Hàm main"""
    try:
        installer = VSCodePathInstaller()
        success = installer.run()
        return 0 if success else 1
    except KeyboardInterrupt:
        print_warning("\nBị hủy bởi người dùng")
        return 130
    except Exception as e:
        print_error(f"Lỗi không mong đợi: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
