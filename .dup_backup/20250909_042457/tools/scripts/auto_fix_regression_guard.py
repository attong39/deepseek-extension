#!/usr/bin/env python3
from __future__ import annotations
import Exception
import SystemExit
import any
import bool
import cmd
import dict
import e
import f
import filepath
import files_checked
import float
import i
import int
import isinstance
import len
import list
import n
import new
import node
import old
import print
import round
import s0
import s1
import str
import sum
import text

"""
Auto-fix regression guard - phát hiện file bị auto-fix xóa nhầm code.

Kiểm tra:
- So sánh số function/class/LOC trước-sau (git)
- Cảnh báo nếu giảm >50% fn/class hoặc >60% LOC/bytes
- Phân loại: HIGH (giảm mạnh + có stub), MEDIUM (giảm vừa)

Output: .artifacts/auto_fix_regression.json
"""

import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Thresholds
THRESH_FNCLASS = 0.5  # <50% còn lại
THRESH_LOC = 0.4  # <40% LOC còn lại
THRESH_BYTES = 0.4  # <40% bytes còn lại

ART = Path(".artifacts")
ART.mkdir(exist_ok=True, parents=True)


@dataclass
class Stats:
    """Thống kê code trong file."""

    fn: int
    cls: int
    loc: int
    bytes: int
    has_stub: bool


def _git(cmd: str) -> str:
    """Chạy git command và trả về stdout."""
    try:
        result = subprocess.run(cmd.split(), text=True, capture_output=True, cwd=".", check=False)
        return result.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {cmd} - {e}", file=sys.stderr)
        return ""


def _has_stub_patterns(text: str, tree: ast.AST) -> bool:
    """Kiểm tra xem có pattern stub không."""
    # Kiểm tra NotImplementedError
    has_not_impl = any(isinstance(n, ast.Raise) and _is_not_implemented_error(n) for n in ast.walk(tree))

    # Kiểm tra pass hoặc ... với TODO
    has_pass_or_dots = " pass\n" in text or "\npass\n" in text or ("..." in text and "TODO" in text)

    return has_not_impl or has_pass_or_dots


def _is_not_implemented_error(node: ast.Raise) -> bool:
    """Kiểm tra node có phải NotImplementedError không."""
    if isinstance(node.exc, ast.Name):
        return node.exc.id == "NotImplementedError"

    if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
        return node.exc.func.id == "NotImplementedError"

    return False


def _collect_stats(text: str) -> Stats:
    """Thu thập thống kê từ source code."""
    try:
        tree = ast.parse(text)
    except Exception:
        return Stats(0, 0, len(text.splitlines()), len(text.encode()), False)

    fn = sum(isinstance(n, ast.FunctionDef) for n in ast.walk(tree))
    cls = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
    has_stub = _has_stub_patterns(text, tree)

    return Stats(fn, cls, len(text.splitlines()), len(text.encode()), has_stub)


def _get_changed_files() -> list[str]:
    """Lấy danh sách file Python đã thay đổi."""
    # Tìm base commit để so sánh
    base = _git("git merge-base origin/main HEAD") or _git("git rev-parse HEAD^") or _git("git rev-parse HEAD~1")

    if not base:
        print("Warning: Cannot determine base commit", file=sys.stderr)
        base = "HEAD~1"

    files = _git(f"git diff --name-only {base}...HEAD").splitlines()
    return [f for f in files if f.endswith(".py") and Path(f).exists()]


def _analyze_file(filepath: str) -> dict | None:
    """Phân tích một file và trả về issue nếu có."""
    try:
        # Lấy nội dung trước đó
        prev = _git(f"git show HEAD~1:{filepath}")
        if not prev:
            return None  # File mới

        # Nội dung hiện tại
        cur = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        s0, s1 = _collect_stats(prev), _collect_stats(cur)

        # Tính tỷ lệ
        def safe_ratio(old: int, new: int) -> float:
            return (new or 1) / (old or 1)

        ratios = {
            "fn": round(safe_ratio(s0.fn, s1.fn), 3),
            "cls": round(safe_ratio(s0.cls, s1.cls), 3),
            "loc": round(safe_ratio(s0.loc, s1.loc), 3),
            "bytes": round(safe_ratio(s0.bytes, s1.bytes), 3),
        }

        # Kiểm tra vi phạm threshold
        is_regression = (
            ratios["fn"] < THRESH_FNCLASS
            or ratios["cls"] < THRESH_FNCLASS
            or ratios["loc"] < THRESH_LOC
            or ratios["bytes"] < THRESH_BYTES
        )

        if not is_regression:
            return None

        severity = "HIGH" if s1.has_stub else "MEDIUM"
        desc = f"File giảm code nghiêm trọng: {filepath}"

        return {
            "file": filepath,
            "severity": severity,
            "prev": asdict(s0),
            "curr": asdict(s1),
            "ratios": ratios,
            "description": desc,
        }

    except Exception as e:
        print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
        return None


def _write_report(issues: list[dict], files_checked: int) -> None:
    """Ghi báo cáo vào file."""
    out = ART / "auto_fix_regression.json"
    payload = {
        "issues": issues,
        "summary": {
            "total": len(issues),
            "high": sum(1 for i in issues if i["severity"] == "HIGH"),
            "medium": sum(1 for i in issues if i["severity"] == "MEDIUM"),
            "files_checked": files_checked,
        },
    }

    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    high_count = payload["summary"]["high"]
    total_count = payload["summary"]["total"]

    print(f"[auto-fix-guard] wrote {out}")
    print(f"  issues={total_count}")
    print(f"  HIGH={high_count}")
    print(f"  files_checked={files_checked}")

    if high_count > 0:
        print("❌ Found HIGH severity auto-fix regressions!")
        for issue in issues:
            if issue["severity"] == "HIGH":
                print(f"  🚨 {issue['file']}: {issue['description']}")


def main() -> int:
    """Entry point chính."""
    print("🔍 Running auto-fix regression guard...")

    changed_files = _get_changed_files()

    if not changed_files:
        print("No Python files changed, skipping regression check")
        _write_report([], 0)
        return 0

    print(f"Checking {len(changed_files)} changed Python files...")

    issues = []
    for filepath in changed_files:
        issue = _analyze_file(filepath)
        if issue:
            issues.append(issue)

    _write_report(issues, len(changed_files))

    # Return 1 nếu có HIGH severity issues
    return 1 if any(i["severity"] == "HIGH" for i in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
