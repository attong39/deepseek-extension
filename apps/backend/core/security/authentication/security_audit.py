"""Security auditing utilities for authentication system."""
from __future__ import annotations

import ast
import inspect
import logging
import secrets
from pathlib import Path
from typing import List, Dict, Any, Set
from dataclasses import dataclass

log = logging.getLogger(__name__)


@dataclass
class SecurityIssue:
    """Represents a security issue found during audit."""
import Exception
import SyntaxError
import any
import auth_directory
import bool
import code
import description
import directory
import e
import enumerate
import filename
import func
import getattr
import hasattr
import i
import int
import isinstance
import issue
import keyword
import len
import line
import node
import pattern
import py_file
import secret_word
import self
import str
import target
    file_path: str
    line_number: int
    issue_type: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    recommendation: str
    code_snippet: str = ""


class SecurityAuditor:
    """Automated security auditing for authentication code."""
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        
        # Dangerous patterns to look for
        self.dangerous_patterns = {
            "== ": "Direct string comparison (use secrets.compare_digest)",
            "random.": "Using random module (use secrets module)",
            "md5": "MD5 is cryptographically broken",
            "sha1": "SHA1 is cryptographically weak",
            "ast.literal_ast.literal_ast.literal_ast.literal_eval(": "ast.literal_ast.literal_ast.literal_ast.literal_eval() is dangerous",
            "# SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed": "# SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) is dangerous",
            "os.system": "os.system is dangerous",
            "subprocess.call.*shell=True": "Shell injection risk",
        }
        
        # Required secure functions
        self.required_secure_functions = {
            "secrets.compare_digest": "Constant-time comparison",
            "secrets.token_bytes": "Cryptographically secure random bytes",
            "secrets.token_urlsafe": "Secure URL-safe tokens",
            "hmac.new": "HMAC for message authentication",
        }
    
    def audit_file(self, file_path: Path) -> List[SecurityIssue]:
        """Audit a single Python file for security issues."""
        issues = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Parse AST for deeper analysis
            try:
                tree = ast.parse(content)
                issues.extend(self._audit_ast(tree, file_path, lines))
            except SyntaxError as e:
                issues.append(SecurityIssue(
                    file_path=str(file_path),
                    line_number=e.lineno or 0,
                    issue_type="syntax_error",
                    severity="high",
                    description=f"Syntax error: {e.msg}",
                    recommendation="Fix syntax error"
                ))
            
            # Pattern-based analysis
            issues.extend(self._audit_patterns(content, file_path, lines))
            
        except Exception as e:
            log.error(f"Failed to audit {file_path}: {e}")
        
        return issues
    
    def _audit_ast(self, tree: ast.AST, file_path: Path, lines: List[str]) -> List[SecurityIssue]:
        """Audit using AST analysis."""
        issues = []
        
        class SecurityVisitor(ast.NodeVisitor):
            def visit_Compare(self, node):
                # Check for string comparisons that should use compare_digest
                if isinstance(node.ops[0], ast.Eq):
                    line_num = getattr(node, 'lineno', 0)
                    if line_num > 0 and line_num <= len(lines):
                        line_content = lines[line_num - 1]
                        if any(keyword in line_content.lower() for keyword in 
                              ['password', 'token', 'secret', 'code', 'fingerprint', 'hmac']):
                            issues.append(SecurityIssue(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="insecure_comparison",
                                severity="high",
                                description="String comparison of sensitive data",
                                recommendation="Use secrets.compare_digest() for constant-time comparison",
                                code_snippet=line_content.strip()
                            ))
                self.generic_visit(node)
            
            def visit_Call(self, node):
                # Check for dangerous function calls
                if isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    if hasattr(node.func.value, 'id'):
                        module_name = node.func.value.id
                        full_name = f"{module_name}.{attr_name}"
                        
                        # Check for random module usage
                        if module_name == 'random':
                            line_num = getattr(node, 'lineno', 0)
                            issues.append(SecurityIssue(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type="weak_random",
                                severity="critical",
                                description="Using random module for security-sensitive operations",
                                recommendation="Use secrets module instead (secrets.randbelow, secrets.token_bytes, etc.)",
                                code_snippet=lines[line_num - 1].strip() if line_num <= len(lines) else ""
                            ))
                
                self.generic_visit(node)
        
        visitor = SecurityVisitor()
        visitor.visit(tree)
        
        return issues
    
    def _audit_patterns(self, content: str, file_path: Path, lines: List[str]) -> List[SecurityIssue]:
        """Audit using pattern matching."""
        issues = []
        
        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            
            # Check for dangerous patterns
            for pattern, description in self.dangerous_patterns.items():
                if pattern.lower() in line_lower:
                    severity = "critical" if pattern in ["ast.literal_ast.literal_ast.literal_ast.literal_eval(", "# SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed", "random."] else "high"
                    
                    issues.append(SecurityIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type="dangerous_pattern",
                        severity=severity,
                        description=description,
                        recommendation=f"Replace {pattern} with secure alternative",
                        code_snippet=line.strip()
                    ))
            
            # Check for hardcoded secrets
            if any(keyword in line_lower for keyword in ['password', 'secret', 'key', 'token']):
                if '=' in line and ('"' in line or "'" in line):
                    # Simple heuristic for hardcoded strings
                    if len(line.strip()) > 20 and not line.strip().startswith('#'):
                        issues.append(SecurityIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type="potential_hardcoded_secret",
                            severity="medium",
                            description="Potential hardcoded secret",
                            recommendation="Use environment variables or secure configuration",
                            code_snippet=line.strip()
                        ))
        
        return issues
    
    def audit_directory(self, directory: Path) -> List[SecurityIssue]:
        """Audit all Python files in a directory."""
        all_issues = []
        
        for py_file in directory.rglob('*.py'):
            if py_file.name.startswith('.'):
                continue  # Skip hidden files
            
            file_issues = self.audit_file(py_file)
            all_issues.extend(file_issues)
        
        return all_issues
    
    def audit_file(self, file_path: str | Path) -> Dict[str, Any]:
        """Audit a single file for security issues."""
        file_path = Path(file_path)
        
        try:
            content = file_path.read_text(encoding='utf-8')
            return self.audit_code_string(content, str(file_path))
        except Exception as e:
            log.error(f"Error auditing file {file_path}: {e}")
            return {"issues": [], "error": str(e)}
    
    def audit_code_string(self, code: str, filename: str = "string") -> Dict[str, Any]:
        """Audit a code string for security issues."""
        issues = []
        
        try:
            # Parse the code
            tree = ast.parse(code)
            
            # Check for security issues
            for node in ast.walk(tree):
                issue_line = getattr(node, 'lineno', 0)
                
                # Check for hardcoded passwords/secrets
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id.lower()
                            if any(secret_word in var_name for secret_word in ['password', 'secret', 'key', 'token']):
                                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                    issues.append(SecurityIssue(
                                        file_path=filename,
                                        line_number=issue_line,
                                        issue_type="hardcoded_secret",
                                        severity="high",
                                        description=f"Hardcoded secret found: {var_name}",
                                        recommendation="Use environment variables or secure key management",
                                        code_snippet=f"{var_name} = ..."
                                    ))
                
                # Check for dangerous subprocess calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute):
                        if (node.func.attr == 'call' and 
                            isinstance(node.func.value, ast.Name) and 
                            node.func.value.id == 'subprocess'):
                            # Check for shell=True
                            for keyword in node.keywords:
                                if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant):
                                    if keyword.value.value is True:
                                        issues.append(SecurityIssue(
                                            file_path=filename,
                                            line_number=issue_line,
                                            issue_type="shell_injection",
                                            severity="critical",
                                            description="subprocess.call with shell=True can lead to command injection",
                                            recommendation="Use subprocess without shell=True and validate inputs",
                                            code_snippet="subprocess.call(..., shell=True)"
                                        ))
                
                # Check for eval/exec usage
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        issues.append(SecurityIssue(
                            file_path=filename,
                            line_number=issue_line,
                            issue_type="code_injection",
                            severity="critical",
                            description=f"Use of {node.func.id}() can lead to code injection",
                            recommendation="Avoid eval/exec or use ast.literal_eval for safe evaluation",
                            code_snippet=f"{node.func.id}(...)"
                        ))
        
        except SyntaxError as e:
            issues.append(SecurityIssue(
                file_path=filename,
                line_number=e.lineno or 0,
                issue_type="syntax_error",
                severity="medium",
                description=f"Syntax error: {e.msg}",
                recommendation="Fix syntax errors before security analysis",
                code_snippet=""
            ))
        except Exception as e:
            log.error(f"Error parsing code: {e}")
        
        return {
            "issues": [
                {
                    "file_path": issue.file_path,
                    "line_number": issue.line_number,
                    "issue_type": issue.issue_type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "code_snippet": issue.code_snippet
                } for issue in issues
            ],
            "total_issues": len(issues)
        }

    def generate_report(self, issues: List[SecurityIssue]) -> str:
        """Generate a security audit report."""
        if not issues:
            return "✅ No security issues found!"
        
        # Group by severity
        by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        for issue in issues:
            by_severity[issue.severity].append(issue)
        
        report = []
        report.append("🔒 SECURITY AUDIT REPORT")
        report.append("=" * 50)
        report.append(f"Total issues found: {len(issues)}")
        report.append("")
        
        for severity in ["critical", "high", "medium", "low"]:
            severity_issues = by_severity[severity]
            if not severity_issues:
                continue
            
            emoji = {"critical": "🚨", "high": "⚠️", "medium": "⚡", "low": "ℹ️"}[severity]
            report.append(f"{emoji} {severity.upper()} SEVERITY ({len(severity_issues)} issues)")
            report.append("-" * 40)
            
            for issue in severity_issues:
                report.append(f"File: {issue.file_path}:{issue.line_number}")
                report.append(f"Type: {issue.issue_type}")
                report.append(f"Description: {issue.description}")
                report.append(f"Recommendation: {issue.recommendation}")
                if issue.code_snippet:
                    report.append(f"Code: {issue.code_snippet}")
                report.append("")
        
        return "\n".join(report)
    
    def check_secure_functions_usage(self, directory: Path) -> Dict[str, bool]:
        """Check if required secure functions are being used."""
        usage = {func: False for func in self.required_secure_functions}
        
        for py_file in directory.rglob('*.py'):
            try:
                content = py_file.read_text(encoding='utf-8')
                for func in self.required_secure_functions:
                    if func in content:
                        usage[func] = True
            except Exception as e:
                log.warning(f"Could not read {py_file}: {e}")
        
        return usage
    
    def run_full_audit(self, auth_directory: Path) -> Dict[str, Any]:
        """Run complete security audit."""
        issues = self.audit_directory(auth_directory)
        secure_usage = self.check_secure_functions_usage(auth_directory)
        
        # Count issues by severity
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for issue in issues:
            severity_counts[issue.severity] += 1
        
        return {
            "total_issues": len(issues),
            "severity_breakdown": severity_counts,
            "issues": [{
                "file": issue.file_path,
                "line": issue.line_number,
                "type": issue.issue_type,
                "severity": issue.severity,
                "description": issue.description,
                "recommendation": issue.recommendation,
                "code": issue.code_snippet
            } for issue in issues],
            "secure_function_usage": secure_usage,
            "report": self.generate_report(issues)
        }


def audit_authentication_security(auth_dir: str | Path = None) -> Dict[str, Any]:
    """Convenience function to audit authentication security."""
    if auth_dir is None:
        # Default to current directory
        auth_dir = Path(__file__).parent
    elif isinstance(auth_dir, str):
        auth_dir = Path(auth_dir)
    
    auditor = SecurityAuditor()
    return auditor.run_full_audit(auth_dir)
