from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol
import Exception
import UTC
import any
import asdict
import bool
import c_names
import cls
import cm
import cur_keys
import current
import dict
import diffs
import filepath
import get_type_hints
import getattr
import hash
import int
import isinstance
import issues
import k
import len
import list
import member
import methods
import mi
import n
import name
import node
import o_names
import obj
import old_keys
import om
import p
import package
import path
import protos
import reversed
import seg
import set
import snapshot_data
import sorted
import str
import tuple
import version

"""

import ast
import importlib
import inspect
import json
import os
import pkgutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol, get_type_hints

Tools: quét Protocols trong gói ports, sinh manifest, đối chiếu snapshot,
kiểm tra docstring/type/annotations.
"""


DEFAULT_PORTS_PKG = os.environ.get("PORTS_PACKAGE", "zeta_vn.core.ports")
SNAPSHOT_PATH = Path("contracts/ports_manifest.json")


@dataclass
class MethodInfo:
    name: str
    signature: str
    has_doc: bool
    has_annotations: bool


@dataclass
class ProtocolInfo:
    name: str
    module: str
    doc_hash: int
    filepath: str
    category: str
    methods: list[MethodInfo]


@dataclass
class Manifest:
    version: str
    generated_at: str
    package: str
    protocols: list[ProtocolInfo]


def _category_from_module(mod: str) -> str:
    """Heuristic: last segment (e.g., zeta_vn.core.ports.observability -> observability)."""
    parts = mod.split(".")
    for seg in reversed(parts):
        if seg in {
            "observability",
            "alerting",
            "alerts",
            "infrastructure",
            "ml",
            "memory",
            "security",
            "testing",
            "mlops",
            "cache",
            "backup",
            "documentation",
            "feature_toggles",
            "metrics",
        }:
            return seg
    return "uncategorized"


def _file_has_future_annotations(filepath: str) -> bool:
    """Check if file has 'from __future__ import annotations'."""
    try:
        src = Path(filepath).read_text(encoding="utf-8")
        tree = ast.parse(src)
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                if any(n.name == "annotations" for n in node.names):
                    return True
        return False
    except Exception:
        return False


def _iter_protocol_classes(package: str):
    """Iterate over all Protocol classes in package."""
    pkg = importlib.import_module(package)
    for mod in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        try:
            m = importlib.import_module(mod.name)
            for _name, obj in inspect.getmembers(m, inspect.isclass):
                # Protocol marker (_is_protocol) ổn định từ Python 3.8+
                if getattr(obj, "_is_protocol", False) and obj is not Protocol:
                    yield obj
        except Exception:
            # Skip modules that can't be imported
            continue


def gather_manifest(
    package: str = DEFAULT_PORTS_PKG, version: str = "1.0.0"
) -> Manifest:
    """Gather all Protocol information into manifest."""
    protos: list[ProtocolInfo] = []

    for cls in _iter_protocol_classes(package):
        try:
            src_file = inspect.getsourcefile(cls) or ""
            mod = cls.__module__
            doc = inspect.getdoc(cls) or ""
            methods: list[MethodInfo] = []

            for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
                if name.startswith("_"):
                    continue

                sig = str(inspect.signature(member))
                doc_ok = bool(inspect.getdoc(member))

                try:
                    hints = get_type_hints(member, include_extras=True)
                    # Require return annotation & at least one param annotation (nếu có param)
                    has_ann = ("return" in hints) or any(
                        k != "return" for k in hints
                    )
                except Exception:
                    has_ann = False

                methods.append(
                    MethodInfo(
                        name=name,
                        signature=sig,
                        has_doc=doc_ok,
                        has_annotations=has_ann,
                    )
                )

            protos.append(
                ProtocolInfo(
                    name=cls.__name__,
                    module=mod,
                    doc_hash=hash(doc),
                    filepath=src_file,
                    category=_category_from_module(mod),
                    methods=sorted(methods, key=lambda m: m.name),
                )
            )
        except Exception:
            # Không làm hỏng pipeline khi gặp 1 lớp lỗi; tiếp tục quét
            continue

    protos.sort(key=lambda p: (p.category, p.module, p.name))
    return Manifest(
        version=version,
        generated_at=datetime.now(UTC).isoformat(),
        package=package,
        protocols=protos,
    )


def write_snapshot(m: Manifest, path: Path = SNAPSHOT_PATH) -> None:
    """Write manifest to snapshot file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "version": m.version,
        "generated_at": m.generated_at,
        "package": m.package,
        "protocols": [
            {
                "name": p.name,
                "module": p.module,
                "doc_hash": p.doc_hash,
                "filepath": p.filepath,
                "category": p.category,
                "methods": [asdict(mi) for mi in p.methods],
            }
            for p in m.protocols
        ],
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_snapshot(path: Path = SNAPSHOT_PATH) -> dict[str, Any]:
    """Load snapshot from file."""
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_for_compare(data: dict[str, Any]) -> dict[str, Any]:
    """Chỉ giữ shape ảnh hưởng breaking changes (tên + chữ ký methods)."""
    return {
        "package": data.get("package"),
        "protocols": [
            {
                "name": p["name"],
                "module": p["module"],
                "methods": [
                    {"name": m["name"], "signature": m["signature"]}
                    for m in p.get("methods", [])
                ],
            }
            for p in data.get("protocols", [])
        ],
    }


def compare_with_snapshot(
    current: Manifest, snapshot_data: dict[str, Any]
) -> tuple[bool, list[str]]:
    """Compare current manifest with snapshot to detect breaking changes."""
    cur = _normalize_for_compare(
        json.loads(
            json.dumps(
                {
                    "package": current.package,
                    "protocols": [
                        {
                            "name": p.name,
                            "module": p.module,
                            "methods": [
                                {"name": m.name, "signature": m.signature}
                                for m in p.methods
                            ],
                        }
                        for p in current.protocols
                    ],
                }
            )
        )
    )
    old = _normalize_for_compare(snapshot_data)
    diffs: list[str] = []

    # Create lookup maps
    old_idx = {
        (p["module"], p["name"]): {m["name"]: m["signature"] for m in p["methods"]}
        for p in old["protocols"]
    }
    cur_idx = {
        (p["module"], p["name"]): {m["name"]: m["signature"] for m in p["methods"]}
        for p in cur["protocols"]
    }

    # Added/removed protocols
    old_keys, cur_keys = set(old_idx.keys()), set(cur_idx.keys())
    for k in sorted(cur_keys - old_keys):
        diffs.append(f"+ Added protocol: {k}")
    for k in sorted(old_keys - cur_keys):
        diffs.append(f"- Removed protocol: {k}")

    # Method changes in existing protocols
    for k in sorted(cur_keys & old_keys):
        om, cm = old_idx[k], cur_idx[k]
        o_names, c_names = set(om.keys()), set(cm.keys())

        for m in sorted(c_names - o_names):
            diffs.append(f"+ {k}: added method {m}{cm[m]}")
        for m in sorted(o_names - c_names):
            diffs.append(f"- {k}: removed method {m}{om[m]}")
        for m in sorted(c_names & o_names):
            if om[m] != cm[m]:
                diffs.append(f"* {k}: signature changed {m}: {om[m]} -> {cm[m]}")

    is_same = len(diffs) == 0
    return is_same, diffs


def validate_quality(m: Manifest) -> list[str]:
    """Validate quality requirements for protocols."""
    issues: list[str] = []

    for p in m.protocols:
        if not _file_has_future_annotations(p.filepath):
            issues.append(
                f"[annotations] missing __future__.annotations in {p.filepath}"
            )

        for mi in p.methods:
            if not mi.has_doc:
                issues.append(f"[docstring] {p.name}.{mi.name} missing docstring")
            if not mi.has_annotations:
                issues.append(f"[typing] {p.name}.{mi.name} missing type hints")

    return issues
