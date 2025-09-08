# apps/backend/app/api/v1/rag_router.py
from __future__ import annotations
import io
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from ...serializers.rag import (
import Exception
import body
import chunk
import e
import f
import files
import p
import page
import payload
import s
import str
import t
import tmp
import ws
    IngestTextIn, IngestOut, SearchIn, SearchOut, SearchHit,
    ChatClientMsg, ChatServerMsg,
)
from ...dependencies import require_permissions
from ...ai.rag_service import RagService
from ...ai.llm import LLMClient

router = APIRouter(prefix="/rag", tags=["v1", "rag"])

# -------- DI factories (imported via dependencies) --------
def get_rag_service() -> RagService:
    return RagService(data_dir="data")

def get_llm_client() -> LLMClient:
    return LLMClient()

# -------- Helper: read uploaded file & extract text --------
def _read_text_from_file(f: UploadFile) -> str:
    name = (f.filename or "").lower()
    raw = f.file.read()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        import docx
        doc = docx.Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")
    if name.endswith((".png", ".jpg", ".jpeg", ".bmp")):
        from ...ai.ocr_service import OCRService
        ocr = OCRService()
        if ocr.available():
            import tempfile, os
            with tempfile.NamedTemporaryFile(delete=False, suffix=name[name.rfind("."):]) as tmp:
                tmp.write(raw)
                tmp_path = tmp.name
            try:
                return ocr.ocr_image(tmp_path)
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
        return ""
    # fallback: raw bytes → utf‑8 text
    try:
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return ""

# -------- REST endpoints --------
@router.post(
    "/ingest/text",
    response_model=IngestOut,
    dependencies=[Depends(require_permissions("rag:ingest"))],
)
async def ingest_text(
    payload: IngestTextIn,
    rag: RagService = Depends(get_rag_service),
) -> IngestOut:
    return IngestOut(chunks_added=rag.add_texts(payload.texts))

@router.post(
    "/ingest/upload",
    response_model=IngestOut,
    dependencies=[Depends(require_permissions("rag:ingest"))],
)
async def ingest_upload(
    files: List[UploadFile] = File(...),
    rag: RagService = Depends(get_rag_service),
) -> IngestOut:
    texts = [_read_text_from_file(f) for f in files]
    texts = [t for t in texts if t.strip()]
    return IngestOut(chunks_added=rag.add_texts(texts))

@router.post(
    "/search",
    response_model=SearchOut,
    dependencies=[Depends(require_permissions("rag:search"))],
)
async def search(
    body: SearchIn,
    rag: RagService = Depends(get_rag_service),
) -> SearchOut:
    hits = rag.search(body.query, k=body.top_k)
    return SearchOut(hits=[SearchHit(text=t, score=s) for t, s in hits])

# -------- WS streaming chat --------
@router.websocket("/chat/ws")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    rag = RagService(data_dir="data")
    llm = LLMClient()
    try:
        while True:
            raw = await ws.receive_text()
            try:
                client_msg = ChatClientMsg.model_validate_json(raw)
            except ValidationError as e:
                await ws.send_text(
                    ChatServerMsg(type="error", id="parse", error=str(e)).model_dump_json()
                )
                continue

            if client_msg.type != "user_message":
                await ws.send_text(
                    ChatServerMsg(type="error", id=client_msg.id, error="unsupported_type")
                    .model_dump_json()
                )
                continue

            # retrieve context from RAG
            context = [t for t, _ in rag.search(client_msg.text, k=5)]
            answer = await llm.generate(client_msg.text, context)

            # stream per sentence (or per chunk)
            for chunk in answer.split(". "):
                await ws.send_text(
                    ChatServerMsg(type="token", id=client_msg.id, text=chunk.strip())
                    .model_dump_json()
                )
            await ws.send_text(ChatServerMsg(type="done", id=client_msg.id).model_dump_json())
    except WebSocketDisconnect:
        return
