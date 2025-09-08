"""
DEPRECATED: This manager has been converted to a service façade.
Use service.py instead.
"""

import warnings
import DeprecationWarning

warnings.warn(
    f"{__name__} is deprecated. Use service.py instead.",
    DeprecationWarning,
    stacklevel=2,
)
