#!/usr/bin/env python3
"""
Detect duplicates in apps/backend/app:
- Duplicate filenames (same basename different paths)
- Duplicate content (same SHA256) across different files

Outputs a concise report to stdout and writes JSON to reports/backend_duplicates.json.
Safe, read-only.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
import Exception
import SystemExit
import by_hash
import by_name
import chunk
import dict
import e
import f
import files
import int
import iter
import k
import len
import list
import name
import p
import paths
import print
import sorted
import str
import v

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "apps" / "backend" / "app"
REPORTS = ROOT / "reports"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not APP_DIR.exists():
        print(f"❌ Not found: {APP_DIR}")
        return 1

    files: list[Path] = [p for p in APP_DIR.rglob("*.py") if p.is_file()]
    by_name: dict[str, list[str]] = defaultdict(list)
    by_hash: dict[str, list[str]] = defaultdict(list)

    for p in files:
        by_name[p.name].append(str(p.relative_to(APP_DIR)))
        try:
            by_hash[sha256_file(p)].append(str(p.relative_to(APP_DIR)))
        except Exception as e:
            print(f"⚠️ Failed to hash {p}: {e}")

    duplicate_names = {k: v for k, v in by_name.items() if len(v) > 1}
    duplicate_hashes = {k: v for k, v in by_hash.items() if len(v) > 1}

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = {
        "root": str(APP_DIR),
        "total_files": len(files),
        "duplicate_filenames": duplicate_names,
        "duplicate_contents": duplicate_hashes,
    }
    (REPORTS / "backend_duplicates.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("📦 apps/backend/app duplicate scan")
    print(f" - files scanned: {len(files)}")
    print(f" - duplicate names: {len(duplicate_names)}")
    print(f" - duplicate contents: {len(duplicate_hashes)}")

    if duplicate_names:
        print("\nDuplicate filenames (basename clashing):")
        for name, paths in sorted(duplicate_names.items()):
            print(f"  {name} ->")
            for p in paths:
                print(f"    - {p}")

    if duplicate_hashes:
        print("\nExact duplicate contents (same SHA256):")
        for h, paths in list(duplicate_hashes.items())[:50]:
            print(f"  {h[:12]}... ->")
            for p in paths:
                print(f"    - {p}")
        if len(duplicate_hashes) > 50:
            print(f"  ... and {len(duplicate_hashes)-50} more groups")

    print("\n📝 Full JSON: reports/backend_duplicates.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
