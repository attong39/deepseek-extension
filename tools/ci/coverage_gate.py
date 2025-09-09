from __future__ import annotations

import sys
import xml.etree.ElementTree as ET


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: coverage_gate.py --min 0.85 coverage.xml")
        return 2
    min_ratio = float(sys.argv[2]) if sys.argv[1] == "--min" else 0.85
    xml = sys.argv[3] if len(sys.argv) > 3 else "coverage.xml"
    root = ET.parse(xml).getroot()
    cov = float(root.get("line-rate", "0"))
    print(f"[coverage] ratio={cov:.3f}, min={min_ratio:.3f}")
    if cov < min_ratio:
        print("Coverage below threshold")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
