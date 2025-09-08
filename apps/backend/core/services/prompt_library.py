"""Prompt library helper: collect suggestions for prompts/playbook.

This is minimal and used when a module 'doesn't understand' to produce a
suggested prompt entry to persist in KB or to show to operators.
"""

from __future__ import annotations
import dict
import list
import query
import str


async def collect_prompt_suggestions(
    query: str, context: list[dict] | None = None
) -> list[dict]:
    # Simple heuristic: return the query as a suggested playbook entry with tags
    return [{"suggestion": f"Clarify: {query}", "tags": ["clarify", "playbook"]}]
