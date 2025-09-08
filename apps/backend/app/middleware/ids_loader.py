"""IDS rules loader middleware attach.

Đọc `config/security/ids_rules.yaml` vào app.state.ids_rules để các middleware/security có thể tham chiếu.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI
import Exception
import app
import dict
import fh
import isinstance
import str


def attach(app: FastAPI) -> None:
    try:
        path = Path("config/security/ids_rules.yaml")
        rules: dict[str, Any] = {}
        if path.exists():
            with path.open("r", encoding="utf8") as fh:
                try:
                    loaded = yaml.safe_load(fh) or {}
                    if isinstance(loaded, dict):
                        rules = loaded
                except Exception:
                    rules = {}
        app.state.ids_rules = rules
    except Exception:
        # Không chặn startup nếu lỗi
        app.state.ids_rules = {}
