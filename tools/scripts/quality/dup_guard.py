from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path
import Exception
import dict
import directory
import e
import f
import files
import func_name
import isinstance
import issue
import len
import line
import list
import name
import node
import open
import print
import py_file
import str

"""
Duplicate guard - kiểm tra code trùng lặp và import không sử dụng
"""


def check_unused_imports() -> list[str]:
    """Check for unused imports using ruff"""
    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "check", ".", "--select=F401", "--quiet"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        if result.returncode == 0:
            return []
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception as e:
        print(f"Error checking unused imports: {e}")
        return []


def check_star_imports() -> list[str]:
    """Check for star imports using ruff"""
    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "check", ".", "--select=F403,F405", "--quiet"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent,
        )
        if result.returncode == 0:
            return []
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception as e:
        print(f"Error checking star imports: {e}")
        return []


def find_duplicate_functions(directory: Path) -> dict[str, list[str]]:
    """Find duplicate function definitions"""
    functions = {}
    for py_file in directory.rglob("*.py"):
        if "test" in str(py_file) or "__pycache__" in str(py_file):
            continue
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in functions:
                        functions[node.name].append(str(py_file))
                    else:
                        functions[node.name] = [str(py_file)]
        except Exception:
            continue
    return {name: files for name, files in functions.items() if len(files) > 1}


def main():
    print("🔍 DUPLICATE GUARD - Checking for code duplication")
    root_dir = Path(__file__).parent.parent.parent
    zeta_vn_dir = root_dir / "zeta_vn"
    issues = []
    print("Checking unused imports...")
    unused_imports = check_unused_imports()
    if unused_imports:
        issues.extend([f"Unused import: {line}" for line in unused_imports])
    print("Checking star imports...")
    star_imports = check_star_imports()
    if star_imports:
        issues.extend([f"Star import: {line}" for line in star_imports])
    print("Checking duplicate functions...")
    duplicates = find_duplicate_functions(zeta_vn_dir)
    if duplicates:
        for func_name, files in duplicates.items():
            if len(files) > 1:
                issues.append(f"Duplicate function '{func_name}' in: {', '.join(files)}")
    if issues:
        print("\n❌ DUPLICATION ISSUES FOUND:")
        for issue in issues[:10]:  # Limit output
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
        print(f"\nTotal issues: {len(issues)}")
        sys.exit(1)
    else:
        print("✅ No duplication issues found")


if __name__ == "__main__":
    main()
