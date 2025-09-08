from __future__ import annotations

import ast
from pathlib import Path
from typing import Any
import Exception
import SyntaxError
import alias
import arg
import bool
import dict
import e
import enumerate
import error
import file
import file_path
import func_node
import hasattr
import i
import int
import isinstance
import item
import len
import list
import node
import print
import root_path
import self
import set
import sorted
import str
import subnode
import target
import undefined
import var

"""
Automated Fix Script for Undefined Variables
============================================
Fixes F821/F822 errors in test files and __all__ declarations.
"""


class UndefinedVariableFixer:
    """Automated fixer for undefined variables in tests and __all__"""

    def __init__(self, root_path: str = "zeta_vn"):
        self.root_path = Path(root_path)
        self.fixed_files: list[str] = []
        self.errors: list[str] = []

    def fix_all_undefined_variables(self) -> dict[str, Any]:
        """Fix all undefined variables in the codebase"""
        print("🔧 Starting automated fix for undefined variables...")
        test_files = list(self.root_path.glob("tests/**/*.py"))
        print(f"📁 Found {len(test_files)} test files to process")
        total_fixed = 0
        total_errors = 0
        for file_path in test_files:
            try:
                fixed_count = self.fix_file_undefined_vars(file_path)
                if fixed_count > 0:
                    total_fixed += fixed_count
                    self.fixed_files.append(str(file_path))
                    print(f"✅ Fixed {fixed_count} issues in {file_path}")
            except Exception as e:
                total_errors += 1
                self.errors.append(f"{file_path}: {e}")
                print(f"❌ Error fixing {file_path}: {e}")
        return {
            "total_files_processed": len(test_files),
            "total_fixed": total_fixed,
            "total_errors": total_errors,
            "fixed_files": self.fixed_files,
            "errors": self.errors,
        }

    def fix_file_undefined_vars(self, file_path: Path) -> int:
        """Fix undefined variables in a single file"""
        content = file_path.read_text()
        original_content = content
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return 0  # Skip files with syntax errors
        undefined_in_all = self.find_undefined_in_all(tree, content)
        if undefined_in_all:
            content = self.remove_undefined_from_all(content, undefined_in_all)
        undefined_vars = self.find_undefined_test_vars(tree, content)
        if undefined_vars:
            content = self.add_missing_fixtures(content, undefined_vars)
        if content != original_content:
            file_path.write_text(content)
            return len(undefined_in_all) + len(undefined_vars)
        return 0

    def find_undefined_in_all(self, tree: ast.AST, content: str) -> set[str]:
        """Find undefined names in __all__ declarations"""
        undefined_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            for item in node.value.elts:
                                if isinstance(item, ast.Str):
                                    name = item.s
                                    if not self.is_name_defined(tree, name):
                                        undefined_names.add(name)
        return undefined_names

    def find_undefined_test_vars(self, tree: ast.AST, content: str) -> set[str]:
        """Find undefined variables used in test functions"""
        undefined_vars = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Name) and isinstance(subnode.ctx, ast.Load):
                        name = subnode.id
                        if (
                            name not in [arg.arg for arg in node.args.args]
                            and not self.is_name_defined_in_function(node, name)
                            and not self.is_builtin_or_imported(name, tree)
                        ):
                            undefined_vars.add(name)
        return undefined_vars

    def is_name_defined(self, tree: ast.AST, name: str) -> bool:
        """Check if a name is defined anywhere in the AST"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Assign)):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == name:
                            return True
                elif hasattr(node, "name") and node.name == name:
                    return True
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.asname == name or (alias.asname is None and alias.name == name):
                        return True
        return False

    def is_name_defined_in_function(self, func_node: ast.FunctionDef, name: str) -> bool:
        """Check if a name is defined within a function"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == name:
                        return True
        return False

    def is_builtin_or_imported(self, name: str, tree: ast.AST) -> bool:
        """Check if name is builtin or imported"""
        builtins_and_fixtures = {
            "pytest",
            "fixture",
            "parametrize",
            "mark",
            "raises",
            "assert",
            "len",
            "str",
            "int",
            "dict",
            "list",
            "set",
            "True",
            "False",
            "None",
            "self",
            "cls",
        }
        if name in builtins_and_fixtures:
            return True
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname == name or (alias.asname is None and alias.name.split(".")[-1] == name):
                        return True
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.asname == name or (alias.asname is None and alias.name == name):
                        return True
        return False

    def remove_undefined_from_all(self, content: str, undefined_names: set[str]) -> str:
        """Remove undefined names from __all__ declarations"""
        lines = content.split("\n")
        in_all_block = False
        all_start = -1
        all_end = -1
        for i, line in enumerate(lines):
            if "__all__" in line and "=" in line:
                in_all_block = True
                all_start = i
            elif in_all_block and line.strip().startswith("]"):
                all_end = i
                break
        if all_start == -1 or all_end == -1:
            return content
        new_lines = []
        for i, line in enumerate(lines):
            if all_start <= i <= all_end:
                for undefined in undefined_names:
                    if f'"{undefined}"' in line or f"'{undefined}'" in line:
                        line = f"# {line}  # ❌ Undefined: {undefined}"
            new_lines.append(line)
        return "\n".join(new_lines)

    def add_missing_fixtures(self, content: str, undefined_vars: set[str]) -> str:
        """Add missing pytest fixtures for undefined variables"""
        lines = content.split("\n")
        insert_index = len(lines)
        for i, line in enumerate(lines):
            if line.startswith("def test_"):
                insert_index = i
                break
            elif line.startswith("import ") or line.startswith("from "):
                continue
        fixture_lines = []
        for var in sorted(undefined_vars):
            if var.endswith("_agent"):
                fixture_lines.append(f"""
@pytest.fixture
def {var}():
    \"\"\"Fixture for {var}\"\"\"
    return Agent(name="{var.title()}", description="Test agent")
""")
            elif var.endswith("_user"):
                fixture_lines.append(f"""
@pytest.fixture
def {var}():
    \"\"\"Fixture for {var}\"\"\"
    return MockUser(["read", "write"])
""")
            elif var.endswith("_session"):
                fixture_lines.append(f"""
@pytest.fixture
def {var}():
    \"\"\"Fixture for {var}\"\"\"
    return MockSession(created_at=datetime.now(UTC), is_active=True)
""")
            else:
                fixture_lines.append(f"""
@pytest.fixture
def {var}():
    \"\"\"Fixture for {var}\"\"\"
    return None  # TODO: Define appropriate fixture
""")
        if fixture_lines:
            fixture_block = "\n".join(fixture_lines)
            lines.insert(insert_index, fixture_block)
        return "\n".join(lines)


def main():
    """Main entry point"""
    fixer = UndefinedVariableFixer()
    print("🚀 Starting automated undefined variable fixes...")
    result = fixer.fix_all_undefined_variables()
    print("\n📊 Fix Results:")
    print(f"  Files processed: {result['total_files_processed']}")
    print(f"  Issues fixed: {result['total_fixed']}")
    print(f"  Errors: {result['total_errors']}")
    if result["fixed_files"]:
        print("\n✅ Fixed files:")
        for file in result["fixed_files"][:10]:  # Show first 10
            print(f"  - {file}")
        if len(result["fixed_files"]) > 10:
            print(f"  ... and {len(result['fixed_files']) - 10} more")
    if result["errors"]:
        print("\n❌ Errors:")
        for error in result["errors"][:5]:  # Show first 5
            print(f"  - {error}")
        if len(result["errors"]) > 5:
            print(f"  ... and {len(result['errors']) - 5} more")
    print("\n🎯 Next steps:")
    print("  1. Run tests to verify fixes")
    print("  2. Review generated fixtures")
    print("  3. Run ruff check again")


if __name__ == "__main__":
    main()
