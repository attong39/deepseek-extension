#!/usr/bin/env python3
"""
Diff-gate: Chỉ bắt lỗi mới trong PR (so với baseline) trên dòng code thay đổi.

Kiểm tra policy và routing theo CODEOWNERS.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any
import Exception
import SystemExit
import any
import bool
import cmd
import dict
import e
import f
import file_path
import file_ranges
import i
import int
import issue
import issues_by_owner
import item
import kind
import len
import line_num
import list
import owner
import owner_issues
import path
import path_variant
import pattern_owners
import print
import r
import range
import set
import sorted
import str
import sum
import tuple
import variant

# Paths
ARTIFACTS_DIR = Path(".artifacts")
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = ARTIFACTS_DIR / "missing_code_report.json"
DELTA_FILE = ARTIFACTS_DIR / "missing_code_delta.json"
BASELINE_FILE = Path("contracts/missing_code_baseline.json")
POLICY_FILE = Path("configs/missing_code_policy.yml")
CODEOWNERS_FILE = Path(".github/CODEOWNERS")


def run_shell(cmd: str) -> str:
    """Run shell command and return stdout."""
    try:
        result = subprocess.run(cmd, shell=False, text=True, capture_output=True, check=False)
        return result.stdout.strip()
    except Exception:
        return ""


@dataclass
class Issue:
    """Represents a code issue."""

    path: str
    line: int
    severity: str
    kind: str
    message: str = ""


def load_current_report() -> list[Issue]:
    """Load issues from current audit report."""
    if not REPORT_FILE.exists():
        print("[diff-gate] ❌ Missing report; run missing_code_audit.py first")
        sys.exit(2)

    data = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
    issues = []

    for item in data.get("issues", []):
        issues.append(
            Issue(
                path=item["path"],
                line=int(item["line"]),
                severity=item["severity"],
                kind=item["kind"],
                message=item.get("message", ""),
            )
        )

    return issues


def load_baseline() -> set[tuple[str, int, str]]:
    """Load baseline issues for comparison."""
    if not BASELINE_FILE.exists():
        print("[diff-gate] ⚠️ No baseline found - all issues will be considered new")
        return set()

    baseline_data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    baseline_issues = set()

    for item in baseline_data.get("issues", []):
        baseline_issues.add((item["path"], int(item["line"]), item["kind"]))

    return baseline_issues


def load_policy() -> dict[str, Any]:
    """Load policy configuration."""
    default_policy = {
        "fail_on_new_high": True,
        "min_reduction_high": 0,
        "owner_report": True,
        "thresholds": {"max_new_high_per_pr": 0, "warn_medium_threshold": 10},
    }

    if not POLICY_FILE.exists():
        return default_policy

    try:
        import yaml

        policy_data = yaml.safe_load(POLICY_FILE.read_text(encoding="utf-8"))
        return {**default_policy, **(policy_data or {})}
    except Exception as e:
        print(f"[diff-gate] ⚠️ Error loading policy: {e}, using defaults")
        return default_policy


def get_changed_file_ranges() -> dict[str, list[range]]:
    """Get ranges of changed lines per file in current PR/branch."""
    # Try to get base reference from GitHub environment
    base_ref = os.environ.get("GITHUB_BASE_REF", "main")

    # Find merge base
    merge_base = run_shell(f"git merge-base origin/{base_ref} HEAD")
    if not merge_base:
        # Fallback to comparing with HEAD~1
        merge_base = run_shell("git rev-parse HEAD~1")

    if not merge_base:
        # Last resort: get all staged/modified files
        files = run_shell("git diff --name-only HEAD~1").splitlines()
        return {f: [range(1, 999999)] for f in files if f}

    # Get unified diff
    diff_output = run_shell(f"git diff --unified=0 {merge_base}...HEAD")

    file_ranges: dict[str, list[range]] = {}
    current_file = None

    for line in diff_output.splitlines():
        # New file marker
        if line.startswith("+++ b/"):
            current_file = line[6:]  # Remove "+++ b/" prefix
            continue

        # Hunk header: @@ -old_start,old_count +new_start,new_count @@
        hunk_match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if current_file and hunk_match:
            start = int(hunk_match.group(1))
            count = int(hunk_match.group(2) or "1")

            if current_file not in file_ranges:
                file_ranges[current_file] = []

            file_ranges[current_file].append(range(start, start + count))

    return file_ranges


def is_line_changed(file_path: str, line_num: int, changed_ranges: dict[str, list[range]]) -> bool:
    """Check if a specific line is in the changed ranges."""
    # Try different path formats
    for path_variant in [file_path, f"./{file_path}", file_path.lstrip("./")]:
        if path_variant in changed_ranges:
            return any(line_num in r for r in changed_ranges[path_variant])

    return False


def parse_codeowners() -> list[tuple[str, list[str]]]:
    """Parse CODEOWNERS file and return pattern -> owners mapping."""
    if not CODEOWNERS_FILE.exists():
        return []

    codeowners_rules = []

    try:
        content = CODEOWNERS_FILE.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) >= 2:
                pattern = parts[0]
                owners = parts[1:]
                codeowners_rules.append((pattern, owners))

    except Exception as e:
        print(f"[diff-gate] ⚠️ Error parsing CODEOWNERS: {e}")

    return codeowners_rules


def find_owners_for_file(file_path: str, codeowners_rules: list[tuple[str, list[str]]]) -> list[str]:
    """Find owners for a specific file based on CODEOWNERS patterns."""
    owners = []

    # Check patterns (later patterns override earlier ones)
    for pattern, pattern_owners in codeowners_rules:
        path_variants = [file_path, f"./{file_path}", file_path.lstrip("./")]

        for variant in path_variants:
            if fnmatch(variant, pattern):
                owners = pattern_owners
                break

    return owners or ["@unowned"]


def main() -> int:
    """Main diff-gate logic."""
    print("[diff-gate] 🔍 Starting PR-specific audit...")

    # Load data
    policy = load_policy()
    current_issues = load_current_report()
    baseline_issues = load_baseline()
    changed_ranges = get_changed_file_ranges()
    codeowners_rules = parse_codeowners()

    print(f"[diff-gate] 📊 Loaded {len(current_issues)} current issues")
    print(f"[diff-gate] 📊 Baseline has {len(baseline_issues)} issues")
    print(f"[diff-gate] 📊 Found {len(changed_ranges)} changed files")

    # Filter for new issues in changed lines only
    new_issues = []
    for issue in current_issues:
        # Check if issue is new (not in baseline)
        issue_key = (issue.path, issue.line, issue.kind)
        if issue_key in baseline_issues:
            continue

        # Check if issue is in changed lines
        if not is_line_changed(issue.path, issue.line, changed_ranges):
            continue

        new_issues.append(issue)

    # Group by owner
    issues_by_owner: dict[str, list[dict[str, Any]]] = {}

    for issue in new_issues:
        owners = find_owners_for_file(issue.path, codeowners_rules)

        issue_dict = {
            "path": issue.path,
            "line": issue.line,
            "severity": issue.severity,
            "kind": issue.kind,
            "message": issue.message[:100] + "..." if len(issue.message) > 100 else issue.message,
        }

        for owner in owners:
            if owner not in issues_by_owner:
                issues_by_owner[owner] = []
            issues_by_owner[owner].append(issue_dict)

    # Calculate summary
    new_high_count = sum(1 for issue in new_issues if issue.severity == "HIGH")
    new_medium_count = sum(1 for issue in new_issues if issue.severity == "MEDIUM")
    new_low_count = sum(1 for issue in new_issues if issue.severity == "LOW")

    baseline_high_count = sum(
        1
        for path, line, kind in baseline_issues
        if any(i.path == path and i.line == line and i.kind == kind and i.severity == "HIGH" for i in current_issues)
    )

    # Create report
    delta_report = {
        "policy": policy,
        "summary": {
            "new_total": len(new_issues),
            "new_high": new_high_count,
            "new_medium": new_medium_count,
            "new_low": new_low_count,
            "baseline_high_count": baseline_high_count,
            "changed_files": len(changed_ranges),
        },
        "new_issues": [
            {
                "path": issue.path,
                "line": issue.line,
                "severity": issue.severity,
                "kind": issue.kind,
                "message": issue.message,
            }
            for issue in new_issues
        ],
        "by_owner": issues_by_owner,
    }

    # Write delta report
    DELTA_FILE.write_text(json.dumps(delta_report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary
    print(f"[diff-gate] 📝 Report written: {DELTA_FILE}")
    print(f"[diff-gate] 📊 New issues: {len(new_issues)} (HIGH: {new_high_count})")

    if issues_by_owner:
        print("[diff-gate] 👥 Issues by owner:")
        for owner, owner_issues in sorted(issues_by_owner.items()):
            high_count = sum(1 for i in owner_issues if i["severity"] == "HIGH")
            print(f"  {owner}: {len(owner_issues)} issues (HIGH: {high_count})")

    # Apply policy
    exit_code = 0

    # Check for new HIGH issues
    if policy.get("fail_on_new_high", True) and new_high_count > 0:
        max_allowed = policy.get("thresholds", {}).get("max_new_high_per_pr", 0)
        if new_high_count > max_allowed:
            print(f"[diff-gate] ❌ Policy violation: {new_high_count} new HIGH issues > {max_allowed} allowed")
            exit_code = 1

    # Check MEDIUM threshold
    medium_threshold = policy.get("thresholds", {}).get("warn_medium_threshold", 10)
    if new_medium_count > medium_threshold:
        print(f"[diff-gate] ⚠️ Warning: {new_medium_count} new MEDIUM issues > {medium_threshold} threshold")

    # Check weekly reduction target (only on main branch)
    is_main_branch = os.environ.get("GITHUB_REF_NAME", "") in {"main", "master"}
    reduction_target = policy.get("min_reduction_high", 0)

    if reduction_target > 0 and is_main_branch:
        print(f"[diff-gate] 📈 Weekly reduction target: {reduction_target} HIGH issues")
        print("[diff-gate] 💡 Note: Implement trend tracking to enforce this")

    if exit_code == 0:
        print("[diff-gate] ✅ All policy checks passed")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
