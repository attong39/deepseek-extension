#!/usr/bin/env python3
"""
Phase 1: Cleanup duplicate files theo priority
"""

from __future__ import annotations

from pathlib import Path
import Exception
import any
import bool
import config
import duplicate_file
import e
import enumerate
import f
import file_path
import int
import len
import line
import new_import
import next_line
import old_import
import open
import print
import py_file
import source
import str
import success
import target
import tline
import total
import tuple

# Files duplicate và strategy xử lý
DUPLICATE_CLEANUP_PLAN = {
    # High priority - AI core files
    "zeta_vn/app/ai/demo_simple.py": {
        "action": "merge_to",
        "target": "zeta_vn/app/ai/demo_setup.py",
        "reason": "Keep full-featured demo_setup.py, merge simple logic if needed",
    },
    "zeta_vn/app/ai/orchestrator_simple.py": {
        "action": "merge_to",
        "target": "zeta_vn/app/ai/orchestrator.py",
        "reason": "Keep main orchestrator, merge simple patterns",
    },
    "zeta_vn/app/ai/chat/service_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/ai/chat/service.py",
        "reason": "Main service.py more complete",
    },
    # RAG duplicates - highest impact
    "zeta_vn/app/ai/rag/chunking_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/ai/rag/chunking.py",
        "reason": "Main chunking.py more feature-rich",
    },
    "zeta_vn/app/ai/rag/chunking_clean.py": {
        "action": "merge_to",
        "target": "zeta_vn/app/ai/rag/chunking.py",
        "reason": "Merge clean patterns into main chunking",
    },
    "zeta_vn/app/ai/rag/pipeline_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/ai/rag/pipeline.py",
        "reason": "Main pipeline more comprehensive",
    },
    "zeta_vn/app/ai/rag/production_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/ai/rag/production_service.py",
        "reason": "production_service.py is the main implementation",
    },
    "zeta_vn/app/ai/rag/cross_encoder_reranker_backup.py": {
        "action": "delete",
        "target": "zeta_vn/app/ai/rag/cross_encoder_reranker.py",
        "reason": "Remove backup file",
    },
    # GraphQL duplicates
    "zeta_vn/app/api/graphql/resolvers_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/api/graphql/resolvers.py",
        "reason": "Keep main resolvers implementation",
    },
    "zeta_vn/app/api/graphql/schema_simple.py": {
        "action": "delete",
        "target": "zeta_vn/app/api/graphql/schema.py",
        "reason": "Keep main schema implementation",
    },
}


def backup_file(file_path: str) -> bool:
    """Backup file trước khi xử lý"""
    try:
        src = Path(file_path)
        if not src.exists():
            return True

        backup_dir = Path("archive/phase1_backup")
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create relative path structure
        rel_path = src.relative_to(Path.cwd())
        backup_file = backup_dir / rel_path
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        import shutil

        shutil.copy2(src, backup_file)
        print(f"  📦 Backed up: {file_path}")
        return True
    except Exception as e:
        print(f"  ❌ Backup failed for {file_path}: {e}")
        return False


def merge_file_content(source: str, target: str) -> bool:
    """Merge useful content từ source vào target"""
    try:
        source_path = Path(source)
        target_path = Path(target)

        if not source_path.exists():
            print(f"  ⚠️  Source not found: {source}")
            return True

        if not target_path.exists():
            print(f"  ⚠️  Target not found: {target}")
            return False

        # Read both files
        with open(source_path, encoding="utf-8") as f:
            source_content = f.read()

        with open(target_path, encoding="utf-8") as f:
            target_content = f.read()

        # Simple heuristic: if source has unique functions/classes, append them
        source_lines = source_content.split("\n")
        target_lines = target_content.split("\n")

        # Look for unique function/class definitions
        unique_content = []
        for line in source_lines:
            line_stripped = line.strip()
            if line_stripped.startswith(("def ", "class ", "async def ")):
                func_name = line_stripped.split("(")[0].split()[-1]
                # Check if this function exists in target
                if not any(func_name in tline for tline in target_lines):
                    unique_content.append(f"# Merged from {source_path.name}")
                    unique_content.append(line)
                    # Add function body (simple implementation)
                    indent_level = len(line) - len(line.lstrip())
                    for i, next_line in enumerate(source_lines[source_lines.index(line) + 1 :], 1):
                        if next_line.strip() and len(next_line) - len(next_line.lstrip()) <= indent_level:
                            break
                        unique_content.append(next_line)

        if unique_content:
            # Append unique content to target
            with open(target_path, "a", encoding="utf-8") as f:
                f.write("\n\n# === MERGED CONTENT ===\n")
                f.write("\n".join(unique_content))
            print(f"  ✅ Merged unique content from {source} to {target}")
        else:
            print(f"  ℹ️  No unique content to merge from {source}")

        return True
    except Exception as e:
        print(f"  ❌ Merge failed: {e}")
        return False


def delete_file(file_path: str) -> bool:
    """Xóa file sau khi backup"""
    try:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            print(f"  🗑️  Deleted: {file_path}")
        return True
    except Exception as e:
        print(f"  ❌ Delete failed: {e}")
        return False


def cleanup_duplicates() -> tuple[int, int]:
    """Cleanup tất cả duplicate files"""
    success_count = 0
    total_count = len(DUPLICATE_CLEANUP_PLAN)

    print(f"🧹 Bắt đầu cleanup {total_count} duplicate files...")

    for duplicate_file, config in DUPLICATE_CLEANUP_PLAN.items():
        print(f"\n📁 Xử lý: {duplicate_file}")
        print(f"   Strategy: {config['action']} -> {config.get('target', 'N/A')}")
        print(f"   Reason: {config['reason']}")

        # Backup first
        if not backup_file(duplicate_file):
            continue

        # Execute action
        if config["action"] == "merge_to":
            if merge_file_content(duplicate_file, config["target"]):
                if delete_file(duplicate_file):
                    success_count += 1
        elif config["action"] == "delete":
            if delete_file(duplicate_file):
                success_count += 1
        else:
            print(f"  ⚠️  Unknown action: {config['action']}")

    return success_count, total_count


def update_imports_after_cleanup():
    """Update imports sau khi cleanup files"""
    print("\n🔗 Updating imports after cleanup...")

    # Simple find/replace for common import patterns
    import_updates = {
        "from apps.backend.app.ai.demo_simple import": "from apps.backend.app.ai.demo_setup import",
        "from apps.backend.app.ai.orchestrator_simple import": "from apps.backend.app.ai.orchestrator import",
        "from apps.backend.app.ai.rag.chunking_simple import": "from apps.backend.app.ai.rag.chunking import",
        "from apps.backend.app.ai.rag.pipeline_simple import": "from apps.backend.app.ai.rag.pipeline import",
        "from apps.backend.app.ai.rag.production_simple import": "from apps.backend.app.ai.rag.production_service import",
    }

    # Find all Python files and update imports
    updated_files = 0
    for py_file in Path("zeta_vn").rglob("*.py"):
        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            original_content = content
            for old_import, new_import in import_updates.items():
                content = content.replace(old_import, new_import)

            if content != original_content:
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(content)
                updated_files += 1
                print(f"  ✅ Updated imports in: {py_file}")

        except Exception as e:
            print(f"  ⚠️  Failed to update {py_file}: {e}")

    print(f"📊 Updated imports in {updated_files} files")


def main():
    """Main execution for Phase 1"""
    print("🚀 PHASE 1: CLEANUP DUPLICATE FILES")

    # 1. Cleanup duplicates
    success, total = cleanup_duplicates()

    # 2. Update imports
    update_imports_after_cleanup()

    # 3. Summary
    print(f"""
✅ PHASE 1 HOÀN TẤT!

📊 Kết quả:
- Đã xử lý: {success}/{total} files
- Success rate: {success / total * 100:.1f}%

🎯 Sẵn sàng cho Phase 2: Layer reorganization
""")


if __name__ == "__main__":
    main()
