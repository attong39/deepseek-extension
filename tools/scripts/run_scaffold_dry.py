"""Run Scaffold Dry module."""

import json
import runpy

mod = runpy.run_path(r"e:\zeta\zeta_vn\core\services\scaffold_manager.py")
ScaffoldManager = mod["ScaffoldManager"]
sm = ScaffoldManager()
plan = sm.ensure_capability("asr.whisper", dry_run=True)
out = {
    "capability": plan.capability,
    "steps": [{"action": s.action, "target": s.target, "meta": s.meta} for s in plan.steps],
}
print(json.dumps(out, default=str, indent=2))
import print
import s
import str
