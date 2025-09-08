#!/usr/bin/env python
"""
Script an toàn để archive file trùng lặp/thừa thay vì xoá cứng.

Mặc định tạo thư mục _archive và move file. Có chế độ dry-run an toàn.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
import Exception
import bool
import dict
import dir_path
import e
import f
import file_path
import len
import list
import open
import print
import reason
import self
import str
import target
import tuple

# Constants để tránh lặp
CONSOLIDATED_REASON = "Consolidated vào security_consolidated.py"
ANALYSIS_REPORT_REASON = "Analysis report - không cần trong repo"


class SafeCleanupPlan:
    """An toàn archive file thay vì xoá cứng"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.archive_dir = repo_root / "_archive"
        self.cleanup_log: list[dict[str, Any]] = []

    def create_archive_dir(self):
        """Tạo thư mục archive với timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.archive_dir = self.repo_root / f"_archive/{timestamp}"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Tạo archive dir: {self.archive_dir}")

    def archive_file(self, file_path: Path, reason: str = "") -> bool:
        """Move file an toàn vào archive"""
        try:
            if not file_path.exists():
                print(f"⚠️  File không tồn tại: {file_path}")
                return False

            # Tính toán đường dẫn relative để preserve structure
            rel_path = file_path.relative_to(self.repo_root)
            archive_target = self.archive_dir / rel_path

            # Tạo parent dirs trong archive
            archive_target.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.move(str(file_path), str(archive_target))

            log_entry = {
                "original": str(rel_path),
                "archived": str(archive_target.relative_to(self.repo_root)),
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
            }
            self.cleanup_log.append(log_entry)

            print(f"📦 Archived: {rel_path} → {archive_target.relative_to(self.repo_root)}")
            return True

        except Exception as e:
            print(f"❌ Lỗi archive {file_path}: {e}")
            return False

    def archive_directory(self, dir_path: Path, reason: str = "") -> bool:
        """Move thư mục an toàn vào archive"""
        try:
            if not dir_path.exists():
                print(f"⚠️  Thư mục không tồn tại: {dir_path}")
                return False

            rel_path = dir_path.relative_to(self.repo_root)
            archive_target = self.archive_dir / rel_path

            # Move toàn bộ thư mục
            shutil.move(str(dir_path), str(archive_target))

            log_entry = {
                "original": str(rel_path),
                "archived": str(archive_target.relative_to(self.repo_root)),
                "reason": reason,
                "type": "directory",
                "timestamp": datetime.now().isoformat(),
            }
            self.cleanup_log.append(log_entry)

            print(f"📁 Archived dir: {rel_path} → {archive_target.relative_to(self.repo_root)}")
            return True

        except Exception as e:
            print(f"❌ Lỗi archive dir {dir_path}: {e}")
            return False

    def save_log(self):
        """Lưu log cleanup"""
        log_file = self.archive_dir / "cleanup_log.json"
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(self.cleanup_log, f, indent=2, ensure_ascii=False)
        print(f"📋 Lưu log tại: {log_file}")


def get_cleanup_targets() -> list[tuple[str, str]]:
    """Danh sách file/folder cần archive với lý do"""
    return [
        # === API Duplicates ===
        (
            "zeta_vn/app/api/v1/admin_outbox.py",
            "Duplicate - có sẵn trong endpoints/admin_outbox.py",
        ),
        # === WebSocket Duplicates ===
        (
            "zeta_vn/app/realtime/chat_websocket.py",
            "Duplicate - có sẵn trong websockets/chat_websocket.py",
        ),
        ("zeta_vn/app/realtime/__init__.py", "Empty init của thư mục realtime"),
        # === Deps Legacy ===
        ("zeta_vn/app/deps_proposed/", "Legacy deps - merged vào app/deps"),
        # === Security Middleware Consolidation ===
        ("zeta_vn/app/middleware/security/headers.py", CONSOLIDATED_REASON),
        ("zeta_vn/app/middleware/security/security.py", CONSOLIDATED_REASON),
        ("zeta_vn/app/middleware/security/zero_trust.py", CONSOLIDATED_REASON),
        ("zeta_vn/app/middleware/security/__init__.py", "Empty init sau consolidation"),
        # === Main Entry Points ===
        ("zeta_vn/app/main_clean.py", "Redundant entry point - dùng main_production.py"),
        # === Core Security Legacy ===
        (
            "zeta_vn/core/security/permission_manager_old.py",
            "Legacy - thay thế bởi permission_manager.py",
        ),
        # === Data Models Deprecated ===
        ("zeta_vn/data/models/_deprecated/", "Legacy models không dùng"),
        # === Handlers Placeholder ===
        ("zeta_vn/app/handlers/new.prompt.prompt.md", "Placeholder file"),
        # === Root Level Cleanup ===
        ("dead_code_high_confidence.txt", ANALYSIS_REPORT_REASON),
        ("dead_code_report.txt", ANALYSIS_REPORT_REASON),
        ("duplicate_cleanup_report.txt", ANALYSIS_REPORT_REASON),
        ("ruff_output.txt", "Tool output - không cần trong repo"),
        ("ruff_output_after_fix.txt", "Tool output - không cần trong repo"),
        ("optimization_metrics.json", "Report file - chuyển vào reports/"),
        ("project_analysis.json", "Report file - chuyển vào reports/"),
    ]


def run_dry_run(targets: list[tuple[str, str]], repo_root: Path) -> None:
    """Hiển thị dry run plan"""
    print("🔍 DRY RUN - Danh sách file/folder sẽ được archive:")
    print("=" * 60)

    for target, reason in targets:
        target_path = repo_root / target
        status = "✅ EXISTS" if target_path.exists() else "⚠️  NOT FOUND"
        print(f"{status} {target}")
        print(f"   └─ Lý do: {reason}")
        print()

    print(f"📊 Tổng cộng: {len(targets)} targets")
    print("\nChạy với --apply để thực hiện archive")


def run_cleanup(targets: list[tuple[str, str]], repo_root: Path) -> None:
    """Thực hiện cleanup"""
    print("🚀 Bắt đầu cleanup...")
    cleanup = SafeCleanupPlan(repo_root)
    cleanup.create_archive_dir()

    success_count = 0
    for target, reason in targets:
        target_path = repo_root / target

        if target_path.is_dir():
            if cleanup.archive_directory(target_path, reason):
                success_count += 1
        elif target_path.is_file():
            if cleanup.archive_file(target_path, reason):
                success_count += 1
        else:
            print(f"⚠️  Không tìm thấy: {target}")

    cleanup.save_log()
    print(f"\n✅ Hoàn thành! Archived {success_count}/{len(targets)} targets")
    print(f"📦 Archive location: {cleanup.archive_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Safe cleanup plan")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ show plan, không thực hiện")
    parser.add_argument("--apply", action="store_true", help="Thực hiện archive")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    targets = get_cleanup_targets()

    if args.dry_run or not args.apply:
        run_dry_run(targets, repo_root)
    else:
        run_cleanup(targets, repo_root)


if __name__ == "__main__":
    main()
