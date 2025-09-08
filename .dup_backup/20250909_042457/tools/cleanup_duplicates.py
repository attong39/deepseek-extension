import Exception
import NotImplementedError
import a
import actions
import alias_shim
import all
import any
import b
import bool
import bytes
import e
import enumerate
import f
import g
import i
import int
import isinstance
import k
import l
import len
import list
import p
import path
import print
import report_path
import self
import shim_paths
import shim_pytest
import sorted
import sp
import src
import str
import tag
import target
import target_ts
# tools/cleanup_duplicates.py
"""
Cleanup Duplicate Code – Safe by default.

Usage:
  uv run python tools/cleanup_duplicates.py \
        --report duplicate_code_report_YYYYMMDD_HHMMSS.json

  # Dry‑run only (produces plan + bash stub)
  uv run python tools/cleanup_duplicates.py --report ...

  # Apply the plan (creates backups in .dup_cleanup_backup/)
  uv run python tools/cleanup_duplicates.py --report ... --apply

  # Optional flags
  --alias-shim      # write shim imports for tests / media preview
  --minify-init    # (dangerous) minify __init__.py that only contains comments/pass
"""

from __future__ import annotations
import argparse, hashlib, json, os, re, shutil
from pathlib import Path
from typing import Iterable, List, Dict, Any, Tuple

ROOT = Path(__file__).resolve().parents[1]           # repo root
BACKUP = ROOT / ".dup_cleanup_backup"
PLAN_MD = ROOT / "cleanup_plan.md"
PLAN_SH = ROOT / "cleanup_generated.sh"

# ------------------------------------------------------------------ #
# Helper utilities
# ------------------------------------------------------------------ #
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]

def read_bytes(p: Path) -> bytes:
    return p.read_bytes()

def ensure_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(p)

def is_test_file(p: Path) -> bool:
    s = rel(p).lower()
    return "/tests/" in s and (p.name.startswith("test_") or p.name.endswith("_test.py"))

def is_media_preview(p: Path) -> bool:
    s = rel(p).lower()
    return any(k in s for k in ("preview", "media")) and p.suffix in {".ts", ".tsx", ".js", ".jsx"}

def is_init_py(p: Path) -> bool:
    return p.name == "__init__.py"

def looks_refactored_copy(p: Path) -> bool:
    return any(tag in p.stem.lower() for tag in ("refactor", "refactored", "copy", "backup", "old"))

def guess_canonical(paths: List[Path]) -> Path:
    """Chọn file "đúng" (đầu vào chuẩn, không chứa tag 'refactor', ngắn hơn)."""
    def score(p: Path) -> Tuple[int, int, int]:
        s = rel(p).lower()
        in_core = 1 if ("/zeta_vn/app/" in s or "/desktop/src/" in s or "/tests/_shared/" in s) else 0
        not_bad = 0 if looks_refactored_copy(p) else 1
        return (in_core, not_bad, -len(s))
    return sorted(paths, key=score, reverse=True)[0]

def make_relative_import(src: Path, target: Path) -> str:
    """Relative import path (TS/JS) without extension."""
    relpath = os.path.relpath(target.with_suffix(""), src.parent)
    relpath = relpath.replace("\\", "/")
    if not relpath.startswith("."):
        relpath = "./" + relpath
    return relpath

# ------------------------------------------------------------------ #
# Action abstractions (plan → markdown + apply)
# ------------------------------------------------------------------ #
class Action:
    def describe(self) -> str: raise NotImplementedError
    def apply(self) -> None: raise NotImplementedError

class MoveKeepShim(Action):
    """Move canonical file to its new location, then generate shim files."""
    def __init__(self, src: Path, dst: Path, shim_paths: List[Path], shim_pytest: bool = True) -> None:
        self.src, self.dst, self.shim_paths, self.shim_pytest = src, dst, shim_paths, shim_pytest

    def describe(self) -> str:
        lines = [f"- MOVE {rel(self.src)} → {rel(self.dst)}"]
        for s in self.shim_paths:
            lines.append(f"  + SHIM {rel(s)} (import *)")
        return "\n".join(lines)

    def apply(self) -> None:
        ensure_dir(self.dst)
        BACKUP.mkdir(exist_ok=True)
        # backup original src
        backup_src = BACKUP / rel(self.src)
        ensure_dir(backup_src)
        shutil.copy2(self.src, backup_src)
        # move
        shutil.move(str(self.src), str(self.dst))
        # create shim files
        for sp in self.shim_paths:
            ensure_dir(sp)
            backup_shim = BACKUP / rel(sp)
            ensure_dir(backup_shim)
            if sp.exists():
                shutil.copy2(sp, backup_shim)
            
            if sp.suffix == ".py":  # test shim
                sp.write_text(
                    f'"""Shim – re‑export shared test module."""\n'
                    f'from tests._shared.{self.dst.stem} import *  # noqa: F403,F401\n',
                    encoding="utf-8",
                )
            else:  # TS/JS shim
                target_import = make_relative_import(sp, MEDIA_SHARED_TS)
                sp.write_text(f"export * from '{target_import}';\n", encoding="utf-8")

class DeleteFile(Action):
    def __init__(self, path: Path) -> None:
        self.path = path

    def describe(self) -> str:
        return f"- DELETE {rel(self.path)}"

    def apply(self) -> None:
        BACKUP.mkdir(exist_ok=True)
        backup_path = BACKUP / rel(self.path)
        ensure_dir(backup_path)
        shutil.copy2(self.path, backup_path)
        self.path.unlink(missing_ok=True)

class ReplaceWithReExport(Action):
    """Replace file with a single re‑export line (TS/JS)."""
    def __init__(self, path: Path, target_ts: Path) -> None:
        self.path, self.target_ts = path, target_ts

    def describe(self) -> str:
        return f"- RE‑EXPORT {rel(self.path)} → {rel(self.target_ts)}"

    def apply(self) -> None:
        ensure_dir(self.path)
        BACKUP.mkdir(exist_ok=True)
        backup_path = BACKUP / rel(self.path)
        ensure_dir(backup_path)
        shutil.copy2(self.path, backup_path)
        target_import = make_relative_import(self.path, self.target_ts)
        self.path.write_text(f"export * from '{target_import}';\n", encoding="utf-8")

# ------------------------------------------------------------------ #
# Planner – build list of Action objects per duplicate group
# ------------------------------------------------------------------ #
TEST_SHARED_DIR = ROOT / "tests" / "_shared"
MEDIA_SHARED_TS = ROOT / "desktop" / "src" / "lib" / "preview" / "media.ts"

def plan_group(paths: List[Path], alias_shim: bool) -> List[Action]:
    """Return actions that resolve one duplicate group."""
    actions: List[Action] = []

    # ------------------------------------------------------------------
    # 1️⃣ Tests
    # ------------------------------------------------------------------
    if all(is_test_file(p) for p in paths):
        TEST_SHARED_DIR.mkdir(parents=True, exist_ok=True)
        canonical = guess_canonical(paths)                     # keep this file
        dst = TEST_SHARED_DIR / canonical.name
        others = [p for p in paths if p != canonical]
        actions.append(
            MoveKeepShim(src=canonical, dst=dst, shim_paths=others, shim_pytest=alias_shim)
        )
        return actions

    # ------------------------------------------------------------------
    # 2️⃣ Media preview (TS/JS)
    # ------------------------------------------------------------------
    if all(is_media_preview(p) for p in paths):
        # ensure the shared file exists (create stub if missing)
        if not MEDIA_SHARED_TS.exists():
            ensure_dir(MEDIA_SHARED_TS)
            MEDIA_SHARED_TS.write_text(
                "// Shared preview utilities – formatBytes, etc.\n"
                "export function formatBytes(n:number){\n"
                "  if(n===0) return '0 B';\n"
                "  const k=1024,dm=2,sizes=['B','KB','MB','GB','TB'];\n"
                "  const i=Math.floor(Math.log(n)/Math.log(k));\n"
                "  return parseFloat((n/Math.pow(k,i)).toFixed(dm))+' '+sizes[i];\n"
                "}\n",
                encoding="utf-8",
            )
        for p in paths:
            if p.resolve() != MEDIA_SHARED_TS.resolve() and alias_shim:
                actions.append(ReplaceWithReExport(path=p, target_ts=MEDIA_SHARED_TS))
        return actions

    # ------------------------------------------------------------------
    # 3️⃣ Refactored copies (suffix contains refactor|copy|old|backup)
    # ------------------------------------------------------------------
    if any(looks_refactored_copy(p) for p in paths):
        keep = guess_canonical(paths)
        for p in paths:
            if p != keep:
                actions.append(DeleteFile(p))
        return actions

    # ------------------------------------------------------------------
    # 4️⃣ __init__.py – chỉ cảnh báo, không tự động thay đổi
    # ------------------------------------------------------------------
    if all(is_init_py(p) for p in paths):
        # do nothing – user can decide manually
        return actions

    # ------------------------------------------------------------------
    # 5️⃣ Generic – delete obvious backup/old files, keep shortest "good" one
    # ------------------------------------------------------------------
    keep = guess_canonical(paths)
    for p in paths:
        if p != keep and any(tag in rel(p).lower() for tag in ("backup", "old", "tmp", "refactor")):
            actions.append(DeleteFile(p))
    return actions

# ------------------------------------------------------------------ #
# Loading the duplicate‑report (any JSON format that lists groups → files)
# ------------------------------------------------------------------ #
def load_groups(report_path: Path) -> list[list[Path]]:
    # Handle BOM encoding issue
    try:
        data = json.loads(report_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        data = json.loads(report_path.read_text(encoding="utf-8"))
    
    # Support multiple JSON formats
    groups: list[list[Path]] = []
    
    # Format 1: { "DuplicateGroups": [...] } (PowerShell script format)
    if "DuplicateGroups" in data:
        raw_groups = data["DuplicateGroups"]
        for g in raw_groups:
            files = g.get("Files", g.get("files", []))
            paths = []
            for file_path in files:
                if isinstance(file_path, str):
                    # Convert absolute paths to relative
                    if file_path.startswith("E:\\zeta-monorepo\\"):
                        rel_path = file_path[len("E:\\zeta-monorepo\\"):].replace("\\", "/")
                    else:
                        rel_path = file_path
                    full_path = (ROOT / rel_path).resolve()
                    if full_path.exists():
                        paths.append(full_path)
            
            if len(paths) >= 2:
                groups.append(paths)
    
    # Format 2: { "groups": [...] } or direct list
    else:
        raw_groups = data.get("groups", data if isinstance(data, list) else [])
        for g in raw_groups:
            files = g.get("files", g.get("items", []))
            paths = []
            for f in files:
                file_path = f.get("name") or f.get("path") or f.get("file") or f
                if file_path:
                    full_path = (ROOT / file_path).resolve()
                    if full_path.exists():
                        paths.append(full_path)
            
            if len(paths) >= 2:
                groups.append(paths)
    
    # Verify groups have identical content
    verified_groups = []
    for paths in groups:
        try:
            digests = {sha256_bytes(read_bytes(p)) for p in paths if p.is_file()}
            if len(digests) == 1:
                verified_groups.append(paths)
        except Exception as e:
            print(f"Warning: Could not verify group {[rel(p) for p in paths[:2]]}: {e}")
            # Still add for manual review
            verified_groups.append(paths)
    
    return verified_groups

# ------------------------------------------------------------------ #
# Write plan files (markdown + stub bash) – always generated even for dry‑run
# ------------------------------------------------------------------ #
def write_plan_md(actions: List[Action]) -> None:
    lines = ["# Duplicate Cleanup Plan", ""]
    if not actions:
        lines.append("No duplicate cleanup actions needed.")
        lines.append("")
    else:
        for a in actions:
            lines.append(a.describe())
            lines.append("")
    PLAN_MD.write_text("\n".join(lines), encoding="utf-8")

def write_plan_sh(actions: List[Action]) -> None:
    # The real apply logic lives in Python; we only provide a helper command.
    content = (
        "#!/usr/bin/env bash\nset -euo pipefail\n\n"
        f"echo \"Run the real apply with: uv run python {rel(Path(__file__))} --report <report>.json --apply\"\n"
    )
    PLAN_SH.write_text(content, encoding="utf-8")
    try:
        os.chmod(PLAN_SH, 0o755)
    except Exception:
        pass  # Windows might not support chmod

# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, help="JSON duplicate‑report file")
    parser.add_argument("--apply", action="store_true", help="Apply plan (default: dry‑run)")
    parser.add_argument("--alias-shim", action="store_true", help="Create shim imports for tests & media")
    parser.add_argument("--minify-init", action="store_true", help="(danger) Minify __init__.py that only contains comments/pass")
    args = parser.parse_args()

    report_file = Path(args.report)
    if not report_file.exists():
        print(f"Error: Report file {args.report} not found")
        return

    groups = load_groups(report_file)
    print(f"Loaded {len(groups)} duplicate groups from {args.report}")
    
    actions: List[Action] = []
    for g in groups:
        group_actions = plan_group(g, alias_shim=args.alias_shim)
        actions.extend(group_actions)

    write_plan_md(actions)
    write_plan_sh(actions)

    if not args.apply:
        print(f"[dry‑run] Plan written to {rel(PLAN_MD)} (and shell stub {rel(PLAN_SH)})")
        print(f"Found {len(actions)} cleanup actions")
        return

    # ---------- APPLY ----------
    print("[apply] Executing actions …")
    for i, a in enumerate(actions, 1):
        print(f"  [{i}/{len(actions)}] {a.describe().split()[1]}")
        try:
            a.apply()
        except Exception as e:
            print(f"    ERROR: {e}")
            continue
    print("[apply] Done – backups stored in .dup_cleanup_backup/")

    # ---------- OPTIONAL MINIFY __init__.py ----------
    if args.minify_init:
        print("[minify-init] Processing __init__.py files...")
        for p in ROOT.rglob("__init__.py"):
            try:
                txt = p.read_text(encoding="utf-8")
                stripped = "\n".join([l for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")])
                if stripped in ("", "pass"):
                    backup = BACKUP / rel(p)
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, backup)
                    p.write_text("# Auto‑minified – only comments/pass remain\n", encoding="utf-8")
                    print(f"   minified {rel(p)}")
                else:
                    print(f"   SKIP {rel(p)} (contains logic)")
            except Exception as e:
                print(f"   ERROR processing {rel(p)}: {e}")

if __name__ == "__main__":
    main()
