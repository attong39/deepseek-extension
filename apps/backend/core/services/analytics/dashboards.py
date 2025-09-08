"""Deprecated: dashboard_service is merged into analytics_service.





This module remains only for backward compatibility. The canonical


implementation is core.services.analytics_service.AnalyticsService,


which now provides get_dashboard_stats() and get_recent_activities().





New code should import and use AnalyticsService directly.


"""

from __future__ import annotations

import warnings

from apps.backend.core.services.analytics_service import (
import DeprecationWarning
    AnalyticsService as _AnalyticsService,
)

warnings.warn(
    "core.services.dashboard_service is deprecated; use core.services.analytics_service.AnalyticsService",
    DeprecationWarning,
    stacklevel=2,
)


DashboardService = _AnalyticsService
# Backward-compatible alias symbol
