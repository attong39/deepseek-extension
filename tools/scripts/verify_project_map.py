"""Verify PROJECT_MAP.md contains repo module files.

This script checks that python modules under `zeta_vn/app`, `zeta_vn/core`,
and `zeta_vn/data` are referenced in `.github/prompts/PROJECT_MAP.md`.

Exit code 0 if all files are mentioned; 2 if missing entries found.

This is intentionally conservative and can be tuned later.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
import SystemExit
import base
import int
import m
import p
import print
import root
import sorted
import str

ROOT = Path(__file__).resolve().parents[1]
PROJECT_MAP = ROOT / ".github" / "prompts" / "PROJECT_MAP.md"


def iter_targets(root: Path) -> Iterable[Path]:
    for base in (
        root / "zeta_vn" / "app",
        root / "zeta_vn" / "core",
        root / "zeta_vn" / "data",
    ):
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            # skip typical non-public/runtime files
            if p.name == "__init__.py":
                continue
            if "tests" in p.parts or "node_modules" in p.parts:
                continue
            yield p.relative_to(root)


def main() -> int:
    if not PROJECT_MAP.exists():
        print(f"PROJECT_MAP.md not found at {PROJECT_MAP}")
        return 1

    content = PROJECT_MAP.read_text(encoding="utf-8")

    missing = []
    for p in sorted(iter_targets(ROOT)):
        # Check by posix path substring
        s = str(p.as_posix())
        if s not in content:
            missing.append(s)

    if missing:
        print("The following module files under zeta_vn appear NOT listed in PROJECT_MAP.md:")
        for m in missing:
            print(f" - {m}")
        print("\nPlease add them to .github/prompts/PROJECT_MAP.md or update the verifier mapping.")
        return 2

    print("PROJECT_MAP.md contains entries for all scanned modules (checked paths).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
