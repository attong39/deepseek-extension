package zeta

import future.keywords.if
import future.keywords.in

# Default deny all access
default allow = false
default reason = "deny_default"

# Input format:
# {
#   "subject": {"user_id": "...", "tenant_id": "...", "roles": [...]},
#   "action": {"name": "router:select", "risk": "medium"},
#   "resource": {"type": "router", "id": "...", "tenant_id": "...", "sensitivity": "..."},
#   "env": {"ip": "...", "user_agent": "...", "device_trust": "..."},
#   "extras": {"provider": "...", "budget_ok": true, "jit_ok": false, ...}
# }

# ============================================================================
# RBAC Check - Basic role-based permissions
# ============================================================================

rbac_allow if {
    input.rbac_ok == true
}

rbac_allow if {
    some role in input.subject.roles
    role_has_permission(role, input.action.name)
}

role_has_permission(role, permission) if {
    permission in data.role_permissions[role]
}

# ============================================================================
# ABAC Check - Attribute-based constraints
# ============================================================================

abac_allow if {
    input.abac_ok == true
}

abac_allow if {
    tenant_matches
    ownership_check
    sensitivity_check
}

# Tenant isolation
tenant_matches if {
    input.subject.tenant_id == input.resource.tenant_id
}

# Ownership check
ownership_check if {
    # System/service accounts bypass ownership
    startswith(input.subject.user_id, "svc:")
}

ownership_check if {
    # Admins bypass ownership
    some role in input.subject.roles
    role in {"admin", "superadmin", "risk_officer"}
}

ownership_check if {
    # Owner can access their resources
    input.resource.owner_id == input.subject.user_id
}

ownership_check if {
    # Public resources accessible to all
    input.resource.sensitivity == "public"
}

# Sensitivity level check
sensitivity_check if {
    input.resource.sensitivity in {"public", "internal"}
}

sensitivity_check if {
    input.resource.sensitivity == "restricted"
    some role in input.subject.roles
    role in {"power_user", "trainer", "data_custodian", "admin", "superadmin", "risk_officer"}
}

sensitivity_check if {
    input.resource.sensitivity == "secret"
    some role in input.subject.roles
    role in {"data_custodian", "superadmin", "risk_officer"}
}

# ============================================================================
# Model Router Specific Policies
# ============================================================================

# Basic router selection allowed if RBAC/ABAC pass
allow if {
    input.action.name == "router:select"
    rbac_allow
    abac_allow
    provider_policy_check
    budget_policy_check
}

# External provider restrictions for sensitive data
provider_policy_check if {
    # Non-sensitive data can use any provider
    input.resource.sensitivity in {"public", "internal"}
}

provider_policy_check if {
    # High/secret data with on-premise providers is OK
    input.resource.sensitivity in {"high", "secret"}
    input.extras.provider in {"local", "vllm", "ollama", "huggingface"}
}

provider_policy_check if {
    # High/secret data with external providers requires JIT + risk officer approval
    input.resource.sensitivity in {"high", "secret"}
    input.extras.provider in {"openai", "anthropic", "google", "azure"}
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"risk_officer", "superadmin"}
}

# Budget constraint enforcement
budget_policy_check if {
    # No budget constraint specified
    not input.extras.budget_constraint
}

budget_policy_check if {
    # Budget constraint satisfied
    input.extras.budget_ok == true
}

# Policy override permissions
allow if {
    input.action.name == "router:policy:update"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"risk_officer", "superadmin"}
}

allow if {
    input.action.name == "router:override_sensitivity"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"risk_officer", "superadmin"}
}

# ============================================================================
# Dataset Governance Policies
# ============================================================================

# Dataset export requires data custodian + JIT
allow if {
    input.action.name == "dataset:export"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"data_custodian", "superadmin"}
}

# Dataset deletion requires high privileges
allow if {
    input.action.name == "dataset:delete"
    rbac_allow
    abac_allow
    some role in input.subject.roles
    role in {"data_custodian", "admin", "superadmin"}
}

# Triage approval restricted to data custodians
allow if {
    input.action.name == "triage:approve"
    rbac_allow
    abac_allow
    some role in input.subject.roles
    role in {"data_custodian", "risk_officer", "superadmin"}
}

# ============================================================================
# Training & Model Management Policies
# ============================================================================

# Model promotion requires evaluation + superadmin
allow if {
    input.action.name == "model:promote"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    input.extras.evaluation_passed == true
    some role in input.subject.roles
    role == "superadmin"
}

# Deployment promotion requires multiple approvals
allow if {
    input.action.name == "deployment:promote"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    input.extras.evaluation_passed == true
    input.extras.risk_assessment_passed == true
    some role in input.subject.roles
    role == "superadmin"
}

# Training operations for trainers and service accounts
allow if {
    input.action.name in {"training:start", "training:cancel"}
    rbac_allow
    abac_allow
    some role in input.subject.roles
    role in {"trainer", "svc_trainer", "admin", "superadmin"}
}

# ============================================================================
# Security & Audit Policies
# ============================================================================

# Secret access heavily restricted
allow if {
    input.action.name == "secret:read"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"data_custodian", "superadmin"}
    high_trust_environment
}

allow if {
    input.action.name == "secret:write"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role == "superadmin"
    high_trust_environment
}

# Policy updates require risk officer approval
allow if {
    input.action.name == "policy:update"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"risk_officer", "superadmin"}
}

# Audit export requires approval
allow if {
    input.action.name == "audit:export"
    rbac_allow
    abac_allow
    input.extras.jit_ok == true
    some role in input.subject.roles
    role in {"risk_officer", "superadmin"}
}

# ============================================================================
# WebSocket Session Policies
# ============================================================================

# WebSocket control requires elevated privileges
allow if {
    input.action.name == "ws_session:control"
    rbac_allow
    abac_allow
    some role in input.subject.roles
    role in {"power_user", "trainer", "admin", "superadmin"}
}

# ============================================================================
# Default Allow for Low Risk Actions
# ============================================================================

# Low and medium risk actions allowed if RBAC/ABAC pass
allow if {
    input.action.risk in {"low", "medium"}
    rbac_allow
    abac_allow
}

# ============================================================================
# Environment Trust Checks
# ============================================================================

high_trust_environment if {
    input.env.device_trust == "high"
    trusted_network
}

trusted_network if {
    # Internal network ranges
    net.cidr_contains("10.0.0.0/8", input.env.ip)
}

trusted_network if {
    net.cidr_contains("172.16.0.0/12", input.env.ip)
}

trusted_network if {
    net.cidr_contains("192.168.0.0/16", input.env.ip)
}

trusted_network if {
    # Localhost
    input.env.ip == "127.0.0.1"
}

# ============================================================================
# Utility Functions
# ============================================================================

has_role(roles, allowed_roles) if {
    some role in roles
    role in allowed_roles
}

# Emergency break-glass for superadmin
allow if {
    input.extras.break_glass == true
    input.extras.jit_ok == true
    input.subject.user_id == "superadmin"
    input.env.device_trust == "high"
}

# Service account bypass for automation
allow if {
    startswith(input.subject.user_id, "svc:")
    rbac_allow
    tenant_matches
    input.env.ip == "127.0.0.1"  # Must be from localhost
}

# ============================================================================
# Reason Codes for Deny
# ============================================================================

reason = "rbac_failed" if {
    not rbac_allow
}

reason = "abac_failed" if {
    rbac_allow
    not abac_allow
}

reason = "tenant_mismatch" if {
    rbac_allow
    not tenant_matches
}

reason = "sensitivity_violation" if {
    rbac_allow
    abac_allow
    not sensitivity_check
}

reason = "provider_policy_violation" if {
    input.action.name == "router:select"
    rbac_allow
    abac_allow
    not provider_policy_check
}

reason = "budget_policy_violation" if {
    input.action.name == "router:select"
    rbac_allow
    abac_allow
    not budget_policy_check
}

reason = "jit_required" if {
    rbac_allow
    abac_allow
    input.action.risk in {"high", "critical"}
    not input.extras.jit_ok
}

reason = "insufficient_role" if {
    rbac_allow
    abac_allow
    input.action.name in {
        "secret:read", "secret:write", "policy:update",
        "model:promote", "deployment:promote"
    }
    not has_role(input.subject.roles, {"data_custodian", "risk_officer", "superadmin"})
}

reason = "untrusted_environment" if {
    rbac_allow
    abac_allow
    input.action.name in {"secret:read", "secret:write"}
    not high_trust_environment
}
