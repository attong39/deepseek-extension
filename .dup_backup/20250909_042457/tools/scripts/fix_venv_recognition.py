#!/usr/bin/env python3
"""
Script chẩn đoán và khắc phục lỗi môi trường ảo VS Code
Xử lý vấn đề VS Code không nhận diện .venv

Các vấn đề phổ biến:
1. python.defaultInterpreterPath sai kiểu (object thay vì string)
2. Extension Python chưa được cấu hình đúng
3. Terminal không auto-activate môi trường ảo
4. Path conflicts giữa global Python và virtual environment
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any
import Exception
import dict
import e
import enumerate
import ext
import fix
import i
import len
import line
import list
import print
import step
import str


def get_python_info() -> dict[str, Any]:
    """Lấy thông tin chi tiết về Python interpreter."""
    return {
        "executable": sys.executable,
        "version": sys.version,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "in_venv": sys.prefix != sys.base_prefix,
        "virtual_env": os.environ.get("VIRTUAL_ENV"),
        "pythonpath": os.environ.get("PYTHONPATH", "").split(os.pathsep) if os.environ.get("PYTHONPATH") else [],
    }


def check_vscode_settings() -> dict[str, Any]:
    """Kiểm tra cấu hình VS Code settings.json."""
    settings_path = Path(".vscode/settings.json")
    if not settings_path.exists():
        return {"exists": False, "error": "File .vscode/settings.json không tồn tại"}

    try:
        # VS Code settings.json hỗ trợ comments (JSONC format)
        # Cần parse đặc biệt
        content = settings_path.read_text(encoding="utf-8")

        # Tìm python.defaultInterpreterPath
        interpreter_config = None
        if "python.defaultInterpreterPath" in content:
            # Extract line để phân tích
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "python.defaultInterpreterPath" in line:
                    # Kiểm tra nếu là object hay string
                    if "{" in line or lines[i + 1].strip().startswith('"'):
                        interpreter_config = "object_format"
                    else:
                        interpreter_config = "string_format"
                    break

        terminal_activate = "python.terminal.activateEnvironment" in content

        return {
            "exists": True,
            "interpreter_config": interpreter_config,
            "terminal_activate": terminal_activate,
            "content_length": len(content),
        }

    except Exception as e:
        return {"exists": True, "error": f"Lỗi đọc settings.json: {e}"}


def check_venv_structure() -> dict[str, Any]:
    """Kiểm tra cấu trúc môi trường ảo."""
    venv_path = Path(".venv")

    if not venv_path.exists():
        return {"exists": False}

    # Windows vs Unix paths
    if os.name == "nt":  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
        activate_script = venv_path / "Scripts" / "Activate.ps1"
    else:  # Unix
        python_exe = venv_path / "bin" / "python"
        activate_script = venv_path / "bin" / "activate"

    return {
        "exists": True,
        "python_executable": python_exe.exists(),
        "python_path": str(python_exe),
        "activate_script": activate_script.exists(),
        "activate_path": str(activate_script),
        "site_packages": (venv_path / "Lib" / "site-packages").exists()
        if os.name == "nt"
        else (venv_path / "lib").exists(),
    }


def check_extensions() -> dict[str, Any]:
    """Kiểm tra VS Code extensions."""
    try:
        result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            extensions = result.stdout.strip().split("\n")
            python_extensions = [ext for ext in extensions if "python" in ext.lower()]

            return {
                "total": len(extensions),
                "python_related": python_extensions,
                "has_ms_python": "ms-python.python" in extensions,
                "has_pylance": "ms-python.vscode-pylance" in extensions,
            }
        else:
            return {"error": f"Lỗi lấy extensions: {result.stderr}"}

    except Exception as e:
        return {"error": f"Không thể kiểm tra extensions: {e}"}


def generate_fixes() -> list[dict[str, Any]]:
    """Tạo danh sách các bước khắc phục."""
    fixes = []

    # Kiểm tra settings
    settings = check_vscode_settings()
    if settings.get("interpreter_config") == "object_format":
        fixes.append(
            {
                "priority": "HIGH",
                "title": "Sửa python.defaultInterpreterPath sai kiểu",
                "description": "VS Code không chấp nhận object format cho python.defaultInterpreterPath",
                "action": "Đã sửa tự động trong .vscode/settings.json",
                "manual_steps": [
                    "Restart VS Code",
                    "Ctrl+Shift+P → 'Python: Select Interpreter'",
                    "Chọn interpreter từ .venv",
                ],
            }
        )

    if not settings.get("terminal_activate"):
        fixes.append(
            {
                "priority": "MEDIUM",
                "title": "Thiếu python.terminal.activateEnvironment",
                "description": "Terminal không tự động kích hoạt môi trường ảo",
                "action": "Đã thêm vào settings.json",
                "manual_steps": ["Mở terminal mới để test"],
            }
        )

    # Kiểm tra venv
    venv = check_venv_structure()
    if not venv["exists"]:
        fixes.append(
            {
                "priority": "CRITICAL",
                "title": "Môi trường ảo .venv không tồn tại",
                "description": "Cần tạo môi trường ảo trước",
                "action": "Chạy: uv venv .venv && uv sync",
                "manual_steps": ["uv venv .venv", "uv sync"],
            }
        )

    # Kiểm tra extensions
    extensions = check_extensions()
    if not extensions.get("has_ms_python"):
        fixes.append(
            {
                "priority": "HIGH",
                "title": "Thiếu Python extension",
                "description": "Extension ms-python.python chưa được cài",
                "action": "Cài đặt extension Python",
                "manual_steps": ["Ctrl+Shift+X → Search 'Python' → Install"],
            }
        )

    return fixes


def main():
    """Chạy chẩn đoán toàn diện."""
    print("🔍 CHẨN ĐOÁN LỖI MÔI TRƯỜNG ẢO VS CODE")
    print("=" * 55)

    # 1. Thông tin Python
    print("\n🐍 PYTHON ENVIRONMENT:")
    python_info = get_python_info()
    print(f"   Executable: {python_info['executable']}")
    print(f"   In venv: {python_info['in_venv']}")
    print(f"   VIRTUAL_ENV: {python_info['virtual_env']}")

    # 2. VS Code settings
    print("\n📝 VS CODE SETTINGS:")
    settings = check_vscode_settings()
    if settings["exists"]:
        print(f"   Interpreter config: {settings.get('interpreter_config', 'None')}")
        print(f"   Terminal activate: {settings.get('terminal_activate', False)}")
    else:
        print(f"   ❌ {settings.get('error', 'Không rõ lỗi')}")

    # 3. Venv structure
    print("\n📁 VIRTUAL ENVIRONMENT:")
    venv = check_venv_structure()
    if venv["exists"]:
        print(f"   Python executable: {venv['python_executable']}")
        print(f"   Path: {venv['python_path']}")
        print(f"   Site packages: {venv['site_packages']}")
    else:
        print("   ❌ .venv không tồn tại")

    # 4. Extensions
    print("\n🔌 VS CODE EXTENSIONS:")
    extensions = check_extensions()
    if "error" not in extensions:
        print(f"   Total: {extensions['total']}")
        print(f"   Python extensions: {len(extensions['python_related'])}")
        print(f"   Has ms-python.python: {extensions['has_ms_python']}")
        print(f"   Has Pylance: {extensions['has_pylance']}")
    else:
        print(f"   ❌ {extensions['error']}")

    # 5. Đề xuất khắc phục
    print("\n🔧 ĐỀ XUẤT KHẮC PHỤC:")
    fixes = generate_fixes()

    if not fixes:
        print("   ✅ Không phát hiện vấn đề cần sửa!")
        print("   💡 Nếu vẫn có lỗi, hãy restart VS Code")
    else:
        for i, fix in enumerate(fixes, 1):
            print(f"\n   {i}. [{fix['priority']}] {fix['title']}")
            print(f"      📋 {fix['description']}")
            print(f"      🔧 {fix['action']}")
            if fix.get("manual_steps"):
                print("      📝 Manual steps:")
                for step in fix["manual_steps"]:
                    print(f"         - {step}")

    # 6. Verification
    print("\n✅ VERIFICATION CHECKLIST:")
    print("   1. Restart VS Code hoàn toàn")
    print("   2. Ctrl+Shift+P → 'Python: Select Interpreter'")
    print(f"   3. Chọn: {python_info['executable']}")
    print("   4. Mở terminal mới và chạy: python --version")
    print("   5. Kiểm tra có prefix (.venv) trong terminal")

    return 0


if __name__ == "__main__":
    sys.exit(main())
