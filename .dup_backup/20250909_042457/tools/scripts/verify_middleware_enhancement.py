#!/usr/bin/env python3
"""
Middleware Enhancement Verification Script

Verify completeness improvements sau khi enhance middleware files.
"""

from __future__ import annotations

import ast
from pathlib import Path
import Exception
import bool
import count
import dict
import e
import file_path
import float
import found
import int
import isinstance
import len
import line
import list
import max
import min
import node
import pattern
import pattern_name
import pattern_text
import print
import str
import sum
import tuple
import x


def count_implementation_features(file_path: str) -> dict[str, int]:
    """Count implementation features in a Python file."""
    if not Path(file_path).exists():
        return {"functions": 0, "classes": 0, "lines": 0, "docstrings": 0, "todos": 0}

    try:
        content = Path(file_path).read_text(encoding="utf-8")
        tree = ast.parse(content)

        functions = 0
        classes = 0
        docstrings = 0
        todos = content.lower().count("todo")
        lines = len([line for line in content.split("\n") if line.strip()])

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions += 1
                # Check for docstring
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    docstrings += 1

            elif isinstance(node, ast.ClassDef):
                classes += 1
                # Check for docstring
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    docstrings += 1

        return {
            "functions": functions,
            "classes": classes,
            "lines": lines,
            "docstrings": docstrings,
            "todos": todos,
        }

    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {"functions": 0, "classes": 0, "lines": 0, "docstrings": 0, "todos": 0}


def calculate_completeness_score(features: dict[str, int]) -> float:
    """Calculate completeness score from features."""
    score = 0

    # Base score from implementation
    score += min(features["functions"] * 8, 40)  # Max 40 points for functions
    score += min(features["classes"] * 15, 30)  # Max 30 points for classes
    score += min(features["lines"] / 10, 20)  # Max 20 points for LOC

    # Documentation bonus
    if features["docstrings"] > 0:
        score += min(features["docstrings"] * 5, 10)  # Max 10 points for docs

    # Penalty for TODOs
    score -= features["todos"] * 2

    return max(0, min(100, score))


def get_quality_status(score: float) -> str:
    """Get quality status icon based on score."""
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    else:
        return "🔴"


def get_pattern_status(percentage: float) -> str:
    """Get pattern compliance status icon."""
    if percentage >= 80:
        return "✅"
    elif percentage >= 60:
        return "⚠️"
    else:
        return "❌"


def analyze_single_file(file_path: str) -> tuple[float, dict[str, int]]:
    """Analyze a single file and return score and features."""
    features = count_implementation_features(file_path)
    score = calculate_completeness_score(features)
    return score, features


def print_verification_results(results: list[tuple[str, float, dict[str, int]]]) -> None:
    """Print verification results summary."""
    total_score = sum(score for _, score, _ in results)

    print("📊 VERIFICATION RESULTS:")
    print(f"   Files analyzed: {len(results)}")
    print(f"   Average score: {total_score / len(results):.1f}")
    print()


def print_detailed_scores(results: list[tuple[str, float, dict[str, int]]]) -> tuple[int, int, int]:
    """Print detailed scores and return quality counts."""
    print("📋 DETAILED SCORES:")
    high_quality = medium_quality = low_quality = 0

    for file_path, score, features in results:
        filename = Path(file_path).name
        status = get_quality_status(score)

        if score >= 80:
            high_quality += 1
        elif score >= 60:
            medium_quality += 1
        else:
            low_quality += 1

        print(f"{status} {score:5.1f} — {filename}")
        print(
            f"     fn:{features['functions']}, cls:{features['classes']}, "
            f"loc:{features['lines']}, docs:{features['docstrings']}"
        )

    return high_quality, medium_quality, low_quality


def count_pattern_in_file(file_path: str, patterns: dict[str, str]) -> dict[str, bool]:
    """Count patterns in a single file."""
    if not Path(file_path).exists():
        return dict.fromkeys(patterns, False)

    content = Path(file_path).read_text(encoding="utf-8")
    results = {}

    for pattern_name, pattern_text in patterns.items():
        results[pattern_name] = pattern_text in content

    return results


def check_pattern_compliance(results: list[tuple[str, float, dict[str, int]]]) -> None:
    """Check pattern compliance across files."""
    print("🔧 PATTERN COMPLIANCE CHECK:")

    patterns = {
        "BaseHTTPMiddleware inheritance": "BaseHTTPMiddleware",
        "async dispatch method": "async def dispatch",
        "Error handling": "except",  # Simplified check
        "Logging integration": "logger",
        "Type hints": "from __future__ import annotations",
        "Docstrings": '"""',
    }

    pattern_counts = dict.fromkeys(patterns, 0)

    for file_path, _, _ in results:
        file_patterns = count_pattern_in_file(file_path, patterns)
        for pattern_name, found in file_patterns.items():
            if found:
                pattern_counts[pattern_name] += 1

    for pattern, count in pattern_counts.items():
        percentage = (count / len(results)) * 100
        status = get_pattern_status(percentage)
        print(f"   {status} {pattern}: {count}/{len(results)} ({percentage:.0f}%)")


def verify_middleware_files() -> None:
    """Verify enhanced middleware files."""
    print("🔍 MIDDLEWARE ENHANCEMENT VERIFICATION")
    print("=" * 50)

    # Key middleware files to verify
    middleware_files = [
        "zeta_vn/app/middleware/auth_middleware.py",
        "zeta_vn/app/middleware/metrics_middleware.py",
        "zeta_vn/app/middleware/zero_trust.py",
        "zeta_vn/app/middleware/logging.py",
        "zeta_vn/app/middleware/api_version.py",
        "zeta_vn/app/middleware/request_id.py",
        "zeta_vn/app/middleware/compression_middleware.py",
        "zeta_vn/app/middleware/cors_middleware.py",
        "zeta_vn/app/middleware/performance_middleware.py",
        "zeta_vn/app/middleware/rate_limiting.py",
        "zeta_vn/app/middleware/security_consolidated.py",
        "zeta_vn/app/middleware/security/__init__.py",
    ]

    results = []

    for file_path in middleware_files:
        if Path(file_path).exists():
            score, features = analyze_single_file(file_path)
            results.append((file_path, score, features))
        else:
            print(f"❌ Missing: {file_path}")

    # Sort by score (lowest first)
    results.sort(key=lambda x: x[1])

    print_verification_results(results)
    high_quality, medium_quality, low_quality = print_detailed_scores(results)

    print()
    print("📈 QUALITY SUMMARY:")
    print(f"   🟢 High quality (80+): {high_quality}")
    print(f"   🟡 Medium quality (60-79): {medium_quality}")
    print(f"   🔴 Needs improvement (<60): {low_quality}")

    print()
    check_pattern_compliance(results)

    print()
    if low_quality == 0:
        print("🎉 ALL MIDDLEWARE FILES MEET QUALITY STANDARDS!")
    else:
        print(f"⚠️  {low_quality} files still need improvement")
        print("   Run quality fixes for remaining issues")


if __name__ == "__main__":
    verify_middleware_files()
