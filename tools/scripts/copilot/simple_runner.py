import subprocess
import sys
from pathlib import Path
import Exception
import bool
import cmd
import desc
import description
import e
import len
import print
import str

"""
Simple Copilot Agent Runner - Chạy các bước chính của Copilot Agent
"""


def run_command(cmd: str, description: str) -> bool:
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout
        )
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {description} - EXCEPTION: {e}")
        return False


def main():
    print("🤖 COPILOT CODING AGENT - SIMPLE RUNNER")
    print("=" * 50)
    if not Path("scripts/copilot/build_context.py").exists():
        print("❌ Không tìm thấy scripts/copilot/build_context.py")
        print("💡 Đảm bảo bạn đang ở thư mục root của project")
        sys.exit(1)
    steps = [
        ("python scripts/copilot/build_context.py", "Build Copilot Context"),
        ("uv run ruff check . --fix", "Python Ruff Check & Fix"),
        ("uv run mypy . --ignore-missing-imports", "Python MyPy Type Check"),
        ("uv run pytest -x -q", "Python Tests"),
    ]
    success_count = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1
        print()  # Empty line for readability
    print("=" * 50)
    print(f"📊 RESULTS: {success_count}/{len(steps)} steps successful")
    if success_count == len(steps):
        print("🎉 COPILOT AGENT RUN COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print("⚠️ Some steps failed. Check output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
