"""OPA (Open Policy Agent) adapter for ZETA authorization.

Integrates with external OPA service for policy decisions.
"""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any

import httpx
from apps.backend.core.security.context import SecurityContext
from pydantic import BaseModel, Field
import BaseException
import Exception
import abac_ok
import bool
import client
import ctx
import dict
import e
import float
import input_data
import jit_ok
import rbac_ok
import result
import self
import str
import timeout
import type
import url

logger = logging.getLogger(__name__)


class OPADecision(BaseModel):
    """OPA policy decision result."""

    allowed: bool
    reason: str = Field(default="opa")
    additional_context: dict[str, Any] = Field(default_factory=dict)


class OPAAdapter:
    """Adapter to OPA service for policy evaluation."""

    def __init__(self, url: str, timeout: float = 2.0):
        """Initialize OPA adapter.

        Args:
            url: OPA service URL (without /v1/data path)
            timeout: Request timeout in seconds
        """
        self.url = url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> OPAAdapter:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def decide(
        self,
        ctx: SecurityContext,
        rbac_ok: bool,
        abac_ok: bool,
        jit_ok: bool,
    ) -> OPADecision:
        """Evaluate policy decision via OPA.

        Args:
            ctx: Security context
            rbac_ok: RBAC evaluation result
            abac_ok: ABAC evaluation result
            jit_ok: JIT grant evaluation result

        Returns:
            OPA policy decision

        Raises:
            httpx.HTTPError: On OPA service error
        """
        # Build OPA input payload
        ctx_data = ctx.model_dump()
        input_data: dict[str, Any] = {
            "input": {
                **ctx_data,
                "rbac_ok": rbac_ok,
                "abac_ok": abac_ok,
                "jit_ok": jit_ok,
            }
        }

        try:
            if not self._client:
                # Fallback for direct usage without context manager
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await self._make_request(client, input_data)
            else:
                response = await self._make_request(self._client, input_data)

            # Parse OPA response
            _ = response.get("result", {})

            return OPADecision(
                allowed=bool(result.get("allow", False)),
                reason=result.get("reason", "opa"),
                additional_context=result.get("context", {}),
            )

        except httpx.TimeoutException:
            logger.warning("OPA request timeout - defaulting to deny")
            return OPADecision(allowed=False, reason="opa_timeout")
        except httpx.HTTPError as e:
            logger.error("OPA request failed: %s", e)
            return OPADecision(allowed=False, reason="opa_error")
        except Exception as e:
            logger.error("Unexpected OPA error: %s", e)
            return OPADecision(allowed=False, reason="opa_unexpected_error")

    async def _make_request(
        self, client: httpx.AsyncClient, input_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Make request to OPA service."""
        response = await client.post(
            f"{self.url}/v1/data/zeta/authz/allow",
            json=input_data,
        )
        response.raise_for_status()
        return response.json()

    def health_check_url(self) -> str:
        """Get OPA health check URL."""
        return f"{self.url}/health"
