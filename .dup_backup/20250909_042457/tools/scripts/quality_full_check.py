#!/usr/bin/env python3
"""
ZETA AI - Hệ thống kiểm tra chất lượng code đầy đủ
Tích hợp tất cả công cụ: ruff, mypy, pytest, bandit, pip-audit, vulture, frontend checks
Tuân thủ domain-driven architecture và Clean Architecture patterns
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import Exception
import bool
import capture
import code
import cwd
import dict
import e
import env
import float
import int
import len
import level
import list
import msg
import name
import print
import round
import self
import step
import step_duration
import str
import tool
import tuple

# === Cấu hình ===
ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
PY_SRC = "zeta_vn"
FE_DIR = ROOT / "desktop_ai_zeta"

# Quality gates thresholds
DEFAULT_COVERAGE_MIN = 80
DEFAULT_FOCUS_INDEX_MIN = 60
DEFAULT_VULN_SEVERITY = "HIGH"

TOOLS_CHECK = {
    "ruff": ["ruff", "--version"],
    "mypy": ["mypy", "--version"],
    "pytest": ["pytest", "--version"],
    "bandit": ["bandit", "--version"],
    "pip-audit": ["pip-audit", "--version"],
    "vulture": ["vulture", "--version"],
}


class QualityChecker:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.results: list[tuple[str, int, float]] = []
        self.total_start = time.time()

    def log(self, msg: str, level: str = "INFO") -> None:
        """Log với timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = f"[{timestamp}] [{level}]"
        print(f"{prefix} {msg}")

    def run_cmd(
        self,
        cmd: list[str],
        cwd: Path | None = None,
        capture: bool = False,
        env: dict[str, str] | None = None,
    ) -> tuple[int, str]:
        """Chạy command với logging và error handling"""
        cmd_str = " ".join(cmd)
        self.log(f"$ {cmd_str}")

        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or ROOT,
                env=env or os.environ.copy(),
                capture_output=capture,
                text=True,
                timeout=300,  # 5 phút timeout
            )
            time.time() - start_time

            if capture:
                return result.returncode, result.stdout
            else:
                return result.returncode, ""

        except subprocess.TimeoutExpired:
            self.log(f"Command timeout: {cmd_str}", "ERROR")
            return 124, ""
        except Exception as e:
            self.log(f"Command failed: {cmd_str} - {e}", "ERROR")
            return 1, ""

    def ensure_reports_dir(self) -> None:
        """Tạo thư mục reports"""
        REPORTS.mkdir(parents=True, exist_ok=True)

    def export_requirements(self) -> Path | None:
        """Export requirements từ uv cho pip-audit"""
        cache_dir = ROOT / ".cache"
        cache_dir.mkdir(exist_ok=True)
        req_file = cache_dir / "requirements.lock.txt"

        code, _ = self.run_cmd(
            [
                "uv",
                "export",
                "--format=requirements-txt",
                "--all-extras",
                "--dev",
                "-o",
                str(req_file),
            ]
        )

        return req_file if code == 0 and req_file.exists() else None

    def check_tool_available(self, tool: str) -> bool:
        """Kiểm tra tool có sẵn không"""
        if tool in TOOLS_CHECK:
            code, _ = self.run_cmd(TOOLS_CHECK[tool], capture=True)
            return code == 0
        return shutil.which(tool) is not None

    def uvrun(self, tool: str, *args: str) -> list[str]:
        """Wrapper uv run hoặc uvx"""
        if self.check_tool_available(tool):
            return ["uv", "run", tool, *args]
        return ["uvx", tool, *args]

    def run_step(self, name: str, cmd: list[str], cwd: Path | None = None) -> bool:
        """Chạy một bước kiểm tra"""
        self.log(f"=== {name} ===", "INFO")
        start_time = time.time()

        code, _ = self.run_cmd(cmd, cwd=cwd)
        duration = time.time() - start_time

        self.results.append((name, code, duration))

        if code == 0:
            self.log(f"✅ {name} - PASS ({duration:.1f}s)", "INFO")
            return True
        else:
            self.log(f"❌ {name} - FAIL (exit {code}) ({duration:.1f}s)", "ERROR")
            return False

    def check_python_format(self) -> bool:
        """Kiểm tra Python formatting"""
        return self.run_step("Python Format Check", self.uvrun("ruff", "format", "--check", "."))

    def check_python_lint(self) -> bool:
        """Kiểm tra Python linting"""
        return self.run_step("Python Lint (Ruff)", self.uvrun("ruff", "check", "--output-format=github", "."))

    def check_python_types(self) -> bool:
        """Kiểm tra Python type checking"""
        return self.run_step("Python Type Check (Mypy)", self.uvrun("mypy", PY_SRC))

    def check_python_tests(self) -> bool:
        """Chạy Python tests với coverage"""
        coverage_xml = REPORTS / "coverage.xml"
        return self.run_step(
            "Python Tests + Coverage",
            self.uvrun(
                "pytest",
                "-q",
                f"--cov={PY_SRC}",
                "--cov-report=term-missing",
                f"--cov-report=xml:{coverage_xml}",
                "--maxfail=3",
                "--disable-warnings",
            ),
        )

    def check_security_bandit(self) -> bool:
        """Kiểm tra security với Bandit"""
        report_file = REPORTS / "bandit.txt"
        return self.run_step(
            "Security Scan (Bandit)",
            self.uvrun("bandit", "-r", PY_SRC, "-x", "tests", "-q", "-f", "txt", "-o", str(report_file)),
        )

    def check_security_audit(self) -> bool:
        """Kiểm tra vulnerabilities với pip-audit"""
        report_file = REPORTS / "pip-audit.json"
        req_file = self.export_requirements()

        if req_file:
            cmd = self.uvrun(
                "pip-audit",
                "-r",
                str(req_file),
                "--progress-spinner=off",
                "--require-hashes=false",
                "--output",
                str(report_file),
                "--format",
                "json",
            )
        else:
            cmd = self.uvrun(
                "pip-audit",
                "--progress-spinner=off",
                "--output",
                str(report_file),
                "--format",
                "json",
            )

        return self.run_step("Vulnerability Audit (pip-audit)", cmd)

    def check_dead_code(self) -> bool:
        """Kiểm tra dead code với Vulture"""
        return self.run_step("Dead Code Detection (Vulture)", self.uvrun("vulture", PY_SRC, "--min-confidence", "80"))

    def check_imports(self) -> bool:
        """Kiểm tra import linting"""
        if (ROOT / "importlinter.ini").exists():
            return self.run_step("Import Linting", self.uvrun("lint-imports"))
        return True

    def check_build(self) -> bool:
        """Kiểm tra build package"""
        return self.run_step("Package Build Test", ["uv", "build"])

    def check_focus_index(self) -> bool:
        """Kiểm tra Focus Index nếu có script"""
        focus_script = ROOT / "scripts" / "focus_index.py"
        if focus_script.exists():
            return self.run_step(
                "Focus Index Check",
                self.uvrun("python", str(focus_script), "--fail-under", str(self.args.focus_min)),
            )
        return True

    def check_predeploy(self) -> bool:
        """Chạy predeploy checks nếu có"""
        predeploy_script = ROOT / "scripts" / "predeploy_check.py"
        if predeploy_script.exists():
            return self.run_step("Pre-deploy Validation", self.uvrun("python", str(predeploy_script)))
        return True

    def check_frontend(self) -> bool:
        """Kiểm tra Frontend (TypeScript/React) nếu có"""
        if not (self.args.frontend and FE_DIR.exists()):
            return True

        self.log("🌐 Frontend checks enabled", "INFO")

        # Detect package manager
        use_pnpm = (FE_DIR / "pnpm-lock.yaml").exists()
        pkg_mgr = "pnpm" if use_pnpm else "npm"

        steps = [
            (
                f"Frontend Install ({pkg_mgr})",
                [pkg_mgr, "ci" if pkg_mgr == "npm" else "install", "--frozen-lockfile"],
            ),
            ("Frontend Lint", [pkg_mgr, "run", "lint"]),
            ("Frontend Type Check", [pkg_mgr, "run", "typecheck"]),
            ("Frontend Tests", [pkg_mgr, "test", "--", "--passWithNoTests"]),
        ]

        success = True
        for name, cmd in steps:
            if not self.run_step(name, cmd, cwd=FE_DIR):
                success = False
                if not self.args.continue_on_error:
                    break

        return success

    def validate_coverage(self) -> bool:
        """Kiểm tra coverage threshold"""
        coverage_xml = REPORTS / "coverage.xml"
        if not coverage_xml.exists():
            return True

        try:
            import xml.etree.ElementTree as ET

            tree = ET.parse(coverage_xml)
            rate = float(tree.getroot().attrib.get("line-rate", "0"))
            coverage_pct = int(round(rate * 100))

            self.log(f"Coverage: {coverage_pct}%", "INFO")

            if coverage_pct < self.args.coverage_min:
                self.log(f"❌ Coverage {coverage_pct}% < {self.args.coverage_min}%", "ERROR")
                return False
            else:
                self.log(f"✅ Coverage {coverage_pct}% >= {self.args.coverage_min}%", "INFO")
                return True

        except Exception as e:
            self.log(f"⚠️  Cannot parse coverage.xml: {e}", "WARN")
            return True

    def print_summary(self) -> bool:
        """In tổng kết và trả về success status"""
        duration = time.time() - self.total_start

        print("\n" + "=" * 60)
        print("🎯 QUALITY CHECK SUMMARY")
        print("=" * 60)

        failed_steps = []
        total_time = 0

        for name, code, step_duration in self.results:
            status = "✅ PASS" if code == 0 else "❌ FAIL"
            print(f"{status:8} {name:30} ({step_duration:5.1f}s)")
            total_time += step_duration

            if code != 0:
                failed_steps.append(name)

        print("-" * 60)
        print(f"Total time: {duration:.1f}s")
        print(f"Steps: {len(self.results)}")
        print(f"Failed: {len(failed_steps)}")

        if failed_steps:
            print("\n❌ FAILED STEPS:")
            for step in failed_steps:
                print(f"  - {step}")
            print(f"\n💡 Check logs above and reports in: {REPORTS}")
            return False
        else:
            print("\n🎉 ALL CHECKS PASSED!")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="ZETA AI - Full Quality Check Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                           # Full check
  %(prog)s --fast                          # Quick check (lint+type+test)
  %(prog)s --all --frontend               # Include frontend checks
  %(prog)s --coverage-min 85 --focus-min 70  # Custom thresholds
        """,
    )

    parser.add_argument("--all", action="store_true", help="Chạy toàn bộ pipeline kiểm tra")
    parser.add_argument("--fast", action="store_true", help="Chạy nhanh (format+lint+type+test)")
    parser.add_argument("--frontend", action="store_true", help="Bao gồm kiểm tra Frontend/TypeScript")
    parser.add_argument(
        "--coverage-min",
        type=int,
        default=DEFAULT_COVERAGE_MIN,
        help=f"Coverage threshold tối thiểu (default: {DEFAULT_COVERAGE_MIN})",
    )
    parser.add_argument(
        "--focus-min",
        type=int,
        default=DEFAULT_FOCUS_INDEX_MIN,
        help=f"Focus Index threshold tối thiểu (default: {DEFAULT_FOCUS_INDEX_MIN})",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Tiếp tục chạy khi có lỗi (không dừng ngay)",
    )
    parser.add_argument("--reports-only", action="store_true", help="Chỉ tạo reports, không fail trên lỗi")

    args = parser.parse_args()

    if not args.all and not args.fast:
        parser.print_help()
        print("\n❗ Hãy chọn --all hoặc --fast")
        sys.exit(1)

    checker = QualityChecker(args)
    checker.ensure_reports_dir()

    checker.log("🚀 Starting ZETA Quality Pipeline", "INFO")
    checker.log(f"Mode: {'FULL' if args.all else 'FAST'}", "INFO")
    checker.log(f"Frontend: {'YES' if args.frontend else 'NO'}", "INFO")

    # === Python checks ===
    steps_success = []

    # Format & Lint
    steps_success.append(checker.check_python_format())
    steps_success.append(checker.check_python_lint())

    # Type checking
    steps_success.append(checker.check_python_types())

    # Tests + Coverage
    steps_success.append(checker.check_python_tests())

    if args.all:
        # Security scans
        steps_success.append(checker.check_security_bandit())
        steps_success.append(checker.check_security_audit())

        # Code quality
        steps_success.append(checker.check_dead_code())
        steps_success.append(checker.check_imports())

        # Build test
        steps_success.append(checker.check_build())

        # Custom checks
        steps_success.append(checker.check_focus_index())
        steps_success.append(checker.check_predeploy())

        # Frontend
        steps_success.append(checker.check_frontend())

    # Coverage validation
    steps_success.append(checker.validate_coverage())

    # Summary
    all_passed = checker.print_summary()

    # Exit codes
    if args.reports_only or all_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
