#!/usr/bin/env python
"""Pre-commit hook for auto-fixing imports and dependencies."""
from __future__ import annotations
import subprocess
import sys
import os
from pathlib import Path

def main() -> int:
    print("🔧 Running Auto-Fix Missing Imports & Dependencies...")
    
    # Change to repo root
    repo_root = Path(__file__).parent.parent.parent
    os.chdir(repo_root)
    
    # Run auto-fix
    result = subprocess.run(
        [sys.executable, "tools/auto_fix/cli.py", "all"],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    # Auto-stage any modified files
    if result.returncode == 0:
        print("📝 Auto-staging modified files...")
        subprocess.run(["git", "add", "."], check=False)
        print("✅ Auto-fix completed successfully")
    elif result.returncode == 2:
        print("⚠️ Auto-fix completed with unresolved symbols")
        subprocess.run(["git", "add", "."], check=False)
    else:
        print("❌ Auto-fix failed")
        return 1
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
import SystemExit
import int
import print
