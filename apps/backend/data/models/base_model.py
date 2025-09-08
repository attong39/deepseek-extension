"""


Base Database Model.





Provides common fields and functionality for all database models.


"""

import uuid
from datetime import UTC, datetime
from typing import Any

# Use the canonical Declarative Base from `data.models.base` to ensure all
# models register on the same metadata. This prevents foreign-key errors when
# creating tables (previously this file created a separate Base via
# declarative_base()).
from apps.backend.data.models.base import Base  # noqa: E402
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func
import TypeError
import ValueError
import action
import bool
import classmethod
import cls
import column
import data
import details
import dict
import getattr
import hasattr
import int
import isinstance
import key
import len
import list
import property
import restored_by
import result
import self
import setattr
import str
import tag
import user_id


class BaseModel(Base):
    """Base model with common fields for all entities.

    NOTE: This class now inherits from the shared `Base` declared in
    `zeta_vn.data.models.base` so that all models share the same
    SQLAlchemy metadata and engine/session initialization.
    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Generate table name from class name."""

        return cls.__name__.lower() + "s"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
        doc="Unique identifier",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Creation timestamp",
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Last update timestamp",
    )

    created_by = Column(
        String(36), nullable=True, doc="User ID who created this record"
    )

    updated_by = Column(
        String(36), nullable=True, doc="User ID who last updated this record"
    )

    version = Column(
        String(50),
        nullable=True,
        default="1.0.0",
        doc="Record version for optimistic locking",
    )

    metadata_json = Column(
        Text, nullable=True, doc="Additional metadata in JSON format"
    )

    def to_dict(self, exclude_fields: list | None = None) -> dict[str, Any]:
        """


        Convert model instance to dictionary.





        Args:


            exclude_fields: Fields to exclude from output





        Returns:


            Dictionary representation of the model


        """

        exclude_fields = exclude_fields or []

        _ = {}

        for column in self.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(self, column.name)

                # Handle datetime serialization

                if isinstance(value, datetime):
                    value = value.isoformat()

                result[column.name] = value

        return result

    def update_from_dict(
        self, data: dict[str, Any], exclude_fields: list | None = None
    ) -> None:
        """


        Update model instance from dictionary.





        Args:


            data: Data to update from


            exclude_fields: Fields to exclude from update


        """

        exclude_fields = exclude_fields or ["id", "created_at", "created_by"]

        for key, value in data.items():
            if hasattr(self, key) and key not in exclude_fields and value is not None:
                setattr(self, key, value)

        # Update the updated_at timestamp

        self.updated_at = datetime.now(UTC)

    @classmethod
    def get_column_names(cls) -> list:
        """


        Get list of column names for this model.





        Returns:


            List of column names


        """

        return [column.name for column in cls.__table__.columns]

    @classmethod
    def get_required_fields(cls) -> list:
        """


        Get list of required (non-nullable) fields.





        Returns:


            List of required field names


        """

        return [
            column.name
            for column in cls.__table__.columns
            if not column.nullable
            and column.default is None
            and column.server_default is None
        ]

    def __repr__(self) -> str:
        """String representation of the model."""

        return f"<{self.__class__.__name__}(id={self.id})>"

    def __str__(self) -> str:
        """String representation of the model."""

        return self.__repr__()


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    deleted_at = Column(
        DateTime(timezone=True), nullable=True, doc="Soft delete timestamp"
    )

    deleted_by = Column(
        String(36), nullable=True, doc="User ID who deleted this record"
    )

    def soft_delete(self, deleted_by: str | None = None) -> None:
        """


        Soft delete the record.





        Args:


            deleted_by: User ID performing the deletion


        """

        self.deleted_at = datetime.now(UTC)

        self.deleted_by = deleted_by

        self.updated_at = datetime.now(UTC)

        self.updated_by = deleted_by

    def restore(self, restored_by: str | None = None) -> None:
        """


        Restore a soft deleted record.





        Args:


            restored_by: User ID performing the restoration


        """

        self.deleted_at = None

        self.deleted_by = None

        self.updated_at = datetime.now(UTC)

        self.updated_by = restored_by

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted."""

        return self.deleted_at is not None


class AuditMixin:
    """Mixin for audit trail functionality."""

    audit_log = Column(Text, nullable=True, doc="Audit log in JSON format")

    def add_audit_entry(
        self,
        action: str,
        user_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """


        Add an audit log entry.





        Args:


            action: Action performed


            user_id: User ID performing the action


            details: Additional details about the action


        """

        import json

        audit_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "action": action,
            "user_id": user_id,
            "details": details or {},
        }

        if self.audit_log:
            try:
                audit_list = json.loads(self.audit_log)

            except json.JSONDecodeError:
                audit_list = []

        else:
            audit_list = []

        audit_list.append(audit_entry)

        # Keep only last 100 entries

        if len(audit_list) > 100:
            audit_list = audit_list[-100:]

        self.audit_log = json.dumps(audit_list)

    def get_audit_entries(self) -> list:
        """


        Get audit log entries.





        Returns:


            List of audit entries


        """

        import json

        if not self.audit_log:
            return []

        try:
            return json.loads(self.audit_log)

        except json.JSONDecodeError:
            return []


class TimestampMixin:
    """Mixin for additional timestamp fields."""

    first_accessed_at = Column(
        DateTime(timezone=True), nullable=True, doc="First access timestamp"
    )

    last_accessed_at = Column(
        DateTime(timezone=True), nullable=True, doc="Last access timestamp"
    )

    access_count = Column(
        String(10), nullable=True, default="0", doc="Number of times accessed"
    )

    def track_access(self) -> None:
        """Track access to this record."""

        now = datetime.now(UTC)

        if not self.first_accessed_at:
            self.first_accessed_at = now

        self.last_accessed_at = now

        try:
            count = int(self.access_count or "0")

            self.access_count = str(count + 1)

        except (ValueError, TypeError):
            self.access_count = "1"


class VersionedMixin:
    """Mixin for record versioning."""

    version_number = Column(
        String(10), nullable=False, default="1", doc="Version number"
    )

    parent_version_id = Column(String(36), nullable=True, doc="ID of parent version")

    is_current_version = Column(
        String(5),
        nullable=False,
        default="true",
        doc="Whether this is the current version",
    )

    def create_new_version(self) -> "VersionedMixin":
        """


        Create a new version of this record.





        Returns:


            New version instance


        """

        # Mark current version as not current

        self.is_current_version = "false"

        # Create new version

        new_version = self.__class__()

        # Copy all attributes except versioning fields

        for column in self.__table__.columns:
            if column.name not in [
                "id",
                "version_number",
                "parent_version_id",
                "is_current_version",
                "created_at",
            ]:
                setattr(new_version, column.name, getattr(self, column.name))

        # Set versioning fields

        try:
            current_version = int(self.version_number)

            new_version.version_number = str(current_version + 1)

        except (ValueError, TypeError):
            new_version.version_number = "2"

        new_version.parent_version_id = self.id

        new_version.is_current_version = "true"

        new_version.id = str(uuid.uuid4())

        return new_version


class TaggedMixin:
    """Mixin for tagging functionality."""

    tags = Column(Text, nullable=True, doc="Tags in JSON array format")

    def add_tag(self, tag: str) -> None:
        """


        Add a tag to the record.





        Args:


            tag: Tag to add


        """

        import json

        current_tags = self.get_tags()

        if tag not in current_tags:
            current_tags.append(tag.strip().lower())

            self.tags = json.dumps(current_tags)

    def remove_tag(self, tag: str) -> None:
        """


        Remove a tag from the record.





        Args:


            tag: Tag to remove


        """

        import json

        current_tags = self.get_tags()

        if tag in current_tags:
            current_tags.remove(tag.strip().lower())

            self.tags = json.dumps(current_tags)

    def get_tags(self) -> list:
        """


        Get list of tags.





        Returns:


            List of tags


        """

        import json

        if not self.tags:
            return []

        try:
            return json.loads(self.tags)

        except json.JSONDecodeError:
            return []

    def has_tag(self, tag: str) -> bool:
        """


        Check if record has a specific tag.





        Args:


            tag: Tag to check





        Returns:


            True if tag exists


        """

        return tag.strip().lower() in self.get_tags()


# Combined model with all mixins


class FullFeaturedBaseModel(
    BaseModel, SoftDeleteMixin, AuditMixin, TimestampMixin, TaggedMixin
):
    """Base model with all available mixins."""

    __abstract__ = True
