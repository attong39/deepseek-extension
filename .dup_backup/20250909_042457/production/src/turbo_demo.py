#!/usr/bin/env python3
"""
🚀 Ollama Turbo Demo for Optimized Project
Test datacenter-grade AI acceleration with the optimized codebase
"""

import json
import sys
import time
from pathlib import Path
from typing import Any
import Exception
import ImportError
import abs
import all
import dict
import e
import f
import k
import len
import min
import model
import open
import part
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


class TurboDemo:
    """Demo showcasing Ollama Turbo capabilities."""
    
    def __init__(self):
        self.config = self._load_config()
        self.client = self._init_client()
        self.demo_results = []
        
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
    
    def test_basic_connection(self) -> dict[str, Any]:
        """Test basic Turbo connection."""
        print("🔗 Testing Ollama Turbo Connection...")
        
        start_time = time.time()
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "user", 
                    "content": "Hello! Confirm Turbo is working with a brief response."
                }]
            )
            
            response_time = time.time() - start_time
            content = response['message']['content']
            
            result = {
                "test": "basic_connection",
                "success": True,
                "response_time": response_time,
                "model": self.config["model"],
                "content": content,
                "tokens": len(content.split())
            }
            
            print(f"✅ SUCCESS: {response_time:.2f}s")
            print(f"🤖 Response: {content}")
            
        except Exception as e:
            result = {
                "test": "basic_connection",
                "success": False,
                "error": str(e)
            }
            print(f"❌ FAILED: {e}")
        
        self.demo_results.append(result)
        return result
    
    def test_code_analysis(self) -> dict[str, Any]:
        """Test AI code analysis with Turbo."""
        print("\n🔍 Testing AI Code Analysis...")
        
        # Read optimized scanner code
        scanner_file = Path("ai_project_scanner.py")
        if scanner_file.exists():
            with open(scanner_file, encoding='utf-8') as f:
                code_sample = f.read()[:1500]  # First 1500 chars
        else:
            code_sample = """
def example_function(data):
    results = []
    for item in data:
        if item > 0:
            results.append(item * 2)
    return results
"""
        
        start_time = time.time()
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are an expert code reviewer. Analyze code for performance, security, and quality issues."
                }, {
                    "role": "user",
                    "content": f"Analyze this Python code:\n\n```python\n{code_sample}\n```\n\nProvide specific improvement suggestions."
                }]
            )
            
            response_time = time.time() - start_time
            content = response['message']['content']
            
            result = {
                "test": "code_analysis",
                "success": True,
                "response_time": response_time,
                "analysis_length": len(content),
                "code_analyzed": len(code_sample),
                "suggestions": content[:500] + "..." if len(content) > 500 else content
            }
            
            print(f"✅ SUCCESS: {response_time:.2f}s")
            print(f"📊 Analysis: {len(content)} chars")
            print(f"💡 Preview: {content[:200]}...")
            
        except Exception as e:
            result = {
                "test": "code_analysis",
                "success": False,
                "error": str(e)
            }
            print(f"❌ FAILED: {e}")
        
        self.demo_results.append(result)
        return result
    
    def test_refactor_suggestions(self) -> dict[str, Any]:
        """Test AI refactoring suggestions."""
        print("\n🔧 Testing Refactor Suggestions...")
        
        # Use one of the complex functions from our analysis
        complex_function_info = {
            "name": "validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html",
            "complexity": 352,
            "file": "setuptools validation module"
        }
        
        start_time = time.time()
        try:
            response = self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "system",
                    "content": "You are a senior software architect specializing in refactoring complex code."
                }, {
                    "role": "user",
                    "content": f"""I have a function '{complex_function_info['name']}' with complexity score {complex_function_info['complexity']}. 

This function appears to be handling HTTPS validation for setuptools project configuration.

Please provide:
1. Specific refactoring strategies
2. Design patterns to apply  
3. How to break it into smaller functions
4. Expected benefits

Keep suggestions practical and actionable."""
                }]
            )
            
            response_time = time.time() - start_time
            content = response['message']['content']
            
            result = {
                "test": "refactor_suggestions",
                "success": True,
                "response_time": response_time,
                "function_complexity": complex_function_info['complexity'],
                "suggestions": content,
                "suggestion_length": len(content)
            }
            
            print(f"✅ SUCCESS: {response_time:.2f}s")
            print(f"🎯 Complexity: {complex_function_info['complexity']}")
            print(f"📝 Suggestions: {len(content)} chars")
            print(f"💡 Preview: {content[:300]}...")
            
        except Exception as e:
            result = {
                "test": "refactor_suggestions", 
                "success": False,
                "error": str(e)
            }
            print(f"❌ FAILED: {e}")
        
        self.demo_results.append(result)
        return result
    
    def test_performance_comparison(self) -> dict[str, Any]:
        """Compare gpt-oss:20b vs gpt-oss:120b performance."""
        print("\n⚡ Testing Model Performance Comparison...")
        
        test_prompt = "Explain the benefits of AI-driven code optimization in 100 words."
        models = ["gpt-oss:20b", "gpt-oss:120b"]
        results = {}
        
        for model in models:
            print(f"\n🧪 Testing {model}...")
            start_time = time.time()
            
            try:
                response = self.client.chat(
                    model,
                    messages=[{
                        "role": "user",
                        "content": test_prompt
                    }]
                )
                
                response_time = time.time() - start_time
                content = response['message']['content']
                
                results[model] = {
                    "success": True,
                    "response_time": response_time,
                    "content_length": len(content),
                    "tokens": len(content.split()),
                    "tokens_per_second": len(content.split()) / response_time
                }
                
                print(f"✅ {model}: {response_time:.2f}s, {len(content.split())} tokens")
                
            except Exception as e:
                results[model] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ {model}: {e}")
        
        # Calculate comparison
        comparison = {}
        if all(r.get('success') for r in results.values()):
            fast_model = min(results.keys(), key=lambda k: results[k]['response_time'])
            comparison = {
                "faster_model": fast_model,
                "speed_difference": abs(results['gpt-oss:20b']['response_time'] - 
                                     results['gpt-oss:120b']['response_time']),
                "quality_vs_speed": "gpt-oss:120b typically provides higher quality responses"
            }
        
        result = {
            "test": "performance_comparison",
            "results": results,
            "comparison": comparison
        }
        
        self.demo_results.append(result)
        return result
    
    def test_streaming_response(self) -> dict[str, Any]:
        """Test streaming response capability."""
        print("\n🌊 Testing Streaming Response...")
        
        start_time = time.time()
        try:
            print("🤖 Streaming response:")
            
            full_response = ""
            chunk_count = 0
            
            for part in self.client.chat(
                self.config["model"],
                messages=[{
                    "role": "user",
                    "content": "Explain the key benefits of our AI-optimized project in 3 bullet points. Be concise and technical."
                }],
                stream=True
            ):
                chunk = part['message']['content']
                full_response += chunk
                chunk_count += 1
                print(chunk, end='', flush=True)
            
            response_time = time.time() - start_time
            
            result = {
                "test": "streaming_response",
                "success": True,
                "response_time": response_time,
                "total_chunks": chunk_count,
                "full_response": full_response,
                "avg_chunk_time": response_time / chunk_count if chunk_count > 0 else 0
            }
            
            print(f"\n✅ Streaming complete: {response_time:.2f}s, {chunk_count} chunks")
            
        except Exception as e:
            result = {
                "test": "streaming_response",
                "success": False,
                "error": str(e)
            }
            print(f"\n❌ FAILED: {e}")
        
        self.demo_results.append(result)
        return result
    
    def generate_test_report(self) -> None:
        """Generate comprehensive test report."""
        print("\n📊 Generating Test Report...")
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": self.config,
            "results": self.demo_results,
            "summary": {
                "total_tests": len(self.demo_results),
                "successful_tests": sum(1 for r in self.demo_results if r.get('success', False)),
                "total_response_time": sum(r.get('response_time', 0) for r in self.demo_results if 'response_time' in r),
                "average_response_time": 0
            }
        }
        
        if report["summary"]["successful_tests"] > 0:
            response_times = [r['response_time'] for r in self.demo_results if r.get('success') and 'response_time' in r]
            report["summary"]["average_response_time"] = sum(response_times) / len(response_times)
        
        # Save report
        with open("turbo_demo_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("✅ Report saved to turbo_demo_report.json")
        print("📊 Summary:")
        print(f"   - Tests: {report['summary']['successful_tests']}/{report['summary']['total_tests']} successful")
        print(f"   - Avg Response Time: {report['summary']['average_response_time']:.2f}s")
        print(f"   - Total Time: {report['summary']['total_response_time']:.2f}s")
        
        return report
    
    def run_full_demo(self) -> None:
        """Run complete Turbo demo."""
        print("🚀 Ollama Turbo Demo - Optimized Project Integration")
        print("=" * 60)
        print(f"🔧 Using model: {self.config['model']}")
        print(f"🌐 Host: {self.config['host']}")
        
        # Run all tests
        self.test_basic_connection()
        self.test_code_analysis()
        self.test_refactor_suggestions()
        self.test_performance_comparison()
        self.test_streaming_response()
        
        # Generate report
        report = self.generate_test_report()
        
        print("\n🎉 Demo Complete!")
        print("🔍 Check turbo_demo_report.json for detailed results")
        
        # Final recommendations
        print("\n💡 Next Steps:")
        print("   1. Review the code analysis suggestions")
        print("   2. Implement the refactoring recommendations")
        print("   3. Use Turbo for ongoing code optimization")
        print("   4. Monitor performance with different models")


def main():
    """Main demo function."""
    try:
        demo = TurboDemo()
        demo.run_full_demo()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Make sure your API key is valid and you have internet connection")


if __name__ == "__main__":
    main()
