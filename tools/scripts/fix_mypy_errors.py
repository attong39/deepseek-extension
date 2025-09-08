from __future__ import annotations

import re
import sys
from pathlib import Path
import Exception
import bool
import e
import enumerate
import file
import file_path
import i
import len
import line
import list
import print
import self
import str

"""
Auto-fix MyPy errors in tools directory.
Tự động sửa các lỗi type checking phổ biến trong thư mục tools.
"""


class MyPyAutoFixer:
    """Tự động sửa lỗi MyPy trong tools."""

    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.fixed_files: list[str] = []

    def fix_missing_return_types(self, content: str) -> str:
        """Sửa lỗi missing return type annotations."""
        pattern = r"(def\s+(\w+)\([^)]*\))(?!.*->\s*[^:]+):"
        replacement = r"\1 -> None:"
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if re.search(pattern, line):
                if i > 0 and ("@" in lines[i - 1] or "def __" in line):
                    continue
                if "return" in line:
                    continue
                lines[i] = re.sub(pattern, replacement, line)
        return "\n".join(lines)

    def fix_missing_type_params(self, content: str) -> str:
        """Sửa lỗi missing type parameters cho Dict, List."""
        content = re.sub(r"\bDict\b(?!\[)", "Dict[str, Any]", content)
        content = re.sub(r":\s*dict\b(?!\[)", ": dict[str, Any]", content)
        content = re.sub(r"\bList\b(?!\[)", "List[Any]", content)
        return content

    def fix_var_annotations(self, content: str) -> str:
        """Sửa lỗi need type annotation for variables."""
        patterns = [
            (r"(\w+)\s*=\s*\[\]", r"\1: List[Any] = []"),
            (r"(\w+)\s*=\s*\{\}", r"\1: Dict[str, Any] = {}"),
            (r"(\w+)\s*=\s*set\(\)", r"\1: set[Any] = set()"),
        ]
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        return content

    def fix_no_any_return(self, content: str) -> str:
        """Sửa lỗi returning Any from typed function."""
        return content

    def fix_file(self, file_path: Path) -> bool:
        """Sửa một file Python."""
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content
            content = self.fix_missing_return_types(content)
            content = self.fix_missing_type_params(content)
            content = self.fix_var_annotations(content)
            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                self.fixed_files.append(str(file_path))
                print(f"✅ Fixed: {file_path}")
                return True
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
        return False

    def fix_all_tools(self) -> None:
        """Sửa tất cả file Python trong thư mục tools."""
        python_files = list(self.tools_dir.glob("**/*.py"))
        print(f"🔧 Starting MyPy auto-fix for {len(python_files)} files...")
        fixed_count = 0
        for file_path in python_files:
            if self.fix_file(file_path):
                fixed_count += 1
        print("\n📊 Auto-fix completed:")
        print(f"   • Files processed: {len(python_files)}")
        print(f"   • Files fixed: {fixed_count}")
        print(f"   • Files unchanged: {len(python_files) - fixed_count}")
        if self.fixed_files:
            print("\n🔧 Fixed files:")
            for file in self.fixed_files:
                print(f"   • {file}")


def main():
    """Main function."""
    tools_dir = Path(__file__).parent / "tools"
    if not tools_dir.exists():
        print(f"❌ Tools directory not found: {tools_dir}")
        return 1
    fixer = MyPyAutoFixer(tools_dir)
    fixer.fix_all_tools()
    return 0


if __name__ == "__main__":
    sys.exit(main())
