# scripts/tests/test_cleanup_duplicates.py
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
import args
import cwd
import f
import list
import p
import print
import str
import text
import tmpdir

SCRIPT = Path(__file__).resolve().parents[1] / "cleanup_duplicates.py"

def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          cwd=str(cwd), capture_output=True, text=True)

def write(p: Path, text: str = "same") -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def test_plan_and_apply_basic():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # create two identical test_router.py files in two locations
        f1 = root / "production/src/api/v1/tests/test_router.py"
        f2 = root / "apps/backend/some/other/tests/test_router.py"
        for f in (f1, f2):
            write(f, "def foo(): pass")

        # generate a minimal JSON duplicate report
        report = root / "report.json"
        report.write_text(json.dumps({
            "DuplicateGroups": [{
                "GroupId": 1,
                "Hash": "deadbeef",
                "FileSizeBytes": 13,
                "Files": [{"Path": str(f1)}, {"Path": str(f2)}]
            }]
        }), encoding="utf-8")

        # ---- PLAN (no changes) ----
        r_plan = run(["--report", str(report), "--root", str(root),
                      "--mode", "plan", "--only-ext", "py"], root)
        assert r_plan.returncode == 0
        assert "duplicate_cleanup_plan" in r_plan.stdout

        # ---- APPLY (hardlink fallback) ----
        r_apply = run(["--report", str(report), "--root", str(root),
                       "--mode", "apply",
                       "--link-strategy", "hardlink"], root)
        assert r_apply.returncode == 0

        # canonical stays (production/src wins over apps/backend)
        assert f1.exists()
        # duplicate was removed then replaced by link/copy
        assert f2.exists()

def test_fail_on_new():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)

        # create duplicate files
        f1 = root / "file1.py"
        f2 = root / "file2.py"
        for f in (f1, f2):
            write(f, "duplicate content")

        # generate report
        report = root / "report.json"
        report.write_text(json.dumps({
            "DuplicateGroups": [{
                "GroupId": 1,
                "Hash": "abc123",
                "FileSizeBytes": 10,
                "Files": [{"Path": str(f1)}, {"Path": str(f2)}]
            }]
        }), encoding="utf-8")

        # ---- PLAN with --fail-on-new should exit 2 ----
        r_plan = run(["--report", str(report), "--root", str(root),
                      "--mode", "plan", "--fail-on-new"], root)
        assert r_plan.returncode == 2

if __name__ == "__main__":
    test_plan_and_apply_basic()
    test_fail_on_new()
    print("All tests passed!")
