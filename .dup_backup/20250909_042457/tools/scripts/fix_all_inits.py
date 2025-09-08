#!/usr/bin/env python3
"""Script tự động sửa tất cả các vấn đề __init__.py files."""

from __future__ import annotations

import re
from pathlib import Path

INIT_FILE_NAME = "__init__.py"


def add_future_annotations(file_path: Path) -> bool:
    """Thêm from __future__ import annotations vào file."""
import Exception
import bool
import dir_path
import e
import enumerate
import f
import file_path
import i
import int
import j
import len
import line
import list
import open
import part
import print
import py_file
import range
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Skip nếu đã có __future__ imports
        if "from __future__" in content:
            return False

        lines = content.split("\n")

        # Tìm vị trí để chèn __future__ import
        insert_pos = 0

        # Skip shebang và encoding
        for i, line in enumerate(lines):
            if line.startswith("#") and ("shebang" in line or "coding" in line or "encoding" in line):
                insert_pos = i + 1
            elif line.strip() == '"""' or line.strip().startswith('"""'):
                # Tìm kết thúc docstring
                if line.strip() == '"""':
                    # Multi-line docstring
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().endswith('"""'):
                            insert_pos = j + 1
                            break
                elif line.strip().startswith('"""') and line.strip().endswith('"""'):
                    # Single-line docstring
                    insert_pos = i + 1
                break
            elif line.strip() and not line.startswith("#"):
                # First non-comment, non-docstring line
                break

        # Chèn __future__ import
        lines.insert(insert_pos, "from __future__ import annotations")
        if insert_pos > 0 and lines[insert_pos - 1].strip():
            lines.insert(insert_pos, "")  # Thêm dòng trống
        if insert_pos + 1 < len(lines) and lines[insert_pos + 1].strip():
            lines.insert(insert_pos + 1, "")  # Thêm dòng trống sau

        # Ghi lại file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return True

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def add_missing_docstring(file_path: Path) -> bool:
    """Thêm module docstring nếu thiếu."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Skip nếu đã có docstring
        if '"""' in content or "'''" in content:
            return False

        lines = content.split("\n")

        # Tìm vị trí để chèn docstring (sau __future__ imports)
        insert_pos = 0

        for i, line in enumerate(lines):
            if line.strip().startswith("from __future__"):
                insert_pos = i + 1
                # Skip empty lines
                while insert_pos < len(lines) and not lines[insert_pos].strip():
                    insert_pos += 1
                break

        # Tạo docstring dựa trên path
        relative_path = file_path.relative_to(Path("zeta_vn"))
        parts = relative_path.parts[:-1]  # Remove __init__.py

        if not parts:
            docstring = '"""ZETA_VN package."""'
        else:
            module_name = " ".join(part.replace("_", " ").title() for part in parts)
            docstring = f'"""{module_name} module."""'

        # Chèn docstring
        lines.insert(insert_pos, docstring)
        if insert_pos > 0 and lines[insert_pos - 1].strip():
            lines.insert(insert_pos, "")  # Thêm dòng trống trước
        if insert_pos + 1 < len(lines) and lines[insert_pos + 1].strip():
            lines.insert(insert_pos + 1, "")  # Thêm dòng trống sau

        # Ghi lại file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return True

    except Exception as e:
        print(f"❌ Error adding docstring to {file_path}: {e}")
        return False


def add_missing_all_declaration(file_path: Path) -> bool:
    """Thêm __all__ declaration nếu cần thiết."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Skip nếu đã có __all__
        if "__all__" in content:
            return False

        # Check nếu có exports (def, class, hoặc imports)
        has_exports = bool(re.search(r"^(def |class |from \w+.*import)", content, re.MULTILINE))

        if not has_exports:
            return False

        lines = content.split("\n")

        # Tìm vị trí để chèn __all__ (sau imports, trước exports)
        insert_pos = len(lines)

        for i, line in enumerate(lines):
            if line.strip().startswith(("def ", "class ")):
                insert_pos = i
                break

        # Tạo __all__ declaration
        all_declaration = "__all__ = []  # TODO: Add exports"

        # Chèn __all__
        lines.insert(insert_pos, all_declaration)
        if insert_pos > 0 and lines[insert_pos - 1].strip():
            lines.insert(insert_pos, "")  # Thêm dòng trống trước
        if insert_pos + 1 < len(lines) and lines[insert_pos + 1].strip():
            lines.insert(insert_pos + 1, "")  # Thêm dòng trống sau

        # Ghi lại file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return True

    except Exception as e:
        print(f"❌ Error adding __all__ to {file_path}: {e}")
        return False


def create_missing_init_files(missing_dirs: list[Path]) -> int:
    """Tạo __init__.py files cho các directories thiếu."""
    created = 0

    for dir_path in missing_dirs:
        init_file = dir_path / INIT_FILE_NAME

        try:
            # Tạo docstring dựa trên path
            relative_path = dir_path.relative_to(Path("zeta_vn"))
            parts = relative_path.parts

            if not parts:
                docstring = "ZETA_VN package."
            else:
                module_name = " ".join(part.replace("_", " ").title() for part in parts)
                docstring = f"{module_name} module."

            content = f'''"""#{docstring}"""

from __future__ import annotations

__all__ = []
'''

            with open(init_file, "w", encoding="utf-8") as f:
                f.write(content)

            created += 1
            print(f"✅ Created {init_file}")

        except Exception as e:
            print(f"❌ Error creating {init_file}: {e}")

    return created


def fix_all_init_issues() -> None:
    """Sửa tất cả các vấn đề __init__.py."""
    print("🔧 Fixing all __init__.py issues...")

    # Tìm tất cả __init__.py files
    init_files = list(Path("zeta_vn").rglob(INIT_FILE_NAME))

    stats = {
        "future_added": 0,
        "docstring_added": 0,
        "all_added": 0,
    }

    # Fix existing files
    for init_file in init_files:
        if add_future_annotations(init_file):
            stats["future_added"] += 1

        if add_missing_docstring(init_file):
            stats["docstring_added"] += 1

        if add_missing_all_declaration(init_file):
            stats["all_added"] += 1

    # Tìm và tạo missing files
    missing_dirs = []
    for py_file in Path("zeta_vn").rglob("*.py"):
        if py_file.name == INIT_FILE_NAME:
            continue

        parent = py_file.parent
        init_file = parent / INIT_FILE_NAME

        if not init_file.exists() and parent not in missing_dirs:
            missing_dirs.append(parent)

    created_files = create_missing_init_files(missing_dirs)

    # Report
    print("\n📊 FIX SUMMARY:")
    print(f"  - Added __future__ annotations: {stats['future_added']} files")
    print(f"  - Added docstrings: {stats['docstring_added']} files")
    print(f"  - Added __all__ declarations: {stats['all_added']} files")
    print(f"  - Created missing __init__.py: {created_files} files")
    print(f"\n✅ Total files processed: {len(init_files) + created_files}")


if __name__ == "__main__":
    fix_all_init_issues()
