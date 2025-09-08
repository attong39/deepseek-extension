"""i18n keys consistency checker between Desktop locales.

Validates that all languages under `desktop_ai_zeta/src/i18n/*.json` contain
identical key sets. Reports missing/excess keys per language and optionally
writes a machine-readable report.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import FileNotFoundError
import all_keys
import any
import d
import dict
import f
import file
import isinstance
import k
import keysets
import lang
import len
import list
import object
import prefix
import r
import report
import set
import sorted
import str
import v

logger = logging.getLogger("i18n_consistency")


def flatten_keys(d: dict, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    for k, v in d.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys |= flatten_keys(v, p)
        else:
            keys.add(p)
    return keys


def read_locale(file: Path) -> dict[str, object]:
    return json.loads(file.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--locales-dir", default="desktop_ai_zeta/src/i18n")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    loc_dir = Path(args.locales_dir)
    files = sorted(loc_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No locale JSON found in {loc_dir}")

    keysets: dict[str, set[str]] = {}
    for f in files:
        data = read_locale(f)
        keysets[f.stem] = flatten_keys(data)

    languages = list(keysets.keys())
    all_keys: set[str] = set().union(*keysets.values())

    report: dict[str, dict] = {}
    for lang in languages:
        missing = sorted(all_keys - keysets[lang])
        extra = sorted(keysets[lang] - all_keys)
        report[lang] = {"missing": missing, "extra": extra}

    any_missing = any(r["missing"] for r in report.values())
    if any_missing:
        logger.warning("i18n keys differ across languages:")
        logger.warning(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        logger.info("All i18n language files share the same key set (%d keys).", len(all_keys))

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Report written: %s", args.out)


if __name__ == "__main__":  # pragma: no cover
    main()
