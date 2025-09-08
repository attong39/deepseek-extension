#!/usr/bin/env python3
"""
Per-file Completeness Score System

Chấm điểm từng file theo tiêu chí:
- Functions/classes count
- Documentation coverage
- Stub detection (TODO, NotImplementedError, pass)
- Type hints coverage
- Export count (for TS)

Score 0-100, severity: OK (80+), WARN (60-79), HIGH (<60)
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal
import Exception
import SystemExit
import any
import bool
import e
import float
import getattr
import int
import isinstance
import len
import list
import max
import min
import n
import path
import pattern
import print
import r
import root
import severity
import sorted
import str
import sum
import x

ART = Path(".artifacts")
ART.mkdir(parents=True, exist_ok=True)

PY_ROOTS = [Path("zeta_vn"), Path("src")]
TS_ROOTS = [Path("desktop_ai_zeta/src"), Path("desktop/src")]

Severity = Literal["OK", "WARN", "HIGH"]


@dataclass
class CompletenessRow:
    """Kết quả đánh giá completeness của một file."""

    path: str
    lang: str
    score: float
    severity: Severity
    funcs: int
    classes: int
    exports: int
    loc: int
    has_stub: bool
    any_count: int
    todos: int
    has_docstring: bool


def score_python_file(text: str) -> CompletenessRow:
    """Chấm điểm file Python."""
    try:
        tree = ast.parse(text)
    except Exception:
        return CompletenessRow("", "py", 0.0, "HIGH", 0, 0, 0, len(text.splitlines()), False, 0, 0, False)

    # Count elements
    funcs = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    classes = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))

    # Detect stubs
    has_stub = (
        any(
            isinstance(n, ast.Raise) and getattr(getattr(n, "exc", None), "id", "") == "NotImplementedError"
            for n in ast.walk(tree)
        )
        or " pass" in text
        or "..." in text
    )

    # LOC
    loc = len(text.splitlines())

    # Documentation check
    has_docstring = '"""' in text or "'''" in text

    # TODO count
    todos = len(re.findall(r"\b(TODO|FIXME|HACK|XXX)\b", text, re.IGNORECASE))

    # Type hints (rough estimate)
    type_hints = len(re.findall(r":\s*[A-Za-z_][\w\[\], ]*(?:\s*=|$)", text))

    # Calculate score
    points = 10  # Base score
    points += min(funcs, 10) * 5  # Functions: up to 50pts
    points += min(classes, 10) * 4  # Classes: up to 40pts
    points += 10 if has_docstring else 0  # Documentation: 10pts
    points += min(type_hints, 5) * 2  # Type hints: up to 10pts
    points -= 20 if has_stub else 0  # Stub penalty: -20pts
    points -= min(todos, 10) * 2  # TODO penalty: up to -20pts

    # Empty file penalty
    if loc < 5:
        points -= 30

    score = max(0.0, min(100.0, points))
    severity: Severity = "OK" if score >= 80 else ("WARN" if score >= 60 else "HIGH")

    return CompletenessRow("", "py", score, severity, funcs, classes, 0, loc, has_stub, 0, todos, has_docstring)


def score_typescript_file(text: str) -> CompletenessRow:
    """Chấm điểm file TypeScript/JavaScript."""
    loc = len(text.splitlines())

    # Count exports
    exports = len(re.findall(r"\bexport\s+(?:default|const|function|class|type|interface)\b", text))

    # Count any types (penalty)
    any_count = len(re.findall(r":\s*any\b|\bas\s+any\b", text))

    # Detect stubs
    has_stub = "throw new Error('Not implemented')" in text or 'throw new Error("Not implemented")' in text

    # TODO count
    todos = len(re.findall(r"\b(TODO|FIXME|HACK|XXX)\b", text, re.IGNORECASE))

    # Functions and classes
    funcs = len(re.findall(r"function\s+[A-Za-z_]", text))
    classes = len(re.findall(r"\bclass\s+[A-Za-z_]", text))

    # Documentation (JSDoc)
    has_docstring = "/**" in text and "*/" in text

    # Calculate score
    points = 10  # Base score
    points += min(exports, 10) * 5  # Exports: up to 50pts
    points += min(funcs, 10) * 3  # Functions: up to 30pts
    points += min(classes, 10) * 3  # Classes: up to 30pts
    points += 10 if has_docstring else 0  # Documentation: 10pts
    points -= min(any_count, 10) * 3  # Any penalty: up to -30pts
    points -= 20 if has_stub else 0  # Stub penalty: -20pts
    points -= min(todos, 10) * 2  # TODO penalty: up to -20pts

    # Empty file penalty
    if loc < 5:
        points -= 30

    score = max(0.0, min(100.0, points))
    severity: Severity = "OK" if score >= 80 else ("WARN" if score >= 60 else "HIGH")

    return CompletenessRow(
        "",
        "ts",
        score,
        severity,
        funcs,
        classes,
        exports,
        loc,
        has_stub,
        any_count,
        todos,
        has_docstring,
    )


def scan_files() -> list[CompletenessRow]:
    """Scan tất cả files trong workspace."""
    rows: list[CompletenessRow] = []

    # Python files
    for root in PY_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                row = score_python_file(text)
                row.path = str(path)
                rows.append(row)
            except Exception as e:
                print(f"⚠️  Error processing {path}: {e}")

    # TypeScript files
    for root in TS_ROOTS:
        if not root.exists():
            continue
        for pattern in ["*.ts", "*.tsx", "*.js", "*.jsx"]:
            for path in root.rglob(pattern):
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    row = score_typescript_file(text)
                    row.path = str(path)
                    rows.append(row)
                except Exception as e:
                    print(f"⚠️  Error processing {path}: {e}")

    return rows


def main() -> int:
    """Generate completeness report."""
    rows = scan_files()

    if not rows:
        print("❌ No files found to analyze")
        return 1

    # Summary statistics
    summary = {
        "threshold": 70.0,
        "total": len(rows),
        "high": sum(1 for r in rows if r.severity == "HIGH"),
        "warn": sum(1 for r in rows if r.severity == "WARN"),
        "ok": sum(1 for r in rows if r.severity == "OK"),
        "avg_score": sum(r.score for r in rows) / len(rows),
    }

    # Generate JSON report
    payload = {"summary": summary, "rows": [asdict(r) for r in rows]}

    json_path = ART / "completeness_report.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # Generate Markdown report (top offenders)
    top_missing = sorted(rows, key=lambda x: x.score)[:50]

    lines = [
        "# Completeness Report - Top Missing Files",
        "",
        f"**Summary:** {summary['total']} files analyzed",
        f"- 🔴 HIGH: {summary['high']} files (score < 60)",
        f"- 🟡 WARN: {summary['warn']} files (score 60-79)",
        f"- 🟢 OK: {summary['ok']} files (score 80+)",
        f"- 📊 Average: {summary['avg_score']:.1f}",
        "",
        "## Top Files Needing Attention",
        "",
    ]

    for row in top_missing:
        icon = "🔴" if row.severity == "HIGH" else ("🟡" if row.severity == "WARN" else "🟢")
        lines.append(
            f"- {icon} **{row.score:.1f}** — `{row.path}` "
            f"(fn:{row.funcs}, cls:{row.classes}, exp:{row.exports}, "
            f"any:{row.any_count}, todos:{row.todos})"
        )

    md_path = ART / "completeness_report.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    # Console output
    print("📊 Completeness Analysis Complete")
    print(f"   Files analyzed: {summary['total']}")
    print(f"   Average score: {summary['avg_score']:.1f}")
    print(f"   🔴 HIGH issues: {summary['high']}")
    print(f"   🟡 WARN issues: {summary['warn']}")
    print(f"   🟢 OK files: {summary['ok']}")
    print(f"📄 Reports: {json_path}, {md_path}")

    # Exit code: fail if too many HIGH issues
    return 1 if summary["high"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
