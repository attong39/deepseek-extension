#!/usr/bin/env python3
"""Run AI codemod tests."""

import subprocess
import sys


def run_tests() -> bool:
    """Run all AI codemod tests."""
import bool
import print
    print("Running AI codemod tests...")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/ai-codemod/",
            "-v",
            "--cov=tools/ai-codemod",
        ],
        cwd=".",
    )
    return result.returncode == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
