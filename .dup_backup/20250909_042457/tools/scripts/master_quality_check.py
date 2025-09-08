#!/usr/bin/env python3
"""
tools/master_quality_check.py

Script tổng thể kiểm tra quality cho cả server và desktop projects.
Chạy tất cả checks: architecture, typing, tests, contracts, consistency.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import Exception
import FileNotFoundError
import bool
import check
import command
import critical
import cwd
import e
import int
import len
import list
import name
import output
import print
import self
import str
import sum
import tuple

ROOT = Path(__file__).resolve().parents[1]
SERVER_ROOT = ROOT / "zeta_vn"
DESKTOP_ROOT = ROOT / "desktop_ai_zeta"


class QualityCheck:
    def __init__(
        self,
        name: str,
        command: list[str],
        cwd: Path | None = None,
        critical: bool = True,
    ):
        self.name = name
        self.command = command
        self.cwd = cwd or ROOT
        self.critical = critical  # Nếu False thì warning thôi, không fail


class MasterQualityChecker:
    def __init__(self) -> None:
        self.checks = self._define_checks()
        self.results: list[tuple[QualityCheck, bool, str]] = []

    def _define_checks(self) -> list[QualityCheck]:
        """Định nghĩa tất cả quality checks."""
        return [
            # 1. Cross-project consistency
            QualityCheck(
                "Cross-Project Consistency",
                ["uv", "run", "python", "tools/cross_project_guard.py"],
            ),
            # 2. Architecture consistency (server)
            QualityCheck(
                "Server Architecture Consistency",
                ["uv", "run", "python", "tools/copilot_guard.py"],
            ),
            # 3. Server code quality
            QualityCheck("Server Format Check", ["uv", "run", "ruff", "format", "--check", "."]),
            QualityCheck("Server Lint Check", ["uv", "run", "ruff", "check", "."]),
            QualityCheck("Server Type Check", ["uv", "run", "mypy", "."]),
            QualityCheck("Server Tests", ["uv", "run", "pytest", "-q", "--maxfail=5"]),
            # 4. Server security (non-critical)
            QualityCheck(
                "Server Security Scan",
                ["uv", "run", "bandit", "-q", "-r", "zeta_vn"],
                critical=False,
            ),
            QualityCheck(
                "Server Dependency Audit",
                ["uv", "run", "pip-audit", "-q"],
                critical=False,
            ),
            # 5. Desktop quality (nếu có node_modules)
            QualityCheck("Desktop Type Check", ["npm", "run", "typecheck"], cwd=DESKTOP_ROOT),
            QualityCheck("Desktop Lint Check", ["npm", "run", "lint"], cwd=DESKTOP_ROOT),
            QualityCheck("Desktop Tests", ["npm", "run", "test"], cwd=DESKTOP_ROOT),
            # 6. Contract validation
            QualityCheck(
                "API Contract Guard",
                ["node", "scripts/contract_guard.mjs"],
                cwd=DESKTOP_ROOT,
            ),
            # 7. Import architecture (server)
            QualityCheck(
                "Import Architecture Check",
                ["uv", "run", "lint-imports", "-c", "importlinter.ini"],
                critical=False,
            ),
        ]

    def run_all(self) -> bool:
        """Chạy tất cả checks và return success status."""
        print("🚀 MASTER QUALITY CHECK - Server + Desktop")
        print("=" * 60)

        # Kiểm tra prerequisites
        if not self._check_prerequisites():
            return False

        # Chạy từng check
        total_count = self._run_all_checks()

        # Report kết quả và return success status
        return self._finalize_results(total_count)

    def _run_all_checks(self) -> int:
        """Chạy tất cả checks applicable."""
        total_count = 0

        for check in self.checks:
            if not self._should_run_check(check):
                print(f"⏭️  Skipping {check.name} (not applicable)")
                continue

            total_count += 1
            print(f"\n🔍 Running: {check.name}")

            success, output = self._run_check(check)
            self.results.append((check, success, output))

            self._report_check_result(check, success, output)

        return total_count

    def _report_check_result(self, check: QualityCheck, success: bool, output: str) -> None:
        """Report kết quả một check."""
        if success:
            print(f"✅ {check.name}: PASSED")
        else:
            status = "⚠️ WARNING" if not check.critical else "❌ FAILED"
            print(f"{status} {check.name}")
            if output.strip():
                print(f"   Output: {output[:200]}...")

            if check.critical:
                print(f"   💡 Khắc phục: {self._get_fix_suggestion(check)}")

    def _finalize_results(self, total_count: int) -> bool:
        """Finalize và report kết quả tổng thể."""
        success_count = sum(1 for _, success, _ in self.results if success)

        # Report final results
        self._report_final_results(success_count, total_count)

        # Return success if all critical checks passed
        critical_failures = [(check, success) for check, success, _ in self.results if check.critical and not success]

        return len(critical_failures) == 0

    def _check_prerequisites(self) -> bool:
        """Kiểm tra các điều kiện tiên quyết."""
        print("🔧 Checking prerequisites...")

        # Check uv
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ uv not found. Install: pip install uv")
            return False

        # Check node (nếu có desktop project)
        if DESKTOP_ROOT.exists():
            try:
                subprocess.run(
                    ["node", "--version"],
                    capture_output=True,
                    check=True,
                    cwd=DESKTOP_ROOT,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Node.js not found. Install Node.js")
                return False

            # Check npm dependencies
            if not (DESKTOP_ROOT / "node_modules").exists():
                print("⚠️  Desktop dependencies not installed. Running npm install...")
                try:
                    subprocess.run(["npm", "install"], check=True, cwd=DESKTOP_ROOT)
                except subprocess.CalledProcessError:
                    print("❌ Failed to install desktop dependencies")
                    return False

        print("✅ Prerequisites OK")
        return True

    def _should_run_check(self, check: QualityCheck) -> bool:
        """Xác định có nên chạy check này không."""
        # Desktop checks chỉ chạy nếu có desktop project
        if "Desktop" in check.name and not DESKTOP_ROOT.exists():
            return False

        # Contract checks chỉ chạy nếu có script
        if "Contract" in check.name:
            script_path = DESKTOP_ROOT / "scripts" / "contract_guard.mjs"
            return script_path.exists()

        return True

    def _run_check(self, check: QualityCheck) -> tuple[bool, str]:
        """Chạy một check và return (success, output)."""
        try:
            result = subprocess.run(
                check.command,
                check=False,
                cwd=check.cwd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            return result.returncode == 0, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return False, "Timeout after 5 minutes"
        except Exception as e:
            return False, f"Exception: {e}"

    def _get_fix_suggestion(self, check: QualityCheck) -> str:
        """Gợi ý cách khắc phục cho từng loại check."""
        suggestions = {
            "Cross-Project Consistency": "Chạy: cd desktop_ai_zeta && npm run api:gen",
            "Server Architecture Consistency": "Thêm tests hoặc cập nhật file liên quan theo copilot_guard",
            "Server Format Check": "Chạy: uv run ruff format .",
            "Server Lint Check": "Chạy: uv run ruff check --fix .",
            "Server Type Check": "Sửa type errors theo mypy output",
            "Server Tests": "Kiểm tra failed tests và sửa",
            "Desktop Type Check": "cd desktop_ai_zeta && npm run typecheck",
            "Desktop Lint Check": "cd desktop_ai_zeta && npm run lint:fix",
            "Desktop Tests": "cd desktop_ai_zeta && npm run test",
            "API Contract Guard": "cd desktop_ai_zeta && node scripts/generate_openapi_types.mjs",
        }

        return suggestions.get(check.name, "Kiểm tra command output để biết cách sửa")

    def _report_final_results(self, success_count: int, total_count: int) -> None:
        """Report kết quả tổng thể."""
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)

        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        print(f"✅ Passed: {success_count}/{total_count} ({success_rate:.1f}%)")

        # Group results by status
        passed = [check for check, success, _ in self.results if success]
        failed_critical = [check for check, success, _ in self.results if not success and check.critical]
        failed_non_critical = [check for check, success, _ in self.results if not success and not check.critical]

        if passed:
            print(f"\n✅ PASSED ({len(passed)}):")
            for check in passed:
                print(f"   - {check.name}")

        if failed_critical:
            print(f"\n❌ FAILED CRITICAL ({len(failed_critical)}):")
            for check in failed_critical:
                print(f"   - {check.name}")

        if failed_non_critical:
            print(f"\n⚠️  WARNINGS ({len(failed_non_critical)}):")
            for check in failed_non_critical:
                print(f"   - {check.name}")

        if failed_critical:
            print("\n💡 Next steps:")
            print("   1. Fix critical failures first")
            print("   2. Run individual checks to debug")
            print("   3. Re-run master check")
        else:
            print(f"\n🎉 ALL CRITICAL CHECKS PASSED! Quality score: {success_rate:.1f}%")


def main() -> None:
    """Main entry point."""
    checker = MasterQualityChecker()
    success = checker.run_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
