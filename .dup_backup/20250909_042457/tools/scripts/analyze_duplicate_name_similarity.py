#!/usr/bin/env python3
"""
Analyze duplicate basenames in apps/backend/app and flag near-identical content.
Writes reports/backend_name_similarity.json
"""

from __future__ import annotations

import difflib
import json
from collections import defaultdict
from pathlib import Path
import Exception
import SystemExit
import dict
import flagged
import groups
import i
import int
import item
import j
import len
import line
import list
import name
import object
import p
import paths
import print
import range
import round
import sims
import str

ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "apps" / "backend" / "app"
REPORTS = ROOT / "reports"


def read_text_norm(p: Path) -> str:
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        t = p.read_text(errors="ignore")
    # Normalize whitespace
    return "\n".join(line.strip() for line in t.splitlines() if line.strip())


def main() -> int:
    files = [p for p in APP_DIR.rglob("*.py") if p.is_file()]
    groups: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        groups[p.name].append(p)

    flagged: dict[str, list[dict[str, object]]] = {}
    for name, paths in groups.items():
        if len(paths) < 2:
            continue
        # Compare pairwise
        n = len(paths)
        sims: list[dict[str, object]] = []
        texts = [read_text_norm(p) for p in paths]
        for i in range(n):
            for j in range(i + 1, n):
                ratio = difflib.SequenceMatcher(None, texts[i], texts[j]).ratio()
                if ratio >= 0.9:
                    sims.append(
                        {
                            "a": str(paths[i].relative_to(APP_DIR)),
                            "b": str(paths[j].relative_to(APP_DIR)),
                            "similarity": round(ratio, 3),
                        }
                    )
        if sims:
            flagged[name] = sims

    REPORTS.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS / "backend_name_similarity.json"
    out_path.write_text(json.dumps(flagged, indent=2, ensure_ascii=False), encoding="utf-8")

    print("🔎 Duplicate basename similarity report")
    print(f" - groups flagged: {len(flagged)}")
    print(f"📝 {out_path}")
    # Print a few examples
    count = 0
    for name, sims in flagged.items():
        print(f"\n{name}:")
        for item in sims[:3]:
            print(f"  {item['a']} ≈ {item['b']} (sim={item['similarity']})")
        count += 1
        if count >= 8:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
