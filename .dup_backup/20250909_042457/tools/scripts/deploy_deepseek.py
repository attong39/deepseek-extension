#!/usr/bin/env python3
"""
DeepSeek Triển Khai Tự Động - Orchestrator Chính

Chạy toàn bộ roadmap triển khai DeepSeek system theo best practices,
tuân thủ domain-driven architecture và quality gates.

Attributes:
    ROOT: Root path của project.
    DEEPSEEK_DIR: Thư mục deepseek.
    AUTO_DIR: Thư mục auto scripts.
    EXTENSION_DIR: Thư mục extension.
"""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
from pathlib import Path

# Constants - không side-effect, immutable
ROOT: Path = Path(__file__).parent.parent  # Adjust for scripts/
DEEPSEEK_DIR: Path = ROOT / "deepseek"
AUTO_DIR: Path = DEEPSEEK_DIR / "auto"
EXTENSION_DIR: Path = ROOT / "deepseek-extension"

# Logging setup - centralized
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def run_command(cmd: list[str], cwd: Path = ROOT, check: bool = False) -> int | None:
    """Chạy lệnh với logging và optional check.

    Args:
        cmd: Danh sách lệnh để chạy.
        cwd: Thư mục làm việc hiện tại.
        check: Nếu True, raise exception nếu exit code != 0.

    Returns:
        Exit code của lệnh, hoặc None nếu không check.

    Raises:
        subprocess.CalledProcessError: Nếu check=True và lệnh fail.
    """
    logger.info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        logger.info(result.stdout.strip())
    if result.stderr:
        logger.error(result.stderr.strip())
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
    return result.returncode


def setup_environment() -> None:
    """Chuẩn bị environment với venv và dependencies.

    Raises:
        subprocess.CalledProcessError: Nếu cài dependencies fail.
    """
    logger.info("🚀 Bước 1: Chuẩn bị Environment")
    venv_path = ROOT / ".venv"
    if not venv_path.exists():
        logger.info("Tạo virtual environment...")
        run_command(["python", "-m", "venv", ".venv"], check=True)
    logger.info("Cài dependencies với uv...")
    run_command(["uv", "sync"], check=True)
    logger.info("✅ Environment ready")


def run_core_scripts() -> None:
    """Chạy core scripts với dependency check và fallback.

    Raises:
        FileNotFoundError: Nếu file script không tồn tại.
        subprocess.CalledProcessError: Nếu script fail.
    """
    logger.info("🔧 Bước 2: Chạy Core Scripts")
    # Check và chạy auto-apply với fix
    auto_apply = AUTO_DIR / "auto_apply.py"
    if not auto_apply.exists():
        raise FileNotFoundError(f"auto_apply.py missing at {auto_apply}")
    try:
        run_command(["python", str(auto_apply), "--commit", "--push", "--llm"], check=True)
    except subprocess.CalledProcessError:
        logger.warning("Auto-apply failed, fallback without LLM")
        run_command(["python", str(auto_apply), "--commit", "--push", "--no-rollback"])
    # Check và chạy AI runner
    ai_runner = AUTO_DIR / "ai_runner.py"
    if not ai_runner.exists():
        raise FileNotFoundError(f"ai_runner.py missing at {ai_runner}")
    run_command(["python", str(ai_runner), "--apply"], check=True)
    logger.info("✅ Core scripts executed")


async def build_extension() -> None:
    """Build VS Code extension async để không block.

    Raises:
        subprocess.CalledProcessError: Nếu build fail.
    """
    logger.info("📦 Bước 3: Build VS Code Extension")
    if EXTENSION_DIR.exists():
        original_cwd = os.getcwd()
        os.chdir(EXTENSION_DIR)
        try:
            proc1 = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                "npm", "install", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await proc1.wait()
            if proc1.returncode is not None and proc1.returncode != 0:
                raise subprocess.CalledProcessError(proc1.returncode, ["npm", "install"])
            proc2 = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                "npm",
                "run",
                "compile",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc2.wait()
            if proc2.returncode is not None and proc2.returncode != 0:
                raise subprocess.CalledProcessError(proc2.returncode, ["npm", "run", "compile"])
            proc3 = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                "npx",
                "vsce",
                "package",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc3.wait()
            if proc3.returncode is not None and proc3.returncode != 0:
                raise subprocess.CalledProcessError(proc3.returncode, ["npx", "vsce", "package"])
        finally:
            os.chdir(original_cwd)
    logger.info("✅ Extension built")


def run_quality_gates() -> None:
    """Chạy quality gates với check.

    Raises:
        subprocess.CalledProcessError: Nếu gates fail.
    """
    logger.info("🛡️ Bước 4: Chạy Quality Gates")
    run_command(["uv", "run", "ruff", "check", "."], check=True)
    run_command(["uv", "run", "mypy", "."], check=True)
    run_command(["uv", "run", "pytest", "-q"], check=True)
    logger.info("✅ Quality gates passed")


async def main() -> None:
    """Main function async để orchestrate deployment.

    Raises:
        Exception: Nếu bất kỳ bước nào fail.
    """
    logger.info("🎯 DeepSeek Triển Khai Tự Động")
    logger.info("=" * 50)
    try:
        setup_environment()
        run_core_scripts()
        await build_extension()
        run_quality_gates()
        logger.info("🎉 Triển khai hoàn thành!")
        logger.info("📋 Tiếp theo:")
        logger.info("  - Review changes trong VS Code")
        logger.info("  - Push to main branch")
        logger.info("  - Monitor CI/CD pipeline")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
