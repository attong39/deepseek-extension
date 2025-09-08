#!/usr/bin/env python3
"""
Compute a Focus Index per file to guide pruning.

Score formula:
  score = 0.4*references + 0.3*coverage + 0.2*recent_activity + 0.1*(1-dup_ratio)

Usage (from repo root):
  # Generate coverage json first
  # uv run pytest --cov=zeta_vn --cov-report=json
  # Then compute index
  # uv run python scripts/focus_index.py | head -n 100

Notes:
- references: currently a stub (0.0); can be populated via pydeps graph later.
- coverage: read from coverage.json (pytest --cov-report=json).
- recent_activity: based on last git commit time; newer -> higher.
- dup_ratio: placeholder from duplicate analyzer JSON (optional), defaults to 0.0.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
from collections import defaultdict
from contextlib import suppress
from pathlib import Path
import Exception
import any
import c
import cmd
import d
import dict
import f
import float
import hits
import int
import len
import list
import m
import max
import min
import module_map
import path
import print
import r
import ref
import rows
import s
import seg
import str
import tuple
import v
import x

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "zeta_vn"


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True, cwd=ROOT, stderr=subprocess.DEVNULL)


def git_recent_score(path: str) -> float:
    try:
        ts = run(["git", "log", "-1", "--format=%ct", path]).strip()
        if not ts:
            return 0.0
        days = max(1.0, (time.time() - float(ts)) / 86400.0)
        # Activity within ~60 days maps closer to 1.0
        return max(0.0, min(1.0, 60.0 / days))
    except Exception:
        return 0.0


def coverage_hits() -> dict[str, float]:
    # Requires pytest --cov --cov-report=json to generate coverage.json
    p = ROOT / "coverage.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text())
    except Exception:
        return {}

    hits: dict[str, float] = {}
    files = data.get("files") or {}
    for f, v in files.items():
        with suppress(Exception):
            rel = str(Path(f).resolve().relative_to(ROOT))
            executed = len(v.get("executed_lines", {}))
            missing = len(v.get("missing_lines", []))
            total = executed + missing
            hits[rel] = (executed / total) if total else 0.0
    return hits


def dup_map() -> defaultdict[str, float]:
    # Optional: if scripts/duplicate_code_analyzer.py outputs JSON, load it here.
    # Fallback to 0.0 for all files.
    return defaultdict(lambda: 0.0)


def import_graph_refs() -> defaultdict[str, int]:
    # Simple placeholder: parse import statements and count occurrences.
    # For accuracy, replace with a graph from pydeps in future.
    refs: defaultdict[str, int] = defaultdict(int)
    files = list(SRC.rglob("*.py"))
    module_map: dict[str, str] = {}
    for p in files:
        # Build module name (best-effort) relative to zeta_vn
        mod = str(p.relative_to(ROOT).with_suffix("")).replace("/", ".").replace("\\", ".")
        module_map[mod] = str(p.relative_to(ROOT))

    import_re = re.compile(r"(?:from\s+([.\w]+)\s+import|import\s+([.\w]+))")
    for f in files:
        txt: str | None = None
        with suppress(Exception):
            txt = f.read_text(errors="ignore")
        if txt is None:
            continue
        for m in import_re.finditer(txt):
            target = m.group(1) or m.group(2)
            if not target:
                continue
            # Normalize: if target maps to a file, count reference
            if target in module_map:
                refs[module_map[target]] += 1
    return refs


def main() -> None:
    cov = coverage_hits()
    dups = dup_map()
    refs = import_graph_refs()

    rows: list[tuple[float, str, float, float, float, float]] = []
    for f in SRC.rglob("*.py"):
        if any(seg.startswith("__pycache__") for seg in f.parts):
            continue
        rel = str(f.relative_to(ROOT))
        cov_s = cov.get(rel, 0.0)
        rec_s = git_recent_score(rel)
        dup_s = float(dups.get(rel, 0.0))
        # Normalize references by max to 0..1
        ref_raw = refs.get(rel, 0)
        ref_den = max(1, max(refs.values()) if refs else 1)
        ref_s = min(1.0, ref_raw / ref_den)

        score = 0.4 * ref_s + 0.3 * cov_s + 0.2 * rec_s + 0.1 * (1.0 - dup_s)
        rows.append((score, rel, ref_s, cov_s, rec_s, dup_s))

    rows.sort(key=lambda x: x[0], reverse=True)
    print("score, file, references, coverage, recent, dup_ratio")
    for s, rel, ref, c, r, d in rows:
        print(f"{s:.3f}, {rel}, {ref:.2f}, {c:.2f}, {r:.2f}, {d:.2f}")


if __name__ == "__main__":
    main()
