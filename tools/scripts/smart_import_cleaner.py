from __future__ import annotations

import re
import subprocess
from pathlib import Path
import Exception
import bool
import e
import f
import file_content
import file_path_str
import import_name
import l
import len
import open
import print
import self
import set
import sorted
import str
import unused

"""
Script sửa import issues một cách thông minh và an toàn.
Smart and safe import cleanup script.
"""


class SmartImportCleaner:
    """Cleaner thông minh cho imports."""

    def __init__(self):
        self.files_processed = 0
        self.imports_removed = 0
        self.safe_removals = {
            "BarColumn",
            "Progress",
            "SpinnerColumn",
            "TaskProgressColumn",
            "TextColumn",
            "Text",
        }

    def is_safe_to_remove(self, import_name: str, file_content: str) -> bool:
        """Kiểm tra có thể an toàn loại bỏ import không."""
        if f"# {import_name}" in file_content or f"#{import_name}" in file_content:
            return False
        if f'"{import_name}"' in file_content or f"'{import_name}'" in file_content:
            return False
        if import_name in self.safe_removals:
            return True
        usage_patterns = [
            f"{import_name}(",  # Function call
            f"{import_name}.",  # Method access
            f"= {import_name}",  # Assignment
            f"isinstance(..., {import_name})",  # Type check
            f": {import_name}",  # Type annotation
        ]
        for pattern in usage_patterns:
            if pattern in file_content:
                return False
        return True

    def clean_file(self, file_path: Path) -> bool:
        """Làm sạch imports trong một file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
            lines = content.split("\n")
            new_lines = []
            imports_removed_in_file = 0
            for line in lines:
                if "from rich.progress import" in line:
                    unused_imports = [
                        "BarColumn",
                        "Progress",
                        "SpinnerColumn",
                        "TaskProgressColumn",
                        "TextColumn",
                    ]
                    for unused in unused_imports:
                        if unused in line and self.is_safe_to_remove(unused, content):
                            pattern = f",?\\s*{unused}\\s*,?"
                            line = re.sub(pattern, "", line)
                            imports_removed_in_file += 1
                    line = re.sub(r",\s*,", ",", line)  # Double commas
                    line = re.sub(r"import\s*,", "import", line)  # Leading comma
                    line = re.sub(r",\s*$", "", line)  # Trailing comma
                    if "import" in line and not re.search(r"import\s*$", line):
                        new_lines.append(line)
                elif "from rich.text import Text" in line:
                    if self.is_safe_to_remove("Text", content):
                        imports_removed_in_file += 1
                        continue  # Skip this line
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            if imports_removed_in_file > 0:
                new_content = "\n".join(new_lines)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.imports_removed += imports_removed_in_file
                print(f"  ✅ {file_path.name}: removed {imports_removed_in_file} imports")
                return True
            else:
                print(f"  📄 {file_path.name}: no changes needed")
                return False
        except Exception as e:
            print(f"  ❌ {file_path}: {e}")
            return False

    def clean_project(self):
        """Làm sạch toàn bộ project."""
        print("🧹 SMART IMPORT CLEANER")
        print("=" * 40)
        result = subprocess.run("uv run ruff check . --select F401", shell=False, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ No unused imports found!")
            return
        files_to_clean = set()
        for line in result.stdout.split("\n"):
            if "-->" in line:
                file_part = line.split("-->")[1].strip()
                file_path = file_part.split(":")[0].strip()
                files_to_clean.add(file_path)
        print(f"📁 Found {len(files_to_clean)} files with unused imports")
        cleaned_count = 0
        for file_path_str in sorted(files_to_clean):
            file_path = Path(file_path_str)
            if file_path.exists():
                self.files_processed += 1
                if self.clean_file(file_path):
                    cleaned_count += 1
        print("\n📊 SUMMARY:")
        print(f"  📁 Files processed: {self.files_processed}")
        print(f"  ✅ Files cleaned: {cleaned_count}")
        print(f"  🗑️  Imports removed: {self.imports_removed}")
        print("\n🔍 Running final validation...")
        result = subprocess.run("uv run ruff check . --select F401", shell=False, capture_output=True, text=True)
        if result.returncode == 0:
            print("🎉 All unused imports cleaned!")
        else:
            remaining = len([l for l in result.stdout.split("\n") if "F401" in l])
            print(f"📊 {remaining} unused imports remaining (need manual review)")


def main():
    """Main function."""
    cleaner = SmartImportCleaner()
    cleaner.clean_project()
    print("\n💡 NEXT STEPS:")
    print("  • Run: uv run ruff format . (format code)")
    print("  • Run: uv run ruff check . --select I (check import order)")
    print("  • Review any remaining F401 errors manually")


if __name__ == "__main__":
    main()
