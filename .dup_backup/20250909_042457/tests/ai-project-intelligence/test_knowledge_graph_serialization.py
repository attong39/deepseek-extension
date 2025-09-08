#!/usr/bin/env python3
"""Tests for KnowledgeGraph JSON serialization/persist."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load_module_by_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT / "tools" / "ai-project-intelligence"

KG_PATH = TOOLS_DIR / "knowledge-graph.py"
kg_mod = load_module_by_path("kg_mod", KG_PATH)

KnowledgeGraph = kg_mod.KnowledgeGraph
Entity = kg_mod.Entity
EntityType = kg_mod.EntityType


def test_to_json_and_persist(tmp_path: Path) -> None:
    storage = tmp_path / ".ai_kg.json"
    kg = KnowledgeGraph(storage_path=storage)

    e = Entity(
        id="py:sample.py",
        name="sample",
        type=EntityType.MODULE,
        file_path="sample.py",
        line=1,
        column=1,
        dependencies={"py:dep.py"},
        dependents=set(),
        metadata={"k": 1},
    )
    kg.add(e)
    kg.relate("py:sample.py", "py:dep.py")

    s = kg.to_json()
    data = json.loads(s)
    assert "entities" in data and "relationships" in data
    ent = data["entities"]["py:sample.py"]
    assert ent["type"] == "module"
    assert isinstance(ent["dependencies"], list)
    assert sorted(data["relationships"]["py:sample.py"]) == ["py:dep.py"]

    # Ensure persist writes the file
    kg.persist()
    assert storage.exists()
    persisted = json.loads(storage.read_text(encoding="utf-8"))
    assert persisted["entities"]["py:sample.py"]["type"] == "module"
import isinstance
import list
import name
import path
import set
import sorted
import str
import tmp_path
