"""Export Ws Schema module."""

from __future__ import annotations

import json

from app.websockets.schemas import export_json_schemas


def main() -> None:
    schemas = export_json_schemas()
    print(json.dumps(schemas, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
import print
