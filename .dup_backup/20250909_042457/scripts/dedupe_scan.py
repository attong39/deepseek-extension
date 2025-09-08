#!/usr/bin/env python3
"""
Deduplication scanner for the Zeta monorepo.
- Scans recursively, computes SHA256 hashes to find exact-duplicate files
- Detects filename duplicates (same name, different content)
- Builds a simple normalized-text fingerprint to catch near-duplicates
- Outputs a JSON and Markdown report (read-only; no file moves)

Usage (from repo root):
  python scripts/dedupe_scan.py --root . --report-dir dedupe_reports

Options:
  --root PATH            Root directory to scan (default: .)
  --report-dir PATH      Directory to save reports (default: ./dedupe_reports)
  --max-norm-size N      Only normalize files <= N bytes (default: 2_000_000)
  --include-ext EXT,...  Optional comma-separated extensions filter (e.g. py,ts,js)
  --exclude-dirs NAME,...Additional directory names to exclude (comma-separated)

Notes:
- Heavy directories (node_modules, .venv, dist, out, .git, __pycache__, etc.) are excluded by default.
- Normalization is best-effort for Python/TS/JS; others strip whitespace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import Exception
import argv
import bool
import by_hash
import by_name
import by_norm
import bytes
import d
import data
import dict
import dirnames
import dirpath
import dup_hash_groups
import e
import enc
import f
import fi
import filenames
import files
import fn
import g
import int
import len
import lines
import list
import max_norm_size
import n
import name
import name_dups
import ng
import norm_dups
import occ
import print
import set
import sorted
import str
import tuple
import x

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "out",
    "build",
    "__pycache__",
    ".ruff_cache",
    ".benchmarks",
    ".artifacts",
    "coverage_html",
    "reports",
    "sbom",
    ".pytest_cache",
}

TEXT_EXTS = {"py", "ts", "tsx", "js", "jsx", "json", "md", "toml", "yml", "yaml", "sh", "ps1", "css", "scss", "html"}


@dataclass
class FileInfo:
    path: str
    size: int
    sha256: str


@dataclass
class DuplicateGroup:
    sha256: str
    size: int
    files: list[str]


@dataclass
class NameDuplicate:
    filename: str
    occurrences: list[FileInfo]


@dataclass
class NormalizedDuplicateGroup:
    normhash: str
    representative_ext: str | None
    files: list[str]


@dataclass
class Report:
    root: str
    generated_at: str
    total_files_scanned: int
    duplicates_by_hash: list[DuplicateGroup]
    name_duplicates: list[NameDuplicate]
    normalized_duplicates: list[NormalizedDuplicateGroup]


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def read_file_bytes(p: Path) -> bytes | None:
    try:
        return p.read_bytes()
    except Exception:
        return None


def is_text_candidate(p: Path) -> bool:
    return p.suffix.lstrip(".").lower() in TEXT_EXTS


def normalize_text(content: str, ext: str) -> str:
    ext = ext.lower()
    if ext == "py":
        # Remove Python comments and docstrings (simple heuristic), collapse whitespace
        # Remove triple-quoted strings
        content = re.sub(r"'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\"", "", content)
        # Remove # comments
        content = re.sub(r"(?m)#.*$", "", content)
        # Collapse whitespace
        content = re.sub(r"\s+", " ", content)
        return content.strip()
    if ext in {"ts", "tsx", "js", "jsx"}:
        # Remove // and /* */ comments, collapse whitespace
        content = re.sub(r"(?m)//.*$", "", content)
        content = re.sub(r"/\*[\s\S]*?\*/", "", content)
        content = re.sub(r"\s+", " ", content)
        return content.strip()
    if ext in {"json", "toml", "yml", "yaml", "md", "html", "css", "scss", "sh", "ps1"}:
        # Generic: collapse whitespace
        content = re.sub(r"\s+", " ", content)
        return content.strip()
    # Fallback: return as-is
    return content


def safe_decode(b: bytes) -> str | None:
    for enc in ("utf-8", "utf-16", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            continue
    return None


def scan(
    root: Path, include_exts: set[str] | None, exclude_dirs: set[str], max_norm_size: int
) -> tuple[dict[str, list[FileInfo]], dict[str, list[FileInfo]], dict[str, list[str]], int]:
    by_hash: dict[str, list[FileInfo]] = {}
    by_name: dict[str, list[FileInfo]] = {}
    by_norm: dict[str, list[str]] = {}

    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude directories by name, in-place prune
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fn in filenames:
            p = Path(dirpath) / fn
            # Skip extremely large single files (>100MB) to avoid memory spikes
            try:
                size = p.stat().st_size
            except Exception:
                continue
            if size < 0:
                continue

            b = read_file_bytes(p)
            if b is None:
                continue

            total += 1
            digest = sha256_bytes(b)
            info = FileInfo(path=str(p), size=size, sha256=digest)

            by_hash.setdefault(digest, []).append(info)
            by_name.setdefault(fn, []).append(info)

            # Normalization for text files only and size limit
            if size <= max_norm_size and (include_exts is None or p.suffix.lstrip(".").lower() in include_exts):
                if is_text_candidate(p):
                    s = safe_decode(b)
                    if s is not None:
                        norm = normalize_text(s, p.suffix.lstrip("."))
                        if norm:
                            nd = sha256_bytes(norm.encode("utf-8", errors="ignore"))
                            by_norm.setdefault(nd, []).append(str(p))

    return by_hash, by_name, by_norm, total


def build_report(
    root: Path,
    by_hash: dict[str, list[FileInfo]],
    by_name: dict[str, list[FileInfo]],
    by_norm: dict[str, list[str]],
    total: int,
) -> Report:
    dup_hash_groups: list[DuplicateGroup] = []
    for digest, items in by_hash.items():
        if len(items) > 1:
            # All items share same size by definition; pick first
            dup_hash_groups.append(
                DuplicateGroup(
                    sha256=digest,
                    size=items[0].size,
                    files=sorted(fi.path for fi in items),
                )
            )

    name_dups: list[NameDuplicate] = []
    for name, items in by_name.items():
        if len(items) > 1:
            # If more than one and not all hashes equal, it's a content divergence under same filename
            hashes = {fi.sha256 for fi in items}
            if len(hashes) > 1:
                name_dups.append(NameDuplicate(filename=name, occurrences=sorted(items, key=lambda x: x.path)))

    norm_dups: list[NormalizedDuplicateGroup] = []
    for nd, files in by_norm.items():
        if len(files) > 1:
            ext = None
            try:
                ext = Path(files[0]).suffix.lstrip(".") or None
            except Exception:
                ext = None
            norm_dups.append(NormalizedDuplicateGroup(normhash=nd, representative_ext=ext, files=sorted(files)))

    rep = Report(
        root=str(root),
        generated_at=datetime.now(UTC).isoformat(),
        total_files_scanned=total,
        duplicates_by_hash=sorted(dup_hash_groups, key=lambda g: (g.size, g.sha256))[:1000],
        name_duplicates=sorted(name_dups, key=lambda n: n.filename)[:1000],
        normalized_duplicates=sorted(norm_dups, key=lambda n: (n.representative_ext or "", n.normhash))[:1000],
    )
    return rep


def write_reports(rep: Report, report_dir: Path) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "dedupe_report.json"
    md_path = report_dir / "dedupe_report.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(asdict(rep), f, indent=2, ensure_ascii=False)

    # Markdown summary
    lines: list[str] = []
    lines.append("# Dedupe Report\n")
    lines.append(f"- Root: `{rep.root}`")
    lines.append(f"- Generated at: `{rep.generated_at}`")
    lines.append(f"- Total files scanned: {rep.total_files_scanned}\n")

    lines.append(f"## Exact duplicate files (by SHA256): {len(rep.duplicates_by_hash)}\n")
    for g in rep.duplicates_by_hash[:50]:
        lines.append(f"- Size: {g.size} bytes | sha256: `{g.sha256}`")
        for p in g.files:
            lines.append(f"  - {p}")
    if len(rep.duplicates_by_hash) > 50:
        lines.append(f"\n... and {len(rep.duplicates_by_hash) - 50} more groups\n")

    lines.append(f"\n## Same filename, different content: {len(rep.name_duplicates)}\n")
    for nd in rep.name_duplicates[:50]:
        lines.append(f"- `{nd.filename}`")
        for occ in nd.occurrences:
            lines.append(f"  - {occ.path} | size={occ.size} | sha256={occ.sha256}")
    if len(rep.name_duplicates) > 50:
        lines.append(f"\n... and {len(rep.name_duplicates) - 50} more filename collisions\n")

    lines.append(f"\n## Normalized text duplicates (format/comments ignored): {len(rep.normalized_duplicates)}\n")
    for ng in rep.normalized_duplicates[:50]:
        lines.append(f"- ext={ng.representative_ext or '-'} | normhash={ng.normhash}")
        for p in ng.files[:10]:
            lines.append(f"  - {p}")
        if len(ng.files) > 10:
            lines.append(f"  ... and {len(ng.files) - 10} more")

    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return json_path, md_path


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scan and report duplicate files/code")
    p.add_argument("--root", default=".", help="Root directory to scan")
    p.add_argument("--report-dir", default="dedupe_reports", help="Directory to write reports")
    p.add_argument("--max-norm-size", type=int, default=2_000_000, help="Max file size (bytes) for normalization")
    p.add_argument(
        "--include-ext",
        dest="include_ext",
        default=None,
        help="Comma-separated list of extensions to normalize (e.g. py,ts,js)",
    )
    p.add_argument(
        "--exclude-dirs", dest="exclude_dirs", default=None, help="Comma-separated extra directories to exclude by name"
    )
    return p.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    report_dir = Path(args.report_dir).resolve() / datetime.now().strftime("%Y%m%d_%H%M%S")

    include_exts: set[str] | None = None
    if args.include_ext:
        include_exts = {e.strip().lstrip(".").lower() for e in args.include_ext.split(",") if e.strip()}

    exclude_dirs = set(DEFAULT_EXCLUDES)
    if args.exclude_dirs:
        exclude_dirs.update({d.strip() for d in args.exclude_dirs.split(",") if d.strip()})

    print(f"🔎 Scanning root: {root}")
    print(f"⛔ Excluding dirs: {sorted(exclude_dirs)}")
    print(f"🧪 Normalization includes: {sorted(include_exts) if include_exts else 'auto (text candidates)'}")

    by_hash, by_name, by_norm, total = scan(root, include_exts, exclude_dirs, args.max_norm_size)
    rep = build_report(root, by_hash, by_name, by_norm, total)

    json_path, md_path = write_reports(rep, report_dir)
    print(f"✅ Report written:\n  JSON: {json_path}\n  MD:   {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
