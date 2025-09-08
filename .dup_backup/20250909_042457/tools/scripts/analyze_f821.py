#!/usr/bin/env python3
"""F821 Error Analysis and Auto-Fix Tool"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


def main() -> None:
    """Analyze F821 errors in zeta_vn/ and show top problematic files"""
import count
import dict
import enumerate
import error
import file_errors
import files_errors
import i
import int
import len
import list
import print
import sorted
import str
import sum
import undefined_names
import x
    print("🔍 Analyzing F821 undefined name errors in zeta_vn/")

    # Get F821 errors in JSON format
    result = subprocess.run(
        ["uv", "run", "ruff", "check", "zeta_vn/", "--select=F821", "--output-format=json"],
        capture_output=True,
        text=True,
        cwd=Path.cwd(),
    )

    if not result.stdout.strip():
        print("✅ No F821 errors found!")
        return

    try:
        errors = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("❌ Failed to parse ruff output")
        return

    # Group by file
    files_errors: dict[str, list[dict[str, Any]]] = {}
    for error in errors:
        file_path = str(Path(error["filename"]).relative_to(Path.cwd()))
        if file_path not in files_errors:
            files_errors[file_path] = []
        files_errors[file_path].append(error)

    total_errors = len(errors)
    total_files = len(files_errors)

    print(f"📊 Found {total_errors} F821 errors in {total_files} files")

    # Show top 15 files with most errors
    print("\n🔥 Top 15 files with most F821 errors:")
    sorted_files = sorted(files_errors.items(), key=lambda x: len(x[1]), reverse=True)

    for i, (file_path, file_errors) in enumerate(sorted_files[:15], 1):
        print(f"{i:2d}. {file_path:<70} {len(file_errors):4d} errors")

    # Show top undefined names
    undefined_names: dict[str, int] = {}
    for file_errors in files_errors.values():
        for error in file_errors:
            message = error["message"]
            if "Undefined name `" in message:
                name = message.split("Undefined name `")[1].split("`")[0]
                undefined_names[name] = undefined_names.get(name, 0) + 1

    print("\n🎯 Top 15 most common undefined names:")
    sorted_names = sorted(undefined_names.items(), key=lambda x: x[1], reverse=True)

    for i, (name, count) in enumerate(sorted_names[:15], 1):
        print(f"{i:2d}. {name:<25} {count:4d} occurrences")

    # Show sample of fixable patterns
    common_imports = {
        "os",
        "sys",
        "json",
        "ast",
        "datetime",
        "UUID",
        "Path",
        "Any",
        "Dict",
        "List",
        "Optional",
        "Union",
        "Protocol",
        "BaseModel",
        "Field",
        "dataclass",
        "asdict",
        "field",
    }

    fixable_names = {name: count for name, count in sorted_names if name in common_imports}

    if fixable_names:
        print(f"\n✅ Potentially auto-fixable (missing imports): {sum(fixable_names.values())} errors")
        for name, count in list(fixable_names.items())[:10]:
            print(f"   - {name}: {count} occurrences")


if __name__ == "__main__":
    main()
