#!/usr/bin/env python3
"""
Script kiểm tra và verify cấu hình VS Code sau khi cài lại đường dẫn
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

# Constants
PYTHON_INTERPRETER_PATH_KEY = "python.defaultInterpreterPath"
PYTHON_TERMINAL_ACTIVATE_KEY = "python.terminal.activateEnvironment"
PYTHON_ANALYSIS_PATHS_KEY = "python.analysis.extraPaths"
PYTHON_TESTING_PYTEST_KEY = "python.testing.pytestEnabled"

try:
    from rich import print as rprint
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    rprint = None
    console = None
    Panel = None
    Table = None


def print_status(status: str, message: str) -> None:
    """Print status với màu sắc"""
    if RICH_AVAILABLE:
        if status == "success":
            rprint(f"[green]✅ {message}[/green]")
        elif status == "warning":
            rprint(f"[yellow]⚠️ {message}[/yellow]")
        elif status == "error":
            rprint(f"[red]❌ {message}[/red]")
        else:
            rprint(f"[blue]ℹ️ {message}[/blue]")
    else:
        symbols = {"success": "✅", "warning": "⚠️", "error": "❌", "info": "ℹ️"}
        print(f"{symbols.get(status, 'ℹ️')} {message}")


def verify_vscode_paths() -> dict[str, Any]:
    """Verify toàn bộ cấu hình VS Code paths"""

    if RICH_AVAILABLE:
        rprint("\n[bold blue]🔍 VERIFYING VS CODE CONFIGURATION[/bold blue]")
    else:
        print("\n🔍 VERIFYING VS CODE CONFIGURATION")

    results = {
        "workspace": {"status": "unknown", "details": {}},
        "venv": {"status": "unknown", "details": {}},
        "python": {"status": "unknown", "details": {}},
        "settings": {"status": "unknown", "details": {}},
        "imports": {"status": "unknown", "details": {}},
        "extensions": {"status": "unknown", "details": {}},
    }

    workspace_root = Path.cwd()
    vscode_dir = workspace_root / ".vscode"
    venv_dir = workspace_root / ".venv"

    # 1. Kiểm tra Workspace
    print_status("info", "Kiểm tra workspace structure...")
    if workspace_root.exists() and (workspace_root / "pyproject.toml").exists():
        results["workspace"]["status"] = "success"
        results["workspace"]["details"] = {
            "root": str(workspace_root),
            "has_pyproject": True,
            "has_vscode": vscode_dir.exists(),
        }
        print_status("success", f"Workspace root: {workspace_root}")
    else:
        results["workspace"]["status"] = "error"
        print_status("error", "Workspace structure không hợp lệ")

    # 2. Kiểm tra Virtual Environment
    print_status("info", "Kiểm tra virtual environment...")
    python_exe = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    if venv_dir.exists() and python_exe.exists():
        try:
            result = subprocess.run(
                [
                    str(python_exe),
                    "-c",
                    "import sys; print(sys.executable); print(sys.version); print(sys.prefix != sys.base_prefix)",
                ],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )

            lines = result.stdout.strip().split("\n")
            results["venv"]["status"] = "success"
            results["venv"]["details"] = {
                "path": str(venv_dir),
                "python_exe": lines[0],
                "version": lines[1],
                "active": lines[2] == "True",
            }
            print_status("success", f"Virtual environment: {venv_dir}")
            print_status("success", f"Python: {lines[1]}")

        except Exception as e:
            results["venv"]["status"] = "error"
            results["venv"]["details"] = {"error": str(e)}
            print_status("error", f"Virtual environment lỗi: {e}")
    else:
        results["venv"]["status"] = "error"
        print_status("error", "Virtual environment không tồn tại")

    # 3. Kiểm tra Python Environment
    print_status("info", "Kiểm tra Python environment hiện tại...")
    try:
        current_python = sys.executable
        venv_active = hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)

        results["python"]["status"] = "success" if venv_active else "warning"
        results["python"]["details"] = {
            "executable": current_python,
            "version": sys.version,
            "venv_active": venv_active,
            "prefix": sys.prefix,
        }

        if venv_active:
            print_status("success", f"Python từ venv: {current_python}")
        else:
            print_status("warning", f"Python global: {current_python}")

    except Exception as e:
        results["python"]["status"] = "error"
        results["python"]["details"] = {"error": str(e)}
        print_status("error", f"Python environment lỗi: {e}")

    # 4. Kiểm tra VS Code Settings
    print_status("info", "Kiểm tra VS Code settings...")
    settings_file = vscode_dir / "settings.json"

    if settings_file.exists():
        try:
            with open(settings_file, encoding="utf-8") as f:
                settings = json.load(f)

            # Kiểm tra các key quan trọng
            important_keys = [
                "python.defaultInterpreterPath",
                "python.terminal.activateEnvironment",
                "python.analysis.extraPaths",
                "python.testing.pytestEnabled",
            ]

            found_keys = {}
            for key in important_keys:
                found_keys[key] = key in settings

            results["settings"]["status"] = "success"
            results["settings"]["details"] = {
                "file_exists": True,
                "keys_found": found_keys,
                "interpreter_path": settings.get("python.defaultInterpreterPath"),
                "extra_paths": settings.get("python.analysis.extraPaths", []),
            }

            print_status("success", f"Settings file: {settings_file}")
            if settings.get("python.defaultInterpreterPath"):
                print_status("success", f"Interpreter path: {settings['python.defaultInterpreterPath']}")

        except Exception as e:
            results["settings"]["status"] = "error"
            results["settings"]["details"] = {"error": str(e)}
            print_status("error", f"Settings file lỗi: {e}")
    else:
        results["settings"]["status"] = "error"
        print_status("error", "Settings file không tồn tại")

    # 5. Kiểm tra Imports
    print_status("info", "Kiểm tra Python imports...")
    try:
        # Test core imports
        import_tests = ["import sys", "import zeta_vn", "from pathlib import Path", "import json"]

        failed_imports = []
        for test in import_tests:
            try:
                # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removedtest)
            except Exception as e:
                failed_imports.append(f"{test}: {e}")

        if not failed_imports:
            results["imports"]["status"] = "success"
            results["imports"]["details"] = {"all_passed": True}
            print_status("success", "Tất cả imports hoạt động")
        else:
            results["imports"]["status"] = "warning"
            results["imports"]["details"] = {"failed": failed_imports}
            print_status("warning", f"Một số imports lỗi: {len(failed_imports)}")

    except Exception as e:
        results["imports"]["status"] = "error"
        results["imports"]["details"] = {"error": str(e)}
        print_status("error", f"Import test lỗi: {e}")

    # 6. Kiểm tra VS Code Extensions (nếu có thể)
    print_status("info", "Kiểm tra VS Code extensions...")
    try:
        result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            extensions = result.stdout.strip().split("\n")
            python_ext = any("python" in ext.lower() for ext in extensions)
            pylance_ext = any("pylance" in ext.lower() for ext in extensions)

            results["extensions"]["status"] = "success" if python_ext else "warning"
            results["extensions"]["details"] = {
                "total": len(extensions),
                "has_python": python_ext,
                "has_pylance": pylance_ext,
                "python_extensions": [ext for ext in extensions if "python" in ext.lower()],
            }

            if python_ext:
                print_status(
                    "success",
                    f"Python extensions: {len([e for e in extensions if 'python' in e.lower()])}",
                )
            else:
                print_status("warning", "Không tìm thấy Python extension")

        else:
            results["extensions"]["status"] = "warning"
            results["extensions"]["details"] = {"error": "VS Code command không available"}
            print_status("warning", "Không thể check VS Code extensions")

    except Exception as e:
        results["extensions"]["status"] = "warning"
        results["extensions"]["details"] = {"error": str(e)}
        print_status("warning", f"Extension check lỗi: {e}")

    return results


def display_summary(results: dict[str, Any]) -> None:
    """Hiển thị tổng kết kết quả"""

    if RICH_AVAILABLE:
        # Tạo bảng tổng kết
        table = Table(title="🎯 VS Code Configuration Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="white")
        table.add_column("Details", style="dim")

        for component, data in results.items():
            status = data["status"]

            # Icon và màu cho status
            if status == "success":
                status_text = "[green]✅ SUCCESS[/green]"
            elif status == "warning":
                status_text = "[yellow]⚠️ WARNING[/yellow]"
            elif status == "error":
                status_text = "[red]❌ ERROR[/red]"
            else:
                status_text = "[dim]❓ UNKNOWN[/dim]"

            # Chi tiết
            details = data.get("details", {})
            if isinstance(details, dict):
                detail_text = ", ".join([f"{k}: {v}" for k, v in details.items()][:2])
            else:
                detail_text = str(details)

            table.add_row(
                component.title(),
                status_text,
                detail_text[:50] + "..." if len(detail_text) > 50 else detail_text,
            )

        console.print(table)

        # Tính toán overall status
        statuses = [data["status"] for data in results.values()]
        success_count = statuses.count("success")
        total_count = len(statuses)

        if success_count == total_count:
            overall_status = "[bold green]🎉 EXCELLENT - All systems operational![/bold green]"
        elif success_count >= total_count * 0.8:
            overall_status = "[bold yellow]⚠️ GOOD - Minor issues need attention[/bold yellow]"
        else:
            overall_status = "[bold red]❌ POOR - Major issues need fixing[/bold red]"

        panel = Panel(
            f"{overall_status}\n\n"
            f"📊 Summary: {success_count}/{total_count} components working\n"
            f"🎯 Next: {'Restart VS Code và chọn Python interpreter' if success_count >= 4 else 'Fix critical issues first'}",
            title="Overall Status",
            border_style="green" if success_count >= 4 else "yellow",
        )
        console.print(panel)

    else:
        print("\n🎯 VS Code Configuration Status:")
        for component, data in results.items():
            status = data["status"]
            symbol = {"success": "✅", "warning": "⚠️", "error": "❌", "unknown": "❓"}[status]
            print(f"  {symbol} {component.title()}: {status.upper()}")


def main() -> int:
    """Main function"""
    try:
        results = verify_vscode_paths()
        display_summary(results)

        # Return code dựa trên kết quả
        statuses = [data["status"] for data in results.values()]
        success_count = statuses.count("success")

        if success_count >= len(statuses) * 0.8:
            return 0  # Success
        else:
            return 1  # Có vấn đề cần fix

    except KeyboardInterrupt:
        print_status("warning", "Bị hủy bởi người dùng")
        return 130
    except Exception as e:
        print_status("error", f"Lỗi không mong đợi: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
