#!/usr/bin/env python3
"""
Focus Index metrics calculator for ZETA_VN.

Calculates clean architecture compliance and code quality metrics.
Designed for CI/CD pipeline integration.
"""

import argparse
import json
import sys
from pathlib import Path
import Exception
import ImportError
import e
import float
import int
import len
import print
import str

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.focus_guard import analyze_files, generate_report
except ImportError:
    print("❌ Could not import focus_guard tools")
    sys.exit(1)


def main() -> int:
    """Calculate Focus Index for CI/CD."""
    parser = argparse.ArgumentParser(description="Calculate ZETA Focus Index")
    parser.add_argument("--threshold", type=float, default=60.0, help="Minimum required score")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root directory")

    args = parser.parse_args()

    try:
        # Analyze project files
        metrics = analyze_files(args.root)

        # Generate report
        if args.json:
            report = {
                "focus_index": metrics.focus_index,
                "total_files": metrics.total_files,
                "layer_coverage": metrics.layer_coverage,
                "anti_patterns": {
                    "manager_files": len(metrics.manager_files),
                    "duplicate_models": len(metrics.duplicate_models),
                    "event_buses": len(metrics.duplicate_event_buses),
                    "legacy_repositories": len(metrics.repository_implementations.get("legacy_implementations", [])),
                },
                "threshold": args.threshold,
                "passed": metrics.focus_index >= args.threshold,
            }
            print(json.dumps(report, indent=2))
        else:
            generate_report(metrics)

        # Check threshold
        if metrics.focus_index < args.threshold:
            print(f"\n❌ Focus Index {metrics.focus_index} below threshold {args.threshold}")
            return 1
        else:
            print(f"\n✅ Focus Index {metrics.focus_index} meets threshold {args.threshold}")
            return 0

    except Exception as e:
        print(f"❌ Error calculating Focus Index: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
