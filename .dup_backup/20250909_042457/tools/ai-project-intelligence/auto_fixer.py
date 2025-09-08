#!/usr/bin/env python3
"""
Auto Fixer - Applies safe automatic fixes when possible.

Implements conservative, validated edits using libCST for Python.
TypeScript/JavaScript fixes are currently not applied; issues are logged for future handling.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import libcst as cst
import Exception
import alias
import applied
import bool
import dict
import int
import isinstance
import issue
import issues
import list
import n
import node
import p
import project_root
import self
import set
import stmt
import str
import updated_node


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


@dataclass
class FixResult:
    file_path: Path
    issue_id: str | None
    message: str


class _AddImportIfMissing(cst.CSTTransformer):
    def __init__(self, module: str | None, names: list[str]) -> None:
        self.module = module
        self.names = names
        self.found = False

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        if self.found:
            return updated_node
        # Build import statement
        if self.module:
            import_node = cst.ImportFrom(
                module=cst.Name(self.module) if self.module.isidentifier() else cst.ParseSyntaxError(),
                names=[cst.ImportAlias(cst.Name(n)) for n in self.names],
            )
        else:
            import_node = cst.Import(names=[cst.ImportAlias(cst.Name(n)) for n in self.names])
        # Prepend import at top with a newline
        new_body = [cst.SimpleStatementLine([import_node])] + list(updated_node.body)
        return updated_node.with_changes(body=new_body)

    def visit_Import(self, node: cst.Import) -> bool | None:
        # e.g., import foo, bar
        existing = {alias.name.value for alias in node.names}
        if not self.module and set(self.names).issubset(existing):
            self.found = True
        return None

    def visit_ImportFrom(self, node: cst.ImportFrom) -> bool | None:
        # e.g., from x import y
        try:
            mod = node.module.value if node.module else None
        except Exception:
            mod = None
        if self.module and mod == self.module:
            existing = {alias.name.value for alias in node.names} if isinstance(node.names, list) else set()
            if set(self.names).issubset(existing):
                self.found = True
        return None


class _AppendFunctionStub(cst.CSTTransformer):
    def __init__(self, name: str, params: list[str] | None = None) -> None:
        self.name = name
        self.params = params or []
        self.added = False

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:
        # If already defined, skip
        for stmt in updated_node.body:
            if isinstance(stmt, cst.FunctionDef) and stmt.name.value == self.name:
                return updated_node
        # Build def name(params):
        params = [cst.Param(cst.Name(p)) for p in self.params]
        func = cst.FunctionDef(
            name=cst.Name(self.name),
            params=cst.Parameters(params=params),
            body=cst.IndentedBlock(cst.SimpleStatementLine([cst.Pass()])),
        )
        new_body = list(updated_node.body) + [cst.EmptyLine(), func, cst.EmptyLine()]
        self.added = True
        return updated_node.with_changes(body=new_body)


class SafeAutoFixer:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.backup_dir = project_root / ".ai-backups"
        _ensure_dir(self.backup_dir)

    def fix_issue(self, issue: dict[str, Any]) -> FixResult | None:  # noqa: C901
        """Safely fix an issue with backup and validation. Returns FixResult if changed."""
        file_path = Path(issue.get("file_path", ""))
        if not file_path.is_file():
            return None

        issue_type = issue.get("type")
        if issue_type not in {"missing_import", "missing_function"}:
            # Only safe Python fixes supported for now
            if file_path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
                # Placeholder: not implemented yet for TS/JS
                return None
            return None

        # Backup
        timestamp = int(time.time())
        backup_path = self.backup_dir / f"{file_path.name}.backup.{timestamp}"
        backup_path.write_text(file_path.read_text(encoding="utf-8"), encoding="utf-8")

        # Transform
        try:
            original_code = file_path.read_text(encoding="utf-8")
            module = cst.parse_module(original_code)
            transformer: cst.CSTTransformer

            if issue_type == "missing_import":
                # Expected keys: module (optional), names: list[str]
                module_name = issue.get("module")
                names = issue.get("names") or ([] if issue.get("name") is None else [issue.get("name")])
                if not isinstance(names, list) or not names:
                    return None
                transformer = _AddImportIfMissing(module_name, [str(n) for n in names])
            elif issue_type == "missing_function":
                # Expected keys: name, params (optional list[str])
                name = issue.get("name")
                if not isinstance(name, str) or not name:
                    return None
                params = issue.get("params") or []
                transformer = _AppendFunctionStub(name, [str(p) for p in params])
            else:
                return None

            new_module = module.visit(transformer)
            new_code = new_module.code
            # Validate syntax
            cst.parse_module(new_code)

            if new_code == original_code:
                return None

            file_path.write_text(new_code, encoding="utf-8")
            return FixResult(
                file_path=file_path,
                issue_id=str(issue.get("id")) if issue.get("id") else None,
                message=f"Applied {issue_type}",
            )
        except Exception:
            # On failure, restore backup
            import contextlib

            with contextlib.suppress(Exception):
                file_path.write_text(backup_path.read_text(encoding="utf-8"), encoding="utf-8")
            return None


def apply_fixes(
    project_root: Path,
    issues: list[dict[str, Any]],
    *,
    allowed_issue_types: set[str] | None = None,
) -> list[str]:
    """
    Apply safe fixes for supported issue types.

    Returns list of human-readable fix summaries.
    """
    fixer = SafeAutoFixer(project_root)
    allowed_issue_types = allowed_issue_types or set()
    applied: list[str] = []

    for issue in issues:
        if allowed_issue_types and issue.get("type") not in allowed_issue_types:
            continue
        res = fixer.fix_issue(issue)
        if res:
            summary = f"{res.file_path}: {res.message} (issue_id={res.issue_id})"
            applied.append(summary)

    return applied
