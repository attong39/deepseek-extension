from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import Exception
import bool
import e
import len
import name
import print
import sum
import test_func

"""Test runner cho auto-fix environment."""


def test_repair_env() -> bool:
    """Test repair_env.py với dry-run."""
    print("Testing repair_env.py (dry-run)...")
    try:
        result = subprocess.run(
            [sys.executable, "scripts/fix/repair_env.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_verify_stack() -> bool:
    """Test verify_stack.py."""
    print("\nTesting verify_stack.py...")
    try:
        result = subprocess.run(
            [sys.executable, "scripts/fix/verify_stack.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if Path(".artifacts/verify_stack.json").exists():
            print("✅ verify_stack.json created")
            return True
        else:
            print("❌ verify_stack.json not created")
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main() -> None:
    """Main test function."""
    print("=== AUTO-FIX ENVIRONMENT TEST ===\n")
    tests = [
        ("repair_env.py", test_repair_env),
        ("verify_stack.py", test_verify_stack),
    ]
    results = []
    for name, test_func in tests:
        print(f"Running {name} test...")
        success = test_func()
        results.append((name, success))
        print(f"{'✅' if success else '❌'} {name}: {'PASS' if success else 'FAIL'}\n")
    print("=== TEST SUMMARY ===")
    passed = sum(1 for _, success in results if success)
    total = len(results)
    for name, success in results:
        print(f"{'✅' if success else '❌'} {name}")
    print(f"\nTotal: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All tests passed! Environment scripts are ready.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
