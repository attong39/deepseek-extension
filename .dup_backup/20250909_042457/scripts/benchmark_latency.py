#!/usr/bin/env python3
"""
benchmark_latency.py - Benchmark Script for Ollama Models

Measures response latency and code quality for different Ollama models
including StarCoder, DeepSeek Coder, and the fine-tuned Vietnamese model.

Usage:
    python benchmark_latency.py

Output:
    - Latency measurements for each model
    - Sample code generation for Vietnamese prompts
    - Performance comparison table
"""

import json
import logging
import statistics
import time
from dataclasses import dataclass
from typing import Any

import requests
import Exception
import any
import avail
import bool
import char
import dict
import e
import enumerate
import f
import filename
import float
import i
import int
import keyword
import len
import list
import max
import min
import model
import num_tests
import ollama_url
import open
import print
import prompt
import self
import sorted
import str
import sum
import timeout
import x

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Benchmark result for a single model"""

    model_name: str
    avg_latency: float
    min_latency: float
    max_latency: float
    std_latency: float
    success_rate: float
    sample_output: str
    vietnamese_quality: int  # 1-10 scale


class OllamaBenchmark:
    """Benchmark suite for Ollama models"""

    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.results = {}

        # Test prompts in Vietnamese
        self.test_prompts = [
            "Viết hàm Python tính giai thừa của một số nguyên",
            "Tạo hàm kiểm tra số nguyên tố",
            "Viết code để sắp xếp danh sách theo thứ tự tăng dần",
            "Tạo hàm tính trung bình cộng của một danh sách số",
            "Viết hàm đệ quy tính số Fibonacci",
            "Tạo class Python để quản lý danh sách sinh viên",
            "Viết hàm đọc file CSV và trả về DataFrame",
            "Tạo decorator để đo thời gian thực thi hàm",
            "Viết hàm kết nối và truy vấn cơ sở dữ liệu SQLite",
            "Tạo API endpoint Flask để xử lý POST request",
        ]

        # Models to benchmark
        self.models = [
            "starcoder:latest",
            "codellama:13b-instruct",
            "deepseek-coder:1.3b",
            "attong39/zeta",  # Our fine-tuned model (if available)
            "zeta-py-teacher",  # Alternative name for our model
        ]

    def check_ollama_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            return False

    def get_available_models(self) -> list[str]:
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                available = [model["name"] for model in models_data.get("models", [])]
                logger.info(f"📋 Available models: {available}")
                return available
            return []
        except Exception as e:
            logger.error(f"❌ Error getting models: {e}")
            return []

    def generate_response(self, model: str, prompt: str, timeout: int = 30) -> dict[str, Any] | None:
        """Generate response from Ollama model"""
        try:
            start_time = time.time()

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "max_tokens": 500, "top_p": 0.9},
            }

            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=timeout)

            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "latency": latency,
                    "response": result.get("response", ""),
                    "model": model,
                    "prompt": prompt,
                }
            else:
                logger.error(f"❌ Model {model} returned status {response.status_code}")
                return {
                    "success": False,
                    "latency": latency,
                    "error": f"HTTP {response.status_code}",
                    "model": model,
                    "prompt": prompt,
                }

        except requests.exceptions.Timeout:
            return {"success": False, "latency": timeout * 1000, "error": "Timeout", "model": model, "prompt": prompt}
        except Exception as e:
            return {"success": False, "latency": 0, "error": str(e), "model": model, "prompt": prompt}

    def assess_vietnamese_quality(self, response: str) -> int:
        """Assess the quality of Vietnamese in the response (1-10 scale)"""
        score = 5  # Base score

        # Check for Vietnamese characters
        vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
        has_vietnamese = any(char in response.lower() for char in vietnamese_chars)
        if has_vietnamese:
            score += 2

        # Check for Vietnamese keywords in comments
        vn_keywords = ["hàm", "tính", "trả về", "tham số", "kết quả", "danh sách", "số", "chuỗi", "dữ liệu"]
        vn_count = sum(1 for keyword in vn_keywords if keyword in response.lower())
        score += min(vn_count, 3)  # Max 3 points

        # Check for proper code structure
        if "def " in response:
            score += 1
        if '"""' in response or "'''" in response:  # Docstring
            score += 1

        return min(score, 10)

    def benchmark_model(self, model: str, num_tests: int = 5) -> BenchmarkResult | None:
        """Benchmark a single model"""
        logger.info(f"🧪 Benchmarking model: {model}")

        latencies = []
        successes = 0
        sample_outputs = []
        vietnamese_scores = []

        for i, prompt in enumerate(self.test_prompts[:num_tests]):
            logger.info(f"  📝 Test {i+1}/{num_tests}: {prompt[:50]}...")

            result = self.generate_response(model, prompt)

            if result["success"]:
                latencies.append(result["latency"])
                successes += 1

                response = result["response"]
                sample_outputs.append(response)

                # Assess Vietnamese quality
                vn_score = self.assess_vietnamese_quality(response)
                vietnamese_scores.append(vn_score)

                logger.info(f"    ✅ Latency: {result['latency']:.0f}ms, VN Score: {vn_score}/10")
            else:
                logger.warning(f"    ❌ Failed: {result.get('error', 'Unknown error')}")

        if not latencies:
            logger.error(f"❌ All tests failed for model {model}")
            return None

        # Calculate statistics
        avg_latency = statistics.mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        std_latency = statistics.stdev(latencies) if len(latencies) > 1 else 0
        success_rate = successes / num_tests
        avg_vn_score = statistics.mean(vietnamese_scores) if vietnamese_scores else 0

        # Get best sample output (highest Vietnamese score)
        if vietnamese_scores:
            best_idx = vietnamese_scores.index(max(vietnamese_scores))
            best_sample = sample_outputs[best_idx]
        else:
            best_sample = sample_outputs[0] if sample_outputs else "No output"

        result = BenchmarkResult(
            model_name=model,
            avg_latency=avg_latency,
            min_latency=min_latency,
            max_latency=max_latency,
            std_latency=std_latency,
            success_rate=success_rate,
            sample_output=best_sample[:500],  # Truncate for display
            vietnamese_quality=int(avg_vn_score),
        )

        logger.info(f"  📊 Results - Avg: {avg_latency:.0f}ms, Success: {success_rate:.1%}, VN: {avg_vn_score:.1f}/10")
        return result

    def run_benchmark(self, num_tests: int = 5) -> dict[str, BenchmarkResult]:
        """Run benchmark on all available models"""
        logger.info("🚀 Starting Ollama Model Benchmark")
        logger.info("=" * 50)

        # Check connection
        if not self.check_ollama_connection():
            logger.error("❌ Cannot connect to Ollama server")
            return {}

        # Get available models
        available_models = self.get_available_models()
        test_models = [
            model for model in self.models if any(avail.startswith(model.split(":")[0]) for avail in available_models)
        ]

        if not test_models:
            logger.warning("⚠️  No target models available, testing all available models")
            test_models = available_models[:3]  # Test first 3 available models

        logger.info(f"🎯 Testing models: {test_models}")

        results = {}
        for model in test_models:
            try:
                result = self.benchmark_model(model, num_tests)
                if result:
                    results[model] = result
                    self.results[model] = result
            except Exception as e:
                logger.error(f"❌ Error benchmarking {model}: {e}")

        return results

    def print_results(self):
        """Print benchmark results in a formatted table"""
        if not self.results:
            logger.error("❌ No results to display")
            return

        print("\n🏆 BENCHMARK RESULTS")
        print("=" * 80)
        print(f"{'Model':<25} {'Avg (ms)':<10} {'Min (ms)':<10} {'Max (ms)':<10} {'Success':<10} {'VN Score':<10}")
        print("-" * 80)

        # Sort by average latency
        sorted_results = sorted(self.results.items(), key=lambda x: x[1].avg_latency)

        for model, result in sorted_results:
            print(
                f"{model:<25} {result.avg_latency:<10.0f} {result.min_latency:<10.0f} "
                f"{result.max_latency:<10.0f} {result.success_rate:<10.1%} {result.vietnamese_quality:<10}"
            )

        print("\n🎯 TARGET METRICS")
        print("-" * 40)
        print("✅ Latency < 1000ms (1 second)")
        print("✅ Success rate > 90%")
        print("✅ Vietnamese score > 7/10")

        print("\n📝 SAMPLE OUTPUTS")
        print("-" * 40)
        for model, result in sorted_results:
            if result.vietnamese_quality >= 7:  # Only show high-quality Vietnamese outputs
                print(f"\n🤖 {model} (VN Score: {result.vietnamese_quality}/10):")
                print("-" * 30)
                print(result.sample_output[:300] + "..." if len(result.sample_output) > 300 else result.sample_output)

    def save_results(self, filename: str = "benchmark_results.json"):
        """Save results to JSON file"""
        if not self.results:
            return

        # Convert to serializable format
        results_data = {}
        for model, result in self.results.items():
            results_data[model] = {
                "model_name": result.model_name,
                "avg_latency": result.avg_latency,
                "min_latency": result.min_latency,
                "max_latency": result.max_latency,
                "std_latency": result.std_latency,
                "success_rate": result.success_rate,
                "sample_output": result.sample_output,
                "vietnamese_quality": result.vietnamese_quality,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Results saved to {filename}")


def main():
    """Main function"""
    logger.info("🚀 Ollama Model Benchmark Suite")
    logger.info("Measuring latency and Vietnamese code quality")

    benchmark = OllamaBenchmark()

    # Run benchmark
    results = benchmark.run_benchmark(num_tests=3)  # Reduced for faster testing

    if results:
        # Print results
        benchmark.print_results()

        # Save results
        benchmark.save_results()

        logger.info("✅ Benchmark completed successfully!")
    else:
        logger.error("❌ Benchmark failed - no results obtained")


if __name__ == "__main__":
    main()
