#!/usr/bin/env python3
"""
Unit tests for ConsistencyGuard functionality
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import patch
import any
import dependencies
import dict
import entity_id
import entity_type
import i
import item
import len
import list
import name
import object
import path
import r
import set
import str
import test_data
import tmp_path


def load_module_by_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT / "tools" / "ai-project-intelligence"

CONSISTENCY_PATH = TOOLS_DIR / "consistency-guard.py"
KG_PATH = TOOLS_DIR / "knowledge-graph.py"

consistency_mod = load_module_by_path("consistency_guard_mod", CONSISTENCY_PATH)
kg_mod = load_module_by_path("kg_mod", KG_PATH)

ConsistencyGuard = consistency_mod.ConsistencyGuard
guard_main = consistency_mod.main
ProjectEntity = kg_mod.Entity
ProjectEntityType = kg_mod.EntityType


def create_test_entity(
    entity_id: str,
    name: str,
    entity_type: ProjectEntityType,
    dependencies: list[str] | None = None,
):
    return ProjectEntity(
        id=entity_id,
        name=name,
        type=entity_type,
        file_path=str(Path("test.py")),
        line=1,
        column=1,
        dependencies=set(dependencies) if dependencies else set(),
        dependents=set(),
        metadata={},
    )


def test_find_broken_references():
    knowledge_graph = {
        "class:User": create_test_entity("class:User", "User", ProjectEntityType.CLASS),
        "func:get_user": create_test_entity("func:get_user", "get_user", ProjectEntityType.FUNCTION, ["class:User"]),
        "func:save_user": create_test_entity(
            "func:save_user",
            "save_user",
            ProjectEntityType.FUNCTION,
            ["class:User", "class:Database"],
        ),
    }
    relationships = {
        "func:get_user": {"class:User"},
        "func:save_user": {"class:User", "class:Database"},
    }

    guard = ConsistencyGuard(knowledge_graph, relationships)
    inconsistencies = guard.find_inconsistencies()

    broken_refs = [i for i in inconsistencies if i["type"] == "broken_reference"]
    assert len(broken_refs) == 1
    assert broken_refs[0]["target"] == "class:Database"
    assert broken_refs[0]["source"] == "func:save_user"
    assert broken_refs[0]["severity"] == 9


def test_find_broken_references_empty_graph():
    guard = ConsistencyGuard({}, {})
    inconsistencies = guard.find_inconsistencies()
    assert inconsistencies == []


def test_find_broken_references_no_relationships():
    knowledge_graph = {
        "class:User": create_test_entity("class:User", "User", ProjectEntityType.CLASS),
    }
    guard = ConsistencyGuard(knowledge_graph, {})
    inconsistencies = guard.find_inconsistencies()
    assert inconsistencies == []


def test_find_broken_references_multiple_broken():
    knowledge_graph = {
        "class:User": create_test_entity("class:User", "User", ProjectEntityType.CLASS),
    }
    relationships = {
        "func:get_user": {"class:User", "class:Database"},
        "func:save_user": {"class:User", "class:Logger"},
    }
    guard = ConsistencyGuard(knowledge_graph, relationships)
    inconsistencies = guard.find_inconsistencies()

    broken_refs = [i for i in inconsistencies if i["type"] == "broken_reference"]
    assert len(broken_refs) == 2
    assert {r["target"] for r in broken_refs} == {"class:Database", "class:Logger"}


def test_consistency_guard_cli(tmp_path: Path):
    test_data: dict[str, object] = {
        "entities": {
            "class:User": {
                "id": "class:User",
                "name": "User",
                "type": "class",
                "file_path": "test.py",
                "line": 1,
                "column": 1,
                "dependencies": [],
                "dependents": [],
                "metadata": {},
            }
        },
        "relationships": {"func:get_user": ["class:User", "class:Database"]},
    }

    kg_file = tmp_path / ".ai_knowledge_graph.json"
    kg_file.write_text(json.dumps(test_data), encoding="utf-8")

    with patch("sys.argv", ["consistency-guard.py", "--root", str(tmp_path)]):
        guard_main()

    output_file = tmp_path / "tools" / "ai-project-intelligence" / "out" / "inconsistencies.json"
    assert output_file.exists()
    results = json.loads(output_file.read_text(encoding="utf-8"))
    assert any("class:Database" in json.dumps(item) for item in results)
