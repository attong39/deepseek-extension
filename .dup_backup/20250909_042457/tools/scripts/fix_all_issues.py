#!/usr/bin/env python3
"""
Auto-fix __all__ issues in Python files.
Scans for F822 errors and fixes __all__ declarations.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
import Exception
import bool
import e
import f
import file_path
import isinstance
import item
import node
import open
import print
import py_file
import set
import str
import target


def extract_defined_names(file_path: Path) -> set[str]:
    """Extract all defined names from a Python file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        defined_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)

        return defined_names
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return set()


def fix_all_issues(file_path: Path) -> bool:
    """Fix __all__ issues in a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Find __all__ declaration
        all_match = re.search(r"__all__\s*=\s*\[([^\]]*)\]", content, re.DOTALL)
        if not all_match:
            return False

        defined_names = extract_defined_names(file_path)

        # Parse current __all__
        all_content = all_match.group(1)
        current_items = []
        for item in re.findall(r"'([^']*)'|'([^']*)'|\"([^\"]*)\"|\"([^\"]*)\"", all_content):
            name = item[0] or item[1] or item[2] or item[3]
            if name and name in defined_names:
                current_items.append(f"'{name}'")

        if not current_items:
            return False

        # Create new __all__
        items_str = ",\n    ".join(current_items)
        new_all = f"__all__ = [\n    {items_str}\n]"

        # Replace in content
        new_content = content.replace(all_match.group(0), new_all)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Fixed {file_path}")
        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Main function."""
    zeta_vn_path = Path("zeta_vn")
    if not zeta_vn_path.exists():
        print("zeta_vn directory not found")
        return

    fixed_count = 0
    for py_file in zeta_vn_path.rglob("*.py"):
        if fix_all_issues(py_file):
            fixed_count += 1

    print(f"Fixed {fixed_count} files")


if __name__ == "__main__":
    main()
