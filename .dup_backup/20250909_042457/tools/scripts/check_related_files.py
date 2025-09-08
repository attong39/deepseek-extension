#!/usr/bin/env python3
"""tools/check_related_files.py

Scan danh sách file thay đổi (so với HEAD hoặc staging) và in ra
các file LIÊN QUAN cần được kiểm tra/cập nhật theo Cross-File Consistency Policy.

Usage:
  python tools/check_related_files.py --base HEAD
  python tools/check_related_files.py --staged
    python tools/check_related_files.py --base origin/main --enforce
        # exit 1 if suggestions present
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
import Exception
import SystemExit
import any
import argv
import bool
import candidate
import dict
import e
import f
import files
import int
import k
import len
import list
import name
import path
import print
import rc
import related
import rx
import s
import set
import sorted
import src
import staged
import str
import suggestions
import t
import targets
import tgt_set
import tok
import ts
import v

ROOT = Path(__file__).resolve().parents[1]

# Patterns theo kiến trúc chuẩn
PATTERNS = {
    "use_case": re.compile(r"^zeta_vn/core/(?:use_cases|domain/(?:aggregates|entities))/.*\.py$"),
    "endpoint_v1": re.compile(r"^zeta_vn/app/api/v1/.*\.py$"),
    "endpoint_v2": re.compile(r"^zeta_vn/app/api/v2/.*\.py$"),
    "repo": re.compile(r"^zeta_vn/(?:data|infrastructure)/repositories/.*\.py$"),
    "schemas": re.compile(r"^zeta_vn/app/schemas/.*\.py$"),
    "errors": re.compile(r"^zeta_vn/app/errors/.*\.py$"),
    "tests_py": re.compile(r"^tests/.*\.py$"),
    "fe_services": re.compile(r"^desktop_ai_zeta/src/services/.*\.ts$"),
    "fe_ws": re.compile(r"^desktop_ai_zeta/src/(?:api/wsSchema\.ts|services/(?:socket|trainingSocket)\.ts)$"),
    "fe_ui": re.compile(r"^desktop_ai_zeta/src/components/.*\.(?:tsx|jsx)$"),
    "fe_i18n": re.compile(r"^desktop_ai_zeta/src/i18n/(?:vi|en)\.json$"),
    "fe_errors": re.compile(r"^desktop_ai_zeta/src/api/errorCodes\.ts$"),
    "fe_tests": re.compile(r"^desktop_ai_zeta/src/(?:__tests__|tests)/.*\.(?:ts|tsx)$"),
}


# Heuristic liên kết theo "feature" (lấy từ path segment)
def extract_feature_parts(path: str) -> list[str]:
    parts = Path(path).parts
    ignore = {
        "zeta_vn",
        "app",
        "api",
        "v1",
        "v2",
        "core",
        "use_cases",
        "domain",
        "aggregates",
        "entities",
        "data",
        "repositories",
        "src",
        "services",
        "components",
        "i18n",
    }
    candidates = [p for p in parts if p not in ignore]
    return candidates


def classify(path: str) -> str | None:
    for name, rx in PATTERNS.items():
        if rx.match(path):
            return name
    return None


# Mapping: một nhóm thay đổi kéo theo nhóm khác
RELATED_BY_CLASS = {
    "use_case": {"repo", "schemas", "endpoint_v1", "endpoint_v2", "tests_py"},
    "repo": {"use_case", "tests_py"},
    "schemas": {"use_case", "endpoint_v1", "endpoint_v2", "tests_py"},
    "endpoint_v1": {
        "use_case",
        "schemas",
        "errors",
        "tests_py",
        "fe_services",
        "fe_ui",
        "fe_errors",
        "fe_tests",
    },
    "endpoint_v2": {
        "use_case",
        "schemas",
        "errors",
        "tests_py",
        "fe_services",
        "fe_ui",
        "fe_errors",
        "fe_tests",
    },
    "errors": {"endpoint_v1", "endpoint_v2", "fe_errors", "fe_i18n"},
    "fe_services": {"fe_ui", "fe_tests", "fe_i18n"},
    "fe_ws": {"fe_ui", "fe_tests", "fe_i18n"},
    "fe_ui": {"fe_services", "fe_tests", "fe_i18n"},
    "fe_errors": {"fe_i18n"},
    "tests_py": set(),
    "fe_tests": set(),
    "fe_i18n": set(),
}


def git_changed_files(base: str | None, staged: bool) -> list[str]:
    if staged:
        cmd = ["git", "diff", "--name-only", "--cached"]
    else:
        base = base or "HEAD"
        cmd = ["git", "diff", "--name-only", base]
    out = subprocess.check_output(cmd, cwd=ROOT).decode().strip().splitlines()
    return [p for p in out if p]


def all_repo_files() -> list[str]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode().splitlines()
    return out


def suggest_related(files: list[str]) -> dict[str, set[str]]:
    suggestions: dict[str, set[str]] = {}
    repo_files = all_repo_files()
    for f in files:
        cls = classify(f)
        if not cls:
            continue
        features = extract_feature_parts(f)
        related_classes = RELATED_BY_CLASS.get(cls, set())
        for rc in related_classes:
            for candidate in repo_files:
                if classify(candidate) == rc:
                    # heuristic: share feature token in path
                    if not features:
                        # if no clear feature token, include common candidates for class
                        suggestions.setdefault(f, set()).add(candidate)
                    else:
                        if any(tok in candidate for tok in features):
                            suggestions.setdefault(f, set()).add(candidate)
    return suggestions


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None, help="Git base ref (default: HEAD)")
    ap.add_argument("--staged", action="store_true", help="Use staged (index) changes")
    ap.add_argument(
        "--stage-related",
        action="store_true",
        help="Automatically git-add suggested related files (safe automation)",
    )
    ap.add_argument(
        "--todo",
        action="store_true",
        help=(
            "Insert a short TODO annotation at the top of each suggested related file\n"
            "(only if the file exists and doesn't already contain the marker)."
        ),
    )
    ap.add_argument("--json", action="store_true", help="Output JSON")
    ap.add_argument(
        "--enforce",
        action="store_true",
        help="Exit non-zero if suggestions exist (CI enforce mode)",
    )
    args = ap.parse_args(argv)

    try:
        changed = git_changed_files(args.base, args.staged)
    except subprocess.CalledProcessError:
        print(
            "Cannot detect git repo or run git diff. Tip: run inside repository.",
            file=sys.stderr,
        )
        return 0

    sugg = suggest_related(changed)

    if args.json:
        print(json.dumps({k: sorted(v) for k, v in sugg.items()}, indent=2, ensure_ascii=False))
    else:
        if not changed:
            print("No changes detected.")
            return 0
        print("Changed files:")
        for f in changed:
            print(f"  - {f}")
        print("\nRELATED files to review/update:")
        if not sugg:
            print("  (none by heuristic)")
        else:
            for src, related in sugg.items():
                print(f"* {src}")
                for t in sorted(related):
                    print(f"    → {t}")

    if args.enforce and sugg:
        print("\nEnforce mode: suggestions found -> exiting non-zero")
        return 2

    # Safe automation helpers: stage related files and optionally insert TODO markers.
    if (args.stage_related or args.todo) and sugg:
        # flatten unique targets
        targets: list[str] = sorted({t for tgt_set in sugg.values() for t in tgt_set})
        if args.todo:
            insert_todo_annotations(targets, sugg)
        if args.stage_related:
            stage_files(targets)

    return 0


def insert_todo_annotations(targets: list[str], sugg: dict[str, set[str]]) -> None:
    """Insert a small TODO annotation at the top of each target file.

    - Only acts on files that exist in the repository working tree.
    - Avoids duplicating the annotation if already present.
    - Chooses comment style based on file extension.
    """
    marker = "# RELATED_CHANGE_AUTOTODO"
    for t in targets:
        p = ROOT / t
        if not p.exists() or not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            # skip binary or unreadable files
            continue

        if marker in text.splitlines()[:5]:
            continue

        # build message listing sources that suggested this target
        sources = [s for s, ts in sugg.items() if t in ts]
        short_sources = ", ".join(sources[:3])
        if len(sources) > 3:
            short_sources += f" (+{len(sources) - 3} more)"

        ext = p.suffix.lower()
        if ext == ".py":
            header = f"{marker}\n# TODO: Review/update because of changes in: {short_sources}\n\n"
        elif ext in {".ts", ".js", ".tsx", ".jsx", ".css", ".scss", ".json"}:
            header = f"// {marker}\n// TODO: Review/update because of changes in: {short_sources}\n\n"
        else:
            # fallback to hash comment
            header = f"{marker}\n# TODO: Review/update because of changes in: {short_sources}\n\n"

        try:
            p.write_text(header + text, encoding="utf-8")
            print(f"Inserted TODO annotation into: {t}")
        except Exception as e:
            print(f"Failed inserting TODO into {t}: {e}")


def stage_files(targets: list[str]) -> None:
    """Stage (git add) the provided target files.

    - Runs `git add` for each file inside the repository root.
    - Fails fast on subprocess errors but does not raise (prints error).
    """
    for t in targets:
        p = Path(t)
        if not (ROOT / p).exists():
            print(f"Skipping missing file: {t}")
            continue
        try:
            subprocess.check_call(["git", "add", str(t)], cwd=ROOT)
            print(f"Staged: {t}")
        except subprocess.CalledProcessError as e:
            print(f"git add failed for {t}: {e}")


if __name__ == "__main__":
    raise SystemExit(main())
