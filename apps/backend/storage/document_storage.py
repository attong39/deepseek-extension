"""


Document Storage





Handles storage and retrieval of documents with metadata and indexing.


Supports various document formats and provides search capabilities.


"""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .file_manager import FileManager, FileMetadata
import any
import author
import bool
import bytes
import checksum
import content
import content_type
import created_at
import description
import dict
import doc
import doc_id
import document_id
import filename
import id
import int
import language
import len
import list
import query
import self
import size
import str
import sum
import tag
import tags
import title
import updated_at


class DocumentMetadata:
    """Document metadata structure."""

    def __init__(
        self,
        id: str,
        filename: str,
        title: str,
        content_type: str,
        size: int,
        checksum: str,
        author: str | None = None,
        tags: list[str] | None = None,
        description: str | None = None,
        language: str = "en",
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id

        self.filename = filename

        self.title = title

        self.content_type = content_type

        self.size = size

        self.checksum = checksum

        self.author = author

        self.tags = tags or []

        self.description = description

        self.language = language

        self.created_at = created_at or datetime.now(UTC)

        self.updated_at = updated_at or datetime.now(UTC)


class DocumentStorage:
    """Document storage and management system."""

    def __init__(self, file_manager: FileManager | None = None):
        """Initialize document storage."""

        self.file_manager = file_manager or FileManager()

        self._document_index: dict[str, DocumentMetadata] = {}

    async def store_document(
        self,
        filename: str,
        content: bytes,
        title: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        description: str | None = None,
        language: str = "en",
    ) -> DocumentMetadata:
        """Store a document with metadata."""

        # Upload file

        file_metadata = await self.file_manager.upload_file(filename, content)

        # Create document metadata

        document_metadata = DocumentMetadata(
            id=file_metadata.id,
            filename=file_metadata.filename,
            title=title or Path(filename).stem,
            content_type=file_metadata.content_type,
            size=file_metadata.size,
            checksum=file_metadata.checksum,
            author=author,
            tags=tags,
            description=description,
            language=language,
        )

        # Index document

        self._document_index[document_metadata.id] = document_metadata

        return document_metadata

    async def get_document(self, document_id: str) -> DocumentMetadata | None:
        """Get document metadata by ID."""

        return self._document_index.get(document_id)

    async def get_document_content(self, document_id: str) -> bytes | None:
        """Get document content by ID."""

        document_metadata = await self.get_document(document_id)

        if not document_metadata:
            return None

        # Get file metadata from file manager

        file_metadata = FileMetadata(
            id=document_metadata.id,
            filename=document_metadata.filename,
            original_filename=document_metadata.filename,
            content_type=document_metadata.content_type,
            size=document_metadata.size,
            checksum=document_metadata.checksum,
            storage_path=f"uploads/{document_metadata.id}",
            storage_backend="local",
            created_at=document_metadata.created_at,
            updated_at=document_metadata.updated_at,
            metadata={},
        )

        return await self.file_manager.download_file(file_metadata)

    async def delete_document(self, document_id: str) -> bool:
        """Delete document and its content."""

        document_metadata = await self.get_document(document_id)

        if not document_metadata:
            return False

        # Create file metadata for deletion

        file_metadata = FileMetadata(
            id=document_metadata.id,
            filename=document_metadata.filename,
            original_filename=document_metadata.filename,
            content_type=document_metadata.content_type,
            size=document_metadata.size,
            checksum=document_metadata.checksum,
            storage_path=f"uploads/{document_metadata.id}",
            storage_backend="local",
            created_at=document_metadata.created_at,
            updated_at=document_metadata.updated_at,
            metadata={},
        )

        # Delete file

        if await self.file_manager.delete_file(file_metadata):
            # Remove from index

            self._document_index.pop(document_id, None)

            return True

        return False

    async def search_documents(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        author: str | None = None,
        content_type: str | None = None,
        language: str | None = None,
    ) -> list[DocumentMetadata]:
        """Search documents by various criteria."""

        results = []

        for document in self._document_index.values():
            # Check query in title and description

            if query:
                query_lower = query.lower()

                if not (
                    query_lower in document.title.lower()
                    or (
                        document.description
                        and query_lower in document.description.lower()
                    )
                ):
                    continue

            # Check tags

            if tags and not any(tag in document.tags for tag in tags):
                continue

            # Check author

            if author and document.author != author:
                continue

            # Check content type

            if content_type and document.content_type != content_type:
                continue

            # Check language

            if language and document.language != language:
                continue

            results.append(document)

        return results

    async def get_documents_by_author(self, author: str) -> list[DocumentMetadata]:
        """Get all documents by specific author."""

        return [doc for doc in self._document_index.values() if doc.author == author]

    async def get_documents_by_tags(self, tags: list[str]) -> list[DocumentMetadata]:
        """Get documents that have any of the specified tags."""

        return [
            doc
            for doc in self._document_index.values()
            if any(tag in doc.tags for tag in tags)
        ]

    async def update_document_metadata(
        self,
        document_id: str,
        title: str | None = None,
        author: str | None = None,
        tags: list[str] | None = None,
        description: str | None = None,
        language: str | None = None,
    ) -> DocumentMetadata | None:
        """Update document metadata."""

        document = self._document_index.get(document_id)

        if not document:
            return None

        # Update fields

        if title is not None:
            document.title = title

        if author is not None:
            document.author = author

        if tags is not None:
            document.tags = tags

        if description is not None:
            document.description = description

        if language is not None:
            document.language = language

        document.updated_at = datetime.now(UTC)

        return document

    async def get_storage_stats(self) -> dict[str, Any]:
        """Get document storage statistics."""

        total_documents = len(self._document_index)

        total_size = sum(doc.size for doc in self._document_index.values())

        # Count by content type

        content_types = {}

        for doc in self._document_index.values():
            content_types[doc.content_type] = content_types.get(doc.content_type, 0) + 1

        # Count by language

        languages = {}

        for doc in self._document_index.values():
            languages[doc.language] = languages.get(doc.language, 0) + 1

        # Count by author

        authors = {}

        for doc in self._document_index.values():
            if doc.author:
                authors[doc.author] = authors.get(doc.author, 0) + 1

        return {
            "total_documents": total_documents,
            "total_size": total_size,
            "content_types": content_types,
            "languages": languages,
            "authors": authors,
            "average_size": total_size / total_documents if total_documents > 0 else 0,
        }

    async def export_index(self) -> dict[str, Any]:
        """Export document index for backup."""

        index_data = {}

        for doc_id, doc in self._document_index.items():
            index_data[doc_id] = {
                "id": doc.id,
                "filename": doc.filename,
                "title": doc.title,
                "content_type": doc.content_type,
                "size": doc.size,
                "checksum": doc.checksum,
                "author": doc.author,
                "tags": doc.tags,
                "description": doc.description,
                "language": doc.language,
                "created_at": doc.created_at.isoformat(),
                "updated_at": doc.updated_at.isoformat(),
            }

        return {
            "version": "1.0",
            "exported_at": datetime.now(UTC).isoformat(),
            "total_documents": len(index_data),
            "documents": index_data,
        }


__all__ = [
    "DocumentStorage",
    "DocumentMetadata",
]
