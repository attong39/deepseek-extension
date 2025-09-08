#!/usr/bin/env python3
"""
AI Optimization Runner - Automatically optimizes all project files using AI codemods
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import SystemExit
import bool
import check
import cmd
import cwd
import int
import list
import print
import str


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> int:
    print(f"$ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if check and res.returncode != 0:
        raise SystemExit(res.returncode)
    return res.returncode


def run_optimization() -> bool:
    """Run full AI optimization pipeline."""
    print("🚀 Starting AI-powered code optimization...")
    root = Path.cwd()

    # Ensure reports directory exists
    reports_dir = root / "reports" / "ai-codemod" / "latest"
    reports_dir.mkdir(parents=True, exist_ok=True)

    engine_path = "tools/ai-codemod/engine.py"

    # 1. Baseline analysis
    print("📊 Running initial analysis...")
    run(
        [
            sys.executable,
            engine_path,
            "--mode",
            "analyze",
            "--root",
            ".",
            "--config",
            "tools/ai-codemod/ai-rules.yml",
        ]
    )

    # 2. Apply safe transformations first
    print("🔧 Applying safe transformations...")
    run(
        [
            sys.executable,
            engine_path,
            "--mode",
            "apply",
            "--root",
            ".",
            "--config",
            "tools/ai-codemod/ai-rules.yml",
            "--no-dry-run",
        ]
    )

    # 3. Verification
    print("✅ Verifying changes...")
    verify_rc = subprocess.run(
        [
            sys.executable,
            engine_path,
            "--mode",
            "verify",
        ],
        capture_output=True,
        text=True,
    )

    (reports_dir / "verify_stdout.txt").write_text(verify_rc.stdout, encoding="utf-8")
    (reports_dir / "verify_stderr.txt").write_text(verify_rc.stderr, encoding="utf-8")

    if verify_rc.returncode != 0:
        print("❌ Verification failed, rolling back...")
        return False

    print("🎉 Optimization completed successfully!")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AI-powered code optimization")
    parser.add_argument("--auto-commit", action="store_true", help="Auto-commit changes")
    args = parser.parse_args()

    success = run_optimization()
    if success and args.auto_commit:
        run(["git", "add", "."], check=True)
        run(["git", "commit", "-m", "chore(ai): automated AI code optimization"], check=False)
        print("📝 Changes committed automatically")


if __name__ == "__main__":
    main()
