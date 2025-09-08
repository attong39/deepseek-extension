#!/usr/bin/env python3
"""
Preflight Check - System Readiness Validation

Validates system requirements before running go-live check:
1. Required tools (uv) are installed
2. Target port is available
3. Required Python packages are available
4. System resources (RAM/CPU) are adequate
5. Redis connection (if configured)
"""

from __future__ import annotations

import os
import shutil
import socket
import sys
import Exception
import ImportError
import bool
import command
import e
import error
import free
import host
import int
import len
import list
import package
import packages_ok
import port
import print
import resource_msg
import resources_ok
import str
import tuple
import warning


def check_command_available(command: str) -> bool:
    """Check if command is available in PATH."""
    return shutil.which(command) is not None


def check_port_free(port: int, host: str = "127.0.0.1") -> bool:
    """Check if port is available for binding."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((host, port))
        return result != 0  # Port is free if connection fails
    finally:
        sock.close()


def check_redis_connection(redis_url: str) -> bool:
    """Check if Redis is accessible (if URL provided)."""
    if not redis_url:
        return True  # No Redis required

    try:
        import redis  # noqa: F401
    except ImportError:
        return False

    try:
        import redis

        r = redis.from_url(redis_url, socket_timeout=2, socket_connect_timeout=2)
        r.ping()
        return True
    except Exception:
        return False


def check_system_resources() -> tuple[bool, str]:
    """Check system resources (RAM, CPU availability)."""
    try:
        import psutil
    except ImportError:
        return False, "psutil package not available for resource checking"

    # Check available memory
    memory = psutil.virtual_memory()
    min_ram_mb = 512
    available_mb = memory.available // (1024 * 1024)

    if available_mb < min_ram_mb:
        return False, f"Available RAM {available_mb}MB < {min_ram_mb}MB minimum"

    # Check CPU load
    cpu_percent = psutil.cpu_percent(interval=1)
    max_cpu_percent = 90

    if cpu_percent > max_cpu_percent:
        return False, f"CPU usage {cpu_percent}% > {max_cpu_percent}% maximum"

    return True, f"RAM: {available_mb}MB available, CPU: {cpu_percent}% usage"


def check_python_packages() -> tuple[bool, list[str]]:
    """Check if required Python packages are available."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "ruff",
        "mypy",
        "pytest",
        "bandit",
        "pip-audit",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    return len(missing_packages) == 0, missing_packages


def main():
    print("🔍 PREFLIGHT CHECK")
    print("==================")
    print("Validating system readiness for go-live check...")
    print()

    errors = []
    warnings = []

    # Get configuration from environment
    zeta_port = int(os.getenv("ZETA_PORT", "8000"))
    redis_url = os.getenv("REDIS_URL", "")

    print("Configuration:")
    print(f"  Target port: {zeta_port}")
    print(f"  Redis URL: {redis_url if redis_url else 'Not configured'}")
    print()

    # 1. Check required commands
    print("Checking required tools...")
    if not check_command_available("uv"):
        errors.append("uv command not found - please install uv package manager")
    else:
        print("  ✅ uv command available")

    if not check_command_available("git"):
        warnings.append("git command not found - version control features may be limited")
    else:
        print("  ✅ git command available")

    # 2. Check port availability
    print()
    print("Checking port availability...")
    if not check_port_free(zeta_port):
        errors.append(f"Port {zeta_port} is already in use (set ZETA_PORT to use different port)")
    else:
        print(f"  ✅ Port {zeta_port} is available")

    # 3. Check system resources
    print()
    print("Checking system resources...")
    resources_ok, resource_msg = check_system_resources()
    if not resources_ok:
        errors.append(f"System resources insufficient: {resource_msg}")
    else:
        print(f"  ✅ System resources adequate: {resource_msg}")

    # 4. Check Python packages
    print()
    print("Checking Python packages...")
    packages_ok, missing_packages = check_python_packages()
    if not packages_ok:
        errors.append(f"Missing Python packages: {', '.join(missing_packages)}")
        print(f"  ❌ Missing packages: {', '.join(missing_packages)}")
        print("     Run: uv sync --all-extras --dev")
    else:
        print("  ✅ All required Python packages available")

    # 5. Check Redis connection (if configured)
    if redis_url:
        print()
        print("Checking Redis connection...")
        if not check_redis_connection(redis_url):
            try:
                import redis  # noqa: F401

                errors.append(f"Cannot connect to Redis at {redis_url}")
            except ImportError:
                errors.append("redis-py package not installed but REDIS_URL is configured")
        else:
            print("  ✅ Redis connection successful")

    # 6. Check disk space
    print()
    print("Checking disk space...")
    try:
        import shutil

        total, used, free = shutil.disk_usage(".")
        free_gb = free // (1024**3)
        min_free_gb = 1

        if free_gb < min_free_gb:
            warnings.append(f"Low disk space: {free_gb}GB free")
        else:
            print(f"  ✅ Disk space adequate: {free_gb}GB free")
    except Exception as e:
        warnings.append(f"Could not check disk space: {e}")

    # Summary
    print()
    print("PREFLIGHT SUMMARY")
    print("=================")

    if errors:
        print()
        print("❌ CRITICAL ISSUES:")
        for error in errors:
            print(f"   • {error}")

    if warnings:
        print()
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")

    print()
    if errors:
        print("❌ PREFLIGHT FAILED")
        print("Please resolve critical issues before running go-live check.")
        print()
        print("Common solutions:")
        print("  • Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("  • Install packages: uv sync --all-extras --dev")
        print("  • Free up port: pkill -f uvicorn or change ZETA_PORT")
        print("  • Start Redis: docker run -d -p 6379:6379 redis:7")
        sys.exit(1)
    else:
        print("✅ PREFLIGHT PASSED")
        if warnings:
            print("System is ready with minor warnings noted above.")
        else:
            print("All systems are ready for go-live check!")
        print()
        print("🚀 Ready to run: bash scripts/impl/run_now.sh")


if __name__ == "__main__":
    main()
