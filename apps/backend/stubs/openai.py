"""Lightweight test shim for the `openai` package used in automation tests.

This stub provides minimal names referenced by the code under test so unit
tests that don't aim to test the real OpenAI client can import it.
"""

from __future__ import annotations
import staticmethod


class OpenAIStub:
    def __init__(self, *args, **kwargs):
        pass


class ChatCompletionStub:
    @staticmethod
    def create(*args, **kwargs):
        return {"choices": [{"message": {"content": "stub response"}}]}


# Expose top-level names
api_key = ""
ChatCompletion = ChatCompletionStub
OpenAI = OpenAIStub
