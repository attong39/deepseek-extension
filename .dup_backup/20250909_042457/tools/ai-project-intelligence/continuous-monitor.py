#!/usr/bin/env python3
"""
Continuous Monitor - Watches for changes and maintains project consistency

On changes:
1) Rebuild Knowledge Graph
2) Run Consistency Guard
3) Optionally apply auto-fixes and re-run understanding
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import logging
import time
from pathlib import Path
from typing import Any

from brain import AIBrain, load_config
from reporter import ReportManager

# Optional watchdog dependency with safe fallbacks
try:  # pragma: no cover - optional at runtime
    events_mod = importlib.import_module("watchdog.events")
    observers_mod = importlib.import_module("watchdog.observers")
    WatchdogEventHandler = events_mod.FileSystemEventHandler
    WatchdogObserver = observers_mod.Observer
    watchdog_available = True
except Exception:  # pragma: no cover
    WatchdogEventHandler = None
    WatchdogObserver = None
    watchdog_available = False


def _load_module(filename: str, module_name: str) -> Any:
    """Dynamically load a Python module by filename located next to this file."""
    mod_path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, str(mod_path))
    if not spec or not spec.loader:
        raise ImportError(f"Unable to load module: {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ai_intelligence.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def _check_and_fix_consistency(project_root: Path, cfg: dict[str, Any], brain: AIBrain) -> list[dict[str, Any]]:
    """Run consistency guard and apply auto-fixes if enabled. Returns list of issues."""
    kg_file = project_root / ".ai_knowledge_graph.json"
    if not kg_file.exists():
        logger.info("Knowledge graph not found; skipping consistency check.")
        return []
    try:
        data = json.loads(kg_file.read_text(encoding="utf-8"))
        entities = data.get("entities", {})
        relationships = {k: set(v) for k, v in data.get("relationships", {}).items()}
    except Exception as e:  # noqa: BLE001
        logger.warning(f"Failed to read knowledge graph: {e}")
        return []

    try:
        cg_mod = _load_module("consistency-guard.py", "consistency_guard")
        cg_class = cg_mod.ConsistencyGuard
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to load Consistency Guard: {e}")
        return []

    guard = cg_class(entities, relationships)
    issues = guard.find_inconsistencies()
    if not issues:
        logger.info("No inconsistencies detected.")
        return []
    logger.info(f"Detected {len(issues)} inconsistencies.")

    if not cfg.get("auto_fix", {}).get("enabled", False):
        logger.info("Auto-fix disabled in config.")
        return issues

    try:
        fixer = _load_module("auto_fixer.py", "auto_fixer")
        apply_fixes = fixer.apply_fixes
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to load Auto Fixer: {e}")
        return issues

    allowed = set(cfg.get("auto_fix", {}).get("allowed_issue_types", []))
    fixes = apply_fixes(project_root, issues, allowed_issue_types=allowed)
    if fixes:
        logger.info(f"Applied {len(fixes)} fixes; rebuilding knowledge graph...")
        try:
            brain.understand_project()
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Post-fix understanding failed: {e}")
    return issues


class _ProjectWatcherMixin:
    def __init__(self, project_root: Path, brain: AIBrain, cfg: dict[str, Any]) -> None:
        self.project_root = project_root
        self.brain = brain
        self.cfg = cfg
        self.last_updated = time.time()
        self.debounce_seconds = 2.0

    def _is_source_file(self, path: str) -> bool:
        return any(path.endswith(ext) for ext in (".py", ".ts", ".tsx", ".js", ".jsx"))

    def on_modified(self, event: Any) -> None:
        if getattr(event, "is_directory", False):
            return
        src_path: str = getattr(event, "src_path", "")
        if self._is_source_file(src_path) and (time.time() - self.last_updated > self.debounce_seconds):
            logger.info(f"Change detected in {src_path}")
            self.last_updated = time.time()
            try:
                self.brain.understand_project()
                issues = _check_and_fix_consistency(self.project_root, self.cfg, self.brain)
                ReportManager(self.project_root).save_issues_report(issues)
                # Optional: auto-run optimizer on change if enabled
                if self.cfg.get("optimization", {}).get("auto_run_on_change", False):
                    try:
                        results = self.brain.optimize_project()
                        out_dir = Path("tools/ai-project-intelligence/out")
                        out_dir.mkdir(parents=True, exist_ok=True)
                        (out_dir / "monitor-change-optimization.json").write_text(
                            json.dumps(results, indent=2), encoding="utf-8"
                        )
                        logger.info("Auto-optimization on change completed")
                    except Exception as e:  # noqa: BLE001
                        logger.warning(f"Auto-optimization on change failed: {e}")
            except Exception as e:  # noqa: BLE001
                logger.error(f"Error processing change: {e}")


class _FallbackEventHandler:  # minimal base when watchdog isn't available
    pass


BaseHandlerForWatcher = (
    WatchdogEventHandler if watchdog_available and WatchdogEventHandler is not None else _FallbackEventHandler
)
ProjectWatcher = type("ProjectWatcher", (_ProjectWatcherMixin, BaseHandlerForWatcher), {})


class ContinuousMonitor:
    observer: Any

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        cfg = load_config(Path("tools/ai-project-intelligence/config.yml"))
        self.cfg = cfg
        self.brain = AIBrain(project_root, cfg)
        self.observer = WatchdogObserver() if watchdog_available and WatchdogObserver is not None else None

        if not watchdog_available:
            logger.warning("Watchdog not installed. Continuous monitoring disabled.")

    def start(self) -> None:
        if not watchdog_available:
            logger.error("Cannot start monitoring: watchdog not installed")
            return

        logger.info("Starting continuous project monitoring...")

        try:
            self.brain.understand_project()
            issues = _check_and_fix_consistency(self.project_root, self.cfg, self.brain)
            ReportManager(self.project_root).save_issues_report(issues)
            # Optional: auto-run optimizer at startup if enabled
            if self.cfg.get("optimization", {}).get("auto_run_on_start", False):
                try:
                    results = self.brain.optimize_project()
                    out_dir = Path("tools/ai-project-intelligence/out")
                    out_dir.mkdir(parents=True, exist_ok=True)
                    (out_dir / "monitor-start-optimization.json").write_text(
                        json.dumps(results, indent=2), encoding="utf-8"
                    )
                    logger.info("Auto-optimization at startup completed")
                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Auto-optimization at startup failed: {e}")
        except Exception as e:  # noqa: BLE001
            logger.error(f"Initial project understanding failed: {e}")
            return

        try:
            obs = self.observer
            if obs is None:
                logger.error("Observer not available")
                return
            event_handler = ProjectWatcher(self.project_root, self.brain, self.cfg)
            obs.schedule(event_handler, str(self.project_root), recursive=True)
            obs.start()
            logger.info("Monitoring started successfully")

            try:
                while True:
                    # TODO: Replace blocking sleep with async await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                obs.stop()

            obs.join()
        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to start monitoring: {e}")


def run_one_shot(project_root: Path) -> list[dict[str, Any]]:
    logger.info("Running one-shot analysis (watchdog not available or disabled)")
    cfg = load_config(Path("tools/ai-project-intelligence/config.yml"))
    brain = AIBrain(project_root, cfg)
    brain.understand_project()
    issues = _check_and_fix_consistency(project_root, cfg, brain)
    ReportManager(project_root).save_issues_report(issues)
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Continuous Monitor")
    parser.add_argument("--one-shot", action="store_true", help="Run a single analysis pass and exit")
    args = parser.parse_args()

    project_root = Path.cwd()
    if args.one_shot or not watchdog_available:
        issues = run_one_shot(project_root)
        logger.info(f"One-shot analysis completed. Found {len(issues)} issues.")
        return

    monitor = ContinuousMonitor(project_root)
    monitor.start()


if __name__ == "__main__":
    main()
