"""Chat service implementation (migrated from top-level chat_service.py).

This module contains the ChatService implementation and is imported by
`core.services.chat.service` which re-exports the class.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import UUID, uuid4

from apps.backend.core.common.base_classes import BaseService
from apps.backend.core.domain.entities.chat import (
import Exception
import agent_id
import aid
import ascending
import bool
import c
import chat_id
import chat_ids
import chat_repo
import chat_type
import cid
import content
import content_filter
import dict
import filters
import float
import for_update
import getattr
import hard
import include_archived
import int
import isinstance
import len
import limit
import list
import m
import max
import message_repo
import metadata
import min
import new_title
import participants
import pid
import query
import role
import round
import self
import since
import str
import sum
import super
import title
import uid_agent
import uid_user
import uow
import uow_factory
import user_id
    Chat,
    ChatStatus,
    ChatType,
    Message,
    MessageRole,
)
from apps.backend.core.interfaces.repositories import (
    FilterExpr,
    NotFoundError,
    Op,
    OrderBy,
    Page,
    PageRequest,
    Query,
    Repository,
    SearchableRepository,
    SortDir,
    UoWFactory,
)

logger = logging.getLogger(__name__)


class ChatRepository(Repository[Chat, UUID], Protocol):
    pass


class MessageRepository(Repository[Message, UUID], Protocol):
    pass


@dataclass(slots=True)
class ChatStats:
    chat_id: str
    title: str
    total_messages: int
    user_messages: int
    agent_messages: int
    system_messages: int
    avg_message_length: float
    total_characters: int
    duration_seconds: float
    created_at: str
    last_activity: str | None
    participant_count: int
    is_archived: bool


class ChatService(BaseService):
    """Business logic cho chat (async, repository + UoW)."""

    def __init__(
        self,
        *,
        chat_repo: ChatRepository,
        message_repo: MessageRepository,
        uow_factory: UoWFactory,
        content_filter: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__()
        self._chat_repo = chat_repo
        self._message_repo = message_repo
        self._uow_factory = uow_factory
        self._content_filter = content_filter

    # ----------------------- Chat CRUD -----------------------

    async def create_chat(
        self,
        *,
        title: str,
        chat_type: ChatType | str = ChatType.PRIVATE,
        user_id: str | None = None,
        agent_id: str | None = None,
        participants: Sequence[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Chat:
        """Tạo hội thoại mới và thêm participants nếu có."""

        ctype = ChatType(chat_type) if isinstance(chat_type, str) else chat_type

        chat = Chat(
            id=uuid4(),
            title=title,
            type=ctype,
            metadata=metadata or {},
        )

        # Map user/agent to domain fields
        if user_id:
            try:
                UUID(str(user_id))
                chat.user_id = uid_user
                chat.add_participant(uid_user)
            except Exception:
                logger.warning(
                    "Invalid user_id provided for chat creation: %s", user_id
                )
        if agent_id:
            try:
                UUID(str(agent_id))
                chat.update_agent(uid_agent)
                chat.add_agent(uid_agent)
            except Exception:
                logger.warning(
                    "Invalid agent_id provided for chat creation: %s", agent_id
                )

        # Additional participants (UUID strings)
        if participants:
            for pid in participants:
                try:
                    chat.add_participant(UUID(str(pid)))
                except Exception:
                    logger.warning("Invalid participant id ignored: %s", pid)

        async with self._uow_factory() as uow:
            await self._chat_repo.add(chat)
            await uow.commit()

        logger.info("Created chat %s ('%s')", chat.id, title)
        return chat

    async def get_chat(
        self, chat_id: str | UUID, *, for_update: bool = False
    ) -> Chat | None:
        """Lấy hội thoại theo id."""
        uid = UUID(str(chat_id))
        return await self._chat_repo.try_get(uid, for_update=for_update)

    async def update_chat_title(self, chat_id: str | UUID, new_title: str) -> bool:
        """Đổi tiêu đề hội thoại."""
        uid = UUID(str(chat_id))
        chat = await self._chat_repo.try_get(uid, for_update=True)
        if not chat:
            return False

        chat.rename(new_title)
        async with self._uow_factory() as uow:
            await self._chat_repo.update(chat)
            await uow.commit()

        logger.info("Updated title for chat %s", chat_id)
        return True

    async def archive_chat(self, chat_id: str | UUID) -> bool:
        """Đánh dấu lưu trữ hội thoại."""
        uid = UUID(str(chat_id))
        chat = await self._chat_repo.try_get(uid, for_update=True)
        if not chat:
            return False

        chat.archive()
        async with self._uow_factory() as uow:
            await self._chat_repo.update(chat)
            await uow.commit()
        logger.info("Archived chat %s", chat_id)
        return True

    async def restore_chat(self, chat_id: str | UUID) -> bool:
        """Bỏ trạng thái lưu trữ -> ACTIVE."""
        uid = UUID(str(chat_id))
        chat = await self._chat_repo.try_get(uid, for_update=True)
        if not chat:
            return False

        chat.status = ChatStatus.ACTIVE
        async with self._uow_factory() as uow:
            await self._chat_repo.update(chat)
            await uow.commit()
        logger.info("Restored chat %s", chat_id)
        return True

    async def delete_chat(self, chat_id: str | UUID, *, hard: bool = False) -> bool:
        """Xoá hội thoại (soft/hard tuỳ repo)."""
        uid = UUID(str(chat_id))
        async with self._uow_factory() as uow:
            try:
                if hard:
                    await self._chat_repo.delete(uid)
                else:
                    await self._chat_repo.soft_delete(uid)
                await uow.commit()
                logger.info("Deleted chat %s (hard=%s)", chat_id, hard)
                return True
            except NotFoundError:
                return False

    # ----------------------- Listing & Search -----------------------

    async def get_user_chats(
        self,
        user_id: str,
        *,
        page: PageRequest | None = None,
        include_archived: bool = True,
    ) -> Page[Chat]:
        """Lấy danh sách hội thoại của user."""
        page = page or PageRequest(
            page=1, size=50, sort=(OrderBy("last_message_at", SortDir.DESC),)
        )
        q = Query(
            filters=[
                FilterExpr("user_id", Op.EQ, user_id),
            ],
            include_deleted=False,
        )
        if not include_archived:
            q = Query(
                filters=[
                    *q.filters,
                    FilterExpr("status", Op.NE, ChatStatus.ARCHIVED.value),
                ]
            )

        return await self._chat_repo.list(query=q, page=page)

    async def get_recent_chats(
        self, user_id: str, *, limit: int = 10
    ) -> Sequence[Chat]:
        """Danh sách hội thoại gần nhất của user."""
        page = PageRequest(
            page=1, size=limit, sort=(OrderBy("last_message_at", SortDir.DESC),)
        )
        return (await self.get_user_chats(user_id, page=page)).items

    async def search_chats(
        self,
        user_id: str,
        query: str,
        *,
        page: PageRequest | None = None,
    ) -> Page[Chat]:
        """Tìm theo tiêu đề/nội dung với FTS fallback."""
        page = page or PageRequest(page=1, size=20)
        if isinstance(self._chat_repo, SearchableRepository):
            return await self._chat_repo.search(
                query, page=page, scopes=[f"user:{user_id}"]
            )  # type: ignore[arg-type]

        q = Query(
            filters=[
                FilterExpr("user_id", Op.EQ, user_id),
                FilterExpr("title", Op.ILIKE, f"%{query}%"),
            ]
        )
        return await self._chat_repo.list(query=q, page=page)

    # ----------------------- Messages -----------------------

    async def add_message(
        self,
        *,
        chat_id: str | UUID,
        role: MessageRole | str,  # "user" | "agent" | "system"
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Thêm message vào chat, cập nhật last_message_at & đếm."""
        if self._content_filter:
            self._content_filter(content)

        uid = UUID(str(chat_id))
        chat = await self._chat_repo.try_get(uid, for_update=True)
        if not chat:
            raise NotFoundError(f"Chat {chat_id} not found")

        mrole = MessageRole(role) if isinstance(role, str) else role
        message = Message(
            id=uuid4(),
            chat_id=uid,
            role=mrole,
            content=content,
            metadata=metadata or {},
        )

        async with self._uow_factory() as uow:
            await self._message_repo.add(message)
            chat.last_message_at = datetime.now(UTC)
            chat.message_count += 1
            await self._chat_repo.update(chat)
            await uow.commit()

        logger.info("Added %s message to chat %s", mrole.value, chat_id)
        return message

    async def get_chat_messages(
        self,
        chat_id: str | UUID,
        *,
        page: PageRequest | None = None,
        since: datetime | None = None,
        ascending: bool = True,
    ) -> Page[Message]:
        """Lấy danh sách message của chat, hỗ trợ since + sort."""
        uid = UUID(str(chat_id))
        filters: list[FilterExpr] = [FilterExpr("chat_id", Op.EQ, str(uid))]
        if since:
            filters.append(FilterExpr("created_at", Op.GT, since.isoformat()))

        sort_dir = SortDir.ASC if ascending else SortDir.DESC
        page = page or PageRequest(
            page=1, size=100, sort=(OrderBy("created_at", sort_dir),)
        )
        return await self._message_repo.list(query=Query(filters=filters), page=page)

    # ----------------------- Statistics & Export -----------------------

    async def get_chat_statistics(self, chat_id: str | UUID) -> ChatStats | None:
        """Tính thống kê của một chat."""
        uid = UUID(str(chat_id))
        chat = await self._chat_repo.try_get(uid)
        if not chat:
            return None

        msgs_page = await self._message_repo.list(
            query=Query(filters=[FilterExpr("chat_id", Op.EQ, str(uid))]),
            page=PageRequest(page=1, size=10_000),
        )
        messages = msgs_page.items

        user_msgs = [m for m in messages if m.role.value == "user"]
        agent_msgs = [m for m in messages if m.role.value == "agent"]
        system_msgs = [m for m in messages if m.role.value == "system"]

        total_len = sum(len(m.content) for m in messages)
        avg_len = round(total_len / len(messages), 2) if messages else 0.0

        if messages:
            first = min(messages, key=lambda m: m.created_at)
            last = max(messages, key=lambda m: m.created_at)
            duration = (last.created_at - first.created_at).total_seconds()
        else:
            duration = 0.0

        return ChatStats(
            chat_id=str(uid),
            title=chat.title,
            total_messages=len(messages),
            user_messages=len(user_msgs),
            agent_messages=len(agent_msgs),
            system_messages=len(system_msgs),
            avg_message_length=avg_len,
            total_characters=total_len,
            duration_seconds=duration,
            created_at=chat.created_at.isoformat(),
            last_activity=chat.last_message_at.isoformat()
            if chat.last_message_at
            else None,
            participant_count=len(chat.participant_ids),
            is_archived=chat.is_archived(),
        )

    async def get_user_chat_statistics(self, user_id: str) -> dict[str, Any]:
        """Tổng hợp thống kê các chat của một user."""
        page = await self.get_user_chats(
            user_id,
            page=PageRequest(
                page=1, size=1_000, sort=(OrderBy("last_message_at", SortDir.DESC),)
            ),
        )
        chats = page.items

        total_chats = len(chats)
        active = sum(1 for c in chats if c.is_active)
        archived = sum(1 for c in chats if c.is_archived())

        total_messages = sum(getattr(c, "message_count", 0) for c in chats)
        avg_per_chat = round(total_messages / total_chats, 2) if total_chats else 0.0

        return {
            "user_id": user_id,
            "total_chats": total_chats,
            "active_chats": active,
            "archived_chats": archived,
            "total_messages": total_messages,
            "avg_messages_per_chat": avg_per_chat,
        }

    async def export_chat(self, chat_id: str | UUID) -> dict[str, Any]:
        """Xuất toàn bộ dữ liệu chat + messages + statistics."""
        stats = await self.get_chat_statistics(chat_id)
        if stats is None:
            raise NotFoundError(f"Chat {chat_id} not found")

        uid = UUID(str(chat_id))
        chat = await self._chat_repo.get(uid)
        msgs_page = await self._message_repo.list(
            query=Query(filters=[FilterExpr("chat_id", Op.EQ, str(uid))]),
            page=PageRequest(
                page=1, size=10_000, sort=(OrderBy("created_at", SortDir.ASC),)
            ),
        )

        return {
            "chat": {
                "id": str(chat.id),
                "title": chat.title,
                "type": chat.type.value,
                "status": chat.status.value,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat(),
                "last_message_at": chat.last_message_at.isoformat()
                if chat.last_message_at
                else None,
                "message_count": chat.message_count,
                "is_archived": chat.is_archived(),
                "participant_ids": [str(pid) for pid in chat.participant_ids],
                "agent_ids": [str(aid) for aid in chat.agent_ids],
            },
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role.value,
                    "content": m.content,
                    "created_at": m.created_at.isoformat(),
                    "metadata": m.metadata,
                }
                for m in msgs_page.items
            ],
            "statistics": stats.__dict__,
        }

    # ----------------------- Bulk ops -----------------------

    async def bulk_archive_chats(
        self, user_id: str, chat_ids: Sequence[str | UUID]
    ) -> int:
        """Archive nhiều chat (chỉ chat mà user là participant)."""
        count = 0
        async with self._uow_factory() as uow:
            for cid in chat_ids:
                uid = UUID(str(cid))
                chat = await self._chat_repo.try_get(uid, for_update=True)
                if not chat:
                    continue
                try:
                    UUID(str(user_id))
                except Exception:
                    pass  # type: ignore[assignment]
                authorized = (uid_user is not None and chat.user_id == uid_user) or (
                    uid_user is not None and uid_user in chat.participant_ids
                )
                if authorized:
                    chat.archive()
                    await self._chat_repo.update(chat)
                    count += 1
            await uow.commit()
        if count:
            logger.info("Archived %s chats for user %s", count, user_id)
        return count


__all__ = ["ChatService"]
