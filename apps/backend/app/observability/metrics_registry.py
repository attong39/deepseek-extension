from __future__ import annotations
import Exception
import getattr

"""Prometheus registry wrapper cho testing mode.

- Nếu biến môi trường ZETA_TEST_PROM=1 và prometheus_client có sẵn,
  cung cấp CollectorRegistry riêng để tránh đụng default REGISTRY.
- Mặc định (prod/dev bình thường) trả về default REGISTRY để không thay đổi hành vi.
"""

import importlib  # noqa: E402
import os  # noqa: E402
from typing import Any  # noqa: E402


def get_registry() -> Any:
    flag = os.getenv("ZETA_TEST_PROM") == "1"
    try:
        importlib.import_module("prometheus_client")
        core = importlib.import_module("prometheus_client.core")
    except Exception:
        return None

    if flag:
        try:
            return core.CollectorRegistry()
        except Exception:
            return getattr(core, "REGISTRY", None)
    return getattr(core, "REGISTRY", None)


__all__ = ["get_registry"]
