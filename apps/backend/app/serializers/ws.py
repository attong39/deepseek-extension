"""WS serializers: xuất JSON Schema và sinh TypeScript types cho WS events.

Tuân thủ Clean Architecture: serializers ở layer `app` và chỉ lo chuyển đổi/khai báo.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from app.websockets.schemas import (
import dict
import exported_names
import isinstance
import k
import lines
import list
import model
import name
import output_dir
import output_file
import prop
import props
import repr
import required
import schema
import str
import tuple
import v
import written
    ActionEvent,
    AssistantReplyEvent,
    ChatCompletedEvent,
    ChatErrorEvent,
    ChatTokenEvent,
    ConversationHistoryEvent,
    NewMessageEvent,
    PingEvent,
    PongEvent,
    StatusUpdatedEvent,
    TrainingCompletedEvent,
    TrainingErrorEvent,
    TrainingProgressEvent,
    TypingIndicatorEvent,
)


def _ws_models() -> list[tuple[str, Any]]:
    return [
        ("AssistantReplyEvent", AssistantReplyEvent),
        ("ActionEvent", ActionEvent),
        ("PingEvent", PingEvent),
        ("PongEvent", PongEvent),
        ("ChatTokenEvent", ChatTokenEvent),
        ("ChatCompletedEvent", ChatCompletedEvent),
        ("ChatErrorEvent", ChatErrorEvent),
        ("NewMessageEvent", NewMessageEvent),
        ("TypingIndicatorEvent", TypingIndicatorEvent),
        ("ConversationHistoryEvent", ConversationHistoryEvent),
        ("StatusUpdatedEvent", StatusUpdatedEvent),
        ("TrainingProgressEvent", TrainingProgressEvent),
        ("TrainingCompletedEvent", TrainingCompletedEvent),
        ("TrainingErrorEvent", TrainingErrorEvent),
    ]


def get_ws_json_schemas() -> dict[str, dict[str, Any]]:
    """Trả về JSON Schema của các WS models.

    Returns:
        dict tên_model -> json schema (dict)
    """

    schemas: dict[str, dict[str, Any]] = {}
    for name, model in _ws_models():
        schemas[name] = model.model_json_schema()
    return schemas


def dump_ws_json_schemas(output_dir: Path | str) -> list[Path]:
    """Ghi JSON Schema ra thư mục.

    Args:
        output_dir: thư mục đích.
    Returns:
        Danh sách file đã ghi.
    """

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, schema in get_ws_json_schemas().items():
        p = out_dir / f"{name}.schema.json"
        p.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(p)
    return written


def _ts_type_for_schema(prop: dict[str, Any]) -> str:
    # Ưu tiên literal const
    if "const" in prop:
        val = prop["const"]
        if isinstance(val, str):
            return f"'{val}'"
        return repr(val)
    t = prop.get("type")
    if t == "string":
        return "string"
    if t == "integer" or t == "number":
        return "number"
    if t == "boolean":
        return "boolean"
    if t == "array":
        items = prop.get("items", {"type": "any"})
        return f"Array<{_ts_type_for_schema(items)}>"
    if t == "object":
        # Đơn giản hoá: map object tự do thành Record<string, any>
        return "Record<string, any>"
    # Fallback
    return "any"


def generate_ts_types() -> str:
    """Sinh TypeScript types từ JSON Schema của các WS models.

    Lưu ý: mapping đơn giản (string/number/boolean/array/object), đủ cho các models hiện tại.
    """

    schemas = get_ws_json_schemas()
    lines: list[str] = [
        "// Auto-generated from server Pydantic models. Do not edit.",
        "// Source: zeta_vn/app/serializers/ws.py::generate_ts_types",
        "",
    ]
    exported_names: list[str] = []
    for name, schema in schemas.items():
        props: dict[str, Any] = schema.get("properties", {})
        required: Iterable[str] = schema.get("required", [])
        lines.append(f"export type {name} = {{")
        for k, v in props.items():
            ts_t = _ts_type_for_schema(v)
            opt = "" if k in required else "?"
            lines.append(f"  {k}{opt}: {ts_t};")
        lines.append("};")
        lines.append("")
        exported_names.append(name)
    # Union tiện dụng
    union = " | ".join(exported_names)
    lines.append(f"export type WsAnyEvent = {union};")
    lines.append("")
    return "\n".join(lines)


def dump_ws_types_ts(output_file: Path | str) -> Path:
    """Ghi file TypeScript types tổng hợp.

    Args:
        output_file: đường dẫn file .ts
    Returns:
        Path file đã ghi
    """

    out = Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(generate_ts_types(), encoding="utf-8")
    return out
