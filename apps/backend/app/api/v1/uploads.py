"""
Upload API router - Multipart file upload
Hỗ trợ text, image, video, audio files
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Literal

from app.api.v1._schemas import UploadResp
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
import OSError
import content_type
import dict
import e
import extensions
import f
import file
import filename
import len
import open
import str

router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

# Cấu hình upload
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types và size limits
ALLOWED_EXTENSIONS = {
    "text": {".txt", ".md", ".json", ".csv", ".log"},
    "image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "video": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"},
    "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"},
    "other": {".pdf", ".doc", ".docx", ".zip", ".rar"},
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


def _detect_kind(
    filename: str, content_type: str
) -> Literal["text", "image", "video", "audio", "other"]:
    """Tự động detect loại file từ extension và MIME type"""
    if not filename:
        return "other"

    ext = Path(filename).suffix.lower()

    # Check by extension first
    for kind, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return kind  # type: ignore[return-value]

    # Check by MIME type
    if content_type.startswith("text/"):
        return "text"
    elif content_type.startswith("image/"):
        return "image"
    elif content_type.startswith("video/"):
        return "video"
    elif content_type.startswith("audio/"):
        return "audio"

    return "other"


@router.post("", response_model=UploadResp)
async def upload_file(
    file: UploadFile = File(...),
    kind: str = Form("auto"),
) -> UploadResp:
    """
    Upload file với auto-detection loại file

    Args:
        file: File upload
        kind: Loại file manual hoặc 'auto' để tự detect

    Returns:
        UploadResp với file_id, path, metadata
    """
    if not file.filename:
        raise HTTPException(400, "Filename không được để trống")

    # Check file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            413, f"File quá lớn (max {MAX_FILE_SIZE // 1024 // 1024}MB)"
        )

    # Auto-detect kind nếu cần
    detected_kind: Literal["text", "image", "video", "audio", "other"]
    if kind == "auto":
        detected_kind = _detect_kind(file.filename, file.content_type or "")
    else:
        # Validate manual kind
        valid_kinds = {"text", "image", "video", "audio", "other"}
        if kind not in valid_kinds:
            raise HTTPException(400, f"Kind không hợp lệ: {kind}")
        detected_kind = kind  # type: ignore[assignment]

    # Generate unique file ID và path
    file_id = f"f_{uuid.uuid4().hex[:12]}"
    ext = Path(file.filename).suffix
    safe_filename = f"{file_id}{ext}"
    file_path = UPLOAD_DIR / safe_filename

    # Save file (sync I/O cho đơn giản DEV)
    try:
        with open(file_path, "wb") as f:  # type: ignore[misc]
            f.write(file_content)
    except OSError as e:
        raise HTTPException(500, f"Lỗi lưu file: {str(e)}")

    return UploadResp(
        file_id=file_id,
        kind=detected_kind,
        path=str(file_path),
        size_bytes=len(file_content),
        original_name=file.filename,
    )


@router.get("/{file_id}/info", response_model=UploadResp)
async def get_file_info(file_id: str) -> UploadResp:
    """Lấy thông tin file đã upload"""
    # Simple scan trong upload dir
    for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
        if file_path.is_file():
            stat = file_path.stat()
            kind = _detect_kind(file_path.name, "")
            return UploadResp(
                file_id=file_id,
                kind=kind,
                path=str(file_path),
                size_bytes=stat.st_size,
                original_name=file_path.name,
            )

    raise HTTPException(404, f"File {file_id} không tồn tại")


@router.delete("/{file_id}")
async def delete_file(file_id: str) -> dict[str, str]:
    """Xóa file đã upload"""
    deleted = False
    for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
        if file_path.is_file():
            file_path.unlink()
            deleted = True

    if not deleted:
        raise HTTPException(404, f"File {file_id} không tồn tại")

    return {"message": f"Đã xóa file {file_id}"}
