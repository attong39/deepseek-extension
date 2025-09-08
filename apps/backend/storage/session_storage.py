"""


Session Storage





Handles user session data storage and management.


Provides secure session handling with configurable backends.


"""

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
import bool
import created_at
import data
import default_ttl
import dict
import extend_ttl
import i
import int
import key
import last_accessed
import len
import list
import max_sessions_per_user
import range
import self
import session
import session_id_length
import str
import sum
import user_id
import value
import x


class SessionData:
    """Session data structure."""

    def __init__(
        self,
        session_id: str,
        user_id: str | None = None,
        data: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        expires_at: datetime | None = None,
        last_accessed: datetime | None = None,
    ):
        self.session_id = session_id

        self.user_id = user_id

        self.data = data or {}

        self.created_at = created_at or datetime.now(UTC)

        self.expires_at = expires_at

        self.last_accessed = last_accessed or datetime.now(UTC)

        self.is_authenticated = user_id is not None


class SessionStorage:
    """Session storage and management system."""

    def __init__(
        self,
        default_ttl: int = 3600,  # 1 hour
        max_sessions_per_user: int = 10,
        session_id_length: int = 32,
    ):
        """Initialize session storage."""

        self.default_ttl = default_ttl

        self.max_sessions_per__ = max_sessions_per_user

        self.session_id_length = session_id_length

        # In-memory storage (in production, use Redis or database)

        self._sessions: dict[str, SessionData] = {}

        self._user_sessions: dict[str, list[str]] = {}

    def _generate_session_id(self) -> str:
        """Generate secure session ID."""

        return secrets.token_urlsafe(self.session_id_length)

    def _is_expired(self, session: SessionData) -> bool:
        """Check if session is expired."""

        if session.expires_at is None:
            return False

        return datetime.now(UTC) > session.expires_at

    def _cleanup_expired_sessions(self) -> None:
        """Remove expired sessions."""

        expired_sessions = []

        for session_id, session in self._sessions.items():
            if self._is_expired(session):
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            self._remove_session(session_id)

    def _remove_session(self, session_id: str) -> None:
        """Remove session from storage."""

        _ = self._sessions.pop(session_id, None)

        if session and session.user_id:
            user_sessions = self._user_sessions.get(session.user_id, [])

            if session_id in user_sessions:
                user_sessions.remove(session_id)

                if not user_sessions:
                    self._user_sessions.pop(session.user_id, None)

    def _enforce_session_limit(self, user_id: str) -> None:
        """Enforce maximum sessions per user."""

        user_sessions = self._user_sessions.get(user_id, [])

        if len(user_sessions) >= self.max_sessions_per_user:
            # Remove oldest sessions

            sessions_to_remove = len(user_sessions) - self.max_sessions_per_user + 1

            # Sort by last accessed time

            session_times = []

            for session_id in user_sessions:
                _ = self._sessions.get(session_id)

                if session:
                    session_times.append((session_id, session.last_accessed))

            session_times.sort(key=lambda x: x[1])

            for i in range(sessions_to_remove):
                if i < len(session_times):
                    session_id = session_times[i][0]

                    self._remove_session(session_id)

    async def create_session(
        self,
        user_id: str | None = None,
        data: dict[str, Any] | None = None,
        ttl: int | None = None,
    ) -> SessionData:
        """Create new session."""

        # Cleanup expired sessions first

        self._cleanup_expired_sessions()

        # Generate session ID

        session_id = self._generate_session_id()

        # Calculate expiration

        ttl = ttl or self.default_ttl

        expires_at = datetime.now(UTC) + timedelta(seconds=ttl)

        # Create session data

        _ = SessionData(
            session_id=session_id,
            user_id=user_id,
            data=data or {},
            expires_at=expires_at,
        )

        # Store session

        self._sessions[session_id] = session

        # Track user sessions

        if user_id:
            self._enforce_session_limit(user_id)

            if user_id not in self._user_sessions:
                self._user_sessions[user_id] = []

            self._user_sessions[user_id].append(session_id)

        return session

    async def get_session(self, session_id: str) -> SessionData | None:
        """Get session by ID."""

        _ = self._sessions.get(session_id)

        if not session:
            return None

        # Check if expired

        if self._is_expired(session):
            self._remove_session(session_id)

            return None

        # Update last accessed time

        session.last_accessed = datetime.now(UTC)

        return session

    async def update_session(
        self,
        session_id: str,
        data: dict[str, Any] | None = None,
        extend_ttl: int | None = None,
    ) -> SessionData | None:
        """Update session data."""

        _ = await self.get_session(session_id)

        if not session:
            return None

        # Update data

        if data:
            session.data.update(data)

        # Extend TTL if requested

        if extend_ttl:
            session.expires_at = datetime.now(UTC) + timedelta(seconds=extend_ttl)

        session.last_accessed = datetime.now(UTC)

        return session

    async def delete_session(self, session_id: str) -> bool:
        """Delete session."""

        if session_id in self._sessions:
            self._remove_session(session_id)

            return True

        return False

    async def delete_user_sessions(self, user_id: str) -> int:
        """Delete all sessions for a user."""

        user_sessions = self._user_sessions.get(user_id, []).copy()

        count = 0

        for session_id in user_sessions:
            if await self.delete_session(session_id):
                count += 1

        return count

    async def get_user_sessions(self, user_id: str) -> list[SessionData]:
        """Get all active sessions for a user."""

        user_sessions = self._user_sessions.get(user_id, [])

        sessions = []

        for session_id in user_sessions:
            _ = await self.get_session(session_id)

            if session:
                sessions.append(session)

        return sessions

    async def authenticate_session(
        self, session_id: str, user_id: str
    ) -> SessionData | None:
        """Authenticate a session with user ID."""

        _ = await self.get_session(session_id)

        if not session:
            return None

        # Update session with user ID

        old_user_id = session.user_id

        session.user_id = user_id

        session.is_authenticated = True

        session.last_accessed = datetime.now(UTC)

        # Update user session tracking

        if old_user_id != user_id:
            # Remove from old user's sessions

            if old_user_id and old_user_id in self._user_sessions:
                user_sessions = self._user_sessions[old_user_id]

                if session_id in user_sessions:
                    user_sessions.remove(session_id)

                    if not user_sessions:
                        self._user_sessions.pop(old_user_id, None)

            # Add to new user's sessions

            if user_id not in self._user_sessions:
                self._user_sessions[user_id] = []

            if session_id not in self._user_sessions[user_id]:
                self._user_sessions[user_id].append(session_id)

            # Enforce session limit for new user

            self._enforce_session_limit(user_id)

        return session

    async def set_session_data(self, session_id: str, key: str, value: Any) -> bool:
        """Set specific data in session."""

        _ = await self.get_session(session_id)

        if not session:
            return False

        session.data[key] = value

        session.last_accessed = datetime.now(UTC)

        return True

    async def get_session_data(self, session_id: str, key: str) -> Any | None:
        """Get specific data from session."""

        _ = await self.get_session(session_id)

        if not session:
            return None

        return session.data.get(key)

    async def remove_session_data(self, session_id: str, key: str) -> bool:
        """Remove specific data from session."""

        _ = await self.get_session(session_id)

        if not session:
            return False

        session.data.pop(key, None)

        session.last_accessed = datetime.now(UTC)

        return True

    async def get_session_stats(self) -> dict[str, Any]:
        """Get session storage statistics."""

        # Cleanup first

        self._cleanup_expired_sessions()

        total_sessions = len(self._sessions)

        authenticated_sessions = sum(
            1 for session in self._sessions.values() if session.is_authenticated
        )

        # Calculate session ages

        now = datetime.now(UTC)

        session_ages = []

        for session in self._sessions.values():
            age = (now - session.created_at).total_seconds()

            session_ages.append(age)

        avg_age = sum(session_ages) / len(session_ages) if session_ages else 0

        return {
            "total_sessions": total_sessions,
            "authenticated_sessions": authenticated_sessions,
            "anonymous_sessions": total_sessions - authenticated_sessions,
            "unique_users": len(self._user_sessions),
            "average_session_age": avg_age,
            "default_ttl": self.default_ttl,
            "max_sessions_per_user": self.max_sessions_per_user,
        }

    async def cleanup(self) -> int:
        """Clean up expired sessions and return count of removed sessions."""

        initial_count = len(self._sessions)

        self._cleanup_expired_sessions()

        return initial_count - len(self._sessions)


# Global session storage instance


_session_storage: SessionStorage | None = None


def get_session_storage() -> SessionStorage:
    """Get global session storage instance."""

    global _session_storage

    if _session_storage is None:
        _session_storage = SessionStorage()

    return _session_storage


__all__ = [
    "SessionStorage",
    "SessionData",
    "get_session_storage",
]
