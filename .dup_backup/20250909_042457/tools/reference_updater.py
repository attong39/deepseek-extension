#!/usr/bin/env python3
"""
Reference Updater (dry-run by default)
- Scans config files for hard-coded monorepo path references and prints or applies fixes:
  - zeta-ai-agent  → apps/zeta-ai-agent
  - desktop        → apps/desktop
  - backend        → apps/backend

Usage:
  # Dry-run (default)
  python tools/reference_updater.py

  # Apply changes and emit a report json
  python tools/reference_updater.py --apply --report reference_updates.json

Options:
  --strict / --no-strict    Safer matching (avoid generic words), default: --strict
  --include <glob>          Additional include patterns (repeatable)
  --exclude <name>          Additional directory names to exclude (repeatable)
  --report <file>           Write JSON report with changes summary
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
import Exception
import any
import apply
import bool
import data
import dict
import e
import fc
import int
import len
import list
import n
import p
import part
import pat
import path
import pattern
import print
import repl
import report
import set
import str
import strict
import tuple

DEFAULT_CANDIDATES = [
    "package.json",
    "**/*.json",
    "**/*.yml",
    "**/*.yaml",
    "**/*.md",
    "**/Makefile",
    "**/*.ps1",
    "**/*.sh",
    "**/*.toml",
]

DEFAULT_EXCLUDES = {"node_modules", ".venv", ".git", "dist", "out"}


def build_patterns(strict: bool) -> list[tuple[re.Pattern[str], str]]:
    if strict:
        # Avoid replacing generic words by ensuring token boundaries (no word/dot/dash around)
        boundary = r"(?<![\w.-])"  # left not word/dot/dash
        rboundary = r"(?![\w.-])"  # right not word/dot/dash
        return [
            (re.compile(boundary + r"zeta-ai-agent" + rboundary), "apps/zeta-ai-agent"),
            (re.compile(boundary + r"desktop" + rboundary), "apps/desktop"),
            (re.compile(boundary + r"backend" + rboundary), "apps/backend"),
        ]
    else:
        return [
            (re.compile(r"\bzeta-ai-agent\b"), "apps/zeta-ai-agent"),
            (re.compile(r"\bdesktop\b"), "apps/desktop"),
            (re.compile(r"\bbackend\b"), "apps/backend"),
        ]


def should_skip(path: Path, excludes: set[str]) -> bool:
    return any(part in excludes for part in path.parts)


@dataclass
class FileChange:
    path: str
    replacements: int


def process_file(path: Path, patterns: Iterable[tuple[re.Pattern[str], str]], apply: bool) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return 0
    original = text
    total = 0
    for pat, repl in patterns:
        text, n = pat.subn(repl, text)
        total += n
    if total > 0 and text != original:
        if apply:
            path.write_text(text, encoding="utf-8")
            print(f"✓ Updated: {path} ({total} repl)")
        else:
            print(f"[DRY RUN] Would update: {path} ({total} repl)")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write changes to disk")
    parser.add_argument(
        "--strict",
        dest="strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Strict token-boundary matching (default)",
    )
    parser.add_argument("--include", action="append", default=[], help="Extra include glob pattern (repeatable)")
    parser.add_argument("--exclude", action="append", default=[], help="Extra directory name to exclude (repeatable)")
    parser.add_argument("--report", default=None, help="Write JSON report to file")
    args = parser.parse_args()

    candidates = list(DEFAULT_CANDIDATES) + list(args.include)
    excludes = set(DEFAULT_EXCLUDES) | set(args.exclude)
    patterns = build_patterns(args.strict)

    root = Path.cwd()
    total_changes = 0
    report: list[FileChange] = []

    for pattern in candidates:
        for p in root.glob(pattern):
            if p.is_file() and not should_skip(p, excludes):
                changed = process_file(p, patterns, apply=args.apply)
                if changed:
                    total_changes += changed
                    report.append(FileChange(path=str(p), replacements=changed))

    if args.report:
        try:
            Path(args.report).parent.mkdir(parents=True, exist_ok=True)
            from typing import Any

            data: dict[str, Any] = {
                "apply": args.apply,
                "strict": args.strict,
                "total_replacements": total_changes,
                "files": [asdict(fc) for fc in report],
            }
            Path(args.report).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"Report written: {args.report}")
        except Exception as e:
            print(f"[WARN] Failed to write report {args.report}: {e}")

    print(f"Done. {'Applied' if args.apply else 'Planned'} replacements: {total_changes} across {len(report)} files.")


if __name__ == "__main__":
    main()
