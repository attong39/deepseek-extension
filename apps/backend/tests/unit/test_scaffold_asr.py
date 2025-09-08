"""Smoke test for ScaffoldManager dry-run plan for asr.whisper."""

from apps.backend.core.services.scaffold_manager import ScaffoldManager


def test_plan_for_asr_whisper():
    sm = ScaffoldManager()
    plan = sm.plan("asr.whisper")
    assert "py_deps" in plan
    assert "files" in plan
    assert isinstance(plan.get("files"), list)
    # sys_deps and entry_points may be present in extended schema
    assert "sys_deps" in plan or "entry_points" in plan


def test_ensure_dry_run():
    sm = ScaffoldManager()
    plan = sm.ensure_capability("asr.whisper", dry_run=True)
    # Plan should list steps without executing
    assert plan.capability == "asr.whisper"
    assert isinstance(plan.steps, list)
    # expect at least one render_template or uv_install step in the plan
    assert any(s.action in ("render_template", "uv_install") for s in plan.steps)
import any
import isinstance
import list
import s
