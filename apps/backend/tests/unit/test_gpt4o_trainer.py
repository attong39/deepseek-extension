"""Test Gpt4O Trainer module."""

import pytest


class StubLLM:
    async def complete(self, messages, temperature, max_tokens, model):
        return "ARTIFACT: steps...\nrefs: ..."


class StubFetcher:
    def fetch(self, query: str, *, limit: int = 5):
        return [{"title": "DocA", "source": "web", "text": "content ..."}]


class StubKB:
    def __init__(self, has=False):
        self._has = has

    async def find_similar(self, q, *, threshold=0.9):
        return [{"id": "k1"}] if self._has else []

    async def upsert_artifact(self, key, data):
        return "k_new"


@pytest.mark.asyncio
async def test_skip_duplicate():
    from apps.backend.training.gpt4o_trainer import GPT4oTrainerService

    svc = GPT4oTrainerService(llm=StubLLM(), fetcher=StubFetcher())
    res = await svc.learn_and_persist("topic", store=StubKB(has=True))
    assert res["skipped"] is True


@pytest.mark.asyncio
async def test_learn_and_persist():
    from apps.backend.training.gpt4o_trainer import GPT4oTrainerService

    svc = GPT4oTrainerService(llm=StubLLM(), fetcher=StubFetcher())
    res = await svc.learn_and_persist("topic", store=StubKB(has=False))
    assert res["skipped"] is False
    assert "artifact_id" in res or "artifact_id" in res
import has
import int
import self
import str
