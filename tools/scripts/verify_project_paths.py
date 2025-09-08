from __future__ import annotations

import json
from pathlib import Path
import Exception
import bool
import check_func
import e
import expected_value
import f
import key
import len
import list
import message
import name
import open
import passed
import path
import print
import results
import str
import success
import sum
import tuple

"""
Script xác nhận cập nhật đường dẫn cho ZETA_VN project.
Kiểm tra xem tất cả các file cấu hình đã được cập nhật đúng chưa.
"""


def check_vscode_settings() -> tuple[bool, str]:
    """Kiểm tra .vscode/settings.json."""
    settings_file = Path(".vscode/settings.json")
    if not settings_file.exists():
        return False, "File không tồn tại"
    with open(settings_file, encoding="utf-8") as f:
        content = f.read()
    checks = [
        ("Python interpreter", "e:/zeta/.venv/Scripts/python.exe" in content),
        ("File nesting zeta_vn", "e:/zeta/zeta_vn" in content),
    ]
    failed = [name for name, passed in checks if not passed]
    if failed:
        return False, f"Thiếu: {', '.join(failed)}"
    return True, "✅ Tất cả đường dẫn đúng"


def check_pyproject_toml() -> tuple[bool, str]:
    """Kiểm tra pyproject.toml."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return False, "File không tồn tại"
    with open(pyproject_file, encoding="utf-8") as f:
        content = f.read()
    checks = [
        ("Coverage source", "e:/zeta/zeta_vn" in content),
        ("Test paths", "e:/zeta/tests" in content),
        ("Exclude .venv", "e:/zeta/.venv" in content),
    ]
    failed = [name for name, passed in checks if not passed]
    if failed:
        return False, f"Thiếu: {', '.join(failed)}"
    return True, "✅ Tất cả đường dẫn đúng"


def check_copilot_config() -> tuple[bool, str]:
    """Kiểm tra .github/.copilot/config.json."""
    config_file = Path(".github/.copilot/config.json")
    if not config_file.exists():
        return False, "File không tồn tại"
    try:
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
        checks = [
            ("Project root", config.get("project_root") == "e:/zeta"),
            ("ZETA_VN path", config.get("zeta_vn_path") == "e:/zeta/zeta_vn"),
            ("VSCode path", config.get("vscode_path") == "e:/zeta/.vscode"),
            ("Venv path", config.get("venv_path") == "e:/zeta/.venv"),
        ]
        failed = [name for name, passed in checks if not passed]
        if failed:
            return False, f"Thiếu: {', '.join(failed)}"
        return True, "✅ Tất cả đường dẫn đúng"
    except json.JSONDecodeError:
        return False, "File JSON không hợp lệ"


def check_workspace_file() -> tuple[bool, str]:
    """Kiểm tra zeta_vn.code-workspace."""
    workspace_file = Path("zeta_vn.code-workspace")
    if not workspace_file.exists():
        return False, "File không tồn tại"
    with open(workspace_file, encoding="utf-8") as f:
        content = f.read()
    checks = [
        ("Root path", '"path": "e:/zeta"' in content),
        ("Python interpreter", "e:/zeta/.venv/Scripts/python.exe" in content),
    ]
    failed = [name for name, passed in checks if not passed]
    if failed:
        return False, f"Thiếu: {', '.join(failed)}"
    return True, "✅ Tất cả đường dẫn đúng"


def check_path_aliases() -> tuple[bool, str]:
    """Kiểm tra .path_aliases.json."""
    aliases_file = Path(".path_aliases.json")
    if not aliases_file.exists():
        return False, "File không tồn tại"
    try:
        with open(aliases_file, encoding="utf-8") as f:
            aliases = json.load(f)
        expected_aliases = {
            "project_root": "e:/zeta",
            "zeta_vn": "e:/zeta/zeta_vn",
            "vscode_config": "e:/zeta/.vscode",
            "venv": "e:/zeta/.venv",
            "copilot_config": "e:/zeta/.github/.copilot",
            "python_exe": "e:/zeta/.venv/Scripts/python.exe",
        }
        failed = []
        for key, expected_value in expected_aliases.items():
            if aliases.get(key) != expected_value:
                failed.append(f"{key}={aliases.get(key)}")
        if failed:
            return False, f"Sai: {', '.join(failed)}"
        return True, "✅ Tất cả aliases đúng"
    except json.JSONDecodeError:
        return False, "File JSON không hợp lệ"


def check_file_existence() -> tuple[bool, str]:
    """Kiểm tra sự tồn tại của các thư mục chính."""
    paths_to_check = [
        Path("e:/zeta/zeta_vn"),
        Path("e:/zeta/.vscode"),
        Path("e:/zeta/.venv"),
        Path("e:/zeta/.github/.copilot"),
    ]
    missing = [str(path) for path in paths_to_check if not path.exists()]
    if missing:
        return False, f"Thiếu thư mục: {', '.join(missing)}"
    return True, "✅ Tất cả thư mục tồn tại"


def main() -> None:
    """Main execution function."""
    print("🔍 KIỂM TRA CẬP NHẬT ĐƯỜNG DẪN ZETA_VN")
    print("=" * 60)
    checks = [
        ("📁 Thư mục tồn tại", check_file_existence),
        ("⚙️  VSCode Settings", check_vscode_settings),
        ("📦 PyProject.toml", check_pyproject_toml),
        ("🤖 Copilot Config", check_copilot_config),
        ("💼 Workspace File", check_workspace_file),
        ("🔗 Path Aliases", check_path_aliases),
    ]
    results: list[tuple[str, bool, str]] = []
    for name, check_func in checks:
        try:
            success, message = check_func()
            results.append((name, success, message))
            status = "✅" if success else "❌"
            print(f"{status} {name}: {message}")
        except Exception as e:
            results.append((name, False, f"Lỗi: {e}"))
            print(f"❌ {name}: Lỗi: {e}")
    print("")
    print("=" * 60)
    total_checks = len(results)
    passed_checks = sum(1 for _, success, _ in results if success)
    failed_checks = total_checks - passed_checks
    print("📊 KẾT QUẢ KIỂM TRA:")
    print(f"  • Tổng số kiểm tra: {total_checks}")
    print(f"  • Thành công: {passed_checks}")
    print(f"  • Thất bại: {failed_checks}")
    print(f"  • Tỷ lệ thành công: {passed_checks / total_checks * 100:.1f}%")
    if failed_checks == 0:
        print("")
        print("🎉 TẤT CẢ ĐƯỜNG DẪN ĐÃ ĐƯỢC CẬP NHẬT THÀNH CÔNG!")
        print("🚀 Project ZETA_VN sẵn sàng với đường dẫn mới")
    else:
        print("")
        print("⚠️  CÓ MỘT SỐ VẤN ĐỀ CẦN KHẮC PHỤC:")
        for name, success, message in results:
            if not success:
                print(f"  • {name}: {message}")
    print("")


if __name__ == "__main__":
    main()
