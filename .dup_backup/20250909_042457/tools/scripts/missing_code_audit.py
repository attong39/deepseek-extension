#!/usr/bin/env python3
"""
Quét repo phát hiện stub/thiếu code cho Python & TS/TSX.

Tìm kiếm các pattern:
- Python: pass/ellipsis/.../raise NotImplementedError, TODO/FIXME,
  hàm return None nhưng annotation non-Optional
- TS/TSX: // TODO|FIXME, throw new Error('Not implemented'), : any, as any

Xuất báo cáo JSON + exit code !=0 nếu có issue HIGH.
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
import all_issues
import any
import bool
import count
import dict
import e
import enumerate
import file_path
import i
import int
import isinstance
import issue
import kind
import len
import line
import list
import n
import node
import part
import print
import root
import root_path
import self
import sorted
import str
import sum
import x

# Severity levels
SEV = Literal["HIGH", "MEDIUM", "LOW"]

# Root directories to scan - adjust based on project structure
SCAN_ROOTS = [
    Path("zeta_vn"),  # Python backend
    Path("desktop_ai_zeta/src"),  # TypeScript frontend
]


@dataclass
class Issue:
    """Represents a code quality issue."""

    path: str
    line: int
    col: int
    severity: SEV
    kind: str
    message: str
    snippet: str | None = None


def scan_python_file(file_path: Path) -> list[Issue]:
    """Scan a Python file for missing code patterns."""
    issues: list[Issue] = []

    try:
        text = file_path.read_text(encoding="utf-8")
        tree = ast.parse(text)
    except Exception as e:
        issues.append(Issue(str(file_path), 1, 0, "HIGH", "syntax-error", f"Cannot parse Python file: {e}"))
        return issues

    class StubVisitor(ast.NodeVisitor):
        """AST visitor to find stub patterns."""

        def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            # Check for stub patterns
            contains_pass = any(isinstance(n, ast.Pass) for n in node.body)
            contains_ellipsis = any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Ellipsis) for n in node.body)
            raises_notimpl = any(isinstance(n, ast.Raise) and self._is_not_implemented_error(n) for n in ast.walk(node))

            if contains_pass or contains_ellipsis or raises_notimpl:
                issues.append(
                    Issue(
                        str(file_path),
                        node.lineno,
                        node.col_offset,
                        "HIGH",
                        "stub-function",
                        f"Function '{node.name}' contains stub (pass/…/NotImplementedError)",
                    )
                )

            # Check for return None mismatch with annotation
            if node.returns is not None:
                try:
                    ann = ast.unparse(node.returns)
                    returns_none = any(isinstance(n, ast.Constant) and n.value is None for n in ast.walk(node))
                    if returns_none and "Optional" not in ann and "None" not in ann and " | None" not in ann:
                        issues.append(
                            Issue(
                                str(file_path),
                                node.lineno,
                                node.col_offset,
                                "MEDIUM",
                                "none-return-mismatch",
                                f"Function '{node.name}' returns None but annotated as non-Optional: {ann}",
                            )
                        )
                except Exception:
                    pass

            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.visit_FunctionDef(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            # Check for empty classes
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                issues.append(
                    Issue(
                        str(file_path),
                        node.lineno,
                        node.col_offset,
                        "LOW",
                        "empty-class",
                        f"Class '{node.name}' is empty (only pass)",
                    )
                )
            self.generic_visit(node)

        def _is_not_implemented_error(self, node: ast.Raise) -> bool:
            """Check if raise statement is NotImplementedError."""
            if node.exc is None:
                return False

            # Direct NotImplementedError
            if isinstance(node.exc, ast.Name) and node.exc.id == "NotImplementedError":
                return True

            # NotImplementedError() call
            if (
                isinstance(node.exc, ast.Call)
                and isinstance(node.exc.func, ast.Name)
                and node.exc.func.id == "NotImplementedError"
            ):
                return True

            return False

    StubVisitor().visit(tree)

    # Scan for TODO/FIXME markers in comments
    for i, line in enumerate(text.splitlines(), start=1):
        if re.search(r"\b(TODO|FIXME|HACK)\b", line):
            issues.append(
                Issue(
                    str(file_path),
                    i,
                    0,
                    "MEDIUM",
                    "todo-marker",
                    "TODO/FIXME marker found",
                    snippet=line.strip(),
                )
            )

    return issues


def scan_typescript_file(file_path: Path) -> list[Issue]:
    """Scan a TypeScript/TSX file for missing code patterns."""
    issues: list[Issue] = []

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [Issue(str(file_path), 1, 0, "HIGH", "io-error", f"Cannot read TypeScript file: {e}")]

    for i, line in enumerate(text.splitlines(), start=1):
        line_stripped = line.strip()

        # TODO/FIXME markers
        if re.search(r"\b(TODO|FIXME|HACK)\b", line_stripped):
            issues.append(
                Issue(
                    str(file_path),
                    i,
                    0,
                    "MEDIUM",
                    "todo-marker",
                    "TODO/FIXME marker found",
                    snippet=line_stripped,
                )
            )

        # Not implemented error
        if re.search(r"throw\s+new\s+Error\(['\"]Not implemented['\"]\)", line_stripped):
            issues.append(
                Issue(
                    str(file_path),
                    i,
                    0,
                    "HIGH",
                    "ts-not-implemented",
                    "Throw 'Not implemented' error found",
                    snippet=line_stripped,
                )
            )

        # Any type usage (bad practice)
        if re.search(r":\s*any\b", line_stripped) or re.search(r"\bas\s+any\b", line_stripped):
            issues.append(
                Issue(
                    str(file_path),
                    i,
                    0,
                    "LOW",
                    "any-type",
                    "Using 'any' type - should be more specific",
                    snippet=line_stripped,
                )
            )

        # Empty function bodies
        if re.search(r"{\s*}\s*$", line_stripped) and "=>" in line_stripped:
            issues.append(
                Issue(
                    str(file_path),
                    i,
                    0,
                    "MEDIUM",
                    "empty-function",
                    "Empty function body",
                    snippet=line_stripped,
                )
            )

    return issues


def scan_directory(root_path: Path) -> list[Issue]:
    """Recursively scan a directory for issues."""
    all_issues: list[Issue] = []

    if not root_path.exists():
        return all_issues

    for file_path in root_path.rglob("*"):
        if not file_path.is_file():
            continue

        # Skip certain directories
        if any(
            part.startswith(".") or part in {"__pycache__", "node_modules", "dist", "build"} for part in file_path.parts
        ):
            continue

        if file_path.suffix == ".py":
            all_issues.extend(scan_python_file(file_path))
        elif file_path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
            all_issues.extend(scan_typescript_file(file_path))

    return all_issues


def generate_report(all_issues: list[Issue]) -> dict:
    """Generate summary report."""
    summary = {
        "total": len(all_issues),
        "high": sum(1 for i in all_issues if i.severity == "HIGH"),
        "medium": sum(1 for i in all_issues if i.severity == "MEDIUM"),
        "low": sum(1 for i in all_issues if i.severity == "LOW"),
    }

    # Group by kind for analysis
    by_kind = {}
    for issue in all_issues:
        if issue.kind not in by_kind:
            by_kind[issue.kind] = 0
        by_kind[issue.kind] += 1

    return {
        "summary": summary,
        "by_kind": by_kind,
        "issues": [asdict(issue) for issue in all_issues],
    }


def main() -> int:
    """Main entry point."""
    print("[missing_code_audit] Starting scan...")

    all_issues: list[Issue] = []

    # Scan all configured root directories
    for root in SCAN_ROOTS:
        print(f"[missing_code_audit] Scanning {root}...")
        issues = scan_directory(root)
        all_issues.extend(issues)
        print(f"[missing_code_audit] Found {len(issues)} issues in {root}")

    # Generate report
    report = generate_report(all_issues)

    # Ensure output directory exists
    output_dir = Path(".artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write report
    output_file = output_dir / "missing_code_report.json"
    output_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary
    summary = report["summary"]
    print(f"[missing_code_audit] Report written to {output_file}")
    print(f"[missing_code_audit] Total issues: {summary['total']}")
    print(f"[missing_code_audit] HIGH: {summary['high']}, " f"MEDIUM: {summary['medium']}, LOW: {summary['low']}")

    # Print top issue kinds
    if report["by_kind"]:
        print("[missing_code_audit] Top issue kinds:")
        for kind, count in sorted(report["by_kind"].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {kind}: {count}")

    # Exit with error code if HIGH severity issues found
    if summary["high"] > 0:
        print(f"[missing_code_audit] ❌ {summary['high']} HIGH severity issues found!")
        return 1

    print("[missing_code_audit] ✅ No HIGH severity issues found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
