"""Enhanced permissions matrix cho comprehensive authorization system.

Mở rộng hệ thống permissions hiện có để support toàn bộ AI learning pipeline:
Router, Ingest, Triage, Training, Evaluation, Deployment, etc.
"""

from apps.backend.core.security.permissions import Permission
import AI_LEARNING_PERMISSIONS
import ENHANCED_ROLE_PERMISSIONS
import bool
import dict
import inherited_role
import list
import name
import new_perms
import perm
import perm_name
import permission
import role
import set
import str

# AI Learning System specific permissions
AI_LEARNING_PERMISSIONS: dict[str, Permission] = {
    # Model Router permissions
    "router:select": Permission(
        "router:select",
        "router",
        "select",
        "medium",
        description="Select model through router",
    ),
    "router:policy:update": Permission(
        "router:policy:update",
        "router",
        "policy_update",
        "critical",
        True,
        description="Update router security policies",
    ),
    "router:override_sensitivity": Permission(
        "router:override_sensitivity",
        "router",
        "override",
        "critical",
        True,
        description="Override data sensitivity constraints",
    ),
    # Registry permissions
    "registry:model:read": Permission(
        "registry:model:read",
        "registry",
        "read",
        "low",
        description="Read model registry",
    ),
    "registry:model:write": Permission(
        "registry:model:write",
        "registry",
        "write",
        "medium",
        description="Write to model registry",
    ),
    "registry:dataset:read": Permission(
        "registry:dataset:read",
        "registry",
        "read",
        "low",
        description="Read dataset registry",
    ),
    "registry:dataset:write": Permission(
        "registry:dataset:write",
        "registry",
        "write",
        "medium",
        description="Write to dataset registry",
    ),
    # Model management permissions
    "model:read": Permission(
        "model:read", "model", "read", "low", description="Read model information"
    ),
    "model:list": Permission(
        "model:list", "model", "list", "low", description="List available models"
    ),
    "model:publish": Permission(
        "model:publish", "model", "publish", "high", description="Publish trained model"
    ),
    "model:promote": Permission(
        "model:promote",
        "model",
        "promote",
        "critical",
        True,
        description="Promote model to production",
    ),
    "model:rollback": Permission(
        "model:rollback",
        "model",
        "rollback",
        "high",
        description="Rollback model deployment",
    ),
    "model:delete": Permission(
        "model:delete", "model", "delete", "high", description="Delete model"
    ),
    # Dataset permissions
    "dataset:create": Permission(
        "dataset:create",
        "dataset",
        "create",
        "medium",
        description="Create new dataset",
    ),
    "dataset:read": Permission(
        "dataset:read", "dataset", "read", "low", description="Read dataset"
    ),
    "dataset:update": Permission(
        "dataset:update", "dataset", "update", "medium", description="Update dataset"
    ),
    "dataset:delete": Permission(
        "dataset:delete", "dataset", "delete", "high", description="Delete dataset"
    ),
    "dataset:list": Permission(
        "dataset:list", "dataset", "list", "low", description="List datasets"
    ),
    "dataset:export": Permission(
        "dataset:export",
        "dataset",
        "export",
        "high",
        True,
        description="Export dataset",
    ),
    "dataset:import": Permission(
        "dataset:import", "dataset", "import", "medium", description="Import dataset"
    ),
    # Shard permissions
    "shard:read": Permission(
        "shard:read", "shard", "read", "low", description="Read data shard"
    ),
    "shard:list": Permission(
        "shard:list", "shard", "list", "low", description="List data shards"
    ),
    "shard:purge": Permission(
        "shard:purge", "shard", "purge", "high", description="Purge data shards"
    ),
    # Ingest permissions
    "ingest:start": Permission(
        "ingest:start", "ingest", "start", "medium", description="Start data ingestion"
    ),
    "ingest:cancel": Permission(
        "ingest:cancel",
        "ingest",
        "cancel",
        "medium",
        description="Cancel data ingestion",
    ),
    "ingest:view_status": Permission(
        "ingest:view_status",
        "ingest",
        "view",
        "low",
        description="View ingestion status",
    ),
    # Triage permissions
    "triage:read": Permission(
        "triage:read", "triage", "read", "low", description="Read triage decisions"
    ),
    "triage:update": Permission(
        "triage:update", "triage", "update", "medium", description="Update triage rules"
    ),
    "triage:approve": Permission(
        "triage:approve",
        "triage",
        "approve",
        "high",
        True,
        description="Approve triage decisions",
    ),
    # Training permissions
    "training:start": Permission(
        "training:start",
        "training",
        "start",
        "medium",
        description="Start training job",
    ),
    "training:cancel": Permission(
        "training:cancel",
        "training",
        "cancel",
        "medium",
        description="Cancel training job",
    ),
    "training:view_status": Permission(
        "training:view_status",
        "training",
        "view",
        "low",
        description="View training status",
    ),
    "training:delete": Permission(
        "training:delete",
        "training",
        "delete",
        "high",
        description="Delete training job",
    ),
    # Evaluation permissions
    "evaluation:run": Permission(
        "evaluation:run",
        "evaluation",
        "run",
        "medium",
        description="Run model evaluation",
    ),
    "evaluation:view": Permission(
        "evaluation:view",
        "evaluation",
        "view",
        "low",
        description="View evaluation results",
    ),
    "evaluation:list": Permission(
        "evaluation:list", "evaluation", "list", "low", description="List evaluations"
    ),
    "evaluation:delete": Permission(
        "evaluation:delete",
        "evaluation",
        "delete",
        "medium",
        description="Delete evaluation",
    ),
    # Deployment permissions
    "deployment:create": Permission(
        "deployment:create",
        "deployment",
        "create",
        "high",
        description="Create deployment",
    ),
    "deployment:read": Permission(
        "deployment:read",
        "deployment",
        "read",
        "low",
        description="Read deployment info",
    ),
    "deployment:promote": Permission(
        "deployment:promote",
        "deployment",
        "promote",
        "critical",
        True,
        description="Promote to production",
    ),
    "deployment:rollback": Permission(
        "deployment:rollback",
        "deployment",
        "rollback",
        "high",
        True,
        description="Rollback deployment",
    ),
    "deployment:delete": Permission(
        "deployment:delete",
        "deployment",
        "delete",
        "high",
        description="Delete deployment",
    ),
    # Security & Policy permissions
    "policy:read": Permission(
        "policy:read", "policy", "read", "medium", description="Read security policies"
    ),
    "policy:update": Permission(
        "policy:update",
        "policy",
        "update",
        "critical",
        True,
        description="Update security policies",
    ),
    "secret:read": Permission(
        "secret:read", "secret", "read", "critical", True, description="Read secrets"
    ),
    "secret:write": Permission(
        "secret:write", "secret", "write", "critical", True, description="Write secrets"
    ),
    # Audit permissions
    "audit:read": Permission(
        "audit:read", "audit", "read", "medium", description="Read audit logs"
    ),
    "audit:export": Permission(
        "audit:export", "audit", "export", "high", True, description="Export audit logs"
    ),
    # WebSocket permissions
    "ws_session:start": Permission(
        "ws_session:start",
        "ws",
        "start",
        "medium",
        description="Start WebSocket session",
    ),
    "ws_session:control": Permission(
        "ws_session:control",
        "ws",
        "control",
        "high",
        description="Control WebSocket session",
    ),
    "ws_session:view": Permission(
        "ws_session:view", "ws", "view", "low", description="View WebSocket session"
    ),
}


# Enhanced role permissions mapping
ENHANCED_ROLE_PERMISSIONS: dict[str, list[str]] = {
    # Guest - minimal read access
    "guest": [
        "router:select",
        "model:read",
        "model:list",
        "dataset:read",
        "dataset:list",
        "shard:read",
        "shard:list",
        "training:view_status",
        "evaluation:view",
        "evaluation:list",
        "registry:model:read",
        "registry:dataset:read",
        "ws_session:view",
    ],
    # User - basic operations
    "user": [
        "agent:read",
        "agent:list",
        "agent:run",
        "router:select",
        "dataset:read",
        "dataset:list",
        "training:start",
        "training:cancel",
        "training:view_status",
        "evaluation:run",
        "evaluation:view",
        "evaluation:list",
        "ws_session:start",
        "ws_session:view",
        "ingest:view_status",
        "triage:read",
    ],
    # Power User - advanced operations
    "power_user": [
        "agent:create",
        "agent:update",
        "shard:purge",
        "dataset:export",
        "dataset:import",
        "evaluation:delete",
        "training:delete",
        "ws_session:control",
        "ingest:start",
        "ingest:cancel",
    ],
    # Trainer - ML pipeline operations
    "trainer": [
        "ingest:start",
        "ingest:cancel",
        "ingest:view_status",
        "triage:read",
        "triage:update",
        "training:start",
        "training:cancel",
        "training:view_status",
        "training:delete",
        "registry:dataset:write",
        "registry:model:write",
        "evaluation:run",
        "evaluation:view",
        "evaluation:list",
        "evaluation:delete",
        "model:publish",
        "dataset:create",
        "dataset:update",
        "dataset:import",
    ],
    # Data Custodian - data governance
    "data_custodian": [
        "dataset:create",
        "dataset:delete",
        "dataset:export",
        "dataset:import",
        "triage:approve",
        "secret:read",
        "audit:read",
        "shard:purge",
        "registry:dataset:write",
        "policy:read",
    ],
    # Risk Officer - security oversight
    "risk_officer": [
        "audit:read",
        "audit:export",
        "policy:read",
        "policy:update",
        "router:policy:update",
        "router:override_sensitivity",
        "triage:approve",
        "secret:read",
    ],
    # Admin - system administration
    "admin": [
        "agent:delete",
        "agent:create",
        "agent:update",
        "audit:read",
        "registry:model:write",
        "registry:dataset:write",
        "deployment:create",
        "deployment:read",
        "deployment:delete",
        "policy:read",
        "model:delete",
        "ws_session:control",
    ],
    # Super Admin - full access
    "superadmin": [
        "deployment:promote",
        "deployment:rollback",
        "model:promote",
        "model:rollback",
        "policy:update",
        "router:policy:update",
        "router:override_sensitivity",
        "secret:read",
        "secret:write",
        "audit:export",
        "triage:approve",
    ],
    # Service Account for Training workflows
    "svc_trainer": [
        "ingest:start",
        "ingest:cancel",
        "ingest:view_status",
        "triage:read",
        "triage:update",
        "training:start",
        "training:cancel",
        "training:view_status",
        "evaluation:run",
        "evaluation:view",
        "model:publish",
        "registry:model:write",
        "registry:dataset:write",
        "dataset:read",
        "dataset:create",
        "dataset:update",
        "router:select",
    ],
    # Service Account for Deployment
    "svc_deployment": [
        "deployment:create",
        "deployment:read",
        "model:read",
        "model:list",
        "evaluation:view",
        "evaluation:list",
        "router:select",
        "registry:model:read",
    ],
}


def get_enhanced_permissions() -> dict[str, Permission]:
    """Get all permissions including AI learning system permissions."""
    from apps.backend.core.security.permissions import PERMISSIONS  # noqa: PLC0415

    # Merge existing permissions with AI learning permissions
    all_permissions = PERMISSIONS.copy()
    all_permissions.update(AI_LEARNING_PERMISSIONS)

    return all_permissions


def get_enhanced_role_permissions() -> dict[str, list[str]]:
    """Get enhanced role permissions including AI learning permissions."""
    from apps.backend.core.security.permissions import (
        DEFAULT_ROLE_PERMISSIONS,  # noqa: PLC0415
    )

    # Merge existing role permissions with enhanced ones
    all_role_perms = DEFAULT_ROLE_PERMISSIONS.copy()

    # Extend existing roles with new permissions
    for role, new_perms in ENHANCED_ROLE_PERMISSIONS.items():
        if role in all_role_perms:
            # Merge with existing permissions
            all_role_perms[role] = list(set(all_role_perms[role] + new_perms))
        else:
            # New role
            all_role_perms[role] = new_perms

    return all_role_perms


def get_ai_learning_permissions_by_domain() -> dict[str, list[str]]:
    """Get AI learning permissions grouped by domain."""
    domains = {}

    for perm_name, perm in AI_LEARNING_PERMISSIONS.items():
        domain = perm.domain
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(perm_name)

    return domains


def get_high_risk_ai_permissions() -> list[str]:
    """Get AI learning permissions that are high risk."""
    return [
        name
        for name, perm in AI_LEARNING_PERMISSIONS.items()
        if perm.risk in ["high", "critical"]
    ]


def get_mfa_required_ai_permissions() -> list[str]:
    """Get AI learning permissions that require MFA."""
    return [name for name, perm in AI_LEARNING_PERMISSIONS.items() if perm.requires_mfa]


def validate_ai_learning_permission(permission: str) -> bool:
    """Validate if permission exists in AI learning system."""
    return permission in AI_LEARNING_PERMISSIONS


def get_permissions_for_ai_role(role: str) -> set[str]:
    """Get all permissions for an AI learning role."""
    base_perms = set(ENHANCED_ROLE_PERMISSIONS.get(role, []))

    # Add inheritance
    role_hierarchy = {
        "user": ["guest"],
        "power_user": ["user", "guest"],
        "trainer": ["user", "guest"],
        "data_custodian": ["power_user", "user", "guest"],
        "admin": ["power_user", "user", "guest"],
        "risk_officer": ["admin", "power_user", "user", "guest"],
        "superadmin": ["admin", "power_user", "user", "guest"],
    }

    inherited_roles = role_hierarchy.get(role, [])
    for inherited_role in inherited_roles:
        base_perms.update(ENHANCED_ROLE_PERMISSIONS.get(inherited_role, []))

    return base_perms
