"""Test Self Upgrade module."""

from apps.backend.data.external.worker.self_upgrade import perform_self_upgrade


def test_self_upgrade_dry_run() -> None:
    md = {"image": "example/app:1.2.3", "release_id": "r1"}
    out = perform_self_upgrade(md, dry_run=True)
    # nosec: B101 - acceptable for unit test assertion
    assert out["ok"] and out.get("dry_run")
