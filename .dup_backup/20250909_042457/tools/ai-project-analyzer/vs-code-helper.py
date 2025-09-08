#!/usr/bin/env python3
"""
VS Code Helper - bridge to run analyzer and optimizer and write VS Code artifacts.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any
import AnalyzerCls
import Exception
import ImportError
import OSError
import ValueError
import data
import dict
import e
import exc
import isinstance
import k
import list
import load_config_fn
import obj
import path
import r
import set
import sorted
import str
import tasks
import tuple
import v

# Project's standard logger
logger = logging.getLogger(__name__)


def _json_safe(obj: Any) -> Any:
    """Recursively convert objects into JSON-serializable forms.

    - set -> sorted list
    - Path -> str
    - dict/list/tuple -> recurse

    Args:
        obj: The object to make JSON-safe.

    Returns:
        A JSON-serializable version of the object.
    """
    if isinstance(obj, set):
        return sorted(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    return obj


def _load_smart_optimizer() -> Any:
    """Load the SmartOptimizer class from the local smart-optimizer.py file.

    Returns:
        The SmartOptimizer class.

    Raises:
        ImportError: If unable to load the SmartOptimizer module.
    """
    mod_path = Path(__file__).with_name("smart-optimizer.py")
    spec = importlib.util.spec_from_file_location("smart_optimizer", str(mod_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        return module.SmartOptimizer  # type: ignore[attr-defined, no-any-return]
    raise ImportError("Unable to load SmartOptimizer")


def _load_analyzer() -> tuple[Any, Callable[[Path], dict[str, Any]]]:
    """Load the ProjectAnalyzer and load_config function.

    Attempts standard import first, then falls back to local file loading.
    This makes the script runnable from the repo root or any working directory.

    Returns:
        A tuple of (ProjectAnalyzer class, load_config function).

    Raises:
        ImportError: If unable to load the analyzer module.
    """
    try:
        # Attempt standard import first
        from analyzer import ProjectAnalyzer, load_config

        return ProjectAnalyzer, load_config
    except Exception as exc:
        # Fallback: load analyzer.py from the same folder as this script
        mod_path = Path(__file__).with_name("analyzer.py")
        spec = importlib.util.spec_from_file_location("analyzer", str(mod_path))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.ProjectAnalyzer, module.load_config
        raise ImportError("Unable to load analyzer module") from exc


def write_json(path: Path, data: Any) -> None:
    """Write data to a JSON file safely.

    Args:
        path: The file path to write to.
        data: The data to serialize and write.

    Raises:
        OSError: If writing to the file fails.
    """
    if not isinstance(path, Path):
        raise ValueError("path must be a Path instance.")
    path.parent.mkdir(parents=True, exist_ok=True)
    safe = _json_safe(data)
    try:
        path.write_text(json.dumps(safe, indent=2), encoding="utf-8")
    except OSError as e:
        logger.error(f"Failed to write to {path}: {e}")
        raise


def build_tasks(recs: list[dict[str, Any]]) -> dict[str, Any]:
    """Build VS Code tasks from recommendations.

    Args:
        recs: List of recommendation dictionaries.

    Returns:
        A dictionary representing the tasks.json content.
    """
    if not isinstance(recs, list):
        raise ValueError("recs must be a list of dictionaries.")
    tasks: list[dict[str, Any]] = []
    for r in recs[:10]:  # Cap to keep tasks tidy
        if not isinstance(r, dict):
            continue
        title = f"AI: {r.get('id', 'optimize')}"
        cmd = "echo"
        args = [r.get("description", "Apply recommendation")]  # Placeholder
        tasks.append({
            "label": title,
            "type": "shell",
            "command": cmd,
            "args": args,
            "group": "none",
        })
    return {
        "version": "2.0.0",
        "tasks": tasks,
    }


def main() -> None:
    """Main entry point for the VS Code helper script.

    Parses arguments, analyzes the project, generates recommendations,
    and writes VS Code artifacts.
    """
    p = argparse.ArgumentParser(description="VS Code helper for AI Project Analyzer")
    p.add_argument("--root", type=Path, default=Path.cwd(),
                   help="Root directory of the project to analyze.")
    p.add_argument("--config", type=Path,
                   default=Path("tools/ai-project-analyzer/config.yml"),
                   help="Path to the configuration file.")
    p.add_argument("--vscode", type=Path, default=Path(".vscode"),
                   help="Directory to write VS Code artifacts.")
    p.add_argument("--out", type=Path,
                   default=Path("tools/ai-project-analyzer/out"),
                   help="Directory to write output files.")
    args = p.parse_args()

    # Validate arguments
    if not args.root.exists() or not args.root.is_dir():
        raise ValueError(f"Root directory {args.root} does not exist or is not a directory.")

    try:
        AnalyzerCls, load_config_fn = _load_analyzer()
    except ImportError as e:
        logger.error(f"Failed to load analyzer: {e}")
        raise

    cfg = {}
    if args.config.exists():
        try:
            cfg = load_config_fn(args.config)
        except Exception as e:
            logger.warning(f"Failed to load config {args.config}: {e}")
    else:
        logger.warning(f"Config file not found: {args.config}")

    try:
        analyzer = AnalyzerCls(args.root, cfg)
        analysis = analyzer.analyze_project()
    except Exception as e:
        logger.error(f"Failed to analyze project: {e}")
        raise

    # Write analysis outputs
    out_dir = args.out
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        analysis_path = out_dir / "analysis.json"
        write_json(analysis_path, analysis)
        logger.info(f"Wrote analysis to {analysis_path}")
    except Exception as e:
        logger.error(f"Failed to write analysis: {e}")
        raise

    # Generate recommendations
    recs = []
    try:
        smart_optimizer_cls = _load_smart_optimizer()
        recs = smart_optimizer_cls(analysis).generate_recommendations()
    except Exception as e:
        logger.warning(f"Recommendation generation failed: {e}")
        recs = []
    try:
        recs_path = out_dir / "recommendations.json"
        write_json(recs_path, recs)
        logger.info(f"Wrote recommendations to {recs_path}")
    except Exception as e:
        logger.error(f"Failed to write recommendations: {e}")
        raise

    # VS Code artifacts
    vscode_dir = args.vscode
    try:
        vscode_dir.mkdir(parents=True, exist_ok=True)
        write_json(vscode_dir / "ai-analysis.json", analysis)
        write_json(vscode_dir / "ai-recommendations.json", recs)
        write_json(vscode_dir / "ai-tasks.json", build_tasks(recs))
        logger.info(f"VS Code artifacts written to {vscode_dir}")
    except Exception as e:
        logger.error(f"Failed to write VS Code artifacts: {e}")
        raise


if __name__ == "__main__":
    main()
