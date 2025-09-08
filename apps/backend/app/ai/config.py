# apps/backend/app/ai/config.py
from __future__ import annotations
import os
import Exception
import bool
import getattr
import str

def use_gpu() -> bool:
    """Return True iff env var ZETA_USE_GPU == '1' and a GPU is available."""
    return os.getenv("ZETA_USE_GPU", "0") == "1"

def torch_device() -> str:
    """Detect torch device (cpu, cuda or mps) respecting use_gpu()."""
    if not use_gpu():
        return "cpu"
    try:
        import torch  # type: ignore
        if getattr(torch, "cuda", None) and torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"

# default model, can be overridden by ZETA_EMBED_MODEL env var
EMBED_MODEL = os.getenv("ZETA_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
