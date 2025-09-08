from __future__ import annotations

import argparse
import os
import site
import subprocess
import sys
from pathlib import Path

import typer
import Exception
import SystemExit
import bool
import check
import cmd
import cwd
import e
import getattr
import int
import list
import mod
import print
import sp
import str

"""Sửa lỗi virtualenv + đảm bảo deps (typer, rich, requests) cho Deepseek Agent.
- Tìm & backup _virtualenv.pth trong site-packages của venv hiện tại.
- Nếu venv hỏng hoặc không có, tạo mới qua `uv venv` và `uv sync`.
- Cài đặt gói tối thiểu nếu thiếu.
"""
VIRTUALENV_PTH = "_virtualenv.pth"
ART = Path(".artifacts")
ART.mkdir(exist_ok=True, parents=True)


def sh(cmd: list[str], cwd: Path | None = None, check: bool = True) -> int:
    """Chạy shell command với logging."""
    print(" $", " ".join(cmd))
    res = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if check and res.returncode != 0:
        raise SystemExit(res.returncode)
    return res.returncode


def find_virtualenv_pth() -> list[Path]:
    """Tìm tất cả _virtualenv.pth trong site-packages."""
    found = []
    try:
        for sp in site.getsitepackages():
            p = Path(sp) / VIRTUALENV_PTH
            if p.exists():
                found.append(p)
    except Exception:
        cand = [
            Path(sys.prefix) / "Lib" / "site-packages" / VIRTUALENV_PTH,
            Path(sys.prefix)
            / "lib"
            / f"python{sys.version_info.major}.{sys.version_info.minor}"
            / "site-packages"
            / VIRTUALENV_PTH,
        ]
        for p in cand:
            if p.exists():
                found.append(p)
    return found


def backup_pth(p: Path) -> Path:
    """Backup _virtualenv.pth file để tránh conflict."""
    bak = p.with_suffix(".pth.bak")
    if not bak.exists():
        p.rename(bak)
        print(f" → Đã backup {p} → {bak}")
    else:
        print(f" → Đã có backup: {bak}")
        try:
            p.unlink()  # nếu còn file gốc
            print(f" → Đã xoá {p} (đã có .bak)")
        except Exception:
            pass
    return bak


def ensure_uv_venv() -> None:
    """Đảm bảo venv được tạo và hoạt động."""
    venv_ok = bool(os.environ.get("VIRTUAL_ENV")) and Path(os.environ["VIRTUAL_ENV"]).exists()
    if not venv_ok:
        print(" → Không phát hiện venv hợp lệ. Tạo venv bằng uv…")
        sh(["uv", "venv"])
    print(" → Đồng bộ deps nếu có pyproject.toml…")
    if Path("pyproject.toml").exists():
        sh(["uv", "sync"], check=False)


def ensure_packages() -> None:
    """Đảm bảo các package bắt buộc được cài đặt."""
    missing = []
    for mod in ("typer", "rich", "requests"):
        try:
            __import__(mod)
        except Exception:
            missing.append(mod)
    if not missing:
        print(" → Các gói bắt buộc đã có: typer, rich, requests")
        return
    print(" → Thiếu gói:", ", ".join(missing))
    if Path("pyproject.toml").exists():
        sh(["uv", "add", *missing, "--dev"], check=False)
    else:
        sh(["uv", "pip", "install", *missing], check=False)


def main() -> None:
    """Main function."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Thực hiện thay đổi (backup .pth)")
    args = ap.parse_args()
    print("▶ Repair virtualenv & deps")
    pths = find_virtualenv_pth()
    if pths:
        print(f" • Phát hiện _virtualenv.pth: {', '.join(str(p) for p in pths)}")
        if args.apply:
            for p in pths:
                backup_pth(p)
        else:
            print("   (dry-run) Sử dụng --apply để backup & vô hiệu hóa .pth")
    else:
        print(" • Không phát hiện _virtualenv.pth trong venv hiện tại.")
    ensure_uv_venv()
    ensure_packages()
    try:
        print(f" ✔ typer OK – version: {getattr(typer, '__version__', 'unknown')}")
    except Exception as e:
        print(" ❌ typer chưa sẵn sàng:", e)
        raise SystemExit(2)
    print("✅ Hoàn tất sửa deps & venv.")


if __name__ == "__main__":
    main()
