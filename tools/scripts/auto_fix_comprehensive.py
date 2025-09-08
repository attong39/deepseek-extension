from __future__ import annotations

import ast
import re
from pathlib import Path
import Exception
import SyntaxError
import bool
import e
import f
import file_path
import import_line
import isinstance
import line
import list
import new
import node
import old
import pattern
import print
import replacement
import self
import set
import sorted
import str
import target

"""
Auto-fix script để xử lý:
1. Thêm __all__ vào các module
2. Sửa lỗi F821 undefined names trong test files
3. Sửa import order issues
"""


class CodeAutoFixer:
    """Auto-fixer cho các lỗi code thường gặp."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.stats = {
            "files_processed": 0,
            "all_added": 0,
            "f821_fixed": 0,
            "imports_fixed": 0,
        }

    def run(self) -> None:
        """Chạy tất cả auto-fixes."""
        print("🔧 Starting comprehensive auto-fix...")
        self._fix_all_declarations()
        self._fix_f821_errors()
        self._fix_import_order()
        self._print_stats()

    def _fix_all_declarations(self) -> None:
        """Thêm __all__ vào các module chưa có."""
        print("📝 Adding __all__ declarations...")
        py_files = []
        for pattern in ["zeta_vn/**/*.py", "desktop_ai_zeta/src/**/*.py"]:
            py_files.extend(self.project_root.glob(pattern))
        py_files = [f for f in py_files if "/test" not in str(f) and "_test" not in f.name]
        for file_path in py_files:
            if self._add_all_to_file(file_path):
                self.stats["all_added"] += 1
                print(f"  ✓ Added __all__ to {file_path.relative_to(self.project_root)}")

    def _add_all_to_file(self, file_path: Path) -> bool:
        """Thêm __all__ vào một file nếu chưa có."""
        try:
            content = file_path.read_text(encoding="utf-8")
            if "__all__" in content:
                return False
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return False
            public_symbols = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith("_"):
                        public_symbols.append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith("_"):
                            public_symbols.append(target.id)
            public_symbols = sorted(set(public_symbols))
            if not public_symbols:
                return False
            all_declaration = f"\n__all__ = {public_symbols!r}\n"
            new_content = content.rstrip() + all_declaration
            file_path.write_text(new_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            return False

    def _fix_f821_errors(self) -> None:
        """Sửa lỗi F821 undefined names trong test files."""
        print("🐞 Fixing F821 undefined name errors...")
        test_files = []
        for pattern in ["tests/**/*.py", "zeta_vn/tests/**/*.py"]:
            test_files.extend(self.project_root.glob(pattern))
        for file_path in test_files:
            if self._fix_f821_in_file(file_path):
                self.stats["f821_fixed"] += 1
                print(f"  ✓ Fixed F821 in {file_path.relative_to(self.project_root)}")

    def _fix_f821_in_file(self, file_path: Path) -> bool:
        """Sửa lỗi F821 trong một test file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content
            fixes = [
                (
                    r"(\s+)await\s+[^.]+\.create_user_session\([^)]+\)\s*$",
                    r"\1user_session = await system_orchestrator.create_user_session(user_data)",
                ),
                (
                    r"(\s+)await\s+[^.]+\.create_agent_and_conversation\([^)]+\)\s*$",
                    r"\1agent_result = await system_orchestrator.create_agent_and_conversation(",
                ),
                (
                    r"(\s+)await\s+[^.]+\.create_connection\([^)]+\)\s*$",
                    r"\1user = await ws_manager.create_connection(",
                ),
                (r"(\s+)await\s+[^.]+\.ping\(\)\s*$", r"\1ping_result = await connection.ping()"),
                (r"(\s+)await\s+[^.]+\.pong\(\)\s*$", r"\1pong_result = await connection.pong()"),
                (
                    r"(\s+for\s+\w+\s+in\s+range\([^)]+\):\s*\n\s+)await\s+([^.]+\.[^(]+\([^)]*\))\s*$",
                    r"\1result = await \2",
                ),
            ]
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            specific_fixes = {
                "users.append(user)": "users.append(user_session)",
                "agents_and_conversations.append(agent_result)": "agents_and_conversations.append(agent_result)",
                "assert agent[": 'assert agent_result["agent"][',
                "if agent.name": "if deleted_agent.name",
                "del self.agents_by_name[agent.name]": "del self.agents_by_name[deleted_agent.name]",
                "assert result.": "assert load_result.",
                "data.append(result)": "data.append(memory_result)",
                "chat_results.append(chat_result)": "chat_results.append(chat_result)",
                "memory_results.append(memory_result)": "memory_results.append(memory_result)",
            }
            for old, new in specific_fixes.items():
                content = content.replace(old, new)
            content = re.sub(r"automation:plan:create\s*=", r"user_with_perms =", content)
            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                return True
            return False
        except Exception as e:
            print(f"  ❌ Error fixing F821 in {file_path}: {e}")
            return False

    def _fix_import_order(self) -> None:
        """Sửa import order issues."""
        print("📦 Fixing import order...")
        py_files = list(self.project_root.glob("**/*.py"))
        for file_path in py_files:
            if self._fix_imports_in_file(file_path):
                self.stats["imports_fixed"] += 1
                print(f"  ✓ Fixed imports in {file_path.relative_to(self.project_root)}")

    def _fix_imports_in_file(self, file_path: Path) -> bool:
        """Sửa import order trong một file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            if not lines:
                return False
            future_imports = []
            standard_imports = []
            third_party_imports = []
            local_imports = []
            other_lines = []
            import_started = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("from __future__"):
                    future_imports.append(line)
                    import_started = True
                elif stripped.startswith(("import ", "from ")) and not stripped.startswith("from __future__"):
                    import_started = True
                    if self._is_standard_library(stripped):
                        standard_imports.append(line)
                    elif self._is_local_import(stripped):
                        local_imports.append(line)
                    else:
                        third_party_imports.append(line)
                elif import_started and (stripped == "" or stripped.startswith("#")):
                    continue
                else:
                    other_lines.append(line)
            new_lines = []
            if future_imports:
                new_lines.extend(future_imports)
                new_lines.append("")
            if standard_imports:
                new_lines.extend(sorted(set(standard_imports)))
                new_lines.append("")
            if third_party_imports:
                new_lines.extend(sorted(set(third_party_imports)))
                new_lines.append("")
            if local_imports:
                new_lines.extend(sorted(set(local_imports)))
                new_lines.append("")
            new_lines.extend(other_lines)
            new_content = "\n".join(new_lines)
            if new_content != content:
                file_path.write_text(new_content, encoding="utf-8")
                return True
            return False
        except Exception as e:
            print(f"  ❌ Error fixing imports in {file_path}: {e}")
            return False

    def _is_standard_library(self, import_line: str) -> bool:
        """Check if import is from standard library."""
        stdlib_modules = {
            "asyncio",
            "collections",
            "datetime",
            "functools",
            "json",
            "logging",
            "os",
            "pathlib",
            "re",
            "sys",
            "time",
            "typing",
            "uuid",
            "warnings",
            "abc",
            "dataclasses",
            "enum",
            "inspect",
            "itertools",
            "operator",
            "traceback",
            "weakref",
            "contextlib",
            "copy",
            "math",
            "random",
            "string",
            "tempfile",
            "shutil",
            "subprocess",
            "concurrent",
            "threading",
            "multiprocessing",
            "queue",
            "socket",
            "ssl",
            "urllib",
            "http",
            "email",
            "base64",
            "hashlib",
            "hmac",
            "secrets",
            "pickle",
            "csv",
            "xml",
            "html",
            "sqlite3",
            "gzip",
            "zipfile",
            "tarfile",
        }
        if import_line.startswith("from ") or import_line.startswith("import "):
            module = import_line.split()[1].split(".")[0]
        else:
            return False
        return module in stdlib_modules

    def _is_local_import(self, import_line: str) -> bool:
        """Check if import is local to project."""
        return "zeta_vn" in import_line or "desktop_ai_zeta" in import_line

    def _print_stats(self) -> None:
        """In thống kê kết quả."""
        print("\n📊 Auto-fix Statistics:")
        print(f"  Files processed: {self.stats['files_processed']}")
        print(f"  __all__ added: {self.stats['all_added']}")
        print(f"  F821 errors fixed: {self.stats['f821_fixed']}")
        print(f"  Import orders fixed: {self.stats['imports_fixed']}")
        print("\n✅ Auto-fix completed!")


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    fixer = CodeAutoFixer(project_root)
    fixer.run()


if __name__ == "__main__":
    main()
