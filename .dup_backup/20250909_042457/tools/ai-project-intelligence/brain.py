#!/usr/bin/env python3
import Exception
import ImportError
import any
import dict
import e
import file_path
import files
import len
import list
import path
import print
import project_root
import seg
import self
import set
import str
import sum
import v
# pyright: reportMissingImports=false
"""
AI Brain - Core intelligence that understands project structure and relationships,
with an optional optimization pipeline.
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

yaml: Any
try:
    yaml = importlib.import_module("yaml")
except Exception:  # pragma: no cover
    yaml = None


def _load_kg_module() -> Any:
    mod_path = Path(__file__).with_name("knowledge-graph.py")
    spec = importlib.util.spec_from_file_location("knowledge_graph", str(mod_path))
    if not spec or not spec.loader:
        raise ImportError("Unable to load knowledge-graph module")
    module = importlib.util.module_from_spec(spec)
    # Ensure the module is discoverable by name during execution (needed for dataclasses/type lookups)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# Dynamically loaded classes from knowledge-graph
_kg_module = _load_kg_module()
KnowledgeGraph = _kg_module.KnowledgeGraph
Entity = _kg_module.Entity
EntityType = _kg_module.EntityType


class AIBrain:
    def __init__(self, project_root: Path, cfg: dict[str, Any] | None = None) -> None:
        self.project_root = project_root
        self.cfg = cfg or {}
        storage = self.cfg.get("knowledge_graph", {}).get("storage_path")
        storage_path = Path(storage) if storage else None
        self.kg = KnowledgeGraph(storage_path=storage_path)
        self.last_analysis_time = 0.0

    def understand_project(self) -> dict[str, Any]:
        self._build_knowledge_graph()
        self._analyze_patterns()
        ts = time.time()
        self.last_analysis_time = ts
        summary: dict[str, Any] = {
            "entities": len(self.kg.entities),
            "relationships": sum(len(v) for v in self.kg.relationships.values()),
            "timestamp": ts,
        }
        if self.cfg.get("knowledge_graph", {}).get("persist", True):
            self.kg.persist()
        return summary

    def _build_knowledge_graph(self) -> None:
        for path in self._find_source_files():
            try:
                if path.suffix == ".py":
                    self._analyze_python_file(path)
                elif path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
                    self._analyze_ts_file(path)
            except Exception as e:  # noqa: BLE001
                print(f"Warning: analysis error for {path}: {e}")

    def _find_source_files(self) -> list[Path]:
        include_exts = {".py", ".ts", ".tsx", ".js", ".jsx"}
        excluded = {"node_modules", "dist", "build", "__pycache__", ".git"}
        files: list[Path] = []
        for p in self.project_root.rglob("*"):
            if p.is_file() and p.suffix in include_exts and not any(seg in excluded for seg in p.parts):
                files.append(p)
        return files

    def _analyze_python_file(self, file_path: Path) -> None:
        content = file_path.read_text(encoding="utf-8")
        name = file_path.stem
        ent = Entity(
            id=f"py:{file_path}",
            name=name,
            type=EntityType.MODULE,
            file_path=str(file_path),
            line=1,
            column=1,
            dependencies=set(),
            dependents=set(),
            metadata={"size": len(content)},
        )
        self.kg.add(ent)

    def _analyze_ts_file(self, file_path: Path) -> None:
        name = file_path.stem
        ent = Entity(
            id=f"ts:{file_path}",
            name=name,
            type=EntityType.MODULE,
            file_path=str(file_path),
            line=1,
            column=1,
            dependencies=set(),
            dependents=set(),
            metadata={},
        )
        self.kg.add(ent)

    def _analyze_patterns(self) -> None:
        # Minimal placeholder: could prompt a local model if configured
        pass

    # --- Optimization pipeline ---
    def optimize_project(self) -> dict[str, Any]:
        """Run project optimization steps and return results."""
        print("🚀 Running project optimization...")
        print("[brain] Building knowledge graph...", flush=True)
        self._build_knowledge_graph()
        print(
            f"[brain] Knowledge graph built: {len(self.kg.entities)} entities, "
            f"{sum(len(v) for v in self.kg.relationships.values())} relationships",
            flush=True,
        )

        # Load optimizer dynamically from tools/ai-code-optimizer/optimizer.py
        tools_dir = Path(__file__).resolve().parents[1]
        optimizer_dir = tools_dir / "ai-code-optimizer"
        optimizer_path = optimizer_dir / "optimizer.py"
        try:
            # Create synthetic packages so relative imports inside optimizer resolve
            import types

            if "tools" not in sys.modules:
                tools_pkg = types.ModuleType("tools")
                tools_pkg.__path__ = [str(tools_dir)]
                sys.modules["tools"] = tools_pkg
            ai_opt_pkg_name = "tools.ai_code_optimizer"
            if ai_opt_pkg_name not in sys.modules:
                ai_opt_pkg = types.ModuleType(ai_opt_pkg_name)
                ai_opt_pkg.__path__ = [str(optimizer_dir)]
                sys.modules[ai_opt_pkg_name] = ai_opt_pkg

            spec = importlib.util.spec_from_file_location("tools.ai_code_optimizer.optimizer", str(optimizer_path))
            if not spec or not spec.loader:
                raise ImportError("spec not available")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            optimizer_cls = mod.AICodeOptimizer
        except Exception as e:  # noqa: BLE001
            return {"error": f"Optimizer not available: {e}"}

        cfg_path = tools_dir / "ai-code-optimizer" / "config.yml"
        optimizer = optimizer_cls(cfg_path)
        print("[brain] Starting optimizer passes...", flush=True)
        results = optimizer.optimize_project(self.project_root)
        print("[brain] Optimizer completed.", flush=True)

        out_dir = Path(__file__).with_name("out")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "optimization-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        return results


def load_config(path: Path) -> dict[str, Any]:
    if yaml is None or not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser(description="AI Brain - Understand project")
    p.add_argument("mode", nargs="?", default="understand")
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--config", type=Path, default=Path("tools/ai-project-intelligence/config.yml"))
    p.add_argument("--out", type=Path, default=Path("tools/ai-project-intelligence/out/brain-summary.json"))
    p.add_argument("--optimize", action="store_true", help="Run optimization instead of understanding")
    args = p.parse_args()

    cfg = load_config(args.config)
    brain = AIBrain(args.root, cfg)
    if args.optimize or args.mode == "optimize":
        results = brain.optimize_project()
        print(json.dumps(results, indent=2))
    else:
        summary = brain.understand_project()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Brain summary written to {args.out}")


if __name__ == "__main__":
    main()
