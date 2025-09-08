from __future__ import annotations

from datetime import datetime

from apps.backend.config.production import Settings
from sqlalchemy import Column, LargeBinary, Text
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

"""
Production Database Models - Clean SQLModel Implementation
Avoids SQLAlchemy conflicts and reserved table names
"""
settings = Settings()


class User(SQLModel, table=True):
    """User model with RBAC support."""

    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, index=True, unique=True)
    hashed_password: str = Field(max_length=255)
    role: str = Field(default="user", max_length=50, index=True)
    is_active: bool = Field(default=True)
    full_name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime | None = Field(default=None)
    documents: list[Document] = Relationship(back_populates="owner")


class Document(SQLModel, table=True):
    """Document model for RAG pipeline."""

    __tablename__ = "documents"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=500, index=True)
    mime_type: str = Field(max_length=100, index=True)
    file_size: int = Field(default=0)
    text_content: str | None = Field(default=None, sa_column=Column(Text))
    processing_status: str = Field(default="pending", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: datetime | None = Field(default=None)
    owner_id: int = Field(foreign_key="users.id", index=True)
    owner: User = Relationship(back_populates="documents")
    chunks: list[Chunk] = Relationship(back_populates="document")


class Chunk(SQLModel, table=True):
    """Text chunks from documents."""

    __tablename__ = "chunks"
    id: int | None = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="documents.id", index=True)
    order: int = Field(default=0, index=True)
    text: str = Field(sa_column=Column(Text))
    start_char: int | None = Field(default=None)
    end_char: int | None = Field(default=None)
    chunk_type: str = Field(default="text", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    document: Document = Relationship(back_populates="chunks")
    embeddings: list[Embedding] = Relationship(back_populates="chunk")


class Embedding(SQLModel, table=True):
    """Vector embeddings for chunks."""

    __tablename__ = "embeddings"
    id: int | None = Field(default=None, primary_key=True)
    chunk_id: int = Field(foreign_key="chunks.id", index=True)
    dimension: int = Field(index=True)
    vector_data: bytes = Field(sa_column=Column(LargeBinary))
    model_name: str = Field(max_length=100, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    chunk: Chunk = Relationship(back_populates="embeddings")


class AuditLog(SQLModel, table=True):
    """Audit logging for security events."""

    __tablename__ = "audit_logs"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    action: str = Field(max_length=100, index=True)
    success: bool = Field(index=True)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    details: str | None = Field(default=None, sa_column=Column(Text))  # JSON as Text
    error_message: str | None = Field(default=None, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class UserSession(SQLModel, table=True):
    """User session tracking."""

    __tablename__ = "user_sessions"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    token_hash: str = Field(max_length=255, index=True)
    ip_address: str | None = Field(default=None, max_length=45)
    user_agent: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    last_activity: datetime | None = Field(default=None)
    is_active: bool = Field(default=True)


def create_engine_for_url(database_url: str):
    """Create SQLAlchemy engine for given database URL."""
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(
        database_url,
        connect_args=connect_args,
        echo=settings.debug,
        pool_pre_ping=True,
    )


def create_db_and_tables(engine=None):
    """Create database tables."""
    if engine is None:
        engine = create_engine_for_url(settings.database_url)
    SQLModel.metadata.create_all(engine)


def get_db_engine():
    """Get database engine."""
    return create_engine_for_url(settings.database_url)


def get_db_session():
    """Get database session."""
    engine = get_db_engine()
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


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Get user by ID."""
    return session.# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removedselect(User).where(User.id == user_id)).first()


__all__ = [
    "AuditLog",
    "Chunk",
    "Document",
    "Embedding",
    "User",
    "UserSession",
    "connect_args",
    "create_db_and_tables",
    "create_engine_for_url",
    "create_user",
    "engine",
    "get_db_engine",
    "get_db_session",
    "get_user_by_email",
    "get_user_by_id",
    "settings",
    "user",
]
