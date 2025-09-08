#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from apps.backend.tools.ports_tools import SNAPSHOT_PATH, gather_manifest, load_snapshot
import int
import lines
import list
import m
import p
import print
import sorted
import str
import x

DOC = Path("docs/PORTS_REGISTRY.md")


def main() -> int:
    """Generate ports documentation from manifest."""
    if SNAPSHOT_PATH.exists():
        data = load_snapshot(SNAPSHOT_PATH)
    else:
        manifest = gather_manifest()
        data = {
            "package": manifest.package,
            "protocols": [
                {
                    "name": p.name,
                    "module": p.module,
                    "category": p.category,
                    "methods": [{"name": m.name, "signature": m.signature} for m in p.methods],
                }
                for p in manifest.protocols
            ],
        }

    groups = defaultdict(list)
    for p in data["protocols"]:
        cat = p.get("category") or "uncategorized"
        groups[cat].append(p)

    lines: list[str] = []
    lines.append("# Ports Registry\n")
    lines.append(f"_Package_: `{data['package']}`\n")
    lines.append("## Mục lục\n")
    for cat in sorted(groups):
        lines.append(f"- [{cat}](#{cat})")
    lines.append("")

    for cat in sorted(groups):
        lines.append(f"## {cat}\n")
        for p in sorted(groups[cat], key=lambda x: (x["module"], x["name"])):
            lines.append(f"### {p['name']}  \n`{p['module']}.{p['name']}`")
            for m in p.get("methods", []):
                lines.append(f"- **{m['name']}**`{m['signature']}`")
            lines.append("")

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text("\n".join(lines), encoding="utf-8")
    print(f"[gen_ports_docs] Wrote {DOC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
