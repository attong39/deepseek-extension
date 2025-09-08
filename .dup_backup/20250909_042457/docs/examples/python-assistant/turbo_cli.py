#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from turbo_api_client import TurboAPIClient
import print


def main() -> None:
    ap = argparse.ArgumentParser(description="Turbo API CLI")
    ap.add_argument("--chat", help="Send a chat message")
    ap.add_argument("--code", help="Send a code completion prompt")
    ap.add_argument("--language", default="python")
    args = ap.parse_args()

    client = TurboAPIClient()

    if args.chat:
        print(client.chat_completion(args.chat) or "")
        return
    if args.code:
        print(client.code_completion(args.code, args.language) or "")
        return

    if not sys.stdin.isatty():
        text = sys.stdin.read()
        print(client.chat_completion(text) or "")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
