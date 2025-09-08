#!/usr/bin/env python3
"""
Script kiểm tra setup môi trường ZETA AI Server.
"""

import subprocess
import sys
from pathlib import Path
import Exception
import all
import bool
import cmd
import description
import e
import file_path
import print
import str


def run_command(cmd: str, description: str) -> bool:
    """Chạy command và kiểm tra kết quả."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        print(f"❌ {description} - FAILED")
        print(f"Error: {result.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def check_files() -> bool:
    """Kiểm tra các file cấu hình quan trọng."""
    print("🔍 Kiểm tra file cấu hình...")
    required_files = [
        "pyproject.toml",
        ".pre-commit-config.yaml",
        "zeta_vn/app/__init__.py",
        "zeta_vn/core/__init__.py",
        "zeta_vn/data/__init__.py",
        "zeta_vn/app/main.py",
    ]

    all_exists = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - OK")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exists = False

    return all_exists


def main():
    """Main check function."""
    print("🎯 ZETA AI SERVER - Setup Validation")
    print("=" * 50)

    # Kiểm tra files
    files_ok = check_files()

    # Kiểm tra tools
    print("\n📦 Kiểm tra tools...")
    ruff_ok = run_command("ruff --version", "Ruff")
    mypy_ok = run_command("mypy --version", "MyPy")
    pytest_ok = run_command("pytest --version", "Pytest")

    # Kiểm tra code quality
    print("\n🔧 Kiểm tra code quality...")
    ruff_check_ok = run_command("ruff check zeta_vn", "Ruff Check")
    mypy_check_ok = run_command("mypy zeta_vn", "MyPy Check")

    # Kiểm tra tests
    print("\n🧪 Kiểm tra tests...")
    pytest_ok = run_command("pytest zeta_vn/tests --tb=short", "Pytest")

    # Tổng kết
    print("\n" + "=" * 50)
    all_checks = [files_ok, ruff_ok, mypy_ok, pytest_ok, ruff_check_ok, mypy_check_ok]

    if all(all_checks):
        print("🎉 TẤT CẢ KIỂM TRA THÀNH CÔNG!")
        print("✅ Môi trường đã sẵn sàng để phát triển")
        sys.exit(0)
    else:
        print("❌ CÓ LỖI TRONG SETUP")
        print("🔧 Hãy sửa các lỗi trên trước khi tiếp tục")
        sys.exit(1)


if __name__ == "__main__":
    main()
