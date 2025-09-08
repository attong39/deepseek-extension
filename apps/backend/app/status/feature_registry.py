"""
Feature Status Registry cho ZETA_VN
Quản lý trạng thái tính năng AI theo thời gian thực với caching và TTL
"""

from __future__ import annotations

import asyncio
import logging
import time
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
import Exception
import TimeoutError
import bool
import callable
import checker_path
import details
import dict
import e
import enumerate
import f
import feature
import feature_config
import float
import func_name
import getattr
import i
import int
import isinstance
import key
import len
import list
import module_path
import next
import open
import result
import round
import status
import str
import sum
import tuple
import use_cache

logger = logging.getLogger(__name__)


class FeatureStatus(BaseModel):
    """Model cho trạng thái của một tính năng"""

    feature_key: str
    feature_name: str
    status: str = Field(..., pattern="^(operational|degraded|down|unknown|starting)$")
    details: str | None = None
    last_checked_at: float
    duration_ms: float | None = None
    dependencies: list[str] = []
    critical: bool = False


class FeatureConfig(BaseModel):
    """Model cấu hình cho một tính năng"""

    key: str
    name: str
    description: str | None = None
    checker: str  # module:function path
    critical: bool = False
    timeout: float = 3.0
    dependencies: list[str] = []


class SystemStatus(BaseModel):
    """Tổng quan trạng thái hệ thống"""

    overall_status: str
    last_updated: float
    features: list[FeatureStatus]
    summary: dict[str, int]
    slo_compliance: dict[str, Any]


# In-memory cache với TTL
_feature_cache: tuple[float, list[FeatureStatus]] | None = None
_config_cache: tuple[float, dict[str, Any]] | None = None
TTL_SECONDS = 15.0
CONFIG_TTL = 300.0  # 5 phút cho config


@lru_cache(maxsize=1)
def get_config_path() -> Path:
    """Lấy đường dẫn file config"""
    return Path(__file__).parent / "features.yaml"


def load_config() -> dict[str, Any]:
    """Load cấu hình từ YAML với caching"""
    global _config_cache

    now = time.time()
    if _config_cache and (now - _config_cache[0] < CONFIG_TTL):
        return _config_cache[1]

    try:
        config_path = get_config_path()
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        _config_cache = (now, config)
        logger.debug(f"Config loaded từ {config_path}")
        return config

    except Exception as e:
        logger.error(f"Lỗi load config: {e}")
        # Fallback config
        fallback = {
            "features": [
                {
                    "key": "inference",
                    "name": "AI Inference",
                    "checker": "zeta_vn.app.status.checks.inference:check",
                    "critical": True,
                }
            ],
            "slo_thresholds": {"availability_target": 0.99},
            "degradation_rules": {
                "operational_threshold": 0.7,
                "degraded_threshold": 0.5,
            },
        }
        _config_cache = (now, fallback)
        return fallback


def _resolve_checker(checker_path: str) -> callable:
    """Resolve checker function từ module path"""
    try:
        module_path, func_name = checker_path.split(":")
        module = import_module(module_path)
        return getattr(module, func_name)
    except Exception as e:
        logger.error(f"Không thể resolve checker {checker_path}: {e}")

        # Fallback checker
        async def fallback_checker() -> tuple[str, str | None]:
            await asyncio.sleep(0.001)  # Make it truly async
            return "unknown", f"Checker not found: {checker_path}"

        return fallback_checker


async def _check_single_feature(feature_config: dict[str, Any]) -> FeatureStatus:
    """Kiểm tra trạng thái một tính năng"""
    start_time = time.perf_counter()

    try:
        checker_fn = _resolve_checker(feature_config["checker"])
        timeout = feature_config.get("timeout", 3.0)

        # Chạy checker với timeout
        status, details = await asyncio.wait_for(checker_fn(), timeout=timeout)

        duration_ms = (time.perf_counter() - start_time) * 1000

        return FeatureStatus(
            feature_key=feature_config["key"],
            feature_name=feature_config["name"],
            status=status,
            details=details,
            last_checked_at=time.time(),
            duration_ms=round(duration_ms, 2),
            dependencies=feature_config.get("dependencies", []),
            critical=feature_config.get("critical", False),
        )

    except TimeoutError:
        duration_ms = (time.perf_counter() - start_time) * 1000
        return FeatureStatus(
            feature_key=feature_config["key"],
            feature_name=feature_config["name"],
            status="down",
            details=f"Timeout after {feature_config.get('timeout', 3.0)}s",
            last_checked_at=time.time(),
            duration_ms=round(duration_ms, 2),
            dependencies=feature_config.get("dependencies", []),
            critical=feature_config.get("critical", False),
        )

    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.warning(f"Lỗi check feature {feature_config['key']}: {e}")

        return FeatureStatus(
            feature_key=feature_config["key"],
            feature_name=feature_config["name"],
            status="unknown",
            details=str(e),
            last_checked_at=time.time(),
            duration_ms=round(duration_ms, 2),
            dependencies=feature_config.get("dependencies", []),
            critical=feature_config.get("critical", False),
        )


async def evaluate_all_features() -> list[FeatureStatus]:
    """Evaluate tất cả features song song"""
    config = load_config()
    features_config = config.get("features", [])

    if not features_config:
        logger.warning("Không có features config")
        return []

    # Chạy tất cả checks song song
    tasks = [_check_single_feature(f_config) for f_config in features_config]

    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)

        feature_statuses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Tạo FeatureStatus cho exception
                f_config = features_config[i]
                feature_statuses.append(
                    FeatureStatus(
                        feature_key=f_config["key"],
                        feature_name=f_config["name"],
                        status="unknown",
                        details=f"Exception: {result}",
                        last_checked_at=time.time(),
                        critical=f_config.get("critical", False),
                    )
                )
            else:
                feature_statuses.append(result)

        return feature_statuses

    except Exception as e:
        logger.error(f"Lỗi evaluate features: {e}")
        return []


def calculate_overall_status(features: list[FeatureStatus]) -> str:
    """Tính toán overall status dựa trên degradation rules"""
    if not features:
        return "unknown"

    config = load_config()
    rules = config.get("degradation_rules", {})
    operational_threshold = rules.get("operational_threshold", 0.7)
    degraded_threshold = rules.get("degraded_threshold", 0.5)

    # Đếm features theo status
    total = len(features)
    operational_count = sum(1 for f in features if f.status == "operational")
    degraded_count = sum(1 for f in features if f.status == "degraded")
    healthy_count = operational_count + degraded_count

    # Tính tỷ lệ healthy
    healthy_ratio = healthy_count / total if total > 0 else 0

    # Quyết định overall status
    if healthy_ratio >= operational_threshold:
        return "operational"
    elif healthy_ratio >= degraded_threshold:
        return "degraded"
    else:
        return "down"


async def get_features_status(use_cache: bool = True) -> list[FeatureStatus]:
    """Lấy trạng thái features với caching"""
    global _feature_cache

    now = time.time()

    # Kiểm tra cache
    if use_cache and _feature_cache and (now - _feature_cache[0] < TTL_SECONDS):
        return _feature_cache[1]

    # Evaluate features mới
    features = await evaluate_all_features()

    # Update cache
    _feature_cache = (now, features)

    return features


async def get_system_status() -> SystemStatus:
    """Lấy tổng quan trạng thái hệ thống"""
    features = await get_features_status()

    # Tính summary
    summary = {"operational": 0, "degraded": 0, "down": 0, "unknown": 0, "starting": 0}
    for feature in features:
        summary[feature.status] = summary.get(feature.status, 0) + 1

    # Overall status
    overall_status = calculate_overall_status(features)

    # SLO compliance (placeholder)
    config = load_config()
    slo_thresholds = config.get("slo_thresholds", {})
    slo_compliance = {
        "availability_target": slo_thresholds.get("availability_target", 0.99),
        "current_availability": summary["operational"] / len(features)
        if features
        else 0,
        "critical_features_down": sum(
            1 for f in features if f.critical and f.status in ["down", "unknown"]
        ),
    }

    return SystemStatus(
        overall_status=overall_status,
        last_updated=time.time(),
        features=features,
        summary=summary,
        slo_compliance=slo_compliance,
    )


# Background refresh (có thể gọi từ startup task)
async def refresh_cache_background():
    """Refresh cache trong background để không block requests"""
    try:
        await get_features_status(use_cache=False)
        logger.debug("Feature status cache refreshed")
    except Exception as e:
        logger.error(f"Lỗi refresh cache: {e}")


# Utility functions
def invalidate_cache():
    """Invalidate cache (dùng khi cập nhật config)"""
    global _feature_cache, _config_cache
    _feature_cache = None
    _config_cache = None


def get_feature_by_key(key: str, features: list[FeatureStatus]) -> FeatureStatus | None:
    """Tìm feature theo key"""
    return next((f for f in features if f.feature_key == key), None)
