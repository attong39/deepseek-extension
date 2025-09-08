"""Security monitoring và auto-patching system.

Tự động quét vulnerabilities và thực hiện auto-patch có kiểm soát.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any
import Exception
import bandit_result
import bool
import code
import dep
import dict
import e
import float
import int
import isinstance
import issue
import len
import list
import output
import pip_audit_result
import pkg
import print
import result
import set
import str
import sum
import target_path
import timeout
import tool_name
import tuple
import v
import vuln


@dataclass
class VulnerabilityReport:
    """Báo cáo vulnerability từ security scan."""

    package_name: str
    current_version: str
    vulnerability_id: str
    severity: str
    description: str
    fix_version: str | None = None
    cve_id: str | None = None
    exploitable: bool = False


@dataclass
class SecurityScanResult:
    """Kết quả của security scan tổng thể."""

    timestamp: float
    pip_audit_result: dict[str, Any]
    bandit_result: dict[str, Any]
    vulnerabilities: list[VulnerabilityReport]
    patched_packages: list[str]
    scan_errors: list[str]
    total_issues: int
    critical_issues: int


# Environment variables cho security control
ALLOW_AUTO_PATCH_ENV = "ZETA_SELF_SECURITY_AUTO_PATCH"
PATCH_ALLOWLIST_ENV = "ZETA_PATCH_ALLOW"


def _run_command(cmd: list[str], timeout: int = 300) -> tuple[int, str]:
    """Run command với timeout và return (exit_code, output)."""
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        output, _ = process.communicate()
        return process.returncode, output
    except subprocess.TimeoutExpired:
        process.kill()
        return -1, f"Command timed out after {timeout}s"
    except Exception as e:
        return -1, f"Command failed: {e}"


def _is_uv_available() -> bool:
    """Check if uv command is available."""
    return (
        os.system(
            "uv --version >nul 2>&1"
            if os.name == "nt"
            else "uv --version >/dev/null 2>&1"
        )
        == 0
    )


def pip_audit_scan() -> dict[str, Any]:
    """Run pip-audit security scan."""
    if _is_uv_available():
        cmd = ["uv", "run", "pip-audit", "-f", "json"]
    else:
        cmd = [sys.executable, "-m", "pip_audit", "-f", "json"]

    code, output = _run_command(cmd)

    try:
        if code == 0:
            data = json.loads(output)
        else:
            # pip-audit returns non-zero when vulnerabilities found
            try:
                data = json.loads(output)
            except json.JSONDecodeError:
                data = {"error": "parse_failed", "raw_output": output}
    except json.JSONDecodeError:
        data = {"error": "invalid_json", "raw_output": output}

    return {"exit_code": code, "result": data, "command": " ".join(cmd)}


def bandit_scan(target_path: str = "zeta_vn") -> dict[str, Any]:
    """Run Bandit static security analysis."""
    if _is_uv_available():
        cmd = ["uv", "run", "bandit", "-q", "-r", target_path, "-f", "json"]
    else:
        cmd = [sys.executable, "-m", "bandit", "-q", "-r", target_path, "-f", "json"]

    code, output = _run_command(cmd)

    try:
        data = json.loads(output) if output.strip() else {}
    except json.JSONDecodeError:
        data = {"error": "parse_failed", "raw_output": output}

    return {"exit_code": code, "result": data, "command": " ".join(cmd)}


def _parse_vulnerabilities(
    pip_audit_result: dict[str, Any],
) -> list[VulnerabilityReport]:
    """Parse vulnerabilities từ pip-audit result."""
    vulnerabilities = []

    if not isinstance(pip_audit_result.get("result"), dict):
        return vulnerabilities

    dependencies = pip_audit_result["result"].get("dependencies", [])

    for dep in dependencies:
        package_name = dep.get("name", "unknown")
        current_version = dep.get("version", "unknown")

        for vuln in dep.get("vulns", []):
            fix_versions = vuln.get("fix_versions", [])
            fix_version = fix_versions[0] if fix_versions else None

            vulnerability = VulnerabilityReport(
                package_name=package_name,
                current_version=current_version,
                vulnerability_id=vuln.get("id", "unknown"),
                severity=vuln.get("severity", "unknown"),
                description=vuln.get("description", ""),
                fix_version=fix_version,
                cve_id=vuln.get("aliases", [None])[0],
                exploitable=vuln.get("severity", "").lower() in ["high", "critical"],
            )
            vulnerabilities.append(vulnerability)

    return vulnerabilities


def _get_patch_allowlist() -> set[str]:
    """Get allowed packages for auto-patching."""
    allowlist_str = os.getenv(PATCH_ALLOWLIST_ENV, "")
    if not allowlist_str:
        return set()

    return set(pkg.strip() for pkg in allowlist_str.split(",") if pkg.strip())


def auto_patch_vulnerabilities(vulnerabilities: list[VulnerabilityReport]) -> list[str]:
    """
    Auto-patch vulnerabilities nếu ZETA_SELF_SECURITY_AUTO_PATCH=1.

    Returns:
        List of successfully patched packages
    """
    if os.getenv(ALLOW_AUTO_PATCH_ENV, "0") != "1":
        return []

    allowlist = _get_patch_allowlist()
    patched = []

    for vuln in vulnerabilities:
        # Only patch if package in allowlist (hoặc allowlist empty = patch all)
        if allowlist and vuln.package_name not in allowlist:
            continue

        if not vuln.fix_version:
            continue

        try:
            package_spec = f"{vuln.package_name}=={vuln.fix_version}"

            if _is_uv_available():
                cmd = ["uv", "pip", "install", package_spec]
            else:
                cmd = [sys.executable, "-m", "pip", "install", package_spec]

            code, output = _run_command(cmd, timeout=180)

            if code == 0:
                patched.append(package_spec)
            else:
                print(f"Failed to patch {vuln.package_name}: {output}")

        except Exception as e:
            print(f"Error patching {vuln.package_name}: {e}")

    return patched


def security_sweep(target_path: str = "zeta_vn") -> SecurityScanResult:
    """
    Perform comprehensive security sweep.

    Returns:
        SecurityScanResult with scan results and patching actions
    """
    timestamp = time.time()
    scan_errors = []

    # Run pip-audit
    try:
        pip_audit_scan()
    except Exception as e:
        {"error": str(e)}
        scan_errors.append(f"pip-audit failed: {e}")

    # Run Bandit
    try:
        bandit_scan(target_path)
    except Exception as e:
        {"error": str(e)}
        scan_errors.append(f"bandit failed: {e}")

    # Parse vulnerabilities
    vulnerabilities = _parse_vulnerabilities(pip_audit_result)

    # Count issues
    critical_issues = sum(1 for v in vulnerabilities if v.exploitable)
    total_issues = len(vulnerabilities)

    # Add Bandit issues to count
    if isinstance(bandit_result.get("result"), dict):
        bandit_issues = bandit_result["result"].get("results", [])
        total_issues += len(bandit_issues)
        critical_issues += sum(
            1
            for issue in bandit_issues
            if issue.get("issue_severity", "").lower() in ["high", "critical"]
        )

    # Auto-patch if enabled
    patched_packages = auto_patch_vulnerabilities(vulnerabilities)

    return SecurityScanResult(
        timestamp=timestamp,
        pip_audit_result=pip_audit_result,
        bandit_result=bandit_result,
        vulnerabilities=vulnerabilities,
        patched_packages=patched_packages,
        scan_errors=scan_errors,
        total_issues=total_issues,
        critical_issues=critical_issues,
    )


def get_security_status() -> dict[str, Any]:
    """Get current security monitoring status."""
    return {
        "auto_patch_enabled": os.getenv(ALLOW_AUTO_PATCH_ENV, "0") == "1",
        "patch_allowlist": list(_get_patch_allowlist()),
        "tools_available": {
            "pip_audit": _check_tool_available("pip-audit"),
            "bandit": _check_tool_available("bandit"),
            "uv": _is_uv_available(),
        },
        "env_vars": {
            "auto_patch_env": ALLOW_AUTO_PATCH_ENV,
            "allowlist_env": PATCH_ALLOWLIST_ENV,
            "auto_patch_value": os.getenv(ALLOW_AUTO_PATCH_ENV, "0"),
            "allowlist_value": os.getenv(PATCH_ALLOWLIST_ENV, ""),
        },
    }


def _check_tool_available(tool_name: str) -> bool:
    """Check if security tool is available."""
    if _is_uv_available():
        cmd = ["uv", "run", tool_name, "--version"]
    else:
        cmd = [sys.executable, "-m", tool_name.replace("-", "_"), "--version"]

    code, _ = _run_command(cmd, timeout=10)
    return code == 0


# Convenience functions
def quick_vulnerability_check() -> dict[str, Any]:
    """Quick vulnerability check without auto-patching."""
    _ = security_sweep()

    return {
        "vulnerabilities_found": len(result.vulnerabilities),
        "critical_vulnerabilities": result.critical_issues,
        "scan_successful": not result.scan_errors,
        "auto_patch_available": os.getenv(ALLOW_AUTO_PATCH_ENV, "0") == "1",
        "most_critical": [
            {
                "package": v.package_name,
                "severity": v.severity,
                "fix_available": bool(v.fix_version),
            }
            for v in result.vulnerabilities
            if v.exploitable
        ][:5],  # Top 5 critical
    }
