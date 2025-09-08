from __future__ import annotations

import logging
from datetime import UTC, datetime

from apps.backend.core.domain.entities.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import Exception
import bool
import e
import email
import getattr
import int
import password_hash
import self
import session
import str
import user_id
import username

"""Async database operations cho authentication module.
Module này cung cấp:
- Async user operations với SQLAlchemy
- Connection pooling và session management
- Optimized queries cho auth workflows
"""
logger = logging.getLogger(__name__)


class AuthDatabaseService:
    """Async database service cho authentication operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Lấy user theo ID với async query.
        Args:
            user_id: User ID
        Returns:
            User entity nếu tìm thấy, None nếu không
        """
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                logger.debug("User found by ID", user_id=user_id)
            else:
                logger.warning("User not found by ID", user_id=user_id)
            return user
        except Exception as e:
            logger.error("Error fetching user by ID", user_id=user_id, error=str(e))
            raise

    async def get_user_by_username(self, username: str) -> User | None:
        """Lấy user theo username với async query.
        Args:
            username: Username
        Returns:
            User entity nếu tìm thấy, None nếu không
        """
        try:
            query = select(User).where(User.username == username)
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                logger.debug("User found by username", username=username)
            else:
                logger.debug("User not found by username", username=username)
            return user
        except Exception as e:
            logger.error(
                "Error fetching user by username", username=username, error=str(e)
            )
            raise

    async def get_user_by_email(self, email: str) -> User | None:
        """Lấy user theo email với async query.
        Args:
            email: Email address
        Returns:
            User entity nếu tìm thấy, None nếu không
        """
        try:
            query = select(User).where(User.email == email)
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                logger.debug("User found by email", email=email)
            else:
                logger.debug("User not found by email", email=email)
            return user
        except Exception as e:
            logger.error("Error fetching user by email", email=email, error=str(e))
            raise

    async def update_user_last_login(self, user_id: int) -> bool:
        """Cập nhật thời gian login cuối cùng của user.
        Args:
            user_id: User ID
        Returns:
            True nếu cập nhật thành công, False nếu thất bại
        """
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                logger.warning(
                    "Cannot update last login - user not found", user_id=user_id
                )
                return False
            user.last_login = datetime.now(UTC)
            await self.session.commit()
            logger.info("User last login updated", user_id=user_id)
            return True
        except Exception as e:
            logger.error(
                "Error updating user last login", user_id=user_id, error=str(e)
            )
            await self.session.rollback()
            return False

    async def validate_user_credentials(
        self, username: str, password_hash: str
    ) -> User | None:
        """Validate user credentials với async query.
        Args:
            username: Username
            password_hash: Hashed password
        Returns:
            User entity nếu credentials hợp lệ, None nếu không
        """
        try:
            user = await self.get_user_by_username(username)
            if not user:
                logger.debug(
                    "User not found for credential validation", username=username
                )
                return None
            if user.password_hash != password_hash:
                logger.warning("Invalid password for user", username=username)
                return None
            if not getattr(user, "is_active", True):
                logger.warning("Inactive user attempted login", username=username)
                return None
            logger.info("User credentials validated successfully", username=username)
            return user
        except Exception as e:
            logger.error(
                "Error validating user credentials", username=username, error=str(e)
            )
            return None


def get_auth_db_service(session: AsyncSession) -> AuthDatabaseService:
    """FastAPI dependency để inject AuthDatabaseService.
    Args:
        session: Async SQLAlchemy session
    Returns:
        AuthDatabaseService instance
    """
    return AuthDatabaseService(session)


__all__ = [
    "AuthDatabaseService",
    "get_auth_db_service",
    "logger",
]
