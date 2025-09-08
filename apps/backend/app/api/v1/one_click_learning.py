"""
One-Click Learning API - RAG + ASR + OCR Integration

Complete learning pipeline: Ingest → Extract → Embed → Search
CPU-first with GPU acceleration via ZETA_USE_GPU=1
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependencies import (
import Exception
import UnicodeDecodeError
import asr_engine
import audio
import auto_ingest
import bool
import dict
import e
import f
import file
import float
import getattr
import image
import int
import language
import len
import list
import ocr_engine
import open
import preprocess
import rag_engine
import request
import search_query
import str
import user
    RAGEngineDep,
    ASREngineDep, 
    OCREngineDep,
    require_permissions,
    CurrentUserDep,
    AuditContextDep,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/one-click",
    tags=["one-click-learning", "rag", "asr", "ocr"],
)


# ── Pydantic Models ──────────────────────────

class TextIngestRequest(BaseModel):
    """Request for text ingestion."""
    texts: list[str]
    metadata: list[dict[str, Any]] | None = None


class SearchRequest(BaseModel):
    """Request for RAG search."""
    query: str
    k: int = 5
    score_threshold: float = 0.1


class SearchResponse(BaseModel):
    """Response for RAG search."""
    query: str
    results: list[dict[str, Any]]
    total_found: int


class TranscriptionResponse(BaseModel):
    """Response for ASR transcription."""
    text: str
    language: str
    duration: float | None = None
    segments: list[dict[str, Any]] = []


class OCRResponse(BaseModel):
    """Response for OCR extraction."""
    text: str
    lines: list[str] = []
    confidences: list[float] = []
    backend: str = "unknown"


class LearningPipelineResponse(BaseModel):
    """Response for complete learning pipeline."""
    status: str
    extracted_text: str
    indexed: bool
    search_results: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}


# ── RAG Endpoints ──────────────────────────

@router.post("/ingest/text", response_model=dict[str, Any])
async def ingest_text(
    request: TextIngestRequest,
    rag_engine: RAGEngineDep,
    user: CurrentUserDep,
    audit_context: AuditContextDep,
    _permissions=Depends(require_permissions(["learning.ingest"])),
) -> dict[str, Any]:
    """
    Ingest text documents into RAG index.
    
    - **texts**: List of text content to index
    - **metadata**: Optional metadata for each text
    """
    try:
        logger.info(f"Ingesting {len(request.texts)} texts for user {user.id}")
        
        # Add documents to RAG engine
        rag_engine.add_documents(
            texts=request.texts,
            metadata=request.metadata,
        )
        
        return {
            "status": "success",
            "message": f"Ingested {len(request.texts)} documents",
            "total_indexed": rag_engine.index.size(),
        }
    
    except Exception as e:
        logger.error(f"Text ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    rag_engine: RAGEngineDep,
    user: CurrentUserDep,
    _permissions=Depends(require_permissions(["learning.search"])),
) -> SearchResponse:
    """
    Search documents using RAG.
    
    - **query**: Search query
    - **k**: Number of results to return
    - **score_threshold**: Minimum similarity score
    """
    try:
        logger.info(f"Searching for: {request.query}")
        
        results = rag_engine.search(
            query=request.query,
            k=request.k,
            score_threshold=request.score_threshold,
        )
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
        )
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── ASR Endpoints ──────────────────────────

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    language: str | None = Form(None, description="Language code (auto-detect if None)"),
    asr_engine: ASREngineDep = None,
    user: CurrentUserDep = None,
    _permissions=Depends(require_permissions(["learning.transcribe"])),
) -> TranscriptionResponse:
    """
    Transcribe audio to text using ASR.
    
    - **audio**: Audio file upload
    - **language**: Optional language code (e.g., 'en', 'vi')
    """
    try:
        # Save uploaded file temporarily
        temp_path = Path(f"/tmp/{audio.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        with open(temp_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        logger.info(f"Transcribing audio: {audio.filename}")
        
        # Transcribe
        result = asr_engine.transcribe(
            audio_path=str(temp_path),
            language=language,
        )
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            duration=result.get("duration"),
            segments=result.get("segments", []),
        )
    
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── OCR Endpoints ──────────────────────────

@router.post("/extract-text", response_model=OCRResponse)
async def extract_text_from_image(
    image: UploadFile = File(..., description="Image file (PNG, JPG, PDF, etc.)"),
    preprocess: bool = Form(True, description="Apply image preprocessing"),
    ocr_engine: OCREngineDep = None,
    user: CurrentUserDep = None,
    _permissions=Depends(require_permissions(["learning.ocr"])),
) -> OCRResponse:
    """
    Extract text from image using OCR.
    
    - **image**: Image file upload
    - **preprocess**: Whether to apply image preprocessing
    """
    try:
        # Save uploaded file temporarily
        temp_path = Path(f"/tmp/{image.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        with open(temp_path, "wb") as f:
            content = await image.read()
            f.write(content)
        
        logger.info(f"Extracting text from image: {image.filename}")
        
        # Extract text
        result = ocr_engine.extract_text(
            image_path=str(temp_path),
            preprocess=preprocess,
        )
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        return OCRResponse(
            text=result["text"],
            lines=result.get("lines", []),
            confidences=result.get("confidences", []),
            backend=result.get("backend", "unknown"),
        )
    
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Complete Learning Pipeline ──────────────────────────

@router.post("/pipeline", response_model=LearningPipelineResponse)
async def complete_learning_pipeline(
    file: UploadFile = File(..., description="File to process (audio, image, or document)"),
    search_query: str | None = Form(None, description="Optional search query after ingestion"),
    auto_ingest: bool = Form(True, description="Automatically add extracted text to RAG index"),
    rag_engine: RAGEngineDep = None,
    asr_engine: ASREngineDep = None,
    ocr_engine: OCREngineDep = None,
    user: CurrentUserDep = None,
    _permissions=Depends(require_permissions(["learning.pipeline"])),
) -> LearningPipelineResponse:
    """
    Complete one-click learning pipeline:
    1. Auto-detect file type (audio/image/text)
    2. Extract text using appropriate engine
    3. Optionally ingest into RAG index
    4. Optionally search for related content
    """
    try:
        temp_path = Path(f"/tmp/{file.filename}")
        temp_path.parent.mkdir(exist_ok=True)
        
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Processing file through learning pipeline: {file.filename}")
        
        extracted_text = ""
        extraction_method = "none"
        
        # Auto-detect and extract
        file_ext = temp_path.suffix.lower()
        
        if file_ext in ['.wav', '.mp3', '.m4a', '.flac', '.aac']:
            # Audio file - use ASR
            asr_result = asr_engine.transcribe(str(temp_path))
            extracted_text = asr_result["text"]
            extraction_method = "asr"
            
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.pdf']:
            # Image file - use OCR
            ocr_result = ocr_engine.extract_text(str(temp_path))
            extracted_text = ocr_result["text"]
            extraction_method = "ocr"
            
        else:
            # Text file - read directly
            try:
                extracted_text = temp_path.read_text(encoding='utf-8')
                extraction_method = "direct"
            except UnicodeDecodeError:
                try:
                    extracted_text = temp_path.read_text(encoding='latin-1')
                    extraction_method = "direct"
                except Exception:
                    raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        # Ingest into RAG if requested
        indexed = False
        if auto_ingest and extracted_text.strip():
            rag_engine.add_documents(
                texts=[extracted_text],
                metadata=[{
                    "filename": file.filename,
                    "extraction_method": extraction_method,
                    "user_id": str(user.id),
                }],
            )
            indexed = True
        
        # Search if query provided
        search_results = []
        if search_query:
            search_results = rag_engine.search(
                query=search_query,
                k=5,
                score_threshold=0.1,
            )
        
        return LearningPipelineResponse(
            status="success",
            extracted_text=extracted_text,
            indexed=indexed,
            search_results=search_results,
            metadata={
                "filename": file.filename,
                "extraction_method": extraction_method,
                "text_length": len(extracted_text),
                "total_indexed": rag_engine.index.size(),
            },
        )
    
    except Exception as e:
        logger.error(f"Learning pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Status Endpoints ──────────────────────────

@router.get("/status")
async def learning_status(
    rag_engine: RAGEngineDep,
    asr_engine: ASREngineDep,
    ocr_engine: OCREngineDep,
) -> dict[str, Any]:
    """Get status of all learning engines."""
    return {
        "rag": {
            "available": rag_engine is not None,
            "indexed_documents": rag_engine.index.size() if rag_engine else 0,
        },
        "asr": {
            "available": asr_engine is not None,
            "device": getattr(asr_engine, "device", "unknown") if asr_engine else "unknown",
        },
        "ocr": {
            "available": ocr_engine is not None,
            "backend": getattr(ocr_engine, "backend", "unknown") if ocr_engine else "unknown",
        },
        "gpu_enabled": bool(getattr(rag_engine, "device", "cpu") == "cuda") if rag_engine else False,
    }


# ── Export ──────────────────────────

__all__ = ["router"]
