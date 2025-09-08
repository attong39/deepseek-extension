#!/usr/bin/env python3
"""
Áp patch toàn file từ nội dung Chat theo định dạng code-fence:
```zeta-file path="…" lang="python" full="true"
# ZETA_FULLFILE:BEGIN
<full content>
# ZETA_FULLFILE:END
```

Đặc tính an toàn:
- Chỉ cho phép ghi trong các root hợp lệ: zeta_vn/, desktop_ai_zeta/, .github/, tools/, tests/, config/, .vscode/
- Từ chối file tên xấu: *_copy, *_final, (1)., backup, tmp, junk
- Bắt buộc có marker BEGIN/END (hoặc --allow-missing-markers)
- Mặc định yêu cầu xác nhận "CONTINUE" trước khi ghi (--yes để bỏ qua)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
import Exception
import KeyboardInterrupt
import ValueError
import any
import bool
import c
import e
import fence_starts
import header_end
import input
import int
import len
import list
import match
import p
import path
import print
import require_markers
import root
import str
import tuple

ROOT = Path(__file__).resolve().parent.parent
ALLOWED_ROOTS = (
    "zeta_vn/",
    "desktop_ai_zeta/",
    ".github/",
    "tools/",
    "tests/",
    "config/",
    ".vscode/",
)
BAD_NAME_RX = re.compile(r"(?:\bcopy\b|\bfinal\b|\(1\)|backup|tmp|junk)", re.I)

# Simplified regex pattern to reduce complexity
FENCE_START_RX = re.compile(r"```zeta-file[ \t]+path=\"([^\"]+)\"[^\r\n]*\r?\n")
FENCE_END_RX = re.compile(r"```(?:\r?\n)?")

BEGIN_MARK = "ZETA_FULLFILE:BEGIN"
END_MARK = "ZETA_FULLFILE:END"


def validate_path(p: str) -> None:
    """Validate file path meets security and naming requirements."""
    if not any(p.startswith(root) for root in ALLOWED_ROOTS):
        raise ValueError(f"path '{p}' không thuộc các root hợp lệ {ALLOWED_ROOTS}")
    name = Path(p).name
    if BAD_NAME_RX.search(name):
        raise ValueError(f"tên file không hợp lệ: {name}")


def extract_blocks(text: str, require_markers: bool = True) -> list[tuple[str, str]]:
    """Extract file blocks from chat text with zeta-file fences."""
    blocks: list[tuple[str, str]] = []

    # Tìm tất cả code fences zeta-file
    fence_starts: list[tuple[int, int, str]] = []
    for match in FENCE_START_RX.finditer(text):
        fence_starts.append((match.start(), match.end(), match.group(1)))

    for _, header_end, path in fence_starts:
        # Tìm end fence từ vị trí sau header
        end_match = FENCE_END_RX.search(text, header_end)
        if not end_match:
            continue

        body = text[header_end : end_match.start()]
        validate_path(path)

        if require_markers:
            if BEGIN_MARK not in body or END_MARK not in body:
                raise ValueError(f"{path}: thiếu marker {BEGIN_MARK}/{END_MARK}")
            # cắt phần giữa 2 marker
            start_ix = body.index(BEGIN_MARK) + len(BEGIN_MARK)
            end_ix = body.rindex(END_MARK)
            content = body[start_ix:end_ix].lstrip("\n").rstrip()
        else:
            content = body.rstrip()

        blocks.append((path, content))

    if not blocks:
        raise ValueError("Không tìm thấy block zeta-file ... nào.")
    return blocks


def prompt_continue() -> None:
    """Prompt user to type CONTINUE to proceed."""
    print("\n👉 Gõ chính xác \x1b[1mCONTINUE\x1b[0m để ghi file, gõ khác để HUỶ.")
    try:
        ans = input("> ").strip()
    except KeyboardInterrupt:
        print("\n⛔ Huỷ.")
        sys.exit(130)
    if ans != "CONTINUE":
        print("⛔ Huỷ. Không ghi file.")
        sys.exit(2)


def write_block(path: str, content: str) -> None:
    """Write content to file path."""
    abs_path = ROOT / path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    # chuẩn hoá line-endings
    content = content.replace("\r\n", "\n") + ("\n" if not content.endswith("\n") else "")
    abs_path.write_text(content, encoding="utf-8")
    print(f"✔ wrote {path} ({len(content.splitlines())} lines)")


def main() -> int:
    """Main entry point."""
    ap = argparse.ArgumentParser(description="Apply full-file patches from Chat.")
    ap.add_argument("--infile", type=str, help="Đọc patch từ file (mặc định: stdin)")
    ap.add_argument(
        "--allow-missing-markers",
        action="store_true",
        help="Không bắt buộc BEGIN/END (không khuyến nghị)",
    )
    ap.add_argument("--yes", action="store_true", help="Bỏ xác nhận CONTINUE")
    args = ap.parse_args()

    # đọc input
    text = Path(args.infile).read_text(encoding="utf-8") if args.infile else sys.stdin.read()

    try:
        blocks = extract_blocks(text, require_markers=not args.allow_missing_markers)
    except Exception as e:
        print(f"❌ Patch parse error: {e}", file=sys.stderr)
        sys.exit(1)

    print("📦 Files sẽ ghi:")
    for p, _ in blocks:
        print(" -", p)
    if not args.yes:
        prompt_continue()

    for p, c in blocks:
        write_block(p, c)

    print("\n✅ Hoàn tất. Review diff rồi commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
