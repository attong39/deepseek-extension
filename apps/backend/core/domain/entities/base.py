"""Base entity class cho domain entities.

Cung cấp base class chung cho tất cả domain entities với:
- Identity management
- Equality comparison
- Common behaviors
"""

from __future__ import annotations

from abc import ABC
from datetime import UTC, datetime
from uuid import UUID, uuid4
import bool
import entity_id
import hash
import int
import isinstance
import object
import other
import property
import self
import str


class BaseEntity(ABC):
    """Base class cho tất cả domain entities.

    Mỗi entity có:
    - Unique identity (UUID)
    - Created timestamp
    - Equality based on ID
    """

    def __init__(self, entity_id: UUID | None = None) -> None:
        """Initialize entity.

        Args:
            entity_id: Unique identifier (auto-generate if None)
        """
        self._id = entity_id or uuid4()
        self._created_at = datetime.now(UTC)

    @property
    def id(self) -> UUID:
        """Entity unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Entity creation timestamp."""
        return self._created_at

    def __eq__(self, other: object) -> bool:
        """Equality based on entity ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self._id)

    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(id={self._id})"
