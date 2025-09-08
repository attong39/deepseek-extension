#!/usr/bin/env python3
"""
Script chẩn đoán lỗi VS Code extensions và môi trường
Phân tích các extension activation failed và vấn đề môi trường
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
import Exception
import ImportError
import PermissionError
import any
import config_file
import count
import d
import dirname
import e
import enumerate
import ext
import f
import fmt
import i
import item
import keyword
import len
import line
import lint
import list
import log_file
import max
import open
import package
import print
import sorted
import x


def check_vscode_logs():
    """Kiểm tra VS Code logs để tìm lỗi."""
    print("📋 VS CODE LOGS ANALYSIS")
    print("=" * 50)

    # VS Code logs location
    logs_base = Path.home() / "AppData" / "Roaming" / "Code" / "logs"

    if not logs_base.exists():
        print("❌ VS Code logs directory không tồn tại")
        return

    # Tìm thư mục log mới nhất
    log_dirs = [d for d in logs_base.iterdir() if d.is_dir()]
    if not log_dirs:
        print("❌ Không tìm thấy log directories")
        return

    latest_log = max(log_dirs, key=lambda x: x.stat().st_mtime)
    print(f"📁 Latest log directory: {latest_log}")

    # Kiểm tra extension host logs
    exthost_logs = list(latest_log.glob("**/exthost*.log"))
    if exthost_logs:
        print(f"🔍 Extension host logs found: {len(exthost_logs)}")

        for log_file in exthost_logs[:2]:  # Chỉ check 2 files mới nhất
            print(f"\n📄 Checking: {log_file.name}")
            try:
                with open(log_file, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Tìm errors
                    error_lines = [
                        line
                        for line in content.split("\n")
                        if any(keyword in line.lower() for keyword in ["error", "failed", "exception", "timeout"])
                    ]

                    if error_lines:
                        print(f"❌ Found {len(error_lines)} error lines:")
                        for i, line in enumerate(error_lines[-5:]):  # 5 lỗi cuối
                            print(f"  {i + 1}. {line[:100]}...")
                    else:
                        print("✅ No obvious errors found")

            except Exception as e:
                print(f"❌ Error reading log: {e}")


def check_extension_status():
    """Kiểm tra trạng thái extensions."""
    print("\n🔌 EXTENSION STATUS ANALYSIS")
    print("=" * 50)

    try:
        # Lấy danh sách extensions
        result = subprocess.run(
            ["code", "--list-extensions", "--show-versions"],
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0:
            extensions = result.stdout.strip().split("\n")
            print(f"📦 Total extensions: {len(extensions)}")

            # Phân loại extensions
            python_exts = [ext for ext in extensions if "python" in ext.lower()]
            ms_exts = [ext for ext in extensions if ext.startswith("ms-")]

            print(f"🐍 Python extensions: {len(python_exts)}")
            print(f"🏢 Microsoft extensions: {len(ms_exts)}")

            # Kiểm tra conflict potential
            print("\n🔍 Potential conflicts:")
            formatters = [
                ext
                for ext in extensions
                if any(fmt in ext.lower() for fmt in ["formatter", "format", "prettier", "black"])
            ]
            linters = [
                ext for ext in extensions if any(lint in ext.lower() for lint in ["lint", "pylint", "ruff", "flake8"])
            ]

            print(f"📝 Formatters: {len(formatters)}")
            for fmt in formatters:
                print(f"  - {fmt}")

            print(f"🔍 Linters: {len(linters)}")
            for lint in linters:
                print(f"  - {lint}")

        else:
            print(f"❌ Error getting extensions: {result.stderr}")

    except Exception as e:
        print(f"❌ Error checking extensions: {e}")


def check_workspace_specific():
    """Kiểm tra workspace-specific issues."""
    print("\n📁 WORKSPACE SPECIFIC ANALYSIS")
    print("=" * 50)

    workspace_root = Path.cwd()

    # Kiểm tra .vscode directory
    vscode_dir = workspace_root / ".vscode"
    if vscode_dir.exists():
        print("✅ .vscode directory exists")

        config_files = list(vscode_dir.glob("*.json"))
        print(f"📄 Config files: {len(config_files)}")

        for config_file in config_files:
            print(f"  📄 {config_file.name}: {config_file.stat().st_size} bytes")

            # Kiểm tra JSON syntax
            try:
                if config_file.name == "settings.json":
                    # JSONC format (with comments)
                    with open(config_file, encoding="utf-8") as f:
                        content = f.read()
                        if "//" in content or "/*" in content:
                            print("    ℹ️  JSONC format (with comments)")
                        else:
                            json.loads(content)
                            print("    ✅ Valid JSON")
                else:
                    with open(config_file, encoding="utf-8") as f:
                        json.load(f)
                    print("    ✅ Valid JSON")

            except json.JSONDecodeError as e:
                print(f"    ❌ JSON syntax error: {e}")
            except Exception as e:
                print(f"    ⚠️  Error reading: {e}")

    # Kiểm tra large directories có thể gây chậm
    large_dirs = []
    for item in workspace_root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            try:
                file_count = len(list(item.rglob("*")))
                if file_count > 1000:
                    large_dirs.append((item.name, file_count))
            except PermissionError:
                pass

    if large_dirs:
        print("\n📊 Large directories (>1000 files):")
        for dirname, count in sorted(large_dirs, key=lambda x: x[1], reverse=True)[:5]:
            print(f"  📁 {dirname}: {count:,} files")


def check_system_resources():
    """Kiểm tra system resources."""
    print("\n💻 SYSTEM RESOURCES ANALYSIS")
    print("=" * 50)

    try:
        # Memory usage
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                'Get-Process | Where-Object {$_.ProcessName -like "*code*"} | Measure-Object WorkingSet -Sum | Select-Object Count, @{Name="MemoryMB";Expression={[math]::Round($_.Sum/1MB,2)}}',
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("🔍 VS Code memory usage:")
            print(result.stdout.strip())

        # CPU usage
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                'Get-Process | Where-Object {$_.ProcessName -like "*code*" -and $_.CPU -gt 1} | Select-Object ProcessName, CPU, WorkingSet | Format-Table -AutoSize',
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("\n⚡ High CPU VS Code processes:")
            print(result.stdout.strip())

    except Exception as e:
        print(f"❌ Error checking system resources: {e}")


def check_python_environment():
    """Kiểm tra Python environment chi tiết."""
    print("\n🐍 PYTHON ENVIRONMENT ANALYSIS")
    print("=" * 50)

    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Virtual env: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

    # Kiểm tra important packages
    important_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "pytest",
        "ruff",
        "mypy",
        "black",
    ]

    print("\n📦 Package status:")
    for package in important_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Not found")
        except Exception as e:
            print(f"  ⚠️  {package} - Error: {e}")


def generate_recommendations():
    """Tạo khuyến nghị dựa trên phân tích."""
    print("\n💡 RECOMMENDATIONS")
    print("=" * 50)

    print("📋 Immediate actions:")
    print("1. 🔄 Restart VS Code completely")
    print("2. 🔌 Disable/re-enable problematic extensions")
    print("3. 🧹 Clear VS Code workspace cache")
    print("4. 🐍 Verify Python interpreter selection")

    print("\n🛠️  Commands to run:")
    print("# Clear workspace cache")
    print("code --user-data-dir temp_profile --extensions-dir temp_extensions .")
    print("")
    print("# Reset extension host")
    print("Ctrl+Shift+P → 'Developer: Restart Extension Host'")
    print("")
    print("# Verify Python interpreter")
    print("Ctrl+Shift+P → 'Python: Select Interpreter'")


def main():
    """Chạy tất cả kiểm tra."""
    print("🔍 VS CODE EXTENSION & ENVIRONMENT DIAGNOSTIC")
    print("=" * 60)
    print(f"Workspace: {Path.cwd()}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    check_python_environment()
    check_extension_status()
    check_workspace_specific()
    check_system_resources()
    check_vscode_logs()
    generate_recommendations()

    print(f"\n{'=' * 60}")
    print("🎯 DIAGNOSTIC COMPLETED")
    print("Check recommendations above for next steps.")


if __name__ == "__main__":
    main()
