#!/usr/bin/env python3
"""
Knowledge Graph - Lightweight project knowledge representation
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any
import data
import dict
import entities_serialized
import entity
import int
import k
import list
import relationships_serialized
import self
import set
import sorted
import source_id
import storage_path
import str
import target_id
import v


class EntityType(str, Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    VARIABLE = "variable"
    INTERFACE = "interface"
    TYPE = "type"


@dataclass
class Entity:
    id: str
    name: str
    type: EntityType
    file_path: str
    line: int
    column: int
    dependencies: set[str]
    dependents: set[str]
    metadata: dict[str, Any]


class KnowledgeGraph:
    def __init__(self, storage_path: Path | None = None) -> None:
        self.entities: dict[str, Entity] = {}
        self.relationships: dict[str, set[str]] = {}
        self.storage_path = storage_path

    def add(self, entity: Entity) -> None:
        self.entities[entity.id] = entity

    def relate(self, source_id: str, target_id: str) -> None:
        self.relationships.setdefault(source_id, set()).add(target_id)

    def to_json(self) -> str:
        # Convert non-serializable fields (Enum, set) into JSON-friendly values
        entities_serialized: dict[str, dict[str, Any]] = {}
        for k, v in self.entities.items():
            ent = asdict(v)
            # Ensure enum is serialized as its string value
            ent["type"] = v.type.value
            # Convert sets to sorted lists for stable output
            ent["dependencies"] = sorted(v.dependencies)
            ent["dependents"] = sorted(v.dependents)
            entities_serialized[k] = ent

        relationships_serialized: dict[str, list[str]] = {k: sorted(v) for k, v in self.relationships.items()}

        data: dict[str, Any] = {
            "entities": entities_serialized,
            "relationships": relationships_serialized,
        }
        return json.dumps(data, indent=2)

    def persist(self) -> None:
        if self.storage_path:
            self.storage_path.write_text(self.to_json(), encoding="utf-8")
