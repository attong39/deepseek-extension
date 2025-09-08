"""Enhanced FastAPI integration with metrics, security, and observability."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import asyncio
from datetime import datetime
import time
import logging

# Authentication system imports
from .factory import create_mfa_system
from .mfa_config import MFAConfig, DEFAULT_MFA_CONFIG
from .mfa_manager import MFAManager
from .metrics import AuthMetrics

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Enhanced Pydantic models for API
class SMSRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="User identifier")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number in E.164 format")

class SMSVerification(BaseModel):
    user_id: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=10, max_length=15)
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")
    device_token: Optional[str] = Field(None, description="Device token for trusted devices")
    device_fingerprint: Optional[str] = Field(None, description="Device fingerprint for trust")

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    base_url: str = Field(default="https://yourapp.com", description="Base URL for verification links")

class EmailVerificationCheck(BaseModel):
    email: EmailStr
    token: Optional[str] = Field(None, description="Verification token from email")
    code: Optional[str] = Field(None, description="Backup verification code")

class AuthResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class SecurityStatsResponse(BaseModel):
    timestamp: str
    failed_attempts_users: int
    total_failed_attempts: int
    device_trust: dict
    rate_limiting: dict
    security_features: dict

class MetricsResponse(BaseModel):
    authentication_operations: dict
    sms_operations: dict
    device_trust_events: dict
    rate_limit_hits: dict
    security_events: dict
    performance: dict

# Global auth system (in production, use dependency injection)
_auth_system = None
_auth_metrics = None
security = HTTPBearer(auto_error=False)

async def get_auth_system():
    """Enhanced dependency to get the authentication system with metrics."""
import Exception
import ValueError
import auth_system
import auth_token
import background_tasks
import bool
import call_next
import credentials
import device
import device_trust
import dict
import e
import email_manager
import exc
import int
import len
import request
import sms_manager
import str
import user_id
    global _auth_system, _auth_metrics
    if _auth_system is None:
        # Initialize with enhanced production-ready configuration
        config = MFAConfig(
            max_failed_attempts=5,
            rate_limit_window_seconds=900,  # 15 minutes
            device_trust_ttl_days=30,
            sms_code_ttl_minutes=5,
            max_sms_per_hour=3,
            max_sms_per_phone_per_day=10,
            email_verification_ttl_hours=24,
            log_security_events=True,
            enable_metrics=True,
            enable_tracing=True,
            hmac_secret_key="your-secret-key-here",  # In production, use secure key management
            secure_token_length=32,
            adaptive_rate_limiting=True,
            enable_dynamic_blocklist=True
        )
        
        # Use memory storage for demo (replace with Redis in production)
        mfa_manager, sms_manager, email_manager, device_trust, metrics = create_mfa_system(
            config, 
            "memory",
            enable_metrics=True,
            enable_tracing=True
        )
        _auth_system = (mfa_manager, sms_manager, email_manager, device_trust)
        _auth_metrics = metrics
    
    return _auth_system

async def get_metrics() -> AuthMetrics:
    """Get metrics instance."""
    if _auth_metrics is None:
        await get_auth_system()  # Initialize if needed
    return _auth_metrics

async def get_optional_auth(credentials: HTTPAuthorizationCredentials = Security(security)) -> Optional[str]:
    """Get optional authentication token."""
    if credentials:
        return credentials.credentials
    return None

# Enhanced FastAPI app
app = FastAPI(
    title="Enhanced Authentication API",
    description="Production-ready authentication with MFA, device trust, rate limiting, metrics, and security auditing",
    version="2.1.0"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Configure for your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Request timing middleware for metrics
@app.middleware("http")
async def add_request_timing(request: Request, call_next):
    """Add request timing and basic metrics."""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    # Record metrics if available
    if _auth_metrics:
        _auth_metrics.record_request_duration(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
            duration=process_time
        )
    
    return response

@app.on_event("startup")
async def startup_event():
    """Initialize enhanced authentication system and start background tasks."""
    mfa_manager, _, _, _ = await get_auth_system()
    
    # Start background cleanup task
    async def cleanup_task():
        while True:
            try:
                await mfa_manager.cleanup_expired_data()
                log.info("Cleanup task completed successfully")
            except Exception as e:
                log.error(f"Cleanup task failed: {e}")
            await asyncio.sleep(3600)  # Every hour
    
    # Start metrics reporting task
    async def metrics_task():
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            try:
                if _auth_metrics and mfa_manager:
                    stats = mfa_manager.get_security_stats()
                    _auth_metrics.set_active_devices(stats["device_trust"]["active_devices"])
                    _auth_metrics.set_failed_attempts_current(stats["failed_attempts_users"])
                    log.info(f"Metrics updated - Active devices: {stats['device_trust']['active_devices']}")
            except Exception as e:
                log.error(f"Metrics task failed: {e}")
    
    asyncio.create_task(cleanup_task())
    asyncio.create_task(metrics_task())
    log.info("Enhanced authentication system and background tasks initialized")

# Enhanced SMS Authentication Endpoints
@app.post("/auth/sms/send", response_model=AuthResponse)
async def send_sms_code(
    request: SMSRequest,
    auth_system=Depends(get_auth_system)
):
    """Send SMS verification code with enhanced rate limiting."""
    mfa_manager, _, _, _ = auth_system
    
    try:
        success = await mfa_manager.send_sms_code(request.user_id, request.phone)
        
        if success:
            return AuthResponse(
                success=True,
                message="SMS code sent successfully",
                data={
                    "phone": request.phone[:3] + "***" + request.phone[-2:] if len(request.phone) > 5 else "***",
                    "user_id": request.user_id
                }
            )
        else:
            raise HTTPException(
                status_code=429,
                detail="SMS sending rate limit exceeded or service unavailable"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"SMS sending error: {e}")
        if _auth_metrics:
            _auth_metrics.increment_security_event("sms_send_error", "medium")
        raise HTTPException(status_code=500, detail="Failed to send SMS")

@app.post("/auth/sms/verify", response_model=AuthResponse)
async def verify_sms_code(
    request: SMSVerification,
    auth_system=Depends(get_auth_system)
):
    """Verify SMS code with enhanced device trust and security."""
    mfa_manager, _, _, _ = auth_system
    
    try:
        success = await mfa_manager.verify_mfa(
            request.user_id,
            request.phone,
            request.code,
            request.device_token,
            request.device_fingerprint
        )
        
        if success:
            # If device fingerprint provided and no existing token, create device trust
            device_token = request.device_token
            if request.device_fingerprint and not device_token:
                device_token = mfa_manager.trust.trust_device(request.device_fingerprint)
            
            return AuthResponse(
                success=True,
                message="SMS code verified successfully",
                data={
                    "user_id": request.user_id,
                    "device_trusted": bool(device_token and request.device_fingerprint),
                    "device_token": device_token
                }
            )
        else:
            # Check if rate limited
            attempts = await mfa_manager.get_failed_attempts(request.user_id)
            max_attempts = mfa_manager.config.max_failed_attempts
            
            if attempts >= max_attempts:
                raise HTTPException(
                    status_code=429,
                    detail="Too many failed attempts. Please try again later."
                )
            
            return AuthResponse(
                success=False,
                message="Invalid or expired SMS code",
                data={
                    "attempts_remaining": max_attempts - attempts,
                    "user_id": request.user_id
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"SMS verification error: {e}")
        if _auth_metrics:
            _auth_metrics.increment_security_event("sms_verify_error", "medium")
        raise HTTPException(status_code=500, detail="Verification failed")

# Enhanced Email Verification Endpoints
@app.post("/auth/email/send", response_model=AuthResponse)
async def send_email_verification(
    request: EmailVerificationRequest,
    auth_system=Depends(get_auth_system)
):
    """Send email verification link and backup code with enhanced logging."""
    _, _, email_manager, _ = auth_system
    
    try:
        token = await email_manager.send_verification(request.email, request.base_url)
        
        if _auth_metrics:
            _auth_metrics.increment_security_event("email_verification_sent", "low")
        
        return AuthResponse(
            success=True,
            message="Verification email sent successfully",
            data={
                "email": request.email,
                "token_preview": token[:8] + "..." if token else None
            }
        )
    
    except Exception as e:
        log.error(f"Email sending error: {e}")
        if _auth_metrics:
            _auth_metrics.increment_security_event("email_send_error", "medium")
        raise HTTPException(status_code=500, detail="Failed to send verification email")

@app.post("/auth/email/verify", response_model=AuthResponse)
async def verify_email(
    request: EmailVerificationCheck,
    auth_system=Depends(get_auth_system)
):
    """Verify email using either token or backup code with enhanced security."""
    _, _, email_manager, _ = auth_system
    
    if not request.token and not request.code:
        raise HTTPException(
            status_code=400,
            detail="Either token or code must be provided"
        )
    
    try:
        if request.token:
            success = await email_manager.verify_token(request.email, request.token)
            method = "token"
        else:
            success = await email_manager.verify_code(request.email, request.code)
            method = "code"
        
        if success:
            if _auth_metrics:
                _auth_metrics.increment_security_event("email_verification_success", "low")
            
            return AuthResponse(
                success=True,
                message=f"Email verified successfully using {method}",
                data={"email": request.email, "method": method}
            )
        else:
            if _auth_metrics:
                _auth_metrics.increment_security_event("email_verification_failed", "low")
                
            return AuthResponse(
                success=False,
                message="Invalid or expired verification",
                data={"method": method}
            )
    
    except Exception as e:
        log.error(f"Email verification error: {e}")
        if _auth_metrics:
            _auth_metrics.increment_security_event("email_verify_error", "medium")
        raise HTTPException(status_code=500, detail="Email verification failed")

# Enhanced Device Trust Management
@app.get("/auth/devices/{user_id}", response_model=AuthResponse)
async def get_user_devices(
    user_id: str,
    auth_system=Depends(get_auth_system),
    auth_token: Optional[str] = Depends(get_optional_auth)
):
    """Get list of trusted devices for user (admin endpoint)."""
    _, _, _, device_trust = auth_system
    
    devices = device_trust.list_devices()
    # In production, filter by user_id and verify admin permissions
    
    return AuthResponse(
        success=True,
        message="Devices retrieved successfully",
        data={
            "user_id": user_id,
            "device_count": len(devices),
            "devices": [
                {
                    "token": device.device_token[:8] + "...",
                    "fingerprint": device.device_fingerprint[:16] + "...",
                    "expires_at": device.expires_at.isoformat(),
                    "last_seen": device.last_seen.isoformat(),
                    "created_at": device.created_at.isoformat()
                }
                for device in devices
            ]
        }
    )

@app.delete("/auth/devices/{device_token}", response_model=AuthResponse)
async def revoke_device(
    device_token: str,
    auth_system=Depends(get_auth_system),
    auth_token: Optional[str] = Depends(get_optional_auth)
):
    """Revoke trust for a specific device with audit logging."""
    mfa_manager, _, _, _ = auth_system
    
    success = mfa_manager.revoke_device_trust(device_token)
    
    if success:
        return AuthResponse(
            success=True,
            message="Device trust revoked successfully",
            data={"device_token": device_token[:8] + "..."}
        )
    else:
        raise HTTPException(
            status_code=404,
            detail="Device not found or already revoked"
        )

@app.post("/auth/devices/revoke-all", response_model=AuthResponse)
async def revoke_all_devices(
    auth_system=Depends(get_auth_system),
    auth_token: Optional[str] = Depends(get_optional_auth)  # In production, require admin auth
):
    """Emergency revoke all devices (admin only)."""
    mfa_manager, _, _, _ = auth_system
    
    # In production, verify admin permissions here
    count = mfa_manager.revoke_all_devices()
    
    return AuthResponse(
        success=True,
        message=f"Emergency revocation completed - {count} devices revoked",
        data={
            "devices_revoked": count,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Enhanced Monitoring and Statistics
@app.get("/auth/security/stats", response_model=SecurityStatsResponse)
async def get_security_stats(
    auth_system=Depends(get_auth_system),
    auth_token: Optional[str] = Depends(get_optional_auth)  # In production, require admin auth
):
    """Get comprehensive security statistics (admin only)."""
    mfa_manager, _, _, _ = auth_system
    
    # In production, verify admin permissions here
    stats = mfa_manager.get_security_stats()
    return SecurityStatsResponse(**stats)

@app.get("/auth/metrics", response_model=MetricsResponse)
async def get_metrics_data(
    metrics: AuthMetrics = Depends(get_metrics),
    auth_token: Optional[str] = Depends(get_optional_auth)  # In production, require admin auth
):
    """Get metrics data (admin only)."""
    # In production, verify admin permissions here
    try:
        metrics_data = metrics.get_all_metrics()
        return MetricsResponse(**metrics_data)
    except Exception as e:
        log.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Metrics temporarily unavailable")

@app.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics(
    metrics: AuthMetrics = Depends(get_metrics)
) -> str:
    """Prometheus metrics endpoint."""
    try:
        return metrics.get_prometheus_metrics()
    except Exception as e:
        log.error(f"Error getting Prometheus metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Metrics temporarily unavailable"
        )

# Enhanced Health and Status Endpoints
@app.get("/auth/health", response_model=AuthResponse)
async def health_check(auth_system=Depends(get_auth_system)):
    """Enhanced health check endpoint."""
    mfa_manager, _, _, device_trust = auth_system
    
    return AuthResponse(
        success=True,
        message="Enhanced authentication system healthy",
        data={
            "version": "2.1.0",
            "config": {
                "max_failed_attempts": mfa_manager.config.max_failed_attempts,
                "rate_limit_window": mfa_manager.config.rate_limit_window_seconds,
                "sms_ttl_minutes": mfa_manager.config.sms_code_ttl_minutes,
                "email_ttl_hours": mfa_manager.config.email_verification_ttl_hours,
                "adaptive_rate_limiting": mfa_manager.config.adaptive_rate_limiting
            },
            "stats": {
                "trusted_devices": len(device_trust.list_devices()),
                "timestamp": datetime.utcnow().isoformat()
            },
            "features": {
                "device_trust": True,
                "rate_limiting": True,
                "metrics": True,
                "security_auditing": True,
                "hmac_fingerprints": True,
                "adaptive_limits": mfa_manager.config.adaptive_rate_limiting
            }
        }
    )

@app.get("/auth/health/detailed", response_model=AuthResponse)
async def detailed_health_check(auth_system=Depends(get_auth_system)):
    """Detailed health check with comprehensive system status."""
    mfa_manager, _, _, _ = auth_system
    
    try:
        stats = mfa_manager.get_security_stats()
        
        return AuthResponse(
            success=True,
            message="Detailed system health check passed",
            data={
                "system_status": "healthy",
                "security_stats": stats,
                "performance": {
                    "metrics_enabled": bool(_auth_metrics),
                    "tracing_enabled": mfa_manager.config.enable_tracing
                }
            }
        )
    except Exception as e:
        log.error(f"Detailed health check failed: {e}")
        return AuthResponse(
            success=False,
            message="System health check degraded",
            data={
                "system_status": "degraded",
                "error": str(e)
            }
        )

@app.post("/auth/cleanup", response_model=AuthResponse)
async def manual_cleanup(
    background_tasks: BackgroundTasks,
    auth_system=Depends(get_auth_system),
    auth_token: Optional[str] = Depends(get_optional_auth)
):
    """Manually trigger cleanup of expired data with audit logging."""
    mfa_manager, _, _, _ = auth_system
    
    # In production, verify admin permissions here
    
    async def cleanup_with_logging():
        try:
            await mfa_manager.cleanup_expired_data()
            if _auth_metrics:
                _auth_metrics.increment_security_event("manual_cleanup_success", "low")
        except Exception as e:
            log.error(f"Manual cleanup failed: {e}")
            if _auth_metrics:
                _auth_metrics.increment_security_event("manual_cleanup_failed", "medium")
    
    # Run cleanup in background
    background_tasks.add_task(cleanup_with_logging)
    
    return AuthResponse(
        success=True,
        message="Enhanced cleanup task scheduled",
        data={
            "scheduled_at": datetime.utcnow().isoformat(),
            "admin_initiated": bool(auth_token)
        }
    )

# Enhanced Error handlers with metrics
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    if _auth_metrics:
        _auth_metrics.increment_security_event("validation_error", "low")
    return HTTPException(
        status_code=400,
        detail=str(exc)
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler with enhanced security logging and metrics."""
    
    logger = logging.getLogger("auth_api")
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    if _auth_metrics:
        _auth_metrics.increment_security_event("unhandled_exception", "high")
    
    return {
        "success": False,
        "message": "Internal server error",
        "data": {
            "error_id": datetime.utcnow().isoformat(),
            "request_path": str(request.url.path)
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Configure enhanced logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the enhanced app
    uvicorn.run(
        "fastapi_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
