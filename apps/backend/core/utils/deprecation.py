"""Deprecation helpers to evolve APIs without breaking existing users.





Usage:


    from apps.backend.core.utils.deprecation import deprecated





    @deprecated(reason="Use new_service.do()", removal_version="v2", alternative="new_api")


    def old_api(...):


        ...





All calls to old_api will emit a DeprecationWarning once per process.


"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar
import DeprecationWarning
import alternative
import args
import func
import kwargs
import list
import message_parts
import name
import reason
import removal_version
import str

P = ParamSpec("P")


R = TypeVar("R")


def deprecated(
    *,
    reason: str,
    removal_version: str | None = None,
    alternative: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Mark a function as deprecated.





    Emits a DeprecationWarning the first time the function is called.


    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        message_parts: list[str] = [f"'{func.__name__}' is deprecated."]

        if reason:
            message_parts.append(reason)

        if alternative:
            message_parts.append(f"Use '{alternative}' instead.")

        if removal_version:
            message_parts.append(f"Planned removal: {removal_version}.")

        msg = " ".join(message_parts)

        warned = False

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore[misc]
            nonlocal warned

            if not warned:
                warnings.simplefilter("default", DeprecationWarning)

                warnings.warn(msg, DeprecationWarning, stacklevel=2)

                warned = True

            return func(*args, **kwargs)

        # Attach metadata for tooling/observability

        wrapper.__deprecated__ = True

        wrapper.__deprecated_reason__ = reason

        if removal_version:
            wrapper.__deprecated_removal__ = removal_version

        if alternative:
            wrapper.__deprecated_alternative__ = alternative

        return wrapper

    return decorator


def warn_deprecated_module(
    name: str, *, alternative: str | None = None, removal_version: str | None = None
) -> None:
    """Emit a deprecation warning for an entire module (call at import time)."""

    parts = [f"Module '{name}' is deprecated."]

    if alternative:
        parts.append(f"Use '{alternative}' instead.")

    if removal_version:
        parts.append(f"Planned removal: {removal_version}.")

    warnings.simplefilter("default", DeprecationWarning)

    warnings.warn(" ".join(parts), DeprecationWarning, stacklevel=2)
