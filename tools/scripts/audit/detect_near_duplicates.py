import difflib
import hashlib
import json
import os
from pathlib import Path
from typing import Any
import Exception
import any
import base
import by_hash
import dict
import dup
import enumerate
import f
import file
import file_info
import group
import i
import j
import len
import line
import list
import open
import p
import path_a
import path_b
import paths
import print
import range
import round
import seg
import str

"""
Tìm file trùng/na ná đơn giản cho SAFE_REPAIR_PLAYBOOK
"""
ROOT = Path(__file__).resolve().parents[2]  # repo root
SCAN_DIRS = ["zeta_vn"]


def get_files() -> list[Path]:
    files = []
    for base in SCAN_DIRS:
        base_path = ROOT / base
        if base_path.exists():
            for p in base_path.rglob("*.py"):
                if ".git" not in p.parts and "__pycache__" not in p.parts:
                    files.append(p)
    return files


def content_hash(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return ""


def simple_content(p: Path) -> str:
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        clean_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        return "\n".join(clean_lines[:100])  # First 100 lines
    except Exception:
        return ""


def find_duplicates() -> dict[str, Any]:
    files = get_files()
    print(f"Scanning {len(files)} files...")
    by_hash: dict[str, list[str]] = {}
    file_info: dict[str, dict[str, str]] = {}
    for p in files:
        h = content_hash(p)
        content = simple_content(p)
        path_str = str(p.relative_to(ROOT))
        if h not in by_hash:
            by_hash[h] = []
        by_hash[h].append(path_str)
        file_info[path_str] = {"hash": h, "content": content}
    exact_dups = [paths for paths in by_hash.values() if len(paths) > 1]
    near_dups = []
    file_paths = list(file_info.keys())
    for i, _ in enumerate(file_paths):
        for j in range(i + 1, len(file_paths)):
            path_a, path_b = file_paths[i], file_paths[j]
            name_a = os.path.basename(path_a)
            name_b = os.path.basename(path_b)
            should_compare = name_a.split(".")[0] == name_b.split(".")[0] or any(
                seg in path_a and seg in path_b for seg in ["api/v1/", "services/", "use_cases/"]
            )
            if should_compare:
                content_a = file_info[path_a]["content"]
                content_b = file_info[path_b]["content"]
                if content_a and content_b:
                    ratio = difflib.SequenceMatcher(a=content_a, b=content_b).ratio()
                    if ratio > 0.85:  # 85% similar
                        near_dups.append({"file_a": path_a, "file_b": path_b, "similarity": round(ratio, 3)})
    return {"exact_duplicates": exact_dups, "near_duplicates": near_dups, "total_files": len(files)}


def main() -> None:
    results = find_duplicates()
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    with open(artifacts_dir / "duplicates_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    lines = ["# Duplicate File Analysis\n"]
    lines.append(f"Total files scanned: {results['total_files']}\n")
    if results["exact_duplicates"]:
        lines.append("## Exact Duplicates\n")
        for group in results["exact_duplicates"]:
            lines.append(f"**Group:** {group[0]}")
            for file in group:
                lines.append(f"- {file}")
            lines.append("")
    if results["near_duplicates"]:
        lines.append("## Near Duplicates (>85% similar)\n")
        for dup in results["near_duplicates"]:
            lines.append(f"- {dup['file_a']} ⇔ {dup['file_b']} ({dup['similarity'] * 100:.1f}% similar)")
    with open(artifacts_dir / "duplicate_groups.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("✅ Analysis complete!")
    print(f"Found {len(results['exact_duplicates'])} exact duplicate groups")
    print(f"Found {len(results['near_duplicates'])} near duplicate pairs")
    print("Reports saved to artifacts/")


if __name__ == "__main__":
    main()
