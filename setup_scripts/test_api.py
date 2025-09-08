#!/usr/bin/env python3
"""
🧪 Ollama API Test Script
Standalone script to test Ollama API connection and functionality
"""

import sys
import time
import json
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("📦 Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

def test_ollama_connection(host="http://127.0.0.1:11434", timeout=10):
    """Test Ollama server connection and API functionality"""
    print(f"🔍 Testing Ollama connection to {host}...")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'host': host,
        'server_running': False,
        'models_available': [],
        'api_working': False,
        'response_time': None,
        'test_response': None,
        'error': None
    }
    
    # Test 1: Server ping
    try:
        start_time = time.time()
        response = requests.get(f"{host}/api/tags", timeout=timeout)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            results['server_running'] = True
            results['response_time'] = round(response_time, 3)
            print(f"✅ Server is running (response time: {results['response_time']}s)")
            
            # Parse models
            data = response.json()
            if 'models' in data:
                results['models_available'] = [model['name'] for model in data['models']]
                print(f"📦 Available models ({len(results['models_available'])}):") 
                for model in results['models_available']:
                    print(f"   - {model}")
            else:
                print("📭 No models found")
        else:
            results['error'] = f"HTTP {response.status_code}"
            print(f"❌ Server responded with error: {response.status_code}")
            return results
            
    except requests.exceptions.ConnectionError:
        results['error'] = "Connection refused"
        print(f"❌ Could not connect to {host}")
        print("💡 Make sure Ollama is running: `ollama serve`")
        return results
    except requests.exceptions.Timeout:
        results['error'] = "Connection timeout"
        print(f"⏰ Connection timed out after {timeout}s")
        return results
    except Exception as e:
        results['error'] = str(e)
        print(f"❌ Unexpected error: {e}")
        return results
    
    # Test 2: API functionality
    if results['server_running'] and results['models_available']:
        print("\n🧪 Testing API functionality...")
        test_model = results['models_available'][0]  # Use first available model
        
        try:
            test_payload = {
                "model": test_model,
                "prompt": "Hello! Please respond with just 'API test successful'",
                "stream": False
            }
            
            start_time = time.time()
            response = requests.post(f"{host}/api/generate", 
                                   json=test_payload, timeout=30)
            api_time = time.time() - start_time
            
            if response.status_code == 200:
                results['api_working'] = True
                data = response.json()
                response_text = data.get('response', '')
                results['test_response'] = response_text
                print(f"✅ API test successful (time: {api_time:.2f}s)")
                print(f"   Model: {test_model}")
                print(f"   Response: {response_text[:100]}...")
            else:
                print(f"❌ API test failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ API test error: {e}")
    
    return results

def run_comprehensive_test(host="http://127.0.0.1:11434"):
    """Run comprehensive test suite"""
    print("🔬 Running Comprehensive Ollama Test Suite")
    print("=" * 50)
    
    # Basic connection test
    results = test_ollama_connection(host)
    
    # Health check summary
    print("\n📊 Test Summary:")
    print(f"   🌐 Server: {'✅ Running' if results['server_running'] else '❌ Not responding'}")
    print(f"   📦 Models: {len(results['models_available'])} available")
    print(f"   🧪 API: {'✅ Working' if results['api_working'] else '❌ Failed'}")
    
    if results['response_time']:
        print(f"   ⚡ Speed: {results['response_time']}s response time")
    
    if results['error']:
        print(f"   ❌ Error: {results['error']}")
    
    # Overall status
    if results['server_running'] and results['api_working']:
        print("\n🎉 All tests passed! Ollama is ready to use.")
        return True
    else:
        print("\n❌ Some tests failed. Check configuration and try again.")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test Ollama API connection')
    parser.add_argument('--host', default='http://127.0.0.1:11434', 
                       help='Ollama server host (default: http://127.0.0.1:11434)')
    parser.add_argument('--timeout', type=int, default=10,
                       help='Connection timeout in seconds (default: 10)')
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test (server ping only)')
    
    args = parser.parse_args()
    
    if args.quick:
        # Quick server ping only
        try:
            response = requests.get(f"{args.host}/api/tags", timeout=args.timeout)
            if response.status_code == 200:
                print("✅ Ollama server is running")
                sys.exit(0)
            else:
                print("❌ Ollama server not responding")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            sys.exit(1)
    
    # Full test
    if args.json:
        results = test_ollama_connection(args.host, args.timeout)
        print(json.dumps(results, indent=2))
    else:
        success = run_comprehensive_test(args.host)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()