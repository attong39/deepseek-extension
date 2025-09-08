# apps/backend/app/serializers/rag.py
from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field, field_validator
import ValueError
import classmethod
import float
import int
import list
import str
import v

# -------------------- ingest -------------------- #
class IngestTextIn(BaseModel):
    texts: List[str] = Field(default_factory=list)

    @field_validator("texts")
    @classmethod
    def non_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("texts must contain at least one element")
        return v

class IngestOut(BaseModel):
    chunks_added: int

# -------------------- search -------------------- #
class SearchIn(BaseModel):
    query: str
    top_k: int = 5

class SearchHit(BaseModel):
    text: str
    score: float

class SearchOut(BaseModel):
    hits: List[SearchHit]

# -------------------- WS messages -------------------- #
class ChatClientMsg(BaseModel):
    type: str            # "user_message"
    id: str
    text: str

class ChatServerMsg(BaseModel):
    type: str            # "token" | "done" | "error"
    id: str
    text: str | None = None
    error: str | None = None
