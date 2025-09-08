"""Enhanced role seeder để support comprehensive authorization system.

Extends existing role seeding với AI learning system roles và permissions.
"""

import logging

from apps.backend.core.security.ai_permissions import (
import Exception
import any
import d
import e
import inherits
import issue
import len
import name
import p
import perm
import perm_name
import perms
import print
import required_perms
import role
import role_name
import service_role
import set
import sorted
    get_enhanced_permissions,
    get_enhanced_role_permissions,
)

logger = logging.getLogger(__name__)


# AI Learning System specific roles to add
AI_LEARNING_ROLES = {
    "trainer": {
        "description": "ML Engineer role for training operations",
        "department": "ml_engineering",
        "risk_level": "medium",
        "requires_approval": False,
    },
    "data_custodian": {
        "description": "Data governance and custodian role",
        "department": "data_governance",
        "risk_level": "high",
        "requires_approval": True,
    },
    "risk_officer": {
        "description": "Security and risk management oversight",
        "department": "security",
        "risk_level": "critical",
        "requires_approval": True,
    },
    "svc_trainer": {
        "description": "Service account for automated training workflows",
        "department": "automation",
        "risk_level": "medium",
        "requires_approval": False,
        "is_service_account": True,
    },
    "svc_deployment": {
        "description": "Service account for deployment operations",
        "department": "automation",
        "risk_level": "high",
        "requires_approval": False,
        "is_service_account": True,
    },
}


def seed_ai_learning_roles():
    """Seed AI learning system roles và permissions."""
    print("🔑 Seeding AI Learning System Roles & Permissions")
    print("=" * 55)

    # Get enhanced permissions and roles
    all_permissions = get_enhanced_permissions()
    all_role_permissions = get_enhanced_role_permissions()

    print(f"\n📋 Total Permissions: {len(all_permissions)}")
    print(f"👥 Total Roles: {len(all_role_permissions)}")

    # Show new AI learning permissions
    ai_learning_perms = [
        perm
        for perm in all_permissions
        if any(
            domain in perm
            for domain in [
                "router:",
                "registry:",
                "model:",
                "dataset:",
                "shard:",
                "ingest:",
                "triage:",
                "training:",
                "evaluation:",
                "deployment:",
                "policy:",
                "secret:",
                "audit:",
                "ws_session:",
            ]
        )
    ]

    print(f"\n🤖 AI Learning Permissions: {len(ai_learning_perms)}")

    # Group by domain
    domains = {}
    for perm in ai_learning_perms:
        domain = perm.split(":")[0]
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(perm)

    for domain, perms in sorted(domains.items()):
        print(f"  📁 {domain}: {len(perms)} permissions")

    # Show role configurations
    print("\n👥 Role Configurations:")

    for role_name in [
        "guest",
        "user",
        "trainer",
        "data_custodian",
        "risk_officer",
        "svc_trainer",
    ]:
        role_perms = all_role_permissions.get(role_name, [])
        ai_perms = [p for p in role_perms if any(d in p for d in domains)]

        role_info = AI_LEARNING_ROLES.get(role_name, {})
        risk_level = role_info.get("risk_level", "low")
        is_service = role_info.get("is_service_account", False)

        service_indicator = " 🤖" if is_service else ""
        print(
            f"  👤 {role_name:<15} | Risk: {risk_level:<8} | AI Perms: {len(ai_perms):>2}{service_indicator}"
        )

    # Show high-risk permissions
    print("\n⚠️ High-Risk Permissions:")
    high_risk_perms = [
        name
        for name, perm in all_permissions.items()
        if perm.risk in ["high", "critical"]
    ]

    for perm in sorted(high_risk_perms):
        perm_obj = all_permissions[perm]
        mfa_req = " 🔐" if perm_obj.requires_mfa else ""
        print(f"  🚨 {perm:<30} | {perm_obj.risk:<8}{mfa_req}")

    # Show role inheritance
    print("\n🔗 Role Inheritance:")
    role_hierarchy = {
        "user": ["guest"],
        "power_user": ["user", "guest"],
        "trainer": ["user", "guest"],
        "data_custodian": ["power_user", "user", "guest"],
        "admin": ["power_user", "user", "guest"],
        "risk_officer": ["admin", "power_user", "user", "guest"],
        "superadmin": ["admin", "power_user", "user", "guest"],
    }

    for role, inherits in role_hierarchy.items():
        print(f"  🔄 {role:<15} inherits: {', '.join(inherits)}")

    print("\n✅ AI Learning System roles seeded successfully!")

    return {
        "total_permissions": len(all_permissions),
        "ai_learning_permissions": len(ai_learning_perms),
        "total_roles": len(all_role_permissions),
        "ai_learning_roles": len(AI_LEARNING_ROLES),
        "high_risk_permissions": len(high_risk_perms),
    }


def validate_role_permissions():
    """Validate role permissions consistency."""
    print("\n🔍 Validating Role Permissions Consistency")
    print("=" * 45)

    all_permissions = get_enhanced_permissions()
    all_role_permissions = get_enhanced_role_permissions()

    issues = []

    # Check for undefined permissions in roles
    for role_name, perms in all_role_permissions.items():
        for perm in perms:
            if perm not in all_permissions:
                issues.append(f"Role '{role_name}' has undefined permission: '{perm}'")

    # Check for service account permissions
    service_roles = ["svc_trainer", "svc_deployment"]
    required_service_perms = {
        "svc_trainer": ["training:start", "model:publish", "registry:model:write"],
        "svc_deployment": ["deployment:create", "model:read"],
    }

    for service_role, required_perms in required_service_perms.items():
        if service_role in all_role_permissions:
            role_perms = set(all_role_permissions[service_role])
            missing_perms = set(required_perms) - role_perms
            if missing_perms:
                issues.append(
                    f"Service role '{service_role}' missing required permissions: {missing_perms}"
                )

    # Check for critical permission isolation
    critical_perms = [
        name for name, perm in all_permissions.items() if perm.risk == "critical"
    ]

    authorized_roles = {"risk_officer", "superadmin"}
    for role_name, perms in all_role_permissions.items():
        if role_name not in authorized_roles:
            critical_in_role = [p for p in perms if p in critical_perms]
            if critical_in_role:
                issues.append(
                    f"Role '{role_name}' has critical permissions but not authorized: {critical_in_role}"
                )

    # Report validation results
    if issues:
        print("❌ Validation Issues Found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ All role permissions are valid!")

    # Show statistics
    print("\n📊 Validation Statistics:")
    print(f"  • Total permissions checked: {len(all_permissions)}")
    print(f"  • Total roles checked: {len(all_role_permissions)}")
    print(f"  • Critical permissions: {len(critical_perms)}")
    print(f"  • Service accounts: {len(service_roles)}")
    print(f"  • Issues found: {len(issues)}")

    return len(issues) == 0


def generate_role_matrix():
    """Generate role-permission matrix for documentation."""
    print("\n📋 Generating Role-Permission Matrix")
    print("=" * 40)

    all_permissions = get_enhanced_permissions()
    all_role_permissions = get_enhanced_role_permissions()

    # Group permissions by domain
    domains = {}
    for perm_name in all_permissions:
        domain = perm_name.split(":")[0]
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(perm_name)

    # Generate matrix
    matrix = {}
    for domain, perms in sorted(domains.items()):
        matrix[domain] = {}
        for role_name in sorted(all_role_permissions.keys()):
            role_perms = set(all_role_permissions[role_name])
            domain_perms = [p for p in perms if p in role_perms]
            matrix[domain][role_name] = len(domain_perms)

    # Display matrix
    print("\n📊 Permissions by Domain & Role:")
    print(f"{'Domain':<15}", end="")
    for role in sorted(all_role_permissions.keys()):
        print(f"{role[:8]:>8}", end="")
    print()
    print("-" * (15 + 8 * len(all_role_permissions)))

    for domain in sorted(matrix.keys()):
        print(f"{domain:<15}", end="")
        for role in sorted(all_role_permissions.keys()):
            count = matrix[domain].get(role, 0)
            print(f"{count:>8}", end="")
        print()

    return matrix


def main():
    """Run role seeding và validation."""
    print("🚀 ZETA AI Learning System - Role Seeding & Validation")
    print("=" * 65)

    try:
        # Seed roles
        stats = seed_ai_learning_roles()

        # Validate permissions
        is_valid = validate_role_permissions()

        # Generate matrix
        matrix = generate_role_matrix()

        print("\n🎉 Seeding completed!")
        print(f"  📊 Stats: {stats}")
        print(f"  ✅ Valid: {is_valid}")
        print(f"  📋 Matrix domains: {len(matrix)}")

        return stats, is_valid, matrix

    except Exception as e:
        print(f"\n💥 Seeding failed: {e}")
        logger.exception("Role seeding failed")
        raise


if __name__ == "__main__":
    main()
