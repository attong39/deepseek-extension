#!/usr/bin/env python3
"""
Project graph utilities: write simple GraphViz DOT for dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import deps
import dict
import k
import lines
import list
import out_path
import print
import src
import str
import targets
import tgt
import v


def write_dot(deps: dict[str, list[str]], out_path: Path) -> None:
    lines: list[str] = ["digraph G {"]
    for src, targets in deps.items():
        src_node = src.replace("\\", "/")
        for tgt in targets:
            tgt_node = tgt.replace("\\", "/")
            lines.append(f'  "{src_node}" -> "{tgt_node}";')
    lines.append("}")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, default=Path("tools/ai-project-analyzer/out/deps.dot"))
    args = p.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    graph = {k: list(v) for k, v in data.get("dependency_graph", {}).items()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_dot(graph, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
