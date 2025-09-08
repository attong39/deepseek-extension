#!/usr/bin/env python3
"""
📦 DEPENDENCY SAFETY CHECKER - Secure Dependency Management

Kiểm tra và quản lý dependencies một cách an toàn.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import Exception
import bool
import dict
import e
import f
import isinstance
import len
import list
import max
import pkg
import print
import project_root
import rec
import self
import str


class DependencySafetyChecker:
    """Safe dependency management."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        self.project_root = project_root
        self.pyproject_toml = project_root / "pyproject.toml"
        self.report_file = project_root / "dependency_report.json"

    def get_installed_packages(self) -> list[dict[str, Any]]:
        """Get list of installed packages."""
        try:
            result = subprocess.run(
                ["uv", "pip", "list", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ Failed to get package list: {e}")
        return []

    def check_vulnerabilities(self) -> dict[str, Any]:
        """Check for security vulnerabilities in dependencies."""
        print("🔍 Checking for security vulnerabilities...")

        try:
            result = subprocess.run(
                ["uv", "run", "pip-audit", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return {
                    "status": "clean",
                    "vulnerabilities": [],
                    "message": "No known vulnerabilities found",
                }
            else:
                # Parse vulnerability report
                try:
                    vulns = json.loads(result.stdout)
                    return {
                        "status": "vulnerable",
                        "vulnerabilities": vulns,
                        "count": len(vulns) if isinstance(vulns, list) else 0,
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "message": "Could not parse vulnerability report",
                        "stderr": result.stderr,
                    }
        except Exception as e:
            return {"status": "error", "message": f"Failed to run vulnerability check: {e}"}

    def check_outdated_packages(self) -> list[dict[str, Any]]:
        """Check for outdated packages."""
        print("📊 Checking for outdated packages...")

        try:
            result = subprocess.run(
                ["uv", "pip", "list", "--outdated", "--format", "json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
        except Exception as e:
            print(f"❌ Failed to check outdated packages: {e}")
        return []

    def analyze_dependency_tree(self) -> dict[str, Any]:
        """Analyze dependency relationships."""
        print("🌳 Analyzing dependency tree...")

        try:
            subprocess.run(
                ["uv", "pip", "show", "--verbose"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Basic analysis - count dependencies
            packages = self.get_installed_packages()

            analysis = {
                "total_packages": len(packages),
                "direct_dependencies": 0,  # Would need pyproject.toml parsing
                "transitive_dependencies": 0,
                "package_sizes": {},
                "license_distribution": {},
            }

            return analysis

        except Exception as e:
            return {"error": f"Failed to analyze dependencies: {e}"}

    def suggest_updates(self) -> dict[str, Any]:
        """Suggest safe dependency updates."""
        outdated = self.check_outdated_packages()
        vulns = self.check_vulnerabilities()

        suggestions = {
            "security_updates": [],
            "minor_updates": [],
            "major_updates": [],
            "recommendations": [],
        }

        # Prioritize security updates
        if vulns["status"] == "vulnerable":
            suggestions["security_updates"] = vulns["vulnerabilities"]
            suggestions["recommendations"].append(
                "🚨 URGENT: Update packages with security vulnerabilities immediately"
            )

        # Categorize other updates
        for pkg in outdated:
            pkg.get("name", "")
            current = pkg.get("version", "")
            latest = pkg.get("latest_version", "")

            # Simple version comparison (could be improved)
            if current and latest:
                current_parts = current.split(".")
                latest_parts = latest.split(".")

                if len(current_parts) >= 1 and len(latest_parts) >= 1:
                    if current_parts[0] != latest_parts[0]:
                        suggestions["major_updates"].append(pkg)
                    else:
                        suggestions["minor_updates"].append(pkg)

        # Add general recommendations
        if len(suggestions["minor_updates"]) > 5:
            suggestions["recommendations"].append("📦 Consider updating multiple minor versions in batches")

        if len(suggestions["major_updates"]) > 0:
            suggestions["recommendations"].append("⚠️ Major version updates require careful testing")

        return suggestions

    def generate_report(self) -> dict[str, Any]:
        """Generate comprehensive dependency report."""
        print("📋 Generating dependency safety report...")

        report = {
            "timestamp": datetime.now(UTC).isoformat(),
            "project_root": str(self.project_root),
            "packages": self.get_installed_packages(),
            "vulnerabilities": self.check_vulnerabilities(),
            "outdated": self.check_outdated_packages(),
            "analysis": self.analyze_dependency_tree(),
            "suggestions": self.suggest_updates(),
        }

        # Calculate safety score
        len(report["packages"])
        vuln_count = 0
        if report["vulnerabilities"]["status"] == "vulnerable":
            vuln_count = report["vulnerabilities"].get("count", 0)

        outdated_count = len(report["outdated"])

        # Simple scoring (could be improved)
        safety_score = max(0, 100 - (vuln_count * 10) - (outdated_count * 2))

        report["safety_score"] = safety_score
        report["recommendations"] = []

        if vuln_count > 0:
            report["recommendations"].append(f"🚨 {vuln_count} packages have security vulnerabilities")

        if outdated_count > 10:
            report["recommendations"].append(f"📦 {outdated_count} packages are outdated")

        if safety_score >= 90:
            report["status"] = "excellent"
        elif safety_score >= 75:
            report["status"] = "good"
        elif safety_score >= 60:
            report["status"] = "fair"
        else:
            report["status"] = "needs_attention"

        return report

    def save_report(self, report: dict[str, Any]) -> None:
        """Save report to file."""
        with self.report_file.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 Report saved to: {self.report_file}")

    def print_summary(self, report: dict[str, Any]) -> None:
        """Print summary to console."""
        print("\n" + "=" * 60)
        print("📦 DEPENDENCY SAFETY REPORT")
        print("=" * 60)
        print(f"📊 Safety Score: {report['safety_score']}/100 ({report['status'].upper()})")
        print(f"📦 Total Packages: {len(report['packages'])}")
        print(f"🔒 Vulnerabilities: {report['vulnerabilities'].get('count', 0)}")
        print(f"📈 Outdated: {len(report['outdated'])}")
        print("=" * 60)

        if report.get("recommendations"):
            print("💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  {rec}")
            print("=" * 60)

        return report["safety_score"] >= 75

    def run_check(self) -> bool:
        """Run complete dependency safety check."""
        print("🚀 Starting dependency safety check...")

        report = self.generate_report()
        self.save_report(report)
        return self.print_summary(report)


def main() -> None:
    """Main entry point."""
    checker = DependencySafetyChecker()
    is_safe = checker.run_check()

    if not is_safe:
        print("\n⚠️ Dependency safety score below 75. Please review dependencies.")
        sys.exit(1)
    else:
        print("\n✅ Dependencies are safe!")
        sys.exit(0)


if __name__ == "__main__":
    main()
