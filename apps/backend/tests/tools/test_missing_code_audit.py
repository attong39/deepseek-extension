"""Tests for missing code audit functionality."""

from __future__ import annotations

from pathlib import Path

from scripts.missing_code_audit import scan_python_file, scan_typescript_file


def create_temp_file(tmp_path: Path, name: str, content: str) -> Path:
    """Helper to create temporary files for testing."""
import any
import content
import i
import isinstance
import len
import list
import name
import str
import tmp_path
    file_path = tmp_path / name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_python_stub_detection(tmp_path: Path) -> None:
    """Test detection of Python stub patterns."""
    # Test pass statement
    py_file = create_temp_file(
        tmp_path,
        "stub_pass.py",
        """
def function_with_pass() -> int:
    pass
""",
    )
    issues = scan_python_file(py_file)
    assert any(
        i.severity == "HIGH" and i.kind == "stub-function" and "pass" in i.message
        for i in issues
    )

    # Test ellipsis
    py_file = create_temp_file(
        tmp_path,
        "stub_ellipsis.py",
        """
def function_with_ellipsis() -> str:
    ...
""",
    )
    issues = scan_python_file(py_file)
    assert any(
        i.severity == "HIGH" and i.kind == "stub-function" and "…" in i.message
        for i in issues
    )

    # Test NotImplementedError
    py_file = create_temp_file(
        tmp_path,
        "stub_not_impl.py",
        """
def function_with_not_implemented() -> bool:
    raise NotImplementedError("Feature not implemented yet")
""",
    )
    issues = scan_python_file(py_file)
    assert any(
        i.severity == "HIGH"
        and i.kind == "stub-function"
        and "NotImplementedError" in i.message
        for i in issues
    )


def test_python_return_none_mismatch(tmp_path: Path) -> None:
    """Test detection of return None with non-Optional annotation."""
    py_file = create_temp_file(
        tmp_path,
        "return_mismatch.py",
        """
def should_return_int() -> int:
    if True:
        return None
    return 42
""",
    )
    issues = scan_python_file(py_file)
    assert any(
        i.severity == "MEDIUM"
        and i.kind == "none-return-mismatch"
        and "non-Optional" in i.message
        for i in issues
    )


def test_python_empty_class(tmp_path: Path) -> None:
    """Test detection of empty classes."""
    py_file = create_temp_file(
        tmp_path,
        "empty_class.py",
        """
class EmptyClass:
    pass
""",
    )
    issues = scan_python_file(py_file)
    assert any(
        i.severity == "LOW" and i.kind == "empty-class" and "empty" in i.message
        for i in issues
    )


def test_python_todo_markers(tmp_path: Path) -> None:
    """Test detection of TODO/FIXME markers."""
    py_file = create_temp_file(
        tmp_path,
        "todo_markers.py",
        """
# TODO: Implement this function
def incomplete_function():
    # FIXME: This is broken
    pass

# HACK: Temporary workaround
def hacky_function():
    return "hack"
""",
    )
    issues = scan_python_file(py_file)
    todo_issues = [i for i in issues if i.kind == "todo-marker"]
    assert len(todo_issues) >= 3  # Should find TODO, FIXME, HACK


def test_typescript_not_implemented(tmp_path: Path) -> None:
    """Test detection of TypeScript 'Not implemented' errors."""
    ts_file = create_temp_file(
        tmp_path,
        "not_impl.ts",
        """
function incompleteFunction(): number {
    throw new Error('Not implemented');
}

const arrowFunction = (): string => {
    throw new Error("Not implemented");
};
""",
    )
    issues = scan_typescript_file(ts_file)
    not_impl_issues = [i for i in issues if i.kind == "ts-not-implemented"]
    assert len(not_impl_issues) >= 2


def test_typescript_any_usage(tmp_path: Path) -> None:
    """Test detection of 'any' type usage."""
    ts_file = create_temp_file(
        tmp_path,
        "any_usage.ts",
        """
function badFunction(param: any): any {
    return param as any;
}

interface BadInterface {
    prop: any;
}
""",
    )
    issues = scan_typescript_file(ts_file)
    any_issues = [i for i in issues if i.kind == "any-type"]
    assert len(any_issues) >= 3  # Should find multiple 'any' usages


def test_typescript_todo_markers(tmp_path: Path) -> None:
    """Test detection of TODO/FIXME in TypeScript."""
    ts_file = create_temp_file(
        tmp_path,
        "todo.ts",
        """
// TODO: Add proper type annotations
function needsWork(): void {
    // FIXME: This logic is wrong
    console.log("broken");
}

/*
 * HACK: Quick fix for deadline
 */
const quickFix = () => {};
""",
    )
    issues = scan_typescript_file(ts_file)
    todo_issues = [i for i in issues if i.kind == "todo-marker"]
    assert len(todo_issues) >= 3


def test_syntax_error_handling(tmp_path: Path) -> None:
    """Test handling of syntax errors in Python files."""
    py_file = create_temp_file(
        tmp_path,
        "syntax_error.py",
        """
def broken_syntax(
    # Missing closing parenthesis
""",
    )
    issues = scan_python_file(py_file)
    assert any(i.severity == "HIGH" and i.kind == "syntax-error" for i in issues)


def test_file_read_error_handling(tmp_path: Path) -> None:
    """Test handling of files that cannot be read."""
    # Create a file with invalid encoding
    binary_file = tmp_path / "binary.ts"
    binary_file.write_bytes(b"\xff\xfe\x00\x00invalid")

    issues = scan_typescript_file(binary_file)
    # Should handle gracefully, not crash
    assert isinstance(issues, list)
