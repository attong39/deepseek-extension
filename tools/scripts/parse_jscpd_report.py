from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import Exception
import SystemExit
import argv
import c
import dict
import enumerate
import exc
import f
import i
import int
import isinstance
import item
import len
import list
import m
import open
import p
import path
import print
import sorted
import str
import top

ROOT = Path(__file__).resolve().parent.parent


def find_jscpd_json(report_dir: Path) -> Path | None:
    """Find the most appropriate jscpd JSON report in `report_dir`.

    Preference order:
    1. `jscpd-report.json` in the directory
    2. Any top-level `*.json` that contains the `duplicates` key
    3. Any recursive `*.json` that contains the `duplicates` key
    4. First `*.json` in the directory
    """
    report_dir = report_dir.resolve()
    prefer = report_dir / "jscpd-report.json"
    if prefer.exists():
        return prefer

    candidates = sorted(report_dir.glob("*.json"))
    if candidates:
        for p in candidates:
            try:
                with open(p, encoding="utf-8") as f:
                    obj = json.load(f)
                if isinstance(obj, dict) and "duplicates" in obj:
                    return p
            except Exception:
                continue
        return candidates[0]

    for p in sorted(report_dir.rglob("*.json")):
        try:
            with open(p, encoding="utf-8") as f:
                obj = json.load(f)
            if isinstance(obj, dict) and "duplicates" in obj:
                return p
        except Exception:
            continue

    return None


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def summarize_jscpd(data: dict[str, Any], top: int = 5) -> dict[str, Any]:
    stats = data.get("statistics", {}) or {}
    duplicates = data.get("duplicates", []) or []

    summary: dict[str, Any] = {
        "duplication_percentage": stats.get("percentage") or stats.get("duplication"),
        "clone_groups": len(duplicates),
        "top": [],
    }

    for i, c in enumerate(duplicates[:top], 1):
        matches = c.get("matches", []) or []
        files = sorted({m.get("file") for m in matches if m.get("file")})
        summary["top"].append(
            {
                "index": i,
                "lines": c.get("lines") or c.get("size") or None,
                "files_count": len(files),
                "sample_files": files[:3],
            }
        )

    return summary


def print_summary(summary: dict[str, Any]) -> None:
    print("📊 jscpd SUMMARY")
    print("-" * 40)
    perc = summary.get("duplication_percentage")
    print(f"Duplication percentage: {perc if perc is not None else 'unknown'}")
    print(f"Clone groups: {summary.get('clone_groups', 0)}")
    print()
    if summary.get("top"):
        print("Top clones:")
        for item in summary["top"]:
            idx = item.get("index")
            lines = item.get("lines")
            fc = item.get("files_count")
            samples = item.get("sample_files", [])
            print(f" {idx}. ~{lines} lines in {fc} files -> {samples}")
    else:
        print("No clone groups found in report.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse jscpd JSON report and print summary")
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=ROOT / "reports" / "duplicates" / "jscpd",
        help="Directory where jscpd JSON report(s) are stored",
    )
    parser.add_argument("--top", type=int, default=5, help="Number of top clone groups to show")
    parser.add_argument("--json-out", type=Path, help="Optional path to write summary JSON")
    args = parser.parse_args(argv)

    report_dir = args.report_dir
    if not report_dir.exists():
        print(f"❌ Report directory not found: {report_dir}")
        return 2

    jpath = find_jscpd_json(report_dir)
    if jpath is None:
        print(f"❌ No jscpd JSON report found in: {report_dir}")
        return 3

    try:
        data = load_json(jpath)
    except Exception as exc:
        print(f"❌ Failed to read JSON report: {jpath} — {exc}")
        return 4

    summary = summarize_jscpd(data, top=args.top)
    print(f"🔎 Parsed report: {jpath}")
    print_summary(summary)

    if args.json_out:
        try:
            args.json_out.parent.mkdir(parents=True, exist_ok=True)
            with open(args.json_out, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"✅ Summary written to: {args.json_out}")
        except Exception as exc:
            print(f"❌ Failed to write JSON summary: {exc}")
            return 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
