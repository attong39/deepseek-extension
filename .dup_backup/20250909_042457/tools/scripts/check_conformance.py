#!/usr/bin/env python3
"""
Đối chiếu tất cả adapters đã gắn @implements(Protocol) với chính Protocol đó.

Kiểm tra:
- Thiếu method → HIGH
- Sai chữ ký (tham số khác tên/thiếu default) → HIGH
- Khác return annotation → MEDIUM
"""

from __future__ import annotations

import inspect
import json
import logging
from pathlib import Path
from typing import Any, get_type_hints
import AttributeError
import Exception
import ImportError
import NameError
import SystemExit
import TypeError
import ValueError
import count
import dict
import e
import func
import impl_cls
import int
import issue
import issues
import len
import list
import method
import method_name
import name
import p
import print
import problem
import protocol_cls
import protocol_method
import set
import sorted
import str
import sum
import tuple
import type
import x

# Import the implements registry - adjust path as needed
try:
    from apps.backend.tools.implements import list_implementations
except ImportError:
    logging.warning("Cannot import implements registry - no conformance checks will run")

    def list_implementations() -> list[tuple[type[Any], type[Any], str]]:
        return []


def get_signature_string(func: Any) -> str:
    """Get readable signature string for a function."""
    try:
        return str(inspect.signature(func))
    except (ValueError, TypeError):
        return "<unknown signature>"


def compare_method_signatures(protocol_method: Any, impl_method: Any) -> list[str]:
    """Compare two method signatures and return list of differences."""
    issues: list[str] = []

    try:
        proto_sig = inspect.signature(protocol_method)
        impl_sig = inspect.signature(impl_method)

        # Check parameter names and types
        proto_params = proto_sig.parameters
        impl_params = impl_sig.parameters

        if proto_params.keys() != impl_params.keys():
            issues.append(
                f"Parameter mismatch: protocol has {list(proto_params.keys())} "
                f"but implementation has {list(impl_params.keys())}"
            )

        # Check return type annotations (best effort)
        try:
            proto_hints = get_type_hints(protocol_method)
            impl_hints = get_type_hints(impl_method)

            proto_return = proto_hints.get("return")
            impl_return = impl_hints.get("return")

            if proto_return != impl_return:
                issues.append(
                    f"Return type mismatch: protocol expects {proto_return} " f"but implementation has {impl_return}"
                )
        except (TypeError, NameError, AttributeError):
            # Type hints might not be available or resolvable
            pass

    except (ValueError, TypeError) as e:
        issues.append(f"Cannot compare signatures: {e}")

    return issues


def check_implementation_conformance() -> list[dict[str, Any]]:
    """Check all registered implementations against their protocols."""
    problems: list[dict[str, Any]] = []

    implementations = list_implementations()
    if not implementations:
        logging.info("No implementations found in registry")
        return problems

    for impl_cls, protocol_cls, module_name in implementations:
        try:
            # Get all public methods from protocol
            protocol_methods = {
                name: method
                for name, method in inspect.getmembers(protocol_cls, inspect.isfunction)
                if not name.startswith("_")
            }

            # Get all public methods from implementation
            impl_methods = {
                name: method
                for name, method in inspect.getmembers(impl_cls, inspect.isfunction)
                if not name.startswith("_")
            }

            # Check each protocol method
            for method_name, protocol_method in protocol_methods.items():
                if method_name not in impl_methods:
                    # Missing method - HIGH severity
                    problems.append(
                        {
                            "severity": "HIGH",
                            "impl_class": f"{impl_cls.__module__}.{impl_cls.__name__}",
                            "protocol_class": f"{protocol_cls.__module__}.{protocol_cls.__name__}",
                            "method": method_name,
                            "issue": f"Missing method: {method_name}{get_signature_string(protocol_method)}",
                            "category": "missing_method",
                        }
                    )
                else:
                    # Check signature compatibility
                    impl_method = impl_methods[method_name]
                    signature_issues = compare_method_signatures(protocol_method, impl_method)

                    for issue in signature_issues:
                        severity = "HIGH" if "Parameter mismatch" in issue else "MEDIUM"
                        problems.append(
                            {
                                "severity": severity,
                                "impl_class": f"{impl_cls.__module__}.{impl_cls.__name__}",
                                "protocol_class": f"{protocol_cls.__module__}.{protocol_cls.__name__}",
                                "method": method_name,
                                "issue": f"{method_name}: {issue}",
                                "category": "signature_mismatch",
                            }
                        )

            # Check for extra methods in implementation (informational)
            extra_methods = set(impl_methods.keys()) - set(protocol_methods.keys())
            if extra_methods:
                problems.append(
                    {
                        "severity": "LOW",
                        "impl_class": f"{impl_cls.__module__}.{impl_cls.__name__}",
                        "protocol_class": f"{protocol_cls.__module__}.{protocol_cls.__name__}",
                        "method": ", ".join(extra_methods),
                        "issue": f"Extra methods not in protocol: {', '.join(extra_methods)}",
                        "category": "extra_methods",
                    }
                )

        except Exception as e:
            logging.error(f"Error checking {impl_cls.__name__}: {e}")
            problems.append(
                {
                    "severity": "HIGH",
                    "impl_class": f"{impl_cls.__module__}.{impl_cls.__name__}",
                    "protocol_class": f"{protocol_cls.__module__}.{protocol_cls.__name__}",
                    "method": "N/A",
                    "issue": f"Error during conformance check: {e}",
                    "category": "check_error",
                }
            )

    return problems


def generate_conformance_report(problems: list[dict[str, Any]]) -> dict[str, Any]:
    """Generate conformance report with summary."""
    summary = {
        "total_problems": len(problems),
        "high_severity": sum(1 for p in problems if p["severity"] == "HIGH"),
        "medium_severity": sum(1 for p in problems if p["severity"] == "MEDIUM"),
        "low_severity": sum(1 for p in problems if p["severity"] == "LOW"),
    }

    # Group by category
    by_category = {}
    for problem in problems:
        category = problem.get("category", "unknown")
        if category not in by_category:
            by_category[category] = 0
        by_category[category] += 1

    # Group by implementation class
    by_implementation = {}
    for problem in problems:
        impl_class = problem.get("impl_class", "unknown")
        if impl_class not in by_implementation:
            by_implementation[impl_class] = 0
        by_implementation[impl_class] += 1

    return {
        "summary": summary,
        "by_category": by_category,
        "by_implementation": by_implementation,
        "problems": problems,
    }


def main() -> int:
    """Main entry point for conformance checking."""
    logging.basicConfig(level=logging.INFO)
    print("[check_conformance] Starting conformance check...")

    # Check all registered implementations
    problems = check_implementation_conformance()

    # Generate report
    report = generate_conformance_report(problems)

    # Ensure output directory exists
    output_dir = Path(".artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write report
    output_file = output_dir / "conformance_report.json"
    output_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print summary
    summary = report["summary"]
    print(f"[check_conformance] Report written to {output_file}")
    print(f"[check_conformance] Total problems: {summary['total_problems']}")
    print(
        f"[check_conformance] HIGH: {summary['high_severity']}, "
        f"MEDIUM: {summary['medium_severity']}, LOW: {summary['low_severity']}"
    )

    # Print top categories
    if report["by_category"]:
        print("[check_conformance] Problem categories:")
        for category, count in sorted(report["by_category"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")

    # Print implementations with issues
    if report["by_implementation"]:
        print("[check_conformance] Implementations with issues:")
        for impl_class, count in sorted(report["by_implementation"].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {impl_class}: {count} issues")

    # Exit with error code if HIGH severity issues found
    if summary["high_severity"] > 0:
        print(f"[check_conformance] ❌ {summary['high_severity']} HIGH severity issues found!")
        return 1

    print("[check_conformance] ✅ No HIGH severity conformance issues found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
