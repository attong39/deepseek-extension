from pathlib import Path
from typing import Any

import yaml
import Exception
import all
import any
import bool
import dict
import dup
import e
import f
import file_path
import isinstance
import item
import len
import line
import list
import open
import placeholder
import print
import str

"""
Sửa file trùng lặp theo queue.yml - SAFE_REPAIR_PLAYBOOK
"""
ROOT = Path(__file__).resolve().parents[2]


def load_queue() -> dict[str, Any]:
    """Load repair queue from YAML"""
    queue_file = ROOT / "scripts/repair/queue.yml"
    if not queue_file.exists():
        return {}
    with open(queue_file, encoding="utf-8") as f:
        content = f.read()
        lines = [line for line in content.split("\n") if not line.strip().startswith("#")]
        yaml_content = "\n".join(lines)
        return yaml.safe_load(yaml_content) or {}


def is_file_empty_or_placeholder(file_path: Path) -> bool:
    """Check if file is empty or contains only placeholder content"""
    if not file_path.exists():
        return True
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        if not content:
            return True
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        if all(line.startswith("#") or line.startswith('"""') or line.startswith("'''") for line in lines):
            return True
        if "AUTO-GENERATED STUB" in content and "TODO: Implement" in content:
            return True
        placeholders = [
            "# TODO",
            "# PLACEHOLDER",
            "pass",
            "...",
            "NotImplemented",
            "# This file is auto-generated",
            "# Empty file",
            "from __future__ import annotations",
        ]
        content_lines = [
            line.strip()
            for line in content.split("\n")
            if line.strip() and not line.startswith("#") and not line.startswith('"""') and not line.startswith("'''")
        ]
        if len(content_lines) <= 2 and any(placeholder in content for placeholder in placeholders):
            return True
        return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def remove_duplicate_files(canonical: str, duplicates: list[str]) -> list[str]:
    """Remove duplicate files that are empty or placeholders"""
    removed_files = []
    canonical_path = ROOT / canonical
    if not canonical_path.exists():
        print(f"⚠️  Canonical file not found: {canonical}")
        return removed_files
    print(f"📁 Processing group with canonical: {canonical}")
    for dup in duplicates:
        dup_path = ROOT / dup
        if not dup_path.exists():
            print(f"  ⚠️  File not found: {dup}")
            continue
        if is_file_empty_or_placeholder(dup_path):
            print(f"  🗑️  Removing empty/placeholder: {dup}")
            try:
                dup_path.unlink()
                removed_files.append(dup)
            except Exception as e:
                print(f"  ❌ Error removing {dup}: {e}")
        else:
            print(f"  📋 Keeping (has content): {dup}")
    return removed_files


def standardize_init_files(canonical: str, duplicates: list[str]) -> list[str]:
    """Standardize __init__.py files"""
    updated_files = []
    canonical_path = ROOT / canonical
    standard_init = '''"""
Module initialization.
"""
__all__ = []
'''
    print(f"📁 Standardizing __init__.py files with canonical: {canonical}")
    if canonical_path.exists():
        if is_file_empty_or_placeholder(canonical_path):
            canonical_path.write_text(standard_init, encoding="utf-8")
            print(f"  ✅ Updated canonical: {canonical}")
    for dup in duplicates:
        dup_path = ROOT / dup
        if not dup_path.exists():
            print(f"  ⚠️  File not found: {dup}")
            continue
        if is_file_empty_or_placeholder(dup_path):
            dup_path.write_text(standard_init, encoding="utf-8")
            print(f"  ✅ Standardized: {dup}")
            updated_files.append(dup)
        else:
            print(f"  📋 Keeping existing content: {dup}")
    return updated_files


def process_repair_queue() -> None:
    """Process repair queue step by step"""
    queue_data = load_queue()
    if not queue_data:
        print("❌ No repair queue found")
        return
    print("🔧 Starting duplicate file repair process...")
    total_removed = 0
    total_updated = 0
    if isinstance(queue_data, list):
        groups = queue_data
    else:
        groups = queue_data.get("groups", [])
    for item in groups:
        if item is None or not isinstance(item, dict):
            continue
        group = item.get("group", "unknown")
        description = item.get("description", "")
        canonical = item.get("canonical", "")
        duplicates = item.get("duplicates", [])
        action = item.get("action", "remove_if_empty_or_merge_logic")
        print(f"\n📋 Processing group: {group}")
        print(f"   Description: {description}")
        print(f"   Action: {action}")
        if not canonical or not duplicates:
            print("   ⚠️  Skipping - missing canonical or duplicates")
            continue
        if action == "remove_if_empty_or_merge_logic":
            removed = remove_duplicate_files(canonical, duplicates)
            total_removed += len(removed)
        elif action == "standardize_init_files":
            updated = standardize_init_files(canonical, duplicates)
            total_updated += len(updated)
        else:
            print(f"   ⚠️  Unknown action: {action}")
    print("\n✅ Repair process completed!")
    print(f"   📊 Files removed: {total_removed}")
    print(f"   📊 Files updated: {total_updated}")
    print("\n💡 Next steps:")
    print("   1. Run: uv run ruff check .")
    print("   2. Run: uv run mypy zeta_vn")
    print("   3. Run: uv run pytest -q")


if __name__ == "__main__":
    process_repair_queue()
