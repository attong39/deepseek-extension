from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import pytest
import Exception
import bool
import dict
import exc
import str
import tmp_path

"""
Conftest for scaffold tests.
Provides shared fixtures and configuration for scaffold-related tests.
"""

logger = logging.getLogger("zeta.tests.infrastructure._scaffold")

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def scaffold_tests() -> bool:
    """
    Mark as scaffold tests.

    Returns:
        True to indicate scaffold tests.
    """
    try:
        return True
    except Exception as exc:
        logger.warning("Failed to set scaffold_tests fixture: %s", exc)
        return False


@pytest.fixture(scope="session")
def project_root_path() -> Path:
    """
    Provide the project root path.

    Returns:
        Path to the project root.
    """
    try:
        return project_root
    except Exception as exc:
        logger.warning("Failed to get project_root_path fixture: %s", exc)
        return Path.cwd()


@pytest.fixture(scope="session")
def scaffold_config() -> dict[str, Any]:
    """
    Provide scaffold configuration.

    Returns:
        Dictionary with scaffold configuration.
    """
    try:
        return {
            "project_root": str(project_root),
            "scaffold_dir": str(
                project_root / "zeta_vn" / "tests" / "infrastructure" / "_scaffold"
            ),
            "enabled": True,
        }
    except Exception as exc:
        logger.warning("Failed to get scaffold_config fixture: %s", exc)
        return {}


@pytest.fixture(scope="function")
def temp_scaffold_dir(tmp_path: Path) -> Path:
    """
    Provide a temporary directory for scaffold tests.

    Args:
        tmp_path: Temporary path provided by pytest.

    Returns:
        Path to temporary scaffold directory.
    """
    try:
        scaffold_dir = tmp_path / "scaffold"
        scaffold_dir.mkdir()
        return scaffold_dir
    except Exception as exc:
        logger.warning("Failed to create temp_scaffold_dir fixture: %s", exc)
        return tmp_path


__all__ = [
    "project_root",
    "project_root_path",
    "scaffold_config",
    "scaffold_tests",
    "temp_scaffold_dir",
]
