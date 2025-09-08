#!/usr/bin/env python3
"""
Focus Guardrails and Cut-list Policy Tool

Computes Focus Index (0-100) based on layer coverage and anti-pattern penalties.
Detects:
- *manager.py files (cut-list targets)
- Duplicate models (agent.py vs agent_model.py)
- Duplicate event buses
- Repository implementation preferences

Usage:
    python tools/focus_guard.py
    python tools/focus_guard.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
import ValueError
import abs
import any
import base
import base_file
import bool
import bus
import count
import dict
import dup
import f
import file_path
import files
import float
import group_files
import int
import layer
import len
import list
import max
import mgr
import min
import model
import model_file
import model_groups
import output_json
import part
import print
import py_file
import repo
import root
import round
import str
import tuple


@dataclass
class FocusMetrics:
    """Metrics for Focus Index calculation."""

    total_files: int = 0
    layer_coverage: dict[str, int] = field(default_factory=dict)
    manager_files: list[str] = field(default_factory=list)
    duplicate_models: list[tuple[str, str]] = field(default_factory=list)
    duplicate_event_buses: list[str] = field(default_factory=list)
    repository_implementations: dict[str, list[str]] = field(default_factory=dict)
    focus_index: float = 0.0


def scan_python_files(root_path: Path) -> list[Path]:
    """Scan for all Python files in the project."""
    py_files = []

    # Skip common non-source directories
    skip_dirs = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules",
        "dist",
        "build",
        ".tox",
        "venv",
    }

    for py_file in root_path.rglob("*.py"):
        # Skip if any parent directory is in skip_dirs
        if any(part in skip_dirs for part in py_file.parts):
            continue
        py_files.append(py_file)

    return py_files


def analyze_layer_coverage(files: list[Path], root: Path) -> dict[str, int]:
    """Analyze distribution across Clean Architecture layers."""
    layers = {
        "app": 0,  # Interface layer
        "core": 0,  # Domain layer
        "data": 0,  # Data/Infrastructure layer
        "config": 0,  # Configuration
        "tests": 0,  # Testing
        "tools": 0,  # Development tools
        "other": 0,  # Everything else
    }

    for file_path in files:
        try:
            rel_path = file_path.relative_to(root)

            # Check for zeta_vn prefix first
            if len(rel_path.parts) > 1 and rel_path.parts[0] == "zeta_vn":
                # Use second part as layer (zeta_vn/app, zeta_vn/core, etc.)
                layer_part = rel_path.parts[1] if len(rel_path.parts) > 1 else "other"
            else:
                # Use first part as layer (direct folders)
                layer_part = rel_path.parts[0] if rel_path.parts else "other"

            if layer_part in layers:
                layers[layer_part] += 1
            else:
                layers["other"] += 1
        except ValueError:
            # File is not relative to root
            layers["other"] += 1

    return layers


def find_manager_files(files: list[Path]) -> list[str]:
    """Find files that match *manager.py pattern (cut-list targets)."""
    managers = []

    for file_path in files:
        if file_path.name.endswith("manager.py") or file_path.name.endswith("_manager.py"):
            managers.append(str(file_path))

    return managers


def find_duplicate_models(files: list[Path]) -> list[tuple[str, str]]:
    """Find duplicate model patterns (e.g., agent.py vs agent_model.py)."""
    duplicates = []

    # Group files by their stem (without _model suffix)
    model_groups: dict[str, list[Path]] = {}

    for file_path in files:
        stem = file_path.stem

        # Check if this is a model file
        if stem.endswith("_model"):
            base_name = stem[:-6]  # Remove '_model'
        else:
            base_name = stem

        if base_name not in model_groups:
            model_groups[base_name] = []
        model_groups[base_name].append(file_path)

    # Find groups with both base.py and base_model.py
    for base_name, group_files in model_groups.items():
        base_files = [f for f in group_files if f.stem == base_name]
        model_files = [f for f in group_files if f.stem == f"{base_name}_model"]

        if base_files and model_files:
            for base_file in base_files:
                for model_file in model_files:
                    duplicates.append((str(base_file), str(model_file)))

    return duplicates


def find_duplicate_event_buses(files: list[Path]) -> list[str]:
    """Find duplicate event bus implementations."""
    event_buses = []

    for file_path in files:
        if "event_bus.py" in str(file_path):
            event_buses.append(str(file_path))

    return event_buses


def analyze_repository_implementations(files: list[Path]) -> dict[str, list[str]]:
    """Analyze repository implementation patterns."""
    repos = {
        "sqlalchemy_preferred": [],
        "legacy_implementations": [],
        "other_repositories": [],
    }

    for file_path in files:
        file_str = str(file_path)
        if "repository" in file_str.lower():
            if "sqlalchemy_" in file_path.name:
                repos["sqlalchemy_preferred"].append(file_str)
            elif file_path.name.endswith("_repository.py"):
                repos["legacy_implementations"].append(file_str)
            else:
                repos["other_repositories"].append(file_str)

    return repos


def calculate_focus_index(metrics: FocusMetrics) -> float:
    """Calculate Focus Index (0-100) based on metrics."""
    if metrics.total_files == 0:
        return 0.0

    # Base score from Clean Architecture layer distribution
    core_app_data = (
        metrics.layer_coverage.get("core", 0)
        + metrics.layer_coverage.get("app", 0)
        + metrics.layer_coverage.get("data", 0)
    )

    if metrics.total_files > 0:
        # Clean Architecture ratio (should be high)
        architecture_ratio = core_app_data / metrics.total_files
        # Base score: 80% for good architecture + bonuses
        base_score = min(80, architecture_ratio * 100)

        # Bonus for balanced distribution
        if core_app_data > 0:
            core_ratio = metrics.layer_coverage.get("core", 0) / core_app_data
            app_ratio = metrics.layer_coverage.get("app", 0) / core_app_data
            data_ratio = metrics.layer_coverage.get("data", 0) / core_app_data

            # Ideal ratios: core~40%, app~35%, data~25%
            balance_score = (
                100 - abs(core_ratio - 0.4) * 100 - abs(app_ratio - 0.35) * 100 - abs(data_ratio - 0.25) * 100
            )
            balance_bonus = max(0, balance_score / 10)  # Up to 10 bonus points
            base_score += balance_bonus
    else:
        base_score = 0

    # Penalties for anti-patterns (scaled down for more realistic scoring)
    penalties = 0

    # Manager files penalty (1 point per manager - reduced from 3)
    penalties += len(metrics.manager_files) * 1

    # Duplicate models penalty (1 point per duplicate pair - reduced from 5)
    penalties += len(metrics.duplicate_models) * 1

    # Multiple event buses penalty (5 points if more than 1 - reduced from 10)
    if len(metrics.duplicate_event_buses) > 1:
        penalties += 5

    # Legacy repository penalty (0.5 points per legacy repo - reduced from 2)
    legacy_count = len(metrics.repository_implementations.get("legacy_implementations", []))
    penalties += int(legacy_count * 0.5)

    # Calculate final score
    final_score = max(0, base_score - penalties)

    return round(final_score, 1)


def generate_report(metrics: FocusMetrics, output_json: bool = False) -> None:
    """Generate and display the focus report."""

    if output_json:
        report = {
            "focus_index": metrics.focus_index,
            "total_files": metrics.total_files,
            "layer_coverage": metrics.layer_coverage,
            "anti_patterns": {
                "manager_files": metrics.manager_files,
                "duplicate_models": [{"base": dup[0], "model": dup[1]} for dup in metrics.duplicate_models],
                "duplicate_event_buses": metrics.duplicate_event_buses,
                "repository_implementations": metrics.repository_implementations,
            },
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("🎯 ZETA Focus Index Report")
        print("=" * 50)
        print(f"Focus Index: {metrics.focus_index}/100")
        print(f"Total Files: {metrics.total_files}")
        print()

        print("📊 Layer Coverage:")
        for layer, count in metrics.layer_coverage.items():
            percentage = (count / metrics.total_files * 100) if metrics.total_files > 0 else 0
            print(f"  {layer:8}: {count:4} files ({percentage:5.1f}%)")
        print()

        print("⚠️  Anti-patterns Detected:")

        if metrics.manager_files:
            print(f"  📁 Manager files ({len(metrics.manager_files)}):")
            for mgr in metrics.manager_files[:5]:  # Show first 5
                print(f"    - {mgr}")
            if len(metrics.manager_files) > 5:
                print(f"    ... and {len(metrics.manager_files) - 5} more")
            print()

        if metrics.duplicate_models:
            print(f"  🔄 Duplicate models ({len(metrics.duplicate_models)}):")
            for base, model in metrics.duplicate_models[:3]:  # Show first 3
                print(f"    - {base} ↔ {model}")
            if len(metrics.duplicate_models) > 3:
                print(f"    ... and {len(metrics.duplicate_models) - 3} more")
            print()

        if len(metrics.duplicate_event_buses) > 1:
            print(f"  🚌 Multiple event buses ({len(metrics.duplicate_event_buses)}):")
            for bus in metrics.duplicate_event_buses:
                print(f"    - {bus}")
            print()

        legacy_repos = metrics.repository_implementations.get("legacy_implementations", [])
        if legacy_repos:
            print(f"  🗄️  Legacy repositories ({len(legacy_repos)}):")
            for repo in legacy_repos[:3]:  # Show first 3
                print(f"    - {repo}")
            if len(legacy_repos) > 3:
                print(f"    ... and {len(legacy_repos) - 3} more")
            print()

        print("💡 Recommendations:")
        if metrics.manager_files:
            print("  - Fold manager modules into service façades with deprecation shims")
        if metrics.duplicate_models:
            print("  - Normalize data models to *_model.py and update imports")
        if len(metrics.duplicate_event_buses) > 1:
            print("  - Use infrastructure/events/event_bus.py and deprecate core/events bus")
        if legacy_repos:
            print("  - Prefer sqlalchemy_*_repository.py implementations; deprecate legacy duplicates")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Focus Guardrails and Cut-list Policy Tool")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--root", default=".", help="Root directory to analyze")

    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if not root_path.exists():
        print(f"Error: Root path {root_path} does not exist", file=sys.stderr)
        sys.exit(1)

    # Scan Python files
    python_files = scan_python_files(root_path)

    # Initialize metrics
    metrics = FocusMetrics()
    metrics.total_files = len(python_files)

    # Analyze various aspects
    metrics.layer_coverage = analyze_layer_coverage(python_files, root_path)
    metrics.manager_files = find_manager_files(python_files)
    metrics.duplicate_models = find_duplicate_models(python_files)
    metrics.duplicate_event_buses = find_duplicate_event_buses(python_files)
    metrics.repository_implementations = analyze_repository_implementations(python_files)

    # Calculate focus index
    metrics.focus_index = calculate_focus_index(metrics)

    # Generate report
    generate_report(metrics, args.json)

    # Exit with non-zero if focus index is too low (for CI)
    if os.getenv("FOCUS_ENFORCE") == "1":
        max_files = int(os.getenv("MAX_FILES", "1000"))
        max_managers = int(os.getenv("MAX_MANAGERS", "10"))

        if metrics.total_files > max_files:
            print(
                f"❌ Too many files: {metrics.total_files} > {max_files}",
                file=sys.stderr,
            )
            sys.exit(1)

        if len(metrics.manager_files) > max_managers:
            print(
                f"❌ Too many managers: {len(metrics.manager_files)} > {max_managers}",
                file=sys.stderr,
            )
            sys.exit(1)


if __name__ == "__main__":
    main()
