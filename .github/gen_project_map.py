#!/usr/bin/env python3
import Exception
import PermissionError
import argv
import bool
import c
import d
import depth
import dir_counts
import e
import enumerate
import ext
import exts
import hints
import idx
import int
import k
import lang_counts
import len
import level
import max
import max_items
import n
import pat
import path
import prefix
import print
import set
import sorted
import str
import sum
import tree_lines
import tuple
import uniq
import v
import x
# -*- coding: utf-8 -*-
"""
Generate a Markdown project map with:
- Directory tree (depth‑limited)
- File/dir statistics
- Heuristic descriptions for common folders/files
- Optional .gitignore‑aware filtering (best‑effort)

Designed for modern AI / Copilot context: clean, deterministic, portable.
"""

from __future__ import annotations
import os
import sys
import argparse
import fnmatch
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Set

# ----------------------------------------------------------------------
# ─── Default ignore sets (always skipped) ─────────────────────────────
# ----------------------------------------------------------------------
DEFAULT_IGNORES = {
    ".git", ".hg", ".svn", ".DS_Store", "__pycache__", ".mypy_cache",
    ".ruff_cache", ".pytest_cache", ".cache", "node_modules", "dist",
    "build", ".venv", "venv", ".idea", ".vscode", ".next", ".turbo",
    ".parcel-cache", ".pnpm-store",
}

# ----------------------------------------------------------------------
# ─── Heuristic hints – folders & files ───────────────────────────────
# ----------------------------------------------------------------------
FOLDER_HINTS = {
    r"\b(app|api)\b": "Lớp interface (HTTP/WebSocket/API endpoints, routers, controllers).",
    r"\b(core|domain)\b": "Business/domain logic: entities, use‑cases, services, value objects.",
    r"\b(data|infra|infrastructure|adapters)\b": "Hạ tầng: repositories, DB adapters, external services.",
    r"\b(models?)\b": "Khai báo model (Pydantic/SQLModel/ORM) và schema dữ liệu.",
    r"\b(scripts|tools)\b": "Scripts CLI / devops, tiện ích build / test / deploy.",
    r"\b(config|settings)\b": "Cấu hình (env, constants, typed settings).",
    r"\b(tests?|specs?)\b": "Kiểm thử unit / integration / e2e, fixtures, helpers.",
    r"\b(docs?|documentation)\b": "Tài liệu hướng dẫn, kiến trúc, quyết định kỹ thuật.",
    r"\b(ui|frontend|web|desktop|electron|react)\b": "Frontend / desktop layer (Electron / React / Vite).",
    r"\b(plugins?|extensions?)\b": "Hệ plugin mở rộng, registry, enable/disable.",
    r"\b(assets?|static|public)\b": "Tài nguyên tĩnh: images, fonts, icons, html.",
    r"\b(migrations?)\b": "Migration DB (alembic / sql).",
    r"\b(examples?|samples?)\b": "Ví dụ, demo, blueprint.",
}

FILE_HINTS = {
    r"README\.md$": "Tài liệu chính cho module / thư mục.",
    r"pyproject\.toml$": "Python project config: build, deps, tooling.",
    r"package\.json$": "Node project manifest & scripts.",
    r"requirements(-\w+)?\.txt$": "Danh sách dependencies Python.",
    r"ruff\.toml$": "Ruff linter config.",
    r"mypy\.ini$": "MyPy strict typing config.",
    r"dockerfile|Dockerfile": "Docker image build instructions.",
    r"compose\.ya?ml$": "Docker‑Compose services.",
    r"tsconfig\.json$": "TypeScript compiler config.",
    r"\.env(\..+)?$": "Biến môi trường (không commit secrets!).",
    r"Makefile$": "Targets build / test tiện dụng.",
    r"LICENSE$": "Giấy phép dự án.",
}

# ----------------------------------------------------------------------
# ─── Language groups – only for a quick “by extension” stats ────────
# ----------------------------------------------------------------------
LANG_GROUPS = {
    "python": (".py",),
    "typescript": (".ts", ".tsx"),
    "javascript": (".js", ".jsx", ".mjs", ".cjs"),
    "shell": (".sh", ".bash"),
    "powershell": (".ps1",),
    "config": (".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"),
    "markdown": (".md",),
    "styles": (".css", ".scss", ".sass"),
    "html": (".html", ".htm"),
    "sql": (".sql",),
    "other": tuple(),
}

# ----------------------------------------------------------------------
# ─── Helper utilities ───────────────────────────────────────────────
# ----------------------------------------------------------------------
def load_gitignore_patterns(root: Path) -> List[str]:
    """Very light .gitignore parser – only simple glob patterns."""
    patterns = []
    gi = root / ".gitignore"
    if gi.exists():
        for line in gi.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def match_any(path: Path, patterns: Iterable[str]) -> bool:
    s = str(path.as_posix())
    for p in patterns:
        # Basic ** support (git‑ignore “/**/” → “/*/” is enough for our use)
        p = p.replace("/**/", "/*/")
        if fnmatch.fnmatch(s, p) or fnmatch.fnmatch(path.name, p):
            return True
    return False


def should_skip(path: Path, ignores: Set[str], extra_patterns: List[str]) -> bool:
    name = path.name
    if name in ignores:
        return True
    if match_any(path, extra_patterns):
        return True
    return False


def classify_lang(ext: str) -> str:
    for k, exts in LANG_GROUPS.items():
        if ext.lower() in exts:
            return k
    return "other"


def human_count(n: int) -> str:
    return f"{n:,}"


def relpath(p: Path, root: Path) -> str:
    """Return a POSIX‑style relative path ('.' for root)."""
    try:
        return p.relative_to(root).as_posix() or "."
    except Exception:
        return p.as_posix()


# ----------------------------------------------------------------------
# ─── Core tree collector ─────────────────────────────────────────────
# ----------------------------------------------------------------------
def collect_tree(
    root: Path,
    depth: int,
    ignores: Set[str],
    extra_patterns: List[str],
) -> Tuple[List[str], Dict[str, int], Dict[str, int], int]:
    """
    Returns:
        tree_lines   – ascii‑tree strings
        lang_counts  – language group → file count
        dir_counts   – directory (relative) → file count **inside** that directory
        total_files  – overall file count (only files that survived filtering)
    """
    tree_lines: List[str] = []
    lang_counts: Dict[str, int] = defaultdict(int)
    dir_counts: Dict[str, int] = defaultdict(int)
    total_files = 0

    def walk(d: Path, level: int, prefix: str):
        nonlocal total_files
        try:
            entries = sorted(
                d.iterdir(),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except PermissionError:
            return

        # Apply ignores
        entries = [e for e in entries if not should_skip(e, ignores, extra_patterns)]

        for idx, e in enumerate(entries):
            is_last = idx == len(entries) - 1
            connector = "└── " if is_last else "├── "
            line = f"{prefix}{connector}{e.name}"
            tree_lines.append(line)

            if e.is_dir():
                if level < depth - 1:
                    sub_prefix = f"{prefix}{'    ' if is_last else '│   '}"
                    walk(e, level + 1, sub_prefix)
            else:
                total_files += 1
                dir_counts[relpath(d, root)] += 1
                lang_counts[classify_lang(e.suffix or "")] += 1

    # Root line (shown as '.' if you run from inside the repo)
    tree_lines.append(relpath(root, root))
    walk(root, 0, "")
    return tree_lines, lang_counts, dir_counts, total_files


# ----------------------------------------------------------------------
# ─── Description inference (heuristics) ───────────────────────────────
# ----------------------------------------------------------------------
def infer_description(name: str, hints: Dict[str, str]) -> str | None:
    for pat, desc in hints.items():
        if re.search(pat, name, flags=re.IGNORECASE):
            return desc
    return None


def summarize_dirs(
    root: Path,
    max_items: int,
    dir_counts: Dict[str, int],
) -> List[Tuple[str, int, str]]:
    """Top directories by file count – with optional heuristic description."""
    items = sorted(
        ((d, c) for d, c in dir_counts.items() if d != "."),
        key=lambda x: x[1],
        reverse=True,
    )[:max_items]

    out = []
    for d, c in items:
        desc = infer_description(Path(d).name, FOLDER_HINTS) or ""
        out.append((d, c, desc))
    return out


def summarize_key_files(root: Path, max_items: int) -> List[Tuple[str, str]]:
    """Find up‑to‑max_items files that match the FILE_HINTS patterns."""
    candidates = []
    for pat in FILE_HINTS.keys():
        for p in root.rglob("*"):
            if p.is_file() and re.search(pat, p.name, flags=re.IGNORECASE):
                rp = relpath(p, root)
                desc = infer_description(p.name, FILE_HINTS) or ""
                candidates.append((rp, desc))

    # Deduplicate while preserving stable ordering (shortest path first)
    seen = set()
    uniq: List[Tuple[str, str]] = []
    for rp, desc in sorted(candidates, key=lambda x: (len(x[0]), x[0].lower())):
        if rp not in seen:
            seen.add(rp)
            uniq.append((rp, desc))
    return uniq[:max_items]


# ----------------------------------------------------------------------
# ─── Markdown renderer ───────────────────────────────────────────────
# ----------------------------------------------------------------------
def render_markdown(
    root: Path,
    depth: int,
    tree_lines: List[str],
    lang_counts: Dict[str, int],
    dir_counts: Dict[str, int],
    total_files: int,
) -> str:
    md = []

    # Header -----------------------------------------------------------
    md.append(f"# Project Map – {root.name}\n")
    md.append(
        "> Tự động sinh: cấu trúc thư mục, thống kê ngôn ngữ, mô tả heuristic cho folder/file then chốt."
    )
    md.append("")

    # Overall stats ----------------------------------------------------
    total_dirs = sum(1 for _ in root.rglob("*") if _.is_dir())
    md.append("## Tổng quan")
    md.append(f"- **Gốc**: `{root.as_posix()}`")
    md.append(f"- **Độ sâu cây**: `{depth}`")
    md.append(f"- **Số thư mục (xấp xỉ)**: `{human_count(total_dirs)}`")
    md.append(f"- **Số file (đếm trong cây)**: `{human_count(total_files)}`")
    if lang_counts:
        md.append("- **Phân bố ngôn ngữ (ước lượng theo đuôi file)**:")
        for k, v in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True):
            if v:
                md.append(f"  - `{k}`: {v}")
    md.append("")

    # Top directories --------------------------------------------------
    top_dirs = summarize_dirs(root, max_items=15, dir_counts=dir_counts)
    if top_dirs:
        md.append("## Thư mục chính (ưu tiên theo số file)")
        md.append("| Thư mục | #files | Gợi ý chức năng |")
        md.append("|---|---:|---|")
        for d, c, desc in top_dirs:
            md.append(f"| `{d}` | {c} | {desc} |")
        md.append("")

    # Key files ---------------------------------------------------------
    kfiles = summarize_key_files(root, max_items=20)
    if kfiles:
        md.append("## File then chốt")
        md.append("| File | Gợi ý vai trò |")
        md.append("|---|---|")
        for p, desc in kfiles:
            md.append(f"| `{p}` | {desc} |")
        md.append("")

    # Directory tree ---------------------------------------------------
    md.append("## Cấu trúc thư mục")
    md.append("```text")
    md.extend(tree_lines)
    md.append("```")
    md.append("")

    # Copilot / AI context suggestions ----------------------------------
    md.append("## Gợi ý dùng làm context cho AI / Copilot")
    md.append("- Dùng phần **Thư mục chính** để ưu tiên nạp vào context trước (core / domain / app / infrastructure / tests).")
    md.append("- Đính kèm `README.md` của từng module khi yêu cầu AI tạo / tối ưu mã.")
    md.append("- Kết hợp với tài liệu kiến trúc để AI hiểu flow: request → use‑case → repo → external adapter.")
    md.append("")
    return "\n".join(md)


# ----------------------------------------------------------------------
# ─── CLI entry point ─────────────────────────────────────────────────
# ----------------------------------------------------------------------
def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Markdown project map (tree + stats + heuristics)."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory (default: current working directory)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Maximum depth to render the tree (default: 3)",
    )
    parser.add_argument(
        "--ignore",
        type=str,
        default="",
        help="Comma‑separated folder/file names to always ignore",
    )
    parser.add_argument(
        "--respect-gitignore",
        action="store_true",
        help="Filter using patterns from .gitignore (best‑effort)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="",
        help="Write output to this file (Markdown). If omitted, prints to stdout.",
    )
    args = parser.parse_args(argv)

    # Resolve root ------------------------------------------------------
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"[ERR] Root path not found or not a directory: {root}", file=sys.stderr)
        return 2

    # Build ignore set --------------------------------------------------
    ignores = set(DEFAULT_IGNORES)
    if args.ignore.strip():
        for name in (n.strip() for n in args.ignore.split(",") if n.strip()):
            ignores.add(name)

    # Optional .gitignore patterns ---------------------------------------
    extra_patterns: List[str] = []
    if args.respect_gitignore:
        extra_patterns = load_gitignore_patterns(root)

    # Collect data -------------------------------------------------------
    tree_lines, lang_counts, dir_counts, total_files = collect_tree(
        root=root,
        depth=max(1, args.depth),
        ignores=ignores,
        extra_patterns=extra_patterns,
    )

    # Render -------------------------------------------------------------
    md = render_markdown(
        root=root,
        depth=args.depth,
        tree_lines=tree_lines,
        lang_counts=lang_counts,
        dir_counts=dir_counts,
        total_files=total_files,
    )

    # Output -------------------------------------------------------------
    if args.out:
        out_path = Path(args.out).resolve()
        out_path.write_text(md, encoding="utf-8")
        print(f"[OK] Wrote {out_path}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
