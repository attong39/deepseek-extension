"""Find desktop router files, backup, create branch, and insert ASRPanel import+route idempotently.

Usage: run from repo root using project's venv python.
"""

from __future__ import annotations

import datetime
import re
import shutil
import subprocess
from pathlib import Path
import Exception
import cand
import e
import enumerate
import i
import ln
import print
import str

REPO_ROOT = Path(__file__).resolve().parents[1]
DESKTOP_SRC = REPO_ROOT / "desktop_ai_zeta" / "src"
CANDIDATES = [
    DESKTOP_SRC / "router.tsx",
    DESKTOP_SRC / "routes.tsx",
    DESKTOP_SRC / "App.tsx",
    DESKTOP_SRC / "main.tsx",
]
BRANCH = "feat/scaffold/asr-desktop-route"
IMPORT_LINE = "import ASRPanel from './components/ASRPanel';\n"
ROUTE_ENTRY = "  { path: '/asr', element: <ASRPanel /> },\n"

modified = []

# create git branch
try:
    subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, cwd=REPO_ROOT)
    # create branch (force new) only if not exists
    existing = subprocess.run(
        ["git", "branch", "--list", BRANCH],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if not existing.stdout.strip():
        subprocess.run(["git", "checkout", "-b", BRANCH], check=True, cwd=REPO_ROOT)
    else:
        subprocess.run(["git", "checkout", BRANCH], check=True, cwd=REPO_ROOT)
    print(f"Using git branch {BRANCH}")
except Exception as e:
    print(
        "Git not available or repo not initialized; continuing without git operations",
        e,
    )

for cand in CANDIDATES:
    if not cand.exists():
        continue
    text = cand.read_text(encoding="utf-8")
    if "ASRPanel" in text:
        print(f"ASRPanel already present in {cand}; skipping")
        continue
    # backup
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    bak = cand.with_suffix(cand.suffix + f".bak.{ts}")
    shutil.copy2(cand, bak)
    print(f"Backup created: {bak}")

    # insert import after last import
    lines = text.splitlines(keepends=True)
    last_import_idx = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith("import "):
            last_import_idx = i
    insert_import_at = last_import_idx + 1
    lines.insert(insert_import_at, IMPORT_LINE)

    new_text = "".join(lines)

    # Try to find routes array to insert entry
    m = re.search(r"(export\s+const|const)\s+\w*routes\w*\s*=\s*\[", new_text)
    if m:
        # find the closing bracket of this array (naive): find the first \n] after m.end()
        start = m.end()
        idx = new_text.find("\n]", start)
        if idx != -1:
            # insert before idx
            new_text = new_text[:idx] + "\n" + ROUTE_ENTRY + new_text[idx:]
            print(f"Inserted route into routes array in {cand}")
        else:
            # fallback: append at end
            new_text = new_text + "\n// Added route for ASR\n" + ROUTE_ENTRY
            print(f"Appended route to end of {cand}")
    else:
        # Try react-router JSX pattern: look for <Routes> ... </Routes>
        m2 = re.search(r"<Routes[^>]*>", new_text)
        if m2:
            # find closing </Routes>
            idx2 = new_text.find("</Routes>", m2.end())
            if idx2 != -1:
                # insert a Route before closing
                route_jsx = '    <Route path="/asr" element={<ASRPanel />} />\n'
                new_text = new_text[:idx2] + route_jsx + new_text[idx2:]
                print(f"Inserted JSX Route into <Routes> in {cand}")
            else:
                new_text = new_text + "\n// Added route for ASR\n" + ROUTE_ENTRY
                print(f"Appended route to end of {cand}")
        else:
            # fallback append
            new_text = new_text + "\n// Added route for ASR - please import ASRPanel manually\n" + ROUTE_ENTRY
            print(f"Appended fallback route to {cand}")

    cand.write_text(new_text, encoding="utf-8")
    modified.append(str(cand))

# git add + commit
try:
    if modified:
        subprocess.run(["git", "add"] + modified, check=True, cwd=REPO_ROOT)
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "feat(scaffold): add ASRPanel import and route for desktop UI",
            ],
            check=True,
            cwd=REPO_ROOT,
        )
        print("Changes committed on branch", BRANCH)
    else:
        print("No files modified")
except Exception as e:
    print("Git add/commit failed or not available:", e)

print("Modified files:")
for m in modified:
    print(m)
