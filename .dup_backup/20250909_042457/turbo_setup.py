#!/usr/bin/env python3
"""
Ollama Turbo Setup & Configuration Tool
Easy setup for datacenter-grade AI acceleration
"""

import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any
import Exception
import FileNotFoundError
import dict
import e
import f
import input
import key
import len
import model
import open
import print
import prompt
import self
import str


class TurboSetupWizard:
    """Interactive setup wizard for Ollama Turbo."""
    
    def __init__(self):
        self.config = {}
        self.platform = platform.system().lower()
        
    def run_setup(self) -> None:
        """Run the complete setup process."""
        print("🚀 Ollama Turbo Setup Wizard")
        print("=" * 50)
        
        # Step 1: Check Ollama installation
        self._check_ollama_installation()
        
        # Step 2: Account setup
        self._setup_account()
        
        # Step 3: API key configuration
        self._configure_api_key()
        
        # Step 4: Model selection
        self._select_models()
        
        # Step 5: Save configuration
        self._save_configuration()
        
        # Step 6: Test connection
        self._test_connection()
        
        print("\n✅ Ollama Turbo setup complete!")
        print("🎯 Ready to use datacenter-grade AI acceleration!")
    
    def _check_ollama_installation(self) -> None:
        """Check if Ollama is installed."""
        print("\n1. Checking Ollama installation...")
        
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Ollama installed: {result.stdout.strip()}")
            else:
                print("❌ Ollama not found")
                self._install_ollama()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Ollama not found")
            self._install_ollama()
    
    def _install_ollama(self) -> None:
        """Guide user to install Ollama."""
        print("\n📥 Installing Ollama...")
        
        if self.platform == "windows":
            print("Windows detected. Please:")
            print("1. Visit https://ollama.com/download")
            print("2. Download and run the Windows installer")
            print("3. Restart this script after installation")
        elif self.platform == "darwin":  # macOS
            print("macOS detected. Installing via curl...")
            try:
                subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh', '|', 'sh'], 
                             shell=True, check=True)
                print("✅ Ollama installed successfully")
            except subprocess.CalledProcessError:
                print("❌ Installation failed. Please visit https://ollama.com/download")
        else:  # Linux
            print("Linux detected. Installing via curl...")
            try:
                subprocess.run(['curl', '-fsSL', 'https://ollama.com/install.sh', '|', 'sh'], 
                             shell=True, check=True)
                print("✅ Ollama installed successfully")
            except subprocess.CalledProcessError:
                print("❌ Installation failed. Please visit https://ollama.com/download")
    
    def _setup_account(self) -> None:
        """Guide user through account setup."""
        print("\n2. Account Setup")
        print("To use Ollama Turbo, you need an account:")
        print("🌐 Visit: https://ollama.com")
        print("📝 Sign up for a free account")
        
        input("Press Enter after creating your account...")
    
    def _configure_api_key(self) -> None:
        """Configure API key."""
        print("\n3. API Key Configuration")
        print("🔑 Create an API key:")
        print("   1. Visit: https://ollama.com/settings/keys")
        print("   2. Click 'Create new key'")
        print("   3. Copy the generated key")
        
        while True:
            api_key = input("\nPaste your API key here: ").strip()
            if api_key:
                self.config['api_key'] = api_key
                break
            print("❌ Please enter a valid API key")
    
    def _select_models(self) -> None:
        """Select Turbo models to use."""
        print("\n4. Model Selection")
        print("Available Turbo models:")
        
        models = {
            "1": {"name": "gpt-oss:20b", "description": "Fast, efficient model"},
            "2": {"name": "gpt-oss:120b", "description": "Most powerful model"},
            "3": {"name": "both", "description": "Configure both models"}
        }
        
        for key, model in models.items():
            print(f"   {key}. {model['name']} - {model['description']}")
        
        while True:
            choice = input("\nSelect model (1-3): ").strip()
            if choice in models:
                if choice == "3":
                    self.config['models'] = ["gpt-oss:20b", "gpt-oss:120b"]
                    self.config['default_model'] = "gpt-oss:120b"
                else:
                    model_name = models[choice]['name']
                    self.config['models'] = [model_name]
                    self.config['default_model'] = model_name
                break
            print("❌ Please select 1, 2, or 3")
    
    def _save_configuration(self) -> None:
        """Save configuration to file."""
        print("\n5. Saving Configuration...")
        
        full_config = {
            "api_key": self.config['api_key'],
            "host": "https://ollama.com",
            "model": self.config['default_model'],
            "available_models": self.config['models'],
            "local_fallback": True,
            "timeout": 30,
            "max_retries": 3
        }
        
        # Save to JSON file
        config_file = Path("ollama_turbo_config.json")
        with open(config_file, 'w') as f:
            json.dump(full_config, f, indent=2)
        
        # Set environment variable
        env_file = Path(".env")
        env_content = f"OLLAMA_API_KEY={self.config['api_key']}\n"
        env_content += f"OLLAMA_TURBO_MODEL={self.config['default_model']}\n"
        
        if env_file.exists():
            with open(env_file) as f:
                existing = f.read()
            if "OLLAMA_API_KEY" not in existing:
                with open(env_file, 'a') as f:
                    f.write("\n" + env_content)
        else:
            with open(env_file, 'w') as f:
                f.write(env_content)
        
        print(f"✅ Configuration saved to {config_file}")
        print("✅ Environment variables added to .env")
    
    def _test_connection(self) -> None:
        """Test Turbo connection."""
        print("\n6. Testing Connection...")
        
        try:
            # Import and test
            from ollama import Client
            
            client = Client(
                host="https://ollama.com",
                headers={'Authorization': f'Bearer {self.config["api_key"]}'}
            )
            
            # Simple test
            response = client.chat(
                self.config['default_model'],
                messages=[{"role": "user", "content": "Hello, Turbo!"}]
            )
            
            print("✅ Turbo connection successful!")
            print(f"🤖 Response: {response['message']['content'][:100]}...")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("Please check your API key and try again")


class TurboManager:
    """Manage Turbo models and performance."""
    
    def __init__(self):
        self.config_file = Path("ollama_turbo_config.json")
        self.load_config()
    
    def load_config(self) -> None:
        """Load existing configuration."""
        if self.config_file.exists():
            with open(self.config_file) as f:
                self.config = json.load(f)
        else:
            print("❌ No configuration found. Run setup first.")
            sys.exit(1)
    
    def list_available_models(self) -> None:
        """List available Turbo models."""
        print("🤖 Available Turbo Models:")
        print("=" * 30)
        
        turbo_models = [
            {
                "name": "gpt-oss:20b",
                "size": "20B parameters",
                "description": "Fast and efficient for most tasks",
                "use_cases": ["Code generation", "Quick analysis", "Chatbots"]
            },
            {
                "name": "gpt-oss:120b",
                "size": "120B parameters", 
                "description": "Most powerful, best quality responses",
                "use_cases": ["Complex reasoning", "Research", "Creative writing"]
            }
        ]
        
        for model in turbo_models:
            print(f"\n📋 {model['name']}")
            print(f"   Size: {model['size']}")
            print(f"   Description: {model['description']}")
            print(f"   Use cases: {', '.join(model['use_cases'])}")
    
    def benchmark_models(self) -> dict[str, Any]:
        """Benchmark different models."""
        print("🏃‍♂️ Benchmarking Turbo Models...")
        
        test_prompts = [
            "Explain quantum computing in 50 words",
            "Write a Python function to sort a list",
            "What are the benefits of AI acceleration?"
        ]
        
        results = {}
        
        try:
            from ollama import Client
            client = Client(
                host="https://ollama.com",
                headers={'Authorization': f'Bearer {self.config["api_key"]}'}
            )
            
            for model in self.config.get('available_models', [self.config['model']]):
                print(f"\nTesting {model}...")
                model_results = []
                
                for prompt in test_prompts:
                    import time
                    start_time = time.time()
                    
                    try:
                        response = client.chat(
                            model,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        
                        response_time = time.time() - start_time
                        tokens = len(response['message']['content'].split())
                        
                        model_results.append({
                            "prompt": prompt,
                            "response_time": response_time,
                            "tokens": tokens,
                            "tokens_per_second": tokens / response_time
                        })
                        
                        print(f"   ✅ {response_time:.2f}s, {tokens} tokens")
                        
                    except Exception as e:
                        print(f"   ❌ Failed: {e}")
                        model_results.append({
                            "prompt": prompt,
                            "error": str(e)
                        })
                
                results[model] = model_results
            
            # Save results
            with open("turbo_benchmark.json", 'w') as f:
                json.dump(results, f, indent=2)
            
            print("\n✅ Benchmark complete! Results saved to turbo_benchmark.json")
            
        except Exception as e:
            print(f"❌ Benchmark failed: {e}")
        
        return results
    
    def monitor_usage(self) -> None:
        """Monitor Turbo usage and costs."""
        print("📊 Turbo Usage Monitor")
        print("=" * 25)
        print("Visit https://ollama.com/settings/billing for detailed usage")
        print("💡 Tip: Use gpt-oss:20b for faster, cheaper responses")
        print("💡 Tip: Use gpt-oss:120b for complex tasks requiring quality")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("🚀 Ollama Turbo Manager")
        print("=" * 25)
        print("Usage:")
        print("  python turbo_setup.py setup     - Run setup wizard")
        print("  python turbo_setup.py models    - List available models")
        print("  python turbo_setup.py benchmark - Benchmark performance")
        print("  python turbo_setup.py monitor   - Monitor usage")
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        wizard = TurboSetupWizard()
        wizard.run_setup()
    
    elif command == "models":
        manager = TurboManager()
        manager.list_available_models()
    
    elif command == "benchmark":
        manager = TurboManager()
        manager.benchmark_models()
    
    elif command == "monitor":
        manager = TurboManager()
        manager.monitor_usage()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'setup', 'models', 'benchmark', or 'monitor'")


if __name__ == "__main__":
    main()
