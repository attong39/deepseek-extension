#!/usr/bin/env python3
"""
Script verification cấu hình VS Code - đơn giản và hiệu quả
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def check_workspace() -> dict[str, Any]:
    """Kiểm tra workspace structure"""
    workspace_root = Path.cwd()
    return {
        "status": "success" if (workspace_root / "pyproject.toml").exists() else "error",
        "path": str(workspace_root),
        "has_pyproject": (workspace_root / "pyproject.toml").exists(),
        "has_vscode": (workspace_root / ".vscode").exists(),
    }


def check_virtual_env() -> dict[str, Any]:
    """Kiểm tra virtual environment"""
    venv_dir = Path.cwd() / ".venv"
    python_exe = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    if not (venv_dir.exists() and python_exe.exists()):
        return {"status": "error", "reason": "Virtual environment không tồn tại"}

    try:
        result = subprocess.run(
            [
                str(python_exe),
                "-c",
                "import sys; print(sys.executable); print(sys.version_info[:2]); print(sys.prefix != sys.base_prefix)",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )

        lines = result.stdout.strip().split("\n")
        return {
            "status": "success",
            "python_exe": lines[0],
            "version": lines[1],
            "is_venv": lines[2] == "True",
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_vscode_settings() -> dict[str, Any]:
    """Kiểm tra VS Code settings"""
    settings_file = Path.cwd() / ".vscode" / "settings.json"

    if not settings_file.exists():
        return {"status": "error", "reason": "Settings file không tồn tại"}

    try:
        with open(settings_file, encoding="utf-8") as f:
            settings = json.load(f)

        required_keys = [
            "python.defaultInterpreterPath",
            "python.terminal.activateEnvironment",
            "python.analysis.extraPaths",
        ]

        missing_keys = [key for key in required_keys if key not in settings]
        interpreter_path = settings.get("python.defaultInterpreterPath", "")

        return {
            "status": "success" if not missing_keys else "warning",
            "interpreter_path": interpreter_path,
            "missing_keys": missing_keys,
            "total_settings": len(settings),
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_python_imports() -> dict[str, Any]:
    """Kiểm tra core Python imports"""
    test_imports = ["import sys", "import json", "from pathlib import Path", "import zeta_vn"]

    failed_imports: list[str] = []
    for test in test_imports:
        try:
            # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removedtest)
        except Exception as e:
            failed_imports.append(f"{test}: {str(e)}")

    return {
        "status": "success" if not failed_imports else "warning",
        "total_tests": len(test_imports),
        "failed_count": len(failed_imports),
        "failed_imports": failed_imports,
    }


def check_current_python() -> dict[str, Any]:
    """Kiểm tra Python hiện tại"""
    venv_active = hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)

    return {
        "status": "success" if venv_active else "warning",
        "executable": sys.executable,
        "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "venv_active": venv_active,
        "prefix": sys.prefix,
    }


def print_results(results: dict[str, dict[str, Any]]) -> None:
    """In kết quả verification"""
    print("🔍 VS CODE CONFIGURATION VERIFICATION")
    print("=" * 50)

    status_symbols = {"success": "✅", "warning": "⚠️", "error": "❌", "unknown": "❓"}

    for component, data in results.items():
        status = data.get("status", "unknown")
        symbol = status_symbols.get(status, "❓")
        print(f"\n{symbol} {component.upper().replace('_', ' ')}: {status.upper()}")

        # In chi tiết quan trọng
        if component == "workspace" and data.get("path"):
            print(f"   📁 Path: {data['path']}")
        elif component == "virtual_env" and data.get("python_exe"):
            print(f"   🐍 Python: {data['python_exe']}")
            print(f"   📦 Version: {data.get('version', 'Unknown')}")
        elif component == "vscode_settings" and data.get("interpreter_path"):
            print(f"   ⚙️ Interpreter: {data['interpreter_path']}")
        elif component == "python_imports" and data.get("failed_count", 0) > 0:
            print(f"   ❌ Failed: {data['failed_count']}/{data.get('total_tests', 0)}")
        elif component == "current_python":
            print(f"   🔧 Current: {data.get('executable', 'Unknown')}")
            print(f"   🔋 VEnv Active: {data.get('venv_active', False)}")

    # Tính toán overall status
    statuses = [data.get("status", "unknown") for data in results.values()]
    success_count = statuses.count("success")
    total_count = len(statuses)

    print(f"\n📊 SUMMARY: {success_count}/{total_count} components OK")

    if success_count == total_count:
        print("🎉 EXCELLENT - All systems operational!")
        print("✨ Next: Restart VS Code and select Python interpreter")
    elif success_count >= total_count * 0.8:
        print("⚠️ GOOD - Minor issues need attention")
        print("🔧 Next: Fix warnings and restart VS Code")
    else:
        print("❌ POOR - Major issues need fixing")
        print("🚨 Next: Fix critical errors first")


def main() -> int:
    """Main verification function"""
    try:
        # Chạy tất cả kiểm tra
        results = {
            "workspace": check_workspace(),
            "virtual_env": check_virtual_env(),
            "vscode_settings": check_vscode_settings(),
            "python_imports": check_python_imports(),
            "current_python": check_current_python(),
        }

        # In kết quả
        print_results(results)

        # Return code dựa trên kết quả
        statuses = [data.get("status", "unknown") for data in results.values()]
        success_count = statuses.count("success")

        return 0 if success_count >= len(statuses) * 0.8 else 1

    except KeyboardInterrupt:
        print("\n⚠️ Verification bị hủy bởi người dùng")
        return 130
    except Exception as e:
        print(f"\n❌ Lỗi không mong đợi: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
