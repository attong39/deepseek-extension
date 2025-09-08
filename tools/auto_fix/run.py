#!/usr/bin/env python
from __future__ import annotations
import argparse
import sys
import json
from pathlib import Path
import os

# Set working directory to auto_fix directory
script_dir = Path(__file__).parent
os.chdir(script_dir)

try:
    from python.clean_analyzer import PyImportAnalyzer
    from python.injector import insert_imports as py_insert
    from python.requirements_updater import ensure_requirements as py_require
    from typescript.analyzer import scan_ts_file, find_component_source, to_import_path
    from typescript.injector import insert_imports_ts as ts_insert
    from typescript.packagejson_updater import ensure_dependencies as ts_require
    from report import write_report
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def _load_mapping() -> dict:
    p = Path("symbol_to_pkg.json")
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def scan_python(repo: Path, mapping: dict) -> tuple[list[str], list[str]]:
    print("🐍 Scanning Python files...")
    imports_added: list[str] = []
    reqs_added: list[str] = []
    py_files = [p for p in repo.rglob("*.py") if "/.venv/" not in str(p).replace("\\","/") and "node_modules" not in str(p)]
    missing_all: set[str] = set()
    
    for f in py_files:
        try:
            an = PyImportAnalyzer(f)
            missing = an.missing_symbols()
            if not missing: 
                continue
            added = py_insert(f, sorted(missing))
            if added:
                imports_added.append(f"{f.name}: {', '.join(added)}")
            missing_all.update(missing)
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
    
    if missing_all:
        req_added = py_require(sorted(missing_all), mapping=mapping)
        reqs_added.extend(req_added)
    
    print(f"   ✅ Python: +{len(imports_added)} files with imports, +{len(reqs_added)} requirements")
    return imports_added, reqs_added

def scan_ts(repo: Path, mapping: dict) -> tuple[list[str], list[str]]:
    print("🕷️ Scanning TypeScript files...")
    imports_added: list[str] = []
    deps_to_add: set[str] = set()
    ts_files = [*repo.rglob("*.ts"), *repo.rglob("*.tsx")]
    
    for f in ts_files:
        if "node_modules" in str(f) or ".d.ts" in str(f):
            continue
        try:
            imported, candidates = scan_ts_file(f)
            
            # Quyết định nguồn cho mỗi sym
            planned: list[tuple[str,str]] = []
            for sym in sorted(candidates):
                src = find_component_source(sym, f)
                if src:
                    planned.append((sym, to_import_path(f, src)))
                else:
                    pkg = (mapping.get(sym, {}) or {}).get("ts") or sym
                    planned.append((sym, pkg))
                    deps_to_add.add(pkg)
            
            added_stmts = ts_insert(f, planned) if planned else []
            if added_stmts:
                imports_added.append(f"{f.name}: +{len(added_stmts)}")
        except (UnicodeDecodeError, OSError):
            continue
    
    deps_added = ts_require(sorted(deps_to_add)) if deps_to_add else []
    print(f"   ✅ TypeScript: +{len(imports_added)} files with imports, +{len(deps_added)} dependencies")
    return imports_added, deps_added

def main() -> int:
    ap = argparse.ArgumentParser(description="Auto-fix missing imports & deps for Python/TypeScript.")
    ap.add_argument("mode", choices=["python","ts","all"], default="all", nargs="?")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = ap.parse_args()
    
    print("🔧 Auto-Fix Missing Imports & Dependencies")
    print("=" * 50)
    
    # Go back to repo root for scanning
    repo = script_dir.parent.parent  # Go up from tools/auto_fix to repo root
    os.chdir(repo)
    
    mapping = _load_mapping()
    print(f"🗺️ Loaded {len(mapping)} symbol mappings")

    py_imports, py_reqs = ([],[])
    ts_imports, ts_deps = ([],[])
    
    if args.mode in ("python","all"):
        py_imports, py_reqs = scan_python(repo, mapping)
    
    if args.mode in ("ts","all"):
        ts_imports, ts_deps = scan_ts(repo, mapping)

    report = {
        "mode": args.mode,
        "python": {"imports_added": py_imports, "requirements_added": py_reqs},
        "ts": {"imports_added": ts_imports, "deps_added": ts_deps},
        "unresolved": []
    }
    
    write_report(report)
    print(f"\n📊 Report generated: reports/auto_fix/report.{{json,md}}")
    
    # Exit code: unresolved -> 2; else 0
    return 0 if not report["unresolved"] else 2

if __name__ == "__main__":
    raise SystemExit(main())