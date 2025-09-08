#!/usr/bin/env python3
"""Simple validation script for enhanced authentication system."""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

def test_enhanced_features():
    """Test the enhanced features that have been implemented."""
import Exception
import FileNotFoundError
import e
import file
import hasattr
import len
import print
    print("🔍 Enhanced Authentication System v2.1 - Simple Validation")
    print("=" * 60)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Configuration enhancements
    total_tests += 1
    try:
        import mfa_config
        config = mfa_config.MFAConfig(
            device_fingerprint_secret=os.getenv("SECRET"),
            enable_metrics=True,
            enable_tracing=True,
            adaptive_rate_limiting=True,
            secure_token_length=32,
            max_sms_per_phone_per_day=15
        )
        
        # Verify new fields exist
        assert hasattr(config, 'device_fingerprint_secret')
        assert hasattr(config, 'enable_metrics')
        assert hasattr(config, 'adaptive_rate_limiting')
        assert hasattr(config, 'secure_token_length')
        assert hasattr(config, 'max_sms_per_phone_per_day')
        
        print("✅ Test 1: Enhanced MFA Configuration - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 1: Enhanced MFA Configuration - FAILED: {e}")
    
    # Test 2: Metrics system
    total_tests += 1
    try:
        import metrics
        
        # Test metrics initialization
        auth_metrics = metrics.initialize_metrics(enable_prometheus=True)
        
        # Test metric operations
        auth_metrics.increment_sms_generated("success")
        auth_metrics.increment_security_event("test_event", "low")
        auth_metrics.set_active_devices(10)
        
        # Test metrics retrieval
        all_metrics = auth_metrics.get_all_metrics()
        prometheus_output = auth_metrics.get_prometheus_metrics()
        
        assert "security_events" in all_metrics
        assert "sms_operations" in all_metrics
        assert len(prometheus_output) > 0
        
        print("✅ Test 2: Metrics System - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 2: Metrics System - FAILED: {e}")
    
    # Test 3: Security auditor
    total_tests += 1
    try:
        import security_audit
        
        auditor = security_audit.SecurityAuditor()
        
        # Test code auditing
        test_code = '''
import subprocess
password=os.getenv("PASSWORD")
subprocess.call(user_input, shell=True)
'''
        result = auditor.audit_code_string(test_code, "test.py")
        
        # Should find security issues
        assert "issues" in result
        assert len(result["issues"]) > 0
        
        print("✅ Test 3: Security Auditor - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 3: Security Auditor - FAILED: {e}")
    
    # Test 4: Enhanced memory storage
    total_tests += 1
    try:
        import memory_storage
        
        # Test MFA storage
        mfa_storage = memory_storage.MemoryMFAStorage()
        
        # Test new methods
        assert hasattr(mfa_storage, '__len__')
        assert hasattr(mfa_storage, '__repr__')
        assert len(mfa_storage) == 0
        
        # Test verification storage
        ver_storage = memory_storage.MemoryVerificationStorage()
        assert hasattr(ver_storage, '__len__')
        assert len(ver_storage) == 0
        
        print("✅ Test 4: Enhanced Memory Storage - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 4: Enhanced Memory Storage - FAILED: {e}")
    
    # Test 5: Device trust enhancements
    total_tests += 1
    try:
        import device_trust_manager
        import mfa_config
        
        config = mfa_config.MFAConfig(
            device_fingerprint_secret=os.getenv("SECRET"),
            secure_token_length=32
        )
        
        device_trust = device_trust_manager.DeviceTrustManager(config)
        
        # Test enhanced methods
        assert hasattr(device_trust, 'get_stats')
        
        # Test device trust with HMAC
        fingerprint = "test-browser-fingerprint"
        token = device_trust.trust_device(fingerprint)
        
        # Verify token length is as configured
        assert len(token) >= 32  # Should be at least 32 characters
        
        # Test stats
        stats = device_trust.get_stats()
        assert "active_devices" in stats
        assert "total_devices_created" in stats
        
        print("✅ Test 5: Enhanced Device Trust Manager - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 5: Enhanced Device Trust Manager - FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 6: File structure validation
    total_tests += 1
    try:
        expected_files = [
            "mfa_config.py",
            "metrics.py", 
            "security_audit.py",
            "device_trust_manager.py",
            "memory_storage.py",
            "factory.py",
            "fastapi_example.py",
            "README.md"
        ]
        
        missing_files = []
        for file in expected_files:
            if not os.path.exists(os.path.join(current_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            raise FileNotFoundError(f"Missing files: {missing_files}")
        
        print("✅ Test 6: File Structure Validation - PASSED")
        success_count += 1
    except Exception as e:
        print(f"❌ Test 6: File Structure Validation - FAILED: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Validation Summary: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED - Enhanced Authentication System v2.1 is ready!")
        print("\n🚀 Key Features Validated:")
        print("   • Enhanced configuration with HMAC secrets")
        print("   • Comprehensive metrics and monitoring")
        print("   • Security auditing and vulnerability detection")
        print("   • Enhanced memory storage with debugging")
        print("   • HMAC-based device trust with secure tokens")
        print("   • Complete file structure and modules")
        return True
    else:
        failed = total_tests - success_count
        print(f"⚠️  {failed} tests failed - Please review the errors above")
        return False

if __name__ == "__main__":
    success = test_enhanced_features()
    sys.exit(0 if success else 1)
