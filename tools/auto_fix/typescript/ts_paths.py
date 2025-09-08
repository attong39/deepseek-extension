from __future__ import annotations

import json
import os
from pathlib import Path
import dict
import ext
import len
import list
import p
import pat
import prefix
import self
import spec
import str
import suffix
import t
import target
import targets
import tsconfig_path

class TSPaths:
    def __init__(self, tsconfig_path: Path):
        self.base = Path(".")
        self.paths: dict[str, list[str]] = {}
        self._load(tsconfig_path)

    def _load(self, p: Path) -> None:
        if not p.exists():
            return
        data = json.loads(p.read_text(encoding="utf-8"))
        compiler = data.get("compilerOptions", {})
        base_url = compiler.get("baseUrl")
        if base_url:
            self.base = (p.parent / base_url).resolve()
        paths = compiler.get("paths") or {}
        self.paths = dict(paths)

    def resolve(self, spec: str) -> str | None:
        """
        Trả về đường dẫn tương đối nếu spec khớp alias, ngược lại None.
        ex: @core/utils -> src/core/utils.tsx (theo mapping)
        """
        for pat, targets in self.paths.items():
            if "*" in pat:
                if self._resolve_wildcard(spec, pat, targets):
                    return self._resolve_wildcard(spec, pat, targets)
            elif spec == pat:
                for t in targets:
                    absf = (self.base / t).with_suffix("")
                    for ext in (".tsx", ".ts", ".jsx", ".js", "/index.tsx", "/index.ts"):
                        if (Path(str(absf) + ext)).exists():
                            return self._to_rel(Path(str(absf) + ext))
        return None

    def _resolve_wildcard(self, spec: str, pat: str, targets: list[str]) -> str | None:
        prefix, suffix = pat.split("*", 1)
        if spec.startswith(prefix) and spec.endswith(suffix):
            mid = spec[len(prefix):len(spec) - len(suffix)]
            for t in targets:
                cand = t.replace("*", mid)
                absf = (self.base / cand).with_suffix("")
                for ext in (".tsx", ".ts", ".jsx", ".js", "/index.tsx", "/index.ts"):
                    if (Path(str(absf) + ext)).exists():
                        return self._to_rel(Path(str(absf) + ext))
        return None

    def _to_rel(self, target: Path) -> str:
        rel = os.path.relpath(target.with_suffix(""), Path("."))
        rel = rel.replace("\\", "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return rel
