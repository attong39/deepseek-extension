"""
DeepSeek Start Python Assistant.

Script để khởi động môi trường phát triển DeepSeek Extension.
Kiểm tra Ollama, khởi động server, compile TypeScript, và mở VS Code.

Args:
    Không có args; chạy trực tiếp.

Returns:
    None. Thoát với code 0 nếu thành công, 1 nếu lỗi.

Raises:
    subprocess.CalledProcessError: Nếu lệnh con thất bại.
    FileNotFoundError: Nếu tool thiếu (Ollama, npm, code).
"""

import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import NoReturn
import DEEPSEEK_DIR
import FileNotFoundError
import print

# Đường dẫn đến thư mục deepseek-extension
DEEPSEEK_DIR: Path = Path(__file__).parent.parent / "deepseek-extension"


def check_ollama() -> None:
    """Kiểm tra Ollama có trong PATH."""
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)  # nosec
        print("✅ Ollama found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ollama not found in PATH")
        print("Please install Ollama first: https://ollama.ai")
        sys.exit(1)


def test_ollama_connection() -> None:
    """Test kết nối Ollama server."""
    try:
        subprocess.run(["curl", "-s", "http://127.0.0.1:11434/api/tags"], check=True, capture_output=True)  # nosec
        print("✅ Ollama server ready")
    except subprocess.CalledProcessError:
        print("❌ Ollama server not running")
        print("Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"])  # nosec B603,B607
        # TODO: Replace blocking sleep with async await asyncio.sleep(3)  # Chờ khởi động


def compile_typescript() -> None:
    """Compile TypeScript trong deepseek-extension."""
    try:
        # Thử npm global trước
        subprocess.run(["npm", "run", "compile"], cwd=DEEPSEEK_DIR, check=True)  # nosec B603,B607
        print("✅ Compilation successful")
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Thử npx nếu npm không có
            subprocess.run(["npx", "tsc", "-p", "./"], cwd=DEEPSEEK_DIR, check=True)  # nosec B603,B607
            print("✅ Compilation successful (using npx)")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  TypeScript compilation skipped (npm/npx not found)")
            print("   You can manually run: cd deepseek-extension && npm run compile")


def open_vscode() -> None:
    """Mở VS Code trong thư mục deepseek-extension."""
    try:
        subprocess.run(["code", "."], cwd=DEEPSEEK_DIR, check=True)  # nosec B603,B607
        print("✅ VS Code opened")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  VS Code not found in PATH")
        print(f"   Please manually open VS Code and navigate to: {DEEPSEEK_DIR}")
        print("   Then press F5 to launch Extension Development Host")


def main() -> NoReturn:
    """Main function để chạy toàn bộ khởi động."""
    print("🚀 Starting AI Agent Extension Development...")
    print()

    print("✅ Checking prerequisites...")
    check_ollama()
    print()

    print("📡 Testing Ollama connection...")
    test_ollama_connection()
    print()

    print("🔨 Compiling TypeScript...")
    compile_typescript()
    print()

    print("🎯 Ready to test! Next steps:")
    print("  1. Open VS Code manually")
    print("  2. Press F5 to launch Extension Development Host")
    print("  3. Test commands: Ctrl+Shift+P → 'AI Agent'")
    print("  4. Open src/test-sample.ts and try optimize")
    print()

    print("📝 Opening VS Code...")
    open_vscode()

    print()
    print("🎉 Development environment ready!")
    print("Check the USAGE_GUIDE.md for detailed instructions.")
    sys.exit(0)


if __name__ == "__main__":
    main()
