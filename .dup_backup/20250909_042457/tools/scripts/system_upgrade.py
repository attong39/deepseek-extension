#!/usr/bin/env python3
"""
Zeta AI System Upgrade Script

Script này thực hiện nâng cấp toàn diện hệ thống:
1. Loại bỏ file thừa (.bak, templates cũ)
2. Hợp nhất modules trùng lặp
3. Tối ưu cấu trúc thư mục
4. Cập nhật imports và references
"""

from __future__ import annotations

import shutil
from pathlib import Path
import Exception
import any
import e
import error
import file_path
import len
import list
import old_file
import pattern
import print
import py_file
import self
import str
import tuple
import x

PROJECT_ROOT = Path(__file__).parent.parent
ZETA_VN_ROOT = PROJECT_ROOT / "zeta_vn"


class SystemUpgrader:
    """Thực hiện nâng cấp toàn diện hệ thống Zeta AI."""

    def __init__(self):
        self.removed_files: list[Path] = []
        self.moved_files: list[tuple[Path, Path]] = []
        self.errors: list[str] = []

    def remove_backup_files(self) -> None:
        """Loại bỏ các file .bak không cần thiết."""
        print("🗑️  Đang loại bỏ file backup...")

        backup_patterns = ["*.bak", "*.backup", "*~"]
        for pattern in backup_patterns:
            for file_path in ZETA_VN_ROOT.rglob(pattern):
                try:
                    file_path.unlink()
                    self.removed_files.append(file_path)
                    print(f"  ✅ Removed: {file_path}")
                except Exception as e:
                    self.errors.append(f"Failed to remove {file_path}: {e}")

    def merge_deps_modules(self) -> None:
        """Hợp nhất app/deps và app/deps_proposed."""
        print("🔄 Đang hợp nhất deps modules...")

        deps_dir = ZETA_VN_ROOT / "app" / "deps"
        deps_proposed_dir = ZETA_VN_ROOT / "app" / "deps_proposed"

        if not deps_proposed_dir.exists():
            print("  ⚠️  deps_proposed không tồn tại, bỏ qua...")
            return

        # Di chuyển các file từ deps_proposed vào deps nếu chưa có
        for file_path in deps_proposed_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            target_path = deps_dir / file_path.name
            if not target_path.exists():
                try:
                    shutil.move(str(file_path), str(target_path))
                    self.moved_files.append((file_path, target_path))
                    print(f"  ✅ Moved: {file_path} -> {target_path}")
                except Exception as e:
                    self.errors.append(f"Failed to move {file_path}: {e}")

        # Xóa thư mục deps_proposed nếu rỗng
        try:
            if deps_proposed_dir.exists() and not any(deps_proposed_dir.iterdir()):
                deps_proposed_dir.rmdir()
                print(f"  ✅ Removed empty directory: {deps_proposed_dir}")
        except Exception as e:
            self.errors.append(f"Failed to remove {deps_proposed_dir}: {e}")

    def consolidate_domain_events(self) -> None:
        """Hợp nhất core/domain/events và core/events."""
        print("🔄 Đang hợp nhất domain events...")

        domain_events_dir = ZETA_VN_ROOT / "core" / "domain" / "events"
        core_events_dir = ZETA_VN_ROOT / "core" / "events"

        if not core_events_dir.exists():
            print("  ⚠️  core/events không tồn tại, bỏ qua...")
            return

        # Di chuyển nội dung từ core/events vào core/domain/events
        for file_path in core_events_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue

            target_path = domain_events_dir / file_path.name
            if not target_path.exists():
                try:
                    shutil.move(str(file_path), str(target_path))
                    self.moved_files.append((file_path, target_path))
                    print(f"  ✅ Moved: {file_path} -> {target_path}")
                except Exception as e:
                    self.errors.append(f"Failed to move {file_path}: {e}")

    def remove_unused_templates(self) -> None:
        """Loại bỏ templates không sử dụng."""
        print("🗑️  Đang loại bỏ templates không dùng...")

        # Loại bỏ templates trùng lặp trong tools/templates
        templates_dir = ZETA_VN_ROOT / "tools" / "templates"
        scaffold_templates = ZETA_VN_ROOT / "tools" / "scaffold" / "templates"

        if templates_dir.exists() and scaffold_templates.exists():
            # Loại bỏ templates_dir vì đã có scaffold/templates
            try:
                shutil.rmtree(templates_dir)
                print(f"  ✅ Removed duplicate templates: {templates_dir}")
            except Exception as e:
                self.errors.append(f"Failed to remove {templates_dir}: {e}")

    def cleanup_test_duplicates(self) -> None:
        """Loại bỏ test files trùng lặp."""
        print("🧹 Đang dọn dẹp test duplicates...")

        # Tìm và loại bỏ các test file trùng lặp
        duplicate_patterns = [
            "**/test_gpt4o_trainer.py",  # Nếu có nhiều versions
        ]

        for pattern in duplicate_patterns:
            matching_files = list(ZETA_VN_ROOT.rglob(pattern))
            if len(matching_files) > 1:
                # Giữ lại file mới nhất, xóa các file cũ
                matching_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for old_file in matching_files[1:]:
                    try:
                        old_file.unlink()
                        self.removed_files.append(old_file)
                        print(f"  ✅ Removed duplicate: {old_file}")
                    except Exception as e:
                        self.errors.append(f"Failed to remove {old_file}: {e}")

    def update_imports(self) -> None:
        """Cập nhật các import references sau khi di chuyển files."""
        print("🔧 Đang cập nhật imports...")

        # Cập nhật imports từ deps_proposed -> deps
        python_files = list(ZETA_VN_ROOT.rglob("*.py"))

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                updated_content = content.replace(
                    "from apps.backend.app.deps_proposed.", "from apps.backend.app.deps."
                ).replace("import zeta_vn.app.deps_proposed.", "import zeta_vn.app.deps.")

                if content != updated_content:
                    py_file.write_text(updated_content, encoding="utf-8")
                    print(f"  ✅ Updated imports in: {py_file}")

            except Exception as e:
                self.errors.append(f"Failed to update imports in {py_file}: {e}")

    def run_upgrade(self) -> None:
        """Chạy toàn bộ quá trình nâng cấp."""
        print("🚀 Bắt đầu nâng cấp hệ thống Zeta AI...")
        print("=" * 50)

        self.remove_backup_files()
        self.merge_deps_modules()
        self.consolidate_domain_events()
        self.remove_unused_templates()
        self.cleanup_test_duplicates()
        self.update_imports()

        print("\n" + "=" * 50)
        print("📊 Tóm tắt kết quả:")
        print(f"  ✅ Đã xóa {len(self.removed_files)} files")
        print(f"  🔄 Đã di chuyển {len(self.moved_files)} files")

        if self.errors:
            print(f"  ⚠️  {len(self.errors)} lỗi:")
            for error in self.errors:
                print(f"    - {error}")
        else:
            print("  🎉 Hoàn thành không có lỗi!")


if __name__ == "__main__":
    upgrader = SystemUpgrader()
    upgrader.run_upgrade()
