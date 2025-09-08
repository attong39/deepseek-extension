"""Meta endpoints for contract/version discovery.

Provides endpoints used by CI/desktop to detect changes in OpenAPI/WS schema and trigger codegen/sync.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from app.common.schemas import APIMeta
from fastapi import APIRouter, HTTPException
import dict
import f
import meta
import path
import str
import ver

router = APIRouter()


def _file_checksum(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


@router.get("/meta/contracts/{ver}", response_model=APIMeta)
async def get_contract_meta(ver: str) -> dict[str, str]:
    """Return contract metadata for a requested version.

    Clients can call `/meta/contracts/v1` to get current OpenAPI/WS schema checksum.
    """

    base = Path(__file__).resolve().parents[3]  # project root from app/api/v1/meta.py

    openapi_path = base / "openapi.json"
    ws_schema_path = base / "zeta_vn" / "app" / "api" / "ws_schema.json"

    openapi_checksum = _file_checksum(openapi_path)
    ws_checksum = _file_checksum(ws_schema_path)

    if not openapi_checksum and not ws_checksum:
        # If no generated files found, return 404 to indicate clients should generate
        raise HTTPException(
            status_code=404, detail="No contract artifacts available yet"
        )

    meta: dict[str, str] = {
        "version": ver,
        "checksum": json.dumps({"openapi": openapi_checksum, "ws": ws_checksum}),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    return meta
