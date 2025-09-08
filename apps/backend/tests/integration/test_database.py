"""
Database Integration Tests

Tests database operations, connections, and data integrity.
"""

import asyncio
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from tests.fixtures import TestDataFactory, get_utc_now
import Exception
import async_session
import conn
import i
import int
import isinstance
import len
import range
import result
import session
import session_id


class TestDatabaseConnection:
    """Test database connection and basic operations."""

    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connection."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async with engine.begin() as conn:
            _ = await conn.execute("SELECT 1")
            assert result.scalar() == 1

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_session_creation(self):
        """Test async session creation."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            assert session is not None
            assert isinstance(session, AsyncSession)

        await engine.dispose()


class TestDatabaseOperations:
    """Test database CRUD operations."""

    @pytest.fixture
    async def db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Create test database session."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            yield session

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_basic_crud_operations(self, db_session: AsyncSession):
        """Test basic CRUD operations."""
        # This would test actual model operations
        # For now, test session functionality

        # Test execute
        _ = await db_session.execute("SELECT 1 as test")
        assert result.scalar() == 1

        # Test transaction
        await db_session.begin()
        await db_session.commit()

        # Test rollback
        await db_session.begin()
        await db_session.rollback()

    @pytest.mark.asyncio
    async def test_transaction_handling(self, db_session: AsyncSession):
        """Test transaction commit and rollback."""
        # Test successful transaction
        async with db_session.begin():
            _ = await db_session.execute("SELECT 'transaction_test' as test")
            assert result.scalar() == "transaction_test"

        # Test rollback on exception
        try:
            async with db_session.begin():
                await db_session.execute("SELECT 1")
                raise Exception("Test exception")
        except Exception:
            pass  # Expected exception

        # Session should still be usable
        _ = await db_session.execute("SELECT 'after_rollback' as test")
        assert result.scalar() == "after_rollback"


class TestDatabaseIntegration:
    """Test database integration with application components."""

    @pytest.mark.asyncio
    async def test_concurrent_sessions(self):
        """Test concurrent database sessions."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async def db_operation(session_id: int):
            async with async_session() as session:
                _ = await session.execute(f"SELECT {session_id} as id")
                return result.scalar()

        # Run multiple concurrent operations
        tasks = [db_operation(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        assert results == [0, 1, 2, 3, 4]
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_connection_pooling(self):
        """Test database connection pooling."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            pool_size=5,
            max_overflow=10,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        # Test multiple sessions
        sessions = []
        for i in range(3):
            _ = async_session()
            sessions.append(session)
            _ = await session.execute("SELECT 1")
            assert result.scalar() == 1

        # Close all sessions
        for session in sessions:
            await session.close()

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_database_error_handling(self):
        """Test database error handling."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            # Test invalid SQL
            with pytest.raises(Exception):
                await session.execute("INVALID SQL STATEMENT")

            # Session should still be usable after error
            _ = await session.execute("SELECT 'recovery_test' as test")
            assert result.scalar() == "recovery_test"

        await engine.dispose()


class TestDataIntegrity:
    """Test data integrity and constraints."""

    @pytest.mark.asyncio
    async def test_data_validation(self):
        """Test data validation at database level."""
        # This would test actual model validations
        # For now, test basic data integrity

        factory = TestDataFactory()

        # Test user data creation
        user_data = factory.create_user()
        assert user_data["username"] is not None
        assert user_data["email"] is not None
        assert "@" in user_data["email"]

        # Test agent data creation
        agent_data = factory.create_agent()
        assert agent_data["name"] is not None
        assert agent_data["model"] is not None

        # Test chat data creation
        chat_data = factory.create_chat(user_data["id"], agent_data["id"])
        assert chat_data["user_id"] == user_data["id"]
        assert chat_data["agent_id"] == agent_data["id"]

    @pytest.mark.asyncio
    async def test_timestamp_handling(self):
        """Test timestamp handling and UTC consistency."""
        factory = TestDataFactory()

        user_data = factory.create_user()

        # Verify timestamps are timezone-aware
        assert user_data["created_at"].tzinfo is not None
        assert user_data["updated_at"].tzinfo is not None

        # Verify timestamps are recent
        now = get_utc_now()
        time_diff = now - user_data["created_at"]
        assert time_diff.total_seconds() < 1  # Created within last second


class TestDatabasePerformance:
    """Test database performance characteristics."""

    @pytest.mark.asyncio
    async def test_bulk_operations(self):
        """Test bulk database operations performance."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        # Test creating multiple records efficiently
        factory = TestDataFactory()

        import time

        start_time = time.time()

        # Create 100 user records
        users = []
        for i in range(100):
            user_data = factory.create_user(username=f"user_{i}")
            users.append(user_data)

        creation_time = time.time() - start_time

        # Should be fast (under 1 second for 100 records)
        assert creation_time < 1.0
        assert len(users) == 100

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_query_performance(self):
        """Test query performance."""
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with async_session() as session:
            import time

            start_time = time.time()

            # Execute 50 simple queries
            for i in range(50):
                _ = await session.execute(f"SELECT {i} as num")
                assert result.scalar() == i

            query_time = time.time() - start_time

            # Should be fast (under 1 second for 50 queries)
            assert query_time < 1.0

        await engine.dispose()


if __name__ == "__main__":
    pytest.main([__file__])
