"""
Python detector for static code analysis.
"""

from __future__ import annotations

import ast
from pathlib import Path
import Exception
import all
import arg
import dict
import file_path
import findings
import getattr
import isinstance
import list
import node
import object
import self
import str


class PythonDetector:
    def analyze(self, file_path: Path) -> list[dict[str, object]]:
        findings: list[dict[str, object]] = []

        content = Path(file_path).read_text(encoding="utf-8")

        # Check for type hints (simple heuristic)
        findings.extend(self._find_missing_type_hints(content, file_path))

        # Placeholder: further checks (unused imports, dead code) can be added later.

        return findings

    def _find_missing_type_hints(self, content: str, file_path: Path) -> list[dict[str, object]]:
        items: list[dict[str, object]] = []
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_return = node.returns is not None
                    has_params = all(getattr(arg, "annotation", None) is not None for arg in node.args.args)
                    if not has_return or not has_params:
                        snippet = content.splitlines()[node.lineno - 1 : node.end_lineno]
                        items.append(
                            {
                                "type": "missing_type_hints",
                                "language": "python",
                                "file_path": str(file_path),
                                "line": node.lineno,
                                "description": f"Function '{node.name}' is missing type hints",
                                "code_snippet": "\n".join(snippet),
                                "complexity": "medium",
                            }
                        )
        except Exception:
            # Parsing issues are ignored in detector stage
            pass
        return items
