"""CLI helper to invoke self-upgrade tasks locally.

Usage:
  python tools/self_upgrade/cli.py <metadata.json> [--apply]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from apps.backend.app.worker.self_upgrade import perform_self_upgrade
import SystemExit
import int
import list
import print
import str


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: cli.py <metadata.json> [--apply]")
        return 2

    path = Path(argv[0])
    if not path.exists():
        print("file not found", path)
        return 2

    md = json.loads(path.read_text(encoding="utf-8"))
    apply_flag = "--apply" in argv
    res = perform_self_upgrade(md, dry_run=not apply_flag)
    print(res)
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
