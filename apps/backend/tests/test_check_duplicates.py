"""Test Check Duplicates module."""

import scripts.check_duplicates as cd


def test_run_jscpd_missing_npx(tmp_path, monkeypatch):
    # Simulate run_jscpd returning rc=127 (npx missing)
    def fake_run_jscpd(targets, out_dir, *, min_tokens=50, min_lines=12):
        return 127, "", "Node.js / npx not found in PATH"

    monkeypatch.setattr(cd, "run_jscpd", fake_run_jscpd)
    out_dir = tmp_path / "jscpd"
    report_dir = tmp_path
    res = cd._run_jscpd_with_fallback([str(tmp_path)], out_dir, report_dir)
    assert "npx not found" in res.lower() or "npx" in res


def test_run_jscpd_no_json(tmp_path, monkeypatch):
    # Simulate jscpd ran but produced no json (stdout present)
    def fake_run_jscpd(targets, out_dir, *, min_tokens=50, min_lines=12):
        return 0, "Detection time: 0.1ms", ""

    monkeypatch.setattr(cd, "run_jscpd", fake_run_jscpd)
    out_dir = tmp_path / "jscpd"
    report_dir = tmp_path
    res = cd._run_jscpd_with_fallback([str(tmp_path)], out_dir, report_dir)
    assert "No jscpd JSON report" in res


def test_run_jscpd_with_json(tmp_path, monkeypatch):
    # Simulate jscpd producing a json file
    def fake_run_jscpd(targets, out_dir, *, min_tokens=50, min_lines=12):
        # create a fake json report
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "jscpd-report.json").write_text('{"statistics":{}}')
        return 0, "ok", ""

    monkeypatch.setattr(cd, "run_jscpd", fake_run_jscpd)
    out_dir = tmp_path / "jscpd"
    report_dir = tmp_path
    res = cd._run_jscpd_with_fallback([str(tmp_path)], out_dir, report_dir)
    assert "No jscpd JSON report" not in res
    assert "No jscpd JSON report" not in res
import monkeypatch
import str
import tmp_path
