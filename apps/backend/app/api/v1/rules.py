"""
Rules API - Quản lý nguyên tắc AI rules
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.api.v1._schemas import RuleResp, RuleUpsert
from fastapi import APIRouter, HTTPException
import RULES
import active_only
import body
import bool
import category
import dict
import list
import r
import str

router = APIRouter(prefix="/v1/rules", tags=["rules"])

# In-memory storage cho demo
RULES: dict[str, RuleResp] = {}


@router.post("", response_model=RuleResp)
async def create_rule(body: RuleUpsert) -> RuleResp:
    """Tạo nguyên tắc AI mới"""
    rule_id = f"r_{uuid.uuid4().hex[:12]}"

    rule = RuleResp(
        id=rule_id,
        text=body.text,
        category=body.category,
        priority=body.priority,
        created_at=datetime.now(UTC),
        is_active=True,
    )

    RULES[rule_id] = rule
    return rule


@router.get("", response_model=list[RuleResp])
async def list_rules(
    category: str | None = None, active_only: bool = True
) -> list[RuleResp]:
    """Lấy danh sách nguyên tắc"""
    rules = list(RULES.values())

    # Filter by category
    if category:
        rules = [r for r in rules if r.category == category]

    # Filter by active status
    if active_only:
        rules = [r for r in rules if r.is_active]

    # Sort by priority (higher first), then by created_at
    rules.sort(key=lambda r: (-r.priority, r.created_at), reverse=False)

    return rules


@router.get("/{rule_id}", response_model=RuleResp)
async def get_rule(rule_id: str) -> RuleResp:
    """Lấy nguyên tắc theo ID"""
    rule = RULES.get(rule_id)
    if not rule:
        raise HTTPException(404, f"Rule {rule_id} không tồn tại")
    return rule


@router.put("/{rule_id}", response_model=RuleResp)
async def update_rule(rule_id: str, body: RuleUpsert) -> RuleResp:
    """Cập nhật nguyên tắc"""
    rule = RULES.get(rule_id)
    if not rule:
        raise HTTPException(404, f"Rule {rule_id} không tồn tại")

    # Update fields
    rule.text = body.text
    rule.category = body.category
    rule.priority = body.priority

    return rule


@router.delete("/{rule_id}")
async def delete_rule(rule_id: str) -> dict[str, str]:
    """Xóa hoặc deactivate nguyên tắc"""
    rule = RULES.get(rule_id)
    if not rule:
        raise HTTPException(404, f"Rule {rule_id} không tồn tại")

    # Soft delete by marking inactive
    rule.is_active = False

    return {"message": f"Đã deactivate rule {rule_id}"}


@router.post("/{rule_id}/activate")
async def activate_rule(rule_id: str) -> RuleResp:
    """Kích hoạt lại nguyên tắc"""
    rule = RULES.get(rule_id)
    if not rule:
        raise HTTPException(404, f"Rule {rule_id} không tồn tại")

    rule.is_active = True
    return rule
