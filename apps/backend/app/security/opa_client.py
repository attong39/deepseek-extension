"""
OPA Client for Zero-Trust Policy Evaluation
"""
from __future__ import annotations
import os
import logging
from typing import Dict, Any, Optional
import asyncio

import httpx
from prometheus_client import Counter, Histogram
import Exception
import bool
import client
import e
import input_data
import int
import list
import reason
import self
import str
import timeout
import url


logger = logging.getLogger(__name__)

# Configuration
OPA_URL = os.getenv("OPA_URL", "")  # e.g., http://localhost:8181/v1/data/zeta/zt
OPA_TIMEOUT = int(os.getenv("OPA_TIMEOUT", "5"))
OPA_ENABLED = os.getenv("ENABLE_OPA", "false").lower() == "true"

# Prometheus metrics
opa_requests_total = Counter(
    "zeta_opa_requests_total",
    "Total OPA policy evaluation requests",
    ["status"]
)

opa_request_duration = Histogram(
    "zeta_opa_request_duration_seconds",
    "OPA policy evaluation duration"
)

opa_policy_decisions = Counter(
    "zeta_opa_policy_decisions_total",
    "OPA policy decisions",
    ["allow", "risk"]
)


class OPAClient:
    """OPA Policy evaluation client"""
    
    def __init__(self, url: str, timeout: int = 5):
        self.url = url
        self.timeout = timeout
        self.enabled = bool(url) and OPA_ENABLED
        
        if self.enabled:
            logger.info(f"OPA Client configured for {url}")
        else:
            logger.info("OPA Client disabled (no URL or ENABLE_OPA=false)")
    
    async def evaluate_policy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate policy using OPA
        
        Args:
            input_data: Policy input data
            
        Returns:
            Policy decision with allow/risk/reasons
        """
        if not self.enabled:
            # Return permissive default when OPA is disabled
            return {
                "allow": True,
                "risk": "low",
                "reasons": ["opa_disabled"]
            }
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {"input": input_data}
                
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                
                result = response.json().get("result", {})
                
                # Normalize result structure
                decision = {
                    "allow": bool(result.get("allow", False)),
                    "risk": result.get("risk", "medium"),
                    "reasons": list(result.get("reasons", []))
                }
                
                # Record metrics
                opa_requests_total.labels(status="success").inc()
                opa_policy_decisions.labels(
                    allow=str(decision["allow"]).lower(),
                    risk=decision["risk"]
                ).inc()
                
                logger.debug(f"OPA decision: {decision}")
                return decision
                
        except httpx.TimeoutException:
            logger.error("OPA request timeout")
            opa_requests_total.labels(status="timeout").inc()
            return self._fallback_decision(input_data, "opa_timeout")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"OPA HTTP error: {e.response.status_code}")
            opa_requests_total.labels(status="http_error").inc()
            return self._fallback_decision(input_data, f"opa_http_{e.response.status_code}")
            
        except Exception as e:
            logger.error(f"OPA evaluation error: {e}")
            opa_requests_total.labels(status="error").inc()
            return self._fallback_decision(input_data, "opa_error")
        
        finally:
            # Record duration
            duration = asyncio.get_event_loop().time() - start_time
            opa_request_duration.observe(duration)
    
    def _fallback_decision(self, input_data: Dict[str, Any], reason: str) -> Dict[str, Any]:
        """
        Generate fallback decision when OPA is unavailable
        """
        # Conservative fallback - deny by default for safety
        subject = input_data.get("subject", {})
        resource = input_data.get("resource", {})
        action = input_data.get("action", "")
        
        # Allow admins and safe operations
        is_admin = "admin" in subject.get("roles", [])
        is_safe_operation = action in ["read"] and resource.get("classification") != "restricted"
        
        allow = is_admin or is_safe_operation
        risk = "low" if is_admin else "high"
        
        return {
            "allow": allow,
            "risk": risk,
            "reasons": [reason, "fallback_decision"]
        }
    
    async def health_check(self) -> bool:
        """Check if OPA is healthy"""
        if not self.enabled:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                # Use OPA health endpoint
                health_url = self.url.replace("/v1/data/", "/health")
                response = await client.get(health_url)
                return response.status_code == 200
        except Exception:
            return False


# Global OPA client instance
opa_client = OPAClient(OPA_URL, OPA_TIMEOUT) if OPA_URL else None


async def opa_decide(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate policy using global OPA client
    
    Args:
        payload: Policy input data
        
    Returns:
        Policy decision
    """
    if opa_client:
        return await opa_client.evaluate_policy(payload)
    
    # No OPA client configured - return permissive default
    return {
        "allow": True,
        "risk": "low",
        "reasons": ["no_opa_configured"]
    }


async def opa_health() -> Dict[str, Any]:
    """Get OPA health status"""
    if not opa_client:
        return {
            "enabled": False,
            "healthy": False,
            "url": None
        }
    
    healthy = await opa_client.health_check()
    
    return {
        "enabled": opa_client.enabled,
        "healthy": healthy,
        "url": opa_client.url
    }
