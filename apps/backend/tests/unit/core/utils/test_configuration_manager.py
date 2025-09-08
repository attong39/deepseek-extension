"""Test Configuration Manager module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from apps.backend.core.utils.configuration_manager import (
    ConfigurationError,
    ConfigurationManager,
)


def test_configuration_manager_save_load(tmp_path: Path) -> None:
    mgr = ConfigurationManager(config_dir=str(tmp_path))
    data: dict[str, Any] = {"debug": True, "log_level": "DEBUG"}
    mgr.save_config("core", data)
    loaded = mgr.load_config("core")
    assert loaded["debug"] is True
    assert loaded["log_level"] == "DEBUG"


def test_configuration_manager_validator(tmp_path: Path) -> None:
    mgr = ConfigurationManager(config_dir=str(tmp_path))

    def validator(conf: dict[str, Any]) -> None:
        if conf.get("port") == 0:
            raise ValueError("invalid port")

    mgr.add_validator("api", validator)
    mgr.save_config("api", {"port": 8000})
    assert mgr.get_config("api", "port") == 8000
    try:
        mgr.save_config("api", {"port": 0})
    except ConfigurationError:
        pass
    else:
        raise AssertionError("Expected ConfigurationError for invalid port")


__all__ = [
    "loaded",
    "mgr",
    "test_configuration_manager_save_load",
    "test_configuration_manager_validator",
    "validator",
]
import AssertionError
import ValueError
import conf
import data
import dict
import str
import tmp_path
