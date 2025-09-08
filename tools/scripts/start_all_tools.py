"""Orchestrator script để khởi động tất cả tools trong ZETA project.

Script này cung cấp interface thống nhất để:
- Khởi động backend server (FastAPI)
- Khởi động frontend/desktop app
- Chạy AI Runner với các actions khác nhau
- Khởi động Deepseek agent
- Monitor health của tất cả services
- Chạy quality checks và tests

Usage:
    python scripts/start_all_tools.py --help
    python scripts/start_all_tools.py --all
    python scripts/start_all_tools.py --backend --frontend
    python scripts/start_all_tools.py --ai-runner --actions "quality,fix imports"
"""

from __future__ import annotations

import argparse
import asyncio
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import aiohttp
import Exception
import KeyboardInterrupt
import actions
import any
import attempt
import background
import base_dir
import bool
import dict
import duration
import e
import float
import int
import max_attempts
import print
import range
import resp
import self
import service
import session
import set
import stderr
import stdout
import str
import timeout
import tool_name
import url


class ToolOrchestrator:
    """Orchestrator để quản lý việc khởi động và monitor các tools."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or Path(__file__).parent.parent)
        self.processes: dict[str, subprocess.Popen[Any]] = {}
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration cho các tools."""
        return {
            "backend": {
                "command": ["uv", "run", "uvicorn", "zeta_vn.app.main_production:app"],
                "args": ["--host", "0.0.0.0", "--port", "8000", "--reload"],
                "cwd": str(self.base_dir),
                "health_url": "http://127.0.0.1:8000/health",
                "name": "Backend Server",
            },
            "frontend": {
                "command": ["npm", "run", "dev"],
                "args": [],
                "cwd": str(self.base_dir / "desktop_ai_zeta"),
                "health_url": "http://127.0.0.1:3000",
                "name": "Frontend App",
            },
            "ai_runner": {
                "command": ["uv", "run", "python", "ai_runner.py"],
                "args": ["--apply"],
                "cwd": str(self.base_dir),
                "name": "AI Runner",
            },
            "deepseek": {
                "command": ["uv", "run", "python", "-m", "deepseek", "agent"],
                "args": ["--apply"],
                "cwd": str(self.base_dir),
                "name": "Deepseek Agent",
            },
        }

    async def check_health(self, url: str, timeout: float = 5.0) -> bool:
        """Kiểm tra health của một service."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                    return resp.status == 200
        except Exception:
            return False

    def start_process(self, tool_name: str, background: bool = True) -> subprocess.Popen[Any] | None:
        """Khởi động một tool process."""
        if tool_name not in self.config:
            print(f"❌ Tool '{tool_name}' không tồn tại")
            return None

        config = self.config[tool_name]
        cmd = config["command"] + config["args"]

        print(f"🚀 Khởi động {config['name']}...")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   CWD: {config['cwd']}")

        try:
            process = subprocess.Popen(
                cmd,
                cwd=config["cwd"],
                stdout=subprocess.PIPE if not background else subprocess.DEVNULL,
                stderr=subprocess.PIPE if not background else subprocess.DEVNULL,
                text=True,
            )

            if background:
                self.processes[tool_name] = process
                print(f"✅ {config['name']} đã khởi động (PID: {process.pid})")
            else:
                # Chờ process hoàn thành
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    print(f"✅ {config['name']} hoàn thành thành công")
                    if stdout:
                        print(f"📄 Output: {stdout[:500]}...")
                else:
                    print(f"❌ {config['name']} thất bại (exit code: {process.returncode})")
                    if stderr:
                        print(f"❌ Error: {stderr[:500]}...")

            return process

        except Exception as e:
            print(f"❌ Lỗi khởi động {config['name']}: {e}")
            return None

    async def wait_for_health(self, tool_name: str, max_attempts: int = 30) -> bool:
        """Chờ một service trở nên healthy."""
        if tool_name not in self.config:
            return False

        config = self.config[tool_name]
        health_url = config.get("health_url")

        if not health_url:
            print(f"⚠️  {config['name']} không có health check URL")
            return True

        print(f"🔍 Đang chờ {config['name']} trở nên healthy...")

        for attempt in range(max_attempts):
            if await self.check_health(health_url):
                print(f"✅ {config['name']} đã healthy!")
                return True

            if attempt < max_attempts - 1:
                print(f"⏳ Chờ lần {attempt + 1}/{max_attempts}...")
                await asyncio.sleep(2)

        print(f"❌ {config['name']} không trở nên healthy sau {max_attempts} lần thử")
        return False

    def stop_all(self) -> None:
        """Dừng tất cả processes đang chạy."""
        print("\n🛑 Đang dừng tất cả services...")

        for tool_name, process in self.processes.items():
            try:
                if process.poll() is None:  # Process vẫn đang chạy
                    print(f"🛑 Dừng {tool_name} (PID: {process.pid})")
                    process.terminate()

                    # Chờ process terminate gracefully
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"⚠️  Force kill {tool_name}")
                        process.kill()
                        process.wait()

            except Exception as e:
                print(f"❌ Lỗi dừng {tool_name}: {e}")

        self.processes.clear()
        print("✅ Đã dừng tất cả services")

    async def run_quality_checks(self) -> None:
        """Chạy quality checks."""
        print("🔍 Chạy quality checks...")

        # Chạy ruff
        self.start_process("quality_ruff", background=False)

        # Chạy mypy
        self.start_process("quality_mypy", background=False)

        # Chạy pytest
        self.start_process("quality_pytest", background=False)

    async def run_ai_actions(self, actions: str) -> None:
        """Chạy AI Runner với các actions cụ thể."""
        print(f"🤖 Chạy AI Runner với actions: {actions}")

        config = self.config["ai_runner"]
        cmd = config["command"] + ["--once", actions] + config["args"]

        try:
            process = subprocess.Popen(
                cmd, cwd=config["cwd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print("✅ AI Runner hoàn thành thành công")
                if stdout:
                    print(f"📄 Output: {stdout[-1000:]}...")  # Show last 1000 chars
            else:
                print(f"❌ AI Runner thất bại (exit code: {process.returncode})")
                if stderr:
                    print(f"❌ Error: {stderr[-1000:]}...")

        except Exception as e:
            print(f"❌ Lỗi chạy AI Runner: {e}")

    async def monitor_services(self, duration: int = 60) -> None:
        """Monitor health của tất cả services."""
        print(f"📊 Monitor services trong {duration} giây...")

        start_time = time.time()
        healthy_services = set()

        while time.time() - start_time < duration:
            for tool_name, config in self.config.items():
                if tool_name in self.processes and "health_url" in config:
                    health_url = config["health_url"]
                    is_healthy = await self.check_health(health_url, timeout=2.0)

                    if is_healthy and tool_name not in healthy_services:
                        healthy_services.add(tool_name)
                        print(f"💚 {config['name']} healthy")
                    elif not is_healthy and tool_name in healthy_services:
                        healthy_services.remove(tool_name)
                        print(f"💔 {config['name']} unhealthy")

            await asyncio.sleep(5)

        print(f"📊 Monitor hoàn thành. Services healthy: {', '.join(healthy_services)}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ZETA Tools Orchestrator - Khởi động và quản lý tất cả tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/start_all_tools.py --all
  python scripts/start_all_tools.py --backend --frontend
  python scripts/start_all_tools.py --ai-runner --actions "quality,fix imports"
  python scripts/start_all_tools.py --deepseek
  python scripts/start_all_tools.py --monitor 120
        """,
    )

    parser.add_argument("--all", action="store_true", help="Khởi động tất cả tools")
    parser.add_argument("--backend", action="store_true", help="Khởi động backend server")
    parser.add_argument("--frontend", action="store_true", help="Khởi động frontend app")
    parser.add_argument("--ai-runner", action="store_true", help="Chạy AI Runner")
    parser.add_argument("--deepseek", action="store_true", help="Chạy Deepseek agent")
    parser.add_argument("--quality", action="store_true", help="Chạy quality checks")
    parser.add_argument("--monitor", type=int, metavar="SECONDS", help="Monitor services trong N giây")
    parser.add_argument("--actions", type=str, default="quality", help="Actions cho AI Runner (default: quality)")
    parser.add_argument("--stop", action="store_true", help="Dừng tất cả services đang chạy")

    args = parser.parse_args()

    # Validate arguments
    if not any(
        [
            args.all,
            args.backend,
            args.frontend,
            args.ai_runner,
            args.deepseek,
            args.quality,
            args.monitor,
            args.stop,
        ]
    ):
        parser.print_help()
        return

    async def run() -> None:
        orchestrator = ToolOrchestrator()

        try:
            # Handle stop command
            if args.stop:
                orchestrator.stop_all()
                return

            # Start services
            services_to_start = []

            if args.all or args.backend:
                services_to_start.append("backend")

            if args.all or args.frontend:
                services_to_start.append("frontend")

            # Start background services
            for service in services_to_start:
                orchestrator.start_process(service, background=True)

            # Wait for services to be healthy
            for service in services_to_start:
                await orchestrator.wait_for_health(service)

            # Run one-time commands
            if args.all or args.ai_runner:
                await orchestrator.run_ai_actions(args.actions)

            if args.all or args.deepseek:
                orchestrator.start_process("deepseek", background=False)

            if args.all or args.quality:
                await orchestrator.run_quality_checks()

            # Monitor if requested
            if args.monitor:
                await orchestrator.monitor_services(args.monitor)

            # Keep running if we have background services
            if services_to_start and not args.monitor:
                print("\n🎯 Services đang chạy. Nhấn Ctrl+C để dừng...")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    pass

        finally:
            orchestrator.stop_all()

    # Run async main
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n👋 Đã dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
