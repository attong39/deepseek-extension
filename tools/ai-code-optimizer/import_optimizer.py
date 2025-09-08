from __future__ import annotations

from typing import Any
import Exception
import alias
import any
import bool
import dict
import e
import f
import file_path
import getattr
import hasattr
import import_node
import isinstance
import list
import new_body
import node
import object
import open
import self
import set
import statement
import str

try:
    import libcst as cst  # type: ignore
except Exception:  # pragma: no cover
    cst = None  # type: ignore


class ImportOptimizer(cst.CSTTransformer if cst is not None else object):
    """Basic import optimizer: remove unused imports.

    Note: This is a minimal implementation to start; can be extended with
    sorting, grouping, and alias normalization.
    """

    def __init__(self) -> None:
        self.imports: dict[str, Any] = {}
        self.used_imports: set[str] = set()

    def visit_Import(self, node: Any) -> None:  # noqa: N802
        for alias in node.names:
            self.imports[alias.name.value] = node

    def visit_ImportFrom(self, node: Any) -> None:  # noqa: N802
        if node.module:
            module_name = node.module.value  # type: ignore[assignment]
            if isinstance(module_name, str):
                self.imports[module_name] = node
            elif hasattr(node.module, "value"):
                self.imports[str(node.module.value)] = node  # type: ignore[arg-type]

    def visit_Name(self, node: Any) -> None:  # noqa: N802
        if node.value in self.imports:
            self.used_imports.add(node.value)

    def optimize_imports(self, tree: Any) -> Any:
        new_body: list[Any] = []
        for statement in tree.body:
            # Using tuple of classes in isinstance is correct; suppress UP038 suggestion.
            if cst is not None and isinstance(statement, (cst.Import, cst.ImportFrom)):  # noqa: UP038
                if self._is_import_used(statement):
                    new_body.append(statement)
            else:
                new_body.append(statement)
        return tree.with_changes(body=new_body)

    def _is_import_used(self, import_node: Any) -> bool:
        if cst is not None and isinstance(import_node, cst.Import):
            return any(alias.name.value in self.used_imports for alias in import_node.names)
        if cst is not None and isinstance(import_node, cst.ImportFrom):
            if import_node.module is None:
                return True
            mod_val = getattr(import_node.module, "value", None)
            if isinstance(mod_val, str):
                return mod_val in self.used_imports
            return False
        return True

    def optimize_file(self, file_path: str | Any) -> dict[str, Any]:
        """Run optimization on a single file path; returns result dict."""
        p = str(file_path)
        try:
            if cst is None:
                return {"file": p, "changed": False, "skipped": "libcst not installed"}
            with open(p, encoding="utf-8") as f:
                src = f.read()
            tree = cst.parse_module(src)
            _ = tree.visit(self)  # populate used_imports
            optimized = self.optimize_imports(tree)
            changed = optimized.code != src
            if changed:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(optimized.code)
            return {"file": p, "changed": changed}
        except Exception as e:  # noqa: BLE001
            return {"file": p, "error": str(e), "changed": False}
