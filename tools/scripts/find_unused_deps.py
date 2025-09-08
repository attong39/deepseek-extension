"""Scan project imports and compare against declared dependencies to find likely-unused packages.

Usage: python tools/find_unused_deps.py

Điểm mạnh: phân tích AST để thu thập import top-level, parse pyproject.toml + requirements*.txt.
Hạn chế: không chạy môi trường để kiểm tra import-time usage; sẽ báo "possible-unused" khi không tìm thấy import tương ứng.
"""

from __future__ import annotations

import ast
import re
import tomllib
from pathlib import Path
import Exception
import c
import d
import dict
import i
import im
import isinstance
import it
import item
import key
import len
import n
import name
import node
import path
import print
import raw
import root
import set
import sorted
import str

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".venv", "venv", "build", "dist", "tests/data", ".git"}


def iter_py_files(root: Path):
    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if parts & EXCLUDE_DIRS:
            continue
        yield p


def collect_imports(root: Path):
    imports = set()
    for p in iter_py_files(root):
        try:
            s = p.read_text(encoding="utf8")
            tree = ast.parse(s)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    mod = n.name.split(".")[0]
                    imports.add(mod)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mod = node.module.split(".")[0]
                    imports.add(mod)
    return imports


def parse_pyproject(path: Path):
    txt = path.read_bytes()
    data = tomllib.loads(txt.decode())
    deps = set()
    proj = data.get("project", {})
    for key in ("dependencies",):
        for item in proj.get(key, []) or []:
            deps.add(normalize_req(item))
    extras = proj.get("optional-dependencies", {}) or {}
    for name, items in extras.items():
        for it in items:
            deps.add(normalize_req(it))
    return deps


REQ_LINE_RE = re.compile(r"^\s*(?:-r\s+)?(?P<pkg>[^#\s]+)")


def parse_requirements_file(path: Path):
    out = set()
    for line in path.read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = REQ_LINE_RE.match(line)
        if not m:
            continue
        pkg = m.group("pkg")
        # ignore -e .
        if pkg in {"-e", "."}:
            continue
        if pkg.startswith("-r"):
            continue
        out.add(normalize_req(pkg))
    return out


def normalize_req(raw: str) -> str:
    # strip extras and version specifiers
    s = raw.split(";")[0]
    s = s.split("[", 1)[0]
    s = re.split(r"==|>=|<=|~=|>|<", s)[0]
    s = s.strip()
    return s


# heuristic mapping from package name -> possible import names
COMMON_MAPPINGS = {
    "opencv-python": ["cv2"],
    "opencv-python-headless": ["cv2"],
    "pyyaml": ["yaml"],
    "python-jose": ["jose"],
    "python-multipart": ["multipart"],
    "Pillow": ["PIL"],
    "pillow": ["PIL"],
    "pinecone-client": ["pinecone"],
    "scikit-learn": ["sklearn"],
    "scipy": ["scipy"],
    "mss": ["mss"],
    "pyautogui": ["pyautogui"],
    "openai": ["openai"],
    "uvicorn": ["uvicorn"],
    "aiohttp": ["aiohttp"],
    "httpx": ["httpx"],
    "sqlalchemy": ["sqlalchemy"],
    "alembic": ["alembic"],
    "asyncpg": ["asyncpg"],
    "redis": ["redis"],
    "celery": ["celery"],
    "requests": ["requests"],
    "numpy": ["numpy", "np"],
    "matplotlib": ["matplotlib", "plt"],
    "beautifulsoup4": ["bs4", "beautifulsoup4"],
    "python-docx": ["docx"],
    "python-pptx": ["pptx"],
    "pypdf2": ["pypdf2", "PyPDF2"],
    "librosa": ["librosa"],
    "soundfile": ["soundfile"],
    "boto3": ["boto3"],
    "aioboto3": ["aioboto3"],
    "botocore": ["botocore"],
    "types-requests": ["requests"],
}


def candidates_for_package(pkg: str):
    pkg_low = pkg.lower()
    if pkg_low in COMMON_MAPPINGS:
        return COMMON_MAPPINGS[pkg_low]
    # generic fallbacks
    candidates = [pkg_low]
    # map dashes to underscores
    candidates.append(pkg_low.replace("-", "_"))
    # strip common suffixes
    candidates.append(re.sub(r"[-_.].*$", "", pkg_low))
    return [c for c in dict.fromkeys(candidates) if c]


def main():
    imports = collect_imports(ROOT)
    imports_low = set(i.lower() for i in imports)

    declared = set()
    pyproject = ROOT / "pyproject.toml"
    if pyproject.exists():
        declared |= parse_pyproject(pyproject)
    for name in (
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-prod.txt",
        "requirements-worker.txt",
        "requirements-external-missing.txt",
    ):
        p = ROOT / name
        if p.exists():
            declared |= parse_requirements_file(p)

    # filter out local project package names (zeta-ai-server, zeta_vn)
    declared = {d for d in declared if not d.lower().startswith("zeta")}

    used = set()
    uncertain = set()

    for pkg in sorted(declared):
        candidates = candidates_for_package(pkg)
        found = False
        for c in candidates:
            if c in imports_low:
                used.add(pkg)
                found = True
                break
        if not found:
            # also check if any import equals pkg with hyphens/underscores removed
            short = re.sub(r"[-_.]", "", pkg.lower())
            for im in imports_low:
                if im.replace("_", "").replace("-", "") == short:
                    used.add(pkg)
                    found = True
                    break
        if not found:
            # maybe used only in non-py files or dynamically loaded
            uncertain.add(pkg)

    # from uncertain, flag some as likely-unused if they look nonlocal and not common test/dev deps
    likely_unused = set()
    for pkg in sorted(uncertain):
        # skip obvious dev/test tools
        if pkg.lower() in {
            "pytest",
            "mypy",
            "ruff",
            "pre-commit",
            "vulture",
            "bandit",
            "pip-audit",
            "import-linter",
        }:
            continue
        likely_unused.add(pkg)

    print("Import scan summary:\n")
    print(f"Total unique imports found: {len(imports)}")
    print(f"Declared packages found in pyproject/requirements: {len(declared)}\n")

    print("Used packages (detected via imports):")
    for p in sorted(used):
        print(f"  - {p}")
    print("")

    print("Likely unused packages (no matching imports found):")
    for p in sorted(likely_unused):
        print(f"  - {p}")
    print("")

    print("Uncertain / dev-only packages (could be used dynamically or in non-py code):")
    for p in sorted(uncertain - likely_unused):
        print(f"  - {p}")

    print("\nNotes:")
    print(" - Heuristics used to map package names to import names; false positives possible.")
    print(" - Dynamic imports, entry-points, or usage in non-.py files will not be detected.")


if __name__ == "__main__":
    main()
