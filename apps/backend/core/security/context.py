"""Security context models cho hệ thống phân quyền ZETA.

Module này định nghĩa các context model cho việc đánh giá quyền hạn:
- Subject: thông tin người/hệ thống thực hiện hành động
- Resource: tài nguyên bị tác động
- Action: hành động cần kiểm tra quyền
- Environment: ngữ cảnh môi trường thực hiện
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field
import bool
import dict
import int
import list
import self
import str

# Type aliases cho tính rõ ràng
Risk = Literal["low", "medium", "high", "critical"]
Sensitivity = Literal["public", "internal", "restricted", "secret"]
DeviceTrust = Literal["low", "medium", "high"]


class Subject(BaseModel):
    """Đối tượng thực hiện hành động (người dùng hoặc service).

    Attributes:
        user_id: ID người dùng duy nhất
        tenant_id: ID tenant/organization (None cho single-tenant)
        roles: danh sách vai trò của user
        mfa_level: mức độ xác thực đa yếu tố (0=không, 1=SMS, 2=TOTP, 3=hardware)
        permissions: quyền hạn cụ thể được gán trực tiếp (JIT grants)
        session_id: ID phiên làm việc hiện tại
        last_activity: thời điểm hoạt động cuối cùng
    """

    user_id: str = Field(..., description="ID người dùng duy nhất")
    tenant_id: str | None = Field(None, description="ID tenant/organization")
    roles: list[str] = Field(default_factory=list, description="Danh sách vai trò")
    mfa_level: int = Field(0, ge=0, le=3, description="Mức độ MFA (0-3)")
    permissions: list[str] = Field(default_factory=list, description="Quyền trực tiếp")
    session_id: str | None = Field(None, description="ID phiên làm việc")
    last_activity: datetime | None = Field(None, description="Hoạt động cuối")

    class Config:
        frozen = True  # Immutable để đảm bảo tính nhất quán


class Resource(BaseModel):
    """Tài nguyên bị tác động bởi hành động.

    Attributes:
        type: loại tài nguyên (file, agent, memory, training, etc.)
        id: ID cụ thể của tài nguyên (None cho hành động tổng quát)
        owner_id: ID chủ sở hữu tài nguyên
        tenant_id: ID tenant chứa tài nguyên
        sensitivity: mức độ nhạy cảm của dữ liệu
        metadata: thông tin bổ sung theo từng loại resource
    """

    type: str = Field(..., description="Loại tài nguyên")
    id: str | None = Field(None, description="ID cụ thể của tài nguyên")
    owner_id: str | None = Field(None, description="ID chủ sở hữu")
    tenant_id: str | None = Field(None, description="ID tenant")
    sensitivity: Sensitivity = Field("internal", description="Mức độ nhạy cảm")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata bổ sung"
    )

    class Config:
        frozen = True


class Action(BaseModel):
    """Hành động cần kiểm tra quyền.

    Attributes:
        name: tên hành động theo format domain:action (vd: files:delete)
        risk: mức độ rủi ro của hành động
        requires_mfa: có yêu cầu MFA không
        rate_limit_key: key để áp dụng rate limiting
        context: ngữ cảnh bổ sung cho hành động
    """

    name: str = Field(..., description="Tên hành động (domain:action)")
    risk: Risk = Field("low", description="Mức độ rủi ro")
    requires_mfa: bool = Field(False, description="Yêu cầu MFA")
    rate_limit_key: str | None = Field(None, description="Key cho rate limiting")
    context: dict[str, Any] = Field(default_factory=dict, description="Ngữ cảnh")

    class Config:
        frozen = True


class Environment(BaseModel):
    """Ngữ cảnh môi trường thực hiện hành động.

    Attributes:
        ip: địa chỉ IP người dùng
        user_agent: thông tin trình duyệt/client
        time_of_day: giờ trong ngày (0-23)
        device_trust: mức độ tin cậy thiết bị
        location: vị trí địa lý (tùy chọn)
        is_vpn: có đang dùng VPN không
        request_id: ID request để tracing
    """

    ip: str | None = Field(None, description="Địa chỉ IP")
    user_agent: str | None = Field(None, description="User agent")
    time_of_day: int | None = Field(None, ge=0, le=23, description="Giờ trong ngày")
    device_trust: DeviceTrust = Field("medium", description="Mức tin cậy thiết bị")
    location: str | None = Field(None, description="Vị trí địa lý")
    is_vpn: bool = Field(False, description="Có dùng VPN")
    request_id: str | None = Field(None, description="ID request")

    class Config:
        frozen = True


class SecurityContext(BaseModel):
    """Context hoàn chỉnh cho việc đánh giá quyền hạn.

    Đây là context chính được truyền vào PolicyEngine để đưa ra quyết định.

    Attributes:
        subject: đối tượng thực hiện hành động
        resource: tài nguyên bị tác động
        action: hành động cần kiểm tra
        environment: ngữ cảnh môi trường
        timestamp: thời điểm đánh giá
    """

    subject: Subject = Field(..., description="Đối tượng thực hiện")
    resource: Resource = Field(..., description="Tài nguyên")
    action: Action = Field(..., description="Hành động")
    environment: Environment = Field(..., description="Môi trường")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Thời điểm"
    )

    class Config:
        frozen = True

    def to_audit_dict(self) -> dict[str, Any]:
        """Chuyển đổi context thành dict để ghi audit log.

        Returns:
            Dictionary chứa thông tin audit
        """
        return {
            "user_id": self.subject.user_id,
            "tenant_id": self.subject.tenant_id,
            "roles": self.subject.roles,
            "resource_type": self.resource.type,
            "resource_id": self.resource.id,
            "action": self.action.name,
            "risk": self.action.risk,
            "ip": self.environment.ip,
            "user_agent": self.environment.user_agent,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.environment.request_id,
        }
