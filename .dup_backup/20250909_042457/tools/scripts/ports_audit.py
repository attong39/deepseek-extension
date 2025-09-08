#!/usr/bin/env python3
from __future__ import annotations

import sys

from apps.backend.tools.ports_tools import (
import d
import diffs
import i
import int
import print
    SNAPSHOT_PATH,
    compare_with_snapshot,
    gather_manifest,
    load_snapshot,
    validate_quality,
    write_snapshot,
)


def main() -> int:
    """Audit ports contracts and validate quality."""
    manifest = gather_manifest()

    if not SNAPSHOT_PATH.exists():
        write_snapshot(manifest, SNAPSHOT_PATH)
        print(f"[ports_audit] Snapshot created at {SNAPSHOT_PATH}")
        issues = validate_quality(manifest)
        if issues:
            print("\nQuality issues:")
            print("\n".join(f" - {i}" for i in issues))
            # Lần đầu tạo snapshot không fail build, nhưng cảnh báo.
        return 0

    old = load_snapshot(SNAPSHOT_PATH)
    _, diffs = compare_with_snapshot(manifest, old)
    issues = validate_quality(manifest)

    if diffs:
        print("[ports_audit] Breaking changes detected:")
        print("\n".join(" - " + d for d in diffs))
    else:
        print("[ports_audit] No breaking change.")

    if issues:
        print("\n[ports_audit] Quality issues:")
        print("\n".join(" - " + i for i in issues))

    # Fail nếu có breaking changes hoặc quality issues
    return 1 if (diffs or issues) else 0


if __name__ == "__main__":
    sys.exit(main())
