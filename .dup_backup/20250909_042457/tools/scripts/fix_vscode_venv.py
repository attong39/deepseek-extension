#!/usr/bin/env python3
"""
Script khắc phục lỗi môi trường ảo VS Code

Kiểm tra và sửa các vấn đề phổ biến với môi trường ảo trong VS Code:
- Kích hoạt môi trường ảo
- Cập nhật Python interpreter path
- Kiểm tra PYTHONPATH
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import Exception
import dict
import e
import f
import isinstance
import open
import print
import str


def main():
    """Chạy các bước khắc phục môi trường ảo."""
    workspace_root = Path(__file__).parent.parent
    venv_path = workspace_root / ".venv"

    print("🔍 Kiểm tra môi trường ảo VS Code...")
    print(f"Workspace: {workspace_root}")
    print(f"Virtual env: {venv_path}")

    # 1. Kiểm tra môi trường ảo tồn tại
    if not venv_path.exists():
        print("❌ Môi trường ảo không tồn tại!")
        print("Chạy: uv venv để tạo môi trường ảo")
        return 1

    # 2. Kiểm tra Python executable
    if os.name == "nt":  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # Linux/macOS
        python_exe = venv_path / "bin" / "python"

    if not python_exe.exists():
        print(f"❌ Python executable không tồn tại: {python_exe}")
        return 1

    print(f"✅ Python executable: {python_exe}")

    # 3. Test import các package chính
    print("\n🧪 Test import packages...")
    try:
        result = subprocess.run(
            [
                str(python_exe),
                "-c",
                "import fastapi, uvicorn, pydantic; print('✅ Core packages OK')",
            ],
            capture_output=True,
            text=True,
            cwd=workspace_root,
        )

        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ Import error: {result.stderr}")
            print("Chạy: uv sync để cài đặt dependencies")
            return 1
    except Exception as e:
        print(f"❌ Lỗi test import: {e}")
        return 1

    # 4. Kiểm tra VS Code settings
    vscode_settings = workspace_root / ".vscode" / "settings.json"
    if vscode_settings.exists():
        print(f"\n📝 Kiểm tra VS Code settings: {vscode_settings}")
        try:
            with open(vscode_settings, encoding="utf-8") as f:
                settings = json.load(f)

            # Kiểm tra python.defaultInterpreterPath
            interpreter_config = settings.get("python.defaultInterpreterPath", {})
            if isinstance(interpreter_config, dict):
                windows_path = interpreter_config.get("windows")
                if windows_path:
                    print(f"✅ Windows interpreter path: {windows_path}")
                else:
                    print("⚠️  Windows interpreter path chưa được cấu hình")
            else:
                print(f"⚠️  Interpreter path: {interpreter_config}")

        except Exception as e:
            print(f"❌ Lỗi đọc settings.json: {e}")

    # 5. Kiểm tra PYTHONPATH
    print("\n🛤️  Kiểm tra PYTHONPATH...")
    try:
        result = subprocess.run(
            [
                str(python_exe),
                "-c",
                "import sys; print('Python paths:'); [print(f'  {p}') for p in sys.path if 'zeta' in p]",
            ],
            capture_output=True,
            text=True,
            cwd=workspace_root,
        )

        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ PYTHONPATH error: {result.stderr}")

    except Exception as e:
        print(f"❌ Lỗi kiểm tra PYTHONPATH: {e}")

    print("\n✅ Hoàn thành kiểm tra môi trường ảo!")
    print("\n📋 Các bước tiếp theo:")
    print("1. Restart VS Code")
    print("2. Ctrl+Shift+P → 'Python: Select Interpreter'")
    print(f"3. Chọn: {python_exe}")
    print("4. Mở terminal mới trong VS Code")

    return 0


if __name__ == "__main__":
    sys.exit(main())
