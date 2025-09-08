#!/usr/bin/env python3
"""
Smart Optimizer - AI-powered code optimization recommendations
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any
import Exception
import all
import analysis_results
import bool
import dict
import enriched
import enumerate
import f
import file_path
import idx
import int
import k
import len
import list
import meta
import model
import part
import path
import print
import r
import self
import str
import v


def _ollama_chat(prompt: str, model: str = "deepseek-coder") -> str | None:
    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=90,
        )
        if proc.returncode == 0:
            return proc.stdout
        return None
    except Exception:
        return None


class SmartOptimizer:
    def __init__(self, analysis_results: dict[str, Any]):
        self.analysis_results = analysis_results
        self.min_priority: int = int(os.getenv("AI_OPT_MIN_PRIORITY", "5"))
        # Limit AI enrichment to avoid long runs; default disabled
        self.max_enrich: int = int(os.getenv("AI_ENRICH_MAX", "0"))

    def _is_internal(self, path: str) -> bool:
        """Return True if path appears to belong to the repo (not vendor/build dirs)."""
        p = Path(path)
        banned = {
            "node_modules",
            ".venv",
            "site-packages",
            "dist",
            "build",
            ".git",
            ".cache",
        }
        return all(part not in banned for part in p.parts)

    def generate_recommendations(self) -> list[dict[str, Any]]:
        recs: list[dict[str, Any]] = []
        for file_path, meta in self.analysis_results.get("file_metadata", {}).items():
            if self._is_internal(file_path):
                recs.extend(self._heuristic_file_recs(file_path, meta))
        recs.extend(self._project_recs())
        # Optionally enrich via local model
        enriched: list[dict[str, Any]] = []
        for idx, r in enumerate(recs):
            if self.max_enrich > 0 and idx < self.max_enrich:
                prompt = (
                    f"Suggest concise improvement for file {r['file']}:\n"
                    f"Issue: {r['description']}\n"
                    "Provide a one-liner suggestion."
                )
                ai = _ollama_chat(prompt)
                if ai:
                    r["ai_note"] = ai.strip()[:400]
            enriched.append(r)
        # Filter by min priority and internal paths only
        return [
            r
            for r in enriched
            if int(r.get("priority", 5)) >= self.min_priority and self._is_internal(r.get("file", ""))
        ]

    def _heuristic_file_recs(self, file_path: str, meta: dict[str, Any]) -> list[dict[str, Any]]:
        recs: list[dict[str, Any]] = []
        if not self._is_internal(file_path):
            return recs
        ftype = meta.get("type")
        if ftype == "python" and not meta.get("functions"):
            recs.append(
                {
                    "id": f"add_tests::{file_path}",
                    "file": file_path,
                    "priority": 6,
                    "description": "Consider adding functions or module-level docs to improve structure.",
                    "impact": "maintainability",
                }
            )
        if ftype == "typescript" and len(meta.get("imports", [])) > 10:
            recs.append(
                {
                    "id": f"reduce_imports::{file_path}",
                    "file": file_path,
                    "priority": 5,
                    "description": "High number of imports; consider barrel files or path aliases.",
                    "impact": "maintainability",
                }
            )
        return recs

    def _project_recs(self) -> list[dict[str, Any]]:
        deps = self.analysis_results.get("dependency_graph", {})
        large_fans_out = [k for k, v in deps.items() if len(v) > 15 and self._is_internal(k)]
        recs: list[dict[str, Any]] = []
        for f in large_fans_out:
            recs.append(
                {
                    "id": f"split_module::{f}",
                    "file": f,
                    "priority": 7,
                    "description": "File has many outgoing deps; consider splitting responsibilities.",
                    "impact": "architecture",
                }
            )
        return recs


def main() -> None:
    p = argparse.ArgumentParser(description="Generate AI optimization recommendations")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument(
        "--out",
        type=Path,
        default=Path("tools/ai-project-analyzer/out/recommendations.json"),
    )
    args = p.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    recs = SmartOptimizer(data).generate_recommendations()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(recs, indent=2), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
