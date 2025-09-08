#!/usr/bin/env python3
"""Run the manifest generator and auto-stage generated files for pre-commit.

This script is intended to be used from a pre-commit hook. It runs
`tools/generate_copilot_manifest.py` and, if the manifest/summary were
created/modified, stages them with git so they become part of the commit.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import Exception
import SystemExit
import any
import bool
import exc
import int
import isinstance
import line
import list
import manifest_path
import msg
import p
import paths
import print
import str
import summary_path
import tuple
import valid

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".copilot" / "assistant_manifest.json"
SUMMARY = ROOT / ".github" / "COPILOT_SUMMARY.md"
GENERATOR = ROOT / "tools" / "generate_copilot_manifest.py"


def run_generator() -> int:
    cmd = [sys.executable, str(GENERATOR)]
    print("Running generator:", " ".join(cmd))
    res = subprocess.run(cmd, check=False)
    return res.returncode


def git_add_if_changed(paths: list[Path]) -> int:
    # Add any of the given paths to the index (staging area) if they exist
    added = 0
    for p in paths:
        if p.exists():
            # git add works whether file is tracked or new
            try:
                subprocess.run(["git", "add", str(p)], check=True)
                print(f"Staged {p}")
                added += 1
            except subprocess.CalledProcessError:
                print(f"Failed to stage {p}")
    return added


def validate_manifest_and_summary(manifest_path: Path, summary_path: Path) -> tuple[bool, str]:
    """Return (True, '') if both files are valid, otherwise (False, error_message).

    Validations:
    - manifest is parseable JSON and contains 'manifest_version' and 'rules' list
    - summary is non-empty and contains at least one markdown heading (# or ##)
    """
    if not manifest_path.exists():
        return False, f"Manifest missing: {manifest_path}"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        if "manifest_version" not in data or "rules" not in data or not isinstance(data["rules"], list):
            return (
                False,
                "Manifest JSON missing required keys (manifest_version, rules)",
            )
    except Exception as exc:
        return False, f"Invalid manifest JSON: {exc}"

    if not summary_path.exists():
        return False, f"Summary missing: {summary_path}"
    txt = summary_path.read_text(encoding="utf-8").strip()
    if not txt:
        return False, "Summary is empty"
    if not any(line.startswith("#") for line in txt.splitlines()):
        return False, "Summary contains no markdown headings"

    return True, ""


def main() -> int:
    rc = run_generator()
    if rc != 0:
        print("Generator returned non-zero:", rc)
        # do not block commit on generator failure; return non-zero to indicate failure
        return rc

    # Validate generated files before staging
    valid, msg = validate_manifest_and_summary(MANIFEST, SUMMARY)
    if not valid:
        print("Validation failed for generated files:", msg)
        return 2

    added = git_add_if_changed([MANIFEST, SUMMARY])
    if added:
        # show what is staged now
        try:
            out = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
            print("Files staged for commit:\n", out)
        except Exception:
            pass
    else:
        print("No generated files staged (no changes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
