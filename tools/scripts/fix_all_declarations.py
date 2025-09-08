from __future__ import annotations

import ast
import re
from pathlib import Path
import Exception
import SyntaxError
import bool
import e
import file_path
import isinstance
import list
import m
import node
import print
import set
import sorted
import str
import target

#!/usr/bin/env python3
"""
Script để sửa lại __all__ declarations bị lỗi từ auto-fix.
Chỉ giữ lại các tên thực sự được định nghĩa trong module.
"""


def extract_defined_names(tree: ast.AST) -> set[str]:
    """Extract all defined names from AST."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.add(target.id)
    return names


def fix_all_declaration(file_path: Path) -> bool:
    """Fix __all__ declaration in a file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return False
        defined_names = extract_defined_names(tree)
        all_pattern = r"__all__\s*=\s*\[([^\]]+)\]"
        match = re.search(all_pattern, content, re.DOTALL)
        if not match:
            return False
        all_content = match.group(1)
        name_pattern = r"'([^']+)'|\"([^\"]+)\""
        all_names = []
        for m in re.finditer(name_pattern, all_content):
            name = m.group(1) or m.group(2)
            if name in defined_names:
                all_names.append(name)
        if not all_names:
            new_content = re.sub(r"__all__\s*=\s*\[[^\]]+\]\s*", "", content)
        else:
            all_str = f"__all__ = {sorted(all_names)!r}"
            new_content = re.sub(all_pattern, all_str, content, flags=re.DOTALL)
        if new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function."""
    project_root = Path(__file__).parent.parent
    py_files = list(project_root.glob("zeta_vn/**/*.py"))
    py_files.extend(project_root.glob("desktop_ai_zeta/**/*.py"))
    fixed_count = 0
    for file_path in py_files:
        if fix_all_declaration(file_path):
            print(f"Fixed __all__ in {file_path.relative_to(project_root)}")
            fixed_count += 1
    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()
