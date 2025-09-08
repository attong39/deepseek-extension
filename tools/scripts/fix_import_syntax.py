from __future__ import annotations

import re
from pathlib import Path
import Exception
import bool
import e
import enumerate
import f
import file_path
import line
import match
import open
import print
import str

"""
Script sửa lỗi syntax trong các file __init__.py và router files.
Fixes try-except blocks and indentation issues.
"""


def fix_try_except_blocks(content: str) -> str:
    """Sửa các try-except block bị comment out imports."""
    pattern = r"try:\s*\n\s*#\s*from\s+.*?\n\s*except ImportError:"

    def replacement(match):
        return "try:\n    pass  # Import commented out\nexcept ImportError:"

    return re.sub(pattern, replacement, content, flags=re.MULTILINE)


def fix_indentation_issues(content: str) -> str:
    """Sửa các lỗi indentation."""
    lines = content.split("\n")
    fixed_lines = []
    for i, line in enumerate(lines):
        if (
            line.strip().startswith("return ")
            and line.startswith("        ")
            or line.strip().startswith("if not ")
            and line.startswith("        ")
        ):
            fixed_line = "    " + line.strip()
            fixed_lines.append(fixed_line)
        elif line.strip().startswith("raise ") and line.startswith("        "):
            fixed_line = "        " + line.strip()  # Indent under if
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    return "\n".join(fixed_lines)


def fix_incomplete_functions(content: str) -> str:
    """Sửa các function không hoàn chỉnh."""
    pattern = r'(async def \w+\([^)]*\):\s*\n\s*"""[^"]*"""\s*\n)(\s*@)'

    def replacement(match):
        return match.group(1) + "    pass\n\n" + match.group(2)

    return re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)


def fix_file(file_path: Path) -> bool:
    """Sửa một file cụ thể."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        original_content = content
        content = fix_try_except_blocks(content)
        content = fix_indentation_issues(content)
        content = fix_incomplete_functions(content)
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"📄 No changes: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False


def main():
    """Main function."""
    print("🔧 FIXING IMPORT SYNTAX ERRORS")
    print("=" * 50)
    files_to_fix = [
        "zeta_vn/app/api/v1/__init__.py",
        "zeta_vn/app/api/v2/__init__.py",
        "zeta_vn/app/deps/__init__.py",
        "zeta_vn/app/middleware/__init__.py",
        "zeta_vn/core/services/__init__.py",
        "zeta_vn/app/api/v1/agent/router.py",
        "zeta_vn/app/api/v1/voice.py",
    ]
    fixed_count = 0
    total_count = 0
    for file_path in files_to_fix:
        full_path = Path(file_path)
        if full_path.exists():
            total_count += 1
            if fix_file(full_path):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    print("\n" + "=" * 50)
    print(f"📊 SUMMARY: Fixed {fixed_count}/{total_count} files")
    if fixed_count > 0:
        print("🚀 Now run: uv run ruff check . --select I --fix")


if __name__ == "__main__":
    main()
