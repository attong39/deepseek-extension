#!/usr/bin/env python3
"""
Ollama Turbo Integration for Optimized Project
Integrate datacenter-grade AI acceleration with the optimized codebase.
"""

import os
import json
import asyncio
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
import subprocess
import sys

try:
    from ollama import Client
    import httpx
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'ollama', 'httpx'], check=True)
    from ollama import Client
    import httpx


@dataclass
class TurboConfig:
    """Configuration for Ollama Turbo integration."""
    host: str = "https://ollama.com"
    api_key: str = ""
    model: str = "gpt-oss:120b"  # Default to most powerful model
    local_fallback: bool = True
    timeout: int = 30


@dataclass
class TurboResponse:
    """Response from Turbo API."""
    content: str
    model: str
    tokens_used: int
    response_time: float
    is_turbo: bool
    error: Optional[str] = None


class OllamaTurboIntegration:
    """Enhanced Ollama integration with Turbo acceleration."""
    
    def __init__(self, config: Optional[TurboConfig] = None):
        self.config = config or self._load_config()
        self.turbo_client = None
        self.local_client = None
        self._initialize_clients()
        
    def _load_config(self) -> TurboConfig:
        """Load configuration from environment and config files."""
        config_file = Path("ollama_turbo_config.json")
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                return TurboConfig(**config_data)
        
        # Load from environment
        return TurboConfig(
            api_key=os.getenv("OLLAMA_API_KEY", ""),
            model=os.getenv("OLLAMA_TURBO_MODEL", "gpt-oss:120b"),
            local_fallback=os.getenv("OLLAMA_LOCAL_FALLBACK", "true").lower() == "true"
        )
    
    def _initialize_clients(self) -> None:
        """Initialize Turbo and local clients."""
        # Initialize Turbo client
        if self.config.api_key:
            try:
                self.turbo_client = Client(
                    host=self.config.host,
                    headers={'Authorization': f'Bearer {self.config.api_key}'}
                )
                print("✅ Ollama Turbo client initialized successfully")
            except Exception as e:
                print(f"⚠️ Failed to initialize Turbo client: {e}")
        
        # Initialize local fallback client
        if self.config.local_fallback:
            try:
                self.local_client = Client(host='http://localhost:11434')
                print("✅ Local Ollama client initialized as fallback")
            except Exception as e:
                print(f"⚠️ Local Ollama client not available: {e}")
    
    async def chat_turbo(self, prompt: str, system_prompt: str = "", stream: bool = False) -> TurboResponse:
        """Enhanced chat with Turbo acceleration."""
        start_time = time.time()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Try Turbo first
        if self.turbo_client:
            try:
                response_content = ""
                token_count = 0
                
                if stream:
                    print("🚀 Using Ollama Turbo (streaming)...")
                    for part in self.turbo_client.chat(
                        self.config.model, 
                        messages=messages, 
                        stream=True
                    ):
                        chunk = part['message']['content']
                        response_content += chunk
                        token_count += 1
                        print(chunk, end='', flush=True)
                else:
                    print("🚀 Using Ollama Turbo...")
                    response = self.turbo_client.chat(
                        self.config.model, 
                        messages=messages
                    )
                    response_content = response['message']['content']
                    token_count = len(response_content.split())
                
                response_time = time.time() - start_time
                return TurboResponse(
                    content=response_content,
                    model=self.config.model,
                    tokens_used=token_count,
                    response_time=response_time,
                    is_turbo=True
                )
                
            except Exception as e:
                print(f"\n⚠️ Turbo failed: {e}")
                
        # Fallback to local
        if self.local_client and self.config.local_fallback:
            try:
                print("🔄 Falling back to local Ollama...")
                response = self.local_client.chat(
                    'llama3.1:8b',  # Use available local model
                    messages=messages
                )
                response_time = time.time() - start_time
                return TurboResponse(
                    content=response['message']['content'],
                    model='llama3.1:8b',
                    tokens_used=len(response['message']['content'].split()),
                    response_time=response_time,
                    is_turbo=False
                )
            except Exception as e:
                error_msg = f"Both Turbo and local failed: {e}"
                return TurboResponse(
                    content="",
                    model="error",
                    tokens_used=0,
                    response_time=time.time() - start_time,
                    is_turbo=False,
                    error=error_msg
                )
        
        return TurboResponse(
            content="",
            model="error",
            tokens_used=0,
            response_time=time.time() - start_time,
            is_turbo=False,
            error="No available clients"
        )
    
    def setup_turbo_account(self) -> None:
        """Guide user through Turbo setup."""
        print("\n🚀 Ollama Turbo Setup Guide")
        print("=" * 50)
        print("1. Sign up for Ollama account at: https://ollama.com")
        print("2. Create API key at: https://ollama.com/settings/keys")
        print("3. Add your key to environment or config file")
        print("\nEnvironment setup:")
        print("export OLLAMA_api_key = os.getenv("API_KEY")")
        print("\nOr create ollama_turbo_config.json:")
        
        config_example = {
            "api_key": "your-api-key-here",
            "model": "gpt-oss:120b",
            "host": "https://ollama.com",
            "local_fallback": True
        }
        
        print(json.dumps(config_example, indent=2))
        
        # Save example config
        with open("ollama_turbo_config.example.json", "w") as f:
            json.dump(config_example, f, indent=2)
        
        print("\n✅ Example config saved to ollama_turbo_config.example.json")
    
    def benchmark_turbo_vs_local(self, test_prompt: str = "Explain quantum computing in 100 words") -> Dict[str, Any]:
        """Benchmark Turbo vs local performance."""
        print("\n🏃‍♂️ Benchmarking Turbo vs Local Performance")
        print("=" * 50)
        
        results = {
            "test_prompt": test_prompt,
            "turbo_result": None,
            "local_result": None,
            "comparison": {}
        }
        
        # Test Turbo
        if self.turbo_client:
            print("Testing Turbo...")
            turbo_response = asyncio.run(self.chat_turbo(test_prompt))
            results["turbo_result"] = asdict(turbo_response)
            print(f"Turbo: {turbo_response.response_time:.2f}s")
        
        # Test Local
        if self.local_client:
            print("Testing Local...")
            start_time = time.time()
            try:
                response = self.local_client.chat('llama3.1:8b', messages=[
                    {"role": "user", "content": test_prompt}
                ])
                local_time = time.time() - start_time
                results["local_result"] = {
                    "response_time": local_time,
                    "model": "llama3.1:8b",
                    "content_length": len(response['message']['content'])
                }
                print(f"Local: {local_time:.2f}s")
            except Exception as e:
                print(f"Local test failed: {e}")
        
        # Calculate comparison
        if results["turbo_result"] and results["local_result"]:
            turbo_time = results["turbo_result"]["response_time"]
            local_time = results["local_result"]["response_time"]
            speedup = local_time / turbo_time if turbo_time > 0 else 0
            
            results["comparison"] = {
                "turbo_faster": turbo_time < local_time,
                "speedup_factor": speedup,
                "time_difference": abs(turbo_time - local_time)
            }
            
            print(f"\n📊 Results:")
            print(f"Turbo is {'faster' if turbo_time < local_time else 'slower'}")
            print(f"Speedup: {speedup:.2f}x")
        
        # Save results
        with open("turbo_benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results


class ProjectAIIntegration:
    """Integrate Ollama Turbo with optimized project features."""
    
    def __init__(self):
        self.turbo = OllamaTurboIntegration()
        self.project_root = Path(".")
        
    async def ai_code_review(self, file_path: str) -> str:
        """AI-powered code review using Turbo."""
        if not Path(file_path).exists():
            return "File not found"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        system_prompt = """You are an expert code reviewer. Analyze the code for:
1. Security issues
2. Performance problems  
3. Code quality improvements
4. Best practices violations
Provide specific, actionable feedback."""
        
        prompt = f"Review this code:\n\n```python\n{code[:2000]}...\n```"
        
        response = await self.turbo.chat_turbo(prompt, system_prompt)
        return response.content
    
    async def ai_refactor_suggestion(self, function_name: str, complexity: int) -> str:
        """Generate refactoring suggestions for complex functions."""
        system_prompt = f"""You are a refactoring expert. For a function with complexity {complexity}, provide:
1. Specific refactoring strategies
2. Design patterns to apply
3. Step-by-step refactor plan
4. Expected benefits"""
        
        prompt = f"Function '{function_name}' has complexity {complexity}. How should I refactor it?"
        
        response = await self.turbo.chat_turbo(prompt, system_prompt)
        return response.content
    
    async def ai_test_generation(self, code_snippet: str) -> str:
        """Generate comprehensive tests for code."""
        system_prompt = """Generate comprehensive pytest test cases including:
1. Unit tests for all functions
2. Edge cases and error handling
3. Mock usage where appropriate
4. Performance tests if relevant"""
        
        prompt = f"Generate tests for:\n\n```python\n{code_snippet}\n```"
        
        response = await self.turbo.chat_turbo(prompt, system_prompt)
        return response.content
    
    async def ai_documentation_generation(self, code_snippet: str) -> str:
        """Generate documentation for code."""
        system_prompt = """Generate comprehensive documentation including:
1. Module/class/function docstrings
2. Type hints
3. Usage examples
4. API documentation"""
        
        prompt = f"Generate documentation for:\n\n```python\n{code_snippet}\n```"
        
        response = await self.turbo.chat_turbo(prompt, system_prompt)
        return response.content


async def main():
    """Main function demonstrating Turbo integration."""
    print("🚀 Ollama Turbo Integration for Optimized Project")
    print("=" * 60)
    
    # Initialize integration
    integration = ProjectAIIntegration()
    
    # Check if API key is configured
    if not integration.turbo.config.api_key:
        print("⚠️ No API key configured. Setting up guide...")
        integration.turbo.setup_turbo_account()
        return
    
    # Run benchmark
    print("\n1. Running Turbo vs Local benchmark...")
    await integration.turbo.benchmark_turbo_vs_local()
    
    # Example AI code review
    print("\n2. AI Code Review Example...")
    if Path("ai_project_scanner.py").exists():
        review = await integration.ai_code_review("ai_project_scanner.py")
        print(f"Code Review:\n{review[:500]}...")
    
    # Example refactor suggestion
    print("\n3. AI Refactor Suggestion...")
    refactor_suggestion = await integration.ai_refactor_suggestion(
        "validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html", 
        352
    )
    print(f"Refactor Suggestion:\n{refactor_suggestion[:500]}...")
    
    print("\n✅ Ollama Turbo integration complete!")
    print("📊 Check turbo_benchmark_results.json for performance data")


if __name__ == "__main__":
    asyncio.run(main())