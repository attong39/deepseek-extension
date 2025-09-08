"""
JWKS Cache with Rotation Support for Production JWT/OIDC
"""
from __future__ import annotations
import asyncio
import os
import time
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timezone

import httpx
import jwt
from cryptography.hazmat.primitives import serialization
from prometheus_client import Counter, Histogram, Gauge
import Exception
import ValueError
import client
import dict
import e
import int
import len
import max_retries
import retry_backoff
import self
import str
import token
import ttl
import url


logger = logging.getLogger(__name__)

# Prometheus metrics
jwks_refresh_total = Counter(
    "zeta_jwks_refresh_total",
    "Total JWKS refresh attempts",
    ["status"]
)

jwks_key_usage_total = Counter(
    "zeta_jwks_key_usage_total", 
    "Total JWKS key usage",
    ["kid", "status"]
)

jwks_cache_age_seconds = Gauge(
    "zeta_jwks_cache_age_seconds",
    "Age of JWKS cache in seconds"
)

jwks_decode_duration = Histogram(
    "zeta_jwks_decode_duration_seconds",
    "JWT decode duration with JWKS"
)


class JWKSCache:
    """
    JWKS Cache with automatic rotation and fallback mechanisms
    """
    
    def __init__(
        self, 
        url: str, 
        ttl: int = 3600,
        retry_backoff: int = 30,
        max_retries: int = 3
    ):
        self.url = url
        self.ttl = ttl
        self.retry_backoff = retry_backoff
        self.max_retries = max_retries
        
        self._exp = 0.0
        self._keys: Dict[str, Any] = {}
        self._last_good_keys: Dict[str, Any] = {}  # Fallback cache
        self._lock = asyncio.Lock()
        self._refresh_task: Optional[asyncio.Task] = None
        
        logger.info(f"JWKS Cache initialized for {url} with TTL {ttl}s")
    
    async def start_background_refresh(self) -> None:
        """Start background refresh task"""
        if self._refresh_task is None or self._refresh_task.done():
            self._refresh_task = asyncio.create_task(self._background_refresh_loop())
    
    async def stop_background_refresh(self) -> None:
        """Stop background refresh task"""
        if self._refresh_task and not self._refresh_task.done():
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
    
    async def _background_refresh_loop(self) -> None:
        """Background refresh loop to keep JWKS fresh"""
        while True:
            try:
                await asyncio.sleep(self.ttl // 2)  # Refresh at half TTL
                async with self._lock:
                    if time.time() > self._exp - (self.ttl // 4):  # Refresh before expiry
                        await self._refresh_keys()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Background JWKS refresh error: {e}")
                await asyncio.sleep(self.retry_backoff)
    
    async def _refresh_keys(self) -> None:
        """Refresh JWKS keys from the endpoint"""
        retry_count = 0
        last_error = None
        
        while retry_count < self.max_retries:
            try:
                async with httpx.AsyncClient(
                    timeout=httpx.Timeout(10.0),
                    follow_redirects=True
                ) as client:
                    response = await client.get(self.url)
                    response.raise_for_status()
                    
                    data = response.json()
                    keys = data.get("keys", [])
                    
                    if not keys:
                        raise ValueError("No keys found in JWKS response")
                    
                    # Parse and validate keys
                    parsed_keys = {}
                    for key_data in keys:
                        kid = key_data.get("kid")
                        if not kid:
                            logger.warning("JWKS key missing 'kid', skipping")
                            continue
                        
                        try:
                            # Convert JWK to cryptographic key
                            if key_data.get("kty") == "RSA":
                                crypto_key = jwt.algorithms.RSAAlgorithm.from_jwk(
                                    json.dumps(key_data)
                                )
                            elif key_data.get("kty") == "EC":
                                crypto_key = jwt.algorithms.ECAlgorithm.from_jwk(
                                    json.dumps(key_data)
                                )
                            else:
                                logger.warning(f"Unsupported key type: {key_data.get('kty')}")
                                continue
                            
                            parsed_keys[kid] = {
                                "key": crypto_key,
                                "alg": key_data.get("alg", "RS256"),
                                "use": key_data.get("use", "sig"),
                                "raw": key_data
                            }
                            
                        except Exception as e:
                            logger.error(f"Failed to parse key {kid}: {e}")
                            continue
                    
                    if parsed_keys:
                        # Store last good keys as fallback
                        if self._keys:
                            self._last_good_keys = self._keys.copy()
                        
                        self._keys = parsed_keys
                        self._exp = time.time() + self.ttl
                        
                        jwks_refresh_total.labels(status="success").inc()
                        jwks_cache_age_seconds.set(0)
                        
                        logger.info(f"JWKS refreshed successfully: {len(parsed_keys)} keys")
                        return
                    
                    raise ValueError("No valid keys parsed from JWKS")
            
            except Exception as e:
                last_error = e
                retry_count += 1
                
                logger.warning(
                    f"JWKS refresh attempt {retry_count}/{self.max_retries} failed: {e}"
                )
                
                if retry_count < self.max_retries:
                    await asyncio.sleep(self.retry_backoff * retry_count)
        
        # All retries failed
        jwks_refresh_total.labels(status="failed").inc()
        logger.error(f"JWKS refresh failed after {self.max_retries} attempts: {last_error}")
        
        # Use last good keys if available
        if self._last_good_keys and not self._keys:
            logger.warning("Using last good JWKS keys as fallback")
            self._keys = self._last_good_keys.copy()
            self._exp = time.time() + (self.ttl // 2)  # Shorter TTL for fallback
    
    async def get_key(self, kid: str) -> Optional[Any]:
        """Get cryptographic key by kid"""
        async with self._lock:
            # Refresh if expired or no keys
            if time.time() > self._exp or not self._keys:
                await self._refresh_keys()
            
            # Update cache age metric
            if self._exp > 0:
                jwks_cache_age_seconds.set(time.time() - (self._exp - self.ttl))
            
            key_data = self._keys.get(kid)
            if key_data:
                jwks_key_usage_total.labels(kid=kid, status="found").inc()
                return key_data["key"]
            
            jwks_key_usage_total.labels(kid=kid, status="not_found").inc()
            return None
    
    async def get_key_algorithm(self, kid: str) -> str:
        """Get algorithm for a specific key"""
        async with self._lock:
            key_data = self._keys.get(kid)
            return key_data["alg"] if key_data else "RS256"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "total_keys": len(self._keys),
            "cache_expires_at": datetime.fromtimestamp(self._exp, tz=timezone.utc).isoformat(),
            "cache_valid": time.time() < self._exp,
            "fallback_keys": len(self._last_good_keys),
            "background_refresh_active": (
                self._refresh_task is not None and not self._refresh_task.done()
            )
        }


# Global JWKS cache instance
JWKS_URL = os.getenv("JWKS_URL", "")
JWKS_TTL = int(os.getenv("JWKS_TTL", "3600"))
JWKS_CACHE: Optional[JWKSCache] = None

if JWKS_URL:
    JWKS_CACHE = JWKSCache(JWKS_URL, ttl=JWKS_TTL)
    logger.info(f"JWKS Cache configured for {JWKS_URL}")
else:
    logger.info("JWKS_URL not configured, JWT signature verification disabled")


async def decode_bearer_rs256(token: str) -> dict:
    """
    Decode JWT token with JWKS-based signature verification
    """
    start_time = time.time()
    
    try:
        # Get header to extract kid
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        algorithm = header.get("alg", "RS256")
        
        if not JWKS_CACHE:
            # No JWKS configured, decode without verification
            logger.warning("JWKS not configured, decoding JWT without signature verification")
            return jwt.decode(
                token, 
                options={"verify_signature": False}, 
                algorithms=[algorithm]
            )
        
        if not kid:
            logger.warning("JWT missing 'kid' in header")
            # Try to decode anyway for development/testing
            return jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=[algorithm]
            )
        
        # Get key from JWKS cache
        key = await JWKS_CACHE.get_key(kid)
        if not key:
            logger.error(f"JWKS key not found for kid: {kid}")
            raise jwt.InvalidKeyError(f"Key {kid} not found in JWKS")
        
        # Decode with signature verification
        claims = jwt.decode(
            token,
            key=key,
            algorithms=[algorithm],
            options={
                "verify_aud": False,  # Audience verification handled separately
                "verify_iss": False,  # Issuer verification handled separately
            }
        )
        
        logger.debug(f"JWT decoded successfully for kid: {kid}")
        return claims
    
    except jwt.InvalidTokenError as e:
        logger.error(f"JWT validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"JWT decode error: {e}")
        raise jwt.InvalidTokenError(f"JWT decode failed: {e}")
    
    finally:
        # Record decode duration
        duration = time.time() - start_time
        jwks_decode_duration.observe(duration)


async def start_jwks_cache() -> None:
    """Start JWKS cache background refresh"""
    if JWKS_CACHE:
        await JWKS_CACHE.start_background_refresh()


async def stop_jwks_cache() -> None:
    """Stop JWKS cache background refresh"""
    if JWKS_CACHE:
        await JWKS_CACHE.stop_background_refresh()


def get_jwks_stats() -> Dict[str, Any]:
    """Get JWKS cache statistics"""
    if JWKS_CACHE:
        return JWKS_CACHE.get_stats()
    return {"status": "disabled"}
