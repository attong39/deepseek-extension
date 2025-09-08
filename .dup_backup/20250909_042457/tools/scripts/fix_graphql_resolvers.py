#!/usr/bin/env python3
"""Fix missing assignments in GraphQL resolvers"""

from __future__ import annotations

import re
from pathlib import Path


def fix_graphql_resolver(file_path: str) -> int:
    """Fix missing assignments in GraphQL resolver file"""
import Exception
import e
import file_path
import int
import pattern
import print
import replacement
import str
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        original = content
        fixes = 0

        # Fix missing current_user assignment
        patterns = [
            # Fix current_user assignment
            (
                r'(\s+)info\.context\.get\("current_user"\)',
                r'\1current_user = info.context.get("current_user")',
            ),
            # Fix use case executions without assignment
            (
                r"(\s+)await create_agent_use_case\.execute\(",
                r"\1created_agent = await create_agent_use_case.execute(",
            ),
            (
                r"(\s+)await get_agent_use_case\.execute\(([^)]+)\)",
                r"\1existing_agent = await get_agent_use_case.execute(\2)",
            ),
            (
                r"(\s+)await update_agent_use_case\.execute\(",
                r"\1updated_agent = await update_agent_use_case.execute(",
            ),
            # Fix generic _ = patterns
            (
                r"(\s+)_ = await get_agent_use_case\.execute\(([^)]+)\)",
                r"\1agent = await get_agent_use_case.execute(\2)",
            ),
        ]

        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                fixes += 1

        # Fix specific issues in agent_resolvers.py
        if "agent_resolvers.py" in file_path:
            # Add missing create_agent_use_case execution assignment
            content = re.sub(
                r"(\s+)# Execute use case\n(\s+)await create_agent_use_case\.execute\(",
                r"\1# Execute use case\n\2created_agent = await create_agent_use_case.execute(",
                content,
            )

            # Add missing update_agent_use_case execution assignment
            content = re.sub(
                r"(\s+)# Execute update\n(\s+)await update_agent_use_case\.execute\(",
                r"\1# Execute update\n\2updated_agent = await update_agent_use_case.execute(",
                content,
            )

        if content != original:
            Path(file_path).write_text(content, encoding="utf-8")
            print(f"✅ Fixed {file_path} ({fixes} patterns)")
            return fixes

        return 0

    except Exception as e:
        print(f"❌ Error in {file_path}: {e}")
        return 0


def main() -> None:
    """Fix GraphQL resolver files"""
    files_to_fix = [
        "zeta_vn/app/api/graphql/resolvers/agent_resolvers.py",
    ]

    total_fixes = 0
    for file_path in files_to_fix:
        if Path(file_path).exists():
            total_fixes += fix_graphql_resolver(file_path)

    print(f"Applied {total_fixes} fixes")


if __name__ == "__main__":
    main()
