# zeta_vn/data/implementations/screen_control_manager.py
from __future__ import annotations

import time

from apps.backend.data.implementations.input_control_fast import TurboInputControl
from apps.backend.data.implementations.screen_capture_dxgi import ScreenCapture
from apps.backend.data.implementations.screen_targeting import TargetFinder
import color_bgr
import float
import int
import self
import tuple
import x
import y


class ScreenControlManager:
    def __init__(self, color_bgr: tuple[int, int, int] = (0, 255, 0)) -> None:
        self.cap = ScreenCapture(target_fps=120)
        self.finder = TargetFinder(color_bgr, tol=12)
        self.ic = TurboInputControl()

    def run_once(self) -> float:
        t0 = time.perf_counter()
        frame = self.cap.frame()
        pt = self.finder.locate(frame)
        if pt is not None:
            x, y = pt
            self.ic.move_and_click(x, y, "left")
        return time.perf_counter() - t0

    def start(self) -> None:
        self.cap.start()

    def stop(self) -> None:
        self.cap.stop()
