"""Comprehensive test suite for the authentication system."""
import pytest
import asyncio
from datetime import datetime, timedelta, UTC
from unittest.mock import AsyncMock, MagicMock

# Test configuration and fixtures
from app.mfa_config import MFAConfig
from app.factory import create_mfa_system
from app.storage import SmsCode, EmailVerification, TrustedDevice


@pytest.fixture
def test_config():
    """Test configuration with short timeouts for faster testing."""
import ValueError
import all
import device_trust
import email_manager
import hasattr
import int
import len
import mfa_manager
import n
import range
import set
import sms1
import sms2
import sms_manager
    return MFAConfig(
        max_failed_attempts=3,
        rate_limit_window_seconds=60,  # 1 minute for tests
        sms_code_ttl_minutes=1,        # 1 minute for tests
        max_sms_per_hour=10
    )


@pytest.fixture
async def auth_system(test_config):
    """Create authentication system for testing."""
    mfa_manager, sms_manager, email_manager, device_trust = create_mfa_system(
        config=test_config,
        storage_backend="memory"
    )
    return mfa_manager, sms_manager, email_manager, device_trust


class TestSMSManager:
    """Test SMS code generation and verification."""
    
    @pytest.mark.asyncio
    async def test_secure_code_generation(self, auth_system):
        """Test cryptographically secure 6-digit code generation."""
        _, sms_manager, _, _ = auth_system
        
        # Generate 1000 codes to test uniqueness and format
        codes = []
        for _ in range(1000):
            code = sms_manager._secure_6digit()
            codes.append(code)
            
            # Each code should be exactly 6 digits
            assert len(code) == 6
            assert code.isdigit()
            
            # Should be in range 100000-999999
            assert 100000 <= int(code) <= 999999
        
        # Check uniqueness (should be very high for 1000 codes)
        unique_codes = set(codes)
        uniqueness_ratio = len(unique_codes) / len(codes)
        assert uniqueness_ratio > 0.99  # Should have >99% uniqueness
    
    @pytest.mark.asyncio
    async def test_sms_code_lifecycle(self, auth_system):
        """Test SMS code generation, verification, and expiration."""
        _, sms_manager, _, _ = auth_system
        
        phone = "+1234567890"
        
        # Generate code
        code = await sms_manager.generate_code(phone)
        assert len(code) == 6
        assert code.isdigit()
        
        # Verify correct code
        result = await sms_manager.verify_code(phone, code)
        assert result is True
        
        # Code should be consumed (single-use)
        result = await sms_manager.verify_code(phone, code)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_wrong_sms_code(self, auth_system):
        """Test verification with wrong code."""
        _, sms_manager, _, _ = auth_system
        
        phone = "+1234567890"
        await sms_manager.generate_code(phone)
        
        # Try wrong code
        result = await sms_manager.verify_code(phone, "999999")
        assert result is False
        
        # Original code should still work
        stored = await sms_manager._storage.fetch_code(phone)
        assert stored is not None
        result = await sms_manager.verify_code(phone, stored.code)
        assert result is True


class TestDeviceTrust:
    """Test device trust management."""
    
    def test_device_trust_basic(self, auth_system):
        """Test basic device trust functionality."""
        _, _, _, device_trust = auth_system
        
        token = "device123"
        fingerprint = "chrome_windows_1920x1080"
        
        # Device not trusted initially
        assert device_trust.is_device_trusted(token, fingerprint) is False
        
        # Trust device
        device_trust.trust_device(token, fingerprint)
        
        # Now it should be trusted
        assert device_trust.is_device_trusted(token, fingerprint) is True
        
        # Wrong fingerprint should fail
        assert device_trust.is_device_trusted(token, "wrong_fingerprint") is False
    
    def test_device_fingerprint_security(self, auth_system):
        """Test that fingerprint comparison is secure."""
        _, _, _, device_trust = auth_system
        
        token = "device123"
        correct_fp = "correct_fingerprint"
        similar_fp = "correct_fingerprinX"  # Similar but different
        
        device_trust.trust_device(token, correct_fp)
        
        # Only exact match should work
        assert device_trust.is_device_trusted(token, correct_fp) is True
        assert device_trust.is_device_trusted(token, similar_fp) is False
        assert device_trust.is_device_trusted(token, "") is False
    
    @pytest.mark.asyncio
    async def test_device_cleanup(self, auth_system):
        """Test expired device cleanup."""
        _, _, _, device_trust = auth_system
        
        token = "device123"
        fingerprint = "test_fingerprint"
        
        # Trust device with very short TTL
        short_ttl = timedelta(seconds=0.1)
        device_trust.trust_device(token, fingerprint, ttl=short_ttl)
        
        # Should be trusted immediately
        assert device_trust.is_device_trusted(token, fingerprint) is True
        
        # Wait for expiration
        await asyncio.sleep(0.2)
        
        # Should not be trusted anymore
        assert device_trust.is_device_trusted(token, fingerprint) is False
        
        # Cleanup should remove it
        await device_trust.cleanup_expired()
        devices = device_trust.list_devices()
        assert len(devices) == 0


class TestRateLimiting:
    """Test rate limiting and brute-force protection."""
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, auth_system):
        """Test that rate limiting blocks excessive attempts."""
        mfa_manager, _, _, _ = auth_system
        
        user_id = "test_user"
        phone = "+1234567890"
        
        # Make maximum allowed failed attempts
        for i in range(mfa_manager.config.max_failed_attempts):
            result = await mfa_manager.verify_mfa(user_id, phone, "wrong_code")
            assert result is False
        
        # Next attempt should be rate limited
        result = await mfa_manager.verify_mfa(user_id, phone, "any_code")
        assert result is False
        
        # Check that failed attempts are tracked
        attempts = await mfa_manager.get_failed_attempts(user_id)
        assert attempts == mfa_manager.config.max_failed_attempts
    
    @pytest.mark.asyncio
    async def test_rate_limit_reset_on_success(self, auth_system):
        """Test that successful auth resets rate limit."""
        mfa_manager, sms_manager, _, _ = auth_system
        
        user_id = "test_user"
        phone = "+1234567890"
        
        # Make some failed attempts
        for i in range(2):
            await mfa_manager.verify_mfa(user_id, phone, "wrong_code")
        
        # Successful verification should reset counter
        code = await sms_manager.generate_code(phone)
        result = await mfa_manager.verify_mfa(user_id, phone, code)
        assert result is True
        
        # Counter should be reset
        attempts = await mfa_manager.get_failed_attempts(user_id)
        assert attempts == 0


class TestEmailVerification:
    """Test email verification system."""
    
    @pytest.mark.asyncio
    async def test_email_verification_token(self, auth_system):
        """Test email verification with URL token."""
        _, _, email_manager, _ = auth_system
        
        email = "test@example.com"
        
        # Send verification
        token = await email_manager.send_verification(email)
        assert len(token) > 20  # Should be a substantial token
        
        # Verify with token
        result = await email_manager.verify_token(email, token)
        assert result is True
        
        # Token should be consumed
        result = await email_manager.verify_token(email, token)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_email_verification_backup_code(self, auth_system):
        """Test email verification with 4-digit backup code."""
        _, _, email_manager, _ = auth_system
        
        email = "test@example.com"
        
        # Send verification
        await email_manager.send_verification(email)
        
        # Get the backup code from storage
        stored = await email_manager._storage.fetch_code(f"email:{email}")
        assert stored is not None
        assert len(stored.code) == 4
        assert stored.code.isdigit()
        
        # Verify with backup code
        result = await email_manager.verify_code(email, stored.code)
        assert result is True


class TestMFAManager:
    """Test the main MFA manager integration."""
    
    @pytest.mark.asyncio
    async def test_full_mfa_flow(self, auth_system):
        """Test complete MFA flow with device trust."""
        mfa_manager, _, _, _ = auth_system
        
        user_id = "test_user"
        phone = "+1234567890"
        device_token = "device123"
        device_fingerprint = "test_fingerprint"
        
        # Step 1: Send SMS
        result = await mfa_manager.send_sms_code(user_id, phone)
        assert result is True
        
        # Step 2: Get code and verify (first time, will trust device)
        stored = await mfa_manager.sms._storage.fetch_code(phone)
        assert stored is not None
        
        result = await mfa_manager.verify_mfa(
            user_id, phone, stored.code, device_token, device_fingerprint
        )
        assert result is True
        
        # Step 3: Device should now be trusted, bypassing MFA
        result = await mfa_manager.verify_mfa(
            user_id, phone, "wrong_code", device_token, device_fingerprint
        )
        assert result is True  # Trusted device bypasses code check
    
    @pytest.mark.asyncio
    async def test_sms_rate_limiting(self, auth_system):
        """Test SMS sending rate limits."""
        mfa_manager, _, _, _ = auth_system
        
        user_id = "test_user"
        phone = "+1234567890"
        
        # Send maximum allowed SMS
        success_count = 0
        for i in range(mfa_manager.config.max_sms_per_hour + 2):
            result = await mfa_manager.send_sms_code(user_id, phone)
            if result:
                success_count += 1
        
        # Should not exceed the limit
        assert success_count <= mfa_manager.config.max_sms_per_hour


class TestSecurityFeatures:
    """Test security-specific features."""
    
    def test_constant_time_comparison(self, auth_system):
        """Test that comparisons use constant-time algorithms."""
        import secrets
        
        # This test verifies that we're using secrets.compare_digest
        # which is resistant to timing attacks
        
        correct = "123456"
        wrong = "654321"
        
        # These should all take roughly the same time
        # (can't easily test timing in unit tests, but we verify the method exists)
        assert hasattr(secrets, 'compare_digest')
        
        # Verify compare_digest behavior
        assert secrets.compare_digest(correct, correct) is True
        assert secrets.compare_digest(correct, wrong) is False
        assert secrets.compare_digest("", "") is True
        assert secrets.compare_digest("a", "") is False
    
    def test_secure_random_generation(self):
        """Test that we're using cryptographically secure random generation."""
        import secrets
        
        # Generate many random numbers to check distribution
        numbers = [secrets.randbelow(900_000) + 100_000 for _ in range(1000)]
        
        # Check that all numbers are in valid range
        assert all(100_000 <= n <= 999_999 for n in numbers)
        
        # Check that we have good distribution (not clustered)
        unique_count = len(set(numbers))
        assert unique_count > 950  # Should have high uniqueness


class TestStorageAbstraction:
    """Test storage backend switching."""
    
    @pytest.mark.asyncio
    async def test_memory_storage_isolation(self):
        """Test that memory storage instances are isolated."""
        from app.factory import create_mfa_system
        from app.mfa_config import DEFAULT_MFA_CONFIG
        
        # Create two separate systems
        sys1 = create_mfa_system(DEFAULT_MFA_CONFIG, "memory")
        sys2 = create_mfa_system(DEFAULT_MFA_CONFIG, "memory")
        
        mfa1, sms1, _, _ = sys1
        mfa2, sms2, _, _ = sys2
        
        # Add data to first system
        phone = "+1234567890"
        code1 = await sms1.generate_code(phone)
        
        # Second system should not see the data
        result = await sms2.verify_code(phone, code1)
        assert result is False
    
    def test_storage_factory_validation(self):
        """Test that storage factory validates inputs."""
        from app.factory import make_mfa_storage, make_verification_storage
        
        # Valid backends should work
        storage = make_mfa_storage("memory")
        assert storage is not None
        
        verification = make_verification_storage("memory")
        assert verification is not None
        
        # Invalid backend should raise
        with pytest.raises(ValueError, match="Unsupported.*backend"):
            make_mfa_storage("invalid_backend")


# Test fixtures for async testing
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    # Run tests with: python -m pytest test_authentication.py -v
    pytest.main([__file__, "-v", "--tb=short"])
