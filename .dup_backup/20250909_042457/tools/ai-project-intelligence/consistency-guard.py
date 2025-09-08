#!/usr/bin/env python3
"""
Consistency Guard - Maintains cross-file consistency and finds issues
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import dep_id
import deps
import dict
import inconsistencies
import int
import k
import knowledge_graph
import len
import list
import print
import relationships
import root
import self
import set
import sorted
import source_id
import str
import tuple
import v
import x


class ConsistencyGuard:
    def __init__(self, knowledge_graph: dict[str, Any], relationships: dict[str, set[str]]) -> None:
        self.knowledge_graph = knowledge_graph
        self.relationships = relationships

    def find_inconsistencies(self) -> list[dict[str, Any]]:
        inconsistencies: list[dict[str, Any]] = []
        # Broken references: relationships pointing to missing ids
        for source_id, deps in self.relationships.items():
            for dep_id in deps:
                if dep_id not in self.knowledge_graph:
                    inconsistencies.append(
                        {
                            "type": "broken_reference",
                            "source": source_id,
                            "target": dep_id,
                            "description": f"Reference to non-existent entity: {dep_id}",
                            "severity": 9,
                        }
                    )
        return sorted(inconsistencies, key=lambda x: int(x.get("severity", 5)), reverse=True)


def _load_brain_output(root: Path) -> tuple[dict[str, Any], dict[str, set[str]]]:
    """Load persisted knowledge graph if present, else return empty structures."""
    kg_path = root / ".ai_knowledge_graph.json"
    if kg_path.exists():
        data = json.loads(kg_path.read_text(encoding="utf-8"))
        entities = data.get("entities", {})
        relationships_raw = data.get("relationships", {})
        relationships: dict[str, set[str]] = {k: set(v) for k, v in relationships_raw.items()}
        return entities, relationships
    return {}, {}


def main() -> None:
    p = argparse.ArgumentParser(description="Consistency Guard")
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--out", type=Path, default=Path("tools/ai-project-intelligence/out/inconsistencies.json"))
    args = p.parse_args()

    entities, relationships = _load_brain_output(args.root)
    guard = ConsistencyGuard(entities, relationships)
    issues = guard.find_inconsistencies()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(issues, indent=2), encoding="utf-8")
    print(f"Found {len(issues)} inconsistencies. Report: {args.out}")


if __name__ == "__main__":
    main()
