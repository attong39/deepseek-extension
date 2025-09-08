#!/usr/bin/env python3
"""
Duplicate Code Scanner

Scans the repository for duplicate function bodies in Python and TS/TSX files
and writes a JSON report with clusters of duplicates by normalized body hash.

Heuristics, not perfect: aims to catch obvious copy-paste duplicates.
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import Exception
import ValueError
import any
import bool
import cfg_path
import clusters
import config
import dict
import f
import file_path
import getattr
import hash
import int
import isinstance
import k
import len
import list
import ln
import m
import max
import n
import node
import occ
import p
import path
import print
import results
import root
import set
import str
import sum
import tuple
import v

try:
    import yaml  # type: ignore
except Exception:
    yaml = None


def load_config(cfg_path: Path) -> dict[str, Any]:
    if yaml is None or not cfg_path.exists():
        return {}
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}


def is_excluded(root: Path, file_path: Path, config: dict[str, Any]) -> bool:
    patterns = config.get("analysis", {}).get(
        "exclude_patterns",
        [
            "**/node_modules/**",
            "**/dist/**",
            "**/build/**",
            "**/__pycache__/**",
            "**/.git/**",
            "**/.venv/**",
            "**/venv/**",
            "**/.*/**",
        ],
    )
    try:
        rel = file_path.relative_to(root).as_posix()
    except ValueError:
        rel = file_path.as_posix()
    candidate = rel if file_path.is_file() else (rel.rstrip("/") + "/")
    return any(fnmatch.fnmatch(candidate, p) for p in patterns)


def find_source_files(root: Path, config: dict[str, Any]) -> list[Path]:
    include_exts = set(config.get("analysis", {}).get("include_extensions", [".py", ".ts", ".tsx"]))
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in include_exts and not is_excluded(root, path, config):
            files.append(path)
    return files


def normalize_source_lines(src: str) -> list[str]:
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in src.splitlines()]
    return [ln for ln in lines if ln and not ln.lstrip().startswith(("#", "//"))]


@dataclass
class Occurrence:
    file: str
    start_line: int
    end_line: int
    kind: str  # python|ts
    name: str


def py_function_bodies(path: Path) -> list[tuple[str, int, int, str]]:
    """Return list of (normalized_body, start, end, name) for Python functions."""
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        tree = ast.parse(src)
    except Exception:
        return []
    lines = src.splitlines()
    results: list[tuple[str, int, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.body:
            try:
                start = node.body[0].lineno
                end = max(getattr(n, "end_lineno", getattr(n, "lineno", start)) for n in node.body)
            except Exception:
                continue
            chunk = "\n".join(lines[start - 1 : end])
            norm = "\n".join(normalize_source_lines(chunk))
            if norm.count("\n") + 1 >= 5 and len(norm) >= 60:  # min 5 lines, 60 chars
                results.append((norm, start, end, node.name))
    return results


TS_FUNC_RE = re.compile(
    r"(?:function\s+(?P<name1>[A-Za-z0-9_]+)\s*\([^)]*\)\s*\{|"
    r"const\s+(?P<name2>[A-Za-z0-9_]+)\s*=\s*\([^)]*\)\s*=>\s*\{)",
)


def ts_function_bodies(path: Path) -> list[tuple[str, int, int, str]]:
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return []
    results: list[tuple[str, int, int, str]] = []
    for m in TS_FUNC_RE.finditer(src):
        name = m.group("name1") or m.group("name2") or "anonymous"
        start = m.end()
        # naive brace matching
        depth = 1
        i = start
        while i < len(src) and depth > 0:
            ch = src[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            i += 1
        body = src[start : i - 1]
        norm = "\n".join(normalize_source_lines(body))
        start_line = src.count("\n", 0, m.start()) + 1
        end_line = src.count("\n", 0, i) + 1
        if norm.count("\n") + 1 >= 5 and len(norm) >= 60:
            results.append((norm, start_line, end_line, name))
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="Duplicate code scanner")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--config", type=Path, default=Path("tools/ai-project-analyzer/config.yml"))
    ap.add_argument("--out", type=Path, default=Path("tools/ai-project-analyzer/out/duplicates.json"))
    args = ap.parse_args()

    cfg = load_config(args.config)
    files = find_source_files(args.root, cfg)

    clusters: dict[str, list[Occurrence]] = {}
    for f in files:
        try:
            if f.suffix == ".py":
                bodies = py_function_bodies(f)
                kind = "python"
            elif f.suffix in {".ts", ".tsx"}:
                bodies = ts_function_bodies(f)
                kind = "ts"
            else:
                continue
            for norm, start, end, name in bodies:
                key = f"{kind}:{hash(norm)}"
                clusters.setdefault(key, []).append(
                    Occurrence(file=str(f), start_line=start, end_line=end, kind=kind, name=name)
                )
        except Exception:
            continue

    # Filter clusters with at least 2 occurrences
    report = {
        "total_clusters": sum(1 for v in clusters.values() if len(v) >= 2),
        "duplicates": [
            {
                "hash": k,
                "count": len(v),
                "occurrences": [occ.__dict__ for occ in v],
            }
            for k, v in clusters.items()
            if len(v) >= 2
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Duplicate report written to {args.out} (clusters: {report['total_clusters']})")


if __name__ == "__main__":
    main()
