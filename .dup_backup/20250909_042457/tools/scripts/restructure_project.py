#!/usr/bin/env python3
"""
Kịch bản tái cấu trúc dự án ZETA_AI theo Clean Architecture
Tự động phân tích, lập kế hoạch và thực hiện migration
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any
import Exception
import bool
import critical_file
import dict
import dup_file
import e
import f
import item
import len
import missing
import open
import pattern
import print
import py_file
import str

# Cấu hình tái cấu trúc
RESTRUCTURE_CONFIG = {
    "backup_dir": "archive/restructure_backup",
    "analysis_report": "reports/restructure_analysis.md",
    "migration_plan": "reports/migration_plan.md",
    # Mapping từ cấu trúc cũ sang mới
    "file_mappings": {
        # Domain layer (core/domain/)
        "zeta_vn/core/domain/entities/": "zeta_vn/core/domain/entities/",
        "zeta_vn/core/domain/value_objects/": "zeta_vn/core/domain/value_objects/",
        "zeta_vn/core/domain/events/": "zeta_vn/core/domain/events/",
        # Use cases (core/use_cases/)
        "zeta_vn/core/use_cases/": "zeta_vn/core/use_cases/",
        # Services (core/services/)
        "zeta_vn/core/services/": "zeta_vn/core/services/",
        # Interfaces/Ports (core/interfaces/)
        "zeta_vn/core/ports/": "zeta_vn/core/interfaces/",
        "zeta_vn/core/adapters/": "zeta_vn/data/adapters/",
        # Application layer (app/)
        "zeta_vn/app/api/": "zeta_vn/app/api/",
        "zeta_vn/app/websockets/": "zeta_vn/app/websockets/",
        "zeta_vn/app/controllers/": "zeta_vn/app/controllers/",
        # Infrastructure layer (data/)
        "zeta_vn/data/models/": "zeta_vn/data/models/",
        "zeta_vn/data/repositories/": "zeta_vn/data/repositories/",
        "zeta_vn/data/database/": "zeta_vn/data/database/",
        "zeta_vn/infrastructure/": "zeta_vn/data/external/",
        # Configuration
        "zeta_vn/config/": "zeta_vn/config/",
        # Tests
        "zeta_vn/tests/": "zeta_vn/tests/",
    },
    # Files để merge/cleanup
    "duplicate_patterns": [
        "_simple.py",
        "_backup.py",
        "_old.py",
        "_copy.py",
        "_v2.py",
        "_clean.py",
        "_optimized.py",
    ],
    # Files quan trọng cần preserve
    "critical_files": [
        "zeta_vn/core/domain/entities/base.py",
        "zeta_vn/core/domain/entities/agent.py",
        "zeta_vn/core/domain/entities/user.py",
        "zeta_vn/app/main_production.py",
        "zeta_vn/config/settings.py",
    ],
}


def analyze_current_structure() -> dict[str, Any]:
    """Phân tích cấu trúc hiện tại"""
    analysis: dict[str, Any] = {
        "total_files": 0,
        "duplicate_files": [],
        "critical_files_missing": [],
        "layer_violations": [],
        "import_cycles": [],
        "files_by_layer": {
            "domain": [],
            "application": [],
            "infrastructure": [],
            "config": [],
            "tests": [],
            "unclear": [],
        },
    }

    zeta_path = Path("zeta_vn")
    if not zeta_path.exists():
        return analysis

    # Scan tất cả Python files
    for py_file in zeta_path.rglob("*.py"):
        analysis["total_files"] += 1

        # Classify by layer
        file_path = str(py_file)
        if "/domain/" in file_path:
            analysis["files_by_layer"]["domain"].append(file_path)
        elif "/app/" in file_path:
            analysis["files_by_layer"]["application"].append(file_path)
        elif "/data/" in file_path or "/infrastructure/" in file_path:
            analysis["files_by_layer"]["infrastructure"].append(file_path)
        elif "/config/" in file_path:
            analysis["files_by_layer"]["config"].append(file_path)
        elif "/tests/" in file_path:
            analysis["files_by_layer"]["tests"].append(file_path)
        else:
            analysis["files_by_layer"]["unclear"].append(file_path)

        # Check for duplicates
        for pattern in RESTRUCTURE_CONFIG["duplicate_patterns"]:
            if pattern in py_file.name:
                analysis["duplicate_files"].append(file_path)
                break

    # Check critical files
    for critical_file in RESTRUCTURE_CONFIG["critical_files"]:
        if not Path(critical_file).exists():
            analysis["critical_files_missing"].append(critical_file)

    return analysis


def create_backup() -> bool:
    """Tạo backup toàn bộ dự án trước khi tái cấu trúc"""
    backup_dir = Path(RESTRUCTURE_CONFIG["backup_dir"])
    backup_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Backup zeta_vn
        if Path("zeta_vn").exists():
            shutil.copytree("zeta_vn", backup_dir / "zeta_vn", dirs_exist_ok=True)

        # Backup desktop_ai_zeta critical files
        if Path("desktop_ai_zeta").exists():
            desktop_backup = backup_dir / "desktop_ai_zeta"
            desktop_backup.mkdir(exist_ok=True)

            # Copy only critical files
            critical_desktop = ["src/", "electron/", "package.json", "tsconfig.json"]
            for item in critical_desktop:
                src = Path("desktop_ai_zeta") / item
                if src.exists():
                    if src.is_file():
                        shutil.copy2(src, desktop_backup / item)
                    else:
                        shutil.copytree(src, desktop_backup / item, dirs_exist_ok=True)

        print(f"✅ Backup hoàn tất tại: {backup_dir}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi backup: {e}")
        return False


def generate_migration_plan(analysis: dict[str, Any]) -> str:
    """Tạo kế hoạch migration chi tiết"""
    plan = f"""# Kế hoạch Migration ZETA_AI

## Phân tích hiện tại
- Tổng files: {analysis["total_files"]}
- Files duplicate: {len(analysis["duplicate_files"])}
- Files thiếu quan trọng: {len(analysis["critical_files_missing"])}

## Files theo layer:
- Domain: {len(analysis["files_by_layer"]["domain"])}
- Application: {len(analysis["files_by_layer"]["application"])}
- Infrastructure: {len(analysis["files_by_layer"]["infrastructure"])}
- Config: {len(analysis["files_by_layer"]["config"])}
- Tests: {len(analysis["files_by_layer"]["tests"])}
- Unclear: {len(analysis["files_by_layer"]["unclear"])}

## Duplicate files cần xử lý:
"""

    for dup_file in analysis["duplicate_files"][:10]:  # Show first 10
        plan += f"- {dup_file}\n"

    plan += """
## Critical files thiếu:
"""
    for missing in analysis["critical_files_missing"]:
        plan += f"- {missing}\n"

    plan += """
## Kế hoạch thực hiện:

### Phase 1: Cleanup duplicates (30 phút)
1. Xác định file chính vs file duplicate
2. Merge logic cần thiết vào file chính
3. Xóa files duplicate
4. Update imports

### Phase 2: Layer reorganization (45 phút)
1. Di chuyển files vào đúng layer
2. Update imports theo Clean Architecture
3. Fix dependency violations

### Phase 3: Domain consolidation (30 phút)
1. Consolidate domain entities
2. Organize value objects
3. Clean up domain events

### Phase 4: Testing & validation (15 phút)
1. Run quality checks
2. Fix broken imports
3. Validate core functionality
"""

    return plan


def main():
    """Main execution"""
    print("🚀 Bắt đầu tái cấu trúc dự án ZETA_AI")

    # 1. Phân tích hiện tại
    print("\n📊 Đang phân tích cấu trúc hiện tại...")
    analysis = analyze_current_structure()

    # 2. Tạo backup
    print("\n💾 Đang tạo backup...")
    if not create_backup():
        print("❌ Không thể tạo backup. Dừng tái cấu trúc.")
        return

    # 3. Tạo migration plan
    print("\n📋 Đang tạo kế hoạch migration...")
    migration_plan = generate_migration_plan(analysis)

    # Save reports
    Path("reports").mkdir(exist_ok=True)
    with open("reports/migration_plan.md", "w", encoding="utf-8") as f:
        f.write(migration_plan)

    print(f"""
✅ Phân tích hoàn tất!

📊 Thống kê:
- Tổng files: {analysis["total_files"]}
- Duplicate files: {len(analysis["duplicate_files"])}
- Files cần migrate: {len(analysis["files_by_layer"]["unclear"])}

📋 Kế hoạch đã lưu tại: reports/migration_plan.md
💾 Backup đã lưu tại: {RESTRUCTURE_CONFIG["backup_dir"]}

🎯 Sẵn sàng bắt đầu Phase 1: Cleanup duplicates
""")


if __name__ == "__main__":
    main()
