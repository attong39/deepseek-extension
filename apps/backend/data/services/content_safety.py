from __future__ import annotations
import api_key
import bool
import len
import self
import str
import text


class ExternalModerationAdapter:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def moderate(self, text: str) -> bool:
        """
        return True if safe, False if block.
        TODO: triển khai call provider (OpenAI, Azure AI, v.v.)
        """
        # placeholder: basic heuristic e.g., block empty/too long input
        if not text:
            return False
        if len(text) > 10000:
            return False
        return True
