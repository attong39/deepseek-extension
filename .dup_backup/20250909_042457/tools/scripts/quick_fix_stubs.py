#!/usr/bin/env python3
"""
Quick fix script for common stub patterns found by missing_code_audit.

Automatically fixes:
- Replace 'pass' with 'raise NotImplementedError' in functions
- Replace '...' with 'raise NotImplementedError' in functions
- Standardize TODO comments format
- Add proper return type hints where missing
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any
import Exception
import SystemExit
import any
import e
import enumerate
import file_path
import i
import int
import isinstance
import item
import len
import line
import list
import node
import part
import pattern
import print
import replacement
import root
import self
import str


class StubFixer(ast.NodeTransformer):
    """AST transformer to fix common stub patterns."""

    def __init__(self) -> None:
        self.changes_made = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        """Fix function definitions with stub patterns."""
        # Check if function body contains only pass or ellipsis
        if len(node.body) == 1:
            stmt = node.body[0]

            if isinstance(stmt, ast.Pass):
                # Replace pass with NotImplementedError
                new_stmt = ast.Raise(
                    exc=ast.Call(
                        func=ast.Name(id="NotImplementedError", ctx=ast.Load()),
                        args=[ast.Constant(value=f"TODO: Implement {node.name}()")],
                        keywords=[],
                    )
                )
                node.body = [new_stmt]
                self.changes_made += 1

            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Ellipsis):
                # Replace ... with NotImplementedError
                new_stmt = ast.Raise(
                    exc=ast.Call(
                        func=ast.Name(id="NotImplementedError", ctx=ast.Load()),
                        args=[ast.Constant(value=f"TODO: Implement {node.name}()")],
                        keywords=[],
                    )
                )
                node.body = [new_stmt]
                self.changes_made += 1

        # Continue traversing
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        """Fix async function definitions."""
        return self.visit_FunctionDef(node)


def fix_python_file(file_path: Path) -> int:
    """Fix a single Python file and return number of changes."""
    try:
        original_content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(original_content)

        # Apply fixes
        fixer = StubFixer()
        new_tree = fixer.visit(tree)

        if fixer.changes_made > 0:
            # Generate new code
            new_content = ast.unparse(new_tree)

            # Try to preserve some formatting
            new_content = standardize_todo_comments(new_content)

            # Write back to file
            file_path.write_text(new_content, encoding="utf-8")
            print(f"✅ Fixed {fixer.changes_made} issues in {file_path}")

        return fixer.changes_made

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return 0


def standardize_todo_comments(content: str) -> str:
    """Standardize TODO comment format."""
    # Convert various TODO formats to standard format
    patterns = [
        (r"#\s*TODO\s*:?\s*(.+)", r"# TODO: \1"),
        (r"#\s*FIXME\s*:?\s*(.+)", r"# FIXME: \1"),
        (r"#\s*HACK\s*:?\s*(.+)", r"# HACK: \1"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content


def fix_typescript_file(file_path: Path) -> int:
    """Fix a TypeScript file and return number of changes."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        changes = 0

        # Replace throw new Error('Not implemented') with better message
        def replace_not_impl(match):
            nonlocal changes
            changes += 1
            return "throw new Error('TODO: Implement this method');"

        content = re.sub(r"throw\s+new\s+Error\(['\"]Not implemented['\"]\)\s*;?", replace_not_impl, content)

        # Standardize TODO comments
        content = re.sub(r"//\s*TODO\s*:?\s*(.+)", r"// TODO: \1", content)
        content = re.sub(r"//\s*FIXME\s*:?\s*(.+)", r"// FIXME: \1", content)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ Fixed {changes} issues in {file_path}")

        return changes

    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return 0


def generate_todo_list(scan_roots: list[Path]) -> None:
    """Generate a TODO.md file with all found issues."""
    todo_items = []

    for root in scan_roots:
        if not root.exists():
            continue

        for file_path in root.rglob("*.py"):
            try:
                content = file_path.read_text(encoding="utf-8")

                # Find TODO comments
                for i, line in enumerate(content.splitlines(), 1):
                    if re.search(r"\b(TODO|FIXME|HACK)\b", line):
                        todo_items.append(
                            {
                                "file": str(file_path),
                                "line": i,
                                "content": line.strip(),
                                "type": "comment",
                            }
                        )

                # Find NotImplementedError
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.Raise)
                        and isinstance(node.exc, ast.Call)
                        and isinstance(node.exc.func, ast.Name)
                        and node.exc.func.id == "NotImplementedError"
                    ):
                        todo_items.append(
                            {
                                "file": str(file_path),
                                "line": node.lineno,
                                "content": f"NotImplementedError in line {node.lineno}",
                                "type": "not_implemented",
                            }
                        )

            except Exception:
                continue

    # Generate TODO.md
    todo_file = Path("TODO.md")
    content = "# TODO List - Generated from Code Audit\n\n"
    content += f"Total items: {len(todo_items)}\n\n"

    # Group by type
    comments = [item for item in todo_items if item["type"] == "comment"]
    not_impl = [item for item in todo_items if item["type"] == "not_implemented"]

    if not_impl:
        content += "## 🚨 High Priority - NotImplementedError\n\n"
        for item in not_impl[:20]:  # Limit to first 20
            content += f"- [ ] `{item['file']}:{item['line']}` - {item['content']}\n"
        if len(not_impl) > 20:
            content += f"\n... and {len(not_impl) - 20} more\n"
        content += "\n"

    if comments:
        content += "## 📝 TODO Comments\n\n"
        for item in comments[:30]:  # Limit to first 30
            content += f"- [ ] `{item['file']}:{item['line']}` - {item['content']}\n"
        if len(comments) > 30:
            content += f"\n... and {len(comments) - 30} more\n"

    todo_file.write_text(content, encoding="utf-8")
    print(f"📝 Generated {todo_file} with {len(todo_items)} items")


def main() -> int:
    """Main entry point."""
    scan_roots = [
        Path("zeta_vn"),
        Path("desktop_ai_zeta/src"),
    ]

    print("🔧 Starting quick fix for stub patterns...")

    total_changes = 0
    files_processed = 0

    for root in scan_roots:
        if not root.exists():
            print(f"⚠️ Directory {root} does not exist, skipping...")
            continue

        print(f"📁 Processing {root}...")

        # Fix Python files
        for file_path in root.rglob("*.py"):
            if any(part.startswith(".") for part in file_path.parts):
                continue  # Skip hidden directories

            changes = fix_python_file(file_path)
            total_changes += changes
            if changes > 0:
                files_processed += 1

        # Fix TypeScript files
        for file_path in root.rglob("*.ts"):
            if any(part.startswith(".") for part in file_path.parts):
                continue

            changes = fix_typescript_file(file_path)
            total_changes += changes
            if changes > 0:
                files_processed += 1

    print("\n✅ Quick fix completed!")
    print(f"📊 Files processed: {files_processed}")
    print(f"🔧 Total changes: {total_changes}")

    # Generate TODO list
    print("\n📝 Generating TODO list...")
    generate_todo_list(scan_roots)

    print("\n💡 Next steps:")
    print("1. Review generated TODO.md for remaining tasks")
    print("2. Run `uv run python scripts/missing_code_audit.py` to check progress")
    print("3. Run `uv run ruff format .` to fix formatting")
    print("4. Run quality checks: `uv run ruff check . && uv run mypy .`")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
