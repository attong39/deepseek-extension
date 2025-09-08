"""Business rule validators at the application boundary.

Keep domain logic out of here; only cross-field/request surface checks.
"""

from __future__ import annotations
import all
import bool
import isinstance
import list
import staticmethod
import str
import t
import tags


class BusinessValidator:
    """Business rule checks."""

    @staticmethod
    def non_empty_tags(tags: list[str] | None) -> bool:
        """Tags list must be None or a non-empty list of non-empty strings."""
        if tags is None:
            return True
        return bool(tags) and all(isinstance(t, str) and t.strip() for t in tags)
