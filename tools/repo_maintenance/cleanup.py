from __future__ import annotations

import shutil
from pathlib import Path

PATTERNS = [
    "dist", "build", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "**/__pycache__", "**/*.log", "**/*.cache", "coverage.xml", "htmlcov",
    "**/*.tmp", "**/*.temp", "**/.backup", "**/*.backup"
]

def safe_remove(path: Path) -> None:
    """Safely remove a file or directory"""
    try:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink(missing_ok=True)
    except Exception:
        pass

def main() -> int:
    """Main cleanup function"""
    removed = []
    for pattern in PATTERNS:
        for path in Path(".").glob(pattern):
            safe_remove(path)
            removed.append(str(path))

    # Create reports directory
    reports_dir = Path("reports/cleanup")
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Write report
    report_content = "\n".join(sorted(set(removed)))
    (reports_dir / "report.txt").write_text(report_content, encoding="utf-8")

    print(f"[cleanup] removed {len(set(removed))} items")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
