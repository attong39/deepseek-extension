"""Central trainer-only policy for internal trainer services.

Services that generate training artifacts (mentors, trainers, summarizers,
planners) should import `TRAINER_POLICY` from here and append it to their
system prompts when running in trainer-only mode.

This keeps a single source-of-truth and avoids duplicated strings across
the codebase.
"""

from __future__ import annotations

TRAINER_POLICY = (
    "You are NOT a user-facing assistant. Never answer end-users directly. "
    "Only produce training artifacts, guidance, evaluation criteria, or prompt libraries."
)
