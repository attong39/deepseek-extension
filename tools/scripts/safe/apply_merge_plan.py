from __future__ import annotations

import json
import pathlib
import a
import b
import item
import key
import pairs
import print
import score

ART = pathlib.Path("artifacts")
OUT = pathlib.Path("artifacts/merged")
OUT.mkdir(parents=True, exist_ok=True)
TEMPLATE = """# Auto-generated MERGED VIEW (manual review required)
{A}
{B}
"""


def main():
    plan_path = ART / "merge_plan.yaml"
    if not plan_path.exists():
        print("No merge_plan.yaml. Run dedup_index.py first.")
        return
    plan = json.loads(plan_path.read_text(encoding="utf-8", errors="ignore"))
    for key, pairs in plan.items():
        for item in pairs:
            a, b, score = item["a"], item["b"], item["score"]
            A = pathlib.Path(a).read_text(encoding="utf-8", errors="ignore")
            B = pathlib.Path(b).read_text(encoding="utf-8", errors="ignore")
            name = key.replace(".py", "")
            out = OUT / f"{name}__MERGED__{pathlib.Path(a).stem}__{pathlib.Path(b).stem}.py"
            out.write_text(TEMPLATE.format(a=a, b=b, score=score, A=A, B=B), encoding="utf-8")
    print(f"✅ wrote merged previews into: {OUT}")


if __name__ == "__main__":
    main()
