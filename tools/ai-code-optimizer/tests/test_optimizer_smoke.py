from __future__ import annotations

from pathlib import Path

from tools.ai_code_optimizer import AICodeOptimizer
import i
import len
import p
import range
import s
import str
import tmp_path


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def test_optimizer_smoke_runs(tmp_path: Path) -> None:
    # Create a tiny project with a duplicate and unused import
    root = tmp_path
    write(root / "pkg" / "__init__.py", "")
    write(
        root / "pkg" / "a.py",
        """
import os
import sys

def foo():
    print(os.path.basename(__file__))
""".strip(),
    )
    duplicate_chunk = "\n".join(
        [
            "x = 1",
            *[f"x = x + {i}" for i in range(1, 20)],
        ]
    )
    # Create two files with identical 20-line chunks to trigger detection
    write(root / "pkg" / "b.py", duplicate_chunk)
    write(root / "pkg" / "c.py", duplicate_chunk)

    cfg_path = Path(__file__).resolve().parents[1] / "config.yml"
    opt = AICodeOptimizer(cfg_path)
    results = opt.optimize_project(root)

    assert "import_optimizations" in results
    assert "duplicate_removals" in results
    assert "structure_enforcements" in results
    # Expect at least one duplicate group detected
    assert len(results["duplicate_removals"]) >= 1
