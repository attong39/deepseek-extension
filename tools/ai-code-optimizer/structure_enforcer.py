"""Structure Enforcer module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import libcst as cst


class StructureEnforcer:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        self.rules = self._load_config(config_path).get("structure_rules", {})

    def _load_config(self, config_path: Path) -> dict[str, Any]:
        try:
            import yaml  # type: ignore
        except Exception:
            return {}
        try:
            return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def enforce_structure(self, file_path: Path) -> bool:
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = cst.parse_module(content)
            transformer = StructureTransformer(self.rules)
            modified_tree = tree.visit(transformer)

            if modified_tree.code != content:
                file_path.write_text(modified_tree.code, encoding="utf-8")
                return True
            return False
        except Exception:
            return False


class StructureTransformer(cst.CSTTransformer):
    def __init__(self, rules: dict[str, Any]) -> None:
        self.rules = rules

    def leave_Module(self, original_node: cst.Module, updated_node: cst.Module) -> cst.Module:  # noqa: N802
        node = updated_node
        if "import_order" in self.rules:
            node = self._reorder_imports(node)
        # Member ordering hooks could be added here
        return node

    def _reorder_imports(self, node: cst.Module) -> cst.Module:
        imports: list[cst.CSTNode] = []
        other_code: list[cst.CSTNode] = []
        for statement in node.body:
            # Prefer PEP 604 unions in isinstance checks for Python 3.11+
            if isinstance(statement, cst.Import | cst.ImportFrom):
                imports.append(statement)
            else:
                other_code.append(statement)

        # Simple alphabetical sort
        def sort_key(stmt: cst.CSTNode) -> tuple[int, str]:
            if isinstance(stmt, cst.Import):
                return (0, stmt.names[0].name.value)
            if isinstance(stmt, cst.ImportFrom):
                mod = stmt.module.value if stmt.module else ""
                try:
                    return (1, str(mod))
                except Exception:
                    return (1, "")
            return (2, "")

        sorted_imports = sorted(imports, key=sort_key)
        return node.with_changes(body=sorted_imports + other_code)
import Exception
import bool
import config_path
import dict
import file_path
import imports
import int
import isinstance
import list
import other_code
import rules
import self
import sorted
import statement
import stmt
import str
import tuple
import updated_node
