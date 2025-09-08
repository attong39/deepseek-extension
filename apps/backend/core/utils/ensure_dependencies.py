"""Auto-import missing dependencies với allowlist security.

Cung cấp khả năng tự động cài đặt dependencies an toàn tại runtime.
"""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from importlib import metadata
from typing import Any
import ImportError
import RuntimeError
import bool
import dict
import e
import len
import list
import min_ver
import min_version
import module_name
import package_name
import required_packages
import str

# Security allowlist - chỉ các package được phép cài tự động
ALLOWLIST = {
    # Security & Crypto
    "pynacl": None,
    "cryptography": None,
    # Monitoring & Security Tools
    "pip-audit": None,
    "bandit": None,
    "psutil": None,
    # Development & Testing
    "pytest": None,
    "pytest-cov": None,
    "pytest-asyncio": None,
    # Common utilities
    "requests": None,
    "aiohttp": None,
    "redis": None,
    "click": None,
}

# Environment control
ALLOW_INSTALL_ENV = "ZETA_ALLOW_RUNTIME_INSTALL"


def _is_runtime_install_allowed() -> bool:
    """Check if runtime installation is allowed."""
    return os.getenv(ALLOW_INSTALL_ENV, "0") == "1"


def _uv_install(pkg: str) -> None:
    """Install package using uv (preferred) or fallback to pip."""
    if not _is_runtime_install_allowed():
        raise RuntimeError(
            f"Runtime install disabled: {pkg}. "
            f"Set {ALLOW_INSTALL_ENV}=1 to enable (development only)"
        )

    if pkg not in ALLOWLIST:
        raise RuntimeError(f"Package not in allowlist: {pkg}")

    # Check if uv is available
    uv_available = (
        os.system(
            "uv --version >nul 2>&1"
            if os.name == "nt"
            else "uv --version >/dev/null 2>&1"
        )
        == 0
    )

    try:
        if uv_available:
            subprocess.check_call(["uv", "pip", "install", pkg], timeout=300)
        else:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg], timeout=300
            )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install {pkg}: {e}") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"Timeout installing {pkg}: {e}") from e


def ensure_module(module_name: str, package_name: str | None = None) -> Any:
    """
    Thử import module; nếu fail và allowlist cho phép thì cài rồi import lại.

    Args:
        module_name: Tên module để import (ví dụ: "nacl.signing")
        package_name: Tên package để cài (ví dụ: "pynacl"). Nếu None, dùng module_name

    Returns:
        Imported module

    Raises:
        ImportError: Nếu module không thể import sau khi cài
        RuntimeError: Nếu runtime install bị disable hoặc package không trong allowlist
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pkg = package_name or module_name.split(".")[0]
        _uv_install(pkg)

        # Try import again after installation
        try:
            return importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(
                f"Failed to import {module_name} even after installing {pkg}"
            ) from e


def ensure_version(package_name: str, min_version: str | None = None) -> str:
    """
    Ensure package có version tối thiểu.

    Args:
        package_name: Tên package
        min_version: Version tối thiểu (ví dụ: "1.2.3")

    Returns:
        Current version của package

    Raises:
        RuntimeError: Nếu không thể upgrade
    """
    try:
        current_version = metadata.version(package_name)

        if min_version and current_version < min_version:
            upgrade_spec = f"{package_name}>={min_version}"
            _uv_install(upgrade_spec)

            # Get new version
            current_version = metadata.version(package_name)

        return current_version

    except metadata.PackageNotFoundError:
        # Package chưa cài - install với version requirement
        if min_version:
            _uv_install(f"{package_name}>={min_version}")
        else:
            _uv_install(package_name)

        return metadata.version(package_name)


def check_dependencies(required_packages: dict[str, str | None]) -> dict[str, Any]:
    """
    Check status của multiple packages.

    Args:
        required_packages: Dict mapping package_name -> min_version (hoặc None)

    Returns:
        Dict với status của từng package
    """
    status = {}

    for pkg, min_ver in required_packages.items():
        try:
            current_ver = metadata.version(pkg)
            status[pkg] = {
                "installed": True,
                "version": current_ver,
                "meets_requirement": not min_ver or current_ver >= min_ver,
                "required_version": min_ver,
            }
        except metadata.PackageNotFoundError:
            status[pkg] = {
                "installed": False,
                "version": None,
                "meets_requirement": False,
                "required_version": min_ver,
            }

    return status


def get_runtime_install_status() -> dict[str, Any]:
    """Get status của runtime install system."""
    return {
        "enabled": _is_runtime_install_allowed(),
        "allowlist_size": len(ALLOWLIST),
        "allowlist": list(ALLOWLIST.keys()),
        "uv_available": _check_uv_available(),
        "env_var": ALLOW_INSTALL_ENV,
        "current_value": os.getenv(ALLOW_INSTALL_ENV, "0"),
    }


def _check_uv_available() -> bool:
    """Check if uv command is available."""
    return (
        os.system(
            "uv --version >nul 2>&1"
            if os.name == "nt"
            else "uv --version >/dev/null 2>&1"
        )
        == 0
    )


# Convenience functions cho common use cases
def ensure_nacl() -> Any:
    """Ensure PyNaCl is available for cryptographic operations."""
    return ensure_module("nacl.signing", "pynacl")


def ensure_security_tools() -> dict[str, Any]:
    """Ensure security scanning tools are available."""
    tools = {}
    tools["pip_audit"] = ensure_module("pip_audit", "pip-audit")
    tools["bandit"] = ensure_module("bandit.core.manager", "bandit")
    return tools


def ensure_psutil() -> Any:
    """Ensure psutil for system monitoring."""
    return ensure_module("psutil", "psutil")
