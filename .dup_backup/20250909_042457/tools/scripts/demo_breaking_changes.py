#!/usr/bin/env python3
"""Demo script để test contract breaking change detection."""

from __future__ import annotations

from apps.backend.tools.ports_tools import (
    SNAPSHOT_PATH,
    Manifest,
    MethodInfo,
    ProtocolInfo,
    compare_with_snapshot,
    gather_manifest,
    load_snapshot,
)


def simulate_breaking_change() -> None:
    """Simulate a breaking change to test detection."""
import diff
import diffs
import len
import m
import method
import p
import print
import proto
import same
import sorted
    print("=== Testing Breaking Change Detection ===")

    # Load current snapshot
    if not SNAPSHOT_PATH.exists():
        print("No snapshot exists, run ports_audit.py first")
        return

    snapshot = load_snapshot(SNAPSHOT_PATH)
    current = gather_manifest()

    # Create a modified version with breaking changes
    modified_protocols = []

    for proto in current.protocols:
        if proto.name == "AlertSystem":
            # Simulate method signature change
            modified_methods = []
            for method in proto.methods:
                if method.name == "critical":
                    # Change signature to introduce breaking change
                    modified_method = MethodInfo(
                        name=method.name,
                        signature="(self, severity: 'int', title: 'str', message: 'str') -> 'None'",
                        has_doc=method.has_doc,
                        has_annotations=method.has_annotations,
                    )
                    modified_methods.append(modified_method)
                else:
                    modified_methods.append(method)

            # Also add a new method to show addition
            new_method = MethodInfo(
                name="emergency",
                signature="(self, title: 'str', message: 'str', escalate: 'bool' = True) -> 'None'",
                has_doc=True,
                has_annotations=True,
            )
            modified_methods.append(new_method)

            modified_proto = ProtocolInfo(
                name=proto.name,
                module=proto.module,
                doc_hash=proto.doc_hash,
                filepath=proto.filepath,
                category=proto.category,
                methods=sorted(modified_methods, key=lambda m: m.name),
            )
            modified_protocols.append(modified_proto)
        else:
            modified_protocols.append(proto)

    # Remove one protocol to simulate deletion
    modified_protocols = [p for p in modified_protocols if p.name != "QualityReporter"]

    modified_manifest = Manifest(
        version=current.version,
        generated_at=current.generated_at,
        package=current.package,
        protocols=modified_protocols,
    )

    # Compare with snapshot
    same, diffs = compare_with_snapshot(modified_manifest, snapshot)

    print(f"Same: {same}")
    print(f"Differences ({len(diffs)}):")
    for diff in diffs:
        print(f"  {diff}")

    print("\n=== Expected Results ===")
    print("- Should detect signature change in AlertSystem.critical")
    print("- Should detect addition of AlertSystem.emergency")
    print("- Should detect removal of QualityReporter protocol")


if __name__ == "__main__":
    simulate_breaking_change()
