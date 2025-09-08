"""
Security Audit & Fix Engine
Comprehensive security scanning and automated fixes for the project.
"""
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import Exception
import bandit_result
import bool
import config_file
import description
import dict
import e
import enumerate
import f
import i
import int
import len
import line
import line_num
import list
import open
import pattern
import print
import project_root
import rec
import replacement
import result_item
import self
import str
import tool
import vuln


@dataclass
class SecurityIssue:
    """Security issue representation."""
    severity: str
    type: str
    file_path: str
    line_number: int
    description: str
    recommendation: str
    auto_fixable: bool

@dataclass
class SecurityReport:
    """Complete security audit report."""
    scan_timestamp: str
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    issues: list[SecurityIssue]
    dependencies: dict[str, Any]
    recommendations: list[str]

class SecurityAuditor:
    """Comprehensive security auditor and fixer."""

    def __init__(self: Any, project_root: str='.') -> Any:
        self.project_root = Path(project_root)
        self.security_tools = {'bandit': 'bandit', 'safety': 'safety', 'semgrep': 'semgrep', 'pip-audit': 'pip-audit'}
        self.issues: list[SecurityIssue] = []

    def run_comprehensive_audit(self: Any) -> SecurityReport:
        """Run complete security audit."""
        print('🔒 Starting Comprehensive Security Audit...')
        print('=' * 80)
        start_time = time.time()
        print('📦 Phase 1: Installing Security Tools')
        self._install_security_tools()
        print('🔍 Phase 2: Static Code Analysis')
        bandit_issues = self._run_bandit_scan()
        semgrep_issues = self._run_semgrep_scan()
        print('📚 Phase 3: Dependency Security Analysis')
        safety_issues = self._run_safety_scan()
        audit_issues = self._run_pip_audit()
        print('🔑 Phase 4: Secret Detection')
        secret_issues = self._detect_secrets()
        print('🌍 Phase 5: Environment Configuration Analysis')
        env_issues = self._analyze_environment_configs()
        print('📊 Phase 6: Generating Security Report')
        all_issues = bandit_issues + semgrep_issues + safety_issues + audit_issues + secret_issues + env_issues
        report = self._generate_security_report(all_issues)
        print('🔧 Phase 7: Applying Automatic Fixes')
        fixed_count = self._apply_auto_fixes(all_issues)
        execution_time = time.time() - start_time
        print(f'✅ Security audit complete! ({execution_time:.2f}s)')
        print(f'📊 Found {len(all_issues)} issues, auto-fixed {fixed_count}')
        return report

    def _install_security_tools(self: Any) -> None:
        """Install required security tools."""
        required_tools = ['bandit[toml]', 'safety', 'pip-audit', 'semgrep', 'detect-secrets']
        for tool in required_tools:
            try:
                print(f'   📦 Installing {tool}...')
                subprocess.run([sys.executable, '-m', 'pip', 'install', tool], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f'   ⚠️ Failed to install {tool}: {e}')

    def _run_bandit_scan(self: Any) -> list[SecurityIssue]:
        """Run Bandit static security analysis."""
        issues = []
        try:
            print('   🔍 Running Bandit scan...')
            result = subprocess.run(['bandit', '-r', str(self.project_root), '-f', 'json', '-ll'], capture_output=True, text=True)
            if result.stdout:
                bandit_data = json.loads(result.stdout)
                for result_item in bandit_data.get('results', []):
                    issue = SecurityIssue(severity=result_item.get('issue_severity', 'UNKNOWN'), type='Static Analysis', file_path=result_item.get('filename', ''), line_number=result_item.get('line_number', 0), description=result_item.get('issue_text', ''), recommendation=result_item.get('test_name', ''), auto_fixable=self._is_auto_fixable_bandit(result_item))
                    issues.append(issue)
                print(f'   ✅ Bandit found {len(issues)} issues')
        except Exception as e:
            print(f'   ❌ Bandit scan failed: {e}')
        return issues

    def _run_semgrep_scan(self: Any) -> list[SecurityIssue]:
        """Run Semgrep security analysis."""
        issues = []
        try:
            print('   🔍 Running Semgrep scan...')
            result = subprocess.run(['semgrep', '--config=auto', '--json', str(self.project_root)], capture_output=True, text=True)
            if result.stdout:
                semgrep_data = json.loads(result.stdout)
                for result_item in semgrep_data.get('results', []):
                    issue = SecurityIssue(severity=result_item.get('extra', {}).get('severity', 'INFO'), type='Pattern Analysis', file_path=result_item.get('path', ''), line_number=result_item.get('start', {}).get('line', 0), description=result_item.get('extra', {}).get('message', ''), recommendation=result_item.get('check_id', ''), auto_fixable=False)
                    issues.append(issue)
                print(f'   ✅ Semgrep found {len(issues)} issues')
        except Exception as e:
            print(f'   ❌ Semgrep scan failed: {e}')
        return issues

    def _run_safety_scan(self: Any) -> list[SecurityIssue]:
        """Run Safety dependency vulnerability scan."""
        issues = []
        try:
            print('   🔍 Running Safety scan...')
            result = subprocess.run(['safety', 'check', '--json'], capture_output=True, text=True)
            if result.stdout:
                safety_data = json.loads(result.stdout)
                for vuln in safety_data:
                    issue = SecurityIssue(severity='HIGH', type='Dependency Vulnerability', file_path='requirements.txt', line_number=0, description=f"{vuln.get('package_name', '')} {vuln.get('installed_version', '')}: {vuln.get('advisory', '')}", recommendation=f"Upgrade to {vuln.get('spec', '')}", auto_fixable=True)
                    issues.append(issue)
                print(f'   ✅ Safety found {len(issues)} vulnerabilities')
        except Exception as e:
            print(f'   ❌ Safety scan failed: {e}')
        return issues

    def _run_pip_audit(self: Any) -> list[SecurityIssue]:
        """Run pip-audit for dependency analysis."""
        issues = []
        try:
            print('   🔍 Running pip-audit...')
            result = subprocess.run(['pip-audit', '--format=json'], capture_output=True, text=True)
            if result.stdout:
                audit_data = json.loads(result.stdout)
                for vuln in audit_data.get('vulnerabilities', []):
                    issue = SecurityIssue(severity='HIGH', type='Package Audit', file_path='installed packages', line_number=0, description=f"{vuln.get('package', '')} {vuln.get('installed_version', '')}: {vuln.get('description', '')}", recommendation=f"Fix available: {vuln.get('fix_versions', [])}", auto_fixable=True)
                    issues.append(issue)
                print(f'   ✅ pip-audit found {len(issues)} vulnerabilities')
        except Exception as e:
            print(f'   ❌ pip-audit failed: {e}')
        return issues

    def _detect_secrets(self: Any) -> list[SecurityIssue]:
        """Detect hardcoded secrets and credentials."""
        issues = []
        print('   🔍 Detecting secrets and credentials...')
        secret_patterns = [('password\\s*=\\s*["\\\'][^"\\\']{8,}["\\\']', 'Hardcoded password'), ('api_key\\s*=\\s*["\\\'][^"\\\']{16,}["\\\']', 'Hardcoded API key'), ('secret\\s*=\\s*["\\\'][^"\\\']{16,}["\\\']', 'Hardcoded secret'), ('token\\s*=\\s*["\\\'][^"\\\']{16,}["\\\']', 'Hardcoded token'), ('["\\\']sk-[a-zA-Z0-9]{32,}["\\\']', 'OpenAI API key'), ('["\\\']AIza[a-zA-Z0-9_-]{35}["\\\']', 'Google API key'), ('["\\\']AKIA[A-Z0-9]{16}["\\\']', 'AWS Access Key'), ('["\\\'](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?["\\\']', 'Base64 encoded secret')]
        python_files = list(self.project_root.glob('**/*.py'))
        config_files = list(self.project_root.glob('**/*.env*')) + list(self.project_root.glob('**/*.yaml')) + list(self.project_root.glob('**/*.json'))
        all_files = python_files + config_files
        for file_path in all_files:
            try:
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.splitlines()
                for line_num, line in enumerate(lines, 1):
                    for pattern, description in secret_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            issue = SecurityIssue(severity='CRITICAL', type='Secret Detection', file_path=str(file_path), line_number=line_num, description=f'{description}: {line.strip()[:50]}...', recommendation='Move to environment variables or secure vault', auto_fixable=True)
                            issues.append(issue)
            except Exception:
                continue
        print(f'   ✅ Secret detection found {len(issues)} potential secrets')
        return issues

    def _analyze_environment_configs(self: Any) -> list[SecurityIssue]:
        """Analyze environment configuration files."""
        issues = []
        print('   🔍 Analyzing environment configurations...')
        config_files = ['.env', '.env.local', '.env.development', '.env.production', 'config.yaml', 'config.yml', 'settings.yaml', 'settings.yml']
        for config_file in config_files:
            file_path = self.project_root / config_file
            if file_path.exists():
                try:
                    with open(file_path) as f:
                        content = f.read()
                    if 'DEBUG=True' in content or 'DEBUG = True' in content:
                        issue = SecurityIssue(severity='MEDIUM', type='Configuration', file_path=str(file_path), line_number=0, description='DEBUG mode enabled in production config', recommendation='Set DEBUG=False in production', auto_fixable=True)
                        issues.append(issue)
                except Exception:
                    continue
        print(f'   ✅ Environment analysis found {len(issues)} configuration issues')
        return issues

    def _is_auto_fixable_bandit(self: Any, bandit_result: dict) -> bool:
        """Check if a Bandit issue can be auto-fixed."""
        auto_fixable_tests = ['B101', 'B601', 'B602', 'B604']
        test_id = bandit_result.get('test_id', '')
        return test_id in auto_fixable_tests

    def _apply_auto_fixes(self: Any, issues: list[SecurityIssue]) -> int:
        """Apply automatic fixes for fixable security issues."""
        fixed_count = 0
        for issue in issues:
            if not issue.auto_fixable:
                continue
            try:
                if issue.type == 'Secret Detection':
                    fixed_count += self._fix_hardcoded_secret(issue)
                elif issue.type == 'Configuration':
                    fixed_count += self._fix_configuration_issue(issue)
                elif issue.type == 'Static Analysis':
                    fixed_count += self._fix_static_analysis_issue(issue)
            except Exception as e:
                print(f'   ❌ Failed to fix {issue.file_path}:{issue.line_number}: {e}')
        return fixed_count

    def _fix_hardcoded_secret(self: Any, issue: SecurityIssue) -> int:
        """Fix hardcoded secrets by moving to environment variables."""
        try:
            file_path = Path(issue.file_path)
            backup_path = file_path.with_suffix(f'{file_path.suffix}.security_backup')
            shutil.copy2(file_path, backup_path)
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            patterns_replacements = [('password\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'password = os.getenv("PASSWORD")'), ('api_key\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'api_key = os.getenv("API_KEY")'), ('secret\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'secret = os.getenv("SECRET")'), ('token\\s*=\\s*["\\\'][^"\\\']+["\\\']', 'token = os.getenv("TOKEN")')]
            for pattern, replacement in patterns_replacements:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if 'import os' not in content and 'os.getenv' in content:
                content = 'import os\n' + content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'   🔧 Fixed hardcoded secret in {file_path}')
            return 1
        except Exception as e:
            print(f'   ❌ Failed to fix secret in {issue.file_path}: {e}')
            return 0

    def _fix_configuration_issue(self: Any, issue: SecurityIssue) -> int:
        """Fix configuration security issues."""
        try:
            file_path = Path(issue.file_path)
            with open(file_path) as f:
                content = f.read()
            if 'DEBUG=True' in issue.description:
                content = content.replace('DEBUG=True', 'DEBUG=False')
                content = content.replace('DEBUG = True', 'DEBUG = False')
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f'   🔧 Fixed DEBUG configuration in {file_path}')
                return 1
        except Exception as e:
            print(f'   ❌ Failed to fix configuration in {issue.file_path}: {e}')
        return 0

    def _fix_static_analysis_issue(self: Any, issue: SecurityIssue) -> int:
        """Fix static analysis security issues."""
        print(f'   📝 Static analysis issue logged: {issue.description}')
        return 0

    def _generate_security_report(self: Any, issues: list[SecurityIssue]) -> SecurityReport:
        """Generate comprehensive security report."""
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for issue in issues:
            severity = issue.severity.upper()
            if severity in severity_counts:
                severity_counts[severity] += 1
        report = SecurityReport(scan_timestamp=time.strftime('%Y-%m-%d %H:%M:%S'), total_issues=len(issues), critical_issues=severity_counts['CRITICAL'], high_issues=severity_counts['HIGH'], medium_issues=severity_counts['MEDIUM'], low_issues=severity_counts['LOW'], issues=issues, dependencies={}, recommendations=self._generate_recommendations(issues))
        with open('SECURITY_AUDIT_REPORT.json', 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        self._generate_markdown_report(report)
        return report

    def _generate_recommendations(self: Any, issues: list[SecurityIssue]) -> list[str]:
        """Generate security recommendations."""
        recommendations = ['🔒 Implement secure secret management (Azure Key Vault/AWS Secrets Manager)', '🔧 Set up automated security scanning in CI/CD pipeline', '📚 Update all dependencies to latest secure versions', '🌍 Review and secure all environment configurations', '🔍 Implement regular security audits and penetration testing', '📋 Create security incident response plan', '🛡️ Add security headers to all web responses', '🔐 Implement proper authentication and authorization']
        return recommendations

    def _generate_markdown_report(self: Any, report: SecurityReport) -> None:
        """Generate markdown security report."""
        markdown_content = f'# 🔒 Security Audit Report\n\n## 📊 Executive Summary\n\n- **Scan Date**: {report.scan_timestamp}\n- **Total Issues Found**: {report.total_issues}\n- **Critical Issues**: {report.critical_issues} 🔴\n- **High Issues**: {report.high_issues} 🟠  \n- **Medium Issues**: {report.medium_issues} 🟡\n- **Low Issues**: {report.low_issues} 🟢\n\n## 🚨 Critical & High Priority Issues\n\n'
        critical_high_issues = [i for i in report.issues if i.severity.upper() in ['CRITICAL', 'HIGH']]
        for issue in critical_high_issues[:10]:
            markdown_content += f"### {issue.severity} - {issue.type}\n- **File**: `{issue.file_path}`\n- **Line**: {issue.line_number}\n- **Description**: {issue.description}\n- **Recommendation**: {issue.recommendation}\n- **Auto-fixable**: {('✅' if issue.auto_fixable else '❌')}\n\n"
        markdown_content += '## 🎯 Recommendations\n\n'
        for i, rec in enumerate(report.recommendations, 1):
            markdown_content += f'{i}. {rec}\n'
        markdown_content += f'\n## 📋 Next Steps\n\n1. **Immediate Action**: Fix all CRITICAL issues\n2. **Priority**: Address HIGH severity issues  \n3. **Setup**: Implement automated security scanning\n4. **Monitor**: Regular security audits\n\n---\n*Generated by Security Auditor - {report.scan_timestamp}*\n'
        with open('SECURITY_AUDIT_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(markdown_content)

def main() -> Any:
    """Main function to run security audit."""
    auditor = SecurityAuditor()
    report = auditor.run_comprehensive_audit()
    print('\n' + '=' * 80)
    print('🔒 SECURITY AUDIT COMPLETE!')
    print('=' * 80)
    print(f'📊 Total Issues: {report.total_issues}')
    print(f'🔴 Critical: {report.critical_issues}')
    print(f'🟠 High: {report.high_issues}')
    print(f'🟡 Medium: {report.medium_issues}')
    print(f'🟢 Low: {report.low_issues}')
    print('\n📋 Reports Generated:')
    print('   - SECURITY_AUDIT_REPORT.json (detailed)')
    print('   - SECURITY_AUDIT_REPORT.md (summary)')
    if report.critical_issues > 0:
        print('\n⚠️  CRITICAL ISSUES FOUND - IMMEDIATE ACTION REQUIRED!')
    else:
        print('\n✅ No critical security issues found!')
if __name__ == '__main__':
    main()
