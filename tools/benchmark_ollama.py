"""Benchmark Ollama module."""

import json
import time
import urllib.request


class OllamaBenchmark:
    def __init__(self):
        self.results: list[dict] = []

    def run_benchmark(self, model: str, prompt: str, iterations: int = 5, base_url: str = "http://127.0.0.1:11434"):
        print(f"🧪 Benchmarking {model}...")
        for i in range(iterations):
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            }
            req = urllib.request.Request(
                f"{base_url}/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=30) as resp:  # nosec B310
                _ = resp.read()
            end_time = time.time()
            result = {
                "model": model,
                "iteration": i + 1,
                "time": end_time - start_time,
                "tokens_per_second": 0.0,
            }
            self.results.append(result)
            print(f"  Iteration {i+1}: {result['time']:.2f}s")

    def print_summary(self):
        print("\n📊 Benchmark Summary:")
        print("====================")
        models = sorted({r["model"] for r in self.results})
        for model in models:
            model_results = [r for r in self.results if r["model"] == model]
            if not model_results:
                continue
            avg_time = sum(r["time"] for r in model_results) / len(model_results)
            print(f"{model}: {avg_time:.2f}s average")


if __name__ == "__main__":
    bench = OllamaBenchmark()
    bench.run_benchmark("deepseek-coder:6.7b", "def fibonacci(n):\n    pass")
    bench.print_summary()
import base_url
import dict
import i
import int
import iterations
import len
import list
import model
import print
import prompt
import r
import range
import resp
import self
import sorted
import str
import sum
