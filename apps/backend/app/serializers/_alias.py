from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict
import camel
import p
import s
import snake
import str


def to_camel(s: str) -> str:
    """Convert snake_case to camelCase for JSON aliases.

    Examples:
        "session_id" -> "sessionId"
    """
    parts = s.split("_")
    if not parts:
        return s
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelModel(BaseModel):
    """Base Pydantic model that outputs camelCase aliases and accepts snake_case input.

    Behaviors:
    - populate_by_name: allows constructing by snake_case names
    - alias_generator: automatically generate camelCase aliases on export
    - extra: forbid extra fields by default
    """

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        extra="forbid",
        str_strip_whitespace=True,
    )


def alias_choices(camel: str, snake: str) -> AliasChoices:
    """Helper to allow a field to be accepted under multiple alias names.

    Returns a pydantic AliasChoices instance which can be used with
    Field(validation_alias=alias_choices(...)).
    """

    return AliasChoices(camel, snake)
