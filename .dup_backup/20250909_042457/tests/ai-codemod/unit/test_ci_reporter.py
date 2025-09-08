# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportMissingImports=false
import sys
from pathlib import Path
import RuntimeError
import comment
import dict
import object
import range
import results
import str


def _add_ai_codemod_to_syspath() -> None:
    root = Path(__file__).resolve()
    for _ in range(10):
        if (root / "tools" / "ai-codemod").exists():
            break
        if root.parent == root:
            raise RuntimeError("Cannot locate repo root for tools/ai-codemod")
        root = root.parent
    sys.path.insert(0, str(root / "tools" / "ai-codemod"))


_add_ai_codemod_to_syspath()
from ci_reporter import generate_comment  # type: ignore  # noqa: E402


def test_ci_reporter_generate_comment() -> None:
    """Test CI reporter comment generation."""
    results: dict[str, object] = {
        "total_files": 10,
        "total_findings": 5,
        "applied_count": 2,
        "dry_run": False,
        "findings": [
            {
                "type": "missing_type_hints",
                "file_path": "src/utils.py",
                "description": "Function foo missing return type hint",
                "confidence": 0.8,
                "complexity": "medium",
            }
        ],
    }

    comment: str = generate_comment(results)

    assert "AI Code Review Results" in comment
    assert "Files analyzed: 10" in comment
    assert "Findings identified: 5" in comment
    assert "Function foo missing return type hint" in comment


def test_ci_reporter_empty_findings() -> None:
    """Test CI reporter with no findings."""
    results: dict[str, object] = {
        "total_files": 0,
        "total_findings": 0,
        "applied_count": 0,
        "dry_run": True,
        "findings": [],
    }

    comment: str = generate_comment(results)

    assert "No significant issues found" in comment or "Findings identified: 0" in comment
