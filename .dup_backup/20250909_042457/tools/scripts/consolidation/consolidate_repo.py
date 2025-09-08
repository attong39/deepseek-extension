#!/usr/bin/env python3
"""
Consolidation script để gộp file trùng lặp và tạo shim tương thích ngược.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path
from typing import Any

import yaml
import Exception
import dict
import e
import f
import from_module
import int
import len
import list
import mod
import module_name
import name
import print
import pyfile
import rule
import str
import target

ROOT = Path(__file__).resolve().parents[2]  # repo root
MAP_FILE = ROOT / "tools/consolidation/CONSOLIDATION_MAP.yaml"
REPORT_FILE = ROOT / ".artifacts/consolidation_report.md"


def _module_to_path(module_name: str) -> Path:
    """Convert module name to file path."""
    return ROOT / "zeta_vn" / Path(module_name.replace("zeta_vn.", "").replace(".", "/") + ".py")


def _write_shim(pyfile: Path, target: str) -> None:
    """Tạo shim file với deprecation warning."""
    pyfile.parent.mkdir(parents=True, exist_ok=True)

    mod, _, name = target.partition(":")
    body = textwrap.dedent(f'''\
        """DEPRECATED: Use {target} instead."""
        from __future__ import annotations

        import warnings as _w

        _w.warn(
            f"Deprecated import: use {target} instead",
            DeprecationWarning,
            stacklevel=2
        )

    ''')

    if name:
        # Import specific function/class
        body += f"from {mod} import {name} as _target\n"
        body += f"__all__ = ['{name}']\n"
        body += f"{name} = _target\n"
    else:
        # Import all from module
        body += f"from {mod} import *  # type: ignore[import-untyped]\n"

    pyfile.write_text(body, encoding="utf-8")
    print(f"✅ Created shim: {pyfile}")


def _create_profile_main() -> None:
    """Tạo main.py với profile dispatch."""
    main_file = ROOT / "zeta_vn/app/main.py"
    main_file.parent.mkdir(parents=True, exist_ok=True)

    content = textwrap.dedent('''\
        """
        Unified entry point với profile-based dispatch.

        Usage:
            ZETA_PROFILE=production python -m zeta_vn.app.main
            ZETA_PROFILE=minimal python -m zeta_vn.app.main
        """
        from __future__ import annotations

        import os
        from typing import Callable


        def _resolve_profile(profile: str) -> Callable[[], None]:
            """Resolve profile to actual implementation."""
            profile_table = {
                "production": "zeta_vn.app.main_production:run",
                "minimal": "zeta_vn.app.main_minimal:run",
                "observability": "zeta_vn.app.main_observability_demo:run",
                "blueprint": "zeta_vn.app.main_blueprint:run",
                "blueprint_demo": "zeta_vn.app.main_blueprint_demo:run",
                "blueprint_working": "zeta_vn.app.main_blueprint_working:run",
            }

            target = profile_table.get(profile, profile_table["production"])
            module_name, _, function_name = target.partition(":")

            try:
                module = __import__(module_name, fromlist=[function_name])
                return getattr(module, function_name)
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Failed to load profile '{profile}': {e}") from e


        def run() -> None:
            """Main entry point với profile dispatch."""
            profile = os.getenv("ZETA_PROFILE", "production")
            print(f"🚀 Starting ZETA with profile: {profile}")

            runner = _resolve_profile(profile)
            runner()


        # ASGI app compatibility
        app = None


        if __name__ == "__main__":
            run()
    ''')

    main_file.write_text(content, encoding="utf-8")
    print(f"✅ Created unified main: {main_file}")


def _create_outbox_unified() -> None:
    """Tạo outbox unified export."""
    outbox_init = ROOT / "zeta_vn/core/application/outbox/__init__.py"
    outbox_init.parent.mkdir(parents=True, exist_ok=True)

    content = textwrap.dedent('''\
        """
        Unified Outbox exports - using hardened implementation as canonical.
        """
        from __future__ import annotations

        # Import từ hardened implementation làm canonical
        from apps.backend.app.outbox_hardened import (
            Outbox,
            OutboxMessage,
            OutboxProcessor,
            OutboxRepository,
            ProcessResult,
        )

        __all__ = [
            "Outbox",
            "OutboxMessage",
            "OutboxProcessor",
            "OutboxRepository",
            "ProcessResult",
        ]
    ''')

    outbox_init.write_text(content, encoding="utf-8")
    print(f"✅ Created outbox unified: {outbox_init}")


def _create_websockets_unified() -> None:
    """Tạo websockets unified export."""
    ws_init = ROOT / "zeta_vn/app/websockets/__init__.py"
    ws_init.parent.mkdir(parents=True, exist_ok=True)

    content = textwrap.dedent('''\
        """
        Unified WebSocket exports.
        """
        from __future__ import annotations

        # Conditional imports để tránh lỗi nếu file chưa tồn tại
        try:
            from .chat_websocket import ChatWebSocket
        except ImportError:
            ChatWebSocket = None  # type: ignore[misc,assignment]

        try:
            from .agent_websocket import AgentWebSocket
        except ImportError:
            AgentWebSocket = None  # type: ignore[misc,assignment]

        try:
            from .training_ws import TrainingWebSocket
        except ImportError:
            # Fallback to old locations
            try:
                from apps.backend.core.websockets.training_ws import TrainingWebSocket
            except ImportError:
                try:
                    from apps.backend.realtime.training_ws import TrainingWebSocket
                except ImportError:
                    TrainingWebSocket = None  # type: ignore[misc,assignment]

        __all__ = ["ChatWebSocket", "AgentWebSocket", "TrainingWebSocket"]
    ''')

    ws_init.write_text(content, encoding="utf-8")
    print(f"✅ Created websockets unified: {ws_init}")


def _handle_profile_rule(rule: dict[str, Any], report_lines: list[str]) -> None:
    """Handle profile consolidation rule."""
    to = rule["to"]
    from_list = rule["from"]

    _create_profile_main()
    report_lines.append(f"- **Profile**: Created unified entry point `{to}`")
    for from_module in from_list:
        report_lines.append(f"  - Mapped: `{from_module}` (via ZETA_PROFILE)")


def _handle_shim_rule(rule: dict[str, Any], report_lines: list[str]) -> None:
    """Handle shim consolidation rule."""
    to = rule["to"]
    from_list = rule["from"]

    for from_module in from_list:
        shim_path = _module_to_path(from_module)
        if not shim_path.exists():
            continue  # Skip if source doesn't exist

        _write_shim(shim_path, to)
        report_lines.append(f"- **Shim**: `{from_module}` → `{to}`")


def _handle_strategy_rule(rule: dict[str, Any], report_lines: list[str]) -> None:
    """Handle strategy consolidation rule."""
    to = rule["to"]
    from_list = rule["from"]

    if "outbox" in to:
        _create_outbox_unified()
    elif "websockets" in to:
        _create_websockets_unified()

    report_lines.append(f"- **Strategy**: Unified `{to}`")
    for from_module in from_list:
        report_lines.append(f"  - Consolidated: `{from_module}`")


def _handle_remove_rule(rule: dict[str, Any], report_lines: list[str]) -> None:
    """Handle remove consolidation rule."""
    to = rule["to"]
    from_list = rule["from"]

    if to is None:  # Demo/temp files
        for from_module in from_list:
            demo_file = ROOT / f"{from_module}.py"
            if demo_file.exists():
                demo_file.unlink()
                report_lines.append(f"- **Removed**: `{demo_file}`")
    else:
        for from_module in from_list:
            old_path = _module_to_path(from_module)
            if old_path.exists():
                old_path.unlink()
                report_lines.append(f"- **Removed**: `{from_module}`")


def _process_consolidation_rules(rules: list[dict[str, Any]]) -> list[str]:
    """Process consolidation rules and return report lines."""
    report_lines = [
        "# Consolidation Report",
        "",
        f"Generated at: {Path.cwd()}",
        "",
        "## Actions Taken:",
        "",
    ]

    rule_handlers = {
        "profile": _handle_profile_rule,
        "shim": _handle_shim_rule,
        "strategy": _handle_strategy_rule,
        "remove": _handle_remove_rule,
    }

    for rule in rules:
        kind = rule["kind"]
        handler = rule_handlers.get(kind)

        if handler:
            handler(rule, report_lines)
        else:
            report_lines.append(f"- **Unknown**: {kind} for {rule.get('to', 'N/A')}")

    return report_lines


def main() -> int:
    """Main consolidation function."""
    if not MAP_FILE.exists():
        print(f"❌ Consolidation map not found: {MAP_FILE}")
        return 1

    # Load consolidation map
    try:
        with MAP_FILE.open(encoding="utf-8") as f:
            consolidation_map = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load consolidation map: {e}")
        return 1

    # Process rules
    rules = consolidation_map.get("rules", [])
    report_lines = _process_consolidation_rules(rules)

    # Write report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report_content = "\n".join(report_lines) + "\n"
    REPORT_FILE.write_text(report_content, encoding="utf-8")

    print("\n📋 Consolidation completed!")
    print(f"📄 Report: {REPORT_FILE}")
    print(f"🔍 Rules processed: {len(rules)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
