"""
API endpoints cho AI Status Dashboard
Cung cấp real-time status của các tính năng AI
"""

from __future__ import annotations

import logging
from typing import Any

from app.status.feature_registry import (
import Exception
import dict
import e
import f
import feature_key
import len
import list
import max
import next
import round
import str
    get_features_status,
    get_system_status,
    invalidate_cache,
    refresh_cache_background,
)
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/status", tags=["AI Status"])


@router.get("/features", response_model=list[dict[str, Any]])
async def list_features() -> list[dict[str, Any]]:
    """
    Lấy danh sách trạng thái tất cả features
    Kết quả được cache 15 giây
    """
    try:
        features = await get_features_status()
        return [feature.model_dump() for feature in features]
    except Exception as e:
        logger.error(f"Lỗi get features status: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to get features status"
        ) from e


@router.get("/summary", response_model=dict[str, Any])
async def status_summary() -> dict[str, Any]:
    """
    Tổng quan trạng thái hệ thống
    Bao gồm overall status và counts theo từng trạng thái
    """
    try:
        system_status = await get_system_status()
        return system_status.model_dump()
    except Exception as e:
        logger.error(f"Lỗi get system status: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to get system status"
        ) from e


@router.get("/health")
async def status_health() -> dict[str, Any]:
    """
    Lightweight status endpoint cho health check
    Chỉ trả về overall status và critical features
    """
    try:
        system_status = await get_system_status()

        # Lọc critical features
        critical_features = [
            f
            for f in system_status.features
            if f.critical and f.status in ["down", "unknown"]
        ]

        return {
            "status": system_status.overall_status,
            "timestamp": system_status.last_updated,
            "critical_issues": len(critical_features),
            "critical_features_down": [
                {"key": f.feature_key, "name": f.feature_name, "status": f.status}
                for f in critical_features
            ],
        }

    except Exception as e:
        logger.error(f"Lỗi get status health: {e}")
        return {
            "status": "unknown",
            "timestamp": 0,
            "critical_issues": -1,
            "error": str(e),
        }


@router.get("/feature/{feature_key}")
async def get_feature_detail(feature_key: str) -> dict[str, Any]:
    """
    Chi tiết trạng thái của một feature cụ thể
    """
    try:
        features = await get_features_status()

        feature = next((f for f in features if f.feature_key == feature_key), None)
        if not feature:
            raise HTTPException(
                status_code=404, detail=f"Feature '{feature_key}' not found"
            )

        return feature.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi get feature {feature_key}: {e}")
        raise HTTPException(
            status_code=503, detail="Unable to get feature status"
        ) from e


@router.post("/refresh")
async def refresh_status_cache() -> dict[str, str]:
    """
    Force refresh status cache
    Chỉ dành cho admin/debugging
    """
    try:
        # Invalidate current cache
        invalidate_cache()

        # Trigger background refresh
        await refresh_cache_background()

        return {"message": "Status cache refreshed successfully"}

    except Exception as e:
        logger.error(f"Lỗi refresh cache: {e}")
        raise HTTPException(status_code=503, detail="Unable to refresh cache") from e


@router.get("/slo")
async def get_slo_status() -> dict[str, Any]:
    """
    SLO (Service Level Objectives) compliance status
    Hiển thị compliance với availability targets
    """
    try:
        system_status = await get_system_status()

        slo_data = system_status.slo_compliance

        # Tính toán SLO compliance
        total_features = len(system_status.features)
        operational_features = system_status.summary.get("operational", 0)
        current_availability = (
            operational_features / total_features if total_features > 0 else 0
        )

        target_availability = slo_data.get("availability_target", 0.99)

        return {
            "availability": {
                "current": round(current_availability, 4),
                "target": target_availability,
                "compliance": current_availability >= target_availability,
                "gap": max(0, target_availability - current_availability),
            },
            "features": {
                "total": total_features,
                "operational": operational_features,
                "critical_down": slo_data.get("critical_features_down", 0),
            },
            "last_updated": system_status.last_updated,
        }

    except Exception as e:
        logger.error(f"Lỗi get SLO status: {e}")
        raise HTTPException(status_code=503, detail="Unable to get SLO status") from e
