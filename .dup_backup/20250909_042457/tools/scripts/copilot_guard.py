#!/usr/bin/env python3
"""
tools/copilot_guard.py

Kiểm tra tính nhất quán thay đổi giữa các lớp kiến trúc.
Đảm bảo khi chạm domain/interfaces/infrastructure/services/use_cases/api
thì có thay đổi tương ứng ở tests và các lớp liên quan.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
import any
import enumerate
import f
import i
import len
import line
import list
import must_trigger_pat
import pattern
import print
import required_pat
import str
import suggestion
import trigger_pattern
import violation

ROOT = Path(__file__).resolve().parents[1]

# Constants for common patterns
TESTS_PATTERN = r"^tests/"
CORE_IMPL_PATTERN = r"^zeta_vn/(core/(infrastructure|services)|data)/"
API_TESTS_PATTERN = r"^(tests/|desktop_ai_zeta/scripts/(contract_guard|generate_openapi_types)\.mjs)"

# Quy tắc: (pattern_trigger, pattern_required)
# Nếu có file thay đổi khớp pattern_trigger thì PHẢI có ít nhất 1 file khớp pattern_required
RULES = [
    # Nếu chạm domain entities/value_objects -> phải có tests thay đổi
    (
        re.compile(r"^zeta_vn/core/domain/(entities|value_objects|domain_events)"),
        re.compile(TESTS_PATTERN),
    ),
    # Nếu chạm interfaces/ports -> cần chạm ít nhất một implementation (infra/services)
    (
        re.compile(r"^zeta_vn/core/interfaces/"),
        re.compile(CORE_IMPL_PATTERN),
    ),
    # Nếu chạm services/use_cases -> cần chạm tests
    (
        re.compile(r"^zeta_vn/core/(services|use_cases)/"),
        re.compile(TESTS_PATTERN),
    ),
    # Nếu chạm api v1 -> cần chạm tests api hoặc desktop contract guard scripts
    (
        re.compile(r"^zeta_vn/app/api/v1/"),
        re.compile(API_TESTS_PATTERN),
    ),
    # Nếu chạm sqlalchemy models -> cần chạm migrations hoặc alembic scripts
    (
        re.compile(r"^zeta_vn/data/models/"),
        re.compile(r"^zeta_vn/data/(migrations\.py|migrations/|database_|alembic/)"),
    ),
    # Nếu chạm repositories -> cần chạm tests
    (
        re.compile(r"^zeta_vn/data/repositories/"),
        re.compile(TESTS_PATTERN),
    ),
    # Nếu chạm domain events -> cần chạm serializers hoặc event handlers
    (
        re.compile(r"^zeta_vn/core/domain/domain_events"),
        re.compile(r"^zeta_vn/(app/serializers|core/services|core/use_cases)/"),
    ),
]


def get_changed_files() -> list[str]:
    """Lấy danh sách file đã thay đổi trong staging area."""
    cmd = ["git", "diff", "--cached", "--name-only"]
    try:
        out = subprocess.check_output(cmd, text=True, cwd=ROOT)
        return [line.strip() for line in out.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        # Fallback: lấy tất cả file thay đổi so với HEAD
        cmd = ["git", "diff", "--name-only", "HEAD"]
        try:
            out = subprocess.check_output(cmd, text=True, cwd=ROOT)
            return [line.strip() for line in out.splitlines() if line.strip()]
        except subprocess.CalledProcessError:
            print("⚠️  copilot_guard: không thể lấy danh sách file thay đổi")
            return []


def enforce() -> None:
    """Kiểm tra và báo lỗi nếu vi phạm quy tắc nhất quán."""
    changed = get_changed_files()

    if not changed:
        print("✅ copilot_guard: không có file thay đổi")
        return

    print(f"📁 copilot_guard: kiểm tra {len(changed)} file thay đổi")

    violations = []

    for must_trigger_pat, required_pat in RULES:
        # Tìm file nào trigger rule này
        touched = [f for f in changed if must_trigger_pat.search(f)]
        if not touched:
            continue

        # Kiểm tra có file nào satisfy requirement không
        satisfied = any(required_pat.search(f) for f in changed)

        if not satisfied:
            violations.append(
                {
                    "reason": f"Khi chạm '{must_trigger_pat.pattern}', cần có thay đổi ở '{required_pat.pattern}'",
                    "triggered_by": touched,
                    "suggestion": _get_suggestion(must_trigger_pat.pattern),
                }
            )

    if violations:
        print("❌ copilot_guard: phát hiện vi phạm tính nhất quán\n")
        for i, violation in enumerate(violations, 1):
            print(f"{i}. {violation['reason']}")
            print(f"   File trigger: {violation['triggered_by']}")
            print(f"   Gợi ý: {violation['suggestion']}\n")

        print("🔧 Cách khắc phục:")
        print("   - Thêm/cập nhật tests tương ứng")
        print("   - Cập nhật contracts/schemas nếu chạm API")
        print("   - Tạo migration nếu chạm database models")
        print("   - Chạy: uv run python tools/check_related_files.py")

        sys.exit(1)

    print("✅ copilot_guard: tất cả quy tắc nhất quán đều được tuân thủ")


def _get_suggestion(trigger_pattern: str) -> str:
    """Đưa ra gợi ý cụ thể dựa trên pattern."""
    suggestions = {
        "domain/(entities|value_objects|domain_events)": "Thêm/cập nhật tests trong tests/unit/domain/ hoặc tests/integration/",
        "interfaces/": "Cập nhật implementation trong core/services/ hoặc data/repositories/",
        "(services|use_cases)/": "Thêm/cập nhật tests trong tests/unit/ hoặc tests/integration/",
        "api/v1/": "Cập nhật tests API hoặc chạy contract guard cho desktop",
        "data/models/": "Tạo Alembic migration hoặc cập nhật database schemas",
        "repositories/": "Thêm/cập nhật repository tests",
        "domain_events": "Cập nhật event serializers và handlers",
    }

    for pattern, suggestion in suggestions.items():
        if pattern in trigger_pattern:
            return suggestion

    return "Đọc PROJECT_MAP.md để xác định file liên quan cần cập nhật"


if __name__ == "__main__":
    enforce()
