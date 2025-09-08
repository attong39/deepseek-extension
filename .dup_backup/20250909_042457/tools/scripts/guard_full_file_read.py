#!/usr/bin/env python3
"""
Guard: phải "đọc toàn bộ file" (chống duplicate symbol).

Kiểm tra Python và TypeScript files để phát hiện duplicate symbols,
dấu hiệu cho thấy developer chưa đọc toàn bộ file trước khi thêm code.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import re
import subprocess
import sys
from collections.abc import Iterable
import OSError
import SyntaxError
import UnicodeDecodeError
import f
import file_path
import group
import int
import isinstance
import item
import line
import list
import match
import node
import print
import problem
import seq
import set
import sorted
import str
import tuple

# TypeScript/JavaScript symbol regex
TS_RX = re.compile(
    r"^(?:export\s+)?(?:class|function|interface|type|const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\b"
    r"|^(?:export\s+)?const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*",
    re.MULTILINE,
)


def scan_python_symbols(text: str) -> tuple[set[str], set[str]]:
    """Scan Python file for function and class names."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set(), set()

    functions = set()
    classes = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Only top-level and class methods, not nested functions
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.add(node.name)

    return functions, classes


def scan_ts_symbols(text: str) -> set[str]:
    """Scan TypeScript/JavaScript file for exported symbols."""
    names = set()
    for match in TS_RX.finditer(text):
        for group in match.groups():
            if group and not group.startswith("_"):
                names.add(group)
    return names


def find_duplicates(seq: Iterable[str]) -> set[str]:
    """Find duplicate items in a sequence."""
    seen = set()
    duplicates = set()
    for item in seq:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates


def check_file(path: pathlib.Path) -> list[str]:
    """Check a single file for duplicate symbols."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return []

    problems = []

    if path.suffix == ".py":
        functions, classes = scan_python_symbols(text)
        dup_functions = find_duplicates(functions)
        dup_classes = find_duplicates(classes)

        if dup_functions:
            problems.append(f"{path}: duplicate functions: {sorted(dup_functions)}")
        if dup_classes:
            problems.append(f"{path}: duplicate classes: {sorted(dup_classes)}")

    elif path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
        symbols = scan_ts_symbols(text)
        duplicates = find_duplicates(symbols)

        if duplicates:
            problems.append(f"{path}: duplicate TS/JS exports/symbols: {sorted(duplicates)}")

    return problems


def get_staged_files() -> list[pathlib.Path]:
    """Get list of staged files that should be checked."""
    try:
        output = subprocess.check_output(["git", "diff", "--name-only", "--cached"], text=True).splitlines()
    except subprocess.CalledProcessError:
        return []

    files = []
    for line in output:
        if line.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
            path = pathlib.Path(line)
            if path.exists():
                files.append(path)

    return files


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(description="Check for duplicate symbols (indicates incomplete file reading)")
    parser.add_argument("files", nargs="*", help="Files to check (default: staged files)")
    args = parser.parse_args()

    if args.files:
        files = [pathlib.Path(f) for f in args.files]
    else:
        files = get_staged_files()

    if not files:
        print("✅ No files to check")
        return 0

    all_problems = []
    for file_path in files:
        if file_path.exists() and file_path.suffix in {
            ".py",
            ".ts",
            ".tsx",
            ".js",
            ".jsx",
        }:
            problems = check_file(file_path)
            all_problems.extend(problems)

    if all_problems:
        print(
            "❌ Full-File Read Guard FAILED (nghi ngờ chưa đọc hết file — trùng symbol):\n",
            file=sys.stderr,
        )
        for problem in all_problems:
            print(f" - {problem}", file=sys.stderr)
        print(
            "\nHướng dẫn: đọc toàn bộ file, hợp nhất/kế thừa thay vì tạo trùng tên; " "cập nhật tests/i18n liên quan.",
            file=sys.stderr,
        )
        return 2

    print("✅ Full-File Read Guard OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
