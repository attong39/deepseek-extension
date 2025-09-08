#!/usr/bin/env python3
"""Auto-fix F821 errors caused by _ = var but using var"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def fix_underscore_assignments(file_path: str) -> int:
    """Fix patterns like: _ = Session(...) where session is used later"""
import Exception
import callable
import e
import error
import int
import len
import m
import pattern
import print
import replacement
import set
import sorted
import str

    try:
        content = Path(file_path).read_text(encoding="utf-8")
        original_content = content
        fixes = 0

        # Common patterns to fix
        patterns = [
            (r"_ = Session\(", "session = Session("),
            (r"_ = Agent\(", "agent = Agent("),
            (r"_ = User\(", "user = User("),
            (r"_ = Memory\(", "memory = Memory("),
            (r"_ = create_session\(", "session = create_session("),
            (r"_ = create_agent\(", "agent = create_agent("),
            (r"_ = create_user\(", "user = create_user("),
            (r"_ = create_memory\(", "memory = create_memory("),
            (r"_ = get_session\(", "session = get_session("),
            (r"_ = get_agent\(", "agent = get_agent("),
            (r"_ = get_user\(", "user = get_user("),
            (r"_ = update_agent\(", "updated_agent = update_agent("),
            (r"_ = deploy_agent\(", "result = deploy_agent("),
            (r"_ = validate_\w+\(", lambda m: m.group(0).replace("_ =", "validation_result =")),
            (r"_ = authenticate\(", "result = authenticate("),
            (r"_ = authorize\(", "result = authorize("),
        ]

        for pattern, replacement in patterns:
            if callable(replacement):
                content = re.sub(pattern, replacement, content)
            else:
                content = re.sub(pattern, replacement, content)

            if content != original_content:
                fixes += 1
                original_content = content

        # Generic patterns for common variables
        generic_patterns = [
            (
                r"(\s+)_ = (\w+)\.(\w+)\(([^)]*)\)([^\n]*\n(?:\s*.*?result.*?\n)+)",
                r"\1result = \2.\3(\4)\5",
            ),
            (
                r"(\s+)_ = (\w+_\w+)\(([^)]*)\)([^\n]*\n(?:\s*.*?cached_result.*?\n)+)",
                r"\1cached_result = \2(\3)\4",
            ),
        ]

        for pattern, replacement in generic_patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            if content != original_content:
                fixes += 1
                original_content = content

        if fixes > 0:
            Path(file_path).write_text(content, encoding="utf-8")
            print(f"✅ {file_path}: Fixed {fixes} underscore assignments")

        return fixes

    except Exception as e:
        print(f"❌ {file_path}: Error - {e}")
        return 0


def main() -> None:
    """Fix F821 errors by replacing _ = var with var = var"""

    # Get list of files with F821 errors
    result = subprocess.run(
        ["uv", "run", "ruff", "check", "zeta_vn/", "--select=F821", "--output-format=json"],
        capture_output=True,
        text=True,
    )

    if not result.stdout.strip():
        print("✅ No F821 errors found!")
        return

    import json

    errors = json.loads(result.stdout)

    # Get unique files with F821 errors
    files_with_errors = set()
    for error in errors:
        file_path = str(Path(error["filename"]).relative_to(Path.cwd()))
        files_with_errors.add(file_path)

    print(f"🔧 Processing {len(files_with_errors)} files with F821 errors...")

    total_fixes = 0
    for file_path in sorted(files_with_errors):
        if "test_" in file_path:  # Prioritize test files
            fixes = fix_underscore_assignments(file_path)
            total_fixes += fixes

    print(f"\n🎉 Applied {total_fixes} fixes to test files!")

    # Show remaining errors
    result = subprocess.run(
        ["uv", "run", "ruff", "check", "zeta_vn/", "--select=F821", "--statistics"],
        capture_output=True,
        text=True,
    )

    if "F821" in result.stdout:
        count = int(result.stdout.split()[0])
        print(f"📊 Remaining F821 errors: {count}")
    else:
        print("✅ All F821 errors fixed!")


if __name__ == "__main__":
    main()
