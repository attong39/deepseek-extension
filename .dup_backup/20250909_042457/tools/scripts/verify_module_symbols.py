#!/usr/bin/env python3
from __future__ import annotations
import Exception
import ImportError
import SystemExit
import all_misses
import dict
import e
import filename
import hasattr
import int
import len
import list
import m
import misses
import module_name
import pkg_name
import print
import r
import spec
import str
import sum
import symbol_name

"""
Kiểm tra module/symbol theo expectations định trước.

Xác thực:
- Module import được không
- Symbol bắt buộc có tồn tại không
- File tối thiểu theo heuristic thư mục

Output: .artifacts/module_symbol_report.json
"""

import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ART = Path(".artifacts")
ART.mkdir(parents=True, exist_ok=True)


@dataclass
class Miss:
    """Thông tin về symbol/module thiếu."""

    module: str
    symbol: str
    severity: str
    message: str


def _load_expectations() -> dict[str, Any]:
    """Load file expectations YAML."""
    try:
        import yaml
    except ImportError:
        print("Error: pyyaml không có. Chạy: uv add pyyaml", file=sys.stderr)
        return {}

    cfg_path = Path("configs/file_expectations.yaml")
    if not cfg_path.exists():
        print(f"Warning: {cfg_path} không tồn tại", file=sys.stderr)
        return {}

    try:
        return yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"Error reading expectations: {e}", file=sys.stderr)
        return {}


def _check_required_symbols(required: dict[str, Any]) -> list[Miss]:
    """Kiểm tra symbols bắt buộc trong modules."""
    misses: list[Miss] = []

    for module_name, spec in required.items():
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            miss = Miss(module=module_name, symbol="*", severity="HIGH", message=f"ImportError: {e}")
            misses.append(miss)
            continue

        # Kiểm tra từng symbol
        for symbol_name in spec.get("symbols", []):
            if not hasattr(module, symbol_name):
                miss = Miss(
                    module=module_name,
                    symbol=symbol_name,
                    severity="HIGH",
                    message="Missing required symbol",
                )
                misses.append(miss)

    return misses


def _check_dir_minimal_files(dir_minimal: dict[str, Any]) -> list[Miss]:
    """Kiểm tra file tối thiểu theo thư mục."""
    misses: list[Miss] = []

    # Tìm src hoặc zeta_vn root
    roots = [Path("zeta_vn"), Path("src")]
    root = None
    for r in roots:
        if r.exists():
            root = r
            break

    if not root:
        miss = Miss(
            module="*",
            symbol="*",
            severity="HIGH",
            message="Cannot find source root (zeta_vn/ or src/)",
        )
        misses.append(miss)
        return misses

    for pkg_name, spec in dir_minimal.items():
        # Convert module path to folder path
        folder = root / pkg_name.replace(".", "/")

        if not folder.exists():
            miss = Miss(
                module=pkg_name,
                symbol="*",
                severity="HIGH",
                message=f"Missing package folder: {folder}",
            )
            misses.append(miss)
            continue

        # Kiểm tra file bắt buộc
        for filename in spec.get("must_have_files", []):
            filepath = folder / filename

            if not filepath.exists():
                miss = Miss(
                    module=pkg_name,
                    symbol=filename,
                    severity="HIGH",
                    message=f"Missing required file: {filename}",
                )
                misses.append(miss)
            else:
                # Kiểm tra file có quá nhỏ/rỗng không
                try:
                    content = filepath.read_text(encoding="utf-8", errors="ignore")
                    if len(content.strip()) < 20:  # Quá nhỏ
                        miss = Miss(
                            module=pkg_name,
                            symbol=filename,
                            severity="MEDIUM",
                            message=f"File too small/empty: {filename}",
                        )
                        misses.append(miss)
                except Exception:
                    pass  # Bỏ qua lỗi đọc file

    return misses


def _generate_summary(misses: list[Miss]) -> dict[str, Any]:
    """Tạo summary từ danh sách misses."""
    return {
        "total": len(misses),
        "high": sum(1 for m in misses if m.severity == "HIGH"),
        "medium": sum(1 for m in misses if m.severity == "MEDIUM"),
        "low": sum(1 for m in misses if m.severity == "LOW"),
    }


def _write_report(misses: list[Miss]) -> int:
    """Ghi báo cáo và return exit code."""
    summary = _generate_summary(misses)

    payload = {"misses": [m.__dict__ for m in misses], "summary": summary}

    out_path = ART / "module_symbol_report.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"[verify-module-symbols] wrote {out_path}")
    print(f"  total={summary['total']}")
    print(f"  HIGH={summary['high']}")
    print(f"  MEDIUM={summary['medium']}")

    if summary["high"] > 0:
        print("❌ Found HIGH severity missing symbols/modules!")
        for miss in misses:
            if miss.severity == "HIGH":
                print(f"  🚨 {miss.module}.{miss.symbol}: {miss.message}")

    return 1 if summary["high"] > 0 else 0


def main() -> int:
    """Entry point chính."""
    print("🔍 Verifying module symbols and required files...")

    expectations = _load_expectations()

    if not expectations:
        print("No expectations loaded, creating empty report")
        _write_report([])
        return 0

    # Chạy tất cả kiểm tra
    all_misses: list[Miss] = []

    # 1. Kiểm tra required symbols
    required = expectations.get("required", {})
    if required:
        print(f"Checking {len(required)} required modules...")
        all_misses.extend(_check_required_symbols(required))

    # 2. Kiểm tra dir minimal files
    dir_minimal = expectations.get("dir_minimal", {})
    if dir_minimal:
        print(f"Checking {len(dir_minimal)} directory requirements...")
        all_misses.extend(_check_dir_minimal_files(dir_minimal))

    return _write_report(all_misses)


if __name__ == "__main__":
    raise SystemExit(main())
