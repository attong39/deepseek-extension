#!/usr/bin/env python3
"""
Find duplicate files in the repository by content hash.

Features:
- Fast grouping by file size, then partial-hash, then full-hash.
- Parallel hashing for speed.
- Configurable excludes, min/max size, hidden files handling.
- Outputs machine-readable JSON and a human-friendly Markdown summary.

Usage (PowerShell):
  python tools/find_duplicate_files.py --paths . \
    --exclude .git --exclude node_modules --exclude .venv \
    --output reports/duplicates/duplicate_files.json \
    --md-output reports/duplicates/duplicate_files.md \
    --print-top 20

Exit code: 0 on success; 2 if duplicates were found (useful for CI); 1 on error.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime as dt
import hashlib
import json
import os
import sys
import time
from collections.abc import Iterable, Sequence
from pathlib import Path
import Exception
import OSError
import algo
import argv
import bool
import by_full
import by_head
import by_size
import chunk_size
import d
import dict
import dirnames
import dirpath
import e
import enumerate
import ex
import excludes
import f
import filenames
import float
import fn
import follow_symlinks
import fut
import g
import groups
import head_bytes
import i
import include_hidden
import int
import len
import list
import lst
import max
import max_size
import min
import min_size
import nbytes
import num
import p
import path
import paths
import print
import set
import sorted
import str
import sum
import tuple
import unit
import workers

DEFAULT_EXCLUDES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "out",
    "coverage",
    "htmlcov",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
}

HASH_ALGOS = set(hashlib.algorithms_available)


def walk_files(
    roots: Sequence[Path], excludes: Sequence[str], include_hidden: bool, follow_symlinks: bool
) -> Iterable[Path]:
    exclude_set = set(excludes)

    for root in roots:
        root = root.resolve()
        if not root.exists():
            continue

        for dirpath, dirnames, filenames in os.walk(root, followlinks=follow_symlinks):
            dirpath_p = Path(dirpath)

            # Filter directories in-place to prune walk
            pruned = []
            for d in dirnames[:]:
                if d in exclude_set:
                    continue
                if not include_hidden and d.startswith("."):
                    continue
                pruned.append(d)
            dirnames[:] = pruned

            # Yield files
            for fn in filenames:
                if fn in exclude_set:
                    continue
                if not include_hidden and fn.startswith("."):
                    continue
                fp = dirpath_p / fn
                # Skip broken symlinks or special files
                try:
                    if not fp.is_file():
                        continue
                except OSError:
                    continue
                yield fp


def file_size(fp: Path) -> int | None:
    try:
        return fp.stat().st_size
    except OSError:
        return None


def hash_file(fp: Path, algo: str = "sha256", chunk_size: int = 1024 * 1024) -> str | None:
    try:
        h = hashlib.new(algo)
        with fp.open("rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def hash_file_head(fp: Path, nbytes: int = 64 * 1024, algo: str = "sha256") -> str | None:
    try:
        h = hashlib.new(algo)
        with fp.open("rb") as f:
            chunk = f.read(nbytes)
            h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def format_bytes(num: int) -> str:
    value = float(num)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} TB"


def find_duplicates(
    files: Iterable[Path],
    *,
    min_size: int = 1,
    max_size: int | None = None,
    head_bytes: int = 64 * 1024,
    algo: str = "sha256",
    workers: int = max(1, (os.cpu_count() or 2) * 2),
) -> tuple[list[dict], int, int]:
    """
    Returns (duplicate_groups, files_considered, bytes_considered)

    duplicate_groups: list of dicts {hash, size, count, wasted_bytes, paths}
    """
    # 1) Group by size
    by_size: dict[int, list[Path]] = {}
    files_considered = 0
    bytes_considered = 0

    for fp in files:
        sz = file_size(fp)
        if sz is None:
            continue
        if sz < min_size:
            continue
        if max_size is not None and sz > max_size:
            continue
        by_size.setdefault(sz, []).append(fp)
        files_considered += 1
        bytes_considered += sz

    # Keep only sizes with >1 files
    candidate_sizes = {sz: lst for sz, lst in by_size.items() if len(lst) > 1}
    if not candidate_sizes:
        return [], files_considered, bytes_considered

    # 2) Hash heads in parallel per size bucket
    by_head: dict[tuple[int, str], list[Path]] = {}
    with futures.ThreadPoolExecutor(max_workers=workers) as ex:
        tasks = {}
        for sz, paths in candidate_sizes.items():
            for p in paths:
                tasks[ex.submit(hash_file_head, p, head_bytes, algo)] = (sz, p)

        for fut in futures.as_completed(tasks):
            sz, p = tasks[fut]
            h = fut.result()
            if h is None:
                continue
            by_head.setdefault((sz, h), []).append(p)

    # 3) For groups >1, compute full hash in parallel
    by_full: dict[tuple[int, str], list[Path]] = {}
    with futures.ThreadPoolExecutor(max_workers=workers) as ex:
        tasks = {}
        for (sz, _hh), paths in by_head.items():
            if len(paths) < 2:
                continue
            for p in paths:
                tasks[ex.submit(hash_file, p, algo)] = (sz, p)

        for fut in futures.as_completed(tasks):
            sz, p = tasks[fut]
            h = fut.result()
            if h is None:
                continue
            by_full.setdefault((sz, h), []).append(p)

    # 4) Build duplicate groups
    groups: list[dict] = []
    for (sz, h), paths in by_full.items():
        if len(paths) < 2:
            continue
        groups.append(
            {
                "hash": h,
                "size": sz,
                "count": len(paths),
                "wasted_bytes": (len(paths) - 1) * sz,
                "paths": sorted(str(p) for p in paths),
            }
        )

    # Sort by wasted space desc
    groups.sort(key=lambda g: (g["wasted_bytes"], g["size"], g["count"]), reverse=True)
    return groups, files_considered, bytes_considered


def write_json_report(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_markdown_report(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dup_count = len(data.get("duplicates", []))
    files_scanned = data.get("scan", {}).get("files_scanned", 0)
    bytes_scanned = data.get("scan", {}).get("bytes_scanned", 0)
    duration = data.get("scan", {}).get("duration_seconds", 0)
    wasted_total = sum(d.get("wasted_bytes", 0) for d in data.get("duplicates", []))

    lines = []
    lines.append("# Duplicate Files Report\n")
    lines.append(f"Generated: {data.get('generated_at')}\n")
    lines.append(f"Roots: {', '.join(data.get('root_paths', []))}\n")
    lines.append("\n## Summary\n")
    lines.append(f"- Files scanned: {files_scanned}")
    lines.append(f"- Data scanned: {format_bytes(bytes_scanned)}")
    lines.append(f"- Duration: {duration:.2f}s")
    lines.append(f"- Duplicate groups: {dup_count}")
    lines.append(f"- Wasted space: {format_bytes(wasted_total)}\n")

    if dup_count:
        lines.append("\n## Groups (sorted by wasted space)\n")
        for i, g in enumerate(data["duplicates"], 1):
            lines.append(
                "\n### "
                f"{i}. {g['count']} files x {format_bytes(g['size'])} | "
                f"Wasted: {format_bytes(g['wasted_bytes'])}"
            )
            lines.append(f"Hash: `{g['hash']}`\n")
            for p in g["paths"]:
                lines.append(f"- {p}")
    else:
        lines.append("\nNo duplicates found.\n")

    content = "\n".join(lines) + "\n"
    with path.open("w", encoding="utf-8") as f:
        f.write(content)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash.")
    parser.add_argument("--paths", nargs="*", default=["."], help="Root paths to scan (default: .)")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=sorted(DEFAULT_EXCLUDES),
        help="Names to exclude (directory or filename exact match).",
    )
    parser.add_argument("--include-hidden", action="store_true", help="Include dotfiles and dot-directories.")
    parser.add_argument("--follow-symlinks", action="store_true", help="Follow symlinks during traversal.")
    parser.add_argument("--min-size", type=int, default=1, help="Minimum file size in bytes to consider (default: 1).")
    parser.add_argument(
        "--max-size", type=int, default=None, help="Maximum file size in bytes to consider (default: None)."
    )
    parser.add_argument(
        "--algo", type=str, default="sha256", choices=sorted(HASH_ALGOS), help="Hash algorithm (default: sha256)."
    )
    parser.add_argument(
        "--head-bytes", type=int, default=64 * 1024, help="Bytes to read for the initial head hash (default: 65536)."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, (os.cpu_count() or 2) * 2),
        help="Parallel worker threads (default: 2x CPUs).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help=("Path to write JSON report (default: " "reports/duplicates/duplicate_files_<timestamp>.json)."),
    )
    parser.add_argument(
        "--md-output",
        type=str,
        default=None,
        help=("Path to write Markdown report (default: " "reports/duplicates/duplicate_files_<timestamp>.md)."),
    )
    parser.add_argument("--relative", action="store_true", help="Output relative paths instead of absolute.")
    parser.add_argument(
        "--print-top",
        type=int,
        default=10,
        help="Print top N duplicate groups to console (default: 10). Use 0 to disable.",
    )
    parser.add_argument(
        "--ci-fail-on-duplicates", action="store_true", help="Exit with code 2 if duplicates are found (useful in CI)."
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    roots = [Path(p) for p in args.paths]
    t0 = time.time()

    files = list(walk_files(roots, args.exclude, args.include_hidden, args.follow_symlinks))
    groups, files_scanned, bytes_scanned = find_duplicates(
        files,
        min_size=args.min_size,
        max_size=args.max_size,
        head_bytes=args.head_bytes,
        algo=args.algo,
        workers=args.workers,
    )
    duration = time.time() - t0

    # Prepare report data
    root_paths = [str(p.resolve()) for p in roots]
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = Path("reports") / "duplicates"
    json_path = Path(args.output) if args.output else reports_dir / f"duplicate_files_{stamp}.json"
    md_path = Path(args.md_output) if args.md_output else reports_dir / f"duplicate_files_{stamp}.md"

    # Optionally convert to relative paths
    if args.relative:
        for g in groups:
            g["paths"] = [str(Path(p).resolve().relative_to(Path.cwd())) if Path(p).exists() else p for p in g["paths"]]

    data = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "root_paths": root_paths,
        "settings": {
            "exclude": args.exclude,
            "include_hidden": args.include_hidden,
            "follow_symlinks": args.follow_symlinks,
            "min_size": args.min_size,
            "max_size": args.max_size,
            "algo": args.algo,
            "head_bytes": args.head_bytes,
            "workers": args.workers,
            "relative_paths": args.relative,
        },
        "scan": {
            "files_scanned": files_scanned,
            "bytes_scanned": bytes_scanned,
            "duration_seconds": duration,
        },
        "duplicates": groups,
    }

    # Write reports
    try:
        write_json_report(json_path, data)
        write_markdown_report(md_path, data)
    except Exception as e:
        print(f"Error writing reports: {e}", file=sys.stderr)
        return 1

    # Console summary
    dup_groups = len(groups)
    dup_files = sum(g["count"] - 1 for g in groups)
    wasted = sum(g["wasted_bytes"] for g in groups)
    print("Duplicate scan complete")
    print(f"- Roots: {', '.join(root_paths)}")
    print(f"- Files scanned: {files_scanned}")
    print(f"- Data scanned: {format_bytes(bytes_scanned)}")
    print(f"- Duration: {duration:.2f}s")
    print(f"- Duplicate groups: {dup_groups}")
    print(f"- Duplicate files (beyond originals): {dup_files}")
    print(f"- Wasted space: {format_bytes(wasted)}")
    print(f"- JSON report: {json_path}")
    print(f"- Markdown report: {md_path}")

    if args.print_top and groups:
        topn = min(args.print_top, len(groups))
        print(f"\nTop {topn} groups:")
        for i, g in enumerate(groups[:topn], 1):
            print(f"{i:>3}. {g['count']} x {format_bytes(g['size'])} | " f"Wasted {format_bytes(g['wasted_bytes'])}")
            for p in g["paths"]:
                print(f"      - {p}")

    if args.ci_fail_on_duplicates and groups:
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
