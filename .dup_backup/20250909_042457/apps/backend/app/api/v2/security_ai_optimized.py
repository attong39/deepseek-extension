import Exception
import ValueError
import a
import action
import active_alerts
import alert_id
import any
import attempts
import background_tasks
import bool
import dict
import domain
import e
import event_data
import events
import f
import float
import ind
import ind_data
import int
import intel_update
import ip_address
import len
import limit
import list
import match
import max
import min
import progress
import scan_request
import scan_result
import scan_results
import security_events
import self
import set
import staticmethod
import status
import str
import threat_level
import tuple
import update_request
import user
import v
import window_minutes
import x
# zeta_vn/app/api/v2/security_ai_optimized.py
"""
Security AI v2 - Optimized với Advanced Threat Detection

Tối ưu hóa:
1. Real-time threat detection với ML models
2. Behavioral analysis và anomaly detection
3. Zero-day exploit detection với pattern matching
4. Automated incident response với playbooks
"""

from __future__ import annotations

import asyncio
import ipaddress
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

import numpy as np
from apps.backend.app.api.v1._common_audit import audit
from apps.backend.app.api.v1._common_cache import acached
from apps.backend.app.api.v1._common_security import Role, User, require_roles
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

router = APIRouter(prefix="/security-ai", tags=["SecurityAI-V2-Optimized"])

# === Constants ===

THREAT_NOT_FOUND = "Threat not found"
SCAN_NOT_FOUND = "Scan not found"
MAX_ALERT_HISTORY = 10000
ANOMALY_THRESHOLD = -0.5  # Isolation Forest threshold

# === Security Models ===


class ThreatLevel(str, Enum):
    LOW = "low"  # Minor threats
    MEDIUM = "medium"  # Moderate threats
    HIGH = "high"  # Serious threats
    CRITICAL = "critical"  # Immediate action required
    UNKNOWN = "unknown"  # Threat level uncertain


class ThreatCategory(str, Enum):
    MALWARE = "malware"  # Virus, trojan, etc.
    INTRUSION = "intrusion"  # Unauthorized access
    DDOS = "ddos"  # Denial of service
    DATA_BREACH = "data_breach"  # Data exfiltration
    PHISHING = "phishing"  # Social engineering
    INJECTION = "injection"  # SQL, XSS, etc.
    PRIVILEGE_ESCALATION = "privilege_escalation"
    ZERO_DAY = "zero_day"  # Unknown exploits
    BEHAVIORAL = "behavioral"  # Unusual behavior
    NETWORK_ANOMALY = "network_anomaly"


class ScanType(str, Enum):
    VULNERABILITY = "vulnerability"  # System vulnerabilities
    MALWARE = "malware"  # Malware detection
    NETWORK = "network"  # Network scanning
    BEHAVIORAL = "behavioral"  # Behavior analysis
    CODE = "code"  # Source code analysis
    REAL_TIME = "real_time"  # Live monitoring


class AlertStatus(str, Enum):
    OPEN = "open"  # Active alert
    INVESTIGATING = "investigating"  # Under investigation
    RESOLVED = "resolved"  # Threat resolved
    FALSE_POSITIVE = "false_positive"  # Not a real threat
    SUPPRESSED = "suppressed"  # Temporarily ignored


class ResponseAction(str, Enum):
    BLOCK_IP = "block_ip"  # Block IP address
    QUARANTINE = "quarantine"  # Isolate resource
    ALERT_ADMIN = "alert_admin"  # Notify administrators
    LOG_INCIDENT = "log_incident"  # Record incident
    AUTO_REMEDIATE = "auto_remediate"  # Automatic fix
    ESCALATE = "escalate"  # Escalate to SOC


@dataclass
class ThreatIndicator:
    """Threat intelligence indicator"""

    indicator_type: str  # IP, domain, hash, etc.
    value: str  # Actual indicator value
    threat_level: ThreatLevel
    category: ThreatCategory
    description: str
    confidence: float  # 0.0 - 1.0
    first_seen: datetime
    last_seen: datetime
    source: str  # Intelligence source

    def to_dict(self) -> dict[str, Any]:
        return {
            "indicator_type": self.indicator_type,
            "value": self.value,
            "threat_level": self.threat_level,
            "category": self.category,
            "description": self.description,
            "confidence": self.confidence,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "source": self.source,
        }


@dataclass
class SecurityEvent:
    """Security event data"""

    event_id: str
    event_type: str
    source_ip: str
    user_id: str | None = None
    resource: str | None = None
    action: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    threat_score: float = 0.0

    def to_features(self) -> list[float]:
        """Convert to ML feature vector"""
        features = []

        # IP address features (simplified)
        try:
            ip = ipaddress.ip_address(self.source_ip)
            features.extend(
                [
                    1.0 if ip.is_private else 0.0,
                    1.0 if ip.is_multicast else 0.0,
                    1.0 if ip.is_loopback else 0.0,
                ]
            )
        except ValueError:
            features.extend([0.0, 0.0, 0.0])

        # Time-based features
        hour = self.timestamp.hour
        features.extend(
            [
                hour / 24.0,  # Normalized hour
                1.0 if 22 <= hour or hour <= 6 else 0.0,  # Night time
                1.0 if self.timestamp.weekday() >= 5 else 0.0,  # Weekend
            ]
        )

        # Action type features (one-hot encoded)
        common_actions = ["login", "access", "download", "upload", "delete"]
        for action in common_actions:
            features.append(1.0 if self.action == action else 0.0)

        # Resource type features
        features.append(len(self.resource) if self.resource else 0.0)
        features.append(1.0 if self.user_id else 0.0)

        return features


@dataclass
class SecurityAlert:
    """Security alert with threat details"""

    alert_id: str
    threat_category: ThreatCategory
    threat_level: ThreatLevel
    title: str
    description: str
    source_event: SecurityEvent
    indicators: list[ThreatIndicator] = field(default_factory=list)
    status: AlertStatus = AlertStatus.OPEN
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    assigned_to: str | None = None
    response_actions: list[ResponseAction] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "threat_category": self.threat_category,
            "threat_level": self.threat_level,
            "title": self.title,
            "description": self.description,
            "source_event": {
                "event_id": self.source_event.event_id,
                "source_ip": self.source_event.source_ip,
                "timestamp": self.source_event.timestamp.isoformat(),
            },
            "indicators": [ind.to_dict() for ind in self.indicators],
            "status": self.status,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "assigned_to": self.assigned_to,
            "response_actions": self.response_actions,
        }


class SecurityScanRequest(BaseModel):
    scan_type: ScanType
    target: str = Field(min_length=1, max_length=500)
    deep_scan: bool = False
    custom_rules: list[str] = Field(default_factory=list)


class EventSubmission(BaseModel):
    event_type: str
    source_ip: str = Field(regex=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    user_id: str | None = None
    resource: str | None = None
    action: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @validator("source_ip")
    def validate_ip(self, v):
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            raise ValueError("Invalid IP address format")


class ThreatIntelUpdate(BaseModel):
    indicators: list[dict[str, Any]]
    source: str = Field(min_length=1, max_length=100)


class AlertUpdateRequest(BaseModel):
    status: AlertStatus
    assigned_to: str | None = None
    notes: str | None = None


# === ML-based Anomaly Detection ===


class AnomalyDetector:
    """Machine learning based anomaly detection"""

    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_history: deque = deque(maxlen=1000)

    def add_training_data(self, events: list[SecurityEvent]):
        """Add events for training"""
        features = [event.to_features() for event in events]
        self.feature_history.extend(features)

        if len(self.feature_history) >= 100:  # Minimum training size
            self._train_model()

    def _train_model(self):
        """Train the anomaly detection model"""
        if len(self.feature_history) < 50:
            return

        # Convert to numpy array
        X = np.array(list(self.feature_history))

        # Fit scaler and model
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True

    def detect_anomaly(self, event: SecurityEvent) -> tuple[bool, float]:
        """Detect if event is anomalous"""
        if not self.is_trained:
            return False, 0.0

        features = np.array([event.to_features()])
        features_scaled = self.scaler.transform(features)

        # Get anomaly score
        score = self.model.decision_function(features_scaled)[0]
        is_anomaly = score < ANOMALY_THRESHOLD

        # Convert score to confidence (0-1)
        confidence = max(0.0, min(1.0, (ANOMALY_THRESHOLD - score) / 2.0))

        return is_anomaly, confidence


# === Pattern-based Threat Detection ===


class ThreatPatterns:
    """Rule-based threat pattern detection"""

    @staticmethod
    def detect_brute_force(
        events: list[SecurityEvent], window_minutes: int = 5
    ) -> SecurityAlert | None:
        """Detect brute force login attempts"""
        now = datetime.now(UTC)
        recent_events = [
            e
            for e in events
            if e.action == "login"
            and (now - e.timestamp).total_seconds() <= window_minutes * 60
        ]

        # Group by source IP
        ip_attempts = defaultdict(int)
        for event in recent_events:
            ip_attempts[event.source_ip] += 1

        # Check for excessive attempts
        for ip, attempts in ip_attempts.items():
            if attempts >= 10:  # Threshold for brute force
                return SecurityAlert(
                    alert_id=f"alert_{uuid.uuid4().hex[:8]}",
                    threat_category=ThreatCategory.INTRUSION,
                    threat_level=ThreatLevel.HIGH,
                    title=f"Brute Force Attack Detected from {ip}",
                    description=f"Detected {attempts} failed login attempts from {ip} in {window_minutes} minutes",
                    source_event=recent_events[-1],  # Latest event
                    confidence=min(1.0, attempts / 20.0),  # Scale confidence
                    response_actions=[
                        ResponseAction.BLOCK_IP,
                        ResponseAction.ALERT_ADMIN,
                    ],
                )

        return None

    @staticmethod
    def detect_data_exfiltration(
        events: list[SecurityEvent],
    ) -> SecurityAlert | None:
        """Detect unusual data download patterns"""
        download_events = [e for e in events if e.action == "download"]

        if not download_events:
            return None

        # Calculate download volume (simplified)
        recent_downloads = [
            e
            for e in download_events
            if (datetime.now(UTC) - e.timestamp).total_seconds() <= 3600  # Last hour
        ]

        if len(recent_downloads) >= 50:  # Unusual volume
            return SecurityAlert(
                alert_id=f"alert_{uuid.uuid4().hex[:8]}",
                threat_category=ThreatCategory.DATA_BREACH,
                threat_level=ThreatLevel.MEDIUM,
                title="Unusual Data Access Pattern",
                description=f"Detected {len(recent_downloads)} downloads in the last hour",
                source_event=recent_downloads[-1],
                confidence=0.7,
                response_actions=[
                    ResponseAction.ALERT_ADMIN,
                    ResponseAction.LOG_INCIDENT,
                ],
            )

        return None

    @staticmethod
    def detect_privilege_escalation(
        events: list[SecurityEvent],
    ) -> SecurityAlert | None:
        """Detect privilege escalation attempts"""
        admin_events = [
            e
            for e in events
            if e.action in ["admin_access", "privilege_change", "user_create"]
        ]

        # Look for rapid privilege changes
        if len(admin_events) >= 3:
            time_span = (
                admin_events[-1].timestamp - admin_events[0].timestamp
            ).total_seconds()
            if time_span <= 300:  # 5 minutes
                return SecurityAlert(
                    alert_id=f"alert_{uuid.uuid4().hex[:8]}",
                    threat_category=ThreatCategory.PRIVILEGE_ESCALATION,
                    threat_level=ThreatLevel.HIGH,
                    title="Rapid Privilege Changes Detected",
                    description=f"Detected {len(admin_events)} privilege operations in {time_span:.0f} seconds",
                    source_event=admin_events[-1],
                    confidence=0.8,
                    response_actions=[
                        ResponseAction.ALERT_ADMIN,
                        ResponseAction.QUARANTINE,
                    ],
                )

        return None


# === Threat Intelligence Engine ===


class ThreatIntelligence:
    """Threat intelligence management"""

    def __init__(self):
        self.indicators: dict[str, ThreatIndicator] = {}
        self.ip_blacklist: set[str] = set()
        self.domain_blacklist: set[str] = set()
        self.hash_blacklist: set[str] = set()

    def add_indicators(self, indicators: list[ThreatIndicator]):
        """Add threat indicators"""
        for indicator in indicators:
            key = f"{indicator.indicator_type}:{indicator.value}"
            self.indicators[key] = indicator

            # Update blacklists
            if indicator.indicator_type == "ip":
                self.ip_blacklist.add(indicator.value)
            elif indicator.indicator_type == "domain":
                self.domain_blacklist.add(indicator.value)
            elif indicator.indicator_type == "hash":
                self.hash_blacklist.add(indicator.value)

    def check_event(self, event: SecurityEvent) -> list[ThreatIndicator]:
        """Check event against threat intelligence"""
        matches = []

        # Check source IP
        if event.source_ip in self.ip_blacklist:
            ip_key = f"ip:{event.source_ip}"
            if ip_key in self.indicators:
                matches.append(self.indicators[ip_key])

        # Check resource (if it's a URL/domain)
        if event.resource and any(
            domain in event.resource for domain in self.domain_blacklist
        ):
            for domain in self.domain_blacklist:
                if domain in event.resource:
                    domain_key = f"domain:{domain}"
                    if domain_key in self.indicators:
                        matches.append(self.indicators[domain_key])

        return matches


# === Automated Response System ===


class IncidentResponse:
    """Automated incident response"""

    @staticmethod
    async def execute_response(alert: SecurityAlert) -> dict[str, Any]:
        """Execute automated response actions"""
        results = {}

        for action in alert.response_actions:
            if action == ResponseAction.BLOCK_IP:
                results[action] = await IncidentResponse._block_ip(
                    alert.source_event.source_ip
                )
            elif action == ResponseAction.ALERT_ADMIN:
                results[action] = await IncidentResponse._alert_admin(alert)
            elif action == ResponseAction.LOG_INCIDENT:
                results[action] = await IncidentResponse._log_incident(alert)
            elif action == ResponseAction.QUARANTINE:
                results[action] = await IncidentResponse._quarantine_resource(alert)

        return results

    @staticmethod
    async def _block_ip(ip_address: str) -> dict[str, Any]:
        """Block IP address"""
        # Placeholder - integrate with firewall/WAF
        await audit(
            "security.response.block_ip", actor="system", payload={"ip": ip_address}
        )
        return {"status": "blocked", "ip": ip_address}

    @staticmethod
    async def _alert_admin(alert: SecurityAlert) -> dict[str, Any]:
        """Send alert to administrators"""
        # Placeholder - integrate with notification system
        await audit(
            "security.response.alert_admin",
            actor="system",
            payload={"alert_id": alert.alert_id},
        )
        return {"status": "notified", "alert_id": alert.alert_id}

    @staticmethod
    async def _log_incident(alert: SecurityAlert) -> dict[str, Any]:
        """Log security incident"""
        await audit("security.incident", actor="system", payload=alert.to_dict())
        return {"status": "logged", "alert_id": alert.alert_id}

    @staticmethod
    async def _quarantine_resource(alert: SecurityAlert) -> dict[str, Any]:
        """Quarantine affected resource"""
        # Placeholder - integrate with access control
        resource = alert.source_event.resource
        await audit(
            "security.response.quarantine",
            actor="system",
            payload={"resource": resource},
        )
        return {"status": "quarantined", "resource": resource}


# === Global State ===

security_events: deque = deque(maxlen=10000)
active_alerts: dict[str, SecurityAlert] = {}
threat_intel = ThreatIntelligence()
anomaly_detector = AnomalyDetector()
scan_results: dict[str, dict[str, Any]] = {}

# === API Endpoints ===


@router.post("/events/submit")
async def submit_security_event(
    event_data: EventSubmission,
    background_tasks: BackgroundTasks,
    user: User = Depends(require_roles(Role.USER)),
):
    """Submit security event for analysis"""
    event = SecurityEvent(
        event_id=f"event_{uuid.uuid4().hex[:8]}",
        event_type=event_data.event_type,
        source_ip=event_data.source_ip,
        user_id=event_data.user_id,
        resource=event_data.resource,
        action=event_data.action,
        metadata=event_data.metadata,
    )

    security_events.append(event)

    await audit(
        "security.event.submit",
        actor=user.sub,
        payload={
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source_ip": event.source_ip,
        },
    )

    # Trigger analysis in background
    background_tasks.add_task(_analyze_event, event)

    return {"event_id": event.event_id, "status": "submitted", "analysis_queued": True}


async def _analyze_event(event: SecurityEvent):
    """Analyze security event for threats"""
    alerts_generated = []

    # Check against threat intelligence
    threat_matches = threat_intel.check_event(event)
    if threat_matches:
        alert = SecurityAlert(
            alert_id=f"alert_{uuid.uuid4().hex[:8]}",
            threat_category=threat_matches[0].category,
            threat_level=threat_matches[0].threat_level,
            title=f"Threat Intelligence Match: {threat_matches[0].description}",
            description=f"Event matches known threat indicator: {threat_matches[0].value}",
            source_event=event,
            indicators=threat_matches,
            confidence=max(match.confidence for match in threat_matches),
            response_actions=[ResponseAction.BLOCK_IP, ResponseAction.ALERT_ADMIN],
        )
        active_alerts[alert.alert_id] = alert
        alerts_generated.append(alert)

    # ML-based anomaly detection
    is_anomaly, confidence = anomaly_detector.detect_anomaly(event)
    if is_anomaly and confidence > 0.7:
        alert = SecurityAlert(
            alert_id=f"alert_{uuid.uuid4().hex[:8]}",
            threat_category=ThreatCategory.BEHAVIORAL,
            threat_level=ThreatLevel.MEDIUM if confidence > 0.9 else ThreatLevel.LOW,
            title="Behavioral Anomaly Detected",
            description=f"Event shows unusual patterns (confidence: {confidence:.2f})",
            source_event=event,
            confidence=confidence,
            response_actions=[ResponseAction.LOG_INCIDENT],
        )
        active_alerts[alert.alert_id] = alert
        alerts_generated.append(alert)

    # Pattern-based detection
    recent_events = list(security_events)[-100:]  # Last 100 events

    # Check for brute force
    brute_force_alert = ThreatPatterns.detect_brute_force(recent_events)
    if brute_force_alert:
        active_alerts[brute_force_alert.alert_id] = brute_force_alert
        alerts_generated.append(brute_force_alert)

    # Check for data exfiltration
    exfiltration_alert = ThreatPatterns.detect_data_exfiltration(recent_events)
    if exfiltration_alert:
        active_alerts[exfiltration_alert.alert_id] = exfiltration_alert
        alerts_generated.append(exfiltration_alert)

    # Execute automated responses
    for alert in alerts_generated:
        if alert.response_actions:
            await IncidentResponse.execute_response(alert)

    # Update ML model
    anomaly_detector.add_training_data([event])


@router.post("/scans/start")
async def start_security_scan(
    scan_request: SecurityScanRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(require_roles(Role.ADMIN)),
):
    """Start security scan"""
    scan_id = f"scan_{uuid.uuid4().hex[:8]}"

    await audit(
        "security.scan.start",
        actor=user.sub,
        payload={
            "scan_id": scan_id,
            "scan_type": scan_request.scan_type,
            "target": scan_request.target,
        },
    )

    # Initialize scan result
    scan_results[scan_id] = {
        "scan_id": scan_id,
        "scan_type": scan_request.scan_type,
        "target": scan_request.target,
        "status": "running",
        "started_at": datetime.now(UTC).isoformat(),
        "progress": 0,
        "findings": [],
    }

    # Start scan in background
    background_tasks.add_task(_execute_scan, scan_id, scan_request)

    return {
        "scan_id": scan_id,
        "status": "started",
        "estimated_duration_minutes": 10 if scan_request.deep_scan else 5,
    }


async def _execute_scan(scan_id: str, scan_request: SecurityScanRequest):
    """Execute security scan"""
    scan_results[scan_id]

    try:
        # Simulate scan progress
        for progress in [25, 50, 75, 100]:
            await asyncio.sleep(1)  # Simulate work
            scan_result["progress"] = progress

        # Generate mock findings based on scan type
        findings = []

        if scan_request.scan_type == ScanType.VULNERABILITY:
            findings = [
                {
                    "type": "vulnerability",
                    "severity": "medium",
                    "title": "Outdated SSL Certificate",
                    "description": "SSL certificate expires in 30 days",
                    "recommendation": "Renew SSL certificate",
                },
                {
                    "type": "vulnerability",
                    "severity": "low",
                    "title": "Missing Security Headers",
                    "description": "Content-Security-Policy header not found",
                    "recommendation": "Add security headers",
                },
            ]

        elif scan_request.scan_type == ScanType.MALWARE:
            findings = [
                {
                    "type": "suspicious_file",
                    "severity": "high",
                    "title": "Potentially Malicious Script",
                    "description": "Detected obfuscated JavaScript",
                    "file_path": "/tmp/suspicious.js",
                    "recommendation": "Review and remove if malicious",
                }
            ]

        scan_result.update(
            {
                "status": "completed",
                "completed_at": datetime.now(UTC).isoformat(),
                "findings": findings,
                "summary": {
                    "total_findings": len(findings),
                    "high_severity": len(
                        [f for f in findings if f.get("severity") == "high"]
                    ),
                    "medium_severity": len(
                        [f for f in findings if f.get("severity") == "medium"]
                    ),
                    "low_severity": len(
                        [f for f in findings if f.get("severity") == "low"]
                    ),
                },
            }
        )

    except Exception as e:
        scan_result.update(
            {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now(UTC).isoformat(),
            }
        )


@router.get("/alerts")
@acached("security:alerts", ttl=60)
async def get_security_alerts(
    status: AlertStatus | None = None,
    threat_level: ThreatLevel | None = None,
    limit: int = Field(default=50, ge=1, le=500),
    user: User = Depends(require_roles(Role.ADMIN)),
):
    """Get security alerts with filtering"""
    await audit("security.alerts.list", actor=user.sub)

    alerts = list(active_alerts.values())

    # Apply filters
    if status:
        alerts = [alert for alert in alerts if alert.status == status]

    if threat_level:
        alerts = [alert for alert in alerts if alert.threat_level == threat_level]

    # Sort by creation time (newest first)
    alerts.sort(key=lambda x: x.created_at, reverse=True)

    # Limit results
    alerts = alerts[:limit]

    return {
        "alerts": [alert.to_dict() for alert in alerts],
        "total_count": len(active_alerts),
        "filtered_count": len(alerts),
    }


@router.get("/scans/{scan_id}")
@acached("security:scan", ttl=30)
async def get_scan_status(
    scan_id: str, user: User = Depends(require_roles(Role.ADMIN))
):
    """Get security scan status"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail=SCAN_NOT_FOUND)

    return scan_results[scan_id]


@router.put("/alerts/{alert_id}")
async def update_alert(
    alert_id: str,
    update_request: AlertUpdateRequest,
    user: User = Depends(require_roles(Role.ADMIN)),
):
    """Update security alert"""
    if alert_id not in active_alerts:
        raise HTTPException(status_code=404, detail=THREAT_NOT_FOUND)

    alert = active_alerts[alert_id]
    alert.status = update_request.status
    alert.updated_at = datetime.now(UTC)

    if update_request.assigned_to:
        alert.assigned_to = update_request.assigned_to

    await audit(
        "security.alert.update",
        actor=user.sub,
        payload={
            "alert_id": alert_id,
            "status": update_request.status,
            "assigned_to": update_request.assigned_to,
        },
    )

    return {"status": "updated", "alert": alert.to_dict()}


@router.post("/threat-intel/update")
async def update_threat_intelligence(
    intel_update: ThreatIntelUpdate, user: User = Depends(require_roles(Role.ADMIN))
):
    """Update threat intelligence indicators"""
    await audit(
        "security.threat_intel.update",
        actor=user.sub,
        payload={
            "source": intel_update.source,
            "indicator_count": len(intel_update.indicators),
        },
    )

    # Convert to ThreatIndicator objects
    indicators = []
    for ind_data in intel_update.indicators:
        indicator = ThreatIndicator(
            indicator_type=ind_data["type"],
            value=ind_data["value"],
            threat_level=ThreatLevel(ind_data.get("threat_level", "medium")),
            category=ThreatCategory(ind_data.get("category", "unknown")),
            description=ind_data.get("description", ""),
            confidence=ind_data.get("confidence", 0.5),
            first_seen=datetime.now(UTC),
            last_seen=datetime.now(UTC),
            source=intel_update.source,
        )
        indicators.append(indicator)

    # Add to threat intelligence
    threat_intel.add_indicators(indicators)

    return {
        "status": "updated",
        "indicators_added": len(indicators),
        "source": intel_update.source,
    }


@router.get("/analytics/dashboard")
async def get_security_dashboard(user: User = Depends(require_roles(Role.ADMIN))):
    """Get security analytics dashboard"""
    await audit("security.dashboard", actor=user.sub)

    # Calculate metrics
    len(security_events)
    total_alerts = len(active_alerts)
    open_alerts = len(
        [a for a in active_alerts.values() if a.status == AlertStatus.OPEN]
    )

    # Threat level distribution
    threat_distribution = defaultdict(int)
    for alert in active_alerts.values():
        threat_distribution[alert.threat_level.value] += 1

    # Category distribution
    category_distribution = defaultdict(int)
    for alert in active_alerts.values():
        category_distribution[alert.threat_category.value] += 1

    # Recent activity (last 24 hours)
    recent_events = [
        e
        for e in security_events
        if (datetime.now(UTC) - e.timestamp).total_seconds() <= 86400
    ]

    return {
        "summary": {
            "total_events_24h": len(recent_events),
            "total_alerts": total_alerts,
            "open_alerts": open_alerts,
            "threat_intelligence_indicators": len(threat_intel.indicators),
            "system_health": "healthy" if open_alerts < 10 else "attention_needed",
        },
        "threat_distribution": dict(threat_distribution),
        "category_distribution": dict(category_distribution),
        "recent_activity": {
            "events_per_hour": len(recent_events) / 24,
            "top_source_ips": list(set(e.source_ip for e in recent_events[-10:])),
            "anomaly_detection_status": "active"
            if anomaly_detector.is_trained
            else "training",
        },
    }
