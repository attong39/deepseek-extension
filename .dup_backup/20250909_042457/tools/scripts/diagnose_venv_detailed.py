#!/usr/bin/env python3
"""
Script chẩn đoán chi tiết môi trường ảo VS Code
Phân tích nguyên nhân tại sao môi trường ảo vẫn chưa được kích hoạt đúng cách
"""

import os
import subprocess
import sys
from pathlib import Path
import Exception
import e
import enumerate
import ext
import f
import i
import j
import len
import line
import open
import p
import print
import range
import req_ext


def check_python_interpreter():
    """Kiểm tra Python interpreter hiện tại."""
    print("🐍 PYTHON INTERPRETER ANALYSIS")
    print("=" * 50)

    print(f"sys.executable: {sys.executable}")
    print(f"sys.prefix: {sys.prefix}")
    print(f"sys.base_prefix: {sys.base_prefix}")
    print(f"Virtual env active: {sys.prefix != sys.base_prefix}")
    print(f"Python version: {sys.version}")

    # Kiểm tra VIRTUAL_ENV
    virtual_env = os.environ.get("VIRTUAL_ENV")
    print(f"VIRTUAL_ENV: {virtual_env}")

    # Kiểm tra PATH
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    python_paths = [p for p in path_entries if "python" in p.lower() or "venv" in p.lower()]
    print(f"Python-related PATH entries: {len(python_paths)}")
    for p in python_paths[:5]:  # Hiển thị 5 đầu tiên
        print(f"  {p}")


def check_vscode_settings():
    """Kiểm tra cấu hình VS Code."""
    print("\n📝 VS CODE SETTINGS ANALYSIS")
    print("=" * 50)

    workspace_root = Path.cwd()
    settings_file = workspace_root / ".vscode" / "settings.json"

    if not settings_file.exists():
        print("❌ .vscode/settings.json không tồn tại!")
        return

    try:
        # VS Code settings.json hỗ trợ comments (JSONC)
        # Cần xử lý đặc biệt
        with open(settings_file, encoding="utf-8") as f:
            content = f.read()

        print(f"✅ Settings file exists: {settings_file}")
        print(f"File size: {len(content)} characters")

        # Tìm python.defaultInterpreterPath
        if "python.defaultInterpreterPath" in content:
            print("✅ python.defaultInterpreterPath được cấu hình")

            # Extract the relevant lines
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "python.defaultInterpreterPath" in line:
                    print(f"  Line {i + 1}: {line.strip()}")
                    # Show next few lines for context
                    for j in range(1, 5):
                        if i + j < len(lines):
                            print(f"  Line {i + j + 1}: {lines[i + j].strip()}")
                    break
        else:
            print("❌ python.defaultInterpreterPath chưa được cấu hình")

    except Exception as e:
        print(f"❌ Lỗi đọc settings.json: {e}")


def check_terminal_integration():
    """Kiểm tra tích hợp terminal."""
    print("\n💻 TERMINAL INTEGRATION ANALYSIS")
    print("=" * 50)

    # Kiểm tra shell hiện tại
    print(f"Current shell: {os.environ.get('SHELL', 'Unknown')}")
    print(f"TERM: {os.environ.get('TERM', 'Unknown')}")
    print(f"VSCODE_SHELL_INTEGRATION: {os.environ.get('VSCODE_SHELL_INTEGRATION', 'Not set')}")

    # Kiểm tra PS1 (prompt)
    ps1 = os.environ.get("PS1", "")
    if ps1:
        print(f"PS1: {ps1}")

    # Kiểm tra PROMPT (Windows)
    prompt = os.environ.get("PROMPT", "")
    if prompt:
        print(f"PROMPT: {prompt}")


def check_extensions():
    """Kiểm tra VS Code extensions."""
    print("\n🔌 EXTENSIONS ANALYSIS")
    print("=" * 50)

    try:
        result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            extensions = result.stdout.strip().split("\n")
            python_extensions = [ext for ext in extensions if "python" in ext.lower()]

            print(f"Total extensions: {len(extensions)}")
            print(f"Python-related extensions: {len(python_extensions)}")

            for ext in python_extensions:
                print(f"  ✅ {ext}")

            # Kiểm tra extension quan trọng
            required_extensions = ["ms-python.python", "ms-python.vscode-pylance"]

            for req_ext in required_extensions:
                if req_ext in extensions:
                    print(f"  ✅ Required: {req_ext}")
                else:
                    print(f"  ❌ Missing: {req_ext}")

        else:
            print(f"❌ Lỗi lấy danh sách extensions: {result.stderr}")

    except Exception as e:
        print(f"❌ Lỗi kiểm tra extensions: {e}")


def check_workspace_trust():
    """Kiểm tra workspace trust."""
    print("\n🔒 WORKSPACE TRUST ANALYSIS")
    print("=" * 50)

    workspace_root = Path.cwd()
    print(f"Workspace root: {workspace_root}")

    # Kiểm tra file .vscode-trusted-domains.json (nếu có)
    trust_file = (
        Path.home()
        / "AppData"
        / "Roaming"
        / "Code"
        / "User"
        / "globalStorage"
        / "vscode-file-trust"
        / "trusted-domains.json"
    )

    if trust_file.exists():
        print(f"✅ Trust file exists: {trust_file}")
    else:
        print("ℹ️  No specific trust file found")


def check_processes():
    """Kiểm tra processes liên quan."""
    print("\n⚙️  PROCESS ANALYSIS")
    print("=" * 50)

    try:
        # Kiểm tra VS Code processes
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                'Get-Process | Where-Object {$_.ProcessName -like "*code*" -or $_.ProcessName -like "*python*"} | Select-Object ProcessName, Id, CPU | Format-Table -AutoSize',
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("VS Code & Python processes:")
            print(result.stdout)
        else:
            print(f"❌ Lỗi kiểm tra processes: {result.stderr}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")


def main():
    """Chạy tất cả kiểm tra."""
    print("🔍 CHẨN ĐOÁN CHI TIẾT MÔI TRƯỜNG ẢO VS CODE")
    print("=" * 60)
    print(f"Thời gian: {os.environ.get('DATE', 'Unknown')}")
    print(f"Workspace: {Path.cwd()}")
    print()

    check_python_interpreter()
    check_vscode_settings()
    check_terminal_integration()
    check_extensions()
    check_workspace_trust()
    check_processes()

    print("\n" + "=" * 60)
    print("🎯 KẾT LUẬN VÀ KHUYẾN NGHỊ")
    print("=" * 60)

    # Phân tích và đưa ra khuyến nghị
    virtual_env = os.environ.get("VIRTUAL_ENV")
    is_venv_active = sys.prefix != sys.base_prefix

    if virtual_env and is_venv_active:
        print("✅ Môi trường ảo ĐÃ HOẠT ĐỘNG ở cấp Python!")
        print("❓ Vấn đề có thể là VS Code chưa nhận diện đúng interpreter")
        print("\n📋 KHUYẾN NGHỊ:")
        print("1. Restart VS Code hoàn toàn")
        print("2. Ctrl+Shift+P → 'Python: Select Interpreter'")
        print(f"3. Chọn: {sys.executable}")
        print("4. Mở terminal mới và kiểm tra lại")
    else:
        print("❌ Môi trường ảo CHƯA hoạt động đúng")
        print("\n📋 KHUYẾN NGHỊ:")
        print("1. Kích hoạt lại: .venv\\Scripts\\Activate.ps1")
        print("2. Kiểm tra execution policy")
        print("3. Tạo lại môi trường ảo nếu cần")


if __name__ == "__main__":
    main()
