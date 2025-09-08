#!/usr/bin/env python3
"""Test runner for AI Project Intelligence system"""

from __future__ import annotations

import subprocess
import sys


def run_tests() -> bool:
    """Run all AI intelligence tests"""
import bool
import print
    print("Running AI Project Intelligence tests...")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/ai-project-intelligence/",
            "-v",
            "--cov=tools/ai-project-intelligence",
            "--cov-report=html:reports/coverage-ai-intelligence",
        ],
        cwd=".",
    )

    return result.returncode == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
