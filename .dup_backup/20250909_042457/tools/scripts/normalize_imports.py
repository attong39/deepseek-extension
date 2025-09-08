#!/usr/bin/env python3
"""
Normalize imports to canonical modules across the repo using LibCST.
- Converts relative imports to absolute under 'zeta_vn'
- Rewrites duplicates per tools/refactor/import_map.json
- Supports --mode check|write and prints a concise report
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import Exception
import alias
import any
import bool
import changed_files
import d
import dict
import e
import err
import f
import file_mod
import fp
import getattr
import int
import isinstance
import issues
import k
import len
import list
import map_path
import mapping
import module
import name
import new_aliases
import p
import print
import py_path
import reversed
import root
import seg
import self
import staticmethod
import str
import tuple
import updated
import x

"""Normalize imports to canonical modules across the repo using LibCST.
- Converts relative imports to absolute under 'zeta_vn'
- Canonicalizes first-party roots (app/core/data/config/infrastructure) to zeta_vn.*
- Rewrites duplicates per tools/refactor/import_map.json
- Supports --mode check|write and prints a concise report"""

import argparse
import json
import sys
from pathlib import Path

import libcst as cst

ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = "zeta_vn"
SRC_ROOT = ROOT / PKG_ROOT
FIRST_PARTY_ROOTS = ("app", "core", "data", "config", "infrastructure")


def load_map(map_path: Path) -> tuple[dict[str, str], dict]:
    data = json.loads(map_path.read_text(encoding="utf-8"))
    opts = data.pop("_options", {})
    return data, opts


def dotted_from_path(py_path: Path) -> str:
    rel = py_path.relative_to(ROOT).with_suffix("")
    return ".".join(rel.parts)


def to_abs(module: str, file_mod: str) -> str:
    # Already absolute or empty
    if not module or module.startswith(PKG_ROOT + "."):
        return module
    # Leading dots -> resolve relative to file's package
    if module.startswith("."):
        dots = len(module) - len(module.lstrip("."))
        base = file_mod.split(".")
        parent = base[:-dots] if dots <= len(base) else []
        rest = module.lstrip(".")
        return ".".join([*parent, rest]).rstrip(".")
    # First-party short roots -> prefix with zeta_vn.
    for root in FIRST_PARTY_ROOTS:
        if module == root or module.startswith(root + "."):
            return f"{PKG_ROOT}.{module}"
    return module


class ImportTransformer(cst.CSTTransformer):
    def __init__(self, file_mod: str, mapping: dict[str, str]):
        self.file_mod = file_mod
        self.mapping = mapping
        self.changed = False

    def _rewrite_name(self, name: str) -> str:
        # Exact or prefix mapping
        if name in self.mapping:
            self.changed = True
            return self.mapping[name]
        best: str | None = None
        for k in self.mapping.keys():
            if name == k or name.startswith(k + "."):
                if best is None or len(k) > len(best):
                    best = k
        if best:
            self.changed = True
            return self.mapping[best] + name[len(best) :]
        return name

    @staticmethod
    def _expr_to_dotted(expr: cst.BaseExpression) -> str:
        if isinstance(expr, cst.Name):
            return expr.value
        if isinstance(expr, cst.Attribute):
            parts: list[str] = []
            cur: cst.BaseExpression = expr
            while isinstance(cur, cst.Attribute):
                parts.append(cur.attr.value)
                cur = cur.value
            if isinstance(cur, cst.Name):
                parts.append(cur.value)
            return ".".join(reversed(parts))
        return cst.Module([]).code_for_node(expr).strip()

    @staticmethod
    def _dotted_to_expr(d: str) -> cst.BaseExpression:
        parts = d.split(".")
        expr: cst.BaseExpression = cst.Name(parts[0])
        for p in parts[1:]:
            expr = cst.Attribute(value=expr, attr=cst.Name(p))
        return expr

    def leave_Import(self, _node: cst.Import, updated: cst.Import) -> cst.Import:  # noqa: N802
        try:
            names = list(updated.names) if getattr(updated, "names", None) else []
            if not names:
                return updated
            new_aliases: list[cst.ImportAlias] = []
            for alias in names:
                dotted = self._expr_to_dotted(alias.name)
                abs_name = to_abs(dotted, self.file_mod)
                new_name = self._rewrite_name(abs_name)
                new_aliases.append(alias.with_changes(name=self._dotted_to_expr(new_name)))
            if tuple(new_aliases) != tuple(names):
                self.changed = True
            return updated.with_changes(names=tuple(new_aliases))
        except Exception:
            # Defensive: if any unexpected CST shape, leave import unchanged
            return updated

    def leave_ImportFrom(self, _node: cst.ImportFrom, updated: cst.ImportFrom) -> cst.ImportFrom:  # noqa: N802
        try:
            if updated.module is None:
                return updated
            dotted = self._expr_to_dotted(updated.module)
            rel = updated.relative
            rel_count = 0
            if rel is None:
                rel_count = 0
            elif isinstance(rel, int):
                rel_count = rel
            else:
                try:
                    rel_count = len(rel)  # type: ignore[arg-type]
                except Exception:
                    rel_count = 0
            rel_prefix = "." * rel_count
            abs_mod = to_abs((rel_prefix + dotted) if rel_prefix else dotted, self.file_mod)
            new_mod = self._rewrite_name(abs_mod)
            self.changed = True if (new_mod != dotted or rel_count) else self.changed
            return updated.with_changes(module=self._dotted_to_expr(new_mod), relative=None)
        except Exception:
            # Defensive: if any unexpected CST shape, leave import unchanged
            return updated


def should_skip(p: Path, allow_rel_tests: bool) -> bool:
    s = str(p).replace("\\", "/")
    if allow_rel_tests and "/zeta_vn/tests/" in s:
        return True
    if any(
        seg in s
        for seg in (
            "/.venv/",
            "/venv/",
            "/.git/",
            "/reports/coverage_html/",
            "/zeta_ai_server.egg-info/",
            "/.copilot/templates/",
            "/zeta_vn/core/services/memory_manager_service.py",
            "/zeta_vn/app/ai/rag/pipeline.py",
            "/zeta_vn/core/services/memory/_manager_core.py",
        )
    ):
        return True
    return not s.endswith(".py")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, help="tools/refactor/import_map.json")
    ap.add_argument("--mode", choices=["check", "write"], default="check")
    args = ap.parse_args()

    mapping, opts = load_map(Path(args.plan))
    allow_rel_tests = bool(opts.get("allow_relative_tests", False))

    targets = [p for p in SRC_ROOT.rglob("*.py") if not should_skip(p, allow_rel_tests)]
    changed_files: list[str] = []
    issues: list[tuple[str, str]] = []

    for fp in targets:
        code = fp.read_bytes().decode("utf-8", errors="replace")
        mod_name = dotted_from_path(fp)
        try:
            tree = cst.parse_module(code)
            tr = ImportTransformer(mod_name, mapping)
            new = tree.visit(tr)
            if tr.changed:
                if args.mode == "write":
                    fp.write_text(new.code, encoding="utf-8")
                changed_files.append(str(fp.relative_to(ROOT)))
        except Exception as e:  # pragma: no cover
            issues.append((str(fp), str(e)))

    print(f"[normalize_imports] changed: {len(changed_files)} files")
    if changed_files:
        for x in changed_files[:30]:
            print("  -", x)
        if len(changed_files) > 30:
            print("  ...")

    if issues:
        print(f"[normalize_imports] parse errors: {len(issues)}")
        for f, err in issues[:20]:
            print("  -", f, "->", err)

    if args.mode == "check" and (changed_files or issues):
        sys.exit(1)


if __name__ == "__main__":
    main()
