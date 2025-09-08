"""
Advanced Threat Detection Service
Real-time anomaly detection with multiple detection algorithms
"""
from __future__ import annotations
from collections import deque, defaultdict
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import statistics
import math
import abs
import bool
import dict
import e
import event
import fail_threshold
import float
import int
import ip
import len
import list
import max_requests_per_minute
import min
import rate_limit_window
import self
import set
import str
import sum
import ts
import user_id
import window_size


class SecurityEvent(BaseModel):
    user_id: str
    event_type: str  # "login", "api_call", "privilege_escalation", "data_access"
    ip: str
    user_agent: str = ""
    success: bool = True
    resource: str = ""
    timestamp: datetime
    metadata: Dict = {}


class LoginEvent(BaseModel):
    user_id: str
    ip: str
    success: bool
    timestamp: datetime = None
    user_agent: str = ""
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class AnomalyResult:
    is_anomaly: bool
    confidence: float  # 0.0-1.0
    anomaly_type: str
    score: float
    details: Dict = None


class ThreatDetectionService:
    """
    Multi-algorithm threat detection with behavioral profiling
    """
    
    def __init__(
        self, 
        window_size: int = 100,
        fail_threshold: float = 0.25,
        rate_limit_window: int = 60,
        max_requests_per_minute: int = 120
    ):
        self.window_size = window_size
        self.fail_threshold = fail_threshold
        self.rate_limit_window = rate_limit_window
        self.max_requests_per_minute = max_requests_per_minute
        
        # Event queues for different detection algorithms
        self._login_events: deque[LoginEvent] = deque(maxlen=window_size)
        self._api_events: deque[SecurityEvent] = deque(maxlen=window_size * 2)
        
        # User behavior baselines
        self._user_baselines: Dict[str, Dict] = defaultdict(dict)
        self._user_locations: Dict[str, List[str]] = defaultdict(list)
        self._user_agents: Dict[str, List[str]] = defaultdict(list)
        
        # Rate limiting tracking
        self._request_counts: Dict[str, List[datetime]] = defaultdict(list)
    
    def record_login(self, event: LoginEvent) -> List[AnomalyResult]:
        """Record login event and detect anomalies"""
        self._login_events.append(event)
        anomalies = []
        
        # Failed login rate detection
        fail_anomaly = self._detect_failed_login_anomaly(event)
        if fail_anomaly.is_anomaly:
            anomalies.append(fail_anomaly)
        
        # Geographic anomaly detection
        geo_anomaly = self._detect_geographic_anomaly(event)
        if geo_anomaly.is_anomaly:
            anomalies.append(geo_anomaly)
        
        # User agent anomaly
        ua_anomaly = self._detect_user_agent_anomaly(event)
        if ua_anomaly.is_anomaly:
            anomalies.append(ua_anomaly)
        
        # Update baselines
        self._update_user_baseline(event)
        
        return anomalies
    
    def record_api_call(self, event: SecurityEvent) -> List[AnomalyResult]:
        """Record API call and detect anomalies"""
        self._api_events.append(event)
        anomalies = []
        
        # Rate limiting detection
        rate_anomaly = self._detect_rate_anomaly(event)
        if rate_anomaly.is_anomaly:
            anomalies.append(rate_anomaly)
        
        # Unusual resource access
        resource_anomaly = self._detect_resource_anomaly(event)
        if resource_anomaly.is_anomaly:
            anomalies.append(resource_anomaly)
        
        # Time-based anomaly (unusual access hours)
        time_anomaly = self._detect_time_anomaly(event)
        if time_anomaly.is_anomaly:
            anomalies.append(time_anomaly)
        
        return anomalies
    
    def _detect_failed_login_anomaly(self, event: LoginEvent) -> AnomalyResult:
        """Detect brute force attacks through failed login rate"""
        if not self._login_events:
            return AnomalyResult(False, 0.0, "failed_login_rate", 0.0)
        
        # Look at recent events for same user/IP
        recent_cutoff = datetime.utcnow() - timedelta(minutes=10)
        recent_events = [
            e for e in self._login_events 
            if e.timestamp > recent_cutoff and (e.user_id == event.user_id or e.ip == event.ip)
        ]
        
        if len(recent_events) < 3:
            return AnomalyResult(False, 0.0, "failed_login_rate", 0.0)
        
        fail_rate = sum(1 for e in recent_events if not e.success) / len(recent_events)
        is_anomaly = fail_rate > self.fail_threshold
        confidence = min(1.0, fail_rate / self.fail_threshold)
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            anomaly_type="failed_login_rate",
            score=fail_rate,
            details={
                "recent_events": len(recent_events),
                "fail_rate": fail_rate,
                "threshold": self.fail_threshold
            }
        )
    
    def _detect_geographic_anomaly(self, event: LoginEvent) -> AnomalyResult:
        """Detect unusual geographic locations"""
        user_locations = self._user_locations[event.user_id]
        
        if len(user_locations) < 3:  # Not enough baseline
            return AnomalyResult(False, 0.0, "geographic", 0.0)
        
        # Simple heuristic: if IP prefix is very different from baseline
        event_prefix = '.'.join(event.ip.split('.')[:2])  # First two octets
        baseline_prefixes = set('.'.join(ip.split('.')[:2]) for ip in user_locations[-10:])
        
        is_anomaly = event_prefix not in baseline_prefixes
        confidence = 0.7 if is_anomaly else 0.0
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            anomaly_type="geographic",
            score=1.0 if is_anomaly else 0.0,
            details={
                "event_prefix": event_prefix,
                "known_prefixes": list(baseline_prefixes)
            }
        )
    
    def _detect_user_agent_anomaly(self, event: LoginEvent) -> AnomalyResult:
        """Detect unusual user agents"""
        user_agents = self._user_agents[event.user_id]
        
        if len(user_agents) < 2:
            return AnomalyResult(False, 0.0, "user_agent", 0.0)
        
        # Check if user agent is completely new
        is_anomaly = event.user_agent not in user_agents[-5:]  # Last 5 UAs
        confidence = 0.5 if is_anomaly else 0.0
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            anomaly_type="user_agent", 
            score=1.0 if is_anomaly else 0.0
        )
    
    def _detect_rate_anomaly(self, event: SecurityEvent) -> AnomalyResult:
        """Detect unusual request rates"""
        now = datetime.utcnow()
        user_requests = self._request_counts[event.user_id]
        
        # Clean old requests
        cutoff = now - timedelta(seconds=self.rate_limit_window)
        user_requests[:] = [ts for ts in user_requests if ts > cutoff]
        user_requests.append(now)
        
        request_rate = len(user_requests)
        is_anomaly = request_rate > self.max_requests_per_minute
        confidence = min(1.0, request_rate / self.max_requests_per_minute) if is_anomaly else 0.0
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            anomaly_type="request_rate",
            score=request_rate / self.max_requests_per_minute,
            details={
                "requests_per_minute": request_rate,
                "threshold": self.max_requests_per_minute
            }
        )
    
    def _detect_resource_anomaly(self, event: SecurityEvent) -> AnomalyResult:
        """Detect access to unusual resources"""
        baseline = self._user_baselines[event.user_id]
        accessed_resources = baseline.get("resources", set())
        
        if len(accessed_resources) < 5:  # Not enough baseline
            return AnomalyResult(False, 0.0, "resource_access", 0.0)
        
        # Check if resource is completely new
        is_anomaly = event.resource not in accessed_resources
        
        # Higher confidence for sensitive resources
        confidence = 0.3
        if "/admin" in event.resource or "/security" in event.resource:
            confidence = 0.8
        elif "/agents" in event.resource:
            confidence = 0.6
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence if is_anomaly else 0.0,
            anomaly_type="resource_access",
            score=1.0 if is_anomaly else 0.0,
            details={"resource": event.resource}
        )
    
    def _detect_time_anomaly(self, event: SecurityEvent) -> AnomalyResult:
        """Detect access during unusual hours"""
        baseline = self._user_baselines[event.user_id]
        access_hours = baseline.get("access_hours", [])
        
        if len(access_hours) < 10:  # Not enough baseline
            return AnomalyResult(False, 0.0, "time_based", 0.0)
        
        current_hour = event.timestamp.hour
        
        # Calculate if current hour is within normal range
        if access_hours:
            mean_hour = statistics.mean(access_hours)
            std_hour = statistics.stdev(access_hours) if len(access_hours) > 1 else 0
            
            # Use 2 standard deviations as threshold
            is_anomaly = abs(current_hour - mean_hour) > (2 * std_hour + 1)
            confidence = min(1.0, abs(current_hour - mean_hour) / (2 * std_hour + 1)) if is_anomaly else 0.0
        else:
            is_anomaly = False
            confidence = 0.0
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            confidence=confidence,
            anomaly_type="time_based",
            score=confidence,
            details={
                "current_hour": current_hour,
                "baseline_hours": access_hours[-20:]  # Last 20 access hours
            }
        )
    
    def _update_user_baseline(self, event: LoginEvent) -> None:
        """Update user behavioral baseline"""
        # Update location history
        self._user_locations[event.user_id].append(event.ip)
        if len(self._user_locations[event.user_id]) > 20:
            self._user_locations[event.user_id] = self._user_locations[event.user_id][-20:]
        
        # Update user agent history
        if event.user_agent:
            self._user_agents[event.user_id].append(event.user_agent)
            if len(self._user_agents[event.user_id]) > 10:
                self._user_agents[event.user_id] = self._user_agents[event.user_id][-10:]
    
    def get_user_risk_score(self, user_id: str) -> float:
        """Get overall risk score for user based on recent activity"""
        recent_cutoff = datetime.utcnow() - timedelta(hours=1)
        
        # Count recent anomalies for this user
        recent_login_anomalies = 0
        for event in self._login_events:
            if event.user_id == user_id and event.timestamp > recent_cutoff:
                anomalies = self.record_login(event)
                recent_login_anomalies += len(anomalies)
        
        recent_api_anomalies = 0
        for event in self._api_events:
            if event.user_id == user_id and event.timestamp > recent_cutoff:
                anomalies = self.record_api_call(event)
                recent_api_anomalies += len(anomalies)
        
        # Normalize to 0-1 scale
        total_anomalies = recent_login_anomalies + recent_api_anomalies
        risk_score = min(1.0, total_anomalies / 10.0)  # Cap at 10 anomalies = max risk
        
        return risk_score
    
    def anomaly_ratio(self) -> float:
        """Legacy method - returns failed login ratio"""
        if not self._login_events:
            return 0.0
        
        recent_cutoff = datetime.utcnow() - timedelta(minutes=30)
        recent_events = [e for e in self._login_events if e.timestamp > recent_cutoff]
        
        if not recent_events:
            return 0.0
        
        fail_count = sum(1 for e in recent_events if not e.success)
        return fail_count / len(recent_events)
