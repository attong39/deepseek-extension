"""Save Plan Asr module."""

import json
import runpy
from pathlib import Path

mod = runpy.run_path(r"e:\zeta\zeta_vn\core\services\scaffold_manager.py")
ScaffoldManager = mod["ScaffoldManager"]
sm = ScaffoldManager()
plan = sm.ensure_capability("asr.whisper", dry_run=True)
out = {
    "capability": plan.capability,
    "steps": [{"action": s.action, "target": s.target, "meta": s.meta} for s in plan.steps],
}

out_dir = Path(r"e:\zeta\build\plans")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / "asr_whisper_plan.json"
out_file.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote plan to {out_file}")
import print
import s
