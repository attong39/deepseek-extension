#!/usr/bin/env python3
from __future__ import annotations
import Exception
import ImportError
import SystemExit
import alias
import dict
import e
import filepath
import files_processed
import hasattr
import i
import int
import isinstance
import len
import list
import node
import pattern
import print
import root
import source_code
import str
import sum
import tuple

"""
Kiểm tra symbol được import nhưng không tồn tại thực tế.

Quét 'from X import Y' và xác thực Y có tồn tại trong X không.
Output: .artifacts/used_but_missing.json
"""

import ast
import importlib
import json
import sys
from pathlib import Path

ART = Path(".artifacts")
ART.mkdir(parents=True, exist_ok=True)

# Thư mục nguồn để quét
SOURCE_DIRS = [Path("zeta_vn"), Path("src")]


def _get_source_root() -> Path | None:
    """Tìm thư mục nguồn chính."""
    for root in SOURCE_DIRS:
        if root.exists() and root.is_dir():
            return root
    return None


def _iter_python_files(root: Path) -> list[Path]:
    """Lấy tất cả file Python trong source tree."""
    files = []

    for pattern in ["**/*.py"]:
        files.extend(root.rglob(pattern))

    # Lọc bỏ test files và __pycache__
    filtered = []
    for filepath in files:
        path_str = str(filepath)
        if (
            "/tests/" not in path_str
            and "\\tests\\" not in path_str
            and "__pycache__" not in path_str
            and ".pytest_cache" not in path_str
        ):
            filtered.append(filepath)

    return filtered


def _extract_imports(source_code: str) -> list[tuple[str, str]]:
    """
    Trích xuất imports dạng 'from X import Y'.

    Returns:
        List of (module_name, symbol_name) tuples
    """
    imports = []

    try:
        tree = ast.parse(source_code)
    except Exception:
        return imports

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.names:
            module_name = node.module

            for alias in node.names:
                if alias.name != "*":  # Skip wildcard imports
                    symbol_name = alias.asname or alias.name
                    imports.append((module_name, symbol_name))

    return imports


def _verify_import(module_name: str, symbol_name: str) -> dict | None:
    """
    Xác thực một import có hợp lệ không.

    Returns:
        Dict với thông tin lỗi nếu có, None nếu OK
    """
    try:
        module = importlib.import_module(module_name)

        if not hasattr(module, symbol_name):
            return {
                "module": module_name,
                "symbol": symbol_name,
                "severity": "HIGH",
                "issue": "symbol-not-found",
                "message": f"Symbol '{symbol_name}' not found in module '{module_name}'",
            }

    except ImportError as e:
        return {
            "module": module_name,
            "symbol": symbol_name,
            "severity": "HIGH",
            "issue": "import-error",
            "message": f"Cannot import module '{module_name}': {e}",
        }
    except Exception as e:
        return {
            "module": module_name,
            "symbol": symbol_name,
            "severity": "MEDIUM",
            "issue": "verification-error",
            "message": f"Error verifying import: {e}",
        }

    return None


def _process_file(filepath: Path) -> list[dict]:
    """Xử lý một file và trả về danh sách lỗi import."""
    issues = []

    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        imports = _extract_imports(content)

        for module_name, symbol_name in imports:
            issue = _verify_import(module_name, symbol_name)
            if issue:
                issue["file"] = str(filepath)
                issues.append(issue)

    except Exception as e:
        # Log error nhưng không crash
        print(f"Error processing {filepath}: {e}", file=sys.stderr)

    return issues


def _write_report(all_issues: list[dict], files_processed: int) -> int:
    """Ghi báo cáo và return exit code."""
    summary = {
        "total": len(all_issues),
        "high": sum(1 for i in all_issues if i.get("severity") == "HIGH"),
        "medium": sum(1 for i in all_issues if i.get("severity") == "MEDIUM"),
        "files_processed": files_processed,
    }

    payload = {"issues": all_issues, "summary": summary}

    out_path = ART / "used_but_missing.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"[used-but-missing] wrote {out_path}")
    print(f"  total={summary['total']}")
    print(f"  HIGH={summary['high']}")
    print(f"  files_processed={files_processed}")

    if summary["high"] > 0:
        print("❌ Found HIGH severity import issues!")
        for issue in all_issues:
            if issue.get("severity") == "HIGH":
                print(f"  🚨 {issue['file']}: {issue['message']}")

    return 1 if summary["high"] > 0 else 0


def main() -> int:
    """Entry point chính."""
    print("🔍 Checking used-but-missing imports...")

    source_root = _get_source_root()
    if not source_root:
        print("Error: Cannot find source directory (zeta_vn/ or src/)")
        return 1

    python_files = _iter_python_files(source_root)
    if not python_files:
        print("No Python files found to check")
        return 0

    print(f"Processing {len(python_files)} Python files...")

    all_issues = []
    for filepath in python_files:
        issues = _process_file(filepath)
        all_issues.extend(issues)

    return _write_report(all_issues, len(python_files))


if __name__ == "__main__":
    raise SystemExit(main())
