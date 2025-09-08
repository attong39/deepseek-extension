# zeta_vn/data/implementations/input_control_fast.py
from __future__ import annotations

import ctypes as C
from collections.abc import Sequence
from dataclasses import dataclass
import Exception
import ValueError
import bool
import bufs
import button
import delta
import dx
import dy
import inputs
import int
import len
import list
import max
import range
import repeat
import reversed
import self
import str
import tuple
import vh
import vk
import vks
import vw
import vx
import vy

# Win32 constants
ULONG_PTR = C.POINTER(C.c_ulong)

# Mouse flags
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_VIRTUALDESK = 0x4000

# Keyboard flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

# INPUT types
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# DPI awareness
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = C.c_void_p(-4)

# System metrics
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79

user32 = C.windll.user32
kernel32 = C.windll.kernel32
shcore = None
try:
    shcore = C.windll.shcore
except Exception:
    shcore = None


class MOUSEINPUT(C.Structure):
    _fields_ = [
        ("dx", C.c_long),
        ("dy", C.c_long),
        ("mouseData", C.c_ulong),
        ("dwFlags", C.c_ulong),
        ("time", C.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class KEYBDINPUT(C.Structure):
    _fields_ = [
        ("wVk", C.c_ushort),
        ("wScan", C.c_ushort),
        ("dwFlags", C.c_ulong),
        ("time", C.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(C.Structure):
    _fields_ = [("uMsg", C.c_ulong), ("wParamL", C.c_short), ("wParamH", C.c_ushort)]


class _INPUTunion(C.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(C.Structure):
    _fields_ = [("type", C.c_ulong), ("union", _INPUTunion)]


# Utilities -----------------------------------------------------------------


def _set_dpi_awareness() -> None:
    """Make process per‑monitor DPI aware so absolute coords are correct."""
    try:
        user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    except Exception:
        if shcore:
            try:
                # PROCESS_PER_MONITOR_DPI_AWARE = 2
                shcore.SetProcessDpiAwareness(2)
            except Exception:
                pass


def _metrics() -> tuple[int, int, int, int]:
    x = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    y = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    w = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    h = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    return x, y, w, h


def _to_absolute(x: int, y: int) -> tuple[int, int]:
    vx, vy, vw, vh = _metrics()
    # Map pixel -> [0..65535]
    ax = int((x - vx) * 65535 / max(vw - 1, 1))
    ay = int((y - vy) * 65535 / max(vh - 1, 1))
    return ax, ay


def _send_inputs(inputs: Sequence[INPUT]) -> int:
    arr = (INPUT * len(inputs))(*inputs)
    sent = user32.SendInput(len(inputs), arr, C.sizeof(INPUT))
    return int(sent)


def _scan_code(vk: int) -> int:
    return int(user32.MapVirtualKeyW(vk, 0))


# Public API ----------------------------------------------------------------


@dataclass(frozen=True)
class MoveOptions:
    absolute: bool = True
    virtual_desktop: bool = True


class TurboInputControl:
    """Siêu tốc: batching `SendInput`, absolute coords (multi‑monitor), DPI‑aware."""

    def __init__(self) -> None:
        _set_dpi_awareness()

    # ---- Mouse ----
    def move_to(self, x: int, y: int, *, opts: MoveOptions | None = None) -> None:
        opts = opts or MoveOptions()
        flags = MOUSEEVENTF_MOVE
        dx, dy = x, y
        if opts.absolute:
            ax, ay = _to_absolute(x, y)
            dx, dy = ax, ay
            flags |= MOUSEEVENTF_ABSOLUTE
            if opts.virtual_desktop:
                flags |= MOUSEEVENTF_VIRTUALDESK
        ev = INPUT(
            type=INPUT_MOUSE,
            union=_INPUTunion(mi=MOUSEINPUT(dx, dy, 0, flags, 0, None)),
        )
        _send_inputs([ev])

    def click(self, button: str = "left") -> None:
        down = up = 0
        if button == "left":
            down, up = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
        elif button == "right":
            down, up = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
        elif button == "middle":
            down, up = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
        else:
            raise ValueError("button must be left/right/middle")
        _send_inputs(
            [
                INPUT(
                    type=INPUT_MOUSE,
                    union=_INPUTunion(mi=MOUSEINPUT(0, 0, 0, down, 0, None)),
                ),
                INPUT(
                    type=INPUT_MOUSE,
                    union=_INPUTunion(mi=MOUSEINPUT(0, 0, 0, up, 0, None)),
                ),
            ]
        )

    def move_and_click(self, x: int, y: int, button: str = "left") -> None:
        self.move_to(x, y)
        self.click(button)

    def scroll(self, delta: int) -> None:
        # positive = up, negative = down; delta multiple of 120
        ev = INPUT(
            type=INPUT_MOUSE,
            union=_INPUTunion(mi=MOUSEINPUT(0, 0, delta, MOUSEEVENTF_WHEEL, 0, None)),
        )
        _send_inputs([ev])

    # ---- Keyboard ----
    def key_down(self, vk: int) -> None:
        sc = _scan_code(vk)
        ev = INPUT(
            type=INPUT_KEYBOARD,
            union=_INPUTunion(ki=KEYBDINPUT(vk, sc, KEYEVENTF_SCANCODE, 0, None)),
        )
        _send_inputs([ev])

    def key_up(self, vk: int) -> None:
        sc = _scan_code(vk)
        ev = INPUT(
            type=INPUT_KEYBOARD,
            union=_INPUTunion(
                ki=KEYBDINPUT(vk, sc, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, None)
            ),
        )
        _send_inputs([ev])

    def tap(self, vk: int, *, repeat: int = 1) -> None:
        sc = _scan_code(vk)
        bufs: list[INPUT] = []
        for _ in range(max(1, repeat)):
            bufs.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    union=_INPUTunion(
                        ki=KEYBDINPUT(vk, sc, KEYEVENTF_SCANCODE, 0, None)
                    ),
                )
            )
            bufs.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    union=_INPUTunion(
                        ki=KEYBDINPUT(
                            vk, sc, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, None
                        )
                    ),
                )
            )
        _send_inputs(bufs)

    def hotkey(self, *vks: int) -> None:
        # press in order, release in reverse → avoids ghosting
        downs = [
            INPUT(
                type=INPUT_KEYBOARD,
                union=_INPUTunion(
                    ki=KEYBDINPUT(vk, _scan_code(vk), KEYEVENTF_SCANCODE, 0, None)
                ),
            )
            for vk in vks
        ]
        ups = [
            INPUT(
                type=INPUT_KEYBOARD,
                union=_INPUTunion(
                    ki=KEYBDINPUT(
                        vk,
                        _scan_code(vk),
                        KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP,
                        0,
                        None,
                    )
                ),
            )
            for vk in reversed(vks)
        ]
        _send_inputs([*downs, *ups])

    # ---- Process / thread priority (optional) ----
    def boost_priority(self) -> None:
        # HIGH_PRIORITY_CLASS = 0x00000080; THREAD_PRIORITY_HIGHEST = 2
        kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), 0x00000080)
        kernel32.SetThreadPriority(kernel32.GetCurrentThread(), 2)
