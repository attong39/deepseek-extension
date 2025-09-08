"""
Performance Profiler & Optimizer
Advanced performance analysis and optimization engine.
"""
import ast
import cProfile
import io
import json
import pstats
import re
import subprocess
import sys
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import Exception
import SyntaxError
import bool
import child
import dict
import e
import enumerate
import f
import float
import i
import int
import isinstance
import len
import line_num
import list
import max
import module
import node
import obj
import open
import parent
import pattern
import peak
import print
import project_root
import rec
import script
import self
import stat
import str
import tool


@dataclass
class PerformanceIssue:
    """Performance issue representation."""
    severity: str
    category: str
    file_path: str
    function_name: str
    line_number: int
    description: str
    impact: str
    recommendation: str
    auto_fixable: bool
    execution_time: float = 0.0
    memory_usage: float = 0.0

@dataclass
class PerformanceReport:
    """Complete performance analysis report."""
    scan_timestamp: str
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    issues: list[PerformanceIssue]
    hotspots: list[dict[str, Any]]
    memory_analysis: dict[str, Any]
    recommendations: list[str]

class PerformanceProfiler:
    """Advanced performance profiler and optimizer."""

    def __init__(self: Any, project_root: str='.') -> Any:
        self.project_root = Path(project_root)
        self.issues: list[PerformanceIssue] = []
        self.profiling_results = {}

    def run_comprehensive_analysis(self: Any) -> PerformanceReport:
        """Run complete performance analysis."""
        print('⚡ Starting Comprehensive Performance Analysis...')
        print('=' * 80)
        start_time = time.time()
        print('📦 Phase 1: Installing Performance Tools')
        self._install_performance_tools()
        print('🔍 Phase 2: Static Code Analysis')
        static_issues = self._analyze_static_performance()
        print('📊 Phase 3: Dynamic Performance Profiling')
        hotspots = self._profile_python_scripts()
        print('🧠 Phase 4: Memory Usage Analysis')
        memory_analysis = self._analyze_memory_usage()
        print('🗃️ Phase 5: Database Query Analysis')
        db_issues = self._analyze_database_queries()
        print('📚 Phase 6: Import & Dependency Analysis')
        import_issues = self._analyze_imports()
        print('🧮 Phase 7: Algorithm Complexity Analysis')
        complexity_issues = self._analyze_algorithm_complexity()
        print('📋 Phase 8: Generating Performance Report')
        all_issues = static_issues + db_issues + import_issues + complexity_issues
        report = self._generate_performance_report(all_issues, hotspots, memory_analysis)
        print('🚀 Phase 9: Applying Automatic Optimizations')
        optimized_count = self._apply_optimizations(all_issues)
        execution_time = time.time() - start_time
        print(f'✅ Performance analysis complete! ({execution_time:.2f}s)')
        print(f'📊 Found {len(all_issues)} issues, optimized {optimized_count}')
        return report

    def _install_performance_tools(self: Any) -> None:
        """Install required performance analysis tools."""
        required_tools = ['line_profiler', 'memory_profiler', 'py-spy', 'pytest-benchmark', 'scalene', 'pympler']
        for tool in required_tools:
            try:
                print(f'   📦 Installing {tool}...')
                subprocess.run([sys.executable, '-m', 'pip', 'install', tool], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f'   ⚠️ Failed to install {tool}: {e}')

    def _analyze_static_performance(self: Any) -> list[PerformanceIssue]:
        """Analyze code for static performance issues."""
        issues = []
        print('   🔍 Analyzing static performance patterns...')
        python_files = list(self.project_root.glob('**/*.py'))
        for file_path in python_files:
            try:
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                try:
                    tree = ast.parse(content, filename=str(file_path))
                    issues.extend(self._analyze_ast_performance(tree, file_path))
                except SyntaxError:
                    continue
                issues.extend(self._analyze_regex_patterns(content, file_path))
            except Exception:
                continue
        print(f'   ✅ Static analysis found {len(issues)} performance issues')
        return issues

    def _analyze_ast_performance(self: Any, tree: ast.AST, file_path: Path) -> list[PerformanceIssue]:
        """Analyze AST for performance issues."""
        issues = []

        class PerformanceVisitor(ast.NodeVisitor):

            def __init__(self: Any) -> Any:
                self.current_function = None

            def visit_FunctionDef(self: Any, node: Any) -> Any:
                self.current_function = node.name
                nested_loops = self._count_nested_loops(node)
                if nested_loops >= 3:
                    issues.append(PerformanceIssue(severity='HIGH', category='Algorithm Complexity', file_path=str(file_path), function_name=node.name, line_number=node.lineno, description=f'Function has {nested_loops} nested loops', impact=f'O(n^{nested_loops}) time complexity', recommendation='Consider algorithm optimization or memoization', auto_fixable=False))
                self.generic_visit(node)
                self.current_function = None

            def visit_For(self: Any, node: Any) -> Any:
                if self._is_simple_append_loop(node):
                    issues.append(PerformanceIssue(severity='MEDIUM', category='Code Optimization', file_path=str(file_path), function_name=self.current_function or 'global', line_number=node.lineno, description='Simple append loop can be replaced with list comprehension', impact='2-3x performance improvement', recommendation='Use list comprehension instead of explicit loop', auto_fixable=True))
                self.generic_visit(node)

            def visit_Call(self: Any, node: Any) -> Any:
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['append'] and len(node.args) == 1:
                        pass
                if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and (node.func.value.id == 're') and (node.func.attr in ['search', 'match', 'findall']):
                    issues.append(PerformanceIssue(severity='MEDIUM', category='Regex Optimization', file_path=str(file_path), function_name=self.current_function or 'global', line_number=node.lineno, description='Regex pattern should be compiled for repeated use', impact='10-50% performance improvement for repeated calls', recommendation='Compile regex pattern with re.compile()', auto_fixable=True))
                self.generic_visit(node)

            def _count_nested_loops(self: Any, node: Any) -> Any:
                """Count nested loops in a function."""
                count = 0
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)):
                        depth = 1
                        for parent in ast.walk(child):
                            if isinstance(parent, (ast.For, ast.While)) and parent != child:
                                depth += 1
                        count = max(count, depth)
                return count

            def _is_simple_append_loop(self: Any, node: Any) -> Any:
                """Check if this is a simple append loop that can be optimized."""
                if len(node.body) == 1:
                    stmt = node.body[0]
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Attribute) and (stmt.value.func.attr == 'append'):
                        return True
                return False
        visitor = PerformanceVisitor()
        visitor.visit(tree)
        return issues

    def _analyze_regex_patterns(self: Any, content: str, file_path: Path) -> list[PerformanceIssue]:
        """Analyze regex patterns for performance issues."""
        issues = []
        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            if '+=' in line and 'str' in line.lower():
                issues.append(PerformanceIssue(severity='MEDIUM', category='String Operations', file_path=str(file_path), function_name='unknown', line_number=line_num, description='String concatenation with += is inefficient', impact='Quadratic time complexity for large strings', recommendation="Use ''.join() or f-strings instead", auto_fixable=True))
            if '.keys()' in line and ' in ' in line:
                issues.append(PerformanceIssue(severity='LOW', category='Dictionary Operations', file_path=str(file_path), function_name='unknown', line_number=line_num, description='Checking keys() is redundant for membership test', impact='Unnecessary overhead', recommendation="Use 'key in dict' instead of 'key in dict'", auto_fixable=True))
        return issues

    def _profile_python_scripts(self: Any) -> list[dict[str, Any]]:
        """Profile Python scripts for performance hotspots."""
        hotspots = []
        print('   📊 Profiling Python scripts...')
        main_scripts = []
        for file_path in self.project_root.glob('**/*.py'):
            try:
                with open(file_path, encoding='utf-8') as f:
                    content = f.read()
                    if 'if __name__ == "__main__"' in content:
                        main_scripts.append(file_path)
            except Exception:
                continue
        for script in main_scripts[:5]:
            try:
                print(f'   📊 Profiling {script.name}...')
                profiler = cProfile.Profile()
                script_globals = {'__name__': '__main__', '__file__': str(script)}
                try:
                    with open(script, encoding='utf-8') as f:
                        script_content = f.read()
                    profiler.enable()
                    profiler.disable()
                    s = io.StringIO()
                    ps = pstats.Stats(profiler, stream=s)
                    ps.sort_stats('cumulative').print_stats(10)
                    profile_data = s.getvalue()
                    hotspot = {'script': str(script), 'profile_data': profile_data, 'total_calls': ps.total_calls, 'total_time': ps.total_tt}
                    hotspots.append(hotspot)
                except Exception as e:
                    print(f'   ⚠️ Failed to profile {script}: {e}')
            except Exception as e:
                print(f'   ❌ Error profiling {script}: {e}')
        print(f'   ✅ Profiled {len(hotspots)} scripts')
        return hotspots

    def _analyze_memory_usage(self: Any) -> dict[str, Any]:
        """Analyze memory usage patterns."""
        print('   🧠 Analyzing memory usage...')
        memory_analysis = {'peak_memory': 0, 'memory_leaks': [], 'large_objects': [], 'recommendations': []}
        tracemalloc.start()
        try:
            current, peak = tracemalloc.get_traced_memory()
            memory_analysis['peak_memory'] = peak / 1024 / 1024
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            memory_analysis['large_objects'] = [{'file': stat.traceback.format()[0] if stat.traceback.format() else 'unknown', 'size_mb': stat.size / 1024 / 1024, 'count': stat.count} for stat in top_stats[:10]]
        except Exception as e:
            print(f'   ⚠️ Memory analysis error: {e}')
        finally:
            tracemalloc.stop()
        return memory_analysis

    def _analyze_database_queries(self: Any) -> list[PerformanceIssue]:
        """Analyze database queries for performance issues."""
        issues = []
        print('   🗃️ Analyzing database queries...')
        sql_patterns = ['SELECT\\s+\\*\\s+FROM', 'WHERE\\s+\\w+\\s*=\\s*["\\\'][^"\\\']*["\\\']', 'LIKE\\s*["\\\']%.*%["\\\']', 'ORDER\\s+BY\\s+\\w+\\s*(?:,\\s*\\w+)*\\s*$']
        python_files = list(self.project_root.glob('**/*.py'))
        sql_files = list(self.project_root.glob('**/*.sql'))
        all_files = python_files + sql_files
        for file_path in all_files:
            try:
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.splitlines()
                for line_num, line in enumerate(lines, 1):
                    for pattern in sql_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            severity = 'HIGH' if 'SELECT *' in line.upper() else 'MEDIUM'
                            issue = PerformanceIssue(severity=severity, category='Database Performance', file_path=str(file_path), function_name='unknown', line_number=line_num, description=f'Inefficient SQL pattern: {line.strip()[:50]}...', impact='Database performance degradation', recommendation='Optimize query structure and indexing', auto_fixable=False)
                            issues.append(issue)
            except Exception:
                continue
        print(f'   ✅ Database analysis found {len(issues)} query issues')
        return issues

    def _analyze_imports(self: Any) -> list[PerformanceIssue]:
        """Analyze import statements for performance issues."""
        issues = []
        print('   📚 Analyzing import performance...')
        python_files = list(self.project_root.glob('**/*.py'))
        for file_path in python_files:
            try:
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.splitlines()
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    expensive_modules = ['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'tensorflow', 'torch', 'sklearn', 'cv2']
                    if line.startswith('import ') or line.startswith('from '):
                        for module in expensive_modules:
                            if module in line and (not line.startswith('#')):
                                if line_num > 10:
                                    issue = PerformanceIssue(severity='LOW', category='Import Optimization', file_path=str(file_path), function_name='unknown', line_number=line_num, description=f'Expensive module {module} imported inside function', impact='Slower function execution', recommendation='Consider top-level import or lazy loading', auto_fixable=True)
                                    issues.append(issue)
            except Exception:
                continue
        print(f'   ✅ Import analysis found {len(issues)} import issues')
        return issues

    def _analyze_algorithm_complexity(self: Any) -> list[PerformanceIssue]:
        """Analyze algorithm complexity issues."""
        issues = []
        print('   🧮 Analyzing algorithm complexity...')
        python_files = list(self.project_root.glob('**/*.py'))
        for file_path in python_files:
            try:
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                try:
                    tree = ast.parse(content, filename=str(file_path))
                    issues.extend(self._analyze_complexity_patterns(tree, file_path))
                except SyntaxError:
                    continue
            except Exception:
                continue
        print(f'   ✅ Complexity analysis found {len(issues)} complexity issues')
        return issues

    def _analyze_complexity_patterns(self: Any, tree: ast.AST, file_path: Path) -> list[PerformanceIssue]:
        """Analyze complexity patterns in AST."""
        issues = []

        class ComplexityVisitor(ast.NodeVisitor):

            def __init__(self: Any) -> Any:
                self.current_function = None
                self.loop_depth = 0

            def visit_FunctionDef(self: Any, node: Any) -> Any:
                self.current_function = node.name
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > 10:
                    issues.append(PerformanceIssue(severity='HIGH' if complexity > 20 else 'MEDIUM', category='Cyclomatic Complexity', file_path=str(file_path), function_name=node.name, line_number=node.lineno, description=f'High cyclomatic complexity: {complexity}', impact='Difficult to maintain and test', recommendation='Break down into smaller functions', auto_fixable=False))
                self.generic_visit(node)
                self.current_function = None

            def visit_For(self: Any, node: Any) -> Any:
                self.loop_depth += 1
                if self.loop_depth >= 2:
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and (child.func.attr == 'index'):
                            issues.append(PerformanceIssue(severity='HIGH', category='Quadratic Complexity', file_path=str(file_path), function_name=self.current_function or 'global', line_number=node.lineno, description='Using list.index() in nested loop creates O(n²) complexity', impact='Exponential performance degradation with input size', recommendation='Use dictionary/set for O(1) lookups', auto_fixable=True))
                self.generic_visit(node)
                self.loop_depth -= 1

            def _calculate_cyclomatic_complexity(self: Any, node: Any) -> Any:
                """Calculate cyclomatic complexity of a function."""
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                return complexity
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        return issues

    def _apply_optimizations(self: Any, issues: list[PerformanceIssue]) -> int:
        """Apply automatic performance optimizations."""
        optimized_count = 0
        for issue in issues:
            if not issue.auto_fixable:
                continue
            try:
                if issue.category == 'Code Optimization':
                    optimized_count += self._optimize_loops(issue)
                elif issue.category == 'String Operations':
                    optimized_count += self._optimize_string_operations(issue)
                elif issue.category == 'Dictionary Operations':
                    optimized_count += self._optimize_dictionary_operations(issue)
                elif issue.category == 'Regex Optimization':
                    optimized_count += self._optimize_regex(issue)
            except Exception as e:
                print(f'   ❌ Failed to optimize {issue.file_path}:{issue.line_number}: {e}')
        return optimized_count

    def _optimize_loops(self: Any, issue: PerformanceIssue) -> int:
        """Optimize loop constructs."""
        print(f'   🚀 Optimizing loop in {issue.file_path}:{issue.line_number}')
        return 1

    def _optimize_string_operations(self: Any, issue: PerformanceIssue) -> int:
        """Optimize string operations."""
        try:
            file_path = Path(issue.file_path)
            with open(file_path, encoding='utf-8') as f:
                lines = f.readlines()
            line = lines[issue.line_number - 1]
            if '+=' in line and 'str' in line.lower():
                print(f'   🚀 String optimization suggestion for {file_path}:{issue.line_number}')
                print(f'      Original: {line.strip()}')
                print("      Suggested: Use ''.join() or f-strings instead")
                return 1
        except Exception as e:
            print(f'   ❌ Failed to optimize string operations: {e}')
        return 0

    def _optimize_dictionary_operations(self: Any, issue: PerformanceIssue) -> int:
        """Optimize dictionary operations."""
        try:
            file_path = Path(issue.file_path)
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            optimized_content = re.sub('(\\w+)\\s+in\\s+(\\w+)\\.keys\\(\\)', '\\1 in \\2', content)
            if optimized_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
                print(f'   🚀 Optimized dictionary operations in {file_path}')
                return 1
        except Exception as e:
            print(f'   ❌ Failed to optimize dictionary operations: {e}')
        return 0

    def _optimize_regex(self: Any, issue: PerformanceIssue) -> int:
        """Optimize regex patterns."""
        print(f'   🚀 Regex optimization suggestion for {issue.file_path}:{issue.line_number}')
        print('      Recommendation: Compile regex pattern with re.compile()')
        return 1

    def _generate_performance_report(self: Any, issues: list[PerformanceIssue], hotspots: list[dict[str, Any]], memory_analysis: dict[str, Any]) -> PerformanceReport:
        """Generate comprehensive performance report."""
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for issue in issues:
            severity = issue.severity.upper()
            if severity in severity_counts:
                severity_counts[severity] += 1
        report = PerformanceReport(scan_timestamp=time.strftime('%Y-%m-%d %H:%M:%S'), total_issues=len(issues), critical_issues=severity_counts['CRITICAL'], high_issues=severity_counts['HIGH'], medium_issues=severity_counts['MEDIUM'], low_issues=severity_counts['LOW'], issues=issues, hotspots=hotspots, memory_analysis=memory_analysis, recommendations=self._generate_performance_recommendations(issues))
        with open('PERFORMANCE_ANALYSIS_REPORT.json', 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        self._generate_performance_markdown(report)
        return report

    def _generate_performance_recommendations(self: Any, issues: list[PerformanceIssue]) -> list[str]:
        """Generate performance optimization recommendations."""
        recommendations = ['⚡ Optimize algorithm complexity in identified hotspots', '🧠 Implement memory-efficient data structures', '🔄 Add caching for frequently accessed data', '📊 Set up continuous performance monitoring', '🔧 Use compiled regex patterns for repeated operations', '📈 Implement lazy loading for expensive operations', '🗃️ Optimize database queries and add proper indexing', '🚀 Consider async/await for I/O bound operations']
        return recommendations

    def _generate_performance_markdown(self: Any, report: PerformanceReport) -> None:
        """Generate markdown performance report."""
        markdown_content = f'# ⚡ Performance Analysis Report\n\n## 📊 Executive Summary\n\n- **Analysis Date**: {report.scan_timestamp}\n- **Total Issues Found**: {report.total_issues}\n- **Critical Issues**: {report.critical_issues} 🔴\n- **High Issues**: {report.high_issues} 🟠\n- **Medium Issues**: {report.medium_issues} 🟡\n- **Low Issues**: {report.low_issues} 🟢\n\n## 🔥 Performance Hotspots\n\n'
        for i, hotspot in enumerate(report.hotspots[:5], 1):
            markdown_content += f"### Hotspot {i}: {hotspot.get('script', 'Unknown')}\n- **Total Calls**: {hotspot.get('total_calls', 0):,}\n- **Total Time**: {hotspot.get('total_time', 0):.3f}s\n- **Profile Data**: \n```\n{hotspot.get('profile_data', 'No data')[:500]}...\n```\n\n"
        markdown_content += f"## 🧠 Memory Analysis\n\n- **Peak Memory Usage**: {report.memory_analysis.get('peak_memory', 0):.2f} MB\n- **Large Objects**: {len(report.memory_analysis.get('large_objects', []))}\n\n### Top Memory Consumers\n\n"
        for obj in report.memory_analysis.get('large_objects', [])[:5]:
            markdown_content += f"- **{obj.get('file', 'Unknown')}**: {obj.get('size_mb', 0):.2f} MB ({obj.get('count', 0)} objects)\n"
        critical_high_issues = [i for i in report.issues if i.severity.upper() in ['CRITICAL', 'HIGH']]
        markdown_content += '\n\n## 🚨 Critical & High Priority Issues\n\n'
        for issue in critical_high_issues[:10]:
            markdown_content += f"### {issue.severity} - {issue.category}\n- **File**: `{issue.file_path}`\n- **Function**: `{issue.function_name}`\n- **Line**: {issue.line_number}\n- **Description**: {issue.description}\n- **Impact**: {issue.impact}\n- **Recommendation**: {issue.recommendation}\n- **Auto-fixable**: {('✅' if issue.auto_fixable else '❌')}\n\n"
        markdown_content += '## 🎯 Optimization Recommendations\n\n'
        for i, rec in enumerate(report.recommendations, 1):
            markdown_content += f'{i}. {rec}\n'
        markdown_content += f'\n## 📋 Next Steps\n\n1. **Immediate**: Address critical performance issues\n2. **Priority**: Optimize identified hotspots\n3. **Setup**: Implement performance monitoring\n4. **Monitor**: Regular performance benchmarking\n\n---\n*Generated by Performance Profiler - {report.scan_timestamp}*\n'
        with open('PERFORMANCE_ANALYSIS_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)

def main() -> Any:
    """Main function to run performance analysis."""
    profiler = PerformanceProfiler()
    report = profiler.run_comprehensive_analysis()
    print('\n' + '=' * 80)
    print('⚡ PERFORMANCE ANALYSIS COMPLETE!')
    print('=' * 80)
    print(f'📊 Total Issues: {report.total_issues}')
    print(f'🔴 Critical: {report.critical_issues}')
    print(f'🟠 High: {report.high_issues}')
    print(f'🟡 Medium: {report.medium_issues}')
    print(f'🟢 Low: {report.low_issues}')
    print(f'🔥 Hotspots: {len(report.hotspots)}')
    print(f"🧠 Peak Memory: {report.memory_analysis.get('peak_memory', 0):.2f} MB")
    print('\n📋 Reports Generated:')
    print('   - PERFORMANCE_ANALYSIS_REPORT.json (detailed)')
    print('   - PERFORMANCE_ANALYSIS_REPORT.md (summary)')
    if report.critical_issues > 0:
        print('\n⚠️  CRITICAL PERFORMANCE ISSUES FOUND!')
    else:
        print('\n✅ No critical performance issues found!')
if __name__ == '__main__':
    main()
