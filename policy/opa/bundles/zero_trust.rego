package zeta.zt

# Default policies
default allow = false
default risk = "medium"

# Helper to check admin role
admin_role := {r | r := input.subject.roles[_]; r == "admin"}
is_admin := count(admin_role) > 0

# Helper to check if resource is restricted
is_restricted := input.resource.classification == "restricted"

# Helper to check if action requires MFA
requires_mfa_action := input.action in ["write", "delete", "execute"]

# Helper to check off-hours
is_off_hours := input.env.hour < 6
is_off_hours := input.env.hour > 22

# Core denial rules
deny_restricted_no_admin {
    is_restricted
    not is_admin
}

deny_requires_mfa {
    requires_mfa_action
    not input.subject.mfa
}

deny_device_untrusted {
    input.action in ["write", "delete"]
    not input.subject.device_trust
}

deny_token_too_old {
    input.env.token_age > 3600  # 1 hour
    input.action in ["write", "delete", "execute"]
}

# Allow rule - must pass all denial checks
allow {
    not deny_restricted_no_admin
    not deny_requires_mfa
    not deny_device_untrusted
    not deny_token_too_old
}

# Risk calculation
risk = "critical" {
    deny_restricted_no_admin
}

risk = "high" {
    deny_requires_mfa
}

risk = "high" {
    deny_device_untrusted
}

risk = "medium" {
    is_off_hours
}

risk = "medium" {
    input.env.token_age > 1800  # 30 minutes
}

risk = "low" {
    is_admin
    input.subject.mfa
    input.subject.device_trust
}

# Additional context for decisions
reasons[msg] {
    deny_restricted_no_admin
    msg := "restricted_resource_requires_admin"
}

reasons[msg] {
    deny_requires_mfa
    msg := "action_requires_mfa"
}

reasons[msg] {
    deny_device_untrusted
    msg := "untrusted_device"
}

reasons[msg] {
    deny_token_too_old
    msg := "token_expired"
}

reasons[msg] {
    is_off_hours
    msg := "off_hours_access"
}

# Resource-specific rules
allow_public_resources {
    input.resource.classification == "public"
}

allow_read_internal {
    input.action == "read"
    input.resource.classification == "internal"
    count(input.subject.roles) > 0  # Any authenticated role
}

# Time-based restrictions
allow_business_hours {
    input.env.hour >= 6
    input.env.hour <= 22
}

# Special permissions for emergency scenarios
emergency_override {
    input.context.emergency == true
    is_admin
    input.subject.mfa
}

# Final allow with overrides
allow {
    allow_public_resources
}

allow {
    allow_read_internal
}

allow {
    emergency_override
}