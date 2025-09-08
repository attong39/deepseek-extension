from __future__ import annotations

from app._base_model import DomainModel
from .base import AggregateRoot, DomainEvent, ensure
import bool
import dict
import getattr
import owner_user_id
import participants
import role
import self
import str
import title
import user_id


class CollabRoomAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for realtime collaboration rooms around a chat/thread.

    Tracks participants (user_id -> role), room state (active/archived).
    """

    AGG = "collab_room"

    def create_room(self, title: str, owner_user_id: str) -> None:
        ensure(title.strip() != "", "Room title required.")
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        meta["room"] = {"title": title, "owner": owner_user_id, "active": True}
        meta["participants"] = {owner_user_id: "owner"}
        self._replace(metadata=meta)
        self._record(DomainEvent.make("RoomCreated", self.AGG, self.id, title=title))

    def join(self, user_id: str, role: str = "member") -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        participants: dict[str, str] = dict(meta.get("participants", {}))
        ensure(meta.get("room", {}).get("active", False), "Room not active.")
        ensure(user_id not in participants, "Already joined.")
        participants[user_id] = role
        meta["participants"] = participants
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make(
                "RoomParticipantJoined", self.AGG, self.id, user_id=user_id
            )
        )

    def leave(self, user_id: str) -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        participants: dict[str, str] = dict(meta.get("participants", {}))
        ensure(user_id in participants, "Participant not in room.")
        participants.pop(user_id)
        meta["participants"] = participants
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make("RoomParticipantLeft", self.AGG, self.id, user_id=user_id)
        )

    def archive(self) -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        ensure(bool(meta.get("room")), "Room metadata missing.")
        ensure(meta["room"].get("active", False), "Room already archived.")
        meta["room"]["active"] = False
        self._replace(metadata=meta)
        self._record(DomainEvent.make("RoomArchived", self.AGG, self.id))
