"""
Enhanced Zero-Trust Middleware with JWT Integration and Prometheus Metrics
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge
import time

from apps.backend.core.security.zero_trust.policy import (
import Exception
import anomaly
import any
import app
import bool
import bypass_paths
import call_next
import dict
import e
import float
import getattr
import int
import ip
import jwt_secret
import len
import list
import locals
import method
import network
import path
import print
import request
import self
import set
import str
import super
import threat_detection_config
import user_id
    Subject, Resource, Environment, abac_decide, get_resource_policy
)
from apps.backend.core.security.zero_trust.risk import risk_engine
from apps.backend.core.security.threat_detection import ThreatDetectionService, SecurityEvent, LoginEvent
from apps.backend.core.security.jwt_adapter import JWTAuthAdapter


# Prometheus metrics
zt_decisions_total = Counter(
    "zeta_zt_decisions_total",
    "Zero-Trust access decisions", 
    ["allow", "risk_level", "resource_type", "action"]
)

zt_request_duration = Histogram(
    "zeta_zt_request_duration_seconds",
    "Zero-Trust middleware processing time",
    ["resource_type"]
)

zt_active_sessions = Gauge(
    "zeta_zt_active_sessions",
    "Number of active authenticated sessions"
)

zt_anomalies_detected = Counter(
    "zeta_zt_anomalies_detected_total",
    "Anomalies detected by threat detection",
    ["anomaly_type", "user_id"]
)

zt_risk_scores = Histogram(
    "zeta_zt_risk_scores",
    "Distribution of computed risk scores",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)


class ZeroTrustMiddleware(BaseHTTPMiddleware):
    """
    Enhanced Zero-Trust middleware with comprehensive security controls
    """
    
    def __init__(
        self, 
        app,
        jwt_secret: str,
        threat_detector: Optional[ThreatDetectionService] = None,
        bypass_paths: list[str] = None
    ):
        super().__init__(app)
        self.jwt_adapter = JWTAuthAdapter(jwt_secret)
        self.threat_detector = threat_detector or ThreatDetectionService()
        self.bypass_paths = bypass_paths or [
            "/health", "/metrics", "/docs", "/openapi.json", "/redoc",
            "/api/v1/auth/login", "/api/v1/auth/register"
        ]
        self.active_sessions = set()
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Skip Zero-Trust for public/health endpoints
        if any(request.url.path.startswith(path) for path in self.bypass_paths):
            return await call_next(request)
        
        try:
            # Extract authentication subject from JWT identity or fallback to headers
            client_ip = self._get_client_ip(request)
            
            # Check if JWT identity was already extracted by JWT dependency
            jwt_identity = getattr(request.state, "identity", None)
            
            if jwt_identity:
                # Use validated JWT identity
                subject = Subject(
                    user_id=jwt_identity.sub,
                    roles=jwt_identity.roles,
                    mfa=jwt_identity.mfa,
                    ip=client_ip,
                    device_trust=jwt_identity.device_trust
                )
            else:
                # Fallback to header-based extraction (legacy/demo mode)
                subject = self.jwt_adapter.extract_subject_from_headers(
                    dict(request.headers), 
                    client_ip
                )
                
                if not subject:
                    return JSONResponse(
                        {"detail": "authentication_required", "error": "missing_or_invalid_token"},
                        status_code=401
                    )
            
            # Track active session
            session_key = f"{subject.user_id}:{client_ip}"
            self.active_sessions.add(session_key)
            zt_active_sessions.set(len(self.active_sessions))
            
            # Get resource policy
            resource = get_resource_policy(request.url.path)
            
            # Build environment context
            now = datetime.now(timezone.utc)
            environment = Environment(
                hour=now.hour,
                geo=request.headers.get("cf-ipcountry"),  # Cloudflare geo header
                token_age_seconds=int(request.headers.get("x-token-age", "0")),
                request_rate=self._get_request_rate(subject.user_id),
                anomaly_score=self._get_user_anomaly_score(subject.user_id),
                network_trust=self._is_network_trusted(client_ip)
            )
            
            # Record security event for threat detection
            await self._record_security_event(request, subject, resource)
            
            # Compute risk score
            risk_score = risk_engine.compute_risk(
                subject.user_id,
                additional_signals=[]
            )
            zt_risk_scores.observe(risk_score.score)
            
            # Make access decision
            action = self._determine_action(request.method)
            decision = abac_decide(subject, action, resource, environment)
            
            # Apply risk-based adjustments
            if risk_score.label in ["high", "critical"]:
                decision.allow = False
                decision.reasons.append(f"risk_score_too_high_{risk_score.label}")
            
            # Record metrics
            zt_decisions_total.labels(
                allow=str(decision.allow).lower(),
                risk_level=decision.risk,
                resource_type=resource.resource_type,
                action=action
            ).inc()
            
            # Record processing time
            processing_time = time.time() - start_time
            zt_request_duration.labels(resource_type=resource.resource_type).observe(processing_time)
            
            # Handle access denial
            if not decision.allow:
                # Log security event
                await self._log_access_denial(request, subject, decision, risk_score)
                
                return JSONResponse({
                    "detail": "access_denied",
                    "risk": {
                        "level": decision.risk,
                        "score": risk_score.score,
                        "reasons": decision.reasons
                    },
                    "required_actions": decision.required_actions,
                    "request_id": request.headers.get("x-request-id", "unknown")
                }, status_code=403)
            
            # Add security context to request
            request.state.zero_trust = {
                "subject": subject,
                "decision": decision,
                "risk_score": risk_score,
                "resource": resource
            }
            
            # Execute request
            response = await call_next(request)
            
            # Add security headers
            response.headers["X-ZT-Risk-Level"] = decision.risk
            response.headers["X-ZT-Decision-ID"] = f"{subject.user_id}:{int(time.time())}"
            if decision.required_actions:
                response.headers["X-ZT-Required-Actions"] = ",".join(decision.required_actions)
            
            return response
            
        except Exception as e:
            # Log error and deny access
            return JSONResponse({
                "detail": "zero_trust_error",
                "error": str(e)
            }, status_code=500)
        finally:
            # Clean up session tracking
            if 'session_key' in locals():
                self.active_sessions.discard(session_key)
                zt_active_sessions.set(len(self.active_sessions))
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract real client IP considering proxies"""
        # Check common proxy headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def _determine_action(self, method: str) -> str:
        """Map HTTP method to ABAC action"""
        method_map = {
            "GET": "read",
            "POST": "write", 
            "PUT": "write",
            "PATCH": "write",
            "DELETE": "delete",
            "OPTIONS": "read",
            "HEAD": "read"
        }
        return method_map.get(method.upper(), "read")
    
    def _get_request_rate(self, user_id: str) -> float:
        """Get current request rate for user (requests per minute)"""
        # This would integrate with rate limiting system
        # For now, return 0 as placeholder
        return 0.0
    
    def _get_user_anomaly_score(self, user_id: str) -> float:
        """Get current anomaly score for user"""
        return self.threat_detector.get_user_risk_score(user_id)
    
    def _is_network_trusted(self, ip: str) -> bool:
        """Check if IP is from trusted network"""
        # Define trusted networks (internal, VPN, etc.)
        trusted_networks = [
            "192.168.", "10.", "172.16.", "172.17.", "172.18.",
            "172.19.", "172.20.", "172.21.", "172.22.", "172.23.",
            "172.24.", "172.25.", "172.26.", "172.27.", "172.28.",
            "172.29.", "172.30.", "172.31."
        ]
        
        return any(ip.startswith(network) for network in trusted_networks)
    
    async def _record_security_event(
        self, 
        request: Request, 
        subject: Subject, 
        resource: Resource
    ) -> None:
        """Record security event for threat analysis"""
        event = SecurityEvent(
            user_id=subject.user_id,
            event_type="api_call",
            ip=self._get_client_ip(request),
            user_agent=request.headers.get("user-agent", ""),
            success=True,  # Will be updated based on response
            resource=resource.name,
            timestamp=datetime.utcnow(),
            metadata={
                "method": request.method,
                "resource_type": resource.resource_type,
                "classification": resource.classification,
                "roles": subject.roles
            }
        )
        
        # Detect anomalies
        anomalies = self.threat_detector.record_api_call(event)
        
        # Record anomaly metrics
        for anomaly in anomalies:
            zt_anomalies_detected.labels(
                anomaly_type=anomaly.anomaly_type,
                user_id=subject.user_id
            ).inc()
            
            # Update user risk score based on anomaly
            risk_engine.record_signal(
                subject.user_id,
                anomaly.anomaly_type,
                anomaly.score
            )
    
    async def _log_access_denial(
        self,
        request: Request,
        subject: Subject,
        decision,
        risk_score
    ) -> None:
        """Log access denial for audit and analysis"""
        denial_event = {
            "event_type": "access_denied",
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": subject.user_id,
            "resource": request.url.path,
            "method": request.method,
            "ip": self._get_client_ip(request),
            "risk_level": decision.risk,
            "risk_score": risk_score.score,
            "reasons": decision.reasons,
            "required_actions": decision.required_actions,
            "user_agent": request.headers.get("user-agent", ""),
            "request_id": request.headers.get("x-request-id", "unknown")
        }
        
        # TODO: Send to security event log (SIEM, etc.)
        print(f"[SECURITY] Access denied: {denial_event}")


def create_zero_trust_middleware(
    jwt_secret: str,
    threat_detection_config: dict = None
) -> ZeroTrustMiddleware:
    """
    Factory function to create configured Zero-Trust middleware
    """
    threat_config = threat_detection_config or {}
    threat_detector = ThreatDetectionService(
        window_size=threat_config.get("window_size", 100),
        fail_threshold=threat_config.get("fail_threshold", 0.25),
        rate_limit_window=threat_config.get("rate_limit_window", 60),
        max_requests_per_minute=threat_config.get("max_requests_per_minute", 120)
    )
    
    return lambda app: ZeroTrustMiddleware(
        app=app,
        jwt_secret=jwt_secret,
        threat_detector=threat_detector
    )
