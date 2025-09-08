#!/usr/bin/env python3
"""Simple duplicate-file finder for this monorepo.

Scans target directories (default: zeta_vn, desktop_ai_zeta) and finds files with
identical content hashes. Skips common build/cache/vendor folders to reduce noise.

Usage:
  python scripts/find_duplicate_files.py [--roots zeta_vn desktop_ai_zeta] \
      [--ext .py .ts .tsx .js .json] [--out reports/duplicates/filehash_duplicates.json]

Outputs:
  - Prints a summary to stdout
  - Writes JSON with groups of duplicates (content-hash -> list of files)

Notes:
  - Exact duplicates only (byte-for-byte). For near-duplicates use jscpd or grep.
  - This is lightweight and does not require Node.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path
import DEFAULT_EXTS
import DEFAULT_OUT
import DEFAULT_ROOTS
import OSError
import SKIP_DIR_NAMES
import SKIP_PATH_CONTAINS
import SystemExit
import algo
import any
import chunk
import dict
import enumerate
import exts
import f
import files
import fp
import groups
import i
import int
import len
import list
import p
import part
import path
import print
import r
import root
import sorted
import str
import sum
import tuple
import v
import x

DEFAULT_ROOTS: tuple[str, ...] = ("zeta_vn", "desktop_ai_zeta")
DEFAULT_EXTS: tuple[str, ...] = (".py", ".ts", ".tsx", ".js", ".json", ".css", ".scss")
DEFAULT_OUT: str = "reports/duplicates/filehash_duplicates.json"

SKIP_DIR_NAMES: tuple[str, ...] = (
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "coverage_html",
    "reports",
    "storage",
)

SKIP_PATH_CONTAINS: tuple[str, ...] = (
    "src/api/generated/",
    "/api/generated/",
)


def iter_files(root: Path, exts: Sequence[str]) -> Iterator[Path]:
    for p in root.rglob("*"):
        try:
            if not p.is_file():
                continue
            # Skip empty files (e.g., many __init__.py placeholders)
            try:
                if p.stat().st_size == 0:
                    continue
            except OSError:
                continue
            # Skip directories by parts early
            if any(part in SKIP_DIR_NAMES for part in p.parts):
                continue
            rel = str(p)
            if any(x in rel for x in SKIP_PATH_CONTAINS):
                continue
            if exts and p.suffix.lower() not in exts:
                continue
            yield p
        except OSError:
            # Ignore permission or transient FS errors
            continue


def file_hash(path: Path, algo: str = "sha256", chunk: int = 1 << 16) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def find_duplicates(roots: Iterable[Path], exts: Sequence[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for root in roots:
        for f in iter_files(root, exts):
            try:
                h = file_hash(f)
                groups.setdefault(h, []).append(str(f))
            except OSError:
                # Skip unreadable files
                continue
    # Keep only hashes with >1 files
    return {h: files for h, files in groups.items() if len(files) > 1}


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash")
    parser.add_argument("--roots", nargs="*", default=list(DEFAULT_ROOTS))
    parser.add_argument("--ext", nargs="*", default=list(DEFAULT_EXTS))
    parser.add_argument("--out", default=DEFAULT_OUT)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    roots = [repo_root / r for r in args.roots]

    print(f"Scanning roots: {', '.join(str(r) for r in roots)}")
    dups = find_duplicates(roots, args.ext)

    total_groups = len(dups)
    total_files = sum(len(v) for v in dups.values())
    print(f"Found {total_groups} duplicate groups covering {total_files} files.")

    # Print top 10 largest duplicate groups
    if dups:
        print("\nTop duplicate groups (up to 10):")
        for i, (h, files) in enumerate(sorted(dups.items(), key=lambda x: len(x[1]), reverse=True)[:10], 1):
            print(f"[{i}] hash={h[:12]}... x{len(files)}")
            for fp in files[:5]:
                print(f"   - {Path(fp).relative_to(repo_root)}")
            if len(files) > 5:
                print(f"   ... and {len(files) - 5} more")

    # Write JSON report
    out_path = repo_root / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(dups, f, indent=2, ensure_ascii=False)
    print(f"\nJSON report written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
