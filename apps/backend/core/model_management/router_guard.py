"""
Guard phân quyền cho Model Router.

Tích hợp với permission_manager để kiểm soát:
- Quyền gọi router
- JIT override cho external models khi sensitivity=high
- Budget gates
"""

from __future__ import annotations

from typing import Any

from apps.backend.core.model_management.router import ModelRequest, ModelRouter
from apps.backend.core.security.context import (
import Exception
import ValueError
import dict
import float
import ip
import req
import self
import str
import subject
import ua
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from apps.backend.core.security.permission_manager import permission_manager


class GuardedModelRouter(ModelRouter):
    """Model Router với tích hợp bảo mật và phân quyền"""

    def select_model_guarded(
        self, req: ModelRequest, subject: Subject, ip: str, ua: str
    ) -> str:
        """
        Chọn model với kiểm tra phân quyền.

        Args:
            req: Model request
            subject: Đối tượng yêu cầu (user/service)
            ip: IP address
            ua: User agent

        Returns:
            Model ID được chọn

        Raises:
            PermissionError: Nếu không có quyền
            ValueError: Nếu vượt ngân sách
        """
        # 1) Quyền gọi router
        context = SecurityContext(
            subject=subject,
            resource=Resource(
                type="router",
                id="default",
                owner_id=subject.user_id,
                tenant_id=subject.tenant_id,
                sensitivity="internal",
            ),
            action=Action(
                name="router:select",
                risk="low",
                requires_mfa=False,
                rate_limit_key=None,
            ),
            environment=Environment(
                ip=ip,
                user_agent=ua,
                device_trust="medium",
                time_of_day=None,
                location=None,
                is_vpn=False,
                request_id=None,
            ),
        )
        permission_manager.ensure(context, "router:select")

        model_id = self.select_model(req)
        chosen = self.models[model_id]
        sens = req.data_sensitivity
        is_external = not chosen.get("self_hosted", False)

        # 2) High sensitivity → nếu external, yêu cầu JIT (hoặc role override)
        if sens == "high" and is_external:
            sensitive_context = SecurityContext(
                subject=subject,
                resource=Resource(
                    type="router",
                    id=model_id,
                    owner_id=subject.user_id,
                    tenant_id=subject.tenant_id,
                    sensitivity="secret",
                ),
                action=Action(
                    name="router:policy:update",
                    risk="high",
                    requires_mfa=True,
                    rate_limit_key=None,
                ),
                environment=Environment(
                    ip=ip,
                    user_agent=ua,
                    device_trust="high",
                    time_of_day=None,
                    location=None,
                    is_vpn=False,
                    request_id=None,
                ),
            )
            permission_manager.ensure(sensitive_context, "router:policy:update")

        # 3) Budget gate (deny sớm nếu quá ngưỡng)
        if req.budget_constraint is not None:
            cost = float(chosen["cost_per_1k"])
            if cost > req.budget_constraint:
                raise ValueError(f"Budget exceeded: {cost} > {req.budget_constraint}")

        return model_id

    def select_model_safe(
        self,
        req: ModelRequest,
        subject: Subject | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        """
        Safe wrapper cho select_model với fallback.

        Args:
            req: Model request
            subject: Đối tượng yêu cầu (optional)
            context: Context thêm (ip, ua, etc.)

        Returns:
            Model ID được chọn
        """
        if subject is None or context is None:
            # Fallback không guard nếu thiếu context
            return self.select_model(req)

        try:
            return self.select_model_guarded(
                req,
                subject,
                ip=context.get("ip", "127.0.0.1"),
                ua=context.get("user_agent", "unknown"),
            )
        except Exception:
            # Fallback về model an toàn nhất
            safe_req = ModelRequest(
                task_type=req.task_type,
                data_sensitivity="high",  # Force self-hosted
                budget_constraint=0.1,  # Force cheap
            )
            return self.select_model(safe_req)
