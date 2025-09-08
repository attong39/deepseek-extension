#!/usr/bin/env python3
"""
🛡️ SAFETY DASHBOARD - Comprehensive Project Safety Overview

Dashboard tổng quan về tình trạng an toàn toàn bộ dự án.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import Exception
import IndexError
import ValueError
import bool
import dict
import e
import f
import int
import isinstance
import issue
import len
import line
import list
import max
import min
import print
import project_root
import py_file
import self
import str
import tuple


class SafetyDashboard:
    """Comprehensive project safety dashboard."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        self.project_root = project_root
        self.reports_dir = project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)

    def get_git_info(self) -> dict[str, Any]:
        """Get git repository information."""
        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Get last commit
            commit_result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%an|%ad|%s"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Get repository status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            commit_info = commit_result.stdout.strip().split("|") if commit_result.stdout else ["", "", "", ""]

            return {
                "branch": branch_result.stdout.strip(),
                "last_commit": {
                    "hash": commit_info[0][:8] if commit_info[0] else "",
                    "author": commit_info[1] if len(commit_info) > 1 else "",
                    "date": commit_info[2] if len(commit_info) > 2 else "",
                    "message": commit_info[3] if len(commit_info) > 3 else "",
                },
                "uncommitted_changes": len(status_result.stdout.strip().splitlines()) if status_result.stdout else 0,
                "is_clean": not bool(status_result.stdout.strip()),
            }
        except Exception:
            return {"error": "Could not get git information"}

    def run_quick_ruff_check(self) -> dict[str, Any]:
        """Quick ruff check for current status."""
        try:
            result = subprocess.run(
                ["uv", "run", "ruff", "check", "zeta_vn/", "--statistics"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {"status": "clean", "errors": 0}

            # Parse error statistics
            lines = result.stdout.strip().split("\n")
            total_errors = 0
            error_types = {}

            for line in lines:
                if line.strip() and not line.startswith("Found"):
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        count = int(parts[0])
                        error_type = parts[1]
                        error_types[error_type] = count
                        total_errors += count

            return {
                "status": "has_errors",
                "total_errors": total_errors,
                "error_types": error_types,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_test_status(self) -> dict[str, Any]:
        """Get quick test status."""
        try:
            # Quick test run
            result = subprocess.run(
                ["uv", "run", "pytest", "--collect-only", "-q"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                # Count collected tests
                lines = result.stdout.strip().split("\n")
                test_count = 0
                for line in lines:
                    if "collected" in line and "items" in line:
                        try:
                            test_count = int(line.split()[0])
                            break
                        except (ValueError, IndexError):
                            continue

                return {"status": "available", "test_count": test_count, "can_run": True}
            else:
                return {"status": "error", "can_run": False, "message": "Test collection failed"}

        except Exception as e:
            return {"status": "error", "can_run": False, "message": str(e)}

    def get_security_status(self) -> dict[str, Any]:
        """Get security scan status."""
        try:
            # Quick bandit check
            result = subprocess.run(
                ["uv", "run", "bandit", "-r", "zeta_vn", "--quiet", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {"status": "clean", "issues": 0}
            else:
                try:
                    data = json.loads(result.stdout)
                    issue_count = len(data.get("results", []))
                    return {"status": "has_issues", "issues": issue_count}
                except json.JSONDecodeError:
                    return {"status": "unknown", "message": "Could not parse security report"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_dependency_status(self) -> dict[str, Any]:
        """Get dependency status."""
        try:
            # Check for vulnerabilities
            result = subprocess.run(
                ["uv", "run", "pip-audit", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {"status": "clean", "vulnerabilities": 0}
            else:
                try:
                    data = json.loads(result.stdout)
                    vuln_count = len(data) if isinstance(data, list) else 0
                    return {"status": "has_vulnerabilities", "vulnerabilities": vuln_count}
                except json.JSONDecodeError:
                    return {"status": "unknown", "message": "Could not parse dependency report"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_project_stats(self) -> dict[str, Any]:
        """Get basic project statistics."""
        try:
            python_files = list(self.project_root.glob("**/*.py"))
            test_files = [f for f in python_files if "test" in str(f)]

            # Calculate total lines of code
            total_lines = 0
            for py_file in python_files:
                try:
                    with py_file.open(encoding="utf-8") as f:
                        total_lines += len(f.readlines())
                except Exception:
                    continue

            return {
                "python_files": len(python_files),
                "test_files": len(test_files),
                "total_lines": total_lines,
                "test_coverage_ratio": len(test_files) / len(python_files) if python_files else 0,
            }
        except Exception as e:
            return {"error": str(e)}

    def calculate_safety_score(self, data: dict[str, Any]) -> tuple[int, str]:
        """Calculate overall safety score."""
        score = 100
        issues = []

        # Git status (-5 points for uncommitted changes)
        git_info = data.get("git", {})
        if not git_info.get("is_clean", True):
            score -= 5
            issues.append("Uncommitted changes")

        # Code quality (-30 points for ruff errors)
        ruff_status = data.get("code_quality", {})
        if ruff_status.get("status") == "has_errors":
            error_count = ruff_status.get("total_errors", 0)
            penalty = min(30, error_count // 10)  # 1 point per 10 errors, max 30
            score -= penalty
            issues.append(f"{error_count} code quality issues")

        # Tests (-20 points if tests can't run)
        test_status = data.get("tests", {})
        if not test_status.get("can_run", False):
            score -= 20
            issues.append("Tests not runnable")

        # Security (-25 points for security issues)
        security_status = data.get("security", {})
        if security_status.get("status") == "has_issues":
            issue_count = security_status.get("issues", 0)
            penalty = min(25, issue_count * 5)  # 5 points per issue, max 25
            score -= penalty
            issues.append(f"{issue_count} security issues")

        # Dependencies (-20 points for vulnerabilities)
        deps_status = data.get("dependencies", {})
        if deps_status.get("status") == "has_vulnerabilities":
            vuln_count = deps_status.get("vulnerabilities", 0)
            penalty = min(20, vuln_count * 10)  # 10 points per vulnerability, max 20
            score -= penalty
            issues.append(f"{vuln_count} dependency vulnerabilities")

        score = max(0, min(100, score))

        # Determine status
        if score >= 90:
            status = "excellent"
        elif score >= 75:
            status = "good"
        elif score >= 60:
            status = "fair"
        else:
            status = "critical"

        return score, status, issues

    def generate_dashboard(self) -> dict[str, Any]:
        """Generate comprehensive safety dashboard."""
        print("🛡️ Generating safety dashboard...")

        dashboard = {
            "timestamp": datetime.now(UTC).isoformat(),
            "project_root": str(self.project_root),
            "git": self.get_git_info(),
            "code_quality": self.run_quick_ruff_check(),
            "tests": self.get_test_status(),
            "security": self.get_security_status(),
            "dependencies": self.get_dependency_status(),
            "project_stats": self.get_project_stats(),
        }

        # Calculate safety score
        score, status, issues = self.calculate_safety_score(dashboard)
        dashboard["safety_score"] = score
        dashboard["status"] = status
        dashboard["issues"] = issues

        return dashboard

    def print_dashboard(self, dashboard: dict[str, Any]) -> bool:
        """Print dashboard to console."""
        print("\n" + "=" * 80)
        print("🛡️  ZETA PROJECT SAFETY DASHBOARD")
        print("=" * 80)

        # Overall status
        score = dashboard["safety_score"]
        status = dashboard["status"]
        color_map = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "critical": "🔴"}

        print(f"\n📊 OVERALL SAFETY SCORE: {score}/100 {color_map.get(status, '⚪')} {status.upper()}")

        if dashboard.get("issues"):
            print("\n⚠️ ISSUES TO ADDRESS:")
            for issue in dashboard["issues"]:
                print(f"  • {issue}")

        # Git status
        git_info = dashboard.get("git", {})
        print("\n📂 GIT STATUS:")
        print(f"  Branch: {git_info.get('branch', 'unknown')}")
        print(f"  Clean: {'✅' if git_info.get('is_clean') else '❌'}")
        if git_info.get("uncommitted_changes", 0) > 0:
            print(f"  Uncommitted: {git_info['uncommitted_changes']} files")

        # Code quality
        ruff_status = dashboard.get("code_quality", {})
        print("\n🔍 CODE QUALITY:")
        if ruff_status.get("status") == "clean":
            print("  Status: ✅ Clean")
        elif ruff_status.get("status") == "has_errors":
            print(f"  Status: ❌ {ruff_status.get('total_errors', 0)} errors")
            if ruff_status.get("error_types"):
                for error_type, count in ruff_status["error_types"].items():
                    print(f"    {error_type}: {count}")

        # Tests
        test_status = dashboard.get("tests", {})
        print("\n🧪 TESTS:")
        print(f"  Available: {'✅' if test_status.get('can_run') else '❌'}")
        if test_status.get("test_count"):
            print(f"  Count: {test_status['test_count']} tests")

        # Security
        security_status = dashboard.get("security", {})
        print("\n🔒 SECURITY:")
        if security_status.get("status") == "clean":
            print("  Status: ✅ Clean")
        elif security_status.get("status") == "has_issues":
            print(f"  Status: ❌ {security_status.get('issues', 0)} issues")

        # Dependencies
        deps_status = dashboard.get("dependencies", {})
        print("\n📦 DEPENDENCIES:")
        if deps_status.get("status") == "clean":
            print("  Status: ✅ Clean")
        elif deps_status.get("status") == "has_vulnerabilities":
            print(f"  Status: ❌ {deps_status.get('vulnerabilities', 0)} vulnerabilities")

        # Project stats
        stats = dashboard.get("project_stats", {})
        print("\n📊 PROJECT STATS:")
        print(f"  Python files: {stats.get('python_files', 0)}")
        print(f"  Test files: {stats.get('test_files', 0)}")
        print(f"  Total lines: {stats.get('total_lines', 0):,}")
        print(f"  Test ratio: {stats.get('test_coverage_ratio', 0):.1%}")

        # Quick actions
        print("\n🚀 QUICK ACTIONS:")
        if ruff_status.get("status") == "has_errors":
            print("  • Run: python tools/safe_cleanup.py")
        if not test_status.get("can_run"):
            print("  • Run: python tools/test_safety.py --unit-only")
        if security_status.get("status") == "has_issues":
            print("  • Run: python tools/safety_audit.py")
        if deps_status.get("status") == "has_vulnerabilities":
            print("  • Run: python tools/dependency_safety.py")

        print("=" * 80)

        return score >= 75

    def save_dashboard(self, dashboard: dict[str, Any]) -> None:
        """Save dashboard to file."""
        dashboard_file = self.reports_dir / "safety_dashboard.json"
        with dashboard_file.open("w", encoding="utf-8") as f:
            json.dump(dashboard, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Dashboard saved to: {dashboard_file}")

    def run_dashboard(self) -> bool:
        """Run complete safety dashboard."""
        dashboard = self.generate_dashboard()
        self.save_dashboard(dashboard)
        return self.print_dashboard(dashboard)


def main() -> None:
    """Main entry point."""
    safety_dashboard = SafetyDashboard()
    is_safe = safety_dashboard.run_dashboard()

    if not is_safe:
        print("\n⚠️ Project safety score below 75. Please address the issues above.")
        sys.exit(1)
    else:
        print("\n✅ Project is in good shape!")
        sys.exit(0)


if __name__ == "__main__":
    main()
