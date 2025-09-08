"""


⚠️ DEPRECATION WARNING:


This file has been renamed to services_client.py


Please update your imports to use the new location.


This file will be removed in future versions.


"""


# Import everything from new location for backward compatibility

import warnings

# Backward-compat: re-export from the canonical client module
from apps.backend.data.external.services_client import *  # noqa: F401,F403
import DeprecationWarning

warnings.warn(
    f"{__file__} is deprecated. Use services_client.py instead.",
    DeprecationWarning,
    stacklevel=2,
)
