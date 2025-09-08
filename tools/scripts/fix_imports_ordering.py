from __future__ import annotations

import os
import subprocess
from pathlib import Path
import Exception
import d
import dirs
import e
import enumerate
import file
import files
import i
import len
import print
import py_file
import root

"""
Fix Import Ordering with Ruff
=============================
Use ruff to automatically fix import ordering issues.
"""


def fix_import_ordering():
    """Fix import ordering in all Python files using ruff."""
    project_root = Path(__file__).parent.parent
    python_files = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__" and d != ".venv"]
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    fixed_count = 0
    total_files = len(python_files)
    print(f"🔧 Processing {total_files} Python files...")
    for i, py_file in enumerate(python_files):
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", "--fix", "--select=I", py_file],
                capture_output=True,
                text=True,
                cwd=project_root,
            )
            if result.returncode == 0 and result.stdout.strip():
                print(f"✅ Fixed imports in {py_file}")
                fixed_count += 1
            elif result.returncode != 0:
                print(f"⚠️  Error fixing {py_file}: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Exception fixing {py_file}: {e}")
        if (i + 1) % 50 == 0:
            print(f"📊 Progress: {i + 1}/{total_files} files processed")
    print(f"\n🎉 Fixed import ordering in {fixed_count} files")
    return fixed_count


if __name__ == "__main__":
    fix_import_ordering()
