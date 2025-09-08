from __future__ import annotations

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.aggregates.base import AggregateRoot, DomainEvent, ensure
import chat_id
import content
import dict
import f
import getattr
import len
import list
import metadata
import metadata_updates
import model_name
import namespace
import reason
import self
import str


class MemoryAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for long-term memory items (documents/chunks) & links to chats.

    Supports store/update/soft-delete, embedding request, and linking to threads.
    """

    AGG = "memory"

    def store(
        self, content: str, metadata: dict | None = None, namespace: str | None = None
    ) -> None:
        ensure(content.strip() != "", "content required.")
        current_meta = getattr(self.entity, "metadata", {}) or {}
        current_namespace = getattr(self.entity, "namespace", None)
        self._replace(
            content=content,
            metadata={**current_meta, **(metadata or {})},
            namespace=namespace or current_namespace,
        )
        self._record(DomainEvent.make("MemoryStored", self.AGG, self.id))

    def update(
        self, content: str | None = None, metadata_updates: dict | None = None
    ) -> None:
        if content is None and not metadata_updates:
            return
        current_meta = getattr(self.entity, "metadata", {}) or {}
        current_content = getattr(self.entity, "content", "")
        merged = {**current_meta}
        if metadata_updates:
            merged.update(metadata_updates)
        self._replace(content=content or current_content, metadata=merged)
        self._record(
            DomainEvent.make(
                "MemoryUpdated",
                self.AGG,
                self.id,
                fields=[
                    f
                    for f in ["content", "metadata"]
                    if f
                    in [
                        "content" if content else None,
                        "metadata" if metadata_updates else None,
                    ]
                    and f is not None
                ],
            )
        )

    def soft_delete(self, reason: str | None = None) -> None:
        current_deleted = getattr(self.entity, "deleted", False)
        ensure(not current_deleted, "Already deleted.")
        self._replace(deleted=True)
        self._record(
            DomainEvent.make("MemoryDeleted", self.AGG, self.id, reason=reason or "")
        )

    def link_to_chat(self, chat_id: str) -> None:
        current_links = getattr(self.entity, "links", []) or []
        links = list(current_links)
        if chat_id in links:
            return
        links.append(chat_id)
        self._replace(links=links)
        self._record(
            DomainEvent.make("MemoryLinkedToChat", self.AGG, self.id, chat_id=chat_id)
        )

    def request_embedding(self, model_name: str = "text-embedding") -> None:
        current_content = getattr(self.entity, "content", "")
        self._record(
            DomainEvent.make(
                "MemoryEmbeddingRequested",
                self.AGG,
                self.id,
                model=model_name,
                content_len=len(current_content),
            )
        )
