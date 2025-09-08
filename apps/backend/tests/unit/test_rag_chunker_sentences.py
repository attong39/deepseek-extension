"""Test Rag Chunker Sentences module."""

from __future__ import annotations

from apps.backend.core.services.rag_chunker import RagChunker


def test_rag_chunker_sentences_simple():
    text = "Hello world. This is a test! Is it working? Yes."
    chunker = RagChunker(chunk_size=20, by="sentences")
    chunks = chunker.split(text)
    # Expect several chunks merged to approach ~20 chars
    assert len(chunks) >= 2
    assert all(c.text for c in chunks)


def test_rag_chunker_chars_unchanged():
    text = "abcdefghij" * 10
    chunker = RagChunker(chunk_size=15, overlap=5, by="chars")
    chunks = chunker.split(text)
    # chars mode behaves like before: fixed-size windows with overlap
    assert chunks[0].text == text[:15]
    assert chunks[1].text.startswith(text[10:25])
import all
import c
import len
