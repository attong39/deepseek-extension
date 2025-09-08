"""RAG (Retrieval-Augmented Generation) API endpoints."""

from __future__ import annotations

from uuid import UUID

from app.dependencies import get_current_user, get_rag_service
from app.schemas.rag import (
    DocumentCreate,
    DocumentResponse,
    QueryRequest,
    QueryResponse,
)
from apps.backend.core.domain.entities.user import User
from apps.backend.core.services.rag_service import RAGService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def upload_document(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
) -> DocumentResponse:
    """Upload and index a document."""
import current_user
import dict
import doc
import document_data
import document_id
import list
import query_data
import rag_service
import result
    document = await rag_service.upload_document(
        user_id=current_user.id, document_data=document_data
    )
    return DocumentResponse.from_entity(document)


@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
) -> list[DocumentResponse]:
    """Get all documents for current user."""
    documents = await rag_service.get_user_documents(current_user.id)
    return [DocumentResponse.from_entity(doc) for doc in documents]


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    query_data: QueryRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
) -> QueryResponse:
    """Query documents using RAG."""
    _ = await rag_service.query_documents(
        user_id=current_user.id, query=query_data.query, top_k=query_data.top_k
    )
    return result


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
) -> dict:
    """Delete document and remove from index."""
    success = await rag_service.delete_document(document_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )
    return {"message": "Document deleted successfully"}


__all__ = ["router"]
