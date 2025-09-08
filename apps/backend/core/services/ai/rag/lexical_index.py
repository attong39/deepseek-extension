"""
TF-IDF Lexical Index for Hybrid RAG.

Lightweight implementation for lexical search to complement vector search.
Performance: O(|query_tokens|) for search, O(|doc_tokens|) for indexing.
"""

from __future__ import annotations

import math
import re
import dict
import doc_key
import float
import int
import key
import len
import list
import max
import meta
import query
import scores
import self
import sorted
import str
import text
import tf_local
import tf_map
import token
import top_k
import tuple
import word
import x

# Regex for tokenization (supports Vietnamese)
_WORD = re.compile(r"[a-zA-ZÀ-ỹ0-9]+")


class LexicalIndex:
    """
    TF-IDF based lexical search index.

    Features:
    - Term frequency (TF) with log normalization
    - Inverse document frequency (IDF)
    - Document length normalization
    - Unicode/Vietnamese text support
    """

    def __init__(self) -> None:
        # Document frequency: word -> number of docs containing word
        self.df: dict[str, int] = {}

        # Term frequency: doc_key -> word -> count
        self.tf: dict[str, dict[str, int]] = {}

        # Document length: doc_key -> token_count
        self.doc_len: dict[str, int] = {}

        # Document storage: doc_key -> (text, metadata)
        self.docs: dict[str, tuple[str, dict]] = {}

    def _tokens(self, text: str) -> list[str]:
        """Tokenize text into lowercase words."""
        return [token.lower() for token in _WORD.findall(text)]

    def add(self, key: str, text: str, meta: dict) -> None:
        """
        Add document to index.

        Args:
            key: Unique document identifier
            text: Document text content
            meta: Document metadata
        """
        tokens = self._tokens(text)

        # Store document
        self.docs[key] = (text, meta)
        self.doc_len[key] = len(tokens)

        # Calculate term frequencies
        tf_local: dict[str, int] = {}
        for word in tokens:
            tf_local[word] = tf_local.get(word, 0) + 1

        self.tf[key] = tf_local

        # Update document frequencies
        for word in tf_local:
            self.df[word] = self.df.get(word, 0) + 1

    def search(self, query: str, top_k: int = 5) -> list[tuple[str, float]]:
        """
        Search for documents matching query.

        Args:
            query: Search query text
            top_k: Maximum number of results to return

        Returns:
            List of (document_key, score) tuples, sorted by relevance
        """
        query_tokens = self._tokens(query)
        num_docs = max(len(self.docs), 1)

        # Calculate TF-IDF scores for each document
        scores: dict[str, float] = {}

        for word in query_tokens:
            doc_freq = self.df.get(word, 0)
            if not doc_freq:
                continue

            # IDF with smoothing: log((N+1)/(df+1)) + 1
            idf = math.log((num_docs + 1) / (doc_freq + 1)) + 1.0

            # Score each document containing this word
            for doc_key, tf_map in self.tf.items():
                term_freq = tf_map.get(word, 0)
                if term_freq > 0:
                    # Document length normalization
                    doc_length = self.doc_len.get(doc_key, 1)
                    length_norm = 1.0 / (1.0 + math.log(1 + doc_length))

                    # TF-IDF score
                    tf_idf_score = term_freq * idf * length_norm
                    scores[doc_key] = scores.get(doc_key, 0.0) + tf_idf_score

        # Sort by score and return top-k
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def get_document(self, key: str) -> tuple[str, dict] | None:
        """Get document content and metadata by key."""
        return self.docs.get(key)

    def size(self) -> int:
        """Return number of indexed documents."""
        return len(self.docs)

    def vocabulary_size(self) -> int:
        """Return vocabulary size (unique terms)."""
        return len(self.df)

    def clear(self) -> None:
        """Clear all indexed data."""
        self.df.clear()
        self.tf.clear()
        self.doc_len.clear()
        self.docs.clear()
