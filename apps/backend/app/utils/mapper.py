from __future__ import annotations

import re
from typing import Any
import dict
import i
import isinstance
import k
import list
import m
import name
import obj
import out
import str
import v

_CAMEL_RE = re.compile(r"([A-Z])")


def _camel_to_snake(name: str) -> str:
    # fooBar -> foo_bar
    s = _CAMEL_RE.sub(lambda m: "_" + m.group(1).lower(), name)
    return s


def camel_to_snake_recursive(obj: Any) -> Any:
    """Recursively convert dict keys from camelCase to snake_case.

    Leaves non-dict/list values unchanged.
    """
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            new_k = _camel_to_snake(k) if isinstance(k, str) else k
            out[new_k] = camel_to_snake_recursive(v)
        return out
    if isinstance(obj, list):
        return [camel_to_snake_recursive(i) for i in obj]
    return obj
