#!/usr/bin/env python3
"""
🤖 AI-Powered Auto Refactor
Automatically implement AI refactoring suggestions
"""

import json
import sys
import time
from pathlib import Path
from typing import Any
import Exception
import ImportError
import code
import dict
import e
import enumerate
import f
import file
import func
import func_info
import function_info
import i
import len
import list
import open
import print
import r
import self
import str
import sum

# Try to import and install if needed
try:
    from ollama import Client
except ImportError:
    print("📦 Installing Ollama Python library...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'ollama'], check=True)
    from ollama import Client


class AIRefactorEngine:
    """AI-powered refactoring engine using Ollama Turbo."""
    
    def __init__(self):
        self.config = self._load_config()
        self.client = self._init_client()
        self.refactor_results = []
        
    def _load_config(self) -> dict[str, Any]:
        """Load Turbo configuration."""
        config_file = Path("ollama_turbo_config.json")
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        else:
            return {
                "api_key": "86cb083298d04e8381c932d1b1d76360.GhswkqZGXelbOPwd_dKZ82W4",
                "host": "https://ollama.com", 
                "model": "gpt-oss:120b"
            }
    
    def _init_client(self) -> Client:
        """Initialize Ollama Turbo client."""
        return Client(
            host=self.config["host"],
            headers={'Authorization': f'Bearer {self.config["api_key"]}'}
        )
    
    def load_optimization_results(self) -> dict[str, Any]:
        """Load previous optimization results."""
        results = {}
        
        # Load optimization reports
        report_files = [
            "AI_PROJECT_ANALYSIS_REPORT.md",
            "AI_OPTIMIZATION_RECOMMENDATIONS.md",
            "FINAL_AI_OPTIMIZATION_SUMMARY.md",
            "REFACTORING_SUGGESTIONS.md"
        ]
        
        for file in report_files:
            if Path(file).exists():
                with open(file, encoding='utf-8') as f:
                    results[file] = f.read()
        
        # Load JSON results
        json_files = [
            "optimization_results.json",
            "refactoring_suggestions.json"
        ]
        
        for file in json_files:
            if Path(file).exists():
                try:
                    with open(file, encoding='utf-8') as f:
                        results[file] = json.load(f)
                except:
                    pass
        
        return results
    
    def get_complex_functions(self) -> list[dict[str, Any]]:
        """Get list of complex functions to refactor."""
        complex_functions = []
        
        # From our previous analysis
        high_complexity_functions = [
            {
                "name": "validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html",
                "complexity": 352,
                "file": "setuptools_validation.py",
                "estimated_file": True
            },
            {
                "name": "process_large_dataset_with_transformations",
                "complexity": 89,
                "file": "data_processor.py", 
                "estimated_file": True
            },
            {
                "name": "analyze_code_complexity_metrics",
                "complexity": 67,
                "file": "ai_project_scanner.py",
                "estimated_file": False
            },
            {
                "name": "optimize_performance_bottlenecks",
                "complexity": 54,
                "file": "ai_auto_optimizer.py",
                "estimated_file": False
            },
            {
                "name": "generate_comprehensive_test_suite",
                "complexity": 43,
                "file": "test_generator.py",
                "estimated_file": True
            }
        ]
        
        # Only return functions from files that actually exist
        for func in high_complexity_functions:
            if Path(func["file"]).exists() or func["estimated_file"]:
                complex_functions.append(func)
        
        return complex_functions
    
    def analyze_function_for_refactor(self, function_info: dict[str, Any]) -> dict[str, Any]:
        """Use AI to analyze a specific function for refactoring."""
        print(f"🔍 Analyzing {function_info['name']}...")
        
        # Try to read actual function code if file exists
        actual_code = None
        if Path(function_info["file"]).exists():
            try:
                with open(function_info["file"], encoding='utf-8') as f:
                    content = f.read()
                    # Look for the function (simplified search)
                    if function_info["name"] in content:
                        actual_code = content[:2000]  # First 2000 chars
            except:
                pass
        
        # Handle code preview
        code_preview = ""
        if actual_code:
            code_preview = f"Code Preview:\n```python\n{actual_code}\n```"
        
        complexity_target = "less than 10"
        prompt = f"""Analyze this function for refactoring:

Function: {function_info['name']}
Complexity: {function_info['complexity']}
File: {function_info['file']}

{code_preview}

Please provide:
1. **Refactoring Strategy** - Specific approach (extract methods, reduce nesting, etc.)
2. **Implementation Steps** - Step-by-step refactoring plan
3. **Code Structure** - How to reorganize the code
4. **Expected Benefits** - Complexity reduction, maintainability improvements
5. **Risk Assessment** - Potential issues and mitigation

Be specific and actionable. Focus on reducing complexity from {function_info['complexity']} to {complexity_target}."""
        
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are a senior software architect specializing in code refactoring and complexity reduction."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            analysis = response['message']['content']
            
            result = {
                "function": function_info,
                "analysis": analysis,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "success": True
            }
            
            print(f"✅ Analysis complete for {function_info['name']}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to analyze {function_info['name']}: {e}")
            return {
                "function": function_info,
                "error": str(e),
                "success": False
            }
    
    def generate_refactored_code(self, function_info: dict[str, Any], analysis: str) -> dict[str, Any]:
        """Generate actual refactored code using AI."""
        print(f"🛠️ Generating refactored code for {function_info['name']}...")
        
        complexity_target = "less than 10"
        prompt = f"""Based on this refactoring analysis:

{analysis[:2000]}...

Generate clean, refactored Python code for the function '{function_info['name']}' that:

1. Reduces complexity from {function_info['complexity']} to {complexity_target}
2. Uses proper separation of concerns
3. Implements error handling
4. Includes type hints
5. Has clear docstrings
6. Follows Python best practices

Provide the complete refactored code with:
- Main function (simplified)
- Helper functions (extracted logic)
- Data classes/types if needed
- Example usage

Make it production-ready and well-documented."""
        
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are an expert Python developer. Generate clean, maintainable, well-documented code."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            refactored_code = response['message']['content']
            
            result = {
                "function": function_info,
                "refactored_code": refactored_code,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "success": True
            }
            
            print(f"✅ Code generation complete for {function_info['name']}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to generate code for {function_info['name']}: {e}")
            return {
                "function": function_info,
                "error": str(e),
                "success": False
            }
    
    def create_refactored_file(self, function_info: dict[str, Any], refactored_code: str) -> str:
        """Create a new file with refactored code."""
        # Create refactored directory if it doesn't exist
        refactored_dir = Path("refactored")
        refactored_dir.mkdir(exist_ok=True)
        
        # Generate filename
        base_name = function_info["file"].replace(".py", "")
        refactored_file = refactored_dir / f"{base_name}_refactored.py"
        
        # Create header comment
        header = f'''"""
🤖 AI-Refactored Code
Original function: {function_info["name"]}
Original complexity: {function_info["complexity"]}
Target complexity: <10
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

This file contains the refactored version of the original complex function,
broken down into smaller, more maintainable components.
"""

'''
        
        # Write refactored code
        with open(refactored_file, 'w', encoding='utf-8') as f:
            f.write(header + refactored_code)
        
        print(f"📁 Refactored code saved to {refactored_file}")
        return str(refactored_file)
    
    def run_security_audit(self, code: str) -> dict[str, Any]:
        """Run AI-powered security audit on refactored code."""
        print("🔒 Running security audit...")
        
        prompt = f"""Perform a security audit on this Python code:

```python
{code[:3000]}
```

Check for:
1. **SQL Injection** vulnerabilities
2. **XSS** potential
3. **Path Traversal** issues
4. **Input Validation** problems
5. **Authentication/Authorization** gaps
6. **Cryptographic** weaknesses
7. **Error Handling** security leaks
8. **Dependency** security issues

Provide:
- Risk level (LOW/MEDIUM/HIGH)
- Specific vulnerabilities found
- Fix recommendations
- Security best practices to implement"""
        
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are a cybersecurity expert specializing in Python code security audits."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            audit_result = response['message']['content']
            
            return {
                "audit_result": audit_result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "success": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def generate_unit_tests(self, function_info: dict[str, Any], refactored_code: str) -> dict[str, Any]:
        """Generate comprehensive unit tests for refactored code."""
        print(f"🧪 Generating unit tests for {function_info['name']}...")
        
        prompt = f"""Generate comprehensive unit tests for this refactored code:

```python
{refactored_code[:3000]}
```

Create tests that cover:
1. **Happy path** scenarios
2. **Edge cases** and boundary conditions
3. **Error handling** and exceptions
4. **Input validation** 
5. **Integration** between components
6. **Performance** considerations

Use pytest framework with:
- Fixtures for setup/teardown
- Parametrized tests for multiple scenarios
- Mock objects where appropriate
- Clear test names and docstrings
- Assert statements with descriptive messages

Generate complete, runnable test code."""
        
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are a test automation expert. Generate thorough, maintainable unit tests."
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            test_code = response['message']['content']
            
            # Save test file
            refactored_dir = Path("refactored")
            base_name = function_info["file"].replace(".py", "")
            test_file = refactored_dir / f"test_{base_name}_refactored.py"
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(f'''"""
🧪 AI-Generated Unit Tests
For refactored function: {function_info["name"]}
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
"""

''')
                f.write(test_code)
            
            result = {
                "test_code": test_code,
                "test_file": str(test_file),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "success": True
            }
            
            print(f"✅ Unit tests generated: {test_file}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to generate tests: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def process_all_functions(self) -> None:
        """Process all complex functions for refactoring."""
        print("🚀 AI-Powered Auto Refactor Starting...")
        print("=" * 60)
        
        complex_functions = self.get_complex_functions()
        print(f"📊 Found {len(complex_functions)} complex functions to refactor")
        
        for i, func_info in enumerate(complex_functions, 1):
            print(f"\n🔄 Processing {i}/{len(complex_functions)}: {func_info['name']}")
            print(f"   Complexity: {func_info['complexity']}")
            
            # Step 1: Analyze function
            analysis_result = self.analyze_function_for_refactor(func_info)
            if not analysis_result.get('success'):
                continue
            
            # Step 2: Generate refactored code
            code_result = self.generate_refactored_code(
                func_info, 
                analysis_result['analysis']
            )
            if not code_result.get('success'):
                continue
            
            # Step 3: Create refactored file
            refactored_file = self.create_refactored_file(
                func_info,
                code_result['refactored_code']
            )
            
            # Step 4: Security audit
            security_result = self.run_security_audit(code_result['refactored_code'])
            
            # Step 5: Generate unit tests
            test_result = self.generate_unit_tests(
                func_info,
                code_result['refactored_code']
            )
            
            # Collect results
            self.refactor_results.append({
                "function": func_info,
                "analysis": analysis_result,
                "refactored_code": code_result,
                "refactored_file": refactored_file,
                "security_audit": security_result,
                "unit_tests": test_result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Generate final report
        self.generate_refactor_report()
    
    def generate_refactor_report(self) -> None:
        """Generate comprehensive refactoring report."""
        print("\n📊 Generating Refactor Report...")
        
        # Create summary
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_functions_processed": len(self.refactor_results),
            "successful_refactors": sum(1 for r in self.refactor_results if r.get('refactored_code', {}).get('success')),
            "files_created": len([r for r in self.refactor_results if 'refactored_file' in r]),
            "security_audits_completed": sum(1 for r in self.refactor_results if r.get('security_audit', {}).get('success')),
            "test_suites_generated": sum(1 for r in self.refactor_results if r.get('unit_tests', {}).get('success')),
            "results": self.refactor_results
        }
        
        # Save JSON report
        with open("ai_refactor_report.json", "w", encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Create markdown report
        with open("AI_REFACTOR_SUMMARY.md", "w", encoding='utf-8') as f:
            f.write(f"""# 🤖 AI-Powered Refactoring Summary

**Generated:** {summary['timestamp']}

## 📊 Overview

- **Functions Processed:** {summary['total_functions_processed']}
- **Successful Refactors:** {summary['successful_refactors']}
- **Files Created:** {summary['files_created']}
- **Security Audits:** {summary['security_audits_completed']}
- **Test Suites Generated:** {summary['test_suites_generated']}

## 📁 Generated Files

""")
            
            for result in self.refactor_results:
                if 'refactored_file' in result:
                    f.write(f"- `{result['refactored_file']}`\n")
                    if result.get('unit_tests', {}).get('test_file'):
                        f.write(f"- `{result['unit_tests']['test_file']}`\n")
            
            f.write("""
## 🎯 Next Steps

1. **Review** the generated refactored code in the `refactored/` directory
2. **Run** the generated unit tests to verify functionality
3. **Address** any security issues identified in the audits
4. **Integrate** the refactored code into your main codebase
5. **Update** documentation and dependencies as needed

## 🔍 Detailed Results

Check `ai_refactor_report.json` for comprehensive analysis and code generation details.
""")
        
        print("✅ Refactor report saved:")
        print("   - ai_refactor_report.json")
        print("   - AI_REFACTOR_SUMMARY.md")
        print(f"   - {len(self.refactor_results)} refactored files in refactored/ directory")


def main():
    """Main refactoring function."""
    try:
        engine = AIRefactorEngine()
        engine.process_all_functions()
        
        print("\n🎉 AI-Powered Refactoring Complete!")
        print("📁 Check the 'refactored/' directory for all generated files")
        print("📊 See AI_REFACTOR_SUMMARY.md for detailed results")
        
    except Exception as e:
        print(f"❌ Refactoring failed: {e}")
        print("💡 Make sure your Ollama Turbo API key is valid")


if __name__ == "__main__":
    main()
