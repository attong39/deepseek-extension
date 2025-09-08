#!/usr/bin/env python3
"""
AI Project Analyzer - Core analysis engine for understanding project structure
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
from pathlib import Path
from typing import Any
import Exception
import ValueError
import any
import bool
import cfg_path
import dep
import dep_graph_json
import dependency
import deps
import dict
import e
import exports
import ext
import file_path
import files
import getattr
import isinstance
import k
import len
import list
import m
import metadata
import name
import node
import path
import pattern
import print
import root_path
import self
import set
import sorted
import source_file
import str
import sum

try:
    import yaml
except Exception:
    yaml = None

try:
    import libcst as cst
except Exception:
    cst = None


def load_config(cfg_path: Path) -> dict[str, Any]:
    if yaml is None:
        return {}
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8"))


class ProjectAnalyzer:
    def __init__(self, root_path: Path, config: dict[str, Any] | None = None):
        self.root_path = root_path
        self.config = config or {}
        # Analysis accumulators
        self.dependency_graph: dict[str, set[str]] = {}
        self.file_metadata: dict[str, dict[str, Any]] = {}

    def analyze_project(self) -> dict[str, Any]:
        source_files = self._find_source_files()
        for file_path in source_files:
            self._analyze_file(file_path)
        self._build_dependency_graph()
        # Ensure JSON-serializable output (convert sets to sorted lists)
        dep_graph_json: dict[str, list[str]] = {k: sorted(v) for k, v in self.dependency_graph.items()}
        return {
            "dependency_graph": dep_graph_json,
            "file_metadata": self.file_metadata,
            "summary": self._generate_summary(),
        }

    def _find_source_files(self) -> list[Path]:
        include_exts = set(
            self.config.get("analysis", {}).get("include_extensions", [".py", ".ts", ".tsx", ".js", ".jsx"])
        )
        files: list[Path] = []
        for path in self.root_path.rglob("*"):
            if path.is_file() and path.suffix in include_exts and not self._is_excluded(path):
                files.append(path)
        return files

    def _is_excluded(self, file_path: Path) -> bool:
        """Return True if file_path matches any exclude pattern.

        Uses a robust fnmatch on a path relative to the configured root to
        ensure Windows paths and dot-directories (like .venv) are excluded.
        """
        excluded_patterns = self.config.get("analysis", {}).get(
            "exclude_patterns",
            [
                "**/node_modules/**",
                "**/dist/**",
                "**/build/**",
                "**/__pycache__/**",
                "**/.git/**",
                "**/.venv/**",
                "**/venv/**",
                "**/.*/**",  # any dot-directory
            ],
        )
        try:
            rel = file_path.relative_to(self.root_path).as_posix()
        except ValueError:
            # Fallback to posix full path if not under root
            rel = file_path.as_posix()
        # Normalize by ensuring directories end with a slash where applicable
        candidate = rel if not file_path.is_dir() else (rel.rstrip("/") + "/")
        return any(fnmatch.fnmatch(candidate, pattern) for pattern in excluded_patterns)

    def _analyze_file(self, file_path: Path) -> None:
        try:
            if file_path.suffix == ".py":
                self._analyze_python_file(file_path)
            elif file_path.suffix in [".ts", ".tsx", ".js", ".jsx"]:
                self._analyze_ts_file(file_path)
        except Exception as e:  # noqa: BLE001
            print(f"Warning: error analyzing {file_path}: {e}")

    def _analyze_python_file(self, file_path: Path) -> None:
        content = file_path.read_text(encoding="utf-8")
        imports: set[str] = set()
        dependencies: set[str] = set()
        classes: list[str] = []
        functions: list[str] = []
        if cst is not None:
            try:
                module = cst.parse_module(content)

                class Visitor(cst.CSTVisitor):
                    def __init__(self) -> None:
                        self.imports: set[str] = set()
                        self.dependencies: set[str] = set()
                        self.classes: list[str] = []
                        self.functions: list[str] = []

                    def visit_Import(self, node: cst.Import) -> None:
                        for name in node.names:
                            val = getattr(getattr(name, "name", None), "value", None)
                            if isinstance(val, str):
                                self.imports.add(val)

                    def visit_ImportFrom(self, node: cst.ImportFrom) -> None:
                        if node.module is not None:
                            mod_val = getattr(node.module, "value", None)
                            if isinstance(mod_val, str):
                                self.imports.add(mod_val)
                                if mod_val.startswith("."):
                                    self.dependencies.add(mod_val)

                    def visit_ClassDef(self, node: cst.ClassDef) -> None:
                        name_val = getattr(node.name, "value", None)
                        if isinstance(name_val, str):
                            self.classes.append(name_val)

                    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
                        name_val = getattr(node.name, "value", None)
                        if isinstance(name_val, str):
                            self.functions.append(name_val)

                v = Visitor()
                module.visit(v)
                imports = v.imports
                dependencies = v.dependencies
                classes = v.classes
                functions = v.functions
            except Exception as e:  # noqa: BLE001
                print(f"Warning: libcst parse error for {file_path}: {e}")
        else:
            # Fallback: regex-based import extraction
            for m in re.finditer(r"^\s*import\s+([\w\.]+)", content, re.MULTILINE):
                imports.add(m.group(1))
            for m in re.finditer(r"^\s*from\s+([\w\.]+)\s+import", content, re.MULTILINE):
                mod = m.group(1)
                imports.add(mod)
                if mod.startswith("."):
                    dependencies.add(mod)

        self.file_metadata[str(file_path)] = {
            "type": "python",
            "imports": sorted(imports),
            "exports": [],
            "dependencies": sorted(dependencies),
            "classes": classes,
            "functions": functions,
        }

    def _analyze_ts_file(self, file_path: Path) -> None:
        content = file_path.read_text(encoding="utf-8")
        imports: set[str] = set()
        exports: set[str] = set()
        dependencies: set[str] = set()
        # Simple regex-based scan for imports/exports
        for m in re.finditer(r"""import\s+.*?from\s+['"]([^'"]+)['"]""", content):
            spec = m.group(1)
            imports.add(spec)
            if spec.startswith("."):
                dependencies.add(spec)
        for m in re.finditer(r"""export\s+\*\s+from\s+['"]([^'"]+)['"]""", content):
            exports.add(m.group(1))
        self.file_metadata[str(file_path)] = {
            "type": "typescript",
            "imports": sorted(imports),
            "exports": sorted(exports),
            "dependencies": sorted(dependencies),
            "classes": [],
            "functions": [],
        }

    def _build_dependency_graph(self) -> None:
        for file_path, metadata in self.file_metadata.items():
            self.dependency_graph[file_path] = set()
            for dep in metadata.get("dependencies", []):
                abs_dep = self._resolve_dependency(Path(file_path), dep)
                if abs_dep:
                    self.dependency_graph[file_path].add(str(abs_dep))

    def _resolve_dependency(self, source_file: Path, dependency: str) -> Path | None:
        if dependency.startswith("."):
            base = source_file.parent / dependency
            # Try common TS/JS/PY extensions
            for ext in (".ts", ".tsx", ".js", ".jsx", ".py"):
                candidate = base.with_suffix(ext)
                if candidate.exists():
                    return candidate
            # Index files
            for ext in (".ts", ".tsx", ".js", ".jsx", ".py"):
                candidate = base / ("index" + ext)
                if candidate.exists():
                    return candidate
        return None

    def _generate_summary(self) -> dict[str, Any]:
        total_files = len(self.file_metadata)
        python_files = sum(1 for m in self.file_metadata.values() if m.get("type") == "python")
        ts_files = sum(1 for m in self.file_metadata.values() if m.get("type") == "typescript")
        return {
            "total_files": total_files,
            "python_files": python_files,
            "typescript_files": ts_files,
            "total_dependencies": sum(len(deps) for deps in self.dependency_graph.values()),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Project Analyzer")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("tools/ai-project-analyzer/config.yml"))
    parser.add_argument("--out", type=Path, default=Path("tools/ai-project-analyzer/out/analysis.json"))
    args = parser.parse_args()

    config = load_config(args.config) if args.config.exists() else {}
    analyzer = ProjectAnalyzer(args.root, config)
    results = analyzer.analyze_project()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Analysis written to {args.out}")


if __name__ == "__main__":
    main()
