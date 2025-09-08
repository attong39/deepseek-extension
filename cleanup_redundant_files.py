#!/usr/bin/env python3
"""
🧹 CLEANUP REDUNDANT FILES - Zeta Monorepo
Xóa các file thừa và không cần thiết một cách an toàn
"""

import shutil
import time
from pathlib import Path
import Exception
import OSError
import PermissionError
import any
import bool
import cache_dir
import category
import e
import file_path
import input
import int
import len
import path
import pattern
import patterns
import print
import protected
import root_path
import self
import sorted
import str
import x


class RedundantFileCleanup:
    """Safe cleanup for redundant files in the project."""
    
    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.backup_dir = self.root / ".cleanup_backup" / f"redundant_{int(time.time())}"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Patterns for redundant files/directories
        self.redundant_patterns = {
            # Cache directories
            "cache_dirs": {
                ".ruff_cache", ".mypy_cache", ".pytest_cache", "__pycache__",
                "node_modules/.cache", ".coverage"
            },
            
            # Backup files
            "backup_files": {
                "*.backup", "*.bak", "*.old", "*~", "*.tmp"
            },
            
            # Log files (old)
            "log_files": {
                "*.log", "cleanup_log_*.txt"
            },
            
            # Old backup directories
            "backup_dirs": {
                "venv_backup_*", ".dup_cleanup_backup", "reports/consolidation_trash"
            },
            
            # Duplicate reports (old)
            "old_reports": {
                "dedupe_reports", ".dup_reports"
            },
            
            # Development artifacts
            "dev_artifacts": {
                ".venv-optimized", ".venv-ollama", "apps/backend/.venv-ollama"
            }
        }
        
        # Protected paths (NEVER delete)
        self.protected_paths = {
            ".venv", ".git", ".github", "production", "apps", "packages",
            "tools", "scripts", "docs", "tests", "src", "config"
        }
        
        self.stats = {
            "scanned": 0,
            "backed_up": 0,
            "deleted": 0,
            "space_freed": 0,
            "errors": 0
        }

    def is_protected_path(self, path: Path) -> bool:
        """Check if path is protected from deletion."""
        path_str = str(path.relative_to(self.root))
        return any(path_str.startswith(protected) for protected in self.protected_paths)

    def get_directory_size(self, path: Path) -> int:
        """Calculate total size of directory."""
        total_size = 0
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except (OSError, PermissionError):
            pass
        return total_size

    def backup_and_delete_path(self, path: Path, category: str) -> bool:
        """Backup and safely delete a path."""
        try:
            if not path.exists():
                return True
                
            # Calculate size before deletion
            size = path.stat().st_size if path.is_file() else self.get_directory_size(path)
            
            # Create backup
            backup_path = self.backup_dir / category / path.name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            if path.is_file():
                shutil.copy2(path, backup_path)
                path.unlink()
            else:
                shutil.copytree(path, backup_path, dirs_exist_ok=True)
                shutil.rmtree(path)
            
            self.stats["backed_up"] += 1
            self.stats["deleted"] += 1
            self.stats["space_freed"] += size
            
            print(f"✅ Deleted: {path.relative_to(self.root)} ({size/1024/1024:.2f} MB)")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting {path}: {e}")
            self.stats["errors"] += 1
            return False

    def cleanup_cache_directories(self) -> None:
        """Remove cache directories."""
        print("\n🗑️  Cleaning cache directories...")
        
        for cache_dir in self.redundant_patterns["cache_dirs"]:
            for path in self.root.rglob(cache_dir):
                if path.is_dir() and not self.is_protected_path(path):
                    self.backup_and_delete_path(path, "cache_dirs")

    def cleanup_backup_files(self) -> None:
        """Remove backup files."""
        print("\n🗑️  Cleaning backup files...")
        
        for pattern in self.redundant_patterns["backup_files"]:
            for path in self.root.rglob(pattern):
                if path.is_file() and not self.is_protected_path(path):
                    self.backup_and_delete_path(path, "backup_files")

    def cleanup_log_files(self) -> None:
        """Remove old log files."""
        print("\n🗑️  Cleaning old log files...")
        
        for pattern in self.redundant_patterns["log_files"]:
            for path in self.root.rglob(pattern):
                if path.is_file() and not self.is_protected_path(path):
                    # Keep recent logs (less than 7 days)
                    try:
                        if time.time() - path.stat().st_mtime > 7 * 24 * 3600:
                            self.backup_and_delete_path(path, "log_files")
                    except OSError:
                        pass

    def cleanup_backup_directories(self) -> None:
        """Remove old backup directories."""
        print("\n🗑️  Cleaning backup directories...")
        
        for pattern in self.redundant_patterns["backup_dirs"]:
            for path in self.root.rglob(pattern):
                if path.is_dir() and not self.is_protected_path(path):
                    self.backup_and_delete_path(path, "backup_dirs")

    def cleanup_old_reports(self) -> None:
        """Remove old report directories."""
        print("\n🗑️  Cleaning old report directories...")
        
        for pattern in self.redundant_patterns["old_reports"]:
            for path in self.root.rglob(pattern):
                if path.is_dir() and not self.is_protected_path(path):
                    self.backup_and_delete_path(path, "old_reports")

    def cleanup_dev_artifacts(self) -> None:
        """Remove development artifacts."""
        print("\n🗑️  Cleaning development artifacts...")
        
        for pattern in self.redundant_patterns["dev_artifacts"]:
            for path in self.root.rglob(pattern):
                if path.is_dir() and not self.is_protected_path(path):
                    self.backup_and_delete_path(path, "dev_artifacts")

    def cleanup_empty_directories(self) -> None:
        """Remove empty directories."""
        print("\n🗑️  Cleaning empty directories...")
        
        # Find empty directories (bottom-up)
        empty_dirs = []
        for path in self.root.rglob('*'):
            if (path.is_dir() and 
                not self.is_protected_path(path) and
                not any(path.iterdir())):
                empty_dirs.append(path)
        
        # Sort by depth (deepest first)
        empty_dirs.sort(key=lambda x: len(x.parts), reverse=True)
        
        for path in empty_dirs:
            try:
                if path.exists() and not any(path.iterdir()):
                    path.rmdir()
                    print(f"✅ Removed empty dir: {path.relative_to(self.root)}")
                    self.stats["deleted"] += 1
            except OSError:
                pass

    def run_full_cleanup(self) -> None:
        """Run complete redundant file cleanup."""
        print("🚀 Starting redundant file cleanup...")
        print(f"📦 Root directory: {self.root}")
        print(f"🔒 Backup directory: {self.backup_dir}")
        
        # Run all cleanup operations
        self.cleanup_cache_directories()
        self.cleanup_backup_files()
        self.cleanup_log_files()
        self.cleanup_backup_directories()
        self.cleanup_old_reports()
        self.cleanup_dev_artifacts()
        self.cleanup_empty_directories()
        
        # Print final statistics
        print("\n" + "="*60)
        print("🎯 CLEANUP SUMMARY")
        print("="*60)
        print(f"📁 Files/dirs backed up: {self.stats['backed_up']}")
        print(f"🗑️  Files/dirs deleted: {self.stats['deleted']}")
        print(f"💾 Space freed: {self.stats['space_freed']/1024/1024:.2f} MB")
        print(f"❌ Errors: {self.stats['errors']}")
        print(f"🔒 Backup location: {self.backup_dir}")
        
        if self.stats['errors'] == 0:
            print("\n✅ Cleanup completed successfully!")
        else:
            print(f"\n⚠️  Cleanup completed with {self.stats['errors']} errors")


def main():
    """Main entry point."""
    cleanup = RedundantFileCleanup()
    
    # Show what will be cleaned
    print("🔍 Redundant file patterns to clean:")
    for category, patterns in cleanup.redundant_patterns.items():
        print(f"  {category}: {', '.join(patterns)}")
    
    print("\n🔒 Protected paths (will NOT be deleted):")
    for protected in sorted(cleanup.protected_paths):
        print(f"  {protected}")
    
    # Confirm before proceeding
    response = input("\n❓ Proceed with cleanup? (y/N): ").lower().strip()
    if response != 'y':
        print("❌ Cleanup cancelled")
        return
    
    cleanup.run_full_cleanup()


if __name__ == "__main__":
    main()
