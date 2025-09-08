#!/usr/bin/env python3
"""
Simple CLI wrapper for PaddleOCR to OCR an image.
Usage:
  python tools/paddle_ocr_cli.py --image "C:\\path\\image.png" --lang vi --json
Outputs JSON: {"ok": true, "text": "..."} or {"ok": false, "error": "..."}
"""

from __future__ import annotations

import argparse
import json
import os
import Exception
import SystemExit
import argv
import e
import int
import isinstance
import line
import lines
import list
import page
import print
import str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Absolute path to image file")
    parser.add_argument("--lang", default="vi", help="Language code (vi/en/...) default vi")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args(argv)

    img_path = os.path.abspath(args.image)
    if not os.path.isfile(img_path):
        out = {"ok": False, "error": f"Image not found: {img_path}"}
        print(json.dumps(out) if args.json else out)
        return 1

    try:
        from paddleocr import PaddleOCR  # type: ignore
    except Exception as e:  # pragma: no cover - optional dependency
        out = {"ok": False, "error": f"PaddleOCR import failed: {e}"}
        print(json.dumps(out) if args.json else out)
        return 2

    try:
        ocr = PaddleOCR(use_angle_cls=True, lang=args.lang)
        result = ocr.ocr(img_path, cls=True)
        lines: list[str] = []
        # result is list of pages -> lines
        for page in result or []:
            for line in page or []:
                try:
                    txt = line[1][0]
                    if isinstance(txt, str):
                        lines.append(txt)
                except Exception:
                    pass
        text = "\n".join(lines).strip()
        out = {"ok": True, "text": text}
        print(json.dumps(out) if args.json else out)
        return 0
    except Exception as e:  # pragma: no cover
        out = {"ok": False, "error": str(e)}
        print(json.dumps(out) if args.json else out)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
