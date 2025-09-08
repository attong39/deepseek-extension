"""
WebSocket Observability Metrics
===============================

Prometheus metrics for WebSocket monitoring with low-cardinality labels.
Tracks connections, messages, and latency for production observability.
"""

from prometheus_client import Gauge, Counter, Histogram

# WebSocket connection gauge
ws_connections = Gauge(
    "zeta_ws_connections", 
    "Số kết nối WebSocket đang mở", 
    ["route"]
)

# WebSocket message counter
ws_messages_total = Counter(
    "zeta_ws_messages_total", 
    "Tổng số message WS trao đổi", 
    ["route", "direction", "event"]
)

# WebSocket send latency histogram
ws_send_latency_seconds = Histogram(
    "zeta_ws_send_latency_seconds", 
    "Độ trễ gửi WS (s)", 
    ["route"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# WebSocket backpressure events
ws_backpressure_total = Counter(
    "zeta_ws_backpressure_total",
    "Số lần xảy ra backpressure (queue full)",
    ["route", "action"]  # action: dropped, throttled
)

# WebSocket errors
ws_errors_total = Counter(
    "zeta_ws_errors_total",
    "Lỗi WebSocket theo loại",
    ["route", "error_type"]
)

# WebSocket heartbeat metrics
ws_heartbeat_total = Counter(
    "zeta_ws_heartbeat_total",
    "Tổng số ping/pong heartbeat",
    ["route", "type"]  # type: ping_sent, pong_received, timeout
)
