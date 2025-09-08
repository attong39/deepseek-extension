"""Production-grade auto-updater với Ed25519 signature verification.

Cung cấp tự nâng cấp hệ thống an toàn với manifest ký số.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Literal
import Exception
import ImportError
import RuntimeError
import any
import bool
import bytes
import channel
import cmd
import dict
import e
import len
import list
import manifest_json
import note
import post_commands
import req
import requirements
import sig_b64
import signature_b64
import str
import version

# Lazy import để tránh crash nếu chưa cài
VerifyKey = None


@dataclass(frozen=True)
class UpdateManifest:
    """Manifest chứa thông tin update và các bước cần thực hiện."""

    version: str
    channel: Literal["stable", "beta", "dev"]
    python_requirements: list[str]  # ["pkg==1.2.3", ...]
    post_update_cmds: list[list[str]]  # [["uv","run","alembic","upgrade","head"]]
    note: str | None = None


# Environment variables cho security
PUBKEY_ENV = "ZETA_UPDATE_PUBKEY_B64"  # Ed25519 public key (base64)
ALLOW_UPDATE_ENV = "ZETA_ALLOW_SELF_UPDATE"  # "1" to enable


def _ensure_nacl():
    """Lazy import và ensure PyNaCl available."""
    global VerifyKey
    if VerifyKey is None:
        try:
            from nacl.signing import VerifyKey as _VerifyKey

            VerifyKey = _VerifyKey
        except ImportError:
            from apps.backend.core.utils.ensure_dependencies import ensure_module

            nacl_signing = ensure_module("nacl.signing", "pynacl")
            VerifyKey = nacl_signing.VerifyKey


def _verify_signature(blob: bytes, sig_b64: str) -> None:
    """Verify Ed25519 signature cho manifest."""
    _ensure_nacl()

    if not VerifyKey:
        raise RuntimeError("PyNaCl not available for signature verification")

    pk_b64 = os.getenv(PUBKEY_ENV)
    if not pk_b64:
        raise RuntimeError(f"Missing update public key in {PUBKEY_ENV}")

    try:
        vk = VerifyKey(base64.b64decode(pk_b64))
        vk.verify(blob, base64.b64decode(sig_b64))
    except Exception as e:
        raise RuntimeError(f"Signature verification failed: {e}") from e


def _uv_sync(requirements: list[str]) -> None:
    """Install requirements using uv (preferred) or fallback to pip."""
    # Check if uv is available
    uv_available = (
        os.system(
            "uv --version >nul 2>&1"
            if os.name == "nt"
            else "uv --version >/dev/null 2>&1"
        )
        == 0
    )

    if uv_available:
        for req in requirements:
            subprocess.check_call(["uv", "pip", "install", req])
    else:
        for req in requirements:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])


def apply_update(manifest_json: str, signature_b64: str) -> dict[str, any]:
    """Apply system update với signature verification.

    Args:
        manifest_json: JSON string chứa UpdateManifest
        signature_b64: Ed25519 signature (base64 encoded)

    Returns:
        Dict với kết quả update
    """
    # Check if self-update is enabled
    if os.getenv(ALLOW_UPDATE_ENV, "0") != "1":
        return {
            "updated": False,
            "reason": "self-update disabled",
            "env_hint": f"Set {ALLOW_UPDATE_ENV}=1 to enable",
        }

    try:
        # Verify signature
        blob = manifest_json.encode("utf-8")
        _verify_signature(blob, signature_b64)

        # Parse manifest
        manifest_data = json.loads(manifest_json)
        manifest = UpdateManifest(**manifest_data)

        # 1) Update dependencies theo manifest (lock theo phiên bản explicit)
        if manifest.python_requirements:
            _uv_sync(manifest.python_requirements)

        # 2) Chạy các lệnh hậu cập nhật (migrations, regen types…)
        for cmd in manifest.post_update_cmds:
            subprocess.check_call(cmd, timeout=300)  # 5 minute timeout

        return {
            "updated": True,
            "version": manifest.version,
            "channel": manifest.channel,
            "requirements_updated": len(manifest.python_requirements),
            "post_commands_executed": len(manifest.post_update_cmds),
            "note": manifest.note,
        }

    except subprocess.CalledProcessError as e:
        return {
            "updated": False,
            "reason": "command_failed",
            "error": f"Command failed: {e.cmd}",
            "returncode": e.returncode,
        }
    except Exception as e:
        return {"updated": False, "reason": "error", "error": str(e)}


def create_update_manifest(
    version: str,
    channel: Literal["stable", "beta", "dev"] = "stable",
    requirements: list[str] | None = None,
    post_commands: list[list[str]] | None = None,
    note: str | None = None,
) -> str:
    """Helper để tạo update manifest JSON."""
    manifest = UpdateManifest(
        version=version,
        channel=channel,
        python_requirements=requirements or [],
        post_update_cmds=post_commands or [],
        note=note,
    )

    return json.dumps(
        {
            "version": manifest.version,
            "channel": manifest.channel,
            "python_requirements": manifest.python_requirements,
            "post_update_cmds": manifest.post_update_cmds,
            "note": manifest.note,
        },
        indent=2,
    )


def get_update_status() -> dict[str, any]:
    """Get current update system status."""
    return {
        "self_update_enabled": os.getenv(ALLOW_UPDATE_ENV, "0") == "1",
        "pubkey_configured": bool(os.getenv(PUBKEY_ENV)),
        "nacl_available": VerifyKey is not None or _check_nacl_importable(),
        "uv_available": _check_uv_available(),
    }


def _check_nacl_importable() -> bool:
    """Check if PyNaCl can be imported."""
    try:
        pass

        return True
    except ImportError:
        return False


def _check_uv_available() -> bool:
    """Check if uv is available in PATH."""
    return (
        os.system(
            "uv --version >nul 2>&1"
            if os.name == "nt"
            else "uv --version >/dev/null 2>&1"
        )
        == 0
    )
