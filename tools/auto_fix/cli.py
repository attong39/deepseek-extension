#!/usr/bin/env python
from __future__ import annotations
import argparse
import json
import subprocess
import shutil
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from git_changed import staged_or_diff
from python.analyzer import PyImportAnalyzer
from python.injector import insert_imports as py_insert
from python.requirements_updater import ensure_requirements as py_require
try:
    from python.pyproject_updater import ensure_pyproject_deps
except ImportError:
    ensure_pyproject_deps = None
from typescript.analyzer import scan_ts_file, find_component_source, to_import_path
from typescript.injector import insert_imports_ts as ts_insert
from typescript.ts_paths import TSPaths
from typescript.packagejson_updater import ensure_dependencies as ts_require
from report import write_report
from cache import load_cache, save_cache, is_stale, mark_fresh

def _load_json(path: str):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

def _run(cmd: list[str]) -> int:
    try:
        return subprocess.run(cmd, check=False).returncode
    except FileNotFoundError:
        return 127

def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-fix missing imports & deps (Python/TS).")
    ap.add_argument("mode", choices=["python","ts","all"])
    ap.add_argument("--changed-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pkg-json", default="package.json")
    ap.add_argument("--tsconfig", default="apps/desktop/tsconfig.json")
    ap.add_argument("--use-pyproject", action="store_true")
    ap.add_argument("--use-cache", action="store_true", help="Bỏ qua file không đổi (mtime/size/hash)")
    ap.add_argument("--lint-fix", action="store_true", help="Chạy ruff/eslint --fix sau auto-fix (nếu có)")
    args = ap.parse_args()

    repo = Path(".")
    allow = set(_load_json("tools/auto_fix/policies/allowlist.json") or [])
    deny  = set(_load_json("tools/auto_fix/policies/denylist.json") or [])
    mapping = _load_json("tools/auto_fix/symbol_to_pkg.json") or {}

    changed = staged_or_diff() if args.changed_only else None
    cache = load_cache() if args.use_cache else {}

    # ---------- Python ----------
    py_imports: list[str] = []; py_reqs: list[str] = []
    if args.mode in ("python","all"):
        targets = [p for p in repo.rglob("*.py")
                   if (not changed or p in changed)
                   and (not args.use_cache or is_stale(p, cache))]
        miss_all: set[str] = set()
        for f in targets:
            try:
                an = PyImportAnalyzer(f)
            except SyntaxError:
                mark_fresh(f, cache); continue
            miss = an.missing_symbols()
            if miss and not args.dry_run:
                added = py_insert(f, sorted(miss))
                if added: py_imports.append(f"{f}: {', '.join(added)}")
            if miss: miss_all.update(miss)
            mark_fresh(f, cache)
        if miss_all:
            from importlib.metadata import packages_distributions
            mod2dist = {m:(d[0] if d else m) for m,d in packages_distributions().items()}
            dists: list[str] = []
            for m in sorted(miss_all):
                cand = mod2dist.get(m) or (mapping.get(m, {}) or {}).get("python") or m
                if (allow and cand not in allow) or cand in deny:
                    continue
                dists.append(cand)
            if not args.dry_run:
                if args.use_pyproject and Path("pyproject.toml").exists():
                    py_reqs = ensure_pyproject_deps(dists)
                else:
                    py_reqs = py_require(dists)  # type: ignore

    # ---------- TypeScript ----------
    ts_imports: list[str] = []; ts_deps: list[str] = []
    if args.mode in ("ts","all"):
        ts_paths = TSPaths(Path(args.tsconfig))
        targets = [*repo.rglob("*.ts"), *repo.rglob("*.tsx")]
        if changed:
            targets = [p for p in targets if p in changed]
        if args.use_cache:
            targets = [p for p in targets if is_stale(p, cache)]
        deps_to_add: set[str] = set()
        for f in targets:
            imported, candidates = scan_ts_file(f)
            plan: list[tuple[str,str]] = []
            for sym in sorted(candidates):
                alias = ts_paths.resolve(sym)
                if alias:
                    plan.append((sym, alias)); continue
                src = find_component_source(sym, f)
                if src:
                    plan.append((sym, to_import_path(f, src)))
                else:
                    pkg = (mapping.get(sym, {}) or {}).get("ts") or sym
                    if (allow and pkg not in allow) or pkg in deny:
                        continue
                    plan.append((sym, pkg)); deps_to_add.add(pkg)
            if plan and not args.dry_run:
                added = ts_insert(f, plan)
                if added: ts_imports.append(f"{f}: +{len(added)}")
            mark_fresh(f, cache)
        if deps_to_add and not args.dry_run:
            ts_deps = ts_require(sorted(deps_to_add), Path(args.pkg_json))

    # lưu cache
    if args.use_cache:
        save_cache(cache)

    report = {
        "python": {"imports_added": py_imports, "requirements_added": py_reqs},
        "ts": {"imports_added": ts_imports, "deps_added": ts_deps},
        "unresolved": []
    }
    write_report(report)
    # Lint-fix (tuỳ chọn)
    if not args.dry_run and args.lint_fix:
        _run(["uv","run","ruff","check","--fix","."])
        # eslint/tsx (không ép buộc)
        if shutil.which("pnpm"):
            _run(["pnpm","-C","apps/desktop","eslint","--ext",".ts,.tsx","--fix","."])
        else:
            _run(["npx","--yes","eslint","--ext",".ts,.tsx","--fix","apps/desktop/src"])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
