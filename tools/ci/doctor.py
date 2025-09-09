from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_WORKFLOWS = [
    ".github/workflows/ci-final-gates.yml",
    ".github/workflows/consistency-guard.yml",
]
REQUIRED_DOCS = [
    "docs/READINESS_CHECKLIST.md",
    "docs/CONSISTENCY_GUARD.md",
    "docs/AUTO_FIX.md",
]
REQUIRED_FILES = [
    "apps/backend/app/main.py",
    "apps/desktop/src/main.tsx",
    "tools/consistency/run_all.py",
    "tools/auto_fix/cli.py",
]

def exists(p: str) -> bool:
    return Path(p).exists()

def main() -> int:
    issues = []
    for w in REQUIRED_WORKFLOWS:
        if not exists(w):
            issues.append(f"missing workflow: {w}")
    for d in REQUIRED_DOCS:
        if not exists(d):
            issues.append(f"missing doc: {d}")
    for f in REQUIRED_FILES:
        if not exists(f):
            issues.append(f"missing file: {f}")

    # Check git hooks path is set (optional, non-block)
    hooks_cfg = (Path(".git") / "config").read_text(encoding="utf-8") if Path(".git/config").exists() else ""
    hooks_ok = "hooksPath = .githooks" in hooks_cfg

    report = {
        "workflows_ok": all(exists(w) for w in REQUIRED_WORKFLOWS),
        "docs_ok": all(exists(d) for d in REQUIRED_DOCS),
        "core_files_ok": all(exists(f) for f in REQUIRED_FILES),
        "git_hooks_configured": hooks_ok,
        "issues": issues,
    }

    # Create reports directory if it doesn't exist
    reports_dir = Path("reports/ci")
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Write report to file
    report_file = reports_dir / "doctor.json"
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Print report to stdout
    print(json.dumps(report, indent=2))

    return 0 if not issues else 1

if __name__ == "__main__":
    sys.exit(main())
