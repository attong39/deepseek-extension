#!/usr/bin/env python3
"""
Wrapper script để chạy kiểm tra duplicate code cho toàn bộ project Zeta.

Mục đích:
- Chạy `jscpd` (qua `npx`) cho JS/TS/Python để lấy báo cáo clones
- Chạy `tools/find_duplicate_files.py` (tập hợp jscpd + pylint) nếu có
- Chạy `scripts/quick_duplicate_check.py` để nhận báo cáo Python nội bộ

Sử dụng:
  python scripts/check_duplicates.py [--fast] [--jscpd-only] [--report-dir REPORT_DIR]

Ghi chú:
- Script này chỉ là wrapper nhẹ để kết hợp các công cụ đã có trong repo.
- Không hard-code đường dẫn tới python; dùng `sys.executable` để chạy các script Python.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import Exception
import FileNotFoundError
import SystemExit
import any
import argv
import bool
import c
import combined_logs
import cwd
import err
import err2
import exc
import f
import fail_if_above
import float
import int
import lf
import list
import map
import min_lines
import min_tokens
import mode
import name
import next
import open
import out
import p
import path
import pout
import print
import script_path
import sorted
import str
import summary
import t
import text
import tuple

# ruff: noqa: C901

ROOT = Path(__file__).resolve().parent.parent
JSCPD_LOG_NAME = "jscpd-run.log"
JSCPD_SUMMARY_NAME = "jscpd_summary.json"
PARSE_JSCPD_SCRIPT = ROOT / "scripts" / "parse_jscpd_report.py"
WARN_SUMMARY_READ = "⚠️ Không đọc được summary JSON để kiểm tra threshold"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Chạy một command và trả về (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError as exc:
        return 127, "", str(exc)


def has_exe(name: str) -> bool:
    return shutil.which(name) is not None


def run_jscpd(targets: list[str], out_dir: Path, *, min_tokens: int = 50, min_lines: int = 12) -> tuple[int, str, str]:
    """Run jscpd via npx with configurable thresholds and reporters.

    Returns (rc, stdout, stderr).
    If Node/npx not present returns rc=127.
    """
    if not has_exe("node") and not has_exe("npx"):
        return 127, "", "Node.js / npx not found in PATH"

    out_dir.mkdir(parents=True, exist_ok=True)

    # Force safe reporter to JSON to avoid optional console/reporters that may not be installed
    reporters = "json"

    # Prefer local binary if project has jscpd installed in node_modules/.bin
    local_candidates = [
        ROOT / "node_modules" / ".bin" / "jscpd",
        ROOT / "node_modules" / ".bin" / "jscpd.cmd",
        ROOT / "node_modules" / ".bin" / "jscpd.exe",
    ]
    local_bin = next((str(p) for p in local_candidates if p.exists()), None)
    if local_bin:
        cmd = [
            local_bin,
            "--reporters",
            reporters,
            "--output",
            str(out_dir),
            "--min-tokens",
            str(min_tokens),
            "--min-lines",
            str(min_lines),
            "--blame",
        ] + targets
    else:
        # Resolve npx binary on PATH
        npx_bin = shutil.which("npx") or shutil.which("npx.cmd") or shutil.which("npx.exe")
        launcher = npx_bin if npx_bin else "npx"
        cmd = [
            launcher,
            "-y",
            "jscpd@3.5.10",
            "--reporters",
            reporters,
            "--output",
            str(out_dir),
            "--min-tokens",
            str(min_tokens),
            "--min-lines",
            str(min_lines),
            "--blame",
        ] + targets

    # Print the command (debug-friendly) — useful when subprocess cannot be found
    try:
        print("Running:", " ".join(map(str, cmd)))
    except Exception:
        pass

    rc, out, err = run(cmd, cwd=ROOT)
    return rc, out or "", err or ""


def _write_log(path: Path, text: str, mode: str = "w", report_dir: Path | None = None) -> None:
    """Write text to a log path, best-effort (avoid raising).

    Kept at module-level so complexity of callers stays low.
    """
    try:
        if report_dir is not None:
            report_dir.mkdir(parents=True, exist_ok=True)
        with open(path, mode, encoding="utf-8") as lf:
            lf.write(text or "")
    except Exception:
        pass


def _compose_jscpd_diagnostic(out_dir: Path, log_path: Path) -> str:
    """Compose a diagnostic message and short listing for out_dir."""
    diag = []
    diag.append("\n\n=== DIAGNOSTIC: No jscpd JSON report produced ===")
    diag.append("1) Verify 'npx' is available and points to Node: e.g., run 'npx -v' or 'where npx' on Windows.")
    diag.append("2) Try running the printed command above manually; it was shown as 'Running: ...' in output.")
    diag.append(
        "3) Run jscpd with the JSON reporter explicitly to avoid console reporter issues:\n   npx -y jscpd@3.5.10 --reporters json --output <out_dir> --min-tokens 50 --min-lines 12 --blame <targets>"
    )
    diag.append(
        "4) If jscpd complains about missing reporter packages, either install them (e.g. 'npm i -g @jscpd/json') or use the JSON-only reporter."
    )
    diag.append(
        f"5) Inspect the jscpd output folder: {out_dir}\n   e.g. 'dir {out_dir}' (Windows) or 'ls -la {out_dir}'"
    )

    # Attach a short listing of out_dir to help debugging
    try:
        files = []
        if out_dir.exists():
            for p in sorted(out_dir.iterdir()):
                try:
                    sz = p.stat().st_size
                    files.append(f"- {p.name} ({sz} bytes)")
                except Exception:
                    files.append(f"- {p.name} (size unknown)")
        else:
            files.append("(output folder does not exist)")
        diag.append("\nOutput folder contents:\n" + "\n".join(files))
    except Exception:
        diag.append("(failed to list output folder contents)")

    diag.append(f"6) Check logs at: {log_path}")
    return "\n".join(diag)


def _attempt_jscpd_retry(targets: list[str], out_dir: Path, log_path: Path) -> str:
    """Attempt a lower-threshold jscpd run and persist retry output to log.

    Returns the stdout/stderr combined string from the retry run (may be empty).
    """
    rc, out2, err2 = run_jscpd(targets, out_dir, min_tokens=10, min_lines=3)
    try:
        now = datetime.now().astimezone().isoformat()
        header = (
            f"\n\n=== RETRY RUN AT {now} ===\nRC: {rc}\n--- STDOUT ---\n{out2 or ''}\n--- STDERR ---\n{err2 or ''}\n\n"
        )
        _write_log(log_path, header + "=== RETRY OUTPUT ===\n\n" + (out2 or ""), mode="a")
    except Exception:
        pass
    return out2 or ""


def _report_exists(out_dir: Path) -> bool:
    """Check whether jscpd JSON report exists in out_dir (including recursive search)."""
    prefer = out_dir / "jscpd-report.json"
    if prefer.exists():
        return True
    if any(out_dir.glob("*.json")):
        return True
    if any(out_dir.rglob("*.json")):
        return True
    return False


def _run_jscpd_with_fallback(  # noqa: C901
    targets: list[str],
    out_dir: Path,
    report_dir: Path,
    min_tokens: int = 50,
    min_lines: int = 12,
) -> str:
    """Run jscpd, save logs, retry with lower thresholds if needed, and return combined logs.

    This function delegates to small helpers to keep cognitive complexity low.
    """

    def _write_log(path: Path, text: str, mode: str = "w") -> None:
        try:
            report_dir.mkdir(parents=True, exist_ok=True)
            with open(path, mode, encoding="utf-8") as lf:
                lf.write(text)
        except Exception:
            # best-effort logging only
            pass

    def _compose_jscpd_diagnostic(out_dir: Path, log_path: Path) -> str:
        diag = []
        diag.append("\n\n=== DIAGNOSTIC: No jscpd JSON report produced ===")
        diag.append("1) Verify 'npx' is available and points to Node: e.g., run 'npx -v' or 'where npx' on Windows.")
        diag.append("2) Try running the printed command above manually; it was shown as 'Running: ...' in output.")
        diag.append(
            "3) Run jscpd with the JSON reporter explicitly to avoid console reporter issues:\n   npx -y jscpd@3.5.10 --reporters json --output <out_dir> --min-tokens 50 --min-lines 12 --blame <targets>"
        )
        diag.append(
            "4) If jscpd complains about missing reporter packages, either install them (e.g. 'npm i -g @jscpd/json') or use the JSON-only reporter."
        )
        diag.append(
            f"5) Inspect the jscpd output folder: {out_dir}\n   e.g. 'dir {out_dir}' (Windows) or 'ls -la {out_dir}'"
        )

        # Attach a short listing of out_dir to help debugging
        try:
            files = []
            if out_dir.exists():
                for p in sorted(out_dir.iterdir()):
                    try:
                        sz = p.stat().st_size
                        files.append(f"- {p.name} ({sz} bytes)")
                    except Exception:
                        files.append(f"- {p.name} (size unknown)")
            else:
                files.append("(output folder does not exist)")
            diag.append("\nOutput folder contents:\n" + "\n".join(files))
        except Exception:
            diag.append("(failed to list output folder contents)")

        diag.append(f"6) Check logs at: {log_path}")
        return "\n".join(diag)

    combined_logs: list[str] = []
    log_path = report_dir / JSCPD_LOG_NAME

    # moved retry logic to module-level helper

    # Initial run
    rc, out, err = run_jscpd(targets, out_dir, min_tokens=min_tokens, min_lines=min_lines)
    if out:
        combined_logs.append(out)
    if err:
        combined_logs.append("\n=== STDERR ===\n" + err)

    # If npx/node missing, return early with diagnostic message
    if rc == 127:
        combined_logs.append(
            "\n\n=== DIAGNOSTIC: Node.js/npx not found or not executable in PATH ===\n"
            "Please install Node.js and ensure 'npx' is on PATH, or run jscpd manually.\n"
        )
        _write_log(log_path, "\n\n=== DIAGNOSTIC: npx not found ===\n", mode="a")
        return "\n".join([c for c in combined_logs if c])

    # Save initial run output
    try:
        now = datetime.now().astimezone().isoformat()
        header = (
            f"\n\n=== INITIAL RUN AT {now} ===\nRC: {rc}\n--- STDOUT ---\n{out or ''}\n--- STDERR ---\n{err or ''}\n\n"
        )
        _write_log(log_path, header + (out or ""), mode="w")
    except Exception:
        # best-effort logging only
        _write_log(log_path, out, mode="w")

    # Retry if no report
    if not _report_exists(out_dir):
        out2 = _attempt_jscpd_retry(targets, out_dir, log_path)
        if out2:
            combined_logs.append(out2)

    # If still no report, add diagnostics and persist
    if not _report_exists(out_dir):
        diag = _compose_jscpd_diagnostic(out_dir, log_path)
        combined_logs.append(diag)
        _write_log(log_path, "\n\n=== DIAGNOSTIC: No JSON report ===\n" + diag, mode="a")

    return "\n".join([c for c in combined_logs if c])


def _evaluate_jscpd_summary(json_out: Path) -> float | None:
    """Load summary JSON produced by parse_jscpd_report and return duplication percentage.

    Returns float value or None if cannot read/parse.
    """
    try:
        if not json_out.exists():
            return None
        with open(json_out, encoding="utf-8") as f:
            s = json.load(f)
        dup = s.get("duplication_percentage")
        if dup is None:
            return 0.0
        return float(dup)
    except Exception:
        return None


def run_jscpd_and_parse(
    targets: list[str],
    out_dir: Path,
    report_dir: Path,
    min_tokens: int,
    min_lines: int,
    fail_if_above: float | None,
) -> int:
    """Run jscpd (with fallback), invoke parser to write JSON summary, and enforce threshold.

    Returns exit code (0 ok, 2 threshold exceeded, 127 node missing, other codes preserved).
    """
    # Run jscpd with fallback and print logs
    combined_log = _run_jscpd_with_fallback(targets, out_dir, report_dir, min_tokens, min_lines)
    if combined_log:
        print(combined_log)

    # Parse and write JSON summary
    json_out = report_dir / JSCPD_SUMMARY_NAME
    _, pout = run_python_script(PARSE_JSCPD_SCRIPT, ["--report-dir", str(out_dir), "--json-out", str(json_out)])
    if pout:
        print(pout)

    # Enforce threshold if requested
    if fail_if_above is not None:
        dup_val = _evaluate_jscpd_summary(json_out)
        if dup_val is None:
            print(WARN_SUMMARY_READ)
            dup_val = 0.0
        if dup_val > fail_if_above:
            print(f"❌ Duplication {dup_val} > threshold {fail_if_above}")
            return 2

    return 0


def handle_jscpd_only(args: argparse.Namespace, report_dir: Path) -> int:
    """Handler for --jscpd-only mode."""
    targets = collect_targets()
    print("🔎 Running jscpd for targets:", targets)
    out_dir = report_dir / "jscpd"
    return run_jscpd_and_parse(
        targets,
        out_dir,
        report_dir,
        args.min_tokens,
        args.min_lines,
        args.fail_if_dup_above,
    )


def handle_fast(_args: argparse.Namespace) -> int:
    """Handler for --fast mode."""
    print("⚡ Running fast/quick analyzer (scripts/quick_duplicate_check.py)")
    rc, out = run_python_tool(ROOT / "scripts" / "quick_duplicate_check.py")
    print(out)
    return 0 if rc == 0 else rc


def handle_full(args: argparse.Namespace, report_dir: Path) -> int:
    """Handler for full run: jscpd, aggregator, quick analyzer.

    Returns exit code (0 OK, non-zero on failure/threshold).
    """
    summary: list[tuple[str, int]] = []

    print("🚀 Starting full duplicate-code check: jscpd -> tools/find_duplicate_files -> quick analyzer")

    # 1) jscpd
    targets = collect_targets()
    if targets:
        print("1/3 — jscpd")
        out_dir = report_dir / "jscpd"
        rc = run_jscpd_and_parse(
            targets,
            out_dir,
            report_dir,
            args.min_tokens,
            args.min_lines,
            args.fail_if_dup_above,
        )
        summary.append(("jscpd", rc))
        if rc != 0:
            # threshold or node missing — bail out with rc
            return rc
    else:
        print("No targets found for jscpd, skipping")
        summary.append(("jscpd", 0))

    # 2) tools/find_duplicate_files.py (aggregator already in repo)
    print("2/3 — tools/find_duplicate_files.py")
    rc, out = run_python_tool(ROOT / "tools" / "find_duplicate_files.py")
    print(out)
    summary.append(("find_duplicate_files", rc))

    # 3) quick analyzer (detailed Python-only analyzer)
    print("3/3 — scripts/quick_duplicate_check.py")
    rc, out = run_python_tool(ROOT / "scripts" / "quick_duplicate_check.py")
    print(out)
    summary.append(("quick_analyzer", rc))

    # Summary
    print("\n=== SUMMARY ===")
    exit_code = 0
    for name, rc in summary:
        status = "OK" if rc == 0 else f"FAIL(rc={rc})"
        print(f"- {name}: {status}")
        if rc != 0 and exit_code == 0:
            exit_code = rc

    print(f"Reports (if produced) are under: {report_dir}")
    return exit_code


def run_python_tool(script_path: Path) -> tuple[int, str]:
    if not script_path.exists():
        return 127, f"Script not found: {script_path}"

    cmd = [sys.executable, str(script_path)]
    rc, out, err = run(cmd, cwd=ROOT)
    combined = out + ("\n" + err if err else "")
    return rc, combined


def run_python_script(script_path: Path, argv: list[str]) -> tuple[int, str]:
    """Run a Python script with given argv (uses sys.executable)."""
    cmd = [sys.executable, str(script_path)] + argv
    rc, out, err = run(cmd, cwd=ROOT)
    combined = out + ("\n" + err if err else "")
    return rc, combined


def collect_targets() -> list[str]:
    # Targets for jscpd — follow existing project layout
    targets: list[str] = []
    # Desktop frontend
    if (ROOT / "desktop_ai_zeta").exists():
        targets.append(str(ROOT / "desktop_ai_zeta"))
    # Python server
    if (ROOT / "zeta_vn").exists():
        targets.append(str(ROOT / "zeta_vn"))
    # include top-level src folders as fallback
    for p in (ROOT / "src", ROOT / "core", ROOT / "app"):
        if p.exists():
            targets.append(str(p))
    # Deduplicate
    unique = []
    for t in targets:
        if t not in unique:
            unique.append(t)
    return unique


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run duplicate-code checks for the repo")
    parser.add_argument("--fast", action="store_true", help="Run only fast/quick analyzer")
    parser.add_argument("--jscpd-only", action="store_true", help="Run only jscpd via npx")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports" / "duplicates")
    parser.add_argument("--min-lines", type=int, default=12, help="Initial jscpd --min-lines value")
    parser.add_argument("--min-tokens", type=int, default=50, help="Initial jscpd --min-tokens value")
    parser.add_argument(
        "--fail-if-dup-above",
        type=float,
        default=None,
        help="Exit non-zero if jscpd duplication percentage is above this value (percent)",
    )
    args = parser.parse_args(argv)

    report_dir = args.report_dir.resolve()
    report_dir.mkdir(parents=True, exist_ok=True)

    if args.jscpd_only:
        return handle_jscpd_only(args, report_dir)

    if args.fast:
        return handle_fast(args)

    return handle_full(args, report_dir)


if __name__ == "__main__":
    raise SystemExit(main())
