"""Generate directory maps and detailed statistics for multiple roots.

Usage (from repo root):
    python .github/prompts/update_project_map.py --roots zeta_vn desktop_ai_zeta

Outputs to .github/prompts/PROJECT_MAP.md by default, including:
    - Directory tree for each root (deterministic order)
    - Stats per root: total dirs/files, total size, file counts by extension

Deterministic, UTF-8, excludes heavy/ephemeral folders by default.
"""

from __future__ import annotations

import argparse
import logging
import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import EXCLUDES_DEFAULT
import OSError
import PermissionError
import body_lines
import bool
import bytes_
import child
import cnt
import counts
import d
import depth
import dict
import dir_path
import enumerate
import ext_counts
import exts
import f
import float
import idx
import int
import kv
import len
import lines
import list
import max
import num_bytes
import options
import p
import path
import r
import root
import s
import sections
import seen
import set
import sorted
import stack
import stat_lines
import str
import tuple
import u

EXCLUDES_DEFAULT: set[str] = {
    ".git",
    ".svn",
    ".hg",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "coverage_html",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".DS_Store",
}


@dataclass
class Options:
    roots: list[Path]
    output: Path
    excludes: set[str]
    include_hidden: bool
    max_depth: int | None
    top_exts: int | None


@dataclass
class Stats:
    total_dirs: int
    total_files: int
    total_size: int
    exts: list[tuple[str, tuple[int, int]]]


def parse_args() -> Options:
    parser = argparse.ArgumentParser(description="Update PROJECT_MAP.md with directory trees")
    parser.add_argument(
        "--roots",
        nargs="*",
        default=["zeta_vn", "desktop_ai_zeta"],
        help="Project roots to include (relative to repo root)",
    )
    parser.add_argument(
        "--output",
        default=".github/prompts/PROJECT_MAP.md",
        help="Output markdown path",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Directory or file names to exclude (exact matches)",
    )
    parser.add_argument("--include-hidden", action="store_true", help="Include dotfiles/directories")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Optional max depth for tree (root=0)",
    )
    parser.add_argument(
        "--top-exts",
        type=int,
        default=None,
        help="Limit number of extensions in stats (default: show all)",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    roots = [Path(r) if Path(r).is_absolute() else repo_root / r for r in args.roots]
    output = Path(args.output) if Path(args.output).is_absolute() else repo_root / args.output
    excludes = set(EXCLUDES_DEFAULT)
    excludes.update(args.exclude)

    return Options(
        roots=roots,
        output=output,
        excludes=excludes,
        include_hidden=bool(args.include_hidden),
        max_depth=args.max_depth,
        top_exts=args.top_exts,
    )


def should_skip(path: Path, options: Options) -> bool:
    name = path.name
    if (not options.include_hidden) and name.startswith(".") and name not in {".github"}:
        return True
    if name in options.excludes:
        return True
    return False


def list_children(dir_path: Path, options: Options) -> list[Path]:
    try:
        children = [p for p in dir_path.iterdir() if not should_skip(p, options)]
    except PermissionError:
        return []
    return sorted(children, key=lambda p: (0 if p.is_dir() else 1, p.name.lower()))


def build_tree(
    dir_path: Path,
    options: Options,
    depth: int = 0,
    dir_counts: dict[Path, int] | None = None,
) -> list[str]:
    lines: list[str] = []
    children = list_children(dir_path, options)
    last_index = len(children) - 1
    for idx, child in enumerate(children):
        is_last = idx == last_index
        if depth == 0:
            prefix = ""
        else:
            branch = "└── " if is_last else "├── "
            prefix = ("    " * (depth - 1)) + branch
        if child.is_dir():
            count_str = ""
            if dir_counts is not None:
                count_str = f" ({dir_counts.get(child, 0)} files)"
            name = f"{child.name}/{count_str}"
        else:
            name = f"{child.name}"
        lines.append(f"{prefix}{name}")
        if child.is_dir():
            if options.max_depth is None or depth < options.max_depth:
                sub = build_tree(child, options, depth + 1, dir_counts)
                lines.extend([("    " * depth) + s for s in sub])
    return lines


def walk_files(root: Path, options: Options) -> Iterable[Path]:
    stack: list[Path] = [root]
    while stack:
        cur = stack.pop()
        try:
            for p in cur.iterdir():
                if should_skip(p, options):
                    continue
                if p.is_dir():
                    stack.append(p)
                elif p.is_file():
                    yield p
        except PermissionError:
            continue


def sizeof_fmt(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    units = ["KB", "MB", "GB", "TB"]
    x = float(num_bytes)
    for u in units:
        x /= 1024.0
        if x < 1024.0:
            return f"{x:.2f} {u}"
    return f"{x:.2f} PB"


def _count_dirs(root: Path, options: Options) -> int:
    total_dirs = 0
    stack: list[Path] = [root]
    seen: set[Path] = set()
    while stack:
        cur = stack.pop()
        if cur in seen or should_skip(cur, options):
            continue
        seen.add(cur)
        if cur.is_dir():
            total_dirs += 1
            try:
                for p in cur.iterdir():
                    if p.is_dir() and not should_skip(p, options):
                        stack.append(p)
            except PermissionError:
                pass
    return max(0, total_dirs - 1)  # exclude root


def compute_stats(root: Path, options: Options) -> Stats:
    total_files = 0
    total_size = 0
    ext_counts: dict[str, tuple[int, int]] = {}

    for f in walk_files(root, options):
        try:
            size = f.stat().st_size
        except OSError:
            size = 0
        total_files += 1
        total_size += size
        ext = f.suffix.lower() or "(no-ext)"
        cnt, bytes_ = ext_counts.get(ext, (0, 0))
        ext_counts[ext] = (cnt + 1, bytes_ + size)

    exts_sorted: list[tuple[str, tuple[int, int]]] = sorted(ext_counts.items(), key=lambda kv: (-kv[1][0], kv[0]))
    if options.top_exts is not None:
        exts_sorted = exts_sorted[: max(0, options.top_exts)]

    return Stats(
        total_dirs=_count_dirs(root, options),
        total_files=total_files,
        total_size=total_size,
        exts=exts_sorted,
    )


def compute_dir_file_counts(root: Path, options: Options) -> dict[Path, int]:
    """Return a mapping of directory -> total files under it (recursive)."""

    counts: dict[Path, int] = {}

    def _dfs(d: Path) -> int:
        try:
            children = [p for p in d.iterdir() if not should_skip(p, options)]
        except PermissionError:
            counts[d] = 0
            return 0
        total = 0
        for p in children:
            if p.is_dir():
                total += _dfs(p)
            elif p.is_file():
                total += 1
        counts[d] = total
        return total

    if root.exists() and root.is_dir():
        _dfs(root)
    return counts


def render_section(root: Path, options: Options) -> str:
    header = f"### {root.name}\n\n"
    body_lines: list[str] = []
    if not root.exists():
        body_lines.append(f"(missing path: {root.as_posix()})")
        code = "\n".join(body_lines)
        return header + "```\n" + code + "\n```\n\n"
    # Root exists: render tree + stats
    dir_counts = compute_dir_file_counts(root, options)
    root_count = dir_counts.get(root, 0)
    body_lines.append(f"{root.name}/ ({root_count} files)")
    tree_lines = build_tree(root, options, depth=1, dir_counts=dir_counts)
    body_lines.extend(tree_lines)
    stats = compute_stats(root, options)
    stat_lines: list[str] = []
    stat_lines.append(f"- Total directories: {stats.total_dirs}")
    stat_lines.append(f"- Total files: {stats.total_files}")
    stat_lines.append(f"- Total size: {sizeof_fmt(stats.total_size)}")
    stat_lines.append("")
    stat_lines.append("Files by extension:")
    exts: list[tuple[str, tuple[int, int]]] = list(stats.exts)
    if not exts:
        stat_lines.append("(no files)")
    else:
        for ext, (cnt, bytes_) in exts:
            stat_lines.append(f"  - {ext}: {cnt} files, {sizeof_fmt(bytes_)}")
    code = "\n".join(body_lines)
    stats_md = "\n".join(stat_lines)
    return header + "```\n" + code + "\n```\n\n" + stats_md + "\n\n"


def write_output(sections: Iterable[str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = [
        "# PROJECT MAP",
        "",
        "> This file is auto-generated by .github/prompts/update_project_map.py. Do not edit manually.",
        "",
    ]
    content.extend(sections)
    text = "\n".join(content)

    # Write atomically to avoid partial writes and ensure overwrite on all platforms
    tmp_path = output.with_suffix(output.suffix + ".tmp")
    tmp_path.write_text(text, encoding="utf-8")
    os.replace(tmp_path, output)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    opts = parse_args()

    sections: list[str] = []
    for root in opts.roots:
        sections.append(render_section(root, opts))

    write_output(sections, opts.output)
    logging.info("Updated %s with %d sections", opts.output.as_posix(), len(sections))


if __name__ == "__main__":
    main()
