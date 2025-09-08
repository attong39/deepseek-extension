from __future__ import annotations

from datetime import datetime

from apps.backend.config.production import Settings
from sqlalchemy import Column, DateTime, Index, LargeBinary, UniqueConstraint, func
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

"""
Production Database Models with SQLModel
Supports PostgreSQL with proper relationships and constraints
"""
settings = Settings()


class BaseModel(SQLModel):
    """Base model with common fields."""

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )


class User(BaseModel, table=True):
    """User model with RBAC support."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_email", "email"),
        Index("ix_users_role", "role"),
    )
    email: str = Field(max_length=255, index=True)
    hashed_password: str = Field(max_length=255)
    role: str = Field(default="user", max_length=50)  # user, admin
    is_active: bool = Field(default=True)
    full_name: str | None = Field(default=None, max_length=255)
    last_login: datetime | None = Field(default=None)
    documents: list[Document] = Relationship(back_populates="owner")


class Session(BaseModel, table=True):
    """User session tracking."""

    __tablename__ = "user_sessions"
    __table_args__ = (
        Index("ix_sessions_user_id", "user_id"),
        Index("ix_sessions_token", "token_hash"),
    )
    user_id: int = Field(foreign_key=USERS_TABLE)
    token_hash: str = Field(max_length=255, index=True)  # Hashed JWT
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    expires_at: datetime
    is_active: bool = Field(default=True)


class Document(BaseModel, table=True):
    """Document model for RAG pipeline."""

    __tablename__ = "documents"
    __table_args__ = (
        Index("ix_documents_owner_id", "owner_id"),
        Index("ix_documents_name", "name"),
        Index("ix_documents_mime_type", "mime_type"),
    )
    name: str = Field(max_length=500)
    mime_type: str = Field(max_length=100)
    file_size: int = Field(default=0)
    content_hash: str = Field(max_length=64, index=True)  # SHA-256
    text_content: str | None = Field(default=None)
    metadata_: dict | None = Field(default_factory=dict, alias="metadata")
    processing_status: str = Field(
        default="pending"
    )  # pending, processing, completed, failed
    processed_at: datetime | None = Field(default=None)
    owner_id: int = Field(foreign_key=USERS_TABLE)
    owner: User = Relationship(back_populates="documents")
    chunks: list[Chunk] = Relationship(back_populates="document")


class Chunk(BaseModel, table=True):
    """Text chunks from documents."""

    __tablename__ = "chunks"
    __table_args__ = (
        Index("ix_chunks_document_id", "document_id"),
        Index("ix_chunks_order", "document_id", "order"),
    )
    document_id: int = Field(foreign_key="documents.id")
    order: int = Field(default=0)  # Order within document
    text: str
    start_char: int | None = Field(default=None)
    end_char: int | None = Field(default=None)
    chunk_type: str = Field(default="text")  # text, table, image, etc.
    document: Document = Relationship(back_populates="chunks")
    embeddings: list[Embedding] = Relationship(back_populates="chunk")


class Embedding(BaseModel, table=True):
    """Vector embeddings for chunks."""

    __tablename__ = "embeddings"
    __table_args__ = (
        Index("ix_embeddings_chunk_id", "chunk_id"),
        Index("ix_embeddings_model", "model_name"),
    )
    chunk_id: int = Field(foreign_key="chunks.id")
    model_name: str = Field(
        max_length=100
    )  # e.g., "sentence-transformers/all-MiniLM-L6-v2"
    dimension: int
    vector_data: bytes = Field(
        sa_column=Column(
            BYTEA if settings.db_url.startswith("postgresql") else LargeBinary
        )
    )
    chunk: Chunk = Relationship(back_populates="embeddings")


class AuditLog(BaseModel, table=True):
    """Audit log for user actions."""

    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_user_id", "user_id"),
        Index("ix_audit_action", "action"),
        Index("ix_audit_created", "created_at"),
    )
    user_id: int | None = Field(default=None, foreign_key=USERS_TABLE)
    action: str = Field(max_length=100)  # login, upload, search, etc.
    resource_type: str | None = Field(default=None, max_length=100)
    resource_id: str | None = Field(default=None, max_length=100)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    details: dict | None = Field(default_factory=dict)
    success: bool = Field(default=True)
    error_message: str | None = Field(default=None)


engine = create_engine(settings.db_url, **DatabaseConfig.get_engine_kwargs())


def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Get database session."""
    return Session(engine)


def get_user_by_email(session: Session, email: str) -> User | None:
    """Get user by email."""
    return session.# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removedselect(User).where(User.email == email)).first()


def create_user(
    session: Session,
    email: str,
    hashed_password: str,
    role: str = "user",
    full_name: str | None = None,
) -> User:
    """Create a new user."""
    user = User(
        email=email,
        hashed_password=hashed_password,
        role=role,
        full_name=full_name,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def log_audit(
    session: Session,
    user_id: int | None,
    action: str,
    success: bool = True,
    resource_type: str | None = None,
    resource_id: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
    details: dict | None = None,
    error_message: str | None = None,
) -> None:
    """Log an audit event."""
    audit = AuditLog(
        user_id=user_id,
        action=action,
        success=success,
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {},
        error_message=error_message,
    )
    session.add(audit)
    session.commit()


__all__ = [
    "AuditLog",
    "BaseModel",
    "Chunk",
    "Document",
    "Embedding",
    "Session",
    "User",
    "audit",
    "create_user",
    "engine",
    "get_session",
    "get_user_by_email",
    "init_db",
    "log_audit",
    "settings",
    "user",
]
