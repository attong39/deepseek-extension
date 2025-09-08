#!/usr/bin/env python3
"""
Phase 0 - Architecture Consolidation Script

Clean up duplicate structures and anti-patterns to improve Focus Index from 0/100 to 60+/100.

This script:
1. Removes duplicate folder (wt_feat_memory_protocol_wiring_clean)
2. Consolidates duplicate models/event buses/repositories
3. Converts manager files to service façades
4. Normalizes to Clean Architecture structure

Usage:
    python tools/phase0_consolidation.py --dry-run
    python tools/phase0_consolidation.py --execute
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
import action
import any
import base_file
import bool
import bus
import dict
import dry_run
import dup
import f
import keep
import legacy
import len
import list
import manager_file
import model_name
import p
import path
import print
import r
import repo_file
import repo_groups
import repos
import self
import skip
import sorted
import str


class Phase0Consolidator:
    """Handles Phase 0 architecture consolidation."""

    # Skip patterns for filtering out non-source files
    SKIP_PATTERNS = [".venv", "site-packages", "build/", "test"]

    def __init__(self, root_path: Path, dry_run: bool = True):
        self.root = root_path
        self.dry_run = dry_run
        self.actions_taken: list[str] = []

    def log_action(self, action: str) -> None:
        """Log an action taken or planned."""
        prefix = "[DRY RUN]" if self.dry_run else "[EXECUTED]"
        print(f"{prefix} {action}")
        self.actions_taken.append(action)

    def remove_duplicate_folder(self) -> None:
        """Remove the duplicate wt_feat_memory_protocol_wiring_clean folder."""
        duplicate_path = self.root / "wt_feat_memory_protocol_wiring_clean"

        if duplicate_path.exists():
            self.log_action(f"Removing duplicate folder: {duplicate_path}")
            if not self.dry_run:
                shutil.rmtree(duplicate_path)
        else:
            self.log_action(f"Duplicate folder not found: {duplicate_path}")

    def consolidate_event_buses(self) -> None:
        """Consolidate multiple event buses into infrastructure/events/event_bus.py."""
        # Find all event_bus.py files
        event_buses = list(self.root.rglob("**/event_bus.py"))

        if len(event_buses) <= 1:
            self.log_action("No duplicate event buses found")
            return

        # Keep infrastructure/events/event_bus.py as canonical
        canonical = None
        duplicates = []

        for bus in event_buses:
            if "infrastructure/events" in str(bus):
                canonical = bus
            else:
                duplicates.append(bus)

        if canonical:
            self.log_action(f"Keeping canonical event bus: {canonical}")
            for dup in duplicates:
                self.log_action(f"Removing duplicate event bus: {dup}")
                if not self.dry_run:
                    dup.unlink()
        else:
            self.log_action("No canonical infrastructure event bus found")

    def normalize_model_files(self) -> None:
        """Normalize model files to *_model.py pattern."""
        # Find potential model files that should be normalized
        model_patterns = [
            ("agent.py", "agent_model.py"),
            ("chat.py", "chat_model.py"),
            ("memory.py", "memory_model.py"),
            ("user.py", "user_model.py"),
        ]

        for base_name, model_name in model_patterns:
            # Look for files in data/models/ that don't follow *_model.py
            base_files = list(self.root.rglob(f"**/data/models/{base_name}"))
            model_files = list(self.root.rglob(f"**/data/models/{model_name}"))

            if base_files and not model_files:
                for base_file in base_files:
                    new_path = base_file.parent / model_name
                    self.log_action(f"Renaming {base_file} to {new_path}")
                    if not self.dry_run:
                        base_file.rename(new_path)

    def convert_managers_to_services(self) -> None:
        """Convert *manager.py files to service façades with deprecation."""
        manager_files = list(self.root.rglob("**/*manager.py"))

        for manager_file in manager_files:
            # Skip test files and dependencies
            if any(skip in str(manager_file) for skip in self.SKIP_PATTERNS):
                continue

            # Determine target service name
            service_name = manager_file.name.replace("manager.py", "service.py")
            service_path = manager_file.parent / service_name

            self.log_action(f"Converting manager {manager_file} to service {service_path}")

            if not self.dry_run and manager_file.exists():
                # Create deprecation shim
                shim_content = f'''"""
DEPRECATED: This manager has been converted to a service façade.
Use {service_name} instead.
"""
import warnings
from .{service_name.replace(".py", "")} import *

warnings.warn(
    f"{{__name__}} is deprecated. Use {service_name} instead.",
    DeprecationWarning,
    stacklevel=2
)
'''
                # If service doesn't exist, rename manager to service
                if not service_path.exists():
                    manager_file.rename(service_path)

                # Create deprecation shim at old location
                manager_file.write_text(shim_content, encoding="utf-8")

    def consolidate_repositories(self) -> None:
        """Prefer sqlalchemy_*_repository.py implementations."""
        repo_files = list(self.root.rglob("**/repositories/*_repository.py"))

        # Filter out dependencies and build artifacts
        repo_files = [f for f in repo_files if not any(skip in str(f) for skip in self.SKIP_PATTERNS)]

        # Group by base name
        repo_groups: dict[str, list[Path]] = {}

        for repo_file in repo_files:
            name = repo_file.name
            if name.startswith("sqlalchemy_"):
                base_name = name.replace("sqlalchemy_", "")
            else:
                base_name = name

            if base_name not in repo_groups:
                repo_groups[base_name] = []
            repo_groups[base_name].append(repo_file)

        # For each group, prefer sqlalchemy_ version
        for base_name, repos in repo_groups.items():
            sqlalchemy_repos = [r for r in repos if "sqlalchemy_" in r.name]
            legacy_repos = [r for r in repos if "sqlalchemy_" not in r.name]

            if sqlalchemy_repos and legacy_repos:
                canonical = sqlalchemy_repos[0]
                self.log_action(f"Keeping preferred repository: {canonical}")

                for legacy in legacy_repos:
                    self.log_action(f"Deprecating legacy repository: {legacy}")

                    if not self.dry_run:
                        # Create deprecation shim
                        shim_content = f'''"""
DEPRECATED: Use {canonical.name} instead.
"""
import warnings
from .{canonical.name.replace(".py", "")} import *

warnings.warn(
    f"{{__name__}} is deprecated. Use {canonical.name} instead.",
    DeprecationWarning,
    stacklevel=2
)
'''
                        legacy.write_text(shim_content, encoding="utf-8")

    def clean_empty_directories(self) -> None:
        """Remove empty directories after consolidation."""
        # Find empty directories (bottom-up)
        for path in sorted(self.root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                # Skip certain directories we want to keep
                if any(keep in str(path) for keep in [".git", ".venv", "__pycache__"]):
                    continue

                self.log_action(f"Removing empty directory: {path}")
                if not self.dry_run:
                    path.rmdir()

    def update_imports(self) -> None:
        """Update imports to use new consolidated paths (basic pass)."""
        # This would be a complex operation requiring AST parsing
        # For now, just log that manual import updates may be needed
        self.log_action("NOTE: Manual import updates may be required after consolidation")
        self.log_action("Run: python tools/autobarrel_python.py to update barrels")
        self.log_action("Run: ruff check --fix . to auto-fix import ordering")

    def generate_summary(self) -> dict:
        """Generate summary of actions taken."""
        return {
            "phase": "Phase 0 - Architecture Consolidation",
            "dry_run": self.dry_run,
            "actions_count": len(self.actions_taken),
            "actions": self.actions_taken,
        }

    def run_consolidation(self) -> None:
        """Run all consolidation steps."""
        print(f"🏗️  Starting Phase 0 Consolidation (dry_run={self.dry_run})")
        print("=" * 60)

        # Step 1: Remove duplicate folders
        self.remove_duplicate_folder()

        # Step 2: Consolidate event buses
        self.consolidate_event_buses()

        # Step 3: Normalize model files
        self.normalize_model_files()

        # Step 4: Convert managers to services
        self.convert_managers_to_services()

        # Step 5: Consolidate repositories
        self.consolidate_repositories()

        # Step 6: Clean empty directories
        self.clean_empty_directories()

        # Step 7: Update imports (placeholder)
        self.update_imports()

        print("\n" + "=" * 60)
        summary = self.generate_summary()
        print(f"✅ Phase 0 Complete: {summary['actions_count']} actions")

        if self.dry_run:
            print("\n🚨 This was a DRY RUN. Use --execute to apply changes.")
        else:
            print("\n✅ Changes applied. Run focus_guard.py to check improved Focus Index.")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Phase 0 Architecture Consolidation")
    parser.add_argument("--execute", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")

    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if not root_path.exists():
        print(f"Error: Root path {root_path} does not exist", file=sys.stderr)
        sys.exit(1)

    # Run consolidation
    consolidator = Phase0Consolidator(root_path, dry_run=not args.execute)
    consolidator.run_consolidation()

    # Output summary
    if args.json:
        summary = consolidator.generate_summary()
        print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
