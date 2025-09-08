#!/usr/bin/env python3
"""
ZETA AI Project Restructuring Tool
Implements Clean Architecture and Domain-Driven Design
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
import Exception
import any
import base_path
import check
import content
import dict
import dir_name
import e
import f
import file_path
import isinstance
import item
import len
import list
import name
import open
import parent
import pattern
import print
import self
import skip
import src_pattern
import str
import structure

# Constants cho cấu trúc thư mục
BACKEND_ROOT = Path("zeta_vn")
FRONTEND_ROOT = Path("desktop_ai_zeta")
INIT_PY = "__init__.py"

# Cấu trúc Clean Architecture cho Backend
CLEAN_ARCHITECTURE_STRUCTURE = {
    "app": {
        "api": {"v1": {}, "v2": {}},
        "websockets": {},
        "controllers": {},
        "middlewares": {},
        "dependencies.py": None,
        "__init__.py": None,
    },
    "core": {
        "domain": {
            "entities": {},
            "aggregates": {},
            "value_objects": {},
            "events": {},
            "specifications": {},
        },
        "use_cases": {
            "agent": {},
            "user": {},
            "chat": {},
            "training": {},
            "memory": {},
        },
        "services": {
            "domain": {},
            "application": {},
        },
        "interfaces": {
            "repositories": {},
            "services": {},
            "gateways": {},
        },
        "__init__.py": None,
    },
    "data": {
        "models": {},
        "repositories": {},
        "database": {
            "migrations": {},
            "seeds": {},
        },
        "external": {
            "apis": {},
            "ai_services": {},
        },
        "__init__.py": None,
    },
    "config": {
        "settings.py": None,
        "constants.py": None,
        "__init__.py": None,
    },
    "tests": {
        "unit": {
            "core": {},
            "app": {},
            "data": {},
        },
        "integration": {},
        "e2e": {},
        "fixtures": {},
        "__init__.py": None,
    },
}

# Cấu trúc cho Frontend
FRONTEND_STRUCTURE = {
    "src": {
        "components": {
            "common": {},
            "dashboard": {},
            "chat": {},
            "training": {},
            "control": {},
        },
        "services": {
            "api": {},
            "websocket": {},
            "system": {},
        },
        "hooks": {},
        "utils": {},
        "types": {},
        "stores": {},
        "i18n": {},
        "electron": {
            "main": {},
            "preload": {},
            "ipc": {},
        },
    },
}


class ProjectRestructurer:
    """Tool để tái cấu trúc dự án theo Clean Architecture"""

    def __init__(self) -> None:
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / "backups" / f"restructure_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.report: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "files_moved": [],
            "files_deleted": [],
            "directories_created": [],
            "errors": [],
        }

    def create_backup(self) -> None:
        """Tạo backup toàn bộ dự án trước khi restructure"""
        print("🔄 Creating project backup...")

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Backup critical directories
        critical_dirs = ["zeta_vn", "desktop_ai_zeta", ".github", "config", "tests"]

        for dir_name in critical_dirs:
            src_dir = self.project_root / dir_name
            if src_dir.exists():
                dst_dir = self.backup_dir / dir_name
                shutil.copytree(
                    src_dir,
                    dst_dir,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", "node_modules", ".git"),
                )
                print(f"  ✅ Backed up: {dir_name}")

    def analyze_duplicate_files(self) -> list[Path]:
        """Phân tích và tìm các file duplicate"""
        print("🔍 Analyzing duplicate files...")

        duplicate_patterns = [
            "*_copy*",
            "*_backup*",
            "*_old*",
            "*_v2*",
            "*_simple*",
            "*_new*",
            "*_temp*",
            "*_test*",
            "*_demo*",
            "*(1)*",
        ]

        duplicates = []
        for pattern in duplicate_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file() and not any(
                    skip in str(file_path) for skip in [".git", "__pycache__", "node_modules"]
                ):
                    duplicates.append(file_path)

        print(f"  🔍 Found {len(duplicates)} potential duplicate files")
        return duplicates

    def create_directory_structure(self, base_path: Path, structure: dict[str, Any]) -> None:
        """Tạo cấu trúc thư mục theo Clean Architecture"""
        for name, content in structure.items():
            dir_path = base_path / name

            if content is None:  # Đây là file
                continue
            elif isinstance(content, dict):  # Đây là directory
                dir_path.mkdir(parents=True, exist_ok=True)
                self.report["directories_created"].append(str(dir_path))

                # Tạo __init__.py cho Python packages
                if base_path.name == "zeta_vn" or any(parent.name == "zeta_vn" for parent in base_path.parents):
                    init_file = dir_path / "__init__.py"
                    if not init_file.exists():
                        init_file.write_text("# Auto-generated __init__.py\n")

                # Đệ quy tạo subdirectories
                if content:
                    self.create_directory_structure(dir_path, content)

    def phase1_cleanup_duplicates(self) -> None:
        """Phase 1: Cleanup duplicate files"""
        print("\n🚀 PHASE 1: Cleanup Duplicate Files")

        duplicates = self.analyze_duplicate_files()

        # Backup và xóa duplicates
        for file_path in duplicates:
            try:
                # Backup file trước khi xóa
                backup_path = self.backup_dir / "duplicates" / file_path.relative_to(self.project_root)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)

                # Xóa file duplicate
                file_path.unlink()
                self.report["files_deleted"].append(str(file_path))
                print(f"  🗑️  Removed: {file_path}")

            except Exception as e:
                self.report["errors"].append(f"Error removing {file_path}: {str(e)}")
                print(f"  ❌ Error removing {file_path}: {e}")

        self.report["phases"]["phase1"] = {
            "duplicates_found": len(duplicates),
            "duplicates_removed": len(self.report["files_deleted"]),
        }

    def phase2_create_structure(self) -> None:
        """Phase 2: Tạo cấu trúc Clean Architecture"""
        print("\n🏗️  PHASE 2: Create Clean Architecture Structure")

        # Tạo cấu trúc Backend
        print("  📦 Creating backend structure...")
        self.create_directory_structure(BACKEND_ROOT, CLEAN_ARCHITECTURE_STRUCTURE)

        # Tạo cấu trúc Frontend
        print("  🖥️  Creating frontend structure...")
        self.create_directory_structure(FRONTEND_ROOT, FRONTEND_STRUCTURE)

        self.report["phases"]["phase2"] = {
            "directories_created": len(self.report["directories_created"]),
        }

    def phase3_move_existing_files(self) -> None:
        """Phase 3: Di chuyển files hiện có vào cấu trúc mới"""
        print("\n📁 PHASE 3: Migrate Existing Files")

        # Mapping rules để di chuyển files
        migration_rules = [
            # Domain entities
            ("zeta_vn/core/entities", "zeta_vn/core/domain/entities"),
            ("zeta_vn/core/value_objects", "zeta_vn/core/domain/value_objects"),
            ("zeta_vn/core/events", "zeta_vn/core/domain/events"),
            # Use cases
            ("zeta_vn/use_cases", "zeta_vn/core/use_cases"),
            # Data layer
            ("zeta_vn/models", "zeta_vn/data/models"),
            ("zeta_vn/repositories", "zeta_vn/data/repositories"),
            ("zeta_vn/database", "zeta_vn/data/database"),
            # API layer
            ("zeta_vn/routers", "zeta_vn/app/api/v1"),
            ("zeta_vn/api", "zeta_vn/app/api"),
            # Config
            ("zeta_vn/settings", "zeta_vn/config"),
        ]

        for src_pattern, dst_dir in migration_rules:
            src_path = Path(src_pattern)
            dst_path = Path(dst_dir)

            if src_path.exists():
                try:
                    dst_path.mkdir(parents=True, exist_ok=True)

                    for item in src_path.iterdir():
                        if item.is_file():
                            dst_file = dst_path / item.name
                            if not dst_file.exists():
                                shutil.move(str(item), str(dst_file))
                                self.report["files_moved"].append(f"{item} -> {dst_file}")
                                print(f"  📂 Moved: {item} -> {dst_file}")

                    # Xóa thư mục cũ nếu trống
                    if src_path.exists() and not any(src_path.iterdir()):
                        src_path.rmdir()
                        print(f"  🗑️  Removed empty directory: {src_path}")

                except Exception as e:
                    self.report["errors"].append(f"Error migrating {src_pattern}: {str(e)}")
                    print(f"  ❌ Error migrating {src_pattern}: {e}")

        self.report["phases"]["phase3"] = {
            "files_moved": len(self.report["files_moved"]),
        }

    def phase4_fix_imports(self) -> None:
        """Phase 4: Fix imports sau khi di chuyển files"""
        print("\n🔧 PHASE 4: Fix Import Statements")

        try:
            # Chạy automated import fixing
            result = subprocess.run(
                ["uv", "run", "python", "-m", "ruff", "check", ".", "--fix", "--unsafe-fixes"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            print(f"  📝 Ruff auto-fix result: {result.returncode}")
            if result.stdout:
                print(f"  📋 Output: {result.stdout[:500]}...")

        except Exception as e:
            self.report["errors"].append(f"Error fixing imports: {str(e)}")
            print(f"  ❌ Error fixing imports: {e}")

        self.report["phases"]["phase4"] = {
            "import_fixes_attempted": True,
        }

    def phase5_quality_check(self) -> None:
        """Phase 5: Chạy quality checks"""
        print("\n✅ PHASE 5: Quality Assurance")

        quality_checks = [
            ["uv", "run", "ruff", "check", ".", "--statistics"],
            ["uv", "run", "mypy", "zeta_vn", "--ignore-missing-imports"],
            ["uv", "run", "pytest", "tests/unit", "-q", "--tb=short"],
        ]

        for check in quality_checks:
            try:
                result = subprocess.run(check, capture_output=True, text=True, cwd=self.project_root)
                tool_name = check[2]  # ruff, mypy, pytest
                print(f"  🔍 {tool_name}: {'✅ PASS' if result.returncode == 0 else '❌ FAIL'}")

                if result.returncode != 0:
                    print(f"    📋 {result.stdout[:200]}...")

            except Exception as e:
                print(f"  ❌ Error running {check[2]}: {e}")

    def generate_report(self) -> None:
        """Tạo báo cáo tái cấu trúc"""
        report_file = self.project_root / "RESTRUCTURE_REPORT.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Restructure report saved to: {report_file}")

        # Summary
        print("\n🎯 RESTRUCTURE SUMMARY:")
        print(f"  📁 Directories created: {len(self.report['directories_created'])}")
        print(f"  📂 Files moved: {len(self.report['files_moved'])}")
        print(f"  🗑️  Files deleted: {len(self.report['files_deleted'])}")
        print(f"  ❌ Errors: {len(self.report['errors'])}")

    def run_full_restructure(self) -> None:
        """Chạy toàn bộ quy trình tái cấu trúc"""
        print("🚀 Starting ZETA AI Project Restructuring...")
        print("📋 Following Clean Architecture & Domain-Driven Design patterns")

        try:
            self.create_backup()
            self.phase1_cleanup_duplicates()
            self.phase2_create_structure()
            self.phase3_move_existing_files()
            self.phase4_fix_imports()
            self.phase5_quality_check()
            self.generate_report()

            print("\n🎉 Project restructuring completed!")
            print("📖 Check RESTRUCTURE_REPORT.json for detailed results")

        except Exception as e:
            print(f"\n💥 Critical error during restructuring: {e}")
            self.report["errors"].append(f"Critical error: {str(e)}")
            self.generate_report()


if __name__ == "__main__":
    restructurer = ProjectRestructurer()
    restructurer.run_full_restructure()
