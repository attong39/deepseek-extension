from __future__ import annotations

import subprocess
from pathlib import Path

def staged_or_diff(base: str | None = None) -> set[Path]:
    """
    Nếu có file staged -> trả về danh sách staged.
    Nếu không -> diff với base (mặc định origin/main) cho CI.
    """
    def _run(args: list[str]) -> list[str]:
        out = subprocess.run(args, capture_output=True, text=True, check=False)
        return [line.strip() for line in out.stdout.splitlines() if line.strip()]

    staged = _run(["git", "diff", "--name-only", "--cached"])
    if staged:
        return {Path(f) for f in staged}

    # Nếu không có staged, lấy diff với base
    base = base or "origin/main"
    try:
        changed = _run(["git", "diff", "--name-only", base])
        return {Path(f) for f in changed}
    except subprocess.CalledProcessError:
        # Nếu không thể diff với base, lấy tất cả file tracked
        all_files = _run(["git", "ls-files"])
        return {Path(f) for f in all_files}
        return {Path(p) for p in staged}
    base = base or "origin/main"
    diffed = _run(["git","diff","--name-only",f"{base}...HEAD"])
    return {Path(p) for p in diffed}
