from __future__ import annotations

import importlib
import json
import subprocess
from pathlib import Path
import Exception
import cmd
import dict
import e
import getattr
import int
import list
import m
import pkg
import print
import report
import status
import str

"""Kiểm tra nhanh stack sau khi sửa environment."""


def check(cmd: list[str]) -> int:
    """Chạy command và hiển thị output."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(" $", " ".join(cmd))
    print(r.stdout.strip())
    if r.stderr.strip():
        print(r.stderr.strip())
    return r.returncode


def main() -> None:
    """Main verification function."""
    report: dict[str, dict[str, str | int]] = {"python": {}, "node": {}}
    for m in ("typer", "rich", "requests"):
        try:
            mod = importlib.import_module(m)
            report["python"][m] = getattr(mod, "__version__", "unknown")
        except Exception as e:
            report["python"][m] = f"missing: {e}"
    if Path("desktop").exists():
        rc = check(["node", "-v"])
        rc2 = check(["npm", "-v"])
        report["node"]["node_rc"] = rc
        report["node"]["npm_rc"] = rc2
    Path(".artifacts/verify_stack.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✔ verify_stack.json → .artifacts/verify_stack.json")
    print("\n=== VERIFICATION SUMMARY ===")
    for pkg, status in report["python"].items():
        print(f"Python {pkg}: {status}")
    if "node" in report:
        print(f"Node.js ready: {report['node']['node_rc'] == 0}")
        print(f"npm ready: {report['node']['npm_rc'] == 0}")


if __name__ == "__main__":
    main()
