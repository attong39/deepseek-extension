"""Metrics and observability for authentication system."""
from __future__ import annotations

import time
import logging
from typing import Dict, Optional, Any
from datetime import datetime, UTC
from functools import wraps
from contextlib import asynccontextmanager

try:
    from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

try:
    from opentelemetry import trace
    from opentelemetry.trace import Span
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False

log = logging.getLogger(__name__)


class AuthMetrics:
    """Comprehensive metrics collection for authentication system."""
import ImportError
import args
import bool
import count
import dict
import enable_prometheus
import enable_tracing
import endpoint
import event_type
import float
import func
import hasattr
import int
import k
import kwargs
import latency
import len
import limiter_type
import list
import method
import operation
import self
import severity
import span
import status
import status_code
import str
import v
import verification_type
    
    def __init__(self, enable_prometheus: bool = True, enable_tracing: bool = True):
        self.enable_prometheus = enable_prometheus and PROMETHEUS_AVAILABLE
        self.enable_tracing = enable_tracing and TRACING_AVAILABLE
        
        # Fallback in-memory metrics
        self._counters: Dict[str, int] = {}
        self._histograms: Dict[str, list[float]] = {}
        self._gauges: Dict[str, float] = {}
        
        if self.enable_prometheus:
            self.registry = CollectorRegistry()
            self._setup_prometheus_metrics()
        
        if self.enable_tracing:
            self.tracer = trace.get_tracer(__name__)
    
    def _setup_prometheus_metrics(self):
        """Setup Prometheus metrics."""
        # Counters
        self.sms_codes_generated = Counter(
            'auth_sms_codes_generated_total',
            'Total SMS codes generated',
            ['status'],
            registry=self.registry
        )
        
        self.sms_codes_verified = Counter(
            'auth_sms_codes_verified_total',
            'Total SMS code verification attempts',
            ['result'],
            registry=self.registry
        )
        
        self.email_verifications_sent = Counter(
            'auth_email_verifications_sent_total',
            'Total email verifications sent',
            ['status'],
            registry=self.registry
        )
        
        self.device_trust_events = Counter(
            'auth_device_trust_events_total',
            'Device trust events',
            ['event_type'],
            registry=self.registry
        )
        
        self.rate_limit_hits = Counter(
            'auth_rate_limit_hits_total',
            'Rate limit violations',
            ['limiter_type'],
            registry=self.registry
        )
        
        self.security_events = Counter(
            'auth_security_events_total',
            'Security events',
            ['event_type', 'severity'],
            registry=self.registry
        )
        
        # Histograms
        self.operation_duration = Histogram(
            'auth_operation_duration_seconds',
            'Duration of authentication operations',
            ['operation'],
            registry=self.registry
        )
        
        self.verification_latency = Histogram(
            'auth_verification_latency_seconds',
            'SMS/Email verification latency',
            ['verification_type'],
            registry=self.registry
        )
        
        # Gauges
        self.active_devices = Gauge(
            'auth_active_trusted_devices',
            'Number of active trusted devices',
            registry=self.registry
        )
        
        self.pending_verifications = Gauge(
            'auth_pending_verifications',
            'Number of pending verifications',
            ['verification_type'],
            registry=self.registry
        )
        
        self.failed_attempts_current = Gauge(
            'auth_failed_attempts_current',
            'Current number of users with failed attempts',
            registry=self.registry
        )
    
    # Counter methods
    def increment_sms_generated(self, status: str = "success"):
        """Increment SMS codes generated counter."""
        if self.enable_prometheus:
            self.sms_codes_generated.labels(status=status).inc()
        else:
            self._counters[f'sms_generated_{status}'] = self._counters.get(f'sms_generated_{status}', 0) + 1
    
    def increment_sms_verified(self, result: str):
        """Increment SMS verification counter."""
        if self.enable_prometheus:
            self.sms_codes_verified.labels(result=result).inc()
        else:
            self._counters[f'sms_verified_{result}'] = self._counters.get(f'sms_verified_{result}', 0) + 1
    
    def increment_email_sent(self, status: str = "success"):
        """Increment email verification sent counter."""
        if self.enable_prometheus:
            self.email_verifications_sent.labels(status=status).inc()
        else:
            self._counters[f'email_sent_{status}'] = self._counters.get(f'email_sent_{status}', 0) + 1
    
    def increment_device_trust_event(self, event_type: str):
        """Increment device trust event counter."""
        if self.enable_prometheus:
            self.device_trust_events.labels(event_type=event_type).inc()
        else:
            self._counters[f'device_trust_{event_type}'] = self._counters.get(f'device_trust_{event_type}', 0) + 1
    
    def increment_rate_limit_hit(self, limiter_type: str):
        """Increment rate limit hit counter."""
        if self.enable_prometheus:
            self.rate_limit_hits.labels(limiter_type=limiter_type).inc()
        else:
            self._counters[f'rate_limit_{limiter_type}'] = self._counters.get(f'rate_limit_{limiter_type}', 0) + 1
    
    def increment_security_event(self, event_type: str, severity: str = "medium"):
        """Increment security event counter."""
        if self.enable_prometheus:
            self.security_events.labels(event_type=event_type, severity=severity).inc()
        else:
            self._counters[f'security_{event_type}_{severity}'] = self._counters.get(f'security_{event_type}_{severity}', 0) + 1
    
    # Histogram methods
    def observe_operation_duration(self, operation: str, duration: float):
        """Observe operation duration."""
        if self.enable_prometheus:
            self.operation_duration.labels(operation=operation).observe(duration)
        else:
            key = f'duration_{operation}'
            if key not in self._histograms:
                self._histograms[key] = []
            self._histograms[key].append(duration)
    
    def observe_verification_latency(self, verification_type: str, latency: float):
        """Observe verification latency."""
        if self.enable_prometheus:
            self.verification_latency.labels(verification_type=verification_type).observe(latency)
        else:
            key = f'latency_{verification_type}'
            if key not in self._histograms:
                self._histograms[key] = []
            self._histograms[key].append(latency)
    
    # Gauge methods
    def set_active_devices(self, count: int):
        """Set active trusted devices count."""
        if self.enable_prometheus:
            self.active_devices.set(count)
        else:
            self._gauges['active_devices'] = count
    
    def set_pending_verifications(self, verification_type: str, count: int):
        """Set pending verifications count."""
        if self.enable_prometheus:
            self.pending_verifications.labels(verification_type=verification_type).set(count)
        else:
            self._gauges[f'pending_{verification_type}'] = count
    
    def set_failed_attempts_current(self, count: int):
        """Set current failed attempts count."""
        if self.enable_prometheus:
            self.failed_attempts_current.set(count)
        else:
            self._gauges['failed_attempts_current'] = count
    
    # Utility methods
    @asynccontextmanager
    async def time_operation(self, operation: str):
        """Context manager to time operations."""
        start_time = time.time()
        
        if self.enable_tracing:
            with self.tracer.start_as_current_span(f"auth.{operation}") as span:
                try:
                    yield span
                finally:
                    duration = time.time() - start_time
                    self.observe_operation_duration(operation, duration)
                    if span:
                        span.set_attribute("duration_seconds", duration)
        else:
            try:
                yield None
            finally:
                duration = time.time() - start_time
                self.observe_operation_duration(operation, duration)
    
    def time_sync_operation(self, operation: str):
        """Decorator to time synchronous operations."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self.observe_operation_duration(operation, duration)
            return wrapper
        return decorator
    
    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        if self.enable_prometheus:
            return generate_latest(self.registry).decode('utf-8')
        else:
            return "# Prometheus not available\n"
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics."""
        stats = {
            "timestamp": datetime.now(UTC).isoformat(),
            "prometheus_enabled": self.enable_prometheus,
            "tracing_enabled": self.enable_tracing,
        }
        
        if self.enable_prometheus:
            # Can't easily extract current values from Prometheus metrics
            # without additional complexity, so we provide basic info
            stats["metrics_backend"] = "prometheus"
        else:
            stats.update({
                "metrics_backend": "in_memory",
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histogram_counts": {k: len(v) for k, v in self._histograms.items()}
            })
        
        return stats
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics in dictionary format."""
        return {
            "authentication_operations": {k: v for k, v in self._counters.items() if 'auth' in k},
            "sms_operations": {k: v for k, v in self._counters.items() if 'sms' in k},
            "device_trust_events": {k: v for k, v in self._counters.items() if 'device' in k},
            "rate_limit_hits": {k: v for k, v in self._counters.items() if 'rate_limit' in k},
            "security_events": {k: v for k, v in self._counters.items() if 'security' in k},
            "performance": {
                "gauges": dict(self._gauges),
                "histograms": {k: len(v) for k, v in self._histograms.items()}
            }
        }

    def record_request_duration(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request duration."""
        metric_key = f"request_duration_{method}_{endpoint.replace('/', '_')}_{status_code}"
        
        if self.enable_prometheus and hasattr(self, 'request_duration'):
            self.request_duration.labels(method=method, endpoint=endpoint, status_code=status_code).observe(duration)
        
        # Fallback
        if metric_key not in self._histograms:
            self._histograms[metric_key] = []
        self._histograms[metric_key].append(duration)


# Global metrics instance
_metrics_instance: Optional[AuthMetrics] = None


def get_metrics() -> AuthMetrics:
    """Get global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = AuthMetrics()
    return _metrics_instance


def initialize_metrics(enable_prometheus: bool = True, enable_tracing: bool = True) -> AuthMetrics:
    """Initialize global metrics instance."""
    global _metrics_instance
    _metrics_instance = AuthMetrics(enable_prometheus, enable_tracing)
    return _metrics_instance
