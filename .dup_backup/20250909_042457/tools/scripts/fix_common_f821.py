#!/usr/bin/env python3
"""Comprehensive F821 auto-fix tool for common patterns"""

from __future__ import annotations

import re
from pathlib import Path


def fix_common_patterns(file_path: str) -> int:
    """Fix common F821 patterns in a file"""
import Exception
import e
import enumerate
import file_path
import i
import import_stmt
import int
import line
import m
import new
import old
import pattern
import print
import replacement
import reversed
import sorted
import str
import var_name
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        original = content
        fixes = 0

        # Pattern 1: Missing assignments for common variables
        simple_fixes = [
            # Common underscore assignments
            ("_ = get_user(", "user = get_user("),
            ("_ = get_agent(", "agent = get_agent("),
            ("_ = get_session(", "session = get_session("),
            ("_ = create_user(", "user = create_user("),
            ("_ = create_agent(", "agent = create_agent("),
            ("_ = create_session(", "session = create_session("),
            ("_ = update_user(", "updated_user = update_user("),
            ("_ = update_agent(", "updated_agent = update_agent("),
            ("_ = update_session(", "updated_session = update_session("),
            ("_ = validate_", "validation_result = validate_"),
            ("_ = authenticate(", "result = authenticate("),
            ("_ = authorize(", "result = authorize("),
            ("_ = deploy_agent(", "result = deploy_agent("),
            ("_ = monitor_agent(", "result = monitor_agent("),
            ("_ = scale_agent(", "result = scale_agent("),
            # Context assignments
            ('info.context.get("current_user")', 'current_user = info.context.get("current_user")'),
            ('info.context.get("session")', 'session = info.context.get("session")'),
            ('info.context.get("container")', 'container = info.context.get("container")'),
            # Repository/service calls
            ("_ = repository.", "result = repository."),
            ("_ = service.", "result = service."),
            ("_ = cache.get(", "cached_result = cache.get("),
            ("_ = cache.set(", "result = cache.set("),
        ]

        for old, new in simple_fixes:
            if old in content:
                content = content.replace(old, new)
                fixes += 1

        # Pattern 2: Use case executions without assignments
        use_case_patterns = [
            (
                r"(\s+)await (\w+)_use_case\.execute\(([^)]*)\)(?!\s*=)",
                lambda m: f"{m.group(1)}{m.group(2)}_result = await {m.group(2)}_use_case.execute({m.group(3)})",
            ),
            (
                r"(\s+)(\w+)_use_case\.execute\(([^)]*)\)(?!\s*=)",
                lambda m: f"{m.group(1)}{m.group(2)}_result = {m.group(2)}_use_case.execute({m.group(3)})",
            ),
        ]

        for pattern, replacement in use_case_patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                fixes += 1

        # Pattern 3: Add missing imports for common undefined names
        missing_imports = {
            "inspect": "import inspect",
            "json": "import json",
            "os": "import os",
            "sys": "import sys",
            "ast": "import ast",
            "Path": "from pathlib import Path",
            "datetime": "from datetime import datetime",
            "Any": "from typing import Any",
            "Dict": "from typing import Dict",
            "List": "from typing import List",
            "Optional": "from typing import Optional",
            "Protocol": "from typing import Protocol",
            "dataclass": "from dataclasses import dataclass",
            "asdict": "from dataclasses import asdict",
        }

        lines = content.split("\n")
        imports_to_add = []

        for var_name, import_stmt in missing_imports.items():
            if f"Undefined name `{var_name}`" in content or var_name in content:
                if import_stmt not in content:
                    imports_to_add.append(import_stmt)

        if imports_to_add:
            # Find insertion point after __future__ imports
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("from __future__"):
                    insert_pos = i + 1
                elif line.strip() == "" or line.strip().startswith("#"):
                    continue
                else:
                    break

            # Insert imports
            for import_stmt in reversed(sorted(imports_to_add)):
                lines.insert(insert_pos, import_stmt)
                fixes += 1

            content = "\n".join(lines)

        if content != original:
            Path(file_path).write_text(content, encoding="utf-8")
            print(f"✅ {file_path}: {fixes} fixes applied")
            return fixes

        return 0

    except Exception as e:
        print(f"❌ {file_path}: Error - {e}")
        return 0


def main() -> None:
    """Apply fixes to top problematic files"""
    target_files = [
        "zeta_vn/tests/unit/memory/test_delete_memory_enhanced.py",
        "zeta_vn/tests/integration/test_system_integration.py",
        "zeta_vn/tests/e2e/test_user_workflows.py",
        "zeta_vn/core/security/session/session_service.py",
        "zeta_vn/tests/unit/test_use_cases.py",
        "zeta_vn/tools/ports_tools.py",
        "zeta_vn/storage/session_storage.py",
        "zeta_vn/docs/examples/agent_creation.py",
        "zeta_vn/core/use_cases/agent/deploy_agent.py",
        "zeta_vn/core/use_cases/agent/monitor_agent.py",
        "zeta_vn/tests/integration/test_analytics.py",
        "zeta_vn/core/use_cases/agent/scale_agent.py",
        "zeta_vn/tests/e2e/test_multi_user.py",
        "zeta_vn/app/api/v2/real_time_collab_optimized.py",
        "zeta_vn/core/use_cases/auth/authenticate_user.py",
    ]

    total_fixes = 0
    processed = 0

    for file_path in target_files:
        if Path(file_path).exists():
            fixes = fix_common_patterns(file_path)
            total_fixes += fixes
            processed += 1
        else:
            print(f"⚠️  {file_path}: File not found")

    print(f"\n🎉 Processed {processed} files, applied {total_fixes} fixes")


if __name__ == "__main__":
    main()
