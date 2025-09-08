"""Dedup Index module."""

from __future__ import annotations

import ast
import csv
import difflib
import hashlib
import itertools
import json
import os
import pathlib

ROOTS = ["zeta_vn"]  # chỉnh nếu dùng src/zeta_vn
ART = pathlib.Path("artifacts")
ART.mkdir(exist_ok=True, parents=True)


def read(p: str) -> str:
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def norm_ast(code: str) -> str:
    try:
        tree = ast.parse(code)
    except Exception:
        return ""
    for node in ast.walk(tree):
        if isinstance(node, (ast.Str, ast.Bytes, ast.Constant)):
            if isinstance(node.value, (str, bytes)):  # avoid numbers to keep signatures
                node.value = "" if isinstance(node.value, str) else b""
    return ast.dump(tree, include_attributes=False)


def file_list() -> list[str]:
    out = []
    for r in ROOTS:
        for d, _, files in os.walk(r):
            for fn in files:
                if fn.endswith(".py"):
                    out.append(os.path.join(d, fn))
    return out


def main():
    files = file_list()
    buckets: dict[str, list[str]] = {}
    for f in files:
        na = norm_ast(read(f))
        h = hashlib.sha1(na.encode()).hexdigest() if na else ""
        buckets.setdefault(h, []).append(f)
    pairs = set()
    for bucket, group in buckets.items():
        if bucket == "" or len(group) == 1:
            continue
        for a, b in itertools.combinations(sorted(group), 2):
            pairs.add((a, b))
    for a, b in itertools.combinations(sorted(files), 2):
        if os.path.basename(a) != os.path.basename(b):
            continue
        ca, cb = read(a), read(b)
        if not ca or not cb:
            continue
        ratio = difflib.SequenceMatcher(None, ca, cb).ratio()
        if ratio >= 0.90:
            pairs.add((a, b))
    plan = {}
    with open(ART / "dedup_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file_a", "file_b", "similarity"])
        for a, b in sorted(pairs):
            ratio = difflib.SequenceMatcher(None, read(a), read(b)).ratio()
            w.writerow([a, b, f"{ratio:.3f}"])
            key = os.path.basename(a)
            plan.setdefault(key, []).append({"a": a, "b": b, "score": round(ratio, 3)})
    (ART / "merge_plan.yaml").write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"✅ wrote: {ART / 'dedup_report.csv'} and {ART / 'merge_plan.yaml'}")


if __name__ == "__main__":
    main()
import Exception
import a
import b
import bucket
import buckets
import bytes
import ca
import cb
import code
import d
import dict
import f
import fn
import group
import isinstance
import len
import list
import node
import open
import p
import print
import r
import round
import set
import sorted
import str
