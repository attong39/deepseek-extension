import Exception
import ValueError
import dict
import getattr
import int
import mod
import str
# apps/backend/app/compat/startup_check.py
"""
Compatibility check – chạy khi FastAPI khởi tạo.
Log một dòng duy nhất: phiên bản NumPy và trạng thái NP2/NP1.
"""
from __future__ import annotations
import importlib, logging

log = logging.getLogger("zeta.compat")

def _ver(mod: str) -> str:
    """Return __version__ if importable, else 'not-installed'."""
    try:
        m = importlib.import_module(mod)
        return getattr(m, "__version__", "unknown")
    except Exception:
        return "not-installed"

def report() -> dict[str, str]:
    info = {
        "numpy": _ver("numpy"),
        "faiss": _ver("faiss"),
        "opencv": _ver("cv2"),
        "torch": _ver("torch"),
        "sentence_transformers": _ver("sentence_transformers"),
    }

    np_version = info["numpy"]
    if np_version != "not-installed":
        try:
            major = int(np_version.split(".")[0])
            if major >= 2:
                log.warning(
                    "🚧 Running with NumPy %s (NP2 profile). "
                    "Make sure faiss, opencv & torch are NP2‑compatible.", np_version
                )
            else:
                log.info("✅ NumPy %s (NP1 pinned) – stable configuration.", np_version)
        except ValueError:
            log.info("🔍 NumPy version: %s", np_version)
    else:
        log.error("❌ NumPy not installed – this should never happen.")
    
    return info
