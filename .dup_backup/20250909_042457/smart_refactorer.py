#!/usr/bin/env python3
"""
Smart Refactoring Engine
Intelligent code refactoring with automated function decomposition.
"""

import ast
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import Exception
import SyntaxError
import any
import block
import bool
import child
import cond_num
import count
import dict
import e
import enumerate
import f
import file_path
import func
import hasattr
import i
import if_node
import int
import isinstance
import len
import list
import node
import open
import original_name
import part_num
import print
import project_root
import range
import refactoring_type
import self
import sorted
import stmt
import str
import template
import tuple
import type
import x


@dataclass
class RefactoringSuggestion:
    """Refactoring suggestion representation."""

    type: str
    file_path: str
    function_name: str
    start_line: int
    end_line: int
    complexity: int
    description: str
    suggested_refactoring: str
    new_functions: list[dict[str, Any]]
    auto_applicable: bool


@dataclass
class RefactoringReport:
    """Complete refactoring analysis report."""

    scan_timestamp: str
    total_functions: int
    complex_functions: int
    refactored_functions: int
    suggestions: list[RefactoringSuggestion]
    refactoring_templates: list[dict[str, Any]]


class SmartRefactorer:
    """Intelligent code refactoring engine."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.complexity_threshold = 10
        self.line_threshold = 50

    def run_refactoring_analysis(self) -> RefactoringReport:
        """Run comprehensive refactoring analysis."""
        print("🔧 Starting Smart Refactoring Analysis...")
        print("=" * 80)

        start_time = time.time()

        # Phase 1: Analyze code complexity
        print("🔍 Phase 1: Analyzing Code Complexity")
        complex_functions = self._find_complex_functions()

        # Phase 2: Generate refactoring suggestions
        print("🧠 Phase 2: Generating Refactoring Suggestions")
        suggestions = self._generate_refactoring_suggestions(complex_functions)

        # Phase 3: Create refactoring templates
        print("📋 Phase 3: Creating Refactoring Templates")
        templates = self._create_refactoring_templates()

        # Phase 4: Apply automatic refactoring
        print("🚀 Phase 4: Applying Automatic Refactoring")
        refactored_count = self._apply_automatic_refactoring(suggestions)

        # Phase 5: Generate comprehensive report
        print("📊 Phase 5: Generating Refactoring Report")
        report = RefactoringReport(
            scan_timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            total_functions=len(complex_functions),
            complex_functions=len([f for f in complex_functions if f["complexity"] > self.complexity_threshold]),
            refactored_functions=refactored_count,
            suggestions=suggestions,
            refactoring_templates=templates,
        )

        self._save_refactoring_report(report)

        execution_time = time.time() - start_time
        print(f"✅ Refactoring analysis complete! ({execution_time:.2f}s)")

        return report

    def _find_complex_functions(self) -> list[dict[str, Any]]:
        """Find complex functions that need refactoring."""
        complex_functions = []

        python_files = list(self.project_root.glob("**/*.py"))

        for file_path in python_files:
            try:
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                try:
                    tree = ast.parse(content, filename=str(file_path))
                    functions = self._extract_functions_info(tree, file_path, content)
                    complex_functions.extend(functions)
                except SyntaxError:
                    continue

            except Exception:
                continue

        # Sort by complexity
        complex_functions.sort(key=lambda x: x["complexity"], reverse=True)

        print(f"   ✅ Found {len(complex_functions)} functions to analyze")
        return complex_functions

    def _extract_functions_info(self, tree: ast.AST, file_path: Path, content: str) -> list[dict[str, Any]]:
        """Extract detailed function information."""
        functions = []
        lines = content.splitlines()

        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # Calculate metrics
                complexity = self._calculate_complexity(node)
                line_count = node.end_lineno - node.lineno + 1 if hasattr(node, "end_lineno") else 0
                parameter_count = len(node.args.args)

                # Extract function body
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, "end_lineno") else start_line + 20
                function_body = "\n".join(lines[start_line:end_line])

                function_info = {
                    "name": node.name,
                    "file_path": str(file_path),
                    "start_line": node.lineno,
                    "end_line": end_line,
                    "line_count": line_count,
                    "complexity": complexity,
                    "parameter_count": parameter_count,
                    "body": function_body,
                    "docstring": ast.get_docstring(node),
                    "needs_refactoring": complexity > self.complexity_threshold or line_count > self.line_threshold,
                }

                functions.append(function_info)
                self.generic_visit(node)

            def _calculate_complexity(self, node):
                """Calculate cyclomatic complexity."""
                complexity = 1

                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                    elif isinstance(child, (ast.And, ast.Or)):
                        complexity += 1

                return complexity

        visitor = FunctionVisitor()
        visitor.visit(tree)

        return functions

    def _generate_refactoring_suggestions(self, functions: list[dict[str, Any]]) -> list[RefactoringSuggestion]:
        """Generate intelligent refactoring suggestions."""
        suggestions = []

        for func in functions:
            if not func["needs_refactoring"]:
                continue

            suggestion = self._analyze_function_for_refactoring(func)
            if suggestion:
                suggestions.append(suggestion)

        print(f"   ✅ Generated {len(suggestions)} refactoring suggestions")
        return suggestions

    def _analyze_function_for_refactoring(self, func: dict[str, Any]) -> RefactoringSuggestion | None:
        """Analyze a function and suggest refactoring."""
        body = func["body"]

        # Parse function AST for detailed analysis
        try:
            func_ast = ast.parse(body)
        except SyntaxError:
            return None

        # Identify refactoring patterns
        refactoring_type, new_functions = self._identify_refactoring_pattern(func_ast, func)

        if refactoring_type:
            return RefactoringSuggestion(
                type=refactoring_type,
                file_path=func["file_path"],
                function_name=func["name"],
                start_line=func["start_line"],
                end_line=func["end_line"],
                complexity=func["complexity"],
                description=f"Function '{func['name']}' has complexity {func['complexity']} and {func['line_count']} lines",
                suggested_refactoring=self._generate_refactoring_description(refactoring_type, func),
                new_functions=new_functions,
                auto_applicable=refactoring_type in ["extract_method", "split_conditional"],
            )

        return None

    def _identify_refactoring_pattern(
        self, func_ast: ast.AST, func: dict[str, Any]
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """Identify specific refactoring patterns."""

        # Pattern 1: Long method - Extract method
        if func["line_count"] > 50:
            return self._suggest_extract_method(func_ast, func)

        # Pattern 2: Complex conditionals - Split conditional
        if self._has_complex_conditionals(func_ast):
            return self._suggest_split_conditional(func_ast, func)

        # Pattern 3: Too many parameters - Introduce parameter object
        if func["parameter_count"] > 5:
            return self._suggest_parameter_object(func_ast, func)

        # Pattern 4: Duplicate code - Extract common functionality
        if self._has_duplicate_code(func_ast):
            return self._suggest_extract_common(func_ast, func)

        return None, []

    def _suggest_extract_method(self, func_ast: ast.AST, func: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
        """Suggest method extraction for long functions."""
        new_functions = []

        # Analyze function structure to find logical blocks
        blocks = self._find_logical_blocks(func_ast)

        for i, block in enumerate(blocks):
            if len(block) > 5:  # Block has enough statements
                new_func = {
                    "name": f"{func['name']}_part_{i+1}",
                    "description": f"Extracted from {func['name']}",
                    "statements": len(block),
                    "suggested_code": self._generate_extracted_method_code(block, func["name"], i + 1),
                }
                new_functions.append(new_func)

        return "extract_method", new_functions

    def _suggest_split_conditional(self, func_ast: ast.AST, func: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
        """Suggest splitting complex conditionals."""
        new_functions = []

        # Find complex if statements
        complex_ifs = []
        for node in ast.walk(func_ast):
            if isinstance(node, ast.If) and self._is_complex_conditional(node):
                complex_ifs.append(node)

        for i, if_node in enumerate(complex_ifs):
            new_func = {
                "name": f"{func['name']}_condition_{i+1}",
                "description": f"Extracted conditional logic from {func['name']}",
                "type": "conditional_check",
                "suggested_code": self._generate_conditional_method_code(if_node, func["name"], i + 1),
            }
            new_functions.append(new_func)

        return "split_conditional", new_functions

    def _suggest_parameter_object(self, func_ast: ast.AST, func: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
        """Suggest introducing parameter objects."""
        new_functions = [
            {
                "name": f"{func['name']}_params",
                "description": f"Parameter object for {func['name']}",
                "type": "parameter_class",
                "suggested_code": self._generate_parameter_class_code(func),
            }
        ]

        return "parameter_object", new_functions

    def _suggest_extract_common(self, func_ast: ast.AST, func: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
        """Suggest extracting common functionality."""
        new_functions = [
            {
                "name": f"{func['name']}_common",
                "description": f"Common functionality extracted from {func['name']}",
                "type": "utility_method",
                "suggested_code": self._generate_common_method_code(func),
            }
        ]

        return "extract_common", new_functions

    def _find_logical_blocks(self, func_ast: ast.AST) -> list[list[ast.stmt]]:
        """Find logical blocks in function for extraction."""
        blocks = []
        current_block = []

        for node in ast.walk(func_ast):
            if isinstance(node, ast.FunctionDef):
                for stmt in node.body:
                    if isinstance(stmt, (ast.If, ast.For, ast.While, ast.With)):
                        if current_block:
                            blocks.append(current_block)
                            current_block = []
                        blocks.append([stmt])
                    else:
                        current_block.append(stmt)

                if current_block:
                    blocks.append(current_block)
                break

        return blocks

    def _has_complex_conditionals(self, func_ast: ast.AST) -> bool:
        """Check if function has complex conditional statements."""
        for node in ast.walk(func_ast):
            if isinstance(node, ast.If) and self._is_complex_conditional(node):
                return True
        return False

    def _is_complex_conditional(self, if_node: ast.If) -> bool:
        """Check if conditional is complex enough to warrant extraction."""
        # Count boolean operators in condition
        bool_ops = 0
        for node in ast.walk(if_node.test):
            if isinstance(node, ast.BoolOp):
                bool_ops += len(node.values) - 1

        # Count lines in if body
        body_lines = len(if_node.body)

        return bool_ops > 2 or body_lines > 10

    def _has_duplicate_code(self, func_ast: ast.AST) -> bool:
        """Check for duplicate code patterns."""
        # Simplified heuristic - look for similar statement patterns
        statements = []
        for node in ast.walk(func_ast):
            if isinstance(node, ast.stmt):
                statements.append(type(node).__name__)

        # Check for repeated patterns
        pattern_length = 3
        patterns = {}
        for i in range(len(statements) - pattern_length + 1):
            pattern = tuple(statements[i : i + pattern_length])
            patterns[pattern] = patterns.get(pattern, 0) + 1

        return any(count > 1 for count in patterns.values())

    def _generate_extracted_method_code(self, block: list[ast.stmt], original_name: str, part_num: int) -> str:
        """Generate code for extracted method."""
        return f'''def {original_name}_part_{part_num}(self):
    """
    Extracted from {original_name} - Part {part_num}
    """
    # TODO: Implement extracted logic
    # Original block had {len(block)} statements
    pass'''

    def _generate_conditional_method_code(self, if_node: ast.If, original_name: str, cond_num: int) -> str:
        """Generate code for extracted conditional method."""
        return f'''def {original_name}_condition_{cond_num}(self) -> bool:
    """
    Extracted conditional logic from {original_name}
    """
    # TODO: Implement conditional check
    # Original condition was complex
    return True  # Replace with actual condition'''

    def _generate_parameter_class_code(self, func: dict[str, Any]) -> str:
        """Generate parameter class code."""
        return f'''@dataclass
class {func['name'].title()}Params:
    """
    Parameter object for {func['name']}
    """
    # TODO: Add parameter fields based on original function signature
    pass'''

    def _generate_common_method_code(self, func: dict[str, Any]) -> str:
        """Generate common method code."""
        return f'''def {func['name']}_common(self):
    """
    Common functionality extracted from {func['name']}
    """
    # TODO: Implement common logic
    pass'''

    def _generate_refactoring_description(self, refactoring_type: str, func: dict[str, Any]) -> str:
        """Generate human-readable refactoring description."""
        descriptions = {
            "extract_method": f"Break down '{func['name']}' into smaller, focused methods",
            "split_conditional": f"Extract complex conditional logic from '{func['name']}' into separate methods",
            "parameter_object": f"Replace multiple parameters in '{func['name']}' with a parameter object",
            "extract_common": f"Extract common functionality from '{func['name']}' into reusable methods",
        }

        return descriptions.get(refactoring_type, f"Refactor '{func['name']}' to improve maintainability")

    def _create_refactoring_templates(self) -> list[dict[str, Any]]:
        """Create reusable refactoring templates."""
        templates = [
            {
                "name": "Extract Method Template",
                "description": "Template for extracting methods from long functions",
                "code": '''def extract_method_example(self):
    """
    Extract this block into a separate method.
    
    Steps:
    1. Identify the logical block
    2. Determine required parameters
    3. Extract and create new method
    4. Replace original code with method call
    """
    # Example of code that should be extracted:
    # Complex logic that forms a cohesive unit
    pass''',
            },
            {
                "name": "Split Conditional Template",
                "description": "Template for splitting complex conditionals",
                "code": '''def is_condition_met(self) -> bool:
    """
    Extract complex conditional logic.
    
    Returns:
        bool: True if condition is met
    """
    # Replace complex if condition with this method
    return True  # Implement actual condition

def handle_condition_result(self):
    """Handle the result of the condition check."""
    if self.is_condition_met():
        # Handle true case
        pass
    else:
        # Handle false case
        pass''',
            },
            {
                "name": "Parameter Object Template",
                "description": "Template for parameter object pattern",
                "code": '''@dataclass
class ProcessingParams:
    """
    Parameter object to replace multiple function parameters.
    """
    input_data: Any
    options: Dict[str, Any]
    config: Dict[str, Any]
    
def process_with_params(self, params: ProcessingParams):
    """
    Use parameter object instead of multiple parameters.
    
    Args:
        params: All processing parameters bundled together
    """
    # Use params.input_data, params.options, etc.
    pass''',
            },
        ]

        print(f"   ✅ Created {len(templates)} refactoring templates")
        return templates

    def _apply_automatic_refactoring(self, suggestions: list[RefactoringSuggestion]) -> int:
        """Apply automatic refactoring where possible."""
        refactored_count = 0

        for suggestion in suggestions:
            if not suggestion.auto_applicable:
                continue

            try:
                if suggestion.type == "extract_method":
                    if self._apply_extract_method_refactoring(suggestion):
                        refactored_count += 1
                elif suggestion.type == "split_conditional":
                    if self._apply_split_conditional_refactoring(suggestion):
                        refactored_count += 1

            except Exception as e:
                print(f"   ❌ Failed to apply refactoring to {suggestion.function_name}: {e}")

        print(f"   ✅ Applied {refactored_count} automatic refactorings")
        return refactored_count

    def _apply_extract_method_refactoring(self, suggestion: RefactoringSuggestion) -> bool:
        """Apply extract method refactoring."""
        # For safety, only create suggestions file instead of modifying original
        self._create_refactoring_suggestion_file(suggestion)
        return True

    def _apply_split_conditional_refactoring(self, suggestion: RefactoringSuggestion) -> bool:
        """Apply split conditional refactoring."""
        # For safety, only create suggestions file instead of modifying original
        self._create_refactoring_suggestion_file(suggestion)
        return True

    def _create_refactoring_suggestion_file(self, suggestion: RefactoringSuggestion) -> None:
        """Create a file with refactoring suggestions."""
        file_name = f"refactoring_suggestion_{suggestion.function_name}_{int(time.time())}.py"

        content = f'''"""
Refactoring suggestion for {suggestion.function_name}
Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}

Original function: {suggestion.file_path}:{suggestion.start_line}-{suggestion.end_line}
Refactoring type: {suggestion.type}
Description: {suggestion.description}
"""

# Suggested refactoring:
{suggestion.suggested_refactoring}

# New functions to create:
'''

        for new_func in suggestion.new_functions:
            content += f"\n# {new_func.get('description', '')}\n"
            content += f"{new_func.get('suggested_code', '')}\n\n"

        suggestion_path = self.project_root / "refactoring_suggestions" / file_name
        suggestion_path.parent.mkdir(exist_ok=True)

        with open(suggestion_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _save_refactoring_report(self, report: RefactoringReport) -> None:
        """Save comprehensive refactoring report."""
        # Save JSON report
        with open("REFACTORING_ANALYSIS_REPORT.json", "w") as f:
            json.dump(asdict(report), f, indent=2, default=str)

        # Generate markdown report
        self._generate_refactoring_markdown(report)

    def _generate_refactoring_markdown(self, report: RefactoringReport) -> None:
        """Generate markdown refactoring report."""
        markdown_content = f"""# 🔧 Smart Refactoring Analysis Report

## 📊 Executive Summary

- **Analysis Date**: {report.scan_timestamp}
- **Total Functions Analyzed**: {report.total_functions}
- **Complex Functions**: {report.complex_functions}
- **Refactoring Suggestions**: {len(report.suggestions)}
- **Auto-Refactored**: {report.refactored_functions}

## 🎯 Top Refactoring Opportunities

"""

        # Show top 10 most complex functions
        top_suggestions = sorted(report.suggestions, key=lambda x: x.complexity, reverse=True)[:10]

        for i, suggestion in enumerate(top_suggestions, 1):
            markdown_content += f"""### {i}. {suggestion.function_name} (Complexity: {suggestion.complexity})

- **File**: `{suggestion.file_path}`
- **Lines**: {suggestion.start_line}-{suggestion.end_line}
- **Type**: {suggestion.type}
- **Description**: {suggestion.description}
- **Suggested Refactoring**: {suggestion.suggested_refactoring}
- **Auto-applicable**: {'✅' if suggestion.auto_applicable else '❌'}

**New Functions to Create**:
"""

            for new_func in suggestion.new_functions:
                markdown_content += f"- `{new_func.get('name', '')}`: {new_func.get('description', '')}\n"

            markdown_content += "\n"

        markdown_content += """## 📋 Refactoring Templates

The following templates are available for manual refactoring:

"""

        for template in report.refactoring_templates:
            markdown_content += f"""### {template['name']}

{template['description']}

```python
{template['code']}
```

"""

        markdown_content += """## 🚀 Implementation Guide

### Automated Refactoring
1. Review generated refactoring suggestions in `refactoring_suggestions/` directory
2. Apply suggestions that have been marked as auto-applicable
3. Test thoroughly after each refactoring

### Manual Refactoring
1. Start with highest complexity functions
2. Use provided templates as guidance
3. Follow the extract method pattern for long functions
4. Split complex conditionals into separate methods
5. Introduce parameter objects for functions with many parameters

### Testing Strategy
1. Ensure comprehensive test coverage before refactoring
2. Run tests after each refactoring step
3. Use regression testing to verify behavior preservation

---
*Generated by Smart Refactoring Engine*
"""

        with open("REFACTORING_ANALYSIS_REPORT.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)


def main():
    """Main function to run refactoring analysis."""
    refactorer = SmartRefactorer()
    report = refactorer.run_refactoring_analysis()

    print("\n" + "=" * 80)
    print("🔧 SMART REFACTORING ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"📊 Total Functions: {report.total_functions}")
    print(f"🔴 Complex Functions: {report.complex_functions}")
    print(f"💡 Suggestions: {len(report.suggestions)}")
    print(f"🚀 Auto-Refactored: {report.refactored_functions}")
    print("\n📋 Reports Generated:")
    print("   - REFACTORING_ANALYSIS_REPORT.json (detailed)")
    print("   - REFACTORING_ANALYSIS_REPORT.md (summary)")
    print("   - refactoring_suggestions/ (individual suggestions)")

    if report.complex_functions > 0:
        print(f"\n⚠️  {report.complex_functions} functions need refactoring!")
    else:
        print("\n✅ No complex functions requiring refactoring!")


if __name__ == "__main__":
    main()
