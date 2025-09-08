"""
Risk Scoring Engine for Zero-Trust
Combines multiple signals to compute continuous risk assessment
"""
from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import math
import additional_signals
import anomaly
import bool
import decay_hours
import device_trust
import float
import hasattr
import int
import isinstance
import kwargs
import list
import mfa
import min
import name
import s
import self
import setattr
import signal_name
import stale
import str
import sum
import timestamp
import ts
import tuple
import user_id
import val
import value


class RiskSignal(BaseModel):
    name: str
    value: float  # 0.0-1.0
    weight: float = 1.0
    confidence: float = 1.0
    source: str = "system"


class RiskScore(BaseModel):
    score: float  # 0.0-1.0
    label: str    # low/medium/high/critical
    signals: List[RiskSignal] = []
    computed_at: datetime
    ttl_seconds: int = 300  # 5 minutes default


@dataclass
class UserRiskProfile:
    user_id: str
    baseline_risk: float = 0.1
    failed_logins: int = 0
    last_failure: datetime | None = None
    location_anomaly: float = 0.0
    device_changes: int = 0
    privilege_escalations: int = 0


class RiskEngine:
    """
    Continuous risk assessment engine with temporal decay
    """
    
    def __init__(self):
        self._profiles: Dict[str, UserRiskProfile] = {}
        self._signal_history: Dict[str, List[tuple[datetime, float]]] = defaultdict(list)
        
    def update_profile(self, user_id: str, **kwargs) -> None:
        """Update user risk profile"""
        if user_id not in self._profiles:
            self._profiles[user_id] = UserRiskProfile(user_id=user_id)
        
        profile = self._profiles[user_id]
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
    
    def record_signal(self, user_id: str, signal_name: str, value: float) -> None:
        """Record risk signal with timestamp"""
        now = datetime.utcnow()
        key = f"{user_id}:{signal_name}"
        self._signal_history[key].append((now, value))
        
        # Keep only last 24 hours
        cutoff = now - timedelta(hours=24)
        self._signal_history[key] = [
            (ts, val) for ts, val in self._signal_history[key] 
            if ts > cutoff
        ]
    
    def get_temporal_signal(self, user_id: str, signal_name: str, decay_hours: float = 2.0) -> float:
        """Get time-decayed signal value"""
        key = f"{user_id}:{signal_name}"
        if key not in self._signal_history:
            return 0.0
            
        now = datetime.utcnow()
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for timestamp, value in self._signal_history[key]:
            age_hours = (now - timestamp).total_seconds() / 3600
            decay_factor = math.exp(-age_hours / decay_hours)
            weighted_sum += value * decay_factor
            weight_sum += decay_factor
            
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def compute_risk(
        self, 
        user_id: str,
        additional_signals: List[RiskSignal] = None
    ) -> RiskScore:
        """
        Compute comprehensive risk score from multiple signals
        """
        now = datetime.utcnow()
        profile = self._profiles.get(user_id, UserRiskProfile(user_id=user_id))
        signals: List[RiskSignal] = additional_signals or []
        
        # Authentication failure signal
        auth_failures = self.get_temporal_signal(user_id, "auth_failure", decay_hours=1.0)
        if auth_failures > 0:
            signals.append(RiskSignal(
                name="auth_failures",
                value=min(1.0, auth_failures / 5.0),  # Normalize to 0-1
                weight=0.3,
                source="auth_monitor"
            ))
        
        # Location anomaly
        location_anomaly = self.get_temporal_signal(user_id, "location_anomaly", decay_hours=6.0)
        if location_anomaly > 0:
            signals.append(RiskSignal(
                name="location_anomaly", 
                value=location_anomaly,
                weight=0.2,
                source="geo_monitor"
            ))
        
        # Device trust
        device_risk = self.get_temporal_signal(user_id, "device_risk", decay_hours=12.0)
        if device_risk > 0:
            signals.append(RiskSignal(
                name="device_risk",
                value=device_risk,
                weight=0.25,
                source="device_monitor"
            ))
        
        # Behavioral anomaly
        behavior_anomaly = self.get_temporal_signal(user_id, "behavior_anomaly", decay_hours=4.0)
        if behavior_anomaly > 0:
            signals.append(RiskSignal(
                name="behavior_anomaly",
                value=behavior_anomaly, 
                weight=0.25,
                source="behavior_monitor"
            ))
        
        # Privilege escalation attempts
        privilege_risk = min(1.0, profile.privilege_escalations / 3.0)
        if privilege_risk > 0:
            signals.append(RiskSignal(
                name="privilege_escalation",
                value=privilege_risk,
                weight=0.4,
                source="privilege_monitor"
            ))
        
        # Compute weighted score
        if not signals:
            score = profile.baseline_risk
        else:
            weighted_sum = sum(s.value * s.weight * s.confidence for s in signals)
            weight_sum = sum(s.weight * s.confidence for s in signals)
            score = profile.baseline_risk + (weighted_sum / weight_sum if weight_sum > 0 else 0)
            score = min(1.0, score)
        
        # Determine risk label
        if score >= 0.8:
            label = "critical"
        elif score >= 0.6:
            label = "high"
        elif score >= 0.3:
            label = "medium"
        else:
            label = "low"
        
        return RiskScore(
            score=score,
            label=label,
            signals=signals,
            computed_at=now,
            ttl_seconds=300
        )


def compute_risk_from_signals(
    anomaly: float, 
    stale: float, 
    mfa: bool, 
    device_trust: bool,
    **kwargs
) -> RiskScore:
    """
    Legacy compatibility function - simplified risk computation
    """
    signals = [
        RiskSignal(name="anomaly", value=anomaly, weight=0.6),
        RiskSignal(name="token_staleness", value=stale, weight=0.3),
        RiskSignal(name="mfa_missing", value=0.1 if not mfa else 0.0, weight=0.1),
        RiskSignal(name="device_untrusted", value=0.1 if not device_trust else 0.0, weight=0.1)
    ]
    
    # Add optional signals
    for name, value in kwargs.items():
        if isinstance(value, (int, float)) and 0 <= value <= 1:
            signals.append(RiskSignal(name=name, value=value, weight=0.05))
    
    weighted_sum = sum(s.value * s.weight for s in signals)
    weight_sum = sum(s.weight for s in signals)
    score = weighted_sum / weight_sum if weight_sum > 0 else 0.0
    score = min(1.0, score)
    
    label = "low" if score < 0.33 else "medium" if score < 0.66 else "high"
    
    return RiskScore(
        score=score,
        label=label,
        signals=signals,
        computed_at=datetime.utcnow()
    )


# Global risk engine instance
risk_engine = RiskEngine()
