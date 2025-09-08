#!/usr/bin/env python3
"""
Import Validation Script for RC v1.1.0
Tests all critical imports to ensure they work correctly.
"""
import sys
import os
import Exception
import description
import e
import exec
import import_statement
import import_stmt
import len
import print

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def test_import(import_statement, description):
    """Test a single import statement"""
    try:
        exec(import_statement)
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Import: {import_statement}")
        print(f"   Error: {e}")
        print()
        return False

def main():
    """Run all import validation tests"""
    print("🔍 RC v1.1.0 Import Validation")
    print("=" * 50)
    
    tests = [
        # Core dependencies
        ("import cryptography", "Cryptography library"),
        ("import httpx", "HTTPX HTTP client"),
        ("import jwt", "PyJWT library"),
        ("from prometheus_client import Counter", "Prometheus client"),
        
        # JWKS Cache
        ("from app.security.jwks_cache import JWKSCache", "JWKS Cache class"),
        ("from app.security.jwks_cache import decode_bearer_rs256", "JWKS decode function"),
        
        # OPA Client  
        ("from app.security.opa_client import OPAClient", "OPA Client class"),
        ("from app.security.opa_client import evaluate_zero_trust_policy", "OPA evaluation function"),
        
        # Zero-Trust Models
        ("from core.security.zero_trust.policy import Subject", "Zero-Trust Subject model"),
        ("from core.security.zero_trust.policy import Resource", "Zero-Trust Resource model"),
        ("from core.security.zero_trust.policy import Environment", "Zero-Trust Environment model"),
        ("from core.security.zero_trust.policy import abac_decide", "ABAC decision function"),
        
        # JWT Dependency
        ("from app.security.jwt_dependency import Identity", "JWT Identity model"),
        ("from app.security.jwt_dependency import get_identity", "JWT get_identity function"),
        
        # Policy Router
        ("from app.api.v1.security.policy_router import router", "Security policy router"),
    ]
    
    passed = 0
    total = len(tests)
    
    for import_stmt, description in tests:
        if test_import(import_stmt, description):
            passed += 1
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} imports successful")
    
    if passed == total:
        print("🎉 All imports working correctly!")
        return 0
    else:
        print("⚠️  Some imports failed - see details above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
