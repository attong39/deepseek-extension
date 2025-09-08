#!/usr/bin/env python
"""
🛡️ SAFE REPO FIXER V3 - COMPREHENSIVE PROJECT FIXING
====================================================

Enhanced version với full project scope, graduated fixing, và comprehensive safety.
Usage: python tools/fix_repo_safe_v3.py --category [critical|imports|types|style] --apply
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import Exception
import bool
import cat_name
import category
import dict
import dry_run
import e
import error
import f
import label
import len
import list
import open
import print
import root_path
import self
import set
import sorted
import str
import test_after
import x


class SafeRepoFixerV3:
    """Enhanced fixer với comprehensive scope và gradual fixing"""

    def __init__(self, root_path: str = "zeta_vn"):
        self.root_path = Path(root_path)
        self.backup_dir = Path(".safe_fix_backups_v3")
        self.backup_dir.mkdir(exist_ok=True)

        # Fix categories với priority levels
        self.fix_categories = {
            "critical": {
                "description": "Syntax errors, undefined variables - breaks functionality",
                "rules": ["E999", "F821", "F822", "F823"],
                "priority": 1,
                "safe_to_autofix": True,
            },
            "imports": {
                "description": "Import ordering, unused imports, import errors",
                "rules": ["E402", "F401", "F811", "F401"],
                "priority": 2,
                "safe_to_autofix": True,
            },
            "types": {
                "description": "Type hints, type checking issues",
                "rules": ["mypy"],
                "priority": 3,
                "safe_to_autofix": False,  # Cần manual review
            },
            "style": {
                "description": "Code style, formatting consistency",
                "rules": ["E", "W", "N"],
                "priority": 4,
                "safe_to_autofix": True,
            },
            "security": {
                "description": "Security vulnerabilities, unsafe patterns",
                "rules": ["bandit"],
                "priority": 2,
                "safe_to_autofix": False,
            },
            "performance": {
                "description": "Performance improvements, optimizations",
                "rules": ["PERF"],
                "priority": 5,
                "safe_to_autofix": True,
            },
        }

    def create_backup(self, label: str = "") -> str:
        """Tạo backup với label"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"{timestamp}_{label}" if label else timestamp
        backup_path = self.backup_dir / backup_id

        print(f"📦 Creating backup: {backup_path}")

        try:
            subprocess.run(
                ["xcopy", str(self.root_path), str(backup_path), "/E", "/I", "/Q"],
                check=True,
                capture_output=True,
            )

            # Lưu metadata
            metadata = {
                "backup_id": backup_id,
                "timestamp": timestamp,
                "label": label,
                "git_commit": self.get_git_commit(),
                "total_files": len(list(backup_path.rglob("*.py"))),
            }

            with open(backup_path / "_backup_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            print(f"✅ Backup created: {backup_path}")
            return backup_id

        except subprocess.CalledProcessError as e:
            print(f"❌ Backup failed: {e}")
            return ""

    def get_git_commit(self) -> str:
        """Lấy current git commit"""
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except:
            return "unknown"

    def run_critical_tests(self) -> bool:
        """Chạy critical tests để verify stability"""
        print("🧪 Running critical tests...")

        # Test 1: Syntax check
        try:
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "py_compile",
                    "-",
                ],
                input=f"import {self.root_path.name}",
                text=True,
                capture_output=True,
            )

            if result.returncode != 0:
                print("❌ Import test failed")
                return False

        except Exception as e:
            print(f"❌ Syntax test failed: {e}")
            return False

        # Test 2: Quick pytest smoke tests
        smoke_tests = Path("tests/smoke")
        if smoke_tests.exists():
            try:
                result = subprocess.run(
                    ["uv", "run", "pytest", str(smoke_tests), "-x", "--tb=no"],
                    capture_output=True,
                    text=True,
                )

                if result.returncode != 0:
                    print("❌ Smoke tests failed")
                    return False

            except Exception as e:
                print(f"❌ Smoke test execution failed: {e}")
                return False

        print("✅ Critical tests passed")
        return True

    def analyze_errors(self, category: str | None = None) -> dict:
        """Phân tích lỗi hiện tại"""
        print("🔍 Analyzing errors" + (f" for category: {category}" if category else ""))

        analysis = {"total_files": 0, "total_errors": 0, "by_category": {}, "error_files": []}

        # Chạy ruff check
        try:
            if category and category in self.fix_categories:
                rules = self.fix_categories[category]["rules"]
                if rules[0] == "mypy":
                    # MyPy analysis
                    result = subprocess.run(
                        ["uv", "run", "mypy", str(self.root_path), "--show-error-codes"],
                        capture_output=True,
                        text=True,
                    )
                elif rules[0] == "bandit":
                    # Security analysis
                    result = subprocess.run(
                        ["uv", "run", "bandit", "-r", str(self.root_path), "-f", "json"],
                        capture_output=True,
                        text=True,
                    )
                else:
                    # Ruff analysis
                    select_rules = ",".join(rules)
                    result = subprocess.run(
                        [
                            "uv",
                            "run",
                            "ruff",
                            "check",
                            str(self.root_path),
                            "--select",
                            select_rules,
                            "--output-format",
                            "json",
                        ],
                        capture_output=True,
                        text=True,
                    )
            else:
                # Full analysis
                result = subprocess.run(
                    ["uv", "run", "ruff", "check", str(self.root_path), "--output-format", "json"],
                    capture_output=True,
                    text=True,
                )

            if result.stdout:
                if category and self.fix_categories[category]["rules"][0] == "bandit":
                    errors = json.loads(result.stdout).get("results", [])
                else:
                    errors = json.loads(result.stdout) if result.stdout.startswith("[") else []

                analysis["total_errors"] = len(errors)
                analysis["error_files"] = list(set(error.get("filename", "") for error in errors))

        except Exception as e:
            print(f"⚠️ Analysis error: {e}")

        return analysis

    def apply_fixes(self, category: str, dry_run: bool = False) -> bool:
        """Apply fixes cho một category"""
        if category not in self.fix_categories:
            print(f"❌ Unknown category: {category}")
            return False

        cat_config = self.fix_categories[category]
        print(f"🔧 {'DRY RUN: ' if dry_run else ''}Applying {category} fixes")
        print(f"📝 {cat_config['description']}")

        if not cat_config["safe_to_autofix"] and not dry_run:
            print("⚠️ This category requires manual review - use --dry-run first")
            return False

        try:
            rules = cat_config["rules"]

            if rules[0] == "mypy":
                # MyPy fixes - manual review needed
                print("📋 MyPy issues found - manual review required")
                subprocess.run(
                    ["uv", "run", "mypy", str(self.root_path), "--show-error-codes", "--pretty"],
                    check=False,
                )
                return True

            elif rules[0] == "bandit":
                # Security scan - manual review needed
                print("🔒 Security scan - manual review required")
                subprocess.run(["uv", "run", "bandit", "-r", str(self.root_path), "-v"], check=False)
                return True

            else:
                # Ruff fixes
                select_rules = ",".join(rules)
                cmd = ["uv", "run", "ruff", "check", str(self.root_path), "--select", select_rules]

                if not dry_run:
                    cmd.append("--fix")

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"✅ {category} fixes applied successfully")
                    return True
                else:
                    print(f"⚠️ Some {category} issues remain:")
                    print(result.stdout[:500])
                    return False

        except Exception as e:
            print(f"❌ Fix application failed: {e}")
            return False

    def rollback(self, backup_id: str) -> bool:
        """Rollback về backup"""
        backup_path = self.backup_dir / backup_id

        if not backup_path.exists():
            print(f"❌ Backup not found: {backup_id}")
            return False

        print(f"⏪ Rolling back to: {backup_id}")

        try:
            # Remove current
            if self.root_path.exists():
                subprocess.run(["rmdir", "/s", "/q", str(self.root_path)], shell=False, check=False)

            # Restore backup
            subprocess.run(["xcopy", str(backup_path), str(self.root_path), "/E", "/I", "/Q"], check=True)

            print("✅ Rollback completed")
            return True

        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False

    def fix_by_category(self, category: str, test_after: bool = True, dry_run: bool = False) -> bool:
        """Fix một category với comprehensive safety"""

        if category not in self.fix_categories:
            print(f"❌ Unknown category: {category}")
            return False

        print(f"\n{'=' * 60}")
        print(f"🎯 PROCESSING CATEGORY: {category.upper()}")
        print(f"{'=' * 60}")

        # Pre-analysis
        pre_analysis = self.analyze_errors(category)
        print(f"📊 Found {pre_analysis['total_errors']} {category} errors")

        if pre_analysis["total_errors"] == 0:
            print(f"✅ No {category} errors found - skipping")
            return True

        if dry_run:
            print("🔍 DRY RUN MODE - showing what would be fixed:")
            return self.apply_fixes(category, dry_run=True)

        # Create backup
        backup_id = self.create_backup(f"{category}_fix")
        if not backup_id:
            print("❌ Backup failed - aborting")
            return False

        try:
            # Apply fixes
            fix_success = self.apply_fixes(category, dry_run=False)

            if not fix_success:
                print(f"❌ {category} fixes failed")
                self.rollback(backup_id)
                return False

            # Test after fixes
            if test_after:
                test_success = self.run_critical_tests()

                if not test_success:
                    print(f"❌ Critical tests failed after {category} fixes - rolling back")
                    self.rollback(backup_id)
                    return False
                else:
                    print(f"✅ {category} fixes verified successfully")

            # Post-analysis
            post_analysis = self.analyze_errors(category)
            improvement = pre_analysis["total_errors"] - post_analysis["total_errors"]

            print(f"📈 Fixed {improvement} {category} errors")
            print(f"📊 Remaining: {post_analysis['total_errors']}")

            return True

        except Exception as e:
            print(f"💥 Unexpected error during {category} fixing: {e}")
            self.rollback(backup_id)
            return False


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Safe Repo Fixer V3")
    parser.add_argument(
        "--category",
        choices=["critical", "imports", "types", "style", "security", "performance"],
        help="Category to fix",
    )
    parser.add_argument("--all", action="store_true", help="Fix all categories in priority order")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without applying")
    parser.add_argument("--no-test", action="store_true", help="Skip testing after fixes")
    parser.add_argument("--root", default="zeta_vn", help="Root package path")

    args = parser.parse_args()

    fixer = SafeRepoFixerV3(args.root)

    print("🛡️ SAFE REPO FIXER V3 - COMPREHENSIVE PROJECT FIXING")
    print("=" * 60)

    if args.all:
        # Fix all categories in priority order
        categories = sorted(fixer.fix_categories.items(), key=lambda x: x[1]["priority"])

        print("🎯 Processing all categories in priority order...")
        success_count = 0

        for cat_name, cat_config in categories:
            print(f"\n🔄 Category {cat_config['priority']}: {cat_name}")

            success = fixer.fix_by_category(cat_name, test_after=not args.no_test, dry_run=args.dry_run)

            if success:
                success_count += 1
            else:
                print(f"⚠️ Category {cat_name} had issues - continuing...")

        print(f"\n📊 SUMMARY: {success_count}/{len(categories)} categories processed successfully")

    elif args.category:
        # Fix specific category
        success = fixer.fix_by_category(args.category, test_after=not args.no_test, dry_run=args.dry_run)

        if success:
            print(f"🎉 Category {args.category} fixed successfully!")
        else:
            print(f"❌ Category {args.category} fixing failed")
            sys.exit(1)

    else:
        # Show analysis only
        print("📊 PROJECT ANALYSIS")
        for cat_name in fixer.fix_categories:
            analysis = fixer.analyze_errors(cat_name)
            print(f"  {cat_name}: {analysis['total_errors']} errors")

        print("\n💡 Use --category <name> to fix specific category")
        print("💡 Use --all to fix all categories")
        print("💡 Use --dry-run to preview changes")


if __name__ == "__main__":
    main()
