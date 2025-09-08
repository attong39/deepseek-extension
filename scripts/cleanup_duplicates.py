#!/usr/bin/env python3
"""
Cleanup duplicate code safely using a JSON report.

Features
--------
* plan mode (default) → duplicate_cleanup_plan.csv + stats.json
* apply mode → delete duplicates, optional link (symlink/hardlink)
* git‑aware deletions (--git)
* Windows‑safe: fallback to hard‑link or copy if symlink not permitted
* Heuristic to choose canonical file
* Backup before deletion (--backup)
* Root‑only safety (--root)
* Pre‑commit friendly (plan + --fail-on-new)

Usage
-----
uv run python scripts/cleanup_duplicates.py \
    --report duplicate_code_report_20250909_035652.json \
    --root . \
    --mode plan                    # only generate plan
uv run python scripts/cleanup_duplicates.py \
    --report duplicate_code_report_20250909_035652.json \
    --root . \
    --mode apply \
    --git --backup --link-strategy symlink
"""
from __future__ import annotations

import argparse, csv, json, os, shutil, subprocess, sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import Exception
import NotImplementedError
import OSError
import PermissionError
import SystemExit
import ValueError
import any
import bool
import candidates
import d
import dict
import dup
import e
import f
import files
import fo
import g
import int
import isinstance
import k
import len
import ln_msg
import msg_del
import ok_del
import ok_hl
import ok_ln
import out
import paths
import print
import r
import repo_root
import rows
import sorted
import src
import str
import strategy
import target
import tok
import use_git
import x

# ------------------------------------------------------------------ #
# 1️⃣ Data models
# ------------------------------------------------------------------ #
@dataclass
class DupFile:
    """Represent a file inside a duplicate group."""
    path: Path
    size: Optional[int] = None


@dataclass
class DupGroup:
    """One group of identical files (same hash)."""
    group_id: int
    hash: Optional[str]
    size: Optional[int]           # total size of the group (bytes)
    files: List[DupFile]


# ------------------------------------------------------------------ #
# 2️⃣ Load JSON report (any of the common shapes)
# ------------------------------------------------------------------ #
POSSIBLE_PATH_KEYS = ("Path", "PathNormalized", "RelativePath", "File", "path", "normalizedPath")

def _extract_path(d: Dict) -> Optional[str]:
    for k in POSSIBLE_PATH_KEYS:
        if k in d and d[k]:
            return d[k]
    return None


def load_report(report_path: Path) -> List[DupGroup]:
    """Parse the duplicate JSON report → list of DupGroup."""
    try:
        raw = json.loads(report_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        raw = json.loads(report_path.read_text(encoding="utf-8"))
    
    groups_raw = raw.get("DuplicateGroups") or raw.get("groups") or []
    out: List[DupGroup] = []

    for g in groups_raw:
        gid = int(g.get("GroupId") or g.get("Id") or len(out) + 1)
        hsh = g.get("Hash") or g.get("hash")
        sz = g.get("FileSizeBytes") or g.get("sizeBytes") or g.get("FileSize")
        files: List[DupFile] = []

        # Handle both direct file list and nested objects
        file_list = g.get("Files") or g.get("files") or []
        for f in file_list:
            if isinstance(f, str):
                # Direct string path
                p = f
                sz_f = None
            else:
                # Object with path info
                p = _extract_path(f) or str(f)
                sz_f = f.get("SizeBytes") or f.get("bytes") if isinstance(f, dict) else None
            
            if p:
                # Handle absolute Windows paths in JSON
                if p.startswith("E:\\zeta-monorepo\\"):
                    p = p[len("E:\\zeta-monorepo\\"):].replace("\\", "/")
                files.append(DupFile(path=Path(p), size=sz_f))

        if len(files) >= 2:
            out.append(DupGroup(group_id=gid, hash=hsh, size=sz, files=files))
    return out


# ------------------------------------------------------------------ #
# 3️⃣ Heuristic – chọn "canonical" (đường dẫn "chuẩn")
# ------------------------------------------------------------------ #
NEG_PATTERNS = ("refactored", "_fixed", "tmp", "sandbox", "node_modules", ".venv", ".cache", "_refactored", "backup", "old")
POS_PRODUCTION = ("production/src",)
POS_BACKEND = ("apps/backend", "backend/")
POS_LIBS = ("packages", "libs/")
POS_TESTS_SHARED = ("tests/_shared",)

def _score_path(p: Path, basename: str) -> Tuple[int, str]:
    """Lower score = better (more canonical)."""
    score = 1000
    sp = str(p).replace("\\", "/")

    # positive boosts (lower score = better)
    if any(tok in sp for tok in POS_TESTS_SHARED):
        score -= 60  # tests/_shared gets highest priority
    if any(tok in sp for tok in POS_PRODUCTION):
        score -= 50
    if any(tok in sp for tok in POS_BACKEND):
        score -= 40
    if any(tok in sp for tok in POS_LIBS):
        score -= 20

    # negative penalties (higher score = worse)
    if any(tok in sp.lower() for tok in NEG_PATTERNS):
        score += 100  # Heavy penalty for refactored/backup files

    # special cases
    if basename == "test_router.py":
        if "api/v1/" in sp:
            score -= 10
        if "/tests/" in sp:
            score -= 5
    if basename == "__init__.py":
        if "api/v1/" in sp:
            score -= 3

    # tie‑breaker: shallow path is preferred
    depth = len(Path(sp).parts)
    score += depth
    return score, sp


def choose_canonical(paths: List[Path]) -> Path:
    """Pick the best canonical file from a list."""
    if not paths:
        raise ValueError("No candidate paths")
    basename = paths[0].name
    ranked = sorted((( _score_path(p, basename), p) for p in paths),
                    key=lambda x: (x[0][0], x[0][1]))
    return ranked[0][1]


# ------------------------------------------------------------------ #
# 4️⃣ Helper actions (backup, link, delete)
# ------------------------------------------------------------------ #
def ensure_within_root(target: Path, root: Path) -> bool:
    """Only act on files that lie inside the repository root."""
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def make_parent_dirs(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def link_file(src: Path, dst: Path, strategy: str) -> Tuple[bool, str]:
    """Create a link from dst → src. Returns (success, method)."""
    try:
        if strategy == "symlink":
            os.symlink(src, dst)
            return True, "symlink"
        if strategy == "hardlink":
            os.link(src, dst)
            return True, "hardlink"
        return False, "none"
    except (OSError, NotImplementedError, PermissionError) as e:
        return False, f"link_failed:{e.__class__.__name__}"


def delete_with_git(p: Path, use_git: bool, repo_root: Path) -> Tuple[bool, str]:
    """Prefer `git rm` when the repo is a git work‑tree."""
    if use_git and (repo_root / ".git").exists():
        try:
            res = subprocess.run(["git", "rm", "-q", "--", str(p)],
                                 cwd=str(repo_root), check=False)
            return (res.returncode == 0), f"git_rm:{res.returncode}"
        except Exception as e:
            return False, f"git_exc:{e.__class__.__name__}"
    try:
        p.unlink(missing_ok=True)
        return True, "os_remove"
    except Exception as e:
        return False, f"os_exc:{e.__class__.__name__}"


# ------------------------------------------------------------------ #
# 5️⃣ CLI – plan / apply
# ------------------------------------------------------------------ #
def main() -> int:
    parser = argparse.ArgumentParser(description="Duplicate‑code cleanup tool")
    parser.add_argument("--report", required=True, help="JSON duplicate report")
    parser.add_argument("--root", required=True, help="Repository root (safety bound)")
    parser.add_argument("--mode", choices=["plan", "apply"], default="plan")
    parser.add_argument("--link-strategy", choices=["none", "symlink", "hardlink"],
                        default="none", help="Create a link from duplicate → canonical")
    parser.add_argument("--git", action="store_true",
                        help="Use `git rm` when .git is present")
    parser.add_argument("--backup", action="store_true",
                        help="Copy duplicate files to a timestamped backup folder before deletion")
    parser.add_argument("--only-ext", default="",
                        help="Comma‑separated list of extensions to process (e.g. py,ts,js)")
    parser.add_argument("--fail-on-new", action="store_true",
                        help="Exit non‑zero in plan mode if any duplicate is found (CI guard)")
    args = parser.parse_args()

    report_path = Path(args.report)
    root = Path(args.root).resolve()
    only_ext = {e.strip().lower() for e in args.only_ext.split(",") if e.strip()}

    if not report_path.exists():
        print(f"Error: Report file {report_path} not found", file=sys.stderr)
        return 1

    groups = load_report(report_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / ".dup_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_csv = out_dir / f"duplicate_cleanup_plan_{timestamp}.csv"
    stats_json = out_dir / f"duplicate_cleanup_stats_{timestamp}.json"
    backup_root = root / f".dup_backup/{timestamp}" if args.backup else None

    total_groups = total_dups = applied = failed = 0
    rows: List[Dict[str, str]] = []

    for g in groups:
        # ------------------- filter & canonical selection -------------------
        candidates: List[Path] = []
        for f in g.files:
            p = (root / f.path) if not f.path.is_absolute() else f.path
            if not ensure_within_root(p, root):
                continue
            if only_ext and p.suffix.lstrip(".").lower() not in only_ext:
                continue
            if p.exists():
                candidates.append(p)

        if len(candidates) < 2:
            continue

        total_groups += 1
        canonical = choose_canonical(candidates)
        duplicates = [p for p in candidates if p != canonical]

        for dup in duplicates:
            total_dups += 1
            rows.append({
                "group_id": str(g.group_id),
                "hash": g.hash or "",
                "size_bytes": str(g.size or ""),
                "canonical": str(canonical.relative_to(root)),
                "duplicate": str(dup.relative_to(root)),
                "action": "delete+link" if args.link_strategy != "none" else "delete",
                "reason": "heuristic"
            })

            if args.mode == "apply":
                # ----- backup -----
                if backup_root:
                    dst = backup_root / dup.relative_to(root)
                    make_parent_dirs(dst)
                    shutil.copy2(dup, dst)

                # ----- delete -----
                ok_del, msg_del = delete_with_git(dup, args.git, root)
                if not ok_del:
                    failed += 1
                    print(f"Failed to delete {dup}: {msg_del}", file=sys.stderr)
                    continue

                # ----- optional link -----
                if args.link_strategy != "none":
                    make_parent_dirs(dup)
                    ok_ln, ln_msg = link_file(canonical, dup, args.link_strategy)
                    if not ok_ln:
                        # fallback hard‑link → copy
                        ok_hl, _ = link_file(canonical, dup, "hardlink")
                        if not ok_hl:
                            try:
                                shutil.copy2(canonical, dup)
                                print(f"Fallback to copy: {dup} → {canonical}")
                            except Exception as e:
                                failed += 1
                                print(f"Failed to link/copy {dup}: {e}", file=sys.stderr)
                                continue
                        else:
                            print(f"Hardlink fallback: {dup} → {canonical}")
                    else:
                        print(f"Linked: {dup} → {canonical} ({ln_msg})")
                applied += 1

    # ------------------- write plan & stats -------------------
    with plan_csv.open("w", newline="", encoding="utf-8") as fo:
        writer = csv.DictWriter(fo,
                                fieldnames=["group_id", "hash", "size_bytes",
                                            "canonical", "duplicate", "action", "reason"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    stats = {
        "mode": args.mode,
        "root": str(root),
        "report": str(report_path),
        "groups_considered": total_groups,
        "duplicates_planned": total_dups,
        "applied": applied,
        "failed": failed,
        "timestamp": timestamp,
        "link_strategy": args.link_strategy,
        "git_used": args.git,
        "backup": bool(backup_root)
    }
    stats_json.write_text(json.dumps(stats, indent=2), encoding="utf-8")

    # ------------------- output & CI exit policy -------------------
    print(f"[dup] Mode: {args.mode}")
    print(f"[dup] Groups processed: {total_groups}")
    print(f"[dup] Duplicates found: {total_dups}")
    
    if args.mode == "plan":
        print(f"[dup] Plan CSV: {plan_csv}")
        print(f"[dup] Stats JSON: {stats_json}")
        if args.fail_on_new and total_dups > 0:
            print(f"[dup] FAIL: Found {total_dups} duplicate files in {total_groups} groups.", file=sys.stderr)
            print(f"[dup] See {plan_csv}", file=sys.stderr)
            return 2
    else:
        print(f"[dup] Applied: {applied}, Failed: {failed}")
        if backup_root:
            print(f"[dup] Backup: {backup_root}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
