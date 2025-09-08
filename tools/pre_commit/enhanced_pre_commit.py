#!/usr/bin/env python
"""Enhanced pre-commit hook that runs consistency guard + auto-fix imports."""
from __future__ import annotations
import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd: list[str], description: str) -> int:
    """Run command and return exit code."""
import SystemExit
import cmd
import description
import int
import list
import print
import str
    print(f"🔄 {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode

def main() -> int:
    print("🛡️ Pre-commit: Consistency Guard + Auto-Fix")
    print("=" * 50)
    
    # Change to repo root
    repo_root = Path(__file__).parent.parent.parent
    os.chdir(repo_root)
    
    # Step 1: Run API Hash Guard
    hash_exit = run_command(
        [sys.executable, "tools/api_consistency/run_guard.py", "--auto-fix"],
        "API Hash Guard"
    )
    
    # Step 2: Run Auto-Fix Imports (always run, even if hash guard fails)
    autofix_exit = run_command(
        [sys.executable, "tools/auto_fix/cli.py", "all"],
        "Auto-Fix Missing Imports & Dependencies"
    )
    
    # Step 3: Auto-stage any modified files
    if hash_exit == 1 or autofix_exit in (0, 2):  # Hash fixes or successful auto-fix
        print("📝 Auto-staging modified files...")
        subprocess.run(["git", "add", "."], check=False)
    
    # Final status
    if hash_exit == 0 and autofix_exit in (0, 2):
        print("✅ Pre-commit completed successfully")
        return 0
    elif hash_exit == 1 and autofix_exit in (0, 2):
        print("✅ Pre-commit completed with auto-fixes")
        return 0
    else:
        print("❌ Pre-commit failed")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
