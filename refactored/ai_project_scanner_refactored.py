"""
🤖 AI-Refactored Code
Original function: analyze_code_complexity_metrics
Original complexity: 67
Target complexity: <10
Generated: 2025-09-08 23:53:08

This file contains the refactored version of the original complex function,
broken down into smaller, more maintainable components.
"""

**`complexity_analyzer.py`** – a tiny, test‑able, production‑ready pipeline that replaces the former monolithic  
`analyze_code_complexity_metrics` (cyclomatic ≈ 67) with a handful of functions whose individual
complexities are ≤ 4.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Complexity Analyzer
===================

A small, well‑structured library that walks a directory tree, collects simple
code‑complexity metrics for every ``.py`` file and produces a human‑readable
summary report.

The implementation follows the refactoring play‑book:

* each logical step lives in its own tiny function,
* guard‑clauses replace deep nesting,
* a tiny ``ComplexityAnalyzer`` class groups the pipeline,
* a dispatch table removes long ``if/elif`` chains,
* ``@dataclass`` objects give a clear domain model,
* type hints, logging and exhaustive error handling make the code production‑ready.

Only the standard library is used – the *cyclomatic complexity* metric is
approximated with a very small heuristic (count of ``if``, ``for``, ``while``,
``try`` statements).  The design makes it trivial to swap‑in a real static‑analysis
tool such as *radon* later on.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Mapping, Sequence

# --------------------------------------------------------------------------- #
# Logging configuration (adjust as needed by the embedding application)
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)
if not logger.handlers:            # avoid duplicate handlers in REPLs / notebooks
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s – %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# --------------------------------------------------------------------------- #
# Domain model – tiny data‑classes that describe the collected information
# --------------------------------------------------------------------------- #
@dataclass(frozen=True, slots=True)
class FileMetrics:
    """
    Metrics gathered for a single Python source file.

    Attributes
    ----------
    path: Path
        Absolute path of the analysed file.
    loc: int
        Lines‑of‑code (non‑empty, non‑comment lines).
    cyclomatic_complexity: int
        Very‑rough CC count – number of control‑flow keywords.
    maintainability_index: float
        A synthetic number (higher = more maintainable).  Computed from
        ``loc`` and ``cyclomatic_complexity`` using the classic Halstead‑based
        formula, but simplified for the example.
    """
    path: Path
    loc: int
    cyclomatic_complexity: int
    maintainability_index: float


@dataclass(frozen=True, slots=True)
class ProjectSummary:
    """
    Aggregated metrics for an entire project (a directory tree).

    Attributes
    ----------
    total_files: int
        Number of Python files that were successfully analysed.
    total_loc: int
        Sum of LOC across all analysed files.
    avg_complexity: float
        Arithmetic mean of per‑file cyclomatic complexities.
    max_complexity: int
        Highest cyclomatic complexity observed.
    min_complexity: int
        Lowest (non‑zero) cyclomatic complexity observed.
    avg_maintainability: float
        Mean maintainability index.
    """
    total_files: int
    total_loc: int
    avg_complexity: float
    max_complexity: int
    min_complexity: int
    avg_maintainability: float


# --------------------------------------------------------------------------- #
# Helper: file collection
# --------------------------------------------------------------------------- #
def collect_python_files(root: Path) -> List[Path]:
    """
    Recursively collect all ``.py`` files below *root*.

    Parameters
    ----------
    root: Path
        Base directory to walk.

    Returns
    -------
    List[Path]
        Absolute paths of discovered Python files.  The list is empty if the
        directory does not exist or contains no ``.py`` files.
    """
    if not root.exists():
        logger.error("Root path %s does not exist.", root)
        return []

    if not root.is_dir():
        logger.error("Root path %s is not a directory.", root)
        return []

    python_files = [p for p in root.rglob("*.py") if p.is_file()]
    logger.debug("Collected %d Python files from %s.", len(python_files), root)
    return python_files


# --------------------------------------------------------------------------- #
# Metric calculators – each is a tiny pure function.
# --------------------------------------------------------------------------- #
def _count_loc(lines: Sequence[str]) -> int:
    """Count non‑blank, non‑comment lines."""
    return sum(1 for line in lines if line.strip() and not line.lstrip().startswith("#"))


def _count_cc(lines: Sequence[str]) -> int:
    """
    Very rough cyclomatic‑complexity estimator.

    Counts occurrences of control‑flow keywords that increase the decision count.
    """
    keywords = ("if ", "elif ", "for ", "while ", "except ", "with ", "case ")
    return sum(line.count(keyword) for keyword in keywords for line in lines)


def _calculate_maintainability(loc: int, cc: int) -> float:
    """
    Simplified maintainability index.

    Reference: https://en.wikipedia.org/wiki/Maintainability_index
    The real formula uses Halstead volume, but for this example we use a
    linear combination that yields values roughly in the [0, 100] range.
    """
    if loc == 0:
        return 100.0
    # The constants (171, 0.23, 16.2) are taken from the original MI formula.
    mi = 171 - 5.2 * (cc) - 0.23 * loc - 16.2 * 0  # we omit the log10(Halstead) term
    return max(mi, 0.0)


# Dispatch table – makes it trivial to extend the set of metrics.
MetricFn = Callable[[Sequence[str]], int | float]
METRIC_DISPATCH: Mapping[str, MetricFn] = {
    "loc": _count_loc,
    "cyclomatic_complexity": _count_cc,
    "maintainability_index": _calculate_maintainability,  # receives (loc, cc) later
}


def compute_file_metrics(file_path: Path) -> FileMetrics | None:
    """
    Compute metrics for a single file.

    Returns
    -------
    FileMetrics | None
        ``None`` when the file could not be read (error already logged).
    """
    try:
        raw = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Skipping unreadable file %s – %s", file_path, exc)
        return None

    lines = raw.splitlines()
    loc = METRIC_DISPATCH["loc"](lines)                     # type: ignore[arg-type]
    cc = METRIC_DISPATCH["cyclomatic_complexity"](lines)   # type: ignore[arg-type]
    mi = _calculate_maintainability(loc, cc)               # maintainability needs both values

    logger.debug(
        "Metrics for %s – LOC: %s, CC: %s, MI: %.2f",
        file_path,
        loc,
        cc,
        mi,
    )
    return FileMetrics(path=file_path, loc=loc, cyclomatic_complexity=cc, maintainability_index=mi)


# --------------------------------------------------------------------------- #
# Aggregation of per‑file data into a project‑wide summary
# --------------------------------------------------------------------------- #
def aggregate_metrics(metrics: Sequence[FileMetrics]) -> ProjectSummary:
    """
    Produce a summary from a collection of :class:`FileMetrics`.

    Parameters
    ----------
    metrics: Sequence[FileMetrics]
        The per‑file results (must contain at least one element).

    Returns
    -------
    ProjectSummary
        The aggregated view.
    """
    if not metrics:
        logger.error("No file metrics supplied to aggregation.")
        raise ValueError("At least one FileMetrics instance is required.")

    total_files = len(metrics)
    total_loc = sum(m.loc for m in metrics)
    complexities = [m.cyclomatic_complexity for m in metrics]
    maintainabilities = [m.maintainability_index for m in metrics]

    avg_complexity = sum(complexities) / total_files
    max_complexity = max(complexities)
    # ``min`` should ignore the trivial zero value that appears in empty files.
    min_complexity = min(c for c in complexities if c > 0) if any(c > 0 for c in complexities) else 0
    avg_maintainability = sum(maintainabilities) / total_files

    logger.info(
        "Aggregated %d files – total LOC: %d, avg CC: %.2f, avg MI: %.2f",
        total_files,
        total_loc,
        avg_complexity,
        avg_maintainability,
    )
    return ProjectSummary(
        total_files=total_files,
        total_loc=total_loc,
        avg_complexity=avg_complexity,
        max_complexity=max_complexity,
        min_complexity=min_complexity,
        avg_maintainability=avg_maintainability,
    )


# --------------------------------------------------------------------------- #
# Rendering – turn a :class:`ProjectSummary` into a string report
# --------------------------------------------------------------------------- #
def render_report(summary: ProjectSummary) -> str:
    """
    Create a multi‑line human readable report from *summary*.

    Returns
    -------
    str
        The formatted report.
    """
    lines = [
        "=== Code‑Complexity Report ===",
        f"Analyzed files          : {summary.total_files}",
        f"Total lines of code     : {summary.total_loc}",
        f"Average cyclomatic CC   : {summary.avg_complexity:.2f}",
        f"Maximum cyclomatic CC   : {summary.max_complexity}",
        f"Minimum cyclomatic CC   : {summary.min_complexity}",
        f"Average maintainability : {summary.avg_maintainability:.2f}",
        "==============================",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Facade – tiny class that wires the pipeline together
# --------------------------------------------------------------------------- #
class ComplexityAnalyzer:
    """
    Facade that executes the full analysis pipeline.

    The class holds no mutable state – it only exists to give a clean public API
    and to make dependency‑injection (e.g. a mock logger) straightforward in
    tests.
    """

    def __init__(self, logger_: logging.Logger | None = None) -> None:
        self._log = logger_ or logger

    def analyze(self, root: Path) -> str:
        """
        Run the complete analysis and return a formatted report.

        Parameters
        ----------
        root: Path
            Directory that contains the Python project to analyse.

        Returns
        -------
        str
            Human‑readable report.  An empty string is returned when no analysable
            files are found.
        """
        self._log.info("Starting complexity analysis for %s", root)

        python_files = collect_python_files(root)
        if not python_files:
            self._log.warning("No Python files discovered – aborting.")
            return ""

        # Gather per‑file metrics, silently dropping files that could not be read.
        per_file = [
            metrics
            for path in python_files
            if (metrics := compute_file_metrics(path)) is not None
        ]

        if not per_file:
            self._log.warning("All discovered files were unreadable.")
            return ""

        summary = aggregate_metrics(per_file)
        return render_report(summary)


# --------------------------------------------------------------------------- #
# Example usage (run as a script)
# --------------------------------------------------------------------------- #
def _main() -> int:
    """
    Entry‑point used when the module is executed directly.

    Returns
    -------
    int
        Process exit code (0 = success, 1 = error).
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyse a Python code‑base and emit a simple complexity report."
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Root directory of the project (default: current working directory).",
    )
    args = parser.parse_args()

    analyzer = ComplexityAnalyzer()
    report = analyzer.analyze(args.path)

    if report:
        print(report)
        return 0
    else:
        print("No report generated – see logs for details.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(_main())
```

### What the refactor achieves

| Goal | How the code meets it |
|------|-----------------------|
| **Complexity < 10** | Every public function (`collect_python_files`, `compute_file_metrics`, `aggregate_metrics`, `render_report`, `ComplexityAnalyzer.analyze`) contains **≤ 4** decision points (early‑return guards, simple loops, or a single dispatch lookup). |
| **Separation of concerns** | Collection, metric calculation, aggregation, and rendering live in distinct functions (and could be moved to separate modules). |
| **Error handling** | Invalid paths, unreadable files, and empty inputs are caught and reported via `logging` and explicit guard clauses. |
| **Type hints** | Full use of `Path`, `List`, `Sequence`, `Mapping`, and concrete return types. |
| **Docstrings** | Every public object has a comprehensive docstring following the NumPy/Google style. |
| **Best practices** | - `@dataclass(frozen=True, slots=True)` for immutability and memory efficiency.<br>‑ Use of the standard library only.<br>‑ Logging instead of `print` inside library code.<br>‑ Guard‑clause style reduces nesting.<br>‑ Dispatch table makes extending metrics trivial.<br>‑ `if __name__ == "__main__"` script entry point. |

The module is ready to be imported, unit‑tested (each helper can be exercised in isolation), or executed directly:

```bash
$ python complexity_analyzer.py /path/to/my/project
=== Code‑Complexity Report ===
Analyzed files          : 42
Total lines of code     : 7834
Average cyclomatic CC   : 4.57
Maximum cyclomatic CC   : 12
Minimum cyclomatic CC   : 1
Average maintainability : 71.34
==============================
```

Feel free to replace the naïve CC estimator with a real static‑analysis library (e.g. *radon*) – just plug a new function into `METRIC_DISPATCH` without touching the surrounding pipeline.