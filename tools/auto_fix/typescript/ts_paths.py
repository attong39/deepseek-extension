from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional


class TSPaths:
    """TypeScript path mapping resolver using tsconfig.json paths."""
    
    def __init__(self, tsconfig_path: str = "apps/desktop/tsconfig.json"):
        self.tsconfig_path = Path(tsconfig_path)
        self.paths_map: dict[str, list[str]] = {}
        self.base_url = ""
        self._load_paths()
    
    def _load_paths(self) -> None:
        """Load paths from tsconfig.json."""
        if not self.tsconfig_path.exists():
            return
            
        try:
            config = json.loads(self.tsconfig_path.read_text(encoding="utf-8"))
            compiler_options = config.get("compilerOptions", {})
            self.base_url = compiler_options.get("baseUrl", "")
            self.paths_map = compiler_options.get("paths", {})
        except (json.JSONDecodeError, KeyError):
            pass
    
    def resolve(self, symbol: str) -> Optional[Path]:
        """
        Resolve a symbol to a file path using TypeScript path mapping.
        
        Args:
            symbol: The symbol/module name to resolve
            
        Returns:
            Path to the resolved file, or None if not found
        """
        # Direct symbol match
        if symbol in self.paths_map:
            return self._resolve_path_targets(self.paths_map[symbol])
        
        # Pattern matching (e.g., "@components/*" -> ["src/components/*"])
        for pattern, targets in self.paths_map.items():
            if "*" in pattern:
                prefix = pattern.split("*")[0]
                if symbol.startswith(prefix):
                    suffix = symbol[len(prefix):]
                    resolved_targets = [t.replace("*", suffix) for t in targets]
                    return self._resolve_path_targets(resolved_targets)
        
        return None
    
    def _resolve_path_targets(self, targets: list[str]) -> Optional[Path]:
        """Resolve path targets to actual files."""
        base_path = self.tsconfig_path.parent
        if self.base_url:
            base_path = base_path / self.base_url
        
        for target in targets:
            target_path = base_path / target
            
            # Try different extensions
            extensions = [".ts", ".tsx", ".js", ".jsx"]
            
            # Direct file
            for ext in extensions:
                file_path = target_path.with_suffix(ext)
                if file_path.exists():
                    return file_path
            
            # Index file
            for ext in extensions:
                index_path = target_path / f"index{ext}"
                if index_path.exists():
                    return index_path
        
        return None