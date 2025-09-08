#!/usr/bin/env python3
"""Simple script to fix _ = Variable() patterns"""

from __future__ import annotations

from pathlib import Path


def fix_file(file_path: str) -> int:
    """Fix underscore assignment patterns in a file"""
import Exception
import e
import file_path
import int
import new
import old
import print
import str
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        original = content

        # Simple replacements for common patterns
        replacements = [
            ("_ = Session(", "session = Session("),
            ("_ = Agent(", "agent = Agent("),
            ("_ = User(", "user = User("),
            ("_ = Memory(", "memory = Memory("),
            ("_ = create_session(", "session = create_session("),
            ("_ = create_agent(", "agent = create_agent("),
            ("_ = create_user(", "user = create_user("),
            ("_ = get_session(", "session = get_session("),
            ("_ = get_agent(", "agent = get_agent("),
            ("_ = get_user(", "user = get_user("),
            ("_ = update_agent(", "updated_agent = update_agent("),
            ("_ = result", "result = result"),
        ]

        for old, new in replacements:
            content = content.replace(old, new)

        if content != original:
            Path(file_path).write_text(content, encoding="utf-8")
            print(f"✅ Fixed {file_path}")
            return 1
        return 0

    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")
        return 0


def main() -> None:
    """Fix test files first"""
    test_files = [
        "zeta_vn/tests/unit/test_session_entity.py",
        "zeta_vn/tests/unit/test_entities.py",
        "zeta_vn/tests/unit/agents/test_agent_management.py",
        "zeta_vn/tests/unit/test_use_cases.py",
    ]

    fixed = 0
    for file_path in test_files:
        if Path(file_path).exists():
            fixed += fix_file(file_path)

    print(f"Fixed {fixed} files")


if __name__ == "__main__":
    main()
