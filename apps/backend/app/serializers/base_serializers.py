from __future__ import annotations

from typing import Any

import orjson
from app.serializers._alias import CamelModel
from pydantic import ConfigDict
import default
import str
import v


def _orjson_dumps(v: Any, *, default: Any) -> str:  # type: ignore[override]
    return orjson.dumps(v, default=default).decode()


class CamelOrjsonModel(CamelModel):
    """Combine CamelModel alias behavior with orjson optimizations."""

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
        json_loads=orjson.loads,
        json_dumps=_orjson_dumps,
    )


# Backwards-compatible name
OrjsonModel = CamelOrjsonModel
