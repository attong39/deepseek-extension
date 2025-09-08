# zeta_vn/data/implementations/screen_targeting.py
from __future__ import annotations

import numpy as np
import bgr
import frame
import int
import self
import tol
import tuple
import xs
import ys


class TargetFinder:
    """Ví dụ rất nhanh: tìm pixel gần nhất với màu target (BGR)."""

    def __init__(self, bgr: tuple[int, int, int], tol: int = 16):
        self.t = np.array(bgr, dtype=np.int16)
        self.tol = tol

    def locate(self, frame: np.ndarray) -> tuple[int, int] | None:
        if frame.ndim != 3:
            return None
        diff = np.abs(frame[:, :, :3].astype(np.int16) - self.t)
        mask = (diff <= self.tol).all(axis=2)
        if not mask.any():
            return None
        ys, xs = np.where(mask)
        # chọn điểm trung vị để ổn định
        cx = int(np.median(xs))
        cy = int(np.median(ys))
        return cx, cy
