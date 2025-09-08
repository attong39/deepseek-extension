#!/usr/bin/env python3
"""
Duplicate Code Analyzer for Zeta AI Server
==========================================

Script phân tích toàn diện để phát hiện duplicate code và tối ưu hóa dự án.

Features:
- Phát hiện duplicate functions/classes
- Phân tích import redundant
- Tìm similar code blocks
- Kiểm tra unused code
- Đề xuất refactoring
- Tạo báo cáo chi tiết
"""

import ast
import difflib
import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import Exception
import alias
import any
import arg
import base
import block
import block1
import block2
import blocks
import chr
import count
import dict
import e
import enumerate
import f
import file_path
import files
import float
import i
import imp
import int
import isinstance
import len
import lines
import list
import node
import open
import output_dir
import pattern
import print
import project_root
import py_file
import self
import similarity_threshold
import sorted
import str
import suggestion
import sum
import tuple
import x


@dataclass
class CodeBlock:
    """Represents a code block for analysis."""

    file_path: str
    start_line: int
    end_line: int
    content: str
    hash_value: str
    node_type: str
    name: str = ""


@dataclass
class DuplicateReport:
    """Report for duplicate code findings."""

    duplicate_functions: list[tuple[str, list[CodeBlock]]]
    duplicate_classes: list[tuple[str, list[CodeBlock]]]
    similar_blocks: list[tuple[CodeBlock, CodeBlock, float]]
    redundant_imports: dict[str, list[str]]
    unused_imports: dict[str, list[str]]
    dead_code: list[CodeBlock]
    refactoring_suggestions: list[str]


class DuplicateCodeAnalyzer:
    """Main analyzer class for duplicate code detection."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.python_files = []
        self.code_blocks = []
        self.imports_map = defaultdict(list)
        self.function_signatures = defaultdict(list)
        self.class_signatures = defaultdict(list)

    def scan_project(self) -> None:
        """Scan project for Python files."""
        print("🔍 Scanning project files...")

        # Exclude patterns
        exclude_patterns = {
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "env",
            ".pytest_cache",
            "node_modules",
            ".mypy_cache",
            "migrations",
            "*.pyc",
            "*.pyo",
            "*.pyd",
        }

        for py_file in self.project_root.rglob("*.py"):
            # Skip excluded directories
            if any(pattern in str(py_file) for pattern in exclude_patterns):
                continue
            self.python_files.append(py_file)

        print(f"📁 Found {len(self.python_files)} Python files")

    def extract_code_blocks(self) -> None:
        """Extract code blocks from all Python files."""
        print("📝 Extracting code blocks...")

        for file_path in self.python_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)
                self._extract_from_ast(tree, file_path, content.splitlines())

            except Exception as e:
                print(f"⚠️  Error parsing {file_path}: {e}")
                continue

    def _extract_from_ast(self, tree: ast.AST, file_path: Path, lines: list[str]) -> None:
        """Extract code blocks from AST."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._extract_function(node, file_path, lines)
            elif isinstance(node, ast.ClassDef):
                self._extract_class(node, file_path, lines)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                self._extract_import(node, file_path)

    def _extract_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        file_path: Path,
        lines: list[str],
    ) -> None:
        """Extract function information."""
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        # Get function content
        content_lines = lines[start_line - 1 : end_line]
        content = "\n".join(content_lines)

        # Create signature (exclude implementation details)
        signature = self._create_function_signature(node)

        # Create hash of normalized content
        normalized_content = self._normalize_code(content)
        hash_value = hashlib.md5(normalized_content.encode()).hexdigest()

        code_block = CodeBlock(
            file_path=str(file_path),
            start_line=start_line,
            end_line=end_line,
            content=content,
            hash_value=hash_value,
            node_type="function",
            name=node.name,
        )

        self.code_blocks.append(code_block)
        self.function_signatures[signature].append(code_block)

    def _extract_class(self, node: ast.ClassDef, file_path: Path, lines: list[str]) -> None:
        """Extract class information."""
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        content_lines = lines[start_line - 1 : end_line]
        content = "\n".join(content_lines)

        signature = self._create_class_signature(node)
        normalized_content = self._normalize_code(content)
        hash_value = hashlib.md5(normalized_content.encode()).hexdigest()

        code_block = CodeBlock(
            file_path=str(file_path),
            start_line=start_line,
            end_line=end_line,
            content=content,
            hash_value=hash_value,
            node_type="class",
            name=node.name,
        )

        self.code_blocks.append(code_block)
        self.class_signatures[signature].append(code_block)

    def _extract_import(self, node: ast.Import | ast.ImportFrom, file_path: Path) -> None:
        """Extract import information."""
        if isinstance(node, ast.Import):
            for alias in node.names:
                self.imports_map[str(file_path)].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                import_name = f"{module}.{alias.name}" if module else alias.name
                self.imports_map[str(file_path)].append(import_name)

    def _create_function_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Create function signature for comparison."""
        args = [arg.arg for arg in node.args.args]
        return f"{node.name}({','.join(args)})"

    def _create_class_signature(self, node: ast.ClassDef) -> str:
        """Create class signature for comparison."""
        bases = [ast.unparse(base) for base in node.bases]
        return f"{node.name}({','.join(bases)})"

    def _normalize_code(self, content: str) -> str:
        """Normalize code for comparison (remove comments, whitespace, etc.)."""
        # Remove comments
        content = re.sub(r"#.*$", "", content, flags=re.MULTILINE)
        # Remove docstrings
        content = re.sub(r'""".*?"""', "", content, flags=re.DOTALL)
        content = re.sub(r"'''.*?'''", "", content, flags=re.DOTALL)
        # Normalize whitespace
        content = re.sub(r"\s+", " ", content)
        return content.strip()

    def find_duplicate_functions(self) -> list[tuple[str, list[CodeBlock]]]:
        """Find duplicate functions."""
        print("🔍 Analyzing duplicate functions...")

        duplicates = []
        for signature, blocks in self.function_signatures.items():
            if len(blocks) > 1:
                # Group by hash to find exact duplicates
                hash_groups = defaultdict(list)
                for block in blocks:
                    hash_groups[block.hash_value].append(block)

                for hash_value, duplicate_blocks in hash_groups.items():
                    if len(duplicate_blocks) > 1:
                        duplicates.append((signature, duplicate_blocks))

        return duplicates

    def find_duplicate_classes(self) -> list[tuple[str, list[CodeBlock]]]:
        """Find duplicate classes."""
        print("🔍 Analyzing duplicate classes...")

        duplicates = []
        for signature, blocks in self.class_signatures.items():
            if len(blocks) > 1:
                hash_groups = defaultdict(list)
                for block in blocks:
                    hash_groups[block.hash_value].append(block)

                for hash_value, duplicate_blocks in hash_groups.items():
                    if len(duplicate_blocks) > 1:
                        duplicates.append((signature, duplicate_blocks))

        return duplicates

    def find_similar_blocks(self, similarity_threshold: float = 0.8) -> list[tuple[CodeBlock, CodeBlock, float]]:
        """Find similar code blocks using sequence matching."""
        print("🔍 Analyzing similar code blocks...")

        similar_blocks = []

        # Compare all code blocks pairwise
        for i, block1 in enumerate(self.code_blocks):
            for j, block2 in enumerate(self.code_blocks[i + 1 :], i + 1):
                if block1.file_path == block2.file_path:
                    continue  # Skip same file comparisons

                # Calculate similarity
                similarity = difflib.SequenceMatcher(
                    None,
                    self._normalize_code(block1.content),
                    self._normalize_code(block2.content),
                ).ratio()

                if similarity >= similarity_threshold:
                    similar_blocks.append((block1, block2, similarity))

        return sorted(similar_blocks, key=lambda x: x[2], reverse=True)

    def find_redundant_imports(self) -> dict[str, list[str]]:
        """Find redundant imports across files."""
        print("🔍 Analyzing redundant imports...")

        # Count import usage across project
        import_usage = Counter()
        for file_path, imports in self.imports_map.items():
            for imp in imports:
                import_usage[imp] += 1

        # Find imports that appear in multiple files
        redundant = defaultdict(list)
        for imp, count in import_usage.items():
            if count > 3:  # Appears in more than 3 files
                files_with_import = [file_path for file_path, imports in self.imports_map.items() if imp in imports]
                redundant[imp] = files_with_import

        return dict(redundant)

    def find_unused_imports(self) -> dict[str, list[str]]:
        """Find potentially unused imports (basic analysis)."""
        print("🔍 Analyzing unused imports...")

        unused = defaultdict(list)

        for file_path in self.python_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content)

                # Extract all imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        for alias in node.names:
                            imports.append(alias.name)

                # Check if import is used in code
                for imp in imports:
                    if imp not in content.replace(f"import {imp}", "").replace(f"from {imp}", ""):
                        unused[str(file_path)].append(imp)

            except Exception:
                continue

        return dict(unused)

    def generate_refactoring_suggestions(
        self,
        duplicate_functions: list[tuple[str, list[CodeBlock]]],
        redundant_imports: dict[str, list[str]],
    ) -> list[str]:
        """Generate refactoring suggestions."""
        suggestions = []

        # Suggestions for duplicate functions
        if duplicate_functions:
            suggestions.append("🔧 DUPLICATE FUNCTIONS:")
            for signature, blocks in duplicate_functions:
                suggestions.append(f"  • Extract '{signature}' to a common utility module")
                suggestions.append(f"    Found in {len(blocks)} files:")
                for block in blocks:
                    suggestions.append(f"    - {block.file_path}:{block.start_line}")

        # Suggestions for redundant imports
        if redundant_imports:
            suggestions.append("\n🔧 REDUNDANT IMPORTS:")
            for imp, files in redundant_imports.items():
                if len(files) > 5:
                    suggestions.append(f"  • Consider creating a central import for '{imp}'")
                    suggestions.append(f"    Used in {len(files)} files")

        # General suggestions
        suggestions.extend(
            [
                "\n🔧 GENERAL RECOMMENDATIONS:",
                "  • Create shared utility modules for common functions",
                "  • Use inheritance or composition for similar classes",
                "  • Implement factory patterns for repetitive object creation",
                "  • Consider using decorators for repeated functionality",
                "  • Extract constants to a central configuration file",
            ]
        )

        return suggestions

    def analyze(self) -> DuplicateReport:
        """Run complete analysis."""
        print("🚀 Starting duplicate code analysis...")

        self.scan_project()
        self.extract_code_blocks()

        duplicate_functions = self.find_duplicate_functions()
        duplicate_classes = self.find_duplicate_classes()
        similar_blocks = self.find_similar_blocks()
        redundant_imports = self.find_redundant_imports()
        unused_imports = self.find_unused_imports()

        refactoring_suggestions = self.generate_refactoring_suggestions(duplicate_functions, redundant_imports)

        return DuplicateReport(
            duplicate_functions=duplicate_functions,
            duplicate_classes=duplicate_classes,
            similar_blocks=similar_blocks,
            redundant_imports=redundant_imports,
            unused_imports=unused_imports,
            dead_code=[],  # TODO: Implement dead code detection
            refactoring_suggestions=refactoring_suggestions,
        )


class ReportGenerator:
    """Generate detailed reports from analysis results."""

    def __init__(self, report: DuplicateReport, output_dir: str):
        self.report = report
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_console_report(self) -> None:
        """Generate console report."""
        print("\n" + "=" * 80)
        print("📊 DUPLICATE CODE ANALYSIS REPORT")
        print("=" * 80)

        # Summary
        print("\n📈 SUMMARY:")
        print(f"  • Duplicate Functions: {len(self.report.duplicate_functions)}")
        print(f"  • Duplicate Classes: {len(self.report.duplicate_classes)}")
        print(f"  • Similar Code Blocks: {len(self.report.similar_blocks)}")
        print(f"  • Redundant Imports: {len(self.report.redundant_imports)}")
        print(f"  • Unused Imports: {sum(len(imports) for imports in self.report.unused_imports.values())}")

        # Duplicate Functions
        if self.report.duplicate_functions:
            print(f"\n🔄 DUPLICATE FUNCTIONS ({len(self.report.duplicate_functions)}):")
            for signature, blocks in self.report.duplicate_functions[:5]:  # Show top 5
                print(f"\n  📝 {signature}")
                for block in blocks:
                    print(f"    📁 {block.file_path}:{block.start_line}-{block.end_line}")

        # Similar Blocks
        if self.report.similar_blocks:
            print("\n🔍 SIMILAR CODE BLOCKS (Top 5):")
            for block1, block2, similarity in self.report.similar_blocks[:5]:
                print(f"\n  📊 Similarity: {similarity:.1%}")
                print(f"    📁 {block1.file_path}:{block1.start_line}-{block1.end_line}")
                print(f"    📁 {block2.file_path}:{block2.start_line}-{block2.end_line}")

        # Redundant Imports
        if self.report.redundant_imports:
            print("\n📦 REDUNDANT IMPORTS (Top 10):")
            sorted_imports = sorted(
                self.report.redundant_imports.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )
            for imp, files in sorted_imports[:10]:
                print(f"  📝 {imp} (used in {len(files)} files)")

        # Refactoring Suggestions
        if self.report.refactoring_suggestions:
            print(f"\n{chr(10).join(self.report.refactoring_suggestions)}")

        print("\n" + "=" * 80)

    def generate_html_report(self) -> str:
        """Generate HTML report."""
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Duplicate Code Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .duplicate-item { background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .similar-item { background: #d1ecf1; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .import-item { background: #f8d7da; padding: 5px; margin: 2px 0; border-radius: 3px; }
        .suggestion { background: #d4edda; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .code-path { font-family: monospace; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Duplicate Code Analysis Report</h1>
        <p>Generated on: {timestamp}</p>
    </div>

    <div class="section">
        <h2>📈 Summary</h2>
        <ul>
            <li>Duplicate Functions: {duplicate_functions_count}</li>
            <li>Duplicate Classes: {duplicate_classes_count}</li>
            <li>Similar Code Blocks: {similar_blocks_count}</li>
            <li>Redundant Imports: {redundant_imports_count}</li>
        </ul>
    </div>

    <div class="section">
        <h2>🔄 Duplicate Functions</h2>
        {duplicate_functions_html}
    </div>

    <div class="section">
        <h2>🔍 Similar Code Blocks</h2>
        {similar_blocks_html}
    </div>

    <div class="section">
        <h2>📦 Redundant Imports</h2>
        {redundant_imports_html}
    </div>

    <div class="section">
        <h2>🔧 Refactoring Suggestions</h2>
        {suggestions_html}
    </div>
</body>
</html>
        """.strip()

        # Generate HTML sections
        from datetime import datetime

        duplicate_functions_html = ""
        for signature, blocks in self.report.duplicate_functions:
            duplicate_functions_html += '<div class="duplicate-item">'
            duplicate_functions_html += f"<h4>{signature}</h4>"
            for block in blocks:
                duplicate_functions_html += (
                    f'<div class="code-path">{block.file_path}:{block.start_line}-{block.end_line}</div>'
                )
            duplicate_functions_html += "</div>"

        similar_blocks_html = ""
        for block1, block2, similarity in self.report.similar_blocks[:10]:
            similar_blocks_html += '<div class="similar-item">'
            similar_blocks_html += f"<h4>Similarity: {similarity:.1%}</h4>"
            similar_blocks_html += (
                f'<div class="code-path">{block1.file_path}:{block1.start_line}-{block1.end_line}</div>'
            )
            similar_blocks_html += (
                f'<div class="code-path">{block2.file_path}:{block2.start_line}-{block2.end_line}</div>'
            )
            similar_blocks_html += "</div>"

        redundant_imports_html = ""
        for imp, files in self.report.redundant_imports.items():
            redundant_imports_html += '<div class="import-item">'
            redundant_imports_html += f"<strong>{imp}</strong> (used in {len(files)} files)"
            redundant_imports_html += "</div>"

        suggestions_html = ""
        for suggestion in self.report.refactoring_suggestions:
            suggestions_html += f'<div class="suggestion">{suggestion}</div>'

        # Fill template
        html_content = html_content.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duplicate_functions_count=len(self.report.duplicate_functions),
            duplicate_classes_count=len(self.report.duplicate_classes),
            similar_blocks_count=len(self.report.similar_blocks),
            redundant_imports_count=len(self.report.redundant_imports),
            duplicate_functions_html=duplicate_functions_html,
            similar_blocks_html=similar_blocks_html,
            redundant_imports_html=redundant_imports_html,
            suggestions_html=suggestions_html,
        )

        # Save HTML report
        html_file = self.output_dir / "duplicate_analysis_report.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(html_file)

    def generate_json_report(self) -> str:
        """Generate JSON report for programmatic access."""
        import json

        report_data = {
            "duplicate_functions": [
                {
                    "signature": signature,
                    "blocks": [
                        {
                            "file_path": block.file_path,
                            "start_line": block.start_line,
                            "end_line": block.end_line,
                            "name": block.name,
                        }
                        for block in blocks
                    ],
                }
                for signature, blocks in self.report.duplicate_functions
            ],
            "similar_blocks": [
                {
                    "similarity": similarity,
                    "block1": {
                        "file_path": block1.file_path,
                        "start_line": block1.start_line,
                        "end_line": block1.end_line,
                    },
                    "block2": {
                        "file_path": block2.file_path,
                        "start_line": block2.start_line,
                        "end_line": block2.end_line,
                    },
                }
                for block1, block2, similarity in self.report.similar_blocks
            ],
            "redundant_imports": self.report.redundant_imports,
            "unused_imports": self.report.unused_imports,
            "refactoring_suggestions": self.report.refactoring_suggestions,
        }

        json_file = self.output_dir / "duplicate_analysis_report.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return str(json_file)


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze duplicate code in Python project")
    parser.add_argument("project_path", help="Path to project root")
    parser.add_argument("--output", "-o", default="./reports", help="Output directory for reports")
    parser.add_argument(
        "--similarity",
        "-s",
        type=float,
        default=0.8,
        help="Similarity threshold (0.0-1.0)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["console", "html", "json", "all"],
        default="all",
        help="Report format",
    )

    args = parser.parse_args()

    # Run analysis
    analyzer = DuplicateCodeAnalyzer(args.project_path)
    report = analyzer.analyze()

    # Generate reports
    generator = ReportGenerator(report, args.output)

    if args.format in ["console", "all"]:
        generator.generate_console_report()

    if args.format in ["html", "all"]:
        html_file = generator.generate_html_report()
        print(f"\n📄 HTML report generated: {html_file}")

    if args.format in ["json", "all"]:
        json_file = generator.generate_json_report()
        print(f"📊 JSON report generated: {json_file}")

    # Calculate duplicate percentage
    total_blocks = len(analyzer.code_blocks)
    duplicate_blocks = sum(len(blocks) for _, blocks in report.duplicate_functions)
    if total_blocks > 0:
        duplicate_percentage = (duplicate_blocks / total_blocks) * 100
        print(f"\n📊 Project Duplication Rate: {duplicate_percentage:.1f}%")

        if duplicate_percentage > 20:
            print("⚠️  HIGH duplication detected! Consider refactoring.")
        elif duplicate_percentage > 10:
            print("⚡ MODERATE duplication. Refactoring recommended.")
        else:
            print("✅ LOW duplication. Good code organization!")


if __name__ == "__main__":
    main()
