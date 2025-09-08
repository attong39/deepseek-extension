"""WebSocket events schema consistency checker.

Compares server WS schema (Python Pydantic models) with Desktop TS schema
(validators) to ensure event types and required fields are aligned.

- Server: zeta_vn/app/websockets/schemas.py
- Desktop: desktop_ai_zeta/src/services/wsSchema.ts

Outputs mismatches by event type: missing fields, extra fields, type name divergence.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
import annot
import desktop
import dict
import enumerate
import events
import evt
import f
import idx
import it
import k
import len
import list
import m
import name
import py_file
import report
import req
import required_raw
import server
import set
import sorted
import str
import ts_file
import v
import x

logger = logging.getLogger("ws_events_consistency")


@dataclass
class EventSpec:
    name: str
    required: set[str]


PY_CLASS_HEADER = re.compile(r"class\s+\w+\(BaseModel\):", re.MULTILINE)
PY_FIELD_RE = re.compile(r"\n\s+(\w+):\s+[^=\n]+")

TS_VALIDATOR_RE = re.compile(
    r"const\s+(\w+)Schema\s*=\s*\{[\s\S]*?type:\s*\{\s*const:\s*\"([^\"]+)\"\s*\}[\s\S]*?required:\s*\[([^\]]*)\]",
    re.MULTILINE,
)


def parse_server_events(py_file: Path) -> dict[str, EventSpec]:
    txt = py_file.read_text(encoding="utf-8")
    events: dict[str, EventSpec] = {}
    # Find blocks per class by scanning class headers and slicing positions
    headers = list(PY_CLASS_HEADER.finditer(txt))
    for idx, m in enumerate(headers):
        start = m.start()
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(txt)
        block = txt[start:end]
        mtype = re.search(r"type:\s+Literal\[\"([^\"]+)\"\]", block)
        if not mtype:
            continue
        evt_type = mtype.group(1)
        # required fields: those declared without Optional and not defaulted
        req: set[str] = set()
        for f in re.finditer(r"\n\s+(\w+):\s+([^\n=]+)", block):
            name, annot = f.group(1), f.group(2)
            if name == "type":
                continue
            if "Optional" in annot or "| None" in annot:
                continue
            # Has default?
            if re.search(rf"\n\s+{name}:[^\n]+=", block):
                continue
            req.add(name)
        events[evt_type] = EventSpec(name=evt_type, required=req)
    return events


def parse_desktop_events(ts_file: Path) -> dict[str, EventSpec]:
    txt = ts_file.read_text(encoding="utf-8")
    events: dict[str, EventSpec] = {}
    for m in TS_VALIDATOR_RE.finditer(txt):
        _schema_name, evt_type, required_raw = m.groups()
        # required list elements are JSON-like strings '"field"', possibly with whitespace
        items = [s for s in (x.strip() for x in required_raw.split(",")) if s]
        required = {it.strip("\"'") for it in items}
        # type is always implicitly required
        required.add("type")
        events[evt_type] = EventSpec(name=evt_type, required=required)
    return events


def compare(server: dict[str, EventSpec], desktop: dict[str, EventSpec]) -> dict[str, dict]:
    report: dict[str, dict] = {}
    all_evt_types = set(server.keys()) | set(desktop.keys())
    for evt in sorted(all_evt_types):
        s = server.get(evt)
        d = desktop.get(evt)
        if not s or not d:
            report[evt] = {
                "status": "missing",
                "missing_side": "desktop" if s and not d else "server",
                "server_required": sorted(s.required) if s else None,
                "desktop_required": sorted(d.required) if d else None,
            }
            continue
        missing_in_desktop = sorted(s.required - d.required)
        missing_in_server = sorted(d.required - s.required - {"type"})
        report[evt] = {
            "status": "ok" if not missing_in_server and not missing_in_desktop else "diverged",
            "missing_in_desktop": missing_in_desktop,
            "missing_in_server": missing_in_server,
        }
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--server-schema", default="zeta_vn/app/websockets/schemas.py")
    ap.add_argument("--desktop-schema", default="desktop_ai_zeta/src/services/wsSchema.ts")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    server_events = parse_server_events(Path(args.server_schema))
    desktop_events = parse_desktop_events(Path(args.desktop_schema))

    rep = compare(server_events, desktop_events)
    diverged = {k: v for k, v in rep.items() if v.get("status") != "ok"}

    logger.info("Total event types: %d", len(rep))
    logger.info("Diverged/missing: %d", len(diverged))

    if diverged:
        logger.warning(json.dumps(diverged, indent=2))

    if args.out:
        Path(args.out).write_text(json.dumps(rep, indent=2), encoding="utf-8")
        logger.info("Report written: %s", args.out)


if __name__ == "__main__":  # pragma: no cover
    main()
