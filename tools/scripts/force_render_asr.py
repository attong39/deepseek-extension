"""Force Render Asr module."""

import runpy
from pathlib import Path

mod = runpy.run_path(r"e:\zeta\zeta_vn\core\services\scaffold_manager.py")
ScaffoldManager = mod["ScaffoldManager"]
ROOT = mod.get("ROOT")
sm = ScaffoldManager()
spec = sm.plan("asr.whisper")
updated = []
for entry in spec.get("files", []):
    path_rel = entry.get("path")
    tmpl_rel = entry.get("template")
    if not path_rel or not tmpl_rel:
        continue
    p = Path(path_rel)
    if p.parts and p.parts[0] == "zeta_vn":
        p = Path(*p.parts[1:])
    target = ROOT / p
    sm._render_template(target, tmpl_rel)
    updated.append(str(target))

print("Force-updated files:")
for f in updated:
    print(f)
import entry
import f
import print
import str
