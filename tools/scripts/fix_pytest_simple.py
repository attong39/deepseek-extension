from __future__ import annotations

import os
from pathlib import Path
import Exception
import e
import enumerate
import f
import file
import files
import i
import line
import open
import print
import root
import test_file

"""
Simple Auto-Fix for Pytest Imports
==================================
Fix missing pytest imports in test files.
"""


def fix_pytest_imports():
    """Fix missing pytest imports in all test files."""
    project_root = Path(__file__).parent.parent
    test_files = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith(".py") and ("test" in file.lower() or "spec" in file.lower()):
                test_files.append(Path(root) / file)
    fixed_count = 0
    for test_file in test_files:
        try:
            with open(test_file, encoding="utf-8") as f:
                content = f.read()
            has_pytest_usage = "@pytest.fixture" in content or "pytest." in content
            has_pytest_import = "import pytest" in content
            if has_pytest_usage and not has_pytest_import:
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
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ Fixed pytest import in {test_file}")
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error fixing {test_file}: {e}")
    print(f"\n🎉 Fixed pytest imports in {fixed_count} files")
    return fixed_count


if __name__ == "__main__":
    fix_pytest_imports()
