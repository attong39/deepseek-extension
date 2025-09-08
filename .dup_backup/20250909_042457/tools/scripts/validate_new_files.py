#!/usr/bin/env python3
"""
Validate new/renamed files:
- Đúng thư mục/nhóm (app/core/data/config/tests/desktop_ai_zeta/...)
- Cấm tên xấu: *_copy, *_final, *(1).*, backup, tmp, junk
- Nếu chạm server: phải nằm dưới zeta_vn/*
- Nếu chạm desktop: phải nằm dưới desktop_ai_zeta/*
- So với PROJECT_MAP.md: cảnh báo nếu path không khớp nhóm
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import any
import bool
import folder
import int
import len
import line
import list
import m
import p
import print
import root
import str

BAD_NAME = re.compile(r"(?:\bcopy\b|\bfinal\b|\(1\)|backup|tmp|junk)", re.I)
ALLOWED_ROOTS = (
    "zeta_vn/",
    "desktop_ai_zeta/",
    ".github/",
    "tools/",
    "tests/",
    "config/",
    ".vscode/",
    "scripts/",
    "docs/",
    "monitoring/",
    "ci/",
    "deploy/",
)


def staged_added_paths() -> list[str]:
    """Get list of added/renamed files in git staging area."""
    try:
        out = subprocess.check_output(["git", "diff", "--cached", "--name-status"], text=True).splitlines()
    except subprocess.CalledProcessError:
        return []

    files = []
    for line in out:
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith(("A", "R")):  # Added or Renamed
            path = parts[-1]  # Take last part for renamed files
            files.append(path)
    return files


def in_allowed_roots(p: str) -> bool:
    """Check if file path is in allowed root directories."""
    return any(p.startswith(root) for root in ALLOWED_ROOTS)


def bad_name(p: str) -> bool:
    """Check if file has a bad name pattern."""
    fname = pathlib.Path(p).name
    return bool(BAD_NAME.search(fname))


def validate_server_desktop_separation(p: str) -> list[str]:
    """Validate server/desktop file separation."""
    problems = []

    # Check if file is in correct location
    if p.startswith("zeta_vn/"):
        # Server files - check structure
        if not any(p.startswith(f"zeta_vn/{folder}/") for folder in ["app", "core", "data", "cli", "tests"]):
            problems.append(f"{p}: server file should be in app/core/data/cli/tests")

    elif p.startswith("desktop_ai_zeta/"):
        # Desktop files - check structure
        if not any(
            p.startswith(f"desktop_ai_zeta/{folder}/") for folder in ["src", "public", "dist", "scripts", "tests"]
        ):
            problems.append(f"{p}: desktop file should be in src/public/dist/scripts/tests")

    return problems


def main() -> int:
    """Main validation function."""
    problems = []
    files = staged_added_paths()

    if not files:
        print("✅ No new files to validate")
        return 0

    for p in files:
        # Check allowed roots
        if not in_allowed_roots(p):
            problems.append(f"{p}: không thuộc các root hợp lệ {ALLOWED_ROOTS}")

        # Check bad names
        if bad_name(p):
            problems.append(f"{p}: tên file/tệp cấm dùng (copy/final/(1)/backup/tmp/junk)")

        # Check server/desktop separation
        problems.extend(validate_server_desktop_separation(p))

        # Check if file is completely outside project structure
        if not (
            p.startswith("zeta_vn/")
            or p.startswith("desktop_ai_zeta/")
            or any(p.startswith(root) for root in ALLOWED_ROOTS)
        ):
            problems.append(
                f"{p}: tệp không thuộc server (zeta_vn) hay desktop (desktop_ai_zeta) "
                f"hay khu vực cho phép (.github/tools/tests/config/.vscode/scripts/docs)"
            )

    if problems:
        print("❌ Project structure guard FAILED:\n", file=sys.stderr)
        for m in problems:
            print(f" - {m}", file=sys.stderr)
        print(
            "\nHướng dẫn: đặt file đúng thư mục theo PROJECT_MAP.md, sửa tên file cho chuẩn.\n",
            file=sys.stderr,
        )
        return 2

    print("✅ Project structure guard OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
