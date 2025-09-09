from __future__ import annotations
import ast
from pathlib import Path
from typing import Set

# Built-in symbols that don't need imports
BUILTINS = {
    'int', 'str', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
    'len', 'print', 'range', 'enumerate', 'sorted', 'sum', 'max', 'min',
    'any', 'all', 'isinstance', 'hasattr', 'getattr', 'setattr',
    'open', 'input', 'abs', 'chr', 'ord', 'round', 'type', 'id',
    'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
    'AttributeError', 'ImportError', 'OSError', 'FileNotFoundError',
    'PermissionError', 'KeyboardInterrupt', 'SyntaxError', 'UnicodeDecodeError',
    'True', 'False', 'None', '__name__', '__file__', '__doc__'
}

# Common variable patterns to exclude
COMMON_VARS = {
    'self', 'cls', 'args', 'kwargs', 'e', 'f', 'i', 'j', 'k', 'v', 'x', 'y', 'z',
    'item', 'key', 'value', 'result', 'data', 'line', 'lines', 'file', 'path',
    'name', 'filename', 'content', 'text', 'msg', 'message', 'error', 'err',
    'response', 'request', 'payload', 'params', 'config', 'settings', 'options'
}

class PyImportAnalyzer:
    def __init__(self, src_path: Path):
        self.path = src_path
        try:
            self.text = src_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Try with different encodings
            try:
                self.text = src_path.read_text(encoding="latin-1")
            except UnicodeDecodeError:
                # If all else fails, read with error handling
                self.text = src_path.read_text(encoding="utf-8", errors="ignore")
        
        try:
            self.tree = ast.parse(self.text)
        except SyntaxError:
            # Skip files that aren't valid Python
            self.tree = ast.Module(body=[], type_ignores=[])
        
        self._locals: Set[str] = set()
        self._imported: Set[str] = set()
        self._collect_defs()

    def _collect_defs(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._imported.add(alias.asname or alias.name.split(".", 1)[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self._imported.add(alias.asname or alias.name)
                # cũng đánh dấu module gốc (vd: from x import y -> x)
                if node.module:
                    self._imported.add(node.module.split(".", 1)[0])
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self._locals.add(node.name)
            elif isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        self._locals.add(t.id)

    def missing_symbols(self) -> Set[str]:
        """Tìm symbols có thể là module/class cần import."""
        candidates: Set[str] = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                name = node.id
                
                # Skip if already defined/imported/builtin
                if (name in BUILTINS or name in self._locals or 
                    name in self._imported or name in COMMON_VARS):
                    continue
                
                # Skip private symbols
                if name.startswith("_"):
                    continue
                
                # Skip single letters (likely loop variables)
                if len(name) <= 1:
                    continue
                
                # Only consider PascalCase (classes) or known modules
                if name[0].isupper():
                    candidates.add(name)
                elif name in {'pandas', 'numpy', 'requests', 'json', 'os', 'sys', 'pathlib', 'typing', 'datetime', 're', 'collections', 'itertools', 'functools', 'asyncio'}:
                    candidates.add(name)
                    
        return candidates