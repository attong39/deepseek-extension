"""AI-powered comprehensive project scanner and optimizer."""
import ast
import json
import os
import re
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
import Exception
import OSError
import SyntaxError
import alias
import any
import child
import chr
import d
import dict
import dirs
import e
import enumerate
import f
import fa
import filename
import filenames
import float
import i
import imp
import int
import isinstance
import item
import len
import line
import list
import max
import message
import min
import node
import open
import pattern
import print
import project_root
import root
import self
import sorted
import str
import sum
import tuple
import x
    path: str
    size: int
    lines: int
    functions: int
    classes: int
    imports: list[str]
    syntax_errors: list[str]
    complexity_score: int
    duplicated_code: list[str]
    security_issues: list[str]
    performance_issues: list[str]
    maintainability_score: float
    test_coverage: float
    documentation_score: float

@dataclass
class ProjectOptimizations:
    """Optimization suggestions for the project."""
    remove_duplicates: list[str]
    refactor_complex: list[str]
    add_tests: list[str]
    fix_security: list[str]
    improve_performance: list[str]
    update_dependencies: list[str]
    consolidate_modules: list[str]
    add_documentation: list[str]

class AIProjectScanner:
    """AI-powered project scanner and optimizer."""

    def __init__(self: Any, project_root: str='.') -> Any:
        self.project_root = Path(project_root)
        self.file_analyses: list[FileAnalysis] = []
        self.project_stats: dict[str, Any] = {'total_files': 0, 'total_lines': 0, 'total_size': 0, 'languages': Counter(), 'file_types': Counter()}
        self.common_patterns: dict[str, Any] = {'duplicated_imports': defaultdict(list), 'similar_functions': defaultdict(list), 'unused_imports': defaultdict(list), 'complex_functions': [], 'large_files': [], 'test_files': [], 'config_files': []}

    def scan_project(self: Any) -> dict[str, Any]:
        """Scan entire project and analyze all files."""
        print('🔍 AI Project Scanner Starting...')
        print('=' * 80)
        start_time = time.time()
        print('📁 Phase 1: File Discovery')
        files = self._discover_files()
        print(f'   Found {len(files)} files to analyze')
        print('🔬 Phase 2: Deep File Analysis')
        for i, file_path in enumerate(files):
            if i % 100 == 0:
                print(f'   Progress: {i}/{len(files)} files analyzed')
            self._analyze_file(file_path)
        print('🧠 Phase 3: Pattern Detection & AI Analysis')
        self._detect_patterns()
        print('⚡ Phase 4: Optimization Recommendations')
        optimizations = self._generate_optimizations()
        print('📊 Phase 5: Report Generation')
        report = self._generate_comprehensive_report(optimizations)
        total_time = time.time() - start_time
        print(f'✅ AI Analysis Complete! ({total_time:.2f}s)')
        return {'summary': self.project_stats, 'file_analyses': [asdict(fa) for fa in self.file_analyses], 'patterns': dict(self.common_patterns), 'optimizations': asdict(optimizations), 'report': report, 'scan_duration': total_time}

    def _discover_files(self: Any) -> list[Path]:
        """Discover all relevant files in the project."""
        files = []
        exclude_patterns = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'dist', 'build', '.eggs', '*.egg-info'}
        for root, dirs, filenames in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.suffix in {'.pyc', '.pyo', '.so', '.dll', '.exe'}:
                    continue
                try:
                    if file_path.stat().st_size > 10 * 1024 * 1024:
                        continue
                except OSError:
                    continue
                files.append(file_path)
                self.project_stats['file_types'][file_path.suffix] += 1
        return files

    def _analyze_file(self: Any, file_path: Path) -> None:
        """Analyze a single file comprehensively."""
        try:
            with open(file_path, encoding='utf-8', errors='ignore') as f:
                content = f.read()
            size = len(content)
            lines = len(content.splitlines())
            self.project_stats['total_files'] += 1
            self.project_stats['total_lines'] += lines
            self.project_stats['total_size'] += size
            language = self._detect_language(file_path)
            self.project_stats['languages'][language] += 1
            if language == 'python':
                analysis = self._analyze_python_file(file_path, content)
            elif language in ['javascript', 'typescript']:
                analysis = self._analyze_js_file(file_path, content)
            else:
                analysis = self._analyze_generic_file(file_path, content)
            self.file_analyses.append(analysis)
            if lines > 500:
                self.common_patterns['large_files'].append(str(file_path))
        except Exception as e:
            analysis = FileAnalysis(path=str(file_path), size=0, lines=0, functions=0, classes=0, imports=[], syntax_errors=[f'Failed to analyze: {str(e)}'], complexity_score=0, duplicated_code=[], security_issues=[], performance_issues=[], maintainability_score=0.0, test_coverage=0.0, documentation_score=0.0)
            self.file_analyses.append(analysis)

    def _detect_language(self: Any, file_path: Path) -> str:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()
        language_map = {'.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.jsx': 'javascript', '.tsx': 'typescript', '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.cs': 'csharp', '.php': 'php', '.rb': 'ruby', '.go': 'go', '.rs': 'rust', '.md': 'markdown', '.txt': 'text', '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml', '.toml': 'toml', '.ini': 'ini', '.cfg': 'config', '.conf': 'config'}
        return language_map.get(ext, 'unknown')

    def _analyze_python_file(self: Any, file_path: Path, content: str) -> FileAnalysis:
        """Deep analysis of Python files."""
        imports = []
        functions = 0
        classes = 0
        syntax_errors = []
        complexity_score = 0
        security_issues = []
        performance_issues = []
        try:
            tree = ast.parse(content)
            imports, functions, classes, complexity_score = self._extract_ast_info(tree)
        except SyntaxError as e:
            syntax_errors.append(f'Line {e.lineno}: {e.msg}')
        except Exception as e:
            syntax_errors.append(f'Parse error: {str(e)}')
        security_issues.extend(self._check_security_issues(content))
        performance_issues.extend(self._check_performance_issues(content))
        self._track_file_patterns(file_path, imports)
        return FileAnalysis(path=str(file_path), size=len(content), lines=len(content.splitlines()), functions=functions, classes=classes, imports=imports, syntax_errors=syntax_errors, complexity_score=complexity_score, duplicated_code=[], security_issues=security_issues, performance_issues=performance_issues, maintainability_score=self._calculate_maintainability(content, complexity_score), test_coverage=0.0, documentation_score=self._calculate_documentation_score(content))

    def _extract_ast_info(self: Any, tree: ast.AST) -> tuple[list[str], int, int, int]:
        """Extract information from AST."""
        imports = []
        functions = 0
        classes = 0
        complexity_score = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f'{module}.{alias.name}')
            elif isinstance(node, ast.FunctionDef):
                functions += 1
                func_complexity = self._calculate_complexity(node)
                complexity_score += func_complexity
                if func_complexity > 10:
                    complex_functions = self.common_patterns.get('complex_functions', [])
                    if isinstance(complex_functions, list):
                        complex_functions.append(f'Function complexity: {func_complexity}')
            elif isinstance(node, ast.ClassDef):
                classes += 1
        return (imports, functions, classes, complexity_score)

    def _track_file_patterns(self: Any, file_path: Path, imports: list[str]) -> None:
        """Track file patterns for later analysis."""
        duplicated_imports = self.common_patterns.get('duplicated_imports', {})
        if isinstance(duplicated_imports, dict):
            for imp in imports:
                if imp not in duplicated_imports:
                    duplicated_imports[imp] = []
                duplicated_imports[imp].append(str(file_path))
        if 'test' in file_path.name.lower() or file_path.parent.name == 'tests':
            test_files = self.common_patterns.get('test_files', [])
            if isinstance(test_files, list):
                test_files.append(str(file_path))

    def _analyze_js_file(self: Any, file_path: Path, content: str) -> FileAnalysis:
        """Basic analysis of JavaScript/TypeScript files."""
        imports = re.findall('import\\s+.*?\\s+from\\s+[\\\'"]([^\\\'"]+)[\\\'"]', content)
        functions = len(re.findall('function\\s+\\w+|const\\s+\\w+\\s*=\\s*\\(.*?\\)\\s*=>', content))
        classes = len(re.findall('class\\s+\\w+', content))
        return FileAnalysis(path=str(file_path), size=len(content), lines=len(content.splitlines()), functions=functions, classes=classes, imports=imports, syntax_errors=[], complexity_score=functions * 2 + classes * 3, duplicated_code=[], security_issues=[], performance_issues=[], maintainability_score=0.5, test_coverage=0.0, documentation_score=self._calculate_documentation_score(content))

    def _analyze_generic_file(self: Any, file_path: Path, content: str) -> FileAnalysis:
        """Basic analysis for other file types."""
        return FileAnalysis(path=str(file_path), size=len(content), lines=len(content.splitlines()), functions=0, classes=0, imports=[], syntax_errors=[], complexity_score=0, duplicated_code=[], security_issues=[], performance_issues=[], maintainability_score=1.0, test_coverage=0.0, documentation_score=self._calculate_documentation_score(content))

    def _calculate_complexity(self: Any, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _check_security_issues(self: Any, content: str) -> list[str]:
        """Check for potential security issues."""
        issues = []
        security_patterns = [('eval\\s*\\(', 'Dangerous ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval() usage'), ('exec\\s*\\(', 'Dangerous # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed) usage'), ('shell=False', 'Shell injection risk'), ('password\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'Hardcoded password'), ('api_key\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'Hardcoded API key'), ('secret\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'Hardcoded secret'), ('subprocess\\.call.*shell=False', 'Shell injection in subprocess')]
        for pattern, message in security_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(message)
        return issues

    def _check_performance_issues(self: Any, content: str) -> list[str]:
        """Check for potential performance issues."""
        issues = []
        performance_patterns = [('for\\s+\\w+\\s+in\\s+range\\(len\\(', 'Use enumerate() instead of range(len())'), ('\\.append\\(.*?\\)\\s*\\n.*?for\\s+', 'Consider list comprehension'), ('time\\.sleep\\(', 'Blocking sleep in code'), ('print\\s*\\(', 'Print statements may impact performance'), ('global\\s+\\w+', 'Global variables can impact performance')]
        for pattern, message in performance_patterns:
            if re.search(pattern, content):
                issues.append(message)
        return issues

    def _calculate_maintainability(self: Any, content: str, complexity: int) -> float:
        """Calculate maintainability score (0-1)."""
        lines = len(content.splitlines())
        complexity_penalty = min(complexity / 100, 0.5)
        length_penalty = min(lines / 1000, 0.3)
        has_docstrings = '"""' in content or "'''" in content
        has_type_hints = ': ' in content and '->' in content
        has_comments = '#' in content
        bonus = 0
        if has_docstrings:
            bonus += 0.2
        if has_type_hints:
            bonus += 0.1
        if has_comments:
            bonus += 0.1
        score = 1.0 - complexity_penalty - length_penalty + bonus
        return max(0.0, min(1.0, score))

    def _calculate_documentation_score(self: Any, content: str) -> float:
        """Calculate documentation score (0-1)."""
        lines = content.splitlines()
        if not lines:
            return 0.0
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        docstring_blocks = content.count('"""') + content.count("'''")
        doc_ratio = (comment_lines + docstring_blocks * 3) / len(lines)
        return min(1.0, doc_ratio * 2)

    def _detect_patterns(self: Any) -> None:
        """Detect common patterns across the project."""
        for imp, files in self.common_patterns['duplicated_imports'].items():
            if len(files) > 5:
                pass

    def _generate_optimizations(self: Any) -> ProjectOptimizations:
        """Generate comprehensive optimization recommendations."""
        large_files = [f for f in self.file_analyses if f.lines > 500]
        complex_files = [f for f in self.file_analyses if f.complexity_score > 50]
        poorly_documented = [f for f in self.file_analyses if f.documentation_score < 0.2]
        security_issues = [f for f in self.file_analyses if f.security_issues]
        performance_issues = [f for f in self.file_analyses if f.performance_issues]
        return ProjectOptimizations(remove_duplicates=[f"Consolidate {len(self.common_patterns['duplicated_imports'])} common imports", f"Remove {len([f for f in self.file_analyses if 'duplicate' in f.path.lower()])} potential duplicate files"], refactor_complex=[f'Refactor {len(complex_files)} complex files with high complexity scores', f'Break down {len(large_files)} large files (>500 lines)'], add_tests=[f"Add tests for {len([f for f in self.file_analyses if not any('test' in f.path.lower() for _ in [f])])} files without tests", f'Improve test coverage for {len(self.file_analyses)} total files'], fix_security=[f'Fix security issues in {len(security_issues)} files', 'Review hardcoded credentials and dangerous functions'], improve_performance=[f'Optimize {len(performance_issues)} files with performance issues', f'Review {len([f for f in self.file_analyses if f.complexity_score > 30])} files with high complexity'], update_dependencies=['Review and update package dependencies', 'Check for deprecated imports and functions'], consolidate_modules=[f'Consider consolidating {len(large_files)} large modules', f'Organize {len(self.file_analyses)} files into better structure'], add_documentation=[f'Add documentation to {len(poorly_documented)} poorly documented files', 'Improve overall documentation coverage'])

    def _generate_comprehensive_report(self: Any, optimizations: ProjectOptimizations) -> str:
        """Generate a comprehensive markdown report."""
        total_files = len(self.file_analyses)
        total_lines = sum(f.lines for f in self.file_analyses)
        avg_complexity = sum(f.complexity_score for f in self.file_analyses) / total_files if total_files > 0 else 0
        avg_maintainability = sum(f.maintainability_score for f in self.file_analyses) / total_files if total_files > 0 else 0
        top_complex_files = sorted(self.file_analyses, key=lambda x: x.complexity_score, reverse=True)[:5]
        top_large_files = sorted(self.file_analyses, key=lambda x: x.lines, reverse=True)[:5]
        files_with_security = [f for f in self.file_analyses if f.security_issues][:5]
        report = f"# 🚀 AI Project Analysis Report\n\n## 📊 Project Overview\n- **Total Files**: {total_files:,}\n- **Total Lines of Code**: {total_lines:,}\n- **Average Complexity**: {avg_complexity:.1f}\n- **Average Maintainability**: {avg_maintainability:.2f}\n- **Languages**: {dict(self.project_stats['languages'])}\n\n## 🎯 Key Findings\n\n### 🔴 Critical Issues\n- **{len(files_with_security)} files** with security vulnerabilities\n- **{len([f for f in self.file_analyses if f.syntax_errors])} files** with syntax errors\n- **{len(top_complex_files)} files** with very high complexity\n\n### 🟡 Performance Opportunities  \n- **{len([f for f in self.file_analyses if f.performance_issues])} files** with performance issues\n- **{len(top_large_files)} files** are very large (>500 lines)\n- **{len([f for f in self.file_analyses if f.maintainability_score < 0.5])} files** have low maintainability\n\n### 🟢 Quality Metrics\n- **{len([f for f in self.file_analyses if f.documentation_score > 0.5])} files** are well documented\n- **{len([f for f in self.file_analyses if not f.syntax_errors])} files** have clean syntax\n- **{len([f for f in self.file_analyses if f.maintainability_score > 0.7])} files** have high maintainability\n\n## 📋 Detailed Recommendations\n\n### 🚨 Priority 1: Security & Syntax\n"
        if files_with_security:
            report += '\n**Security Issues:**\n'
            for f in files_with_security[:3]:
                report += f"- `{f.path}`: {', '.join(f.security_issues[:2])}\n"
        syntax_error_files = [f for f in self.file_analyses if f.syntax_errors]
        if syntax_error_files:
            report += '\n**Syntax Errors:**\n'
            for f in syntax_error_files[:3]:
                report += f"- `{f.path}`: {', '.join(f.syntax_errors[:1])}\n"
        report += '\n\n### ⚡ Priority 2: Performance & Complexity\n**Most Complex Files:**\n'
        for f in top_complex_files[:3]:
            report += f'- `{f.path}`: Complexity {f.complexity_score}, {f.lines} lines\n'
        report += '\n\n**Largest Files:**\n'
        for f in top_large_files[:3]:
            report += f'- `{f.path}`: {f.lines} lines, {f.functions} functions, {f.classes} classes\n'
        report += '\n\n### 📚 Priority 3: Documentation & Maintainability\n**Poorly Documented Files:**\n'
        poorly_documented = sorted(self.file_analyses, key=lambda x: x.documentation_score)[:3]
        for f in poorly_documented:
            report += f'- `{f.path}`: Documentation score {f.documentation_score:.2f}\n'
        report += f"\n\n## 🎯 Optimization Action Plan\n\n### Phase 1: Critical Fixes (1-2 days)\n{chr(10).join(f'- {item}' for item in optimizations.fix_security + optimizations.refactor_complex[:2])}\n\n### Phase 2: Performance & Structure (1 week)  \n{chr(10).join(f'- {item}' for item in optimizations.improve_performance + optimizations.consolidate_modules)}\n\n### Phase 3: Quality & Testing (2 weeks)\n{chr(10).join(f'- {item}' for item in optimizations.add_tests + optimizations.add_documentation)}\n\n### Phase 4: Long-term Maintenance (1 month)\n{chr(10).join(f'- {item}' for item in optimizations.update_dependencies + optimizations.remove_duplicates)}\n\n## 📈 Expected Impact\n\n- **Security**: 🔒 Eliminate all critical vulnerabilities\n- **Performance**: ⚡ 20-30% improvement in complex modules  \n- **Maintainability**: 🛠️ 40-50% improvement in code quality scores\n- **Documentation**: 📖 Achieve 80%+ documentation coverage\n- **Testing**: 🧪 Establish comprehensive test coverage\n\n---\n*Generated by AI Project Scanner v2.0 - {time.strftime('%Y-%m-%d %H:%M:%S')}*\n"
        return report

def main() -> Any:
    """Main function to run AI project scanner."""
    scanner = AIProjectScanner()
    results = scanner.scan_project()
    with open('ai_project_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    with open('AI_PROJECT_ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(results['report'])
    print('\n🎉 Analysis complete!')
    print('📊 Results saved to: ai_project_analysis.json')
    print('📋 Report saved to: AI_PROJECT_ANALYSIS_REPORT.md')
    print('\n📈 Quick Stats:')
    print(f"   - {results['summary']['total_files']} files analyzed")
    print(f"   - {results['summary']['total_lines']:,} lines of code")
    print(f"   - {len(results['file_analyses'])} detailed file analyses")
    print(f"   - Scan completed in {results['scan_duration']:.2f} seconds")
if __name__ == '__main__':
    main()
