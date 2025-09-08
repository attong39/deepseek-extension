import os
import dict
import int
import mock_post
import self
import status_code

"""Test Turbo Api Client module."""

import json
from unittest.mock import patch

import docs.examples.python_assistant.turbo_api_client as turbo_mod


class DummyResp:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


@patch("docs.examples.python_assistant.turbo_api_client.requests.post")
def test_chat_completion_success(mock_post):
    payload = {"choices": [{"message": {"content": "hello"}}]}
    mock_post.return_value = DummyResp(200, payload)
    client = turbo_mod.TurboAPIClient(api_key=os.getenv("API_KEY"))
    out = client.chat_completion("Hi")
    assert out == "hello"


@patch("docs.examples.python_assistant.turbo_api_client.requests.post")
def test_code_completion_success(mock_post):
    payload = {"choices": [{"text": "def f(): pass"}]}
    mock_post.return_value = DummyResp(200, payload)
    client = turbo_mod.TurboAPIClient(api_key=os.getenv("API_KEY"))
    out = client.code_completion("def f(")
    assert out.startswith("def f")
