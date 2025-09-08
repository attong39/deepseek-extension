from __future__ import annotations

import json
import re
from pathlib import Path
import f
import open
import print

"""
Script cập nhật đường dẫn cho các thư mục quan trọng trong dự án ZETA_VN.
Cập nhật: zeta_vn, .vscode, .venv, .github/.copilot
"""
PROJECT_ROOT = "e:/zeta"
PYTHON_EXE = "e:/zeta/.venv/Scripts/python.exe"
ZETA_VN_PATH = "e:/zeta/zeta_vn"
VSCODE_PATH = "e:/zeta/.vscode"
VENV_PATH = "e:/zeta/.venv"
COPILOT_PATH = "e:/zeta/.github/.copilot"


def update_vscode_settings() -> None:
    """Cập nhật VSCode settings.json với đường dẫn mới."""
    settings_file = Path(".vscode/settings.json")
    if not settings_file.exists():
        print(f"⚠️  {settings_file} không tồn tại")
        return
    print(f"🔧 Cập nhật {settings_file}...")
    with open(settings_file, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'"python\.defaultInterpreterPath":\s*"[^"]*"',
        '"python.defaultInterpreterPath": "./e:/zeta/.venv/Scripts/python.exe"',
        content,
    )
    content = re.sub(r'"zeta_vn":\s*"zeta_vn/\*"', '"zeta_vn": "e:/zeta/zeta_vn/*"', content)
    content = re.sub(r'"\.copilot":\s*"\.copilot/\*"', '".copilot": "e:/zeta/.github/.copilot/*"', content)
    with open(settings_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã cập nhật {settings_file}")


def update_pyproject_toml() -> None:
    """Cập nhật pyproject.toml với đường dẫn mới."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        print(f"⚠️  {pyproject_file} không tồn tại")
        return
    print(f"🔧 Cập nhật {pyproject_file}...")
    with open(pyproject_file, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'exclude = \[([^\]]*)"\.venv"([^\]]*)\]', r'exclude = [\1"e:/zeta/.venv"\2]', content)
    content = re.sub(r'source = \["zeta_vn"\]', 'source = ["e:/zeta/zeta_vn"]', content)
    content = re.sub(
        r'testpaths = \["tests", "zeta_vn/tests"\]',
        'testpaths = ["e:/zeta/tests", "e:/zeta/zeta_vn/tests"]',
        content,
    )
    with open(pyproject_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã cập nhật {pyproject_file}")


def update_copilot_config() -> None:
    """Cập nhật config cho .github/.copilot."""
    copilot_dir = Path(".github/.copilot")
    if not copilot_dir.exists():
        print(f"⚠️  {copilot_dir} không tồn tại")
        return
    print(f"🔧 Cập nhật cấu hình Copilot trong {copilot_dir}...")
    config_file = copilot_dir / "config.json"
    if config_file.exists():
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
        if "project_root" in config:
            config["project_root"] = "e:/zeta"
        if "zeta_vn_path" in config:
            config["zeta_vn_path"] = "e:/zeta/zeta_vn"
        if "vscode_path" in config:
            config["vscode_path"] = "e:/zeta/.vscode"
        if "venv_path" in config:
            config["venv_path"] = "e:/zeta/.venv"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã cập nhật {config_file}")
    vscode_integration_file = copilot_dir / "vscode_integration.json"
    if vscode_integration_file.exists():
        with open(vscode_integration_file, encoding="utf-8") as f:
            integration = json.load(f)
        if "workspace_folders" in integration:
            integration["workspace_folders"] = [{"name": "zeta", "uri": "file:///e:/zeta"}]
        if "python_paths" in integration:
            integration["python_paths"] = {
                "interpreter": "e:/zeta/.venv/Scripts/python.exe",
                "site_packages": "e:/zeta/.venv/Lib/site-packages",
            }
        with open(vscode_integration_file, "w", encoding="utf-8") as f:
            json.dump(integration, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã cập nhật {vscode_integration_file}")


def update_workspace_file() -> None:
    """Cập nhật zeta_vn.code-workspace với đường dẫn mới."""
    workspace_file = Path("zeta_vn.code-workspace")
    if not workspace_file.exists():
        print(f"⚠️  {workspace_file} không tồn tại")
        return
    print(f"🔧 Cập nhật {workspace_file}...")
    with open(workspace_file, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'"path":\s*"\."', '"path": "e:/zeta"', content)
    content = re.sub(
        r'"python\.defaultInterpreterPath":\s*"[^"]*"',
        '"python.defaultInterpreterPath": "e:/zeta/.venv/Scripts/python.exe"',
        content,
    )
    content = re.sub(
        r'"python\.terminal\.activateEnvironment":\s*\w+',
        '"python.terminal.activateEnvironment": true',
        content,
    )
    with open(workspace_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã cập nhật {workspace_file}")


def update_tasks_json() -> None:
    """Cập nhật .vscode/tasks.json với đường dẫn mới."""
    tasks_file = Path(".vscode/tasks.json")
    if not tasks_file.exists():
        print(f"⚠️  {tasks_file} không tồn tại")
        return
    print(f"🔧 Cập nhật {tasks_file}...")
    with open(tasks_file, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'"cwd":\s*"\$\{workspaceFolder\}"', f'"cwd": "{PROJECT_ROOT}"', content)
    content = re.sub(r'"command":\s*"python\s', f'"command": "{PYTHON_EXE} ', content)
    with open(tasks_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã cập nhật {tasks_file}")


def update_launch_json() -> None:
    """Cập nhật .vscode/launch.json với đường dẫn mới (nếu tồn tại)."""
    launch_file = Path(".vscode/launch.json")
    if not launch_file.exists():
        print(f"⚠️  {launch_file} không tồn tại - bỏ qua")
        return
    print(f"🔧 Cập nhật {launch_file}...")
    with open(launch_file, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'"program":\s*"\$\{workspaceFolder\}([^"]*)"', f'"program": "{PROJECT_ROOT}\\1"', content)
    content = re.sub(r'"cwd":\s*"\$\{workspaceFolder\}"', f'"cwd": "{PROJECT_ROOT}"', content)
    content = re.sub(r'"python":\s*"[^"]*python[^"]*"', f'"python": "{PYTHON_EXE}"', content)
    with open(launch_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã cập nhật {launch_file}")


def create_path_aliases() -> None:
    """Tạo aliases đường dẫn cho dễ sử dụng."""
    alias_file = Path(".path_aliases.json")
    aliases = {
        "project_root": "e:/zeta",
        "zeta_vn": "e:/zeta/zeta_vn",
        "vscode_config": "e:/zeta/.vscode",
        "venv": "e:/zeta/.venv",
        "copilot_config": "e:/zeta/.github/.copilot",
        "python_exe": "e:/zeta/.venv/Scripts/python.exe",
        "python_lib": "e:/zeta/.venv/Lib/site-packages",
        "tests": "e:/zeta/tests",
        "docs": "e:/zeta/docs",
        "tools": "e:/zeta/tools",
    }
    with open(alias_file, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2, ensure_ascii=False)
    print(f"✅ Đã tạo {alias_file} với path aliases")


def main() -> None:
    """Main execution function."""
    print("🚀 Bắt đầu cập nhật đường dẫn cho ZETA_VN project")
    print("=" * 60)
    current_dir = Path.cwd()
    print(f"📍 Thư mục hiện tại: {current_dir}")
    print("📍 Cập nhật đường dẫn tuyệt đối: e:/zeta")
    print("")
    update_vscode_settings()
    update_pyproject_toml()
    update_copilot_config()
    update_workspace_file()
    update_tasks_json()
    update_launch_json()
    create_path_aliases()
    print("")
    print("=" * 60)
    print("📊 Tóm tắt cập nhật:")
    print("✅ .vscode/settings.json - Python interpreter & file nesting")
    print("✅ pyproject.toml - Source paths & excludes")
    print("✅ .github/.copilot/config.json - Copilot configuration")
    print("✅ zeta_vn.code-workspace - Workspace folders")
    print("✅ .vscode/tasks.json - Task working directories")
    print("✅ .vscode/launch.json - Debug configurations")
    print("✅ .path_aliases.json - Path aliases reference")
    print("")
    print("🎯 Đường dẫn đã được chuẩn hóa thành:")
    print("  • Project Root: e:/zeta")
    print("  • ZETA_VN Package: e:/zeta/zeta_vn")
    print("  • VSCode Config: e:/zeta/.vscode")
    print("  • Virtual Environment: e:/zeta/.venv")
    print("  • Copilot Config: e:/zeta/.github/.copilot")
    print("")
    print("✨ Cập nhật đường dẫn hoàn thành thành công!")


if __name__ == "__main__":
    main()
