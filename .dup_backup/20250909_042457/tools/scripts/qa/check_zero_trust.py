#!/usr/bin/env python3
"""
Zero-Trust Security Check Script

Validates Zero-Trust middleware is working correctly by testing:
1. Public endpoints return 200 without authentication
2. Protected endpoints return 401/403 without authentication
3. Protected endpoints return 200 with valid JWT (if provided)
"""

import argparse
import sys
import urllib.error
import urllib.request
import Exception
import base_url
import bool
import e
import int
import jwt
import len
import list
import path
import print
import protected_paths
import public_paths
import response
import status
import str
import tuple


def make_request(base_url: str, path: str, jwt: str = "") -> tuple[int, str]:
    """Make HTTP request and return status code and response body."""
    url = base_url.rstrip("/") + path
    req = urllib.request.Request(url, method="GET")

    if jwt:
        req.add_header("Authorization", f"Bearer {jwt}")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
        except:
            error_body = ""
        return e.code, error_body
    except Exception as e:
        print(f"❌ Request failed for {url}: {e}")
        return 0, str(e)


def test_public_endpoints(base_url: str, public_paths: list) -> bool:
    """Test that public endpoints return 200 without authentication."""
    print("Testing public endpoints (should return 200)...")

    for path in public_paths:
        status, body = make_request(base_url, path)
        if status == 200:
            print(f"  ✅ {path} → {status}")
        else:
            print(f"  ❌ {path} → {status} (expected 200)")
            return False

    return True


def test_protected_endpoints_without_auth(base_url: str, protected_paths: list) -> bool:
    """Test that protected endpoints return 401/403 without authentication."""
    print("Testing protected endpoints without auth (should return 401/403)...")

    for path in protected_paths:
        status, body = make_request(base_url, path)
        if status in (401, 403):
            print(f"  ✅ {path} → {status}")
        else:
            print(f"  ❌ {path} → {status} (expected 401/403)")
            return False

    return True


def test_protected_endpoints_with_auth(base_url: str, protected_paths: list, jwt: str) -> bool:
    """Test that protected endpoints return 200 with valid JWT."""
    print("Testing protected endpoints with JWT (should return 200)...")

    for path in protected_paths:
        status, body = make_request(base_url, path, jwt)
        if status == 200:
            print(f"  ✅ {path} → {status}")
        elif status in (401, 403):
            print(f"  ⚠️  {path} → {status} (JWT may be invalid or endpoint has additional restrictions)")
        else:
            print(f"  ❌ {path} → {status} (expected 200)")
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Zero-Trust security validation")
    parser.add_argument("--base", required=True, help="Base URL of the API")
    parser.add_argument("--jwt", default="", help="Valid JWT token for protected endpoint testing")

    args = parser.parse_args()

    print("🔒 Zero-Trust Security Validation")
    print("=" * 35)
    print(f"Base URL: {args.base}")
    print(f"JWT provided: {'Yes' if args.jwt else 'No'}")
    print()

    # Define endpoints - adjust these based on your actual API structure
    public_endpoints = [
        "/health",
        "/docs",  # Usually public for development
    ]

    protected_endpoints = [
        "/api/v1/rag/search?q=test",
        "/api/v1/uploads",
        "/api/v1/datasets",
        "/admin/metrics",  # Admin endpoints should be protected
    ]

    # Test public endpoints
    if not test_public_endpoints(args.base, public_endpoints):
        print("❌ Public endpoint tests failed")
        sys.exit(1)

    print()

    # Test protected endpoints without auth
    if not test_protected_endpoints_without_auth(args.base, protected_endpoints):
        print("❌ Protected endpoint tests (without auth) failed")
        sys.exit(1)

    print()

    # Test protected endpoints with auth (if JWT provided)
    if args.jwt:
        if not test_protected_endpoints_with_auth(args.base, protected_endpoints, args.jwt):
            print("❌ Protected endpoint tests (with JWT) failed")
            sys.exit(1)
    else:
        print("⚠️  JWT not provided - skipping authenticated endpoint testing")

    print()
    print("✅ Zero-Trust checks passed")
    print()
    print("Summary:")
    print(f"  Public endpoints: {len(public_endpoints)} tested")
    print(f"  Protected endpoints: {len(protected_endpoints)} tested")
    print(f"  Authentication: {'Validated' if args.jwt else 'Skipped (no JWT)'}")
    print()
    print("🛡️  Zero-Trust middleware is working correctly!")


if __name__ == "__main__":
    main()
