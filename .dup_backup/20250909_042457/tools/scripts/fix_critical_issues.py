#!/usr/bin/env python3
"""
🚀 ZETA_VN Code Quality Fix Script
Automated script để fix các lỗi critical trong codebase

Usage:
    python scripts/fix_critical_issues.py [--phase=1,2,3] [--dry-run]
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
import Exception
import KeyboardInterrupt
import any
import bool
import cmd
import dict
import dry_run
import e
import exit_code
import file_path
import fix
import imports
import indent
import int
import line
import list
import module
import pattern
import print
import self
import sorted
import stderr
import stdout
import str
import tool
import tuple


class ZetaCodeFixer:
    """Main class để fix code quality issues"""

    def __init__(self, project_root: Path, dry_run: bool = False):
        self.project_root = project_root
        self.dry_run = dry_run
        self.fixes_applied = []

    def run_command(self, cmd: str, cwd: Path = None) -> tuple[int, str, str]:
        """Run shell command and return exit code, stdout, stderr"""
        if self.dry_run:
            print(f"[DRY RUN] Would run: {cmd}")
            return 0, "", ""

        cwd = cwd or self.project_root
        result = subprocess.run(cmd, check=False, shell=False, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def fix_phase1_critical_syntax(self):
        """Phase 1: Fix critical syntax errors"""
        print("🔧 Phase 1: Fixing critical syntax errors...")

        # 1. Fix empty permissions.py file
        self._fix_empty_permissions_file()

        # 2. Fix import issues
        self._fix_import_issues()

        # 3. Fix indentation issues
        self._fix_indentation_issues()

        # 4. Run ruff autofix
        self._run_ruff_autofix()

    def _fix_empty_permissions_file(self):
        """Recreate empty permissions.py file"""
        permissions_file = self.project_root / "zeta_vn/core/security/permissions.py"

        if not permissions_file.exists() or permissions_file.stat().st_size == 0:
            print(f"🔄 Recreating {permissions_file}")

            content = '''"""Permission definitions and role mappings for ZETA security system."""

from __future__ import annotations

from typing import Literal

Risk = Literal["low", "medium", "high", "critical"]

# Permission registry với risk levels
PERMISSIONS: dict[str, dict[str, str]] = {
    # Agent permissions
    "agent:create": {"risk": "medium"},
    "agent:read": {"risk": "low"},
    "agent:update": {"risk": "medium"},
    "agent:delete": {"risk": "high"},
    "agent:run": {"risk": "high"},
    
    # Memory permissions
    "memory:ingest": {"risk": "low"},
    "memory:search": {"risk": "low"},
    "memory:read": {"risk": "low"},
    "memory:update": {"risk": "medium"},
    "memory:delete": {"risk": "high"},
    "memory:purge": {"risk": "critical"},
    
    # File permissions
    "files:upload": {"risk": "low"},
    "files:download": {"risk": "low"},
    "files:read": {"risk": "low"},
    "files:write": {"risk": "medium"},
    "files:delete": {"risk": "high"},
    
    # Training permissions
    "training:start": {"risk": "medium"},
    "training:stop": {"risk": "low"},
    "training:cancel": {"risk": "medium"},
    "training:view_status": {"risk": "low"},
    "training:view_logs": {"risk": "low"},
    "training:delete": {"risk": "high"},
    
    # Admin permissions
    "admin:user:list": {"risk": "medium"},
    "admin:user:create": {"risk": "high"},
    "admin:user:update": {"risk": "high"},
    "admin:user:delete": {"risk": "critical"},
    "admin:user:invite": {"risk": "medium"},
    "admin:user:disable": {"risk": "high"},
    
    # System permissions
    "system:audit:read": {"risk": "medium"},
    "system:logs:read": {"risk": "medium"},
    "system:metrics:read": {"risk": "low"},
    "system:health:read": {"risk": "low"},
    
    # Operations permissions
    "ops:backup:create": {"risk": "medium"},
    "ops:backup:restore": {"risk": "critical"},
    "ops:policy:read": {"risk": "medium"},
    "ops:policy:update": {"risk": "critical"},
    "ops:system:restart": {"risk": "critical"},
}

# Role-based permission mappings
DEFAULT_ROLE_PERMS: dict[str, list[str]] = {
    "guest": [
        "system:health:read",
    ],
    "user": [
        "agent:read",
        "agent:run",
        "memory:search",
        "memory:read",
        "files:upload",
        "files:download",
        "files:read",
        "training:start",
        "training:view_status",
        "training:view_logs",
        "system:health:read",
        "system:metrics:read",
    ],
    "power_user": [
        "agent:create",
        "agent:update",
        "memory:ingest",
        "memory:update",
        "files:write",
        "files:delete",
        "training:stop",
        "training:cancel",
        "system:logs:read",
    ],
    "admin": [
        "agent:delete",
        "memory:delete",
        "training:delete",
        "admin:user:list",
        "admin:user:create",
        "admin:user:update",
        "admin:user:invite",
        "admin:user:disable",
        "system:audit:read",
        "ops:backup:create",
        "ops:policy:read",
    ],
    "superadmin": [
        "memory:purge",
        "admin:user:delete",
        "ops:backup:restore",
        "ops:policy:update",
        "ops:system:restart",
    ],
}

# Export all roles for easy access
ROLES = list(DEFAULT_ROLE_PERMS.keys())

def get_permission_risk(permission: str) -> str:
    """Get risk level for a permission"""
    return PERMISSIONS.get(permission, {}).get("risk", "medium")

def get_permissions_for_role(role: str) -> list[str]:
    """Get all permissions for a role (including inherited)"""
    if role not in DEFAULT_ROLE_PERMS:
        return []
    
    permissions = set()
    
    # Add direct permissions
    permissions.update(DEFAULT_ROLE_PERMS[role])
    
    # Add inherited permissions from lower roles
    role_hierarchy = ["guest", "user", "power_user", "admin", "superadmin"]
    try:
        role_index = role_hierarchy.index(role)
        for lower_role in role_hierarchy[:role_index]:
            permissions.update(DEFAULT_ROLE_PERMS[lower_role])
    except ValueError:
        pass  # Role not in hierarchy
    
    return list(permissions)

def has_permission(user_roles: list[str], permission: str) -> bool:
    """Check if user with given roles has permission"""
    for role in user_roles:
        role_permissions = get_permissions_for_role(role)
        if permission in role_permissions:
            return True
    return False

def get_required_permissions(action: str) -> list[str]:
    """Get required permissions for an action"""
    return [action]  # Simple 1:1 mapping for now

def is_high_risk_action(action: str) -> bool:
    """Check if action is high risk"""
    risk = get_permission_risk(action)
    return risk in ["high", "critical"]

def requires_mfa(action: str) -> bool:
    """Check if action requires MFA"""
    return get_permission_risk(action) == "critical"

__all__ = [
    "PERMISSIONS",
    "DEFAULT_ROLE_PERMS",
    "ROLES",
    "Risk",
    "get_permission_risk",
    "get_permissions_for_role",
    "has_permission",
    "get_required_permissions",
    "is_high_risk_action",
    "requires_mfa",
]
'''

            if not self.dry_run:
                permissions_file.write_text(content, encoding="utf-8")
                self.fixes_applied.append("Recreated permissions.py")

    def _fix_import_issues(self):
        """Fix common import issues"""
        print("🔄 Fixing import issues...")

        # Find Python files with import issues
        python_files = list(self.project_root.rglob("*.py"))

        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content

                # Fix relative imports to absolute
                content = self._convert_relative_imports(content, file_path)

                # Fix import order
                content = self._fix_import_order(content)

                if content != original_content and not self.dry_run:
                    file_path.write_text(content, encoding="utf-8")
                    self.fixes_applied.append(f"Fixed imports in {file_path.relative_to(self.project_root)}")

            except Exception as e:
                print(f"Warning: Could not fix imports in {file_path}: {e}")

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            "__pycache__",
            ".venv",
            ".git",
            "node_modules",
            ".pytest_cache",
            "migrations/versions",  # Don't touch migration files
        ]

        str_path = str(file_path)
        return any(pattern in str_path for pattern in skip_patterns)

    def _convert_relative_imports(self, content: str, file_path: Path) -> str:
        """Convert relative imports to absolute imports"""
        lines = content.split("\n")
        modified_lines = []

        for line in lines:
            # Pattern for relative imports: from .module import something
            if re.match(r"^\s*from\s+\.", line):
                # Calculate the module path
                relative_to_root = file_path.relative_to(self.project_root)
                package_path = ".".join(relative_to_root.parent.parts)

                # Convert relative import
                match = re.match(r"^(\s*)from\s+(\.*)(.*?)\s+import\s+(.*)$", line)
                if match:
                    indent, dots, module, imports = match.groups()

                    # Calculate absolute module path
                    if package_path.startswith("zeta_vn"):
                        if module:
                            abs_module = f"{package_path}.{module}"
                        else:
                            abs_module = package_path

                        new_line = f"{indent}from {abs_module} import {imports}"
                        modified_lines.append(new_line)
                        continue

            modified_lines.append(line)

        return "\n".join(modified_lines)

    def _fix_import_order(self, content: str) -> str:
        """Fix import order using isort-like logic"""
        lines = content.split("\n")

        # Simple import grouping
        import_groups = {"stdlib": [], "third_party": [], "local": [], "future": []}

        non_import_lines = []
        in_imports = True

        stdlib_modules = {
            "os",
            "sys",
            "datetime",
            "typing",
            "asyncio",
            "logging",
            "json",
            "uuid",
            "re",
            "pathlib",
            "subprocess",
            "functools",
        }

        for line in lines:
            if line.strip().startswith("from __future__"):
                import_groups["future"].append(line)
            elif line.strip().startswith(("import ", "from ")) and in_imports:
                # Determine import type
                if "zeta_vn" in line:
                    import_groups["local"].append(line)
                else:
                    # Check if it's stdlib
                    module_match = re.match(r"^(?:from\s+)?([a-zA-Z_][a-zA-Z0-9_]*)", line.strip())
                    if module_match:
                        module_name = module_match.group(1)
                        if module_name in stdlib_modules:
                            import_groups["stdlib"].append(line)
                        else:
                            import_groups["third_party"].append(line)
                    else:
                        import_groups["third_party"].append(line)
            else:
                if line.strip() and in_imports:
                    in_imports = False
                non_import_lines.append(line)

        # Rebuild content with proper import order
        new_lines = []

        # Add future imports first
        if import_groups["future"]:
            new_lines.extend(import_groups["future"])
            new_lines.append("")

        # Add stdlib imports
        if import_groups["stdlib"]:
            new_lines.extend(sorted(import_groups["stdlib"]))
            new_lines.append("")

        # Add third party imports
        if import_groups["third_party"]:
            new_lines.extend(sorted(import_groups["third_party"]))
            new_lines.append("")

        # Add local imports
        if import_groups["local"]:
            new_lines.extend(sorted(import_groups["local"]))
            new_lines.append("")

        # Add rest of the file
        new_lines.extend(non_import_lines)

        return "\n".join(new_lines)

    def _fix_indentation_issues(self):
        """Fix basic indentation issues"""
        print("🔄 Fixing indentation issues...")

        # Use autopep8 for basic formatting
        exit_code, stdout, stderr = self.run_command("uv run autopep8 --in-place --recursive zeta_vn/")
        if exit_code == 0:
            self.fixes_applied.append("Fixed indentation with autopep8")

    def _run_ruff_autofix(self):
        """Run ruff with autofix"""
        print("🔄 Running ruff autofix...")

        # Format first
        exit_code, stdout, stderr = self.run_command("uv run ruff format zeta_vn/")
        if exit_code == 0:
            self.fixes_applied.append("Applied ruff formatting")

        # Then fix what can be auto-fixed
        exit_code, stdout, stderr = self.run_command("uv run ruff check --fix zeta_vn/")
        if exit_code == 0:
            self.fixes_applied.append("Applied ruff auto-fixes")

    def run_quality_check(self) -> dict[str, Any]:
        """Run quality checks and return results"""
        print("📊 Running quality checks...")

        results = {}

        # Ruff check
        exit_code, stdout, stderr = self.run_command("uv run ruff check . --statistics")
        results["ruff"] = {"exit_code": exit_code, "output": stdout, "errors": stderr}

        # MyPy check (basic)
        exit_code, stdout, stderr = self.run_command("uv run mypy zeta_vn/core/security/ --no-error-summary")
        results["mypy"] = {"exit_code": exit_code, "output": stdout, "errors": stderr}

        return results

    def generate_report(self):
        """Generate improvement report"""
        print("\n📋 IMPROVEMENT REPORT")
        print("=" * 50)

        if self.fixes_applied:
            print("✅ Fixes Applied:")
            for fix in self.fixes_applied:
                print(f"  - {fix}")
        else:
            print("ℹ️  No fixes applied (dry run mode)" if self.dry_run else "⚠️  No fixes needed")

        print("\n🔍 Quality Check Results:")
        results = self.run_quality_check()

        for tool, result in results.items():
            status = "✅ PASS" if result["exit_code"] == 0 else "❌ FAIL"
            print(f"  {tool.upper()}: {status}")
            if result["exit_code"] != 0 and result["output"]:
                print(f"    Output: {result['output'][:200]}...")


def main():
    parser = argparse.ArgumentParser(description="Fix ZETA_VN code quality issues")
    parser.add_argument("--phase", choices=["1", "2", "3"], default="1", help="Which phase to run (default: 1)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    fixer = ZetaCodeFixer(project_root, dry_run=args.dry_run)

    print(f"🚀 Starting ZETA_VN Code Quality Fix - Phase {args.phase}")
    print(f"📁 Project root: {project_root}")
    print(f"🔍 Dry run mode: {args.dry_run}")
    print()

    try:
        if args.phase == "1":
            fixer.fix_phase1_critical_syntax()
        elif args.phase == "2":
            print("Phase 2: Security enhancements (not implemented yet)")
        elif args.phase == "3":
            print("Phase 3: Production readiness (not implemented yet)")

        fixer.generate_report()

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
