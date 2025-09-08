#!/usr/bin/env python3
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import RuntimeError
import any
import c
import check
import cwd
import d
import dict
import enumerate
import err
import exts
import f
import float
import g
import globs
import i
import ig
import int
import len
import list
import m
import open
import out
import print
import rc
import str
import sum
import tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
DESKTOP_DIRS = ["desktop_ai_zeta"]
PY_DIRS = ["zeta_vn"]

# Ngưỡng có thể override qua ENV
MAX_JSC_PD = float(os.getenv("DUPC_MAX_JSC_PD", "2.0"))  # % duplication tối đa (jscpd)
MIN_SIM_LINES = int(os.getenv("DUPC_MIN_SIM_LINES", "30"))  # pylint --min-similarity-lines
MAX_PYLINT_DUPGROUPS = int(os.getenv("DUPC_MAX_PYLINT_GROUPS", "0"))  # số nhóm duplicate-code cho phép

# Ignore mặc định
IGNORES = [
    "**/node_modules/**",
    "**/dist/**",
    "**/build/**",
    "**/.next/**",
    "**/.venv/**",
    "**/.tox/**",
    "**/.mypy_cache/**",
    "**/.ruff_cache/**",
    "**/coverage/**",
    "**/migrations/**",
    "**/tests/**",
    "**/mocks/**",
    "**/*.min.*",
    "**/*.snap",
    "**/*.lock",
    "**/*.d.ts",
]


def run(cmd: list[str], cwd: pathlib.Path | None = None, check=True) -> tuple[int, str, str]:
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if check and proc.returncode != 0:
        print(f"[!] Command failed ({proc.returncode}): {' '.join(cmd)}", file=sys.stderr)
        print(err or out, file=sys.stderr)
        sys.exit(proc.returncode)
    return proc.returncode, out, err


def ensure_tool():
    # jscpd (qua npx, không cần cài global). pin version để ổn định CI
    if shutil.which("node") is None:
        print("[!] Node.js không có trong PATH. Cần Node để chạy jscpd.", file=sys.stderr)
        sys.exit(1)
    # pylint (chạy qua uvx để không cần thêm deps vào env)
    if shutil.which("uvx") is None and shutil.which("pylint") is None:
        print(
            "[!] Không tìm thấy uvx hoặc pylint. Cài uv (https://docs.astral.sh/uv/) hoặc cài pylint.",
            file=sys.stderr,
        )
        sys.exit(1)


def jscpd_scan(targets: list[str]) -> dict:
    tmpdir = tempfile.mkdtemp(prefix="jscpd_")
    report_json = os.path.join(tmpdir, "jscpd-report.json")
    # build ignore args
    args_ignore = sum([["--ignore", ig] for ig in IGNORES], [])
    cmd = (
        [
            "npx",
            "-y",
            "jscpd@3.5.10",
            "--reporters",
            "json",
            "--output",
            tmpdir,
            "--min-tokens",
            "50",
            "--min-lines",
            "12",
            "--blame",
        ]
        + args_ignore
        + targets
    )
    rc, out, err = run(cmd, cwd=ROOT, check=False)
    # jscpd trả mã 3 nếu vượt threshold mặc định; ta vẫn đọc report để tự đánh giá
    if not os.path.exists(report_json):
        print(out or err)
        raise RuntimeError("Không tạo được jscpd-report.json")
    with open(report_json, encoding="utf-8") as f:
        data = json.load(f)
    return data


def pylint_dup_python(py_files: list[str]) -> list[dict]:
    if not py_files:
        return []
    cmd = []
    if shutil.which("uvx"):
        cmd = ["uvx", "pylint"]
    else:
        cmd = ["pylint"]
    cmd += [
        "-j",
        "0",
        "--disable=all",
        "--enable=duplicate-code",
        f"--min-similarity-lines={MIN_SIM_LINES}",
        "--output-format=json",
    ] + py_files
    rc, out, err = run(cmd, cwd=ROOT, check=False)
    if rc not in (0, 2, 4, 32):  # pylint trả nhiều mã khác nhau; vẫn parse JSON
        print(err, file=sys.stderr)
    try:
        items = json.loads(out or "[]")
        return [m for m in items if m.get("symbol") == "duplicate-code"]
    except json.JSONDecodeError:
        # Có thể không có cảnh báo nào -> out rỗng
        return []


def collect_files(globs: list[str], exts: tuple[str, ...]) -> list[str]:
    files = []
    for g in globs:
        p = ROOT / g
        if p.is_dir():
            for f in p.rglob("*"):
                if f.suffix.lower() in exts and not any(f.match(ig) for ig in IGNORES):
                    files.append(str(f))
        elif p.exists():
            files.append(str(p))
    return files


def main():
    ensure_tool()

    # 1) JS/TS/Python với jscpd
    targets = [str(ROOT / d) for d in DESKTOP_DIRS + PY_DIRS]
    jdata = jscpd_scan(targets)
    stats = jdata.get("statistics", {}) or {}
    dup_percent = float(stats.get("percentage", stats.get("duplication", 0.0)))
    clones = jdata.get("duplicates", []) or []

    # 2) Python chuyên sâu bằng pylint R0801
    py_files = collect_files(PY_DIRS, exts=(".py",))
    py_dups = pylint_dup_python(py_files)

    # 3) Tổng hợp & in bảng
    print("\n=== DUPLICATION REPORT ===")
    print(f"jscpd: {dup_percent:.2f}% | clone groups: {len(clones)}")
    print(f"pylint duplicate-code (min {MIN_SIM_LINES} lines): {len(py_dups)} groups\n")

    if clones:
        print("Top jscpd clones (<=5):")
        for i, c in enumerate(clones[:5], 1):
            files = {m.get("file") for m in c.get("matches", [])}
            lines = c.get("lines", "?")
            print(f"  {i}. ~{lines} lines in {len(files)} files")
            for f in list(files)[:3]:
                print(f"     - {os.path.relpath(f, ROOT)}")
        print()

    if py_dups:
        print("Pylint duplicate-code examples (<=5):")
        for m in py_dups[:5]:
            print(f"  - {m.get('path')}:{m.get('line')}: {m.get('message')}")
        print()

    # 4) Fail điều kiện
    ok = True
    if dup_percent > MAX_JSC_PD:
        print(f"[FAIL] jscpd duplication {dup_percent:.2f}% > {MAX_JSC_PD:.2f}%")
        ok = False
    if len(py_dups) > MAX_PYLINT_DUPGROUPS:
        print(f"[FAIL] pylint duplicate groups {len(py_dups)} > {MAX_PYLINT_DUPGROUPS}")
        ok = False

    # Gợi ý ignore thêm
    if not ok:
        print("\nGợi ý giảm false positive:")
        print(" - Tăng --min-tokens/--min-lines của jscpd (hoặc thêm pattern vào IGNORES).")
        print(" - Tăng --min-similarity-lines cho pylint qua env DUPC_MIN_SIM_LINES.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
