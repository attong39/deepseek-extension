"""Bootstrap example for setting up the complete authentication system."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, UTC

# Configure logging for demonstration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def demo_authentication_system():
    """Demonstrate the complete authentication system."""
import Exception
import ImportError
import all
import code
import device_trust
import e
import email_manager
import len
import mfa_manager
import print
import range
import set
import sms_manager
    
    # Create complete MFA system with in-memory storage
    from .factory import create_mfa_system
    from .mfa_config import MFAConfig
    
    # Custom configuration
    config = MFAConfig(
        max_failed_attempts=3,
        rate_limit_window_seconds=300,  # 5 minutes
        sms_code_ttl_minutes=3,
        max_sms_per_hour=5
    )
    
    # Create the system (using memory storage for demo)
    mfa_manager, sms_manager, email_manager, device_trust = create_mfa_system(
        config=config,
        storage_backend="memory"
    )
    
    print("🚀 Authentication system initialized!")
    print("=" * 60)
    
    # Demo 1: SMS Code Generation and Verification
    print("\n1️⃣ SMS Code Demo")
    print("-" * 30)
    
    user_id = "user123"
    phone = "+1234567890"
    
    # Send SMS code
    success = await mfa_manager.send_sms_code(user_id, phone)
    print(f"SMS sent: {success}")
    
    # Get the code from storage (in real app, this comes from SMS)
    from .memory_storage import MemoryVerificationStorage
    verification_storage = sms_manager._storage
    stored_sms = await verification_storage.fetch_code(phone)
    if stored_sms:
        test_code = stored_sms.code
        print(f"Generated code: {test_code}")
        
        # Verify correct code
        result = await mfa_manager.verify_mfa(user_id, phone, test_code)
        print(f"Verification result: {result}")
    
    # Demo 2: Device Trust
    print("\n2️⃣ Device Trust Demo")
    print("-" * 30)
    
    device_token = "device_abc123"
    device_fingerprint = "fp_browser_chrome_windows"
    
    # First verification without trusted device
    await mfa_manager.send_sms_code(user_id, phone)
    stored_sms = await verification_storage.fetch_code(phone)
    if stored_sms:
        # Verify and trust device
        result = await mfa_manager.verify_mfa(
            user_id, phone, stored_sms.code, 
            device_token, device_fingerprint
        )
        print(f"First verification (device will be trusted): {result}")
    
    # Second verification with trusted device (should bypass MFA)
    result = await mfa_manager.verify_mfa(
        user_id, phone, "wrong_code",  # Wrong code, but device is trusted
        device_token, device_fingerprint
    )
    print(f"Second verification (trusted device): {result}")
    
    # Demo 3: Rate Limiting
    print("\n3️⃣ Rate Limiting Demo")
    print("-" * 30)
    
    new_user = "user456"
    attempts = 0
    for i in range(5):
        result = await mfa_manager.verify_mfa(new_user, phone, "wrong_code")
        attempts += 1
        print(f"Attempt {attempts}: {result}")
        if not result and attempts >= config.max_failed_attempts:
            print("Rate limit should kick in now...")
            break
    
    # This should be rate limited
    result = await mfa_manager.verify_mfa(new_user, phone, "any_code")
    print(f"Rate limited attempt: {result}")
    
    # Demo 4: Email Verification
    print("\n4️⃣ Email Verification Demo")
    print("-" * 30)
    
    email = "user@example.com"
    token = await email_manager.send_verification(email)
    print(f"Email verification token generated: {token[:16]}...")
    
    # Get verification data
    stored_email = await verification_storage.fetch_code(f"email:{email}")
    if stored_email:
        print(f"Backup code: {stored_email.code}")
        
        # Verify with backup code
        result = await email_manager.verify_code(email, stored_email.code)
        print(f"Email verified with backup code: {result}")
    
    # Demo 5: Cleanup
    print("\n5️⃣ Cleanup Demo")
    print("-" * 30)
    
    print("Devices before cleanup:", len(device_trust.list_devices()))
    await mfa_manager.cleanup_expired_data()
    print("Cleanup completed")
    
    # Demo 6: Security Features
    print("\n6️⃣ Security Features Demo")
    print("-" * 30)
    
    # Show cryptographically secure code generation
    codes = [sms_manager._secure_6digit() for _ in range(10)]
    print(f"10 secure codes: {codes}")
    print(f"All 6 digits: {all(len(code) == 6 and code.isdigit() for code in codes)}")
    print(f"All different: {len(set(codes)) == len(codes)}")
    
    print("\n✅ Authentication system demo completed!")
    return mfa_manager, sms_manager, email_manager, device_trust


async def demo_with_redis():
    """Demo with Redis backend (requires redis server running)."""
    try:
        import aioredis
        
        # Connect to Redis
        redis = await aioredis.from_url("redis://localhost:6379")
        
        from .factory import create_mfa_system
        from .mfa_config import DEFAULT_MFA_CONFIG
        
        # Create system with Redis backend
        mfa_manager, sms_manager, email_manager, device_trust = create_mfa_system(
            config=DEFAULT_MFA_CONFIG,
            storage_backend="redis",
            redis_client=redis
        )
        
        print("🔴 Redis-backed authentication system created!")
        
        # Test basic functionality
        user_id = "redis_user"
        phone = "+9876543210"
        
        success = await mfa_manager.send_sms_code(user_id, phone)
        print(f"Redis SMS sent: {success}")
        
        await redis.aclose()
        
    except ImportError:
        print("⚠️  aioredis not installed, skipping Redis demo")
    except Exception as e:
        print(f"⚠️  Redis demo failed: {e}")


def create_production_system():
    """Example of creating production-ready system."""
    
    # This would be your actual production bootstrap
    production_config = """
    # In your production app (e.g., FastAPI startup)
    
    import asyncio
    import aioredis
    from core.security.authentication import create_mfa_system, MFAConfig
    
    async def setup_auth():
        # Production configuration
        config = MFAConfig(
            max_failed_attempts=5,
            rate_limit_window_seconds=900,  # 15 minutes
            device_trust_ttl_days=30,
            device_inactive_ttl_days=7,
            sms_code_ttl_minutes=5,
            max_sms_per_hour=3,
            email_verification_ttl_hours=24,
            log_security_events=True,
            structured_logging=True
        )
        
        # Redis connection
        redis = await aioredis.from_url(
            "redis://your-redis-host:6379",
            encoding="utf-8",
            decode_responses=True
        )
        
        # Create production system
        mfa_manager, sms_manager, email_manager, device_trust = create_mfa_system(
            config=config,
            storage_backend="redis",
            redis_client=redis
        )
        
        # Schedule background cleanup
        async def background_cleanup():
            while True:
                await mfa_manager.cleanup_expired_data()
                await asyncio.sleep(3600)  # Every hour
        
        asyncio.create_task(background_cleanup())
        
        return mfa_manager, sms_manager, email_manager, device_trust
    
    # Use in your FastAPI dependency injection:
    # app.dependency_overrides[MFAManager] = lambda: mfa_manager
    """
    
    print("📋 Production setup example:")
    print(production_config)


if __name__ == "__main__":
    # Run demos
    asyncio.run(demo_authentication_system())
    print("\n" + "=" * 60)
    asyncio.run(demo_with_redis())
    print("\n" + "=" * 60)
    create_production_system()
