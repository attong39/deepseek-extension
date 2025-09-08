import sys
import tempfile
from pathlib import Path
from typing import Any
import RuntimeError
import content
import dict
import object
import range
import reporter
import results
import str
import temp_dir

# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportMissingImports=false


def _add_ai_codemod_to_syspath() -> None:
    root = Path(__file__).resolve()
    for _ in range(10):
        if (root / "tools" / "ai-codemod").exists():
            break
        if root.parent == root:
            raise RuntimeError("Cannot locate repo root for tools/ai-codemod")
        root = root.parent
    sys.path.insert(0, str(root / "tools" / "ai-codemod"))


def test_markdown_reporter_generates_file() -> None:
    """Test that the markdown reporter creates a file with expected content."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _add_ai_codemod_to_syspath()
        from reporters.markdown_reporter import MarkdownReporter  # type: ignore

        reporter: Any = MarkdownReporter(temp_path)

        results: dict[str, object] = {
            "total_files": 5,
            "total_findings": 3,
            "applied_count": 0,
            "dry_run": True,
            "findings": [
                {
                    "type": "unused_import",
                    "file_path": "src/main.py",
                    "description": "Unused import os",
                    "confidence": 0.9,
                    "complexity": "low",
                }
            ],
        }

        output_path = temp_path / "test_report.md"
        reporter.generate_report(results, output_path)

        assert output_path.exists()
        content: str = output_path.read_text(encoding="utf-8")
        assert "AI Codemod Report" in content
        assert "Files analyzed: 5" in content
        assert "Unused import os" in content


def test_markdown_reporter_handles_empty_findings() -> None:
    """Test reporter with no findings."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        _add_ai_codemod_to_syspath()
        from reporters.markdown_reporter import MarkdownReporter  # type: ignore

        reporter: Any = MarkdownReporter(temp_path)

        results: dict[str, object] = {
            "total_files": 0,
            "total_findings": 0,
            "applied_count": 0,
            "dry_run": True,
            "findings": [],
        }

        output_path = temp_path / "empty_report.md"
        reporter.generate_report(results, output_path)

        assert output_path.exists()
        content: str = output_path.read_text(encoding="utf-8")
        assert "No significant issues found" in content or "Findings identified: 0" in content
