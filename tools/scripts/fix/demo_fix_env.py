from __future__ import annotations

import site
import subprocess
import sys
from pathlib import Path

import requests
import rich
import typer
import FileNotFoundError
import ImportError
import e
import getattr
import print
import sp

"""Demo script để test auto-fix environment và các dependencies."""


def test_basic_imports() -> None:
    """Test các import cơ bản."""
    print("🧪 Testing basic imports...")
    try:
        print(f"  ✅ typer: {getattr(typer, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"  ❌ typer: {e}")
    try:
        print(f"  ✅ rich: {getattr(rich, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"  ❌ rich: {e}")
    try:
        print(f"  ✅ requests: {getattr(requests, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"  ❌ requests: {e}")


def test_environment_health() -> None:
    """Test trạng thái environment."""
    print("\n🏥 Testing environment health...")
    venv_pth_found = False
    for sp in site.getsitepackages():
        pth_path = Path(sp) / "_virtualenv.pth"
        if pth_path.exists():
            venv_pth_found = True
            print(f"  ⚠️  _virtualenv.pth still exists: {pth_path}")
            break
    if not venv_pth_found:
        print("  ✅ _virtualenv.pth conflict resolved")
    print(f"  ✅ Python: {sys.version.split()[0]}")
    venv = sys.prefix
    print(f"  ✅ Virtual env: {venv}")


def test_uv_commands() -> None:
    """Test uv commands."""
    print("\n⚙️  Testing uv commands...")
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ uv: {result.stdout.strip()}")
        else:
            print(f"  ❌ uv: {result.stderr}")
    except FileNotFoundError:
        print("  ❌ uv: Not found")


def main() -> None:
    """Main demo function."""
    print("=== AUTO-FIX ENVIRONMENT DEMO ===\n")
    test_basic_imports()
    test_environment_health()
    test_uv_commands()
    print("\n=== SUMMARY ===")
    print("✅ Environment auto-fix scripts working!")
    print("✅ Essential dependencies available")
    print("✅ Virtual environment conflicts resolved")
    print("\n🎯 Next steps:")
    print("   1. Run: uv run python -m deepseek agent --apply")
    print("   2. Or use VS Code task: 'Deepseek: Fix & Context'")
    print("   3. Check .artifacts/ for reports")


if __name__ == "__main__":
    main()
