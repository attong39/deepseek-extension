#!/usr/bin/env python3
"""
AI Codemod Engine: Orchestrates analyze → propose → patch workflow.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Protocol, cast
import Exception
import FileNotFoundError
import action_type
import alias
import any
import arg
import bool
import by_file
import config_path
import default_config
import dict
import dry_run
import e
import excluded
import f
import ff
import file_findings
import file_path
import finding
import getattr
import isinstance
import len
import list
import mapping
import n
import next
import node
import object
import open
import path
import print
import r
import result_payload
import results
import root_dir
import self
import str

try:
    import yaml  # type: ignore[import-not-found]
except Exception:  # noqa: BLE001
    yaml = None  # type: ignore[assignment]
from detectors.python_detector import PythonDetector
from detectors.typescript_detector import TypeScriptDetector
from providers.ollama import OllamaProvider
from reporters.markdown_reporter import MarkdownReporter


class AICodemodEngine:
    def __init__(self, root_dir: Path, config_path: Path):
        self.root_dir = root_dir
        self.config: dict[str, object] = self._load_config(config_path)
        self.provider = OllamaProvider(self.config)

        class _Detector(Protocol):
            def analyze(self, file_path: Path) -> list[dict[str, object]]: ...

        self.detectors: dict[str, _Detector] = {
            "python": PythonDetector(),
            "typescript": TypeScriptDetector(),
        }
        self.reporter = MarkdownReporter(root_dir)

    def _load_config(self, config_path: Path) -> dict[str, object]:
        """Load configuration from YAML; if unavailable, return sensible defaults.

        This fallback lets the engine run even if PyYAML is not installed or pip is broken.
        """
        default_config: dict[str, object] = {
            "version": 1,
            "rules": [
                {
                    "language": "python",
                    "allowed_transforms": [
                        "imports",
                        "dead_code",
                        "typing",
                        "pydantic_v2",
                        "fastapi",
                        "logging",
                        "docstrings",
                    ],
                    "max_changes_per_file": 10,
                    "max_files_per_run": 50,
                    "excluded_paths": [
                        "**/migrations/**",
                        "**/generated/**",
                        "**/third_party/**",
                        "**/__pycache__/**",
                        "**/.pytest_cache/**",
                        "**/venv/**",
                        "**/.venv/**",
                        "**/site-packages/**",
                        "**/.tox/**",
                        "**/.mypy_cache/**",
                    ],
                },
                {
                    "language": "typescript",
                    "allowed_transforms": [
                        "imports",
                        "unused",
                        "strict_types",
                        "path_aliases",
                        "dedupe_reexports",
                        "react_props",
                    ],
                    "max_changes_per_file": 10,
                    "max_files_per_run": 50,
                    "excluded_paths": [
                        "**/node_modules/**",
                        "**/dist/**",
                        "**/build/**",
                        "**/coverage/**",
                    ],
                },
            ],
            "general": {
                "dry_run_by_default": True,
                "require_test_pass": True,
                "formatters": {"python": "black", "typescript": "prettier"},
                "model": "deepseek-coder",
                "fallback_model": "codellama:latest",
            },
        }

        try:
            if yaml is None:
                print("Config notice: PyYAML not available; using default AI codemod config.")
                return default_config
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:  # noqa: BLE001
            print(f"Config warning: failed to load {config_path} ({e}); using default config.")
            return default_config

    def analyze(self, files: list[Path] | None = None) -> dict[str, object]:
        """Analyze files and return suggestions."""
        findings: list[dict[str, object]] = []

        # If no files specified, analyze all based on rules
        if not files:
            files = self._find_files_to_analyze()

        for file_path in files:
            lang = self._get_language(file_path)
            if not lang or not self._should_analyze(file_path):
                continue

            # Get detector findings
            detector = self.detectors.get(lang)
            if detector:
                findings.extend(detector.analyze(file_path))

        # Get AI suggestions for non-trivial fixes
        ai_suggestions = self.provider.analyze_findings(findings)
        findings.extend(ai_suggestions)

        # Compose result with simple summary metadata
        total_files = len(files)
        total_findings = len(findings)
        result: dict[str, object] = {
            "findings": findings,
            "total_files": total_files,
            "total_findings": total_findings,
            # For analyze mode, no changes are applied
            "applied_count": 0,
            "dry_run": True,
        }
        self._save_results(result, "analysis")
        return result

    def apply(self, findings: dict[str, object], dry_run: bool = True) -> dict[str, object]:
        """Apply fixes from findings.

        Strategy:
        - Group findings by file
        - For each file: perform safe, local transformations based on finding types
          (currently supports: missing_type_hints for Python)
        - When dry_run=True, report intent without changing files
        """
        results: list[dict[str, object]] = []
        applied_count = 0

        # Group findings by file for efficient per-file edits
        by_file: dict[str, list[dict[str, object]]] = {}
        for f in cast(list[dict[str, object]], findings.get("findings", [])):
            if not self._can_apply_finding(f):
                continue
            fp = str(f.get("file_path", ""))
            if not fp:
                continue
            by_file.setdefault(fp, []).append(f)

        for file_path, file_findings in by_file.items():
            lang = self._get_language(Path(file_path))
            if lang == "python":
                has_typing = any(ff.get("type") == "missing_type_hints" for ff in file_findings)
                if has_typing:
                    if dry_run:
                        results.append({
                            "file_path": file_path,
                            "applied": False,
                            "transform": "typing",
                            "detail": "Would add Any annotations for missing type hints",
                        })
                    else:
                        applied = self._apply_python_add_missing_type_hints(Path(file_path))
                        results.append({
                            "file_path": file_path,
                            "applied": applied,
                            "transform": "typing",
                            "detail": "Added Any annotations for missing type hints" if applied else "No changes applied",
                        })
                        if applied:
                            applied_count += 1
            else:
                # Placeholder for other languages/transform types
                for ff in file_findings:
                    results.append({
                        "file_path": file_path,
                        "applied": False,
                        "detail": ff.get("description"),
                        "transform": str(ff.get("type")),
                    })

        # Run formatters if changes were applied
        if applied_count > 0 and not dry_run:
            self._run_formatters()

        result_payload: dict[str, object] = {
            "results": results,
            "applied_count": applied_count,
            "dry_run": dry_run,
        }
        self._save_results(result_payload, "application")
        return result_payload

    def verify(self) -> bool:
        """Verify changes don't break tests."""
        try:
            # Run linters and tests
            subprocess.run(["npm", "run", "check:all"], check=True, cwd=self.root_dir)
            return True
        except subprocess.CalledProcessError:
            return False

    def _find_files_to_analyze(self) -> list[Path]:
        # Simple heuristic: scan repo for relevant extensions, skip excluded
        files: list[Path] = []
        for path in self.root_dir.rglob("*"):
            if path.is_file() and self._get_language(path) and self._should_analyze(path):
                files.append(path)
        return files

    def _get_language(self, file_path: Path) -> str | None:
        ext = file_path.suffix
        if ext in [".py"]:
            return "python"
        if ext in [".ts", ".tsx", ".js", ".jsx"]:
            return "typescript"
        return None

    def _should_analyze(self, file_path: Path) -> bool:
        # Check against excluded paths in config (OS-agnostic)
        from pathlib import PurePosixPath

        rel_path = file_path.resolve().relative_to(self.root_dir.resolve())
        rel_str = str(rel_path).replace("\\", "/")

        # Quick guard for common heavy folders
        if rel_str.startswith("venv/") or rel_str.startswith(".venv/") or rel_str.startswith("node_modules/"):
            return False

        rules = cast(list[dict[str, object]], self.config.get("rules", []))
        for rule in rules:
            if rule.get("language") == self._get_language(file_path):
                for excluded in cast(list[str], rule.get("excluded_paths", [])):
                    if PurePosixPath(rel_str).match(excluded):
                        return False
        return True

    def _can_apply_finding(self, finding: dict[str, object]) -> bool:
        lang = finding.get("language") or self._get_language(Path(str(finding.get("file_path", ""))))
        if not lang:
            return False
        rules = cast(list[dict[str, object]], self.config.get("rules", []))
        rule = next((r for r in rules if r.get("language") == lang), None)
        if not rule:
            return False
        ftype = str(finding.get("type", ""))
        # Map finding types to allowed transforms
        mapping: dict[str, str | None] = {
            "unused_imports": "imports",
            "missing_type_hints": "typing",
            "dead_code": "dead_code",
            "ai_suggestion": None,  # allow but validate separately
        }
        transform = mapping.get(ftype)
        if transform is None:
            return ftype == "ai_suggestion"
        return transform in cast(list[str], rule.get("allowed_transforms", []))

    def _apply_finding(self, finding: dict[str, object], dry_run: bool) -> dict[str, object]:
        # For now, only attach AI diffs; actual patch apply can be added later
        _ = dry_run  # referenced to satisfy linters until real apply logic is added
        return {
            "file_path": finding.get("file_path"),
            "applied": False,
            "detail": finding.get("description"),
            "diff": finding.get("diff"),
        }

    def _apply_python_add_missing_type_hints(self, file_path: Path) -> bool:
        """Annotate missing param and return types with Any, add import if needed.

        Returns True if file content changed.
        """
        import ast
        from typing import Any as _Any  # noqa: F401  # used for type name consistency

        try:
            src = file_path.read_text(encoding="utf-8")
        except Exception:
            return False

        try:
            tree = ast.parse(src)
        except Exception:
            return False

        changed = False

        class Annotator(ast.NodeTransformer):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:  # noqa: N802
                nonlocal changed
                # params
                all_args = (
                    list(node.args.args)
                    + list(getattr(node.args, "posonlyargs", []))
                    + list(node.args.kwonlyargs)
                )
                for arg in all_args:
                    if arg.annotation is None:
                        arg.annotation = ast.Name(id="Any", ctx=ast.Load())
                        changed = True
                if node.args.vararg and node.args.vararg.annotation is None:
                    node.args.vararg.annotation = ast.Name(id="Any", ctx=ast.Load())
                    changed = True
                if node.args.kwarg and node.args.kwarg.annotation is None:
                    node.args.kwarg.annotation = ast.Name(id="Any", ctx=ast.Load())
                    changed = True
                # return
                if node.returns is None:
                    node.returns = ast.Name(id="Any", ctx=ast.Load())
                    changed = True
                return self.generic_visit(node)

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:  # noqa: N802
                return self.visit_FunctionDef(node)  # type: ignore[arg-type]

        annotator = Annotator()
        new_tree = annotator.visit(tree)
        if not changed:
            return False

        # Ensure import from typing import Any exists
        has_any_import = False
        for n in ast.walk(new_tree):
            if (
                isinstance(n, ast.ImportFrom)
                and n.module == "typing"
                and any(alias.name == "Any" for alias in n.names)
            ):
                has_any_import = True
                break
        # Generate updated source
        try:
            new_code = ast.unparse(new_tree)  # type: ignore[attr-defined]
        except Exception:
            # Fallback: if ast.unparse not available, skip applying
            return False

        if not has_any_import:
            # Insert import near top, after shebang/encoding/comments and future imports
            lines = new_code.splitlines()
            insert_at = 0
            # skip shebang/encoding and docstring module (roughly)
            while insert_at < len(lines) and (
                lines[insert_at].startswith(("#", "\ufeff"))
                or lines[insert_at].strip() == ""
            ):
                insert_at += 1
            # keep future imports at top
            while insert_at < len(lines) and lines[insert_at].startswith("from __future__ import"):
                insert_at += 1
            lines.insert(insert_at, "from typing import Any")
            new_code = "\n".join(lines) + ("\n" if not new_code.endswith("\n") else "")

        if new_code != src:
            try:
                file_path.write_text(new_code, encoding="utf-8")
                return True
            except Exception:
                return False
        return False

    def _run_formatters(self) -> None:
        """Run formatters based on config, cross-platform compatible."""
        # Access formatters config safely
        general = cast(dict[str, object], self.config.get("general", {}))
        formatters = cast(dict[str, object], general.get("formatters", {}))

        try:
            # Python: Black
            if "python" in formatters and cast(str, formatters.get("python")) == "black":
                print("Running Black formatter...")
                subprocess.run(
                    [sys.executable, "-m", "black", "."],
                    cwd=self.root_dir,
                    timeout=300,
                    check=False,
                )

            # TypeScript: Prettier via npx
            if "typescript" in formatters and cast(str, formatters.get("typescript")) == "prettier":
                print("Running Prettier formatter...")
                subprocess.run(
                    ["npx", "prettier", "--write", "."],
                    cwd=self.root_dir,
                    timeout=300,
                    check=False,
                )

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"Formatter warning: {e}")
            # Continue execution even if formatters fail

    def _save_results(self, results: dict[str, object], action_type: str) -> None:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.root_dir / "reports" / "ai-codemod"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{action_type}_{timestamp}.json"
        output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

        latest_path = output_dir / "latest.json"
        try:
            if latest_path.exists():
                latest_path.unlink()
        except Exception:
            pass
        latest_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Codemod Engine")
    parser.add_argument("--mode", choices=["analyze", "apply", "verify"], required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("tools/ai-codemod/ai-rules.yml"))
    # Support --dry-run / --no-dry-run for explicit control (default True)
    try:
        bool_action = argparse.BooleanOptionalAction
    except Exception:  # pragma: no cover - fallback for very old Python
        # Fallback shim: accept --dry-run to set True; lack of flag means default
        bool_action = None

    if bool_action is not None:
        parser.add_argument("--dry-run", action=bool_action, default=True)
    else:
        parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--files", nargs="+", type=Path)

    args = parser.parse_args()

    engine = AICodemodEngine(args.root, args.config)

    if args.mode == "analyze":
        result = engine.analyze(args.files)
        print(json.dumps(result, indent=2))
    elif args.mode == "apply":
        findings = engine.analyze(args.files)
        result = engine.apply(findings, args.dry_run)
        print(json.dumps(result, indent=2))
    elif args.mode == "verify":
        success = engine.verify()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
