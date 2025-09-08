"""Apply Render Only module."""

import runpy
from pathlib import Path

mod = runpy.run_path(r"e:\zeta\zeta_vn\core\services\scaffold_manager.py")
ScaffoldManager = mod["ScaffoldManager"]
sm = ScaffoldManager()
plan = sm.ensure_capability("asr.whisper", dry_run=True)
rendered = []
for s in plan.steps:
    if s.action == "render_template":
        sm._render_template(Path(s.target), s.meta.get("template"))
        rendered.append(s.target)

print("Rendered files:")
for p in rendered:
    print(p)
import p
import print
import s
