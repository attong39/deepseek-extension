# zeta_vn/data/implementations/screen_capture_dxgi.py
from __future__ import annotations

import numpy as np
import Exception
import RuntimeError
import bottom
import h
import int
import left
import monitor
import region
import right
import self
import target_fps
import top
import tuple
import w

try:
    import dxcam  # noqa: PLC0415
except Exception:  # pragma: no cover
    dxcam = None

try:
    from mss import mss  # noqa: PLC0415
except Exception:  # pragma: no cover
    mss = None  # type: ignore


class ScreenCapture:
    """High‑FPS screen capture ưu tiên DXGI (dxcam), fallback MSS (GDI)."""

    def __init__(
        self,
        monitor: int = 0,
        target_fps: int = 120,
        region: tuple[int, int, int, int] | None = None,
    ) -> None:
        self.monitor = monitor
        self.target_fps = target_fps
        self.region = region
        self._cam = None
        self._mss = None

    def start(self) -> None:
        if dxcam is not None:
            self._cam = dxcam.create(output_idx=self.monitor, output_color="BGRA")
            self._cam.start(  # type: ignore
                region=self.region, target_fps=self.target_fps, video_mode=True
            )
        elif mss is not None:
            self._mss = mss()  # type: ignore
        else:
            raise RuntimeError("Neither dxcam nor mss is available")

    def stop(self) -> None:
        if self._cam is not None:
            self._cam.stop()
            self._cam = None
        if self._mss is not None:
            self._mss.close()
            self._mss = None

    def frame(self) -> np.ndarray:
        if self._cam is not None:
            img = self._cam.get_latest_frame()
            # dxcam returns BGRA np.ndarray
            if img is None:
                raise RuntimeError("No frame yet")
            return img
        elif self._mss is not None:
            bbox = self.region
            if bbox is None:
                mon = self._mss.monitors[1]  # primary
                bbox = (
                    mon["left"],
                    mon["top"],
                    mon["left"] + mon["width"],
                    mon["top"] + mon["height"],
                )
            left, top, right, bottom = bbox
            w, h = right - left, bottom - top
            raw = self._mss.grab({"left": left, "top": top, "width": w, "height": h})
            img = np.frombuffer(raw.rgb, dtype=np.uint8).reshape(h, w, 3)
            return img
        else:
            raise RuntimeError("Capture not started")
