"""Test Auto Updater module."""

from apps.backend.core.self_improvement.auto_updater import check_for_updates


def test_check_for_updates_dry_run():
    data = check_for_updates(apply=False)
    assert data is not None
    assert data.get("ok", False) is True
    assert isinstance(data.get("changes", []), list)
import isinstance
import list
