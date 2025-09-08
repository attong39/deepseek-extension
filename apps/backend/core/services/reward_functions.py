from __future__ import annotations
import bool
import citations_ok
import coverage
import float
import guard_risk
import len
import max
import pred
import ref
import runtime_regression
import set
import str
import test_pass_rate
import x

"""Reward functions cho self-learning.

Các hàm trả về reward chuẩn hoá [0,1]. Không phụ thuộc SDK ngoài.
"""


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return float(x)


def reward_qa(
    pred: str, ref: str, *, citations_ok: bool = True, guard_risk: float = 0.0
) -> float:
    """Reward đơn giản cho QA/RAG.

    - Nội dung: overlap ký tự (proxy nhanh cho ROUGE/LCS)
    - Citations: cộng nhẹ nếu đúng; Guard risk: trừ theo rủi ro
    """
    if not pred:
        return 0.0
    # Overlap ký tự (min-hash proxy cực đơn giản)
    a = set(pred.lower().split())
    b = set(ref.lower().split()) if ref else set()
    overlap = (len(a & b) / max(1, len(a))) if a else 0.0
    base = 0.6 * overlap
    cite_bonus = 0.2 if citations_ok else 0.0
    risk_penalty = 0.2 * clamp01(guard_risk)
    return clamp01(base + cite_bonus - risk_penalty)


def reward_coding(
    *, test_pass_rate: float, coverage: float = 0.0, runtime_regression: float = 0.0
) -> float:
    """Reward cho coding task.

    - test_pass_rate: [0,1]
    - coverage: [0,1] (tuỳ chọn)
    - runtime_regression: giây chậm thêm (phạt nhẹ)
    """
    base = 0.7 * clamp01(test_pass_rate) + 0.2 * clamp01(coverage)
    penalty = 0.1 * clamp01(runtime_regression / 5.0)  # phạt tối đa 0.1 nếu chậm >=5s
    return clamp01(base - penalty)
