#!/usr/bin/env python3
"""
consolidation_audit.py

Audit a monorepo for consolidation readiness:
- Detect exact duplicate files (by SHA-256) and near-duplicate code (by normalized fingerprints)
- Validate Python imports (static resolution of local modules/packages)
- Validate relative TS/JS imports (resolve file paths with common extensions)

Outputs JSON and Markdown reports under a timestamped directory.

Usage (PowerShell):
    python scripts/consolidation_audit.py \
        --root . \
        --report-dir reports/consolidation_audit \
        --include-ext .py,.ts,.tsx,.js,.jsx,.mjs,.cjs,.json,.md,.yml,.yaml \
        --exclude-dirs .git,.venv,node_modules,dist,build,__pycache__

Notes:
- Only performs static analysis; no code execution
- For TS/JS, only relative imports are validated by default
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import json
import os
import re
import sys
from collections.abc import Iterable
from pathlib import Path
import Exception
import alias
import argv
import base_file
import bool
import chunk
import content
import current_file
import d
import data
import dict
import dirnames
import dirpath
import e
import enable_near
import exact_cnt
import f
import filenames
import fn
import fp
import getattr
import idx
import int
import is_local
import isinstance
import issues
import it
import k
import len
import list
import name
import near_cnt
import node
import packages
import print
import range
import s
import self
import set
import sorted
import spec
import str
import title
import total_files
import tuple
import v

# ----------------------------- Helpers & Types ----------------------------- #

TextExts = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".md", ".yml", ".yaml", ".txt"}
CodeExts = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
INIT_FILE = "__init__.py"

JS_TS_EXT_RESOLUTION = [
    "",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".d.ts",
    ".json",
]

INDEX_CANDIDATES = [
    "index.ts",
    "index.tsx",
    "index.js",
    "index.jsx",
    "index.mjs",
    "index.cjs",
]


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def read_text_safely(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def strip_python_comments_and_docstrings(code: str) -> str:
    """Remove comments and docstrings using AST/tokenization-safe approach."""
    try:
        parsed = ast.parse(code)
    except Exception:
        # Fall back to naive removal if parsing fails
        code = re.sub(r"(^|\s)#.*", "", code)
        return re.sub(r"\s+", " ", code).strip()

    class DocstringRemover(ast.NodeTransformer):
        def _strip(self, node):
            self.generic_visit(node)
            if (
                getattr(node, "body", None)
                and isinstance(node.body[0], ast.Expr)
                and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                node.body = node.body[1:]
            return node

        def visit_FunctionDef(self, node):
            return self._strip(node)

        def visit_AsyncFunctionDef(self, node):
            return self._strip(node)

        def visit_ClassDef(self, node):
            return self._strip(node)

        def visit_Module(self, node):
            return self._strip(node)

    stripped = DocstringRemover().visit(parsed)
    try:
        import astor  # type: ignore

        code_out = astor.to_source(stripped)
    except Exception:
        # Fallback: naive removal of comments & compress whitespace
        code_out = re.sub(r"(^|\s)#.*", "", code)
    return re.sub(r"\s+", " ", code_out).strip()


def strip_js_ts_comments(code: str) -> str:
    # Remove /* */ and // comments, then compress whitespace
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.S)
    code = re.sub(r"(^|\s)//.*", " ", code)
    return re.sub(r"\s+", " ", code).strip()


def code_fingerprint(path: Path, text: str) -> str:
    ext = path.suffix.lower()
    if ext == ".py":
        normalized = strip_python_comments_and_docstrings(text)
    elif ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
        normalized = strip_js_ts_comments(text)
    else:
        # generic normalize
        normalized = re.sub(r"\s+", " ", text).strip()
    # Shorten to avoid huge memory
    base_short = normalized[:100000]  # 100k chars cap
    return hashlib.sha256(base_short.encode("utf-8", errors="ignore")).hexdigest()


def walk_files(root: Path, include_ext: set[str], exclude_dirs: set[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        # mutate dirnames in-place to prune traversal
        pruned = []
        for d in dirnames:
            if d in exclude_dirs:
                continue
            pruned.append(d)
        dirnames[:] = pruned

        for fn in filenames:
            p = Path(dirpath) / fn
            if include_ext and p.suffix.lower() not in include_ext:
                continue
            yield p


# ------------------------------- Duplicates ------------------------------- #


def scan_duplicates(
    files: Iterable[Path], enable_near: bool = True
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    exact: dict[str, list[str]] = {}
    near: dict[str, list[str]] = {}

    for p in files:
        try:
            h = sha256_file(p)
        except Exception:
            continue
        exact.setdefault(h, []).append(str(p))

        if enable_near and p.suffix.lower() in CodeExts | {".md"}:
            txt = read_text_safely(p)
            if not txt:
                continue
            fh = code_fingerprint(p, txt)
            near.setdefault(fh, []).append(str(p))

    # filter only groups with >1
    exact = {k: v for k, v in exact.items() if len(v) > 1}
    near = {k: v for k, v in near.items() if len(v) > 1}
    return exact, near


# --------------------------- Python Import Check -------------------------- #


def py_module_name(root: Path, file: Path) -> str | None:
    try:
        rel = file.relative_to(root)
    except Exception:
        return None
    parts = list(rel.parts)
    if parts[-1] == INIT_FILE:
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    if not parts:
        return None
    return ".".join(parts)


def discover_python_packages(root: Path) -> set[Path]:
    packages: set[Path] = set()
    for dirpath, dirnames, filenames in os.walk(root):
        if "__init__.py" in filenames:
            packages.add(Path(dirpath))
    return packages


def _resolve_abs_python_import(root: Path, name: str) -> tuple[str, str, bool]:
    top = name.split(".")[0]
    candidate = root / top
    if (candidate / INIT_FILE).exists():
        path = root / (name.replace(".", os.sep) + ".py")
        if path.exists():
            return (name, str(path), True)
        pkg_path = root / name.replace(".", os.sep)
        if (pkg_path / INIT_FILE).exists():
            return (name, str(pkg_path), True)
        return (name, "", True)
    return (name, "", False)


def _resolve_rel_python_import(current_file: Path, mod: str, level: int) -> tuple[str, str, bool]:
    base = current_file.parent
    for _ in range(level - 1):
        base = base.parent
    target = base / mod.replace(".", os.sep) if mod else base
    if target.with_suffix(".py").exists():
        return (f"from {'.'*level}{mod} import ...", str(target.with_suffix(".py")), True)
    if (target / INIT_FILE).exists():
        return (f"from {'.'*level}{mod} import ...", str(target), True)
    return (f"from {'.'*level}{mod} import ...", "", True)


def resolve_python_import(root: Path, current_file: Path, node: ast.AST) -> tuple[str, str, bool]:
    """Return (import_repr, resolved_path, is_local). resolved_path may be '' if unknown."""
    if isinstance(node, ast.Import):
        for alias in node.names:
            return _resolve_abs_python_import(root, alias.name)
    if isinstance(node, ast.ImportFrom):
        mod = node.module or ""
        level = getattr(node, "level", 0) or 0
        if level > 0:
            return _resolve_rel_python_import(current_file, mod, level)
        if mod:
            return _resolve_abs_python_import(root, mod)
        return (f"from {mod} import ...", "", False)
    return ("", "", False)


def check_python_imports(root: Path, files: Iterable[Path]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for f in files:
        if f.suffix.lower() != ".py":
            continue
        text = read_text_safely(f)
        try:
            tree = ast.parse(text)
        except Exception as e:
            issues.append({"file": str(f), "type": "syntax_error", "message": str(e)})
            continue

        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            imp, resolved, is_local = resolve_python_import(root, f, node)
            if is_local and not resolved:
                issues.append(
                    {
                        "file": str(f),
                        "type": "unresolved_local_import",
                        "import": imp,
                        "message": "Local import target not found in repo",
                    }
                )
            # External imports are ignored here
    return issues


# -------------------------- TS/JS Relative Imports ------------------------- #

IMPORT_RE = re.compile(r"^\s*import\s+(?:[^'\"]+from\s+)?['\"]([^'\"]+)['\"];?", re.M)
IMPORT_RE2 = re.compile(r"^\s*export\s+\{[^}]*\}\s+from\s+['\"]([^'\"]+)['\"];?", re.M)
REQ_RE = re.compile(r"require\(\s*['\"]([^'\"]+)['\"]\s*\)")


def resolve_js_ts_import(base_file: Path, spec: str) -> Path | None:
    if not spec.startswith("."):
        return None  # treat as external/aliased
    cand = (base_file.parent / spec).resolve()
    # direct file
    for ext in JS_TS_EXT_RESOLUTION:
        p = cand.with_suffix(ext) if ext else cand
        if p.exists():
            return p
    # folder index
    if cand.is_dir():
        for idx in INDEX_CANDIDATES:
            p = cand / idx
            if p.exists():
                return p
    return None


def check_ts_js_imports(files: Iterable[Path]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for f in files:
        if f.suffix.lower() not in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
            continue
        text = read_text_safely(f)
        specs = set()
        specs.update(IMPORT_RE.findall(text))
        specs.update(IMPORT_RE2.findall(text))
        specs.update(REQ_RE.findall(text))
        for s in specs:
            if not s.startswith("."):
                continue  # external or aliased, skip
            resolved = resolve_js_ts_import(f, s)
            if not resolved:
                issues.append(
                    {
                        "file": str(f),
                        "type": "unresolved_relative_import",
                        "import": s,
                        "message": "Relative import target not found",
                    }
                )
    return issues


# --------------------------------- Report --------------------------------- #


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def md_for_duplicates(exact: dict[str, list[str]], near: dict[str, list[str]]) -> str:
    lines = ["# Consolidation Audit - Duplicates", ""]
    lines.append(f"- Exact duplicate groups: {len(exact)}")
    lines.append(f"- Near-duplicate groups: {len(near)}")
    lines.append("")
    if exact:
        lines.append("## Exact Duplicates")
        for k, files in exact.items():
            lines.append(f"- Hash: `{k}` ({len(files)} files)")
            for fp in files:
                lines.append(f"  - `{fp}`")
        lines.append("")
    if near:
        lines.append("## Near Duplicates (normalized code)")
        for k, files in near.items():
            lines.append(f"- Fingerprint: `{k[:16]}...` ({len(files)} files)")
            for fp in files:
                lines.append(f"  - `{fp}`")
        lines.append("")
    return "\n".join(lines)


def md_for_issues(title: str, issues: list[dict[str, str]]) -> str:
    lines = [f"# Consolidation Audit - {title}", ""]
    lines.append(f"- Issue count: {len(issues)}")
    lines.append("")
    for it in issues:
        file = it.get("file", "")
        typ = it.get("type", "")
        msg = it.get("message", "")
        imp = it.get("import", "")
        if imp:
            lines.append(f"- `{file}` | {typ} | `{imp}` | {msg}")
        else:
            lines.append(f"- `{file}` | {typ} | {msg}")
    return "\n".join(lines)


def md_summary(total_files: int, exact_cnt: int, near_cnt: int, py_issues: int, ts_issues: int) -> str:
    lines = ["# Consolidation Audit - Summary", ""]
    lines += [
        f"- Files scanned: {total_files}",
        f"- Exact duplicate groups: {exact_cnt}",
        f"- Near-duplicate groups: {near_cnt}",
        f"- Python import issues: {py_issues}",
        f"- TS/JS relative import issues: {ts_issues}",
        "",
        "## Next Steps",
        "- For exact duplicates: pick a canonical path and delete or redirect duplicates.",
        "- For near-duplicates: review differences; consider refactoring into a shared module.",
        "- For Python import issues: fix module/package layout or adjust import paths.",
        "- For TS/JS issues: fix relative import paths or file locations; consider path aliases if needed.",
    ]
    return "\n".join(lines)


# ---------------------------------- Main ---------------------------------- #


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit monorepo for consolidation readiness")
    p.add_argument("--root", type=str, default=".", help="Root directory to scan")
    p.add_argument("--report-dir", type=str, default="reports/consolidation_audit", help="Directory to write reports")
    p.add_argument(
        "--include-ext",
        type=str,
        default=",".join(sorted(TextExts)),
        help="Comma-separated file extensions to include (e.g. .py,.ts,.js)",
    )
    p.add_argument(
        "--exclude-dirs",
        type=str,
        default=",".join(
            [
                ".git",
                ".venv",
                ".venv-ollama",
                "venv",
                "__pycache__",
                ".mypy_cache",
                ".pytest_cache",
                ".cache",
                "node_modules",
                "dist",
                "build",
                "coverage",
                "lcov-report",
                "htmlcov",
                ".vscode-test",
                "site-packages",
                "dist-info",
                "reports",
                "backups",
                ".idea",
                ".vs",
                "tmp",
                "temp",
            ]
        ),
        help="Comma-separated directory names to exclude anywhere in path",
    )
    p.add_argument("--no-near", action="store_true", help="Disable near-duplicate detection for speed")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"Root not found: {root}", file=sys.stderr)
        return 2

    include_ext = {e.strip().lower() for e in args.include_ext.split(",") if e.strip()}
    exclude_dirs = {e.strip() for e in args.exclude_dirs.split(",") if e.strip()}

    # Collect files
    files = list(walk_files(root, include_ext, exclude_dirs))
    timestamp = now_stamp()
    out_dir = Path(args.report_dir) / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    # Duplicates
    exact, near = scan_duplicates(files, enable_near=(not args.no_near))
    write_json(out_dir / "duplicates.json", exact)
    write_json(out_dir / "near_duplicates.json", near)
    write_md(out_dir / "duplicates.md", md_for_duplicates(exact, near))

    # Python import issues
    py_issues = check_python_imports(root, files)
    write_json(out_dir / "python_import_issues.json", py_issues)
    write_md(out_dir / "python_import_issues.md", md_for_issues("Python Imports", py_issues))

    # TS/JS import issues (relative only)
    ts_issues = check_ts_js_imports(files)
    write_json(out_dir / "ts_import_issues.json", ts_issues)
    write_md(out_dir / "ts_import_issues.md", md_for_issues("TS/JS Relative Imports", ts_issues))

    # Summary
    summary = md_summary(
        total_files=len(files),
        exact_cnt=len(exact),
        near_cnt=len(near),
        py_issues=len(py_issues),
        ts_issues=len(ts_issues),
    )
    write_md(out_dir / "summary.md", summary)

    print("Consolidation audit complete.")
    print(f"Reports written to: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
