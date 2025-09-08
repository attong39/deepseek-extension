import sys
import tempfile
from pathlib import Path
import RuntimeError
import dict
import object
import range
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


def test_engine_analyze_mode() -> None:
    """Test that engine analyze mode runs without errors."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create a simple config file
        config_content = """
        version: 1
        rules:
          - language: python
            allowed_transforms:
              - imports
            max_changes_per_file: 10
            max_files_per_run: 5
            excluded_paths:
              - "**/test_*"
        general:
          dry_run_by_default: true
          require_test_pass: true
          formatters:
            python: black
            typescript: prettier
        """

        config_path = temp_path / "test_config.yml"
        config_path.write_text(config_content)

        # Create a simple Python file to analyze
        src_dir = temp_path / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        test_file = src_dir / "example.py"
        test_file.write_text("import os\nimport sys\n\n\ndef example():\n    return 'hello'")

        # Initialize and run engine
        _add_ai_codemod_to_syspath()
        from engine import AICodemodEngine  # type: ignore

        engine = AICodemodEngine(temp_path, config_path)
        results: dict[str, object] = engine.analyze(files=[test_file])

        assert "findings" in results
        assert "total_files" in results
