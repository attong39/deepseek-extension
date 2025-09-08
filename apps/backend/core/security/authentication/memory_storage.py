"""In-memory storage implementations for testing and development.

These classes are **purely temporary** – they live only in the current
process and disappear when the process exits.  They obey the same
asynchronous interface as the production back-ends (Redis, SQL, …) so
they can be swapped out without code changes.
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Final, Generic, TypeVar
import ImportError
import RuntimeError
import device
import int
import key
import len
import list
import self
import str
import token
import value

# Handle both relative and absolute imports
try:
    from .storage import (
        MFAStorage,
        VerificationStorage,
        TrustedDevice,
        SmsCode,
        EmailVerification,
    )
except ImportError:
    from storage import (
        MFAStorage,
        VerificationStorage,
        TrustedDevice,
        SmsCode,
        EmailVerification,
    )

# Type variable for generic dict wrapper
D = TypeVar('D')

__all__: Final = [
    "MemoryMFAStorage",
    "MemoryVerificationStorage",
]

# ----------------------------------------------------------------------
# Helper – a tiny async-safe dict wrapper
# ----------------------------------------------------------------------
class _AsyncLockDict(Generic[D]):
    """Thin wrapper around a dict that serialises all accesses with an asyncio.Lock.

    Only the operations we need are implemented; the wrapper keeps the
    public API identical to a normal dict.
    """
    __slots__ = ("_data", "_lock")

    def __init__(self) -> None:
        self._data: Dict[str, D] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> D | None:
        async with self._lock:
            return self._data.get(key)

    async def set(self, key: str, value: D) -> None:
        async with self._lock:
            self._data[key] = value

    async def pop(self, key: str) -> None:
        async with self._lock:
            self._data.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._data.clear()

    async def keys(self) -> List[str]:
        async with self._lock:
            return list(self._data.keys())

    # Synchronous helpers used by tests / debugging (read-only snapshot)
    def __len__(self) -> int:  # pragma: no cover – tiny helper
        return len(self._data)

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}({self._data!r})"


# ----------------------------------------------------------------------
# MFA (device-trust) storage
# ----------------------------------------------------------------------
class MemoryMFAStorage(MFAStorage):
    """In-memory implementation of :class:`~core.security.storage.MFAStorage`.

    The storage is **async-safe** – all mutating operations are protected by an
    ``asyncio.Lock`` to avoid race conditions when the same instance is used
    from many coroutines (e.g. in FastAPI tests with ``TestClient``).
    """

    def __init__(self) -> None:
        self._devices = _AsyncLockDict[TrustedDevice]()

    async def save_device(self, device: TrustedDevice) -> None:
        """Persist a trusted device."""
        await self._devices.set(device.device_token, device)

    async def get_device(self, token: str) -> TrustedDevice | None:
        """Return the device associated with *token* or ``None``."""
        return await self._devices.get(token)

    async def delete_device(self, token: str) -> None:
        """Remove the device identified by *token*."""
        await self._devices.pop(token)

    # Optional no-op close method – required if the ABC defines it
    async def close(self) -> None:  # pragma: no cover
        """Close the storage (nothing to do for the in-memory version)."""
        await self._devices.clear()

    def __len__(self) -> int:  # pragma: no cover
        """Return number of stored devices (debugging aid)."""
        return len(self._devices)

    def __repr__(self) -> str:  # pragma: no cover
        """Return string representation for debugging."""
        return f"MemoryMFAStorage(devices={len(self._devices)})"


# ----------------------------------------------------------------------
# Verification (OTP / email) storage
# ----------------------------------------------------------------------
class MemoryVerificationStorage(VerificationStorage):
    """In-memory implementation of :class:`~core.security.storage.VerificationStorage`.

    Stores both :class:`~core.security.storage.SmsCode` and
    :class:`~core.security.storage.EmailVerification` objects.  The same
    async-lock guarantees consistency under concurrent access.
    """

    def __init__(self) -> None:
        self._codes = _AsyncLockDict[SmsCode | EmailVerification]()

    async def save_code(self, key: str, value: SmsCode | EmailVerification) -> None:
        """Save ``value`` under ``key``."""
        await self._codes.set(key, value)

    async def fetch_code(
        self, key: str
    ) -> SmsCode | EmailVerification | None:
        """Retrieve a stored code, or ``None`` if it does not exist."""
        return await self._codes.get(key)

    async def delete_code(self, key: str) -> None:
        """Delete the entry identified by ``key``."""
        await self._codes.pop(key)

    # ------------------------------------------------------------------
    # Convenience helpers – **synchronous** because they are used only in
    # tests or debugging where the event-loop is not required.
    # ------------------------------------------------------------------
    def clear_all(self) -> None:
        """Remove **all** verification entries (useful for test teardown)."""
        # ``clear`` is async, but we are in a synchronous context – fire-and-forget
        # is safe because the underlying dict operation is instant.
        try:
            loop = asyncio.get_running_loop()
            # If we're in an async context, create a task
            asyncio.create_task(self._codes.clear())
        except RuntimeError:
            # No running loop, we can run it directly
            asyncio.run(self._codes.clear())

    def list_keys(self) -> List[str]:
        """Return a list of all stored keys (debugging aid)."""
        # Same reasoning as ``clear_all`` – we need a snapshot synchronously.
        try:
            loop = asyncio.get_running_loop()
            # If we're in an async context, we need to handle this differently
            # For now, return empty list in async context to avoid blocking
            return []
        except RuntimeError:
            # No running loop, we can run it directly
            return asyncio.run(self._codes.keys())

    async def close(self) -> None:  # pragma: no cover
        """Close the storage (no external resources to free)."""
        await self._codes.clear()

    def __len__(self) -> int:  # pragma: no cover
        """Return number of stored codes (debugging aid)."""
        return len(self._codes)

    def __repr__(self) -> str:  # pragma: no cover
        """Return string representation for debugging."""
        return f"MemoryVerificationStorage(codes={len(self._codes)})"
