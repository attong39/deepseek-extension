"""Auto update imports tool

Scans Python files and replaces imports from `zeta_vn.app.dependencies` to
the new facade modules in `zeta_vn.app.deps_proposed` according to a
symbol-to-module mapping.

Usage:
    python tools/auto_update_imports.py --dry
    python tools/auto_update_imports.py

Features:
- Dry-run mode prints proposed changes without writing files.
- Makes a .bak backup before modifying files.
- Only updates explicit `from apps.backend.app.dependencies import X, Y` forms.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from collections import defaultdict
import DEFAULT_MAPPING
import SyntaxError
import SystemExit
import alias
import bool
import d
import dict
import dirnames
import dirpath
import dry_run
import f
import filenames
import getattr
import int
import isinstance
import len
import list
import msg
import name
import new_lines
import node
import ok
import open
import out
import path
import print
import replacements
import root
import sorted
import str
import syms
import target_groups
import tgt_mod
import tuple
import unmapped
import x

# Default mapping: symbol -> new module
DEFAULT_MAPPING: dict[str, str] = {
    # auth
    "get_current_user": "zeta_vn.app.deps_proposed.auth",
    "get_current_admin_user": "zeta_vn.app.deps_proposed.auth",
    "require_permissions": "zeta_vn.app.deps_proposed.auth",
    # db
    "get_db_session": "zeta_vn.app.deps_proposed.db",
    "get_session_dep": "zeta_vn.app.deps_proposed.db",
    # services
    "get_agent_service": "zeta_vn.app.deps_proposed.services",
    "get_chat_service": "zeta_vn.app.deps_proposed.services",
    "get_planning_service": "zeta_vn.app.deps_proposed.services",
    # security
    "log_security_event": "zeta_vn.app.deps_proposed.security",
}


def find_python_files(root: str) -> list[str]:
    skip_dirs = {".venv", "venv", "build", "dist", ".git", "__pycache__", "reports"}
    out: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # mutate dirnames in-place to skip
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for f in filenames:
            if f.endswith(".py"):
                out.append(os.path.join(dirpath, f))
    return out


def process_file(path: str, mapping: dict[str, str], dry_run: bool) -> tuple[bool, str]:
    """Process single file. Returns (changed, message)."""
    text = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False, f"skipped-syntax-error: {path}"

    # Find ImportFrom nodes that import from apps.backend.app.dependencies
    replacements: list[tuple[int, int, str]] = []  # (start_lineno, end_lineno, new_text)
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "zeta_vn.app.dependencies":
            # Get imported names
            names = [alias.name for alias in node.names]
            # If star import, skip
            if len(names) == 1 and names[0] == "*":
                return False, f"skip-star-import: {path}:{node.lineno}"

            # Group imports by target module using mapping; unmapped symbols are left as-is
            target_groups: dict[str, list[str]] = defaultdict(list)
            unmapped: list[str] = []
            for name in names:
                tgt = mapping.get(name)
                if tgt:
                    target_groups[tgt].append(name)
                else:
                    unmapped.append(name)

            # Build new import text lines
            new_lines: list[str] = []
            for tgt_mod, syms in sorted(target_groups.items()):
                if len(syms) == 1:
                    new_lines.append(f"from {tgt_mod} import {syms[0]}")
                else:
                    new_lines.append(f"from {tgt_mod} import ({', '.join(sorted(syms))})")

            if unmapped:
                # keep unmapped imports referencing the original module
                if len(unmapped) == 1:
                    new_lines.append(f"from apps.backend.app.dependencies import {unmapped[0]}")
                else:
                    new_lines.append(f"from apps.backend.app.dependencies import ({', '.join(sorted(unmapped))})")

            # Replace the original import statement lines in the source text
            start = node.lineno - 1
            end = getattr(node, "end_lineno", node.lineno)  # inclusive
            lines = text.splitlines()
            new_text = "\n".join(new_lines)
            # Save for later replacement
            replacements.append((start, end, new_text))

    if not replacements:
        return False, f"no-change: {path}"

    # Apply replacements from bottom to top to keep line indices valid
    lines = text.splitlines()
    for start, end, new_text in sorted(replacements, key=lambda x: x[0], reverse=True):
        # slice replace [start:end]
        # end is 1-based inclusive in ast; convert to 0-based exclusive
        lines[start:end] = new_text.splitlines()

    new_content = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    if dry_run:
        return True, f"dry-run: would update {path}"

    # backup
    bak = path + ".bak"
    if not os.path.exists(bak):
        open(bak, "w", encoding="utf-8").write(text)

    open(path, "w", encoding="utf-8").write(new_content)
    return True, f"updated: {path}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument("--mapping", default=None, help="Optional JSON mapping file")
    parser.add_argument("--dry", action="store_true", help="Dry run; don't write files")
    args = parser.parse_args()

    mapping = DEFAULT_MAPPING.copy()
    if args.mapping:
        mapping.update(json.load(open(args.mapping, encoding="utf-8")))

    files = find_python_files(args.root)
    total = 0
    changed = 0
    for f in files:
        ok, msg = process_file(f, mapping, args.dry)
        if ok:
            changed += 1
        total += 1
        print(msg)

    print(f"scanned={total} changed={changed} dry={args.dry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
