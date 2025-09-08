#!/usr/bin/env python3
"""Generate a machine-readable manifest and a short human summary for Copilot use.

This script scans a small set of canonical files under `.github/` and project prompts
to extract required rules/checks and produce two outputs:

- `./.copilot/assistant_manifest.json` (machine-readable)
- `./.github/COPILOT_SUMMARY.md` (human-friendly short summary)

Usage:
  python tools/generate_copilot_manifest.py        # generate and overwrite
  python tools/generate_copilot_manifest.py --check  # check-only, exit non-zero if out-of-date

The extraction is heuristic: it looks for headings and common keywords (e.g. "Checklist",
"Bắt buộc", "mypy", "ruff", "pytest", "tools/check_related_files.py"). If the
script cannot find explicit rules it falls back to a small set of defaults consistent
with repository guidelines.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
import Exception
import SystemExit
import all_cmds
import any
import bool
import c
import cmds
import commands
import dict
import enumerate
import f
import i
import indexed
import indexed_files
import int
import line
import list
import ln
import manifest_path
import new_summary_text
import p
import path
import print
import r
import s
import sl
import snippets_map
import str
import summary_path
import tuple

ROOT = Path(__file__).resolve().parents[1]
GITHUB_DIR = ROOT / ".github"
PROMPTS_DIR = GITHUB_DIR / "prompts"
FILES_TO_INDEX = [
    GITHUB_DIR / "copilot-instructions.md",
    GITHUB_DIR / "dependabot.yml",
    GITHUB_DIR / "CODEOWNERS",
    PROMPTS_DIR / "GUIDE.md",
    PROMPTS_DIR / "PROJECT_MAP.md",
]

OUT_MANIFEST = ROOT / ".copilot" / "assistant_manifest.json"
OUT_SUMMARY = ROOT / ".github" / "COPILOT_SUMMARY.md"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_headings_and_snippets(text: str) -> list[str]:
    lines = text.splitlines()
    snippets: list[str] = []
    for i, ln in enumerate(lines):
        if re.match(r"^#{1,3}\s+", ln):
            # heading with some context
            ctx = ln.strip()
            # grab following up-to-3 lines as context
            following = " ".join(line.strip() for line in lines[i + 1 : i + 4])
            snippets.append(f"{ctx} — {following}".strip())
        elif re.search(
            r"(?i)checklist|bắt buộc|required|mypy|ruff|pytest|pre-commit|PROJECT_MAP|check_related_files",
            ln,
        ):
            snippets.append(ln.strip())
    return snippets


def find_command_mentions(text: str) -> list[str]:
    cmds: list[str] = []
    # common commands we want to capture
    patterns = [
        r"python\s+tools/check_related_files.py",
        r"ruff\s+check",
        r"mypy\b",
        r"pytest\b",
        r"npm run api:gen",
        r"pre-commit",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            cmds.append(m.group(0))
    return cmds


def build_manifest(indexed_files: list[str], snippets_map: dict[str, list[str]], commands: list[str]) -> dict:
    rules = []

    # Heuristic rules from snippets; this is conservative and idempotent.
    if any("check_related_files" in s for sl in snippets_map.values() for s in sl):
        rules.append(
            {
                "id": "cfcp",
                "title": "Cross-File Consistency Policy (CFCP)",
                "description": "Run tools/check_related_files.py and update related files (endpoints, repos, schemas, tests, i18n) before PR.",
                "required": True,
                "checks": ["python tools/check_related_files.py --staged"],
            }
        )

    # Lint/type/tests rule
    rules.append(
        {
            "id": "lint_type_test",
            "title": "Lint / Type / Tests",
            "description": "Ensure changes pass ruff, mypy --strict and pytest where applicable.",
            "required": True,
            "checks": ["ruff check .", "mypy --config-file mypy.ini .", "pytest -q"],
        }
    )

    # Project map rule
    rules.append(
        {
            "id": "project_map",
            "title": "PROJECT_MAP sync",
            "description": "New files must be listed in .github/prompts/PROJECT_MAP.md (run update_project_map.py).",
            "required": True,
            "checks": ["python .github/prompts/update_project_map.py"],
        }
    )

    # Dependabot note
    if any("dependabot" in f for f in indexed_files):
        rules.append(
            {
                "id": "dependabot",
                "title": "Dependabot updates",
                "description": "Dependabot configured for pip/npm/github-actions (weekly). Review dependency PRs and labels.",
                "required": False,
                "checks": [],
            }
        )

    # Add captured commands as suggested checks
    if commands:
        rules.append(
            {
                "id": "suggested_commands",
                "title": "Suggested checks extracted",
                "description": "Commands heuristically extracted from repository docs.",
                "required": False,
                "checks": commands,
            }
        )

    manifest = {
        "manifest_version": "1.0",
        "last_generated": datetime.now(UTC).isoformat(),
        "indexed_files": indexed_files,
        "rules": rules,
    }
    return manifest


def build_summary(manifest: dict, snippets_map: dict[str, list[str]]) -> str:
    lines: list[str] = []
    lines.append("# COPILOT SUMMARY (auto-generated)")
    lines.append(
        "This file is generated by `tools/generate_copilot_manifest.py`. It summarises repository rules that the assistant and developers should follow."
    )
    lines.append("")
    for r in manifest["rules"]:
        lines.append(f"## {r['title']}")
        lines.append(r["description"])
        if r.get("checks"):
            lines.append("**Checks:**")
            for c in r["checks"]:
                lines.append(f"- `{c}`")
        lines.append("")

    lines.append("---")
    lines.append("### Extracted snippets from source files (for maintainers)")
    for f, snippets in snippets_map.items():
        lines.append(f"#### {f}")
        if snippets:
            for s in snippets[:10]:
                lines.append(f"- {s}")
        else:
            lines.append("- (no explicit snippets found)")
        lines.append("")

    return "\n".join(lines)


def gather_indexed_data() -> tuple[list[str], dict[str, list[str]], list[str]]:
    indexed: list[str] = []
    snippets_map: dict[str, list[str]] = {}
    all_cmds: list[str] = []

    for p in FILES_TO_INDEX:
        try:
            rel = p.relative_to(ROOT)
            indexed.append(rel.as_posix())
        except Exception:
            indexed.append(str(p).replace("\\", "/"))
        text = read_text(p)
        snippets = extract_headings_and_snippets(text)
        key = p.relative_to(ROOT).as_posix() if p.exists() else str(p).replace("\\", "/")
        snippets_map[key] = snippets
        for c in find_command_mentions(text):
            if c not in all_cmds:
                all_cmds.append(c)

    return indexed, snippets_map, all_cmds


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="Check only; exit 0 if up-to-date, 2 if out-of-date",
    )
    args = ap.parse_args()
    indexed, snippets_map, all_cmds = gather_indexed_data()

    manifest = build_manifest(indexed, snippets_map, all_cmds)
    summary = build_summary(manifest, snippets_map)

    OUT_MANIFEST.parent.mkdir(exist_ok=True)
    OUT_SUMMARY.parent.mkdir(exist_ok=True)

    new_manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False)

    if args.check:
        ok = compare_existing_with_new(OUT_MANIFEST, OUT_SUMMARY, new_manifest_text, summary)
        if ok:
            print("Manifest and summary are up-to-date.")
            return 0
        print("Manifest or summary are out-of-date.")
        return 2

    OUT_MANIFEST.write_text(new_manifest_text, encoding="utf-8")
    OUT_SUMMARY.write_text(summary, encoding="utf-8")
    print(f"Wrote {OUT_MANIFEST} and {OUT_SUMMARY}")
    return 0


def compare_existing_with_new(
    manifest_path: Path,
    summary_path: Path,
    new_manifest_text: str,
    new_summary_text: str,
) -> bool:
    """Return True if both manifest and summary match the new versions.

    The manifest comparison ignores the `last_generated` timestamp.
    """
    try:
        if not manifest_path.exists() or not summary_path.exists():
            return False
        old = json.loads(manifest_path.read_text(encoding="utf-8"))
        new = json.loads(new_manifest_text)
        old.pop("last_generated", None)
        new.pop("last_generated", None)
        if old != new:
            return False
        old_summary = summary_path.read_text(encoding="utf-8").strip()
        if old_summary != new_summary_text.strip():
            return False
        return True
    except Exception:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
