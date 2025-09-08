#!/usr/bin/env python3
"""
Auto-add return type annotations to test functions.

Script để tự động thêm `-> None` type annotations cho các test functions
trong thư mục zeta_vn/tests/core/ để fix mypy errors hàng loạt.
"""

from __future__ import annotations

import re
from pathlib import Path
import Exception
import bool
import e
import file_path
import len
import list
import pattern
import print
import replacement
import test_file


def add_return_type_annotations(file_path: Path) -> bool:
    """
    Thêm `-> None` type annotations cho các test functions trong file.

    Args:
        file_path: Đường dẫn tới file Python test

    Returns:
        True nếu có thay đổi, False nếu không
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Pattern để match test functions thiếu return type annotation
        patterns = [
            # def test_function():
            (r"(def test_\w+\([^)]*\)):", r"\1 -> None:"),
            # def setup_method(self):
            (r"(def setup_method\([^)]*\)):", r"\1 -> None:"),
            # def teardown_method(self):
            (r"(def teardown_method\([^)]*\)):", r"\1 -> None:"),
            # Bất kỳ function nào trong test class
            (r"(def (?:test_\w+|setup_method|teardown_method)\([^)]*\))(\s*):", r"\1 -> None\2:"),
        ]

        changes_made = False
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                changes_made = True

        # Tránh duplicate annotations
        content = re.sub(r"-> None -> None", "-> None", content)

        if changes_made and content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"⏩ No changes: {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main() -> None:
    """Main function to process all test files."""
    test_dir = Path("e:/zeta/zeta_vn/tests/core")

    if not test_dir.exists():
        print(f"❌ Directory not found: {test_dir}")
        return

    # Find all Python test files
    test_files = list(test_dir.rglob("test_*.py"))

    if not test_files:
        print(f"❌ No test files found in {test_dir}")
        return

    print(f"🔍 Found {len(test_files)} test files")

    updated_count = 0
    for test_file in test_files:
        if add_return_type_annotations(test_file):
            updated_count += 1

    print("\n📊 Summary:")
    print(f"   Total files: {len(test_files)}")
    print(f"   Updated: {updated_count}")
    print(f"   Unchanged: {len(test_files) - updated_count}")

    if updated_count > 0:
        print("\n🚀 Run this to check results:")
        print("   cd e:/zeta && uv run mypy zeta_vn/tests/core/ --show-error-codes")


if __name__ == "__main__":
    main()
