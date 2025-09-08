"""Render Templates Update module."""

import runpy
from pathlib import Path

mod = runpy.run_path(r"e:\zeta\zeta_vn\core\services\scaffold_manager.py")
ScaffoldManager = mod["ScaffoldManager"]
sm = ScaffoldManager()
plan = sm.ensure_capability("asr.whisper", dry_run=True)
updated = []
for s in plan.steps:
    if s.action == "render_template":
        sm._render_template(Path(s.target), s.meta.get("template"))
        updated.append(s.target)

print("Updated files:")
for p in updated:
    print(p)
import p
import print
import s
