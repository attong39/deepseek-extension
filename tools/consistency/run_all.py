#!/usr/bin/env python
"""
Consistency Guard - Entry Point
Run full Desktop ↔ AI Server contract synchronization check.
Exit code: 0 (ok/warn) or 1 (fail)
"""
import json
import sys
import traceback
from pathlib import Path

# Add current directory and parent to Python path for imports
current_dir = Path(__file__).parent
root_dir = current_dir.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(current_dir))

from backend_scanner import scan_backend
from compare_contracts import compare
from fe_hash import read_fe_hash
from frontend_scanner import scan_frontend
from openapi_hash import calc_hash
from openapi_loader import load_openapi
from report import write_reports


def main() -> int:
    """
    Main entry point for Consistency Guard.
    
    Returns:
        Exit code: 0 for success/warning, 1 for critical failure
    """
    print("🛡️ Consistency Guard - Desktop ↔ AI Server Contract Sync")
    print("=" * 60)
    
    try:
        repo_root = Path(".")
        frontend_root = repo_root / "apps/desktop/src"
        
        # Validate directories exist
        if not frontend_root.exists():
            print(f"⚠️  Frontend directory not found: {frontend_root}")
            print("   Creating minimal structure for testing...")
            frontend_root.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Load OpenAPI specification
        print("\n1️⃣ Loading OpenAPI specification...")
        openapi_doc = load_openapi()
        
        # Step 2: Scan backend contracts
        print("\n2️⃣ Scanning backend contracts...")
        backend_result = scan_backend(openapi_doc, repo_root=str(repo_root))
        
        # Step 3: Scan frontend usage
        print("\n3️⃣ Scanning frontend usage...")
        frontend_result = scan_frontend(str(frontend_root))
        
        # Step 4: Calculate hash comparison
        print("\n4️⃣ Calculating hash status...")
        be_hash = calc_hash(openapi_doc)
        fe_hash = read_fe_hash()
        hash_match = fe_hash == be_hash if fe_hash else False
        
        print(f"   Backend hash: {be_hash}")
        print(f"   Frontend hash: {fe_hash or '<missing>'}")
        print(f"   Hash match: {'✅' if hash_match else '❌'}")
        
        # Step 5: Compare contracts
        print("\n5️⃣ Comparing contracts...")
        comparison_result = compare(frontend_result, backend_result)
        
        # Step 6: Enhanced result with hash info
        enhanced_result = {
            **comparison_result,
            "openapi_hash": be_hash,
            "fe_hash": fe_hash,
            "hash_match": hash_match
        }
        
        # Step 7: Generate reports
        print("\n6️⃣ Generating reports...")
        write_reports(enhanced_result)
        
        # Step 8: Output result for CI consumption
        print("\n7️⃣ Final result:")
        print(json.dumps(enhanced_result, ensure_ascii=False, indent=2))
        
        # Determine exit code
        severity = comparison_result["severity"]
        if severity == "fail":
            print("\n❌ Consistency Guard FAILED - Critical mismatches detected")
            print("   CI will be blocked until issues are resolved")
            return 1
        elif severity == "warn":
            print("\n⚠️  Consistency Guard WARNED - Non-critical issues detected")
            print("   Review the report and consider addressing warnings")
            return 0
        else:
            print("\n✅ Consistency Guard PASSED - All contracts are in sync")
            return 0
            
    except Exception as e:
        print(f"\n💥 Consistency Guard ERROR: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
