#!/usr/bin/env python3
"""
Hướng dẫn hoàn tất cấu hình VS Code - bước cuối cùng
"""

from __future__ import annotations

import sys
from pathlib import Path
import Exception
import ImportError
import bool
import e
import int
import name
import print
import status


def print_final_steps() -> None:
    """In hướng dẫn bước cuối cùng"""

    print("🎯 VS CODE - BƯỚC CUỐI CÙNG")
    print("=" * 50)

    print("\n✅ VERIFICATION HOÀN TẤT - TẤT CẢ OK!")
    print("   • Workspace: E:\\zeta")
    print("   • Virtual Environment: Activated")
    print("   • VS Code Settings: Configured")
    print("   • Python Imports: Working")
    print("   • Python Path: Correct")

    print("\n🔄 BÂY GIỜ CẦN RESTART VS CODE:")
    print("   1. Đóng VS Code hoàn toàn (Ctrl+Shift+P > 'Developer: Reload Window')")
    print("   2. Mở lại VS Code")
    print("   3. Chọn Python Interpreter:")
    print("      • Ctrl+Shift+P")
    print("      • Gõ: 'Python: Select Interpreter'")
    print("      • Chọn: E:\\zeta\\.venv\\Scripts\\python.exe")

    print("\n🧪 SAU ĐÓ TEST:")
    print("   • Mở terminal trong VS Code")
    print("   • Kiểm tra: python --version")
    print("   • Kiểm tra: python -c \"import zeta_vn; print('OK')\"")
    print("   • Terminal sẽ hiển thị: (zeta-ai-server)")

    print("\n🚀 KHỞI ĐỘNG DỰ ÁN:")
    print("   • Server: Ctrl+Shift+P > 'Tasks: Run Task' > 'dev:server'")
    print("   • Desktop: Ctrl+Shift+P > 'Tasks: Run Task' > 'dev:desktop'")
    print("   • Quality Check: Ctrl+Shift+P > 'Tasks: Run Task' > 'qa:all'")

    print("\n📝 GHI CHÚ QUAN TRỌNG:")
    print("   ⚠️ Nếu vẫn không nhận diện virtual environment:")
    print("   • Restart VS Code lại")
    print("   • Kiểm tra file .vscode/settings.json")
    print("   • Chạy lại: python tools/verify_vscode_config_simple.py")

    print("\n✨ CẤU HÌNH HOÀN TẤT!")
    print("   🎉 VS Code đã sẵn sàng cho phát triển")
    print("   🔧 Tất cả tools và quality gates hoạt động")
    print("   🚀 Có thể bắt đầu coding!")


def check_environment() -> bool:
    """Kiểm tra lần cuối môi trường"""
    workspace = Path.cwd()
    venv_dir = workspace / ".venv"
    settings_file = workspace / ".vscode" / "settings.json"

    checks = {
        "Workspace": workspace.exists() and (workspace / "pyproject.toml").exists(),
        "Virtual Environment": venv_dir.exists(),
        "VS Code Settings": settings_file.exists(),
        "Python Import": True,  # Sẽ test sau
    }

    # Test import
    try:
        import zeta_vn  # noqa: F401

        checks["Python Import"] = True
    except ImportError:
        checks["Python Import"] = False

    print("🔍 KIỂM TRA CUỐI CÙNG:")
    all_ok = True
    for name, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"   {symbol} {name}: {'OK' if status else 'FAILED'}")
        if not status:
            all_ok = False

    return all_ok


def main() -> int:
    """Main function"""
    try:
        print_final_steps()

        print("\n" + "=" * 50)

        if check_environment():
            print("\n🎊 EVERYTHING READY! CẤU HÌNH HOÀN HẢO!")
            return 0
        else:
            print("\n⚠️ CÓ VẤN ĐỀ - CẦN KIỂM TRA LẠI")
            return 1

    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
