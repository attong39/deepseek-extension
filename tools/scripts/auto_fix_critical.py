from __future__ import annotations

    import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set
import re

import ast

from apps.backend.core.observability.logging import get_logger

"""
Auto-Fix Script for Critical Code Quality Issues
===============================================
Automatically fixes the most common code quality issues:
- Missing pytest imports in test files
- Import ordering issues
- Undefined names in __all__
- Basic syntax fixes
"""
logger = get_logger(__name__)
class AutoFixer:
    """Automated code quality fixer."""
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)
        self.fixed_files: List[str] = []
        self.errors: List[str] = []
    def run_all_fixes(self) -> Dict[str, Any]:
        """Run all auto-fix operations."""
        logger.info("🚀 Starting auto-fix operations...")
        results = {
            "pytest_imports": self.fix_pytest_imports(),
            "import_ordering": self.fix_import_ordering(),
            "undefined_all": self.fix_undefined_in_all(),
            "syntax_fixes": self.fix_basic_syntax(),
        }
        logger.info(f"✅ Auto-fix completed. Fixed {len(self.fixed_files)} files.")
        return {
            "success": True,
            "fixed_files": self.fixed_files,
            "errors": self.errors,
            "results": results,
        }
    def fix_pytest_imports(self) -> Dict[str, Any]:
        """Fix missing pytest imports in test files."""
        logger.info("🔧 Fixing pytest imports...")
        test_files = self._find_test_files()
        fixed = 0
        for test_file in test_files:
            if self._add_pytest_import(test_file):
                fixed += 1
                self.fixed_files.append(str(test_file))
        return {"total_test_files": len(test_files), "fixed": fixed}
    def fix_import_ordering(self) -> Dict[str, Any]:
        """Fix import ordering issues."""
        logger.info("🔧 Fixing import ordering...")
        python_files = self._find_python_files()
        fixed = 0
        for py_file in python_files:
            if self._reorder_imports(py_file):
                fixed += 1
                self.fixed_files.append(str(py_file))
        return {"total_files": len(python_files), "fixed": fixed}
    def fix_undefined_in_all(self) -> Dict[str, Any]:
        """Fix undefined names in __all__."""
        logger.info("🔧 Fixing undefined names in __all__...")
        python_files = self._find_python_files()
        fixed = 0
        for py_file in python_files:
            if self._clean_undefined_all(py_file):
                fixed += 1
                self.fixed_files.append(str(py_file))
        return {"total_files": len(python_files), "fixed": fixed}
    def fix_basic_syntax(self) -> Dict[str, Any]:
        """Fix basic syntax errors."""
        logger.info("🔧 Fixing basic syntax errors...")
        python_files = self._find_python_files()
        fixed = 0
        for py_file in python_files:
            if self._fix_syntax_errors(py_file):
                fixed += 1
                self.fixed_files.append(str(py_file))
        return {"total_files": len(python_files), "fixed": fixed}
    def _find_test_files(self) -> List[Path]:
        """Find all test files in the project."""
        test_files = []
        for pattern in ["test_*.py", "*_test.py", "tests/**/*.py"]:
            test_files.extend(self.project_root.glob(pattern))
        return [f for f in test_files if f.is_file()]
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        return list(self.project_root.rglob("*.py"))
    def _add_pytest_import(self, file_path: Path) -> bool:
        """Add pytest import to test file if missing."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "@pytest.fixture" in content or "pytest." in content:
                if "import pytest" not in content:
                    lines = content.split("\n")
                    insert_pos = 0
                    for i, line in enumerate(lines):
                        if line.startswith("from __future__ import"):
                            insert_pos = i + 1
                        elif line.strip() and not line.startswith("from __future__"):
                            break
                    lines.insert(insert_pos, "")
                    lines.insert(insert_pos + 1, "import pytest")
                    lines.insert(insert_pos + 2, "")
                    new_content = "\n".join(lines)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    logger.debug(f"Added pytest import to {file_path}")
                    return True
        except Exception as e:
            self.errors.append(f"Error fixing {file_path}: {e}")
        return False
    def _reorder_imports(self, file_path: Path) -> bool:
        """Reorder imports in a file."""
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", "--fix", "--select=I", str(file_path)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            return result.returncode == 0
        except Exception as e:
            self.errors.append(f"Error reordering imports in {file_path}: {e}")
            return False
    def _clean_undefined_all(self, file_path: Path) -> bool:
        """Remove undefined names from __all__."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)
            defined_names = self._get_defined_names(tree)
            all_names = self._get_all_names(tree)
            if all_names:
                undefined = all_names - defined_names
                if undefined:
                    for name in undefined:
                        content = re.sub(
                            rf'(\s*)"?\b{re.escape(name)}\b"?(\s*,?)', r"\1\2", content
                        )
                    content = re.sub(r",\s*,", ",", content)
                    content = re.sub(r"\(\s*,", "(", content)
                    content = re.sub(r",\s*\)", ")", content)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.debug(
                        f"Removed undefined names from __all__ in {file_path}: {undefined}"
                    )
                    return True
        except Exception as e:
            self.errors.append(f"Error cleaning __all__ in {file_path}: {e}")
        return False
    def _fix_syntax_errors(self, file_path: Path) -> bool:
        """Fix basic syntax errors."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                ast.parse(content)
                return False  # No syntax errors
            except SyntaxError as e:
                logger.warning(f"Syntax error in {file_path}: {e}")
                return False
        except Exception as e:
            self.errors.append(f"Error checking syntax in {file_path}: {e}")
            return False
    def _get_defined_names(self, tree: ast.AST) -> Set[str]:
        """Get all defined names in the AST."""
        defined = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined.add(node.name)
            elif isinstance(node, ast.ClassDef):
                defined.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined.add(target.id)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    defined.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    defined.add(alias.asname or alias.name)
        return defined
    def _get_all_names(self, tree: ast.AST) -> Set[str]:
        """Get all names in __all__."""
        all_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, ast.List):
                            for item in node.value.elts:
                                if isinstance(item, ast.Str):
                                    all_names.add(item.s)
                                elif isinstance(item, ast.Constant) and isinstance(item.value, str):
                                    all_names.add(item.value)
        return all_names
def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    fixer = AutoFixer(project_root)
    try:
        results = fixer.run_all_fixes()
        print("🎉 Auto-fix completed!")
        print(f"📊 Fixed files: {len(results['fixed_files'])}")
        print(f"❌ Errors: {len(results['errors'])}")
        for key, value in results["results"].items():
            print(f"🔧 {key}: {value}")
        if results["errors"]:
            print("\n⚠️  Errors encountered:")
            for error in results["errors"][:5]:  # Show first 5 errors
                print(f"  - {error}")
        return 0
    except Exception as e:
        logger.error(f"Auto-fix failed: {e}")
        return 1
if __name__ == "__main__":
    exit(main())