#!/usr/bin/env python3
"""
consolidation_plan_builder.py

Build a consolidation plan from the latest consolidation audit:
- Select canonical files for each exact duplicate group
- Provide recommendations for near-duplicates
- Output a structured JSON plan and a readable Markdown summary

Usage (PowerShell):
    python scripts/consolidation_plan_builder.py \
        --audit-root reports/consolidation_audit \
        --out-dir reports/consolidation_plan
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import Exception
import SystemExit
import any
import data
import dict
import enumerate
import exact_dup
import f
import fh
import files
import glist
import groups
import h
import i
import int
import item
import lang
import len
import lines
import list
import near_dup
import object
import path
import paths
import print
import r
import seg
import sorted
import str
import tuple
import x


def find_latest_audit_dir(audit_root: Path) -> Path | None:
    if not audit_root.exists():
        return None
    subs = [p for p in audit_root.iterdir() if p.is_dir()]
    if not subs:
        return None
    # sort by name descending (timestamp-like), fallback to mtime
    subs.sort(key=lambda p: (p.name, p.stat().st_mtime), reverse=True)
    return subs[0]


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def lang_of(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".py":
        return "py"
    if ext in {".ts", ".tsx"}:
        return "ts"
    if ext in {".js", ".jsx", ".mjs", ".cjs"}:
        return "js"
    return "other"


def score_path_for_canonical(path: str) -> tuple[int, int]:
    """Higher is better. Second value is negative path length as tie-breaker (shorter path preferred)."""
    p = path.replace("\\", "/")
    score = 0
    # Penalize generated/output directories strongly
    if any(
        seg in p
        for seg in [
            "/node_modules/",
            "/dist/",
            "/build/",
            "/out/",
            "/.venv/",
            "/__pycache__/",
            "/.mypy_cache/",
            "/.ruff_cache/",
            "/.pytest_cache/",
        ]
    ):
        score -= 100
    # Penalize reports/docs/tests relative to source code
    if "/reports/" in p or "/dedupe_reports/" in p:
        score -= 50
    if "/tests/" in p or "/test/" in p:
        score -= 10
    # Python preference
    if "/apps/backend/core/" in p:
        score += 50
    elif "/apps/backend/" in p:
        score += 40
    elif "/src/core/" in p:
        score += 30
    # TS/JS preference
    if "/packages/shared/src/" in p:
        score += 45
    elif "/extension/" in p:
        score += 35
    elif "/apps/desktop/" in p:
        score += 25
    elif "/apps/zeta-ai-agent/" in p:
        score += 20
    # Generic fallback: prefer under apps/ or packages/
    if "/apps/" in p:
        score += 5
    if "/packages/" in p:
        score += 5
    # prefer stable config locations
    if "/config/" in p:
        score += 5
    # Tie-breaker: shorter path better
    return score, -len(p)


def choose_canonical(paths: list[str]) -> str:
    ranked = sorted(paths, key=lambda x: score_path_for_canonical(x), reverse=True)
    return ranked[0]


def build_plan(exact_dup: dict[str, list[str]], near_dup: dict[str, list[str]]):
    plan: dict[str, list[dict[str, object]]] = {"exact_groups": [], "near_groups": []}

    for h, files in exact_dup.items():
        # Split by extension; create one plan item per ext subtype
        groups: dict[str, list[str]] = {}
        for f in files:
            groups.setdefault(lang_of(f), []).append(f)
        for lang, glist in groups.items():
            if len(glist) < 2:
                continue
            canonical = choose_canonical(glist)
            redundant = [p for p in glist if p != canonical]
            rec = "delete_redundant"
            note = "Replace references with canonical path; create re-export (TS) or shim module (Python) if needed."
            plan["exact_groups"].append(
                {
                    "hash": h,
                    "language": lang,
                    "canonical": canonical,
                    "redundant": redundant,
                    "recommendation": rec,
                    "notes": note,
                }
            )

    for fh, files in near_dup.items():
        # Only generate a review item; do not auto-choose canonical for near duplicates
        langs = sorted({lang_of(f) for f in files})
        plan["near_groups"].append(
            {
                "fingerprint": fh,
                "languages": langs,
                "files": sorted(files),
                "recommendation": "review_and_refactor",
                "notes": "Consider merging logic into a shared module (packages/shared) or unify one implementation.",
            }
        )

    return plan


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md(path: Path, plan) -> None:
    lines: list[str] = []
    lines.append("# Consolidation Plan\n")
    lines.append(f"- Exact duplicate groups: {len(plan.get('exact_groups', []))}")
    lines.append(f"- Near-duplicate groups: {len(plan.get('near_groups', []))}\n")
    if plan.get("exact_groups"):
        lines.append("## Exact Duplicates\n")
        for i, item in enumerate(plan["exact_groups"], 1):
            lines.append(f"### Group {i}")
            lines.append(f"- Language: {item['language']}")
            lines.append(f"- Canonical: `{item['canonical']}`")
            lines.append("- Redundant:")
            for r in item["redundant"]:
                lines.append(f"  - `{r}`")
            lines.append(f"- Recommendation: {item['recommendation']}")
            lines.append(f"- Notes: {item['notes']}\n")
    if plan.get("near_groups"):
        lines.append("## Near Duplicates\n")
        for i, item in enumerate(plan["near_groups"], 1):
            lines.append(f"### Group {i}")
            lines.append(f"- Languages: {', '.join(item['languages'])}")
            lines.append("- Files:")
            for f in item["files"]:
                lines.append(f"  - `{f}`")
            lines.append(f"- Recommendation: {item['recommendation']}")
            lines.append(f"- Notes: {item['notes']}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Build consolidation plan from latest audit")
    ap.add_argument(
        "--audit-root", type=str, default="reports/consolidation_audit", help="Root folder where audits are written"
    )
    ap.add_argument("--out-dir", type=str, default="reports/consolidation_plan", help="Output directory for plan")
    args = ap.parse_args()

    audit_root = Path(args.audit_root)
    latest = find_latest_audit_dir(audit_root)
    if not latest:
        print(f"No audit found under {audit_root}.")
        return 2

    exact_path = latest / "duplicates.json"
    near_path = latest / "near_duplicates.json"
    exact = read_json(exact_path) or {}
    near = read_json(near_path) or {}

    plan = build_plan(exact, near)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = out_dir / "plan.json"
    md_out = out_dir / "plan.md"
    write_json(json_out, plan)
    write_md(md_out, plan)

    print("Consolidation plan generated.")
    print(f"JSON: {json_out}")
    print(f"Markdown: {md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
