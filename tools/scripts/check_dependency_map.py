"""Simple dependency checker using PROJECT_MAP.md to map file groups.

This tool reads a small mapping (hardcoded patterns) and verifies that when
core files change, related files are present in the diff or at least exist in
the repo. It's intentionally conservative and prints warnings (non-failing)
so teams can triage.

Usage: python tools/check_dependency_map.py --changed-files <file1> <file2>...
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
import SystemExit
import argv
import changed
import dict
import f
import int
import k
import list
import p
import pat
import print
import set
import str
import v

MAP = {
    "core/use_cases": [
        "app/api/v1/*",
        "data/repositories/*",
        "zeta_vn/tests/**",
    ],
    "app/api/v1": [
        "core/use_cases/*",
        "data/repositories/*",
        "zeta_vn/tests/**",
    ],
}


def find_related(changed: Iterable[str]) -> dict[str, set[str]]:
    repo_root = Path.cwd()
    warnings: dict[str, set[str]] = {}
    for p in changed:
        # simple heuristic: if path contains 'core/use_cases' then suggest API + repo + tests
        if "core/use_cases" in p:
            expected = MAP["core/use_cases"]
            found = set()
            for pat in expected:
                # normalize pattern to repo glob
                for f in repo_root.rglob(pat):
                    found.add(str(f))
            if not found:
                warnings[p] = set(expected)

    return warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-files", nargs="*", default=[])  # from CI or pre-commit
    args = parser.parse_args(argv)

    warnings = find_related(args.changed_files)

    if not warnings:
        print("No dependency warnings detected.")
        return 0

    print("Dependency warnings:")
    print(json.dumps({k: list(v) for k, v in warnings.items()}, indent=2))
    # Non-zero exit intentionally avoided to not break CI; teams should triage.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
