#!/usr/bin/env python3
"""
Enterprise Turbo Upgrade Test Suite
Tests the new cache, lint-fix, and automation features
"""

import json
import subprocess
import time
from pathlib import Path
import Exception
import all
import any
import cmd
import cwd
import dict
import e
import f
import len
import open
import print
import r
import self
import str
import target

class TurboTestSuite:
    def __init__(self):
        self.workspace = Path("e:\\zeta-monorepo")
        self.results = {}
        self.start_time = time.time()

    def run_command(self, cmd: str, cwd: Path = None) -> dict[str, any]:
        """Run a command and return results"""
        try:
            start = time.time()
            result = subprocess.run(
                cmd, shell=True, cwd=cwd or self.workspace,
                capture_output=True, text=True, timeout=300
            )
            duration = time.time() - start

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "duration": duration,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out", "duration": 300}
        except Exception as e:
            return {"success": False, "error": str(e), "duration": 0}

    def test_cache_system(self) -> dict[str, any]:
        """Test the new caching system"""
        print("🧪 Testing cache system...")

        # Test cache creation
        cache_result = self.run_command("uv run python tools/auto_fix/cli.py all --dry-run --use-cache")
        cache_file = self.workspace / "tools/auto_fix/.cache/auto_fix_cache.json"

        cache_exists = cache_file.exists()
        cache_size = cache_file.stat().st_size if cache_exists else 0

        # Test cache persistence
        cache_content = {}
        if cache_exists:
            try:
                with open(cache_file) as f:
                    cache_content = json.load(f)
            except Exception:
                pass

        return {
            "cache_created": cache_exists,
            "cache_size": cache_size,
            "cache_entries": len(cache_content),
            "command_success": cache_result["success"],
            "duration": cache_result["duration"]
        }

    def test_lint_fix_integration(self) -> dict[str, any]:
        """Test lint-fix integration"""
        print("🧪 Testing lint-fix integration...")

        # Create a test file with lint issues
        test_file = self.workspace / "test_lint_fix.py"
        test_content = '''
import os,sys,json  # Multiple imports on one line
def test_func( ):
    x=1+2  # No spaces around operator
    return x
'''

        with open(test_file, 'w') as f:
            f.write(test_content)

        # Run lint-fix
        lint_result = self.run_command("uv run python tools/auto_fix/cli.py test_lint_fix.py --lint-fix")

        # Check if file was fixed
        fixed_content = ""
        if test_file.exists():
            with open(test_file) as f:
                fixed_content = f.read()

        # Clean up
        test_file.unlink(missing_ok=True)

        return {
            "command_success": lint_result["success"],
            "file_was_modified": fixed_content != test_content,
            "duration": lint_result["duration"],
            "original_content": test_content.strip(),
            "fixed_content": fixed_content.strip()
        }

    def test_makefile_targets(self) -> dict[str, any]:
        """Test new Makefile targets"""
        print("🧪 Testing Makefile targets...")

        targets = ["fix-imports", "fast-fix", "lint-fix", "cleanup"]
        results = {}

        for target in targets:
            print(f"  Testing make {target}...")
            result = self.run_command(f"make {target}")
            results[target] = {
                "success": result["success"],
                "duration": result["duration"],
                "has_output": len(result["stdout"]) > 0
            }

        return results

    def test_performance_improvement(self) -> dict[str, any]:
        """Test performance improvement with cache"""
        print("🧪 Testing performance improvement...")

        # First run (should create cache)
        start1 = time.time()
        self.run_command("uv run python tools/auto_fix/cli.py all --dry-run --use-cache")
        duration1 = time.time() - start1

        # Second run (should use cache)
        start2 = time.time()
        self.run_command("uv run python tools/auto_fix/cli.py all --dry-run --use-cache")
        duration2 = time.time() - start2

        improvement = duration1 - duration2 if duration2 < duration1 else 0
        improvement_pct = (improvement / duration1 * 100) if duration1 > 0 else 0

        return {
            "first_run_duration": duration1,
            "second_run_duration": duration2,
            "improvement_seconds": improvement,
            "improvement_percent": improvement_pct,
            "cache_working": improvement > 0
        }

    def generate_report(self) -> str:
        """Generate test report"""
        duration = time.time() - self.start_time

        report = f"""
# 🚀 Enterprise Turbo Upgrade Test Report

**Test Duration:** {duration:.2f} seconds
**Test Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Test Results

### Cache System
- ✅ Cache Created: {self.results.get('cache', {}).get('cache_created', False)}
- 📏 Cache Size: {self.results.get('cache', {}).get('cache_size', 0)} bytes
- 📝 Cache Entries: {self.results.get('cache', {}).get('cache_entries', 0)}
- ⏱️ Duration: {self.results.get('cache', {}).get('duration', 0):.2f}s

### Lint-Fix Integration
- ✅ Command Success: {self.results.get('lint_fix', {}).get('command_success', False)}
- 🔧 File Modified: {self.results.get('lint_fix', {}).get('file_was_modified', False)}
- ⏱️ Duration: {self.results.get('lint_fix', {}).get('duration', 0):.2f}s

### Performance Improvement
- 🏃‍♂️ First Run: {self.results.get('performance', {}).get('first_run_duration', 0):.2f}s
- 🏃‍♂️ Second Run: {self.results.get('performance', {}).get('second_run_duration', 0):.2f}s
- 📈 Improvement: {self.results.get('performance', {}).get('improvement_seconds', 0):.2f}s\n"
f"- 📊 Improvement %: {self.results.get('performance', {}).get('improvement_percent', 0):.1f}%\n"

### Makefile Targets
"""

        makefile_results = self.results.get('makefile', {})
        for target, result in makefile_results.items():
            status = "✅" if result["success"] else "❌"
            report += f"- {status} {target}: {result['duration']:.2f}s\n"

        report += """
## 🎯 Summary

"""

        all_passed = all([
            self.results.get('cache', {}).get('cache_created', False),
            self.results.get('lint_fix', {}).get('command_success', False),
            self.results.get('performance', {}).get('cache_working', False),
            all(r["success"] for r in self.results.get('makefile', {}).values())
        ])

        if all_passed:
            report += "🎉 **All tests passed! Enterprise Turbo upgrade is working correctly.**"
        else:
            report += "⚠️ **Some tests failed. Please check the results above.**"

        return report

    def run_all_tests(self) -> dict[str, any]:
        """Run all tests"""
        print("🚀 Starting Enterprise Turbo Upgrade Test Suite")
        print("=" * 50)

        self.results = {
            "cache": self.test_cache_system(),
            "lint_fix": self.test_lint_fix_integration(),
            "makefile": self.test_makefile_targets(),
            "performance": self.test_performance_improvement()
        }

        print("\n" + "=" * 50)
        print("📋 Test Report:")
        print(self.generate_report())

        return self.results

if __name__ == "__main__":
    tester = TurboTestSuite()
    results = tester.run_all_tests()

    # Save detailed results
    with open("turbo_upgrade_test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save report
    with open("TURBO_UPGRADE_TEST_REPORT.md", "w") as f:
        f.write(tester.generate_report())

    print("\n📁 Results saved to:")
    print("  - turbo_upgrade_test_results.json")
    print("  - TURBO_UPGRADE_TEST_REPORT.md")
