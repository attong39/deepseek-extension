#!/usr/bin/env python3
"""
F821 Error Analysis and Auto-Fix Tool
Analyzes and fixes undefined name errors systematically
"""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any
import Exception
import KeyboardInterrupt
import any
import count
import dict
import e
import enumerate
import error
import errs
import f
import file_errors
import i
import import_line
import input
import int
import j
import len
import list
import open
import pattern
import print
import range
import reversed
import set
import sorted
import str
import sum
import var_name
import x

# Constants
UNDEFINED_NAME_MSG = "Undefined name `"


def analyze_f821_errors() -> dict[str, list[dict[str, Any]]]:
    """Phân tích F821 errors theo file và pattern"""
    print("🔍 Analyzing F821 undefined name errors...")

    # Get F821 errors in JSON format
    result = subprocess.run(
        ["uv", "run", "ruff", "check", "zeta_vn/", "--select=F821", "--output-format=json"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Warning: ruff returned code {result.returncode}")

    try:
        errors = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("❌ Failed to parse ruff output as JSON")
        return {}

    # Group errors by file
    errors_by_file = defaultdict(list)
    for error in errors:
        file_path = error["filename"]
        # Convert to relative path
        rel_path = str(Path(file_path).relative_to(Path.cwd()))
        errors_by_file[rel_path].append(error)

    return dict(errors_by_file)


def analyze_error_patterns(errors_by_file: dict[str, list[dict]]) -> None:
    """Phân tích patterns của F821 errors"""
    print(f"\n📊 Found {sum(len(errs) for errs in errors_by_file.values())} F821 errors in {len(errors_by_file)} files")

    # Top 10 files với nhiều lỗi nhất
    print("\n🔥 Top 10 files with most F821 errors:")
    sorted_files = sorted(errors_by_file.items(), key=lambda x: len(x[1]), reverse=True)

    for i, (file_path, file_errors) in enumerate(sorted_files[:10], 1):
        print(f"{i:2d}. {file_path:<60} {len(file_errors):4d} errors")

    # Analyze undefined names patterns
    undefined_names = defaultdict(int)
    for file_errors in errors_by_file.values():
        for error in file_errors:
            message = error["message"]
            if "Undefined name `" in message:
                name = message.split("Undefined name `")[1].split("`")[0]
                undefined_names[name] += 1

    print("\n🎯 Top 15 most common undefined names:")
    sorted_names = sorted(undefined_names.items(), key=lambda x: x[1], reverse=True)

    for i, (name, count) in enumerate(sorted_names[:15], 1):
        print(f"{i:2d}. {name:<20} {count:4d} occurrences")


def get_fixable_patterns() -> dict[str, str]:
    """Định nghĩa các patterns có thể auto-fix"""
    return {
        # Common missing imports
        "os": "import os",
        "sys": "import sys",
        "json": "import json",
        "ast": "import ast",
        "Path": "from pathlib import Path",
        "datetime": "from datetime import datetime",
        "UUID": "from uuid import UUID",
        "Any": "from typing import Any",
        "Dict": "from typing import Dict",
        "List": "from typing import List",
        "Optional": "from typing import Optional",
        "Union": "from typing import Union",
        "dataclass": "from dataclasses import dataclass",
        "asdict": "from dataclasses import asdict",
        "field": "from dataclasses import field",
        "inspect": "import inspect",
        "importlib": "import importlib",
        "pkgutil": "import pkgutil",
        "get_type_hints": "from typing import get_type_hints",
        "Protocol": "from typing import Protocol",
        "UTC": "from datetime import timezone as UTC",
        # Pydantic imports
        "BaseModel": "from pydantic import BaseModel",
        "Field": "from pydantic import Field",
        "validator": "from pydantic import validator",
        "root_validator": "from pydantic import root_validator",
        # Common test patterns
        "pytest": "import pytest",
        "AsyncMock": "from unittest.mock import AsyncMock",
        "Mock": "from unittest.mock import Mock",
        "patch": "from unittest.mock import patch",
    }


def fix_file_imports(file_path: str, errors: list[dict]) -> int:
    """Fix missing imports in a specific file"""
    fixable_patterns = get_fixable_patterns()
    fixes_applied = 0

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Collect needed imports
        needed_imports = set()
        for error in errors:
            message = error["message"]
            if "Undefined name `" in message:
                name = message.split("Undefined name `")[1].split("`")[0]
                if name in fixable_patterns:
                    needed_imports.add(fixable_patterns[name])

        if not needed_imports:
            return 0

        # Add imports at the top (after from __future__ import annotations if present)
        lines = content.split("\n")
        insert_pos = 0

        # Find insertion position (after __future__ imports and docstrings)
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("from __future__"):
                insert_pos = i + 1
            elif line.startswith('"""') or line.startswith("'''"):
                # Skip docstring
                if line.count('"""') == 1 or line.count("'''") == 1:
                    # Multi-line docstring, find end
                    quote = '"""' if '"""' in line else "'''"
                    for j in range(i + 1, len(lines)):
                        if quote in lines[j]:
                            insert_pos = j + 1
                            break
                else:
                    insert_pos = i + 1
            elif line == "" or line.startswith("#"):
                continue
            else:
                break

        # Insert new imports
        new_imports = sorted(needed_imports)
        for import_line in reversed(new_imports):
            lines.insert(insert_pos, import_line)
            fixes_applied += 1

        # Write back
        new_content = "\n".join(lines)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  ✅ {file_path}: Added {fixes_applied} imports")

    except Exception as e:
        print(f"  ❌ {file_path}: Error fixing - {e}")

    return fixes_applied


def fix_variable_assignments(file_path: str, errors: list[dict]) -> int:
    """Fix common variable assignment patterns like _ = func() -> var = func()"""
    fixes_applied = 0

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Common patterns to fix
        variable_fixes = {
            "user": r"_ = User\(",
            "result": r"_ = \w+\(",
            "response": r"_ = \w+\(",
            "agent": r"_ = Agent\(",
            "memory": r"_ = Memory\(",
        }

        modified = False
        for var_name, pattern in variable_fixes.items():
            # Check if this variable is undefined in this file
            has_undefined = any(
                var_name in error["message"] for error in errors if "Undefined name" in error["message"]
            )

            if has_undefined:
                import re

                # Replace _ = with var_name =
                old_pattern = pattern
                new_pattern = pattern.replace("_", var_name, 1)

                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    modified = True
                    fixes_applied += 1

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ {file_path}: Fixed {fixes_applied} variable assignments")

    except Exception as e:
        print(f"  ❌ {file_path}: Error fixing variables - {e}")

    return fixes_applied


def main() -> None:
    """Main function to analyze and fix F821 errors"""
    print("🚀 F821 Undefined Names - Analysis & Auto-Fix Tool")
    print("=" * 60)

    # Analyze errors
    errors_by_file = analyze_f821_errors()
    if not errors_by_file:
        print("✅ No F821 errors found!")
        return

    analyze_error_patterns(errors_by_file)

    # Ask user for action
    print("\n🔧 Auto-fix options:")
    print("1. Fix missing imports (safest)")
    print("2. Fix variable assignments")
    print("3. Both import and variable fixes")
    print("4. Skip auto-fix")

    try:
        choice = input("\nChoose option (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n🚫 Cancelled by user")
        return

    if choice == "4":
        print("📋 Analysis complete. No fixes applied.")
        return

    # Apply fixes
    total_fixes = 0
    print("\n🔧 Applying fixes...")

    # Sort files by error count (fix worst first)
    sorted_files = sorted(errors_by_file.items(), key=lambda x: len(x[1]), reverse=True)

    for file_path, file_errors in sorted_files[:20]:  # Fix top 20 files
        print(f"\n📁 Processing: {file_path} ({len(file_errors)} errors)")

        if choice in ["1", "3"]:
            fixes = fix_file_imports(file_path, file_errors)
            total_fixes += fixes

        if choice in ["2", "3"]:
            fixes = fix_variable_assignments(file_path, file_errors)
            total_fixes += fixes

    print(f"\n🎉 Applied {total_fixes} fixes!")

    # Re-check errors
    print("\n🔍 Re-checking F821 errors...")
    final_result = subprocess.run(
        ["uv", "run", "ruff", "check", "zeta_vn/", "--select=F821", "--statistics"],
        capture_output=True,
        text=True,
    )

    if "F821" in final_result.stdout:
        final_count = int(final_result.stdout.split()[0])
        initial_count = sum(len(errs) for errs in errors_by_file.values())
        improvement = initial_count - final_count
        print(f"📊 F821 errors: {initial_count} → {final_count} ({improvement:+d})")
    else:
        print("✅ All F821 errors fixed!")


if __name__ == "__main__":
    main()
