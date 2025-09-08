#!/usr/bin/env python3
"""
🚀 Đề Xuất Sử Dụng Ollama API Key Tối Ưu
========================================

API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP

Tài liệu hướng dẫn sử dụng API key hiệu quả và tiết kiệm chi phí
"""

import json
import time
from datetime import datetime

from dotenv import load_dotenv

# Load environment (.env first, then .env.local overrides)
load_dotenv()
load_dotenv(".env.local", override=True)


class OllamaAPIOptimizer:
    """Class để tối ưu hóa việc sử dụng Ollama API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "cost_estimate": 0.0,
            "cache_hits": 0,
            "start_time": time.time(),
        }
        self.cache = {}
        self.rate_limiter = {"last_request": 0, "min_interval": 0.1}  # 100ms giữa các request

    def estimate_cost(self, prompt: str, response: str = "") -> float:
        """Ước tính chi phí cho request"""
        # Ước tính: ~1000 tokens = $0.002 (giá tham khảo)
        input_tokens = len(prompt.split()) * 1.3  # ~1.3 tokens per word
        output_tokens = len(response.split()) * 1.3 if response else 100  # ước tính
        total_tokens = input_tokens + output_tokens

        # Chi phí ước tính ($0.002 per 1K tokens)
        cost = (total_tokens / 1000) * 0.002
        return cost

    def should_use_cache(self, prompt: str) -> bool:
        """Kiểm tra xem có nên dùng cache không"""
        cache_key = hash(prompt.lower().strip())

        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            # Cache valid for 10 minutes
            if time.time() - cache_entry["timestamp"] < 600:
                self.usage_stats["cache_hits"] += 1
                return True

        return False

    def get_cached_response(self, prompt: str) -> str:
        """Lấy response từ cache"""
        cache_key = hash(prompt.lower().strip())
        return self.cache[cache_key]["response"]

    def cache_response(self, prompt: str, response: str):
        """Lưu response vào cache"""
        cache_key = hash(prompt.lower().strip())
        self.cache[cache_key] = {"response": response, "timestamp": time.time()}

    def rate_limit_check(self):
        """Kiểm tra rate limiting"""
        now = time.time()
        if now - self.rate_limiter["last_request"] < self.rate_limiter["min_interval"]:
            # TODO: Replace blocking sleep with async await asyncio.sleep(self.rate_limiter["min_interval"])
        self.rate_limiter["last_request"] = time.time()

    def update_stats(self, prompt: str, response: str):
        """Cập nhật thống kê sử dụng"""
        self.usage_stats["total_requests"] += 1
        tokens = len(prompt.split()) + len(response.split())
        self.usage_stats["total_tokens"] += tokens
        self.usage_stats["cost_estimate"] += self.estimate_cost(prompt, response)

    def get_usage_report(self) -> dict:
        """Báo cáo sử dụng API"""
        runtime = time.time() - self.usage_stats["start_time"]

        return {
            "session_duration": f"{runtime/60:.1f} minutes",
            "total_requests": self.usage_stats["total_requests"],
            "total_tokens": self.usage_stats["total_tokens"],
            "estimated_cost": f"${self.usage_stats['cost_estimate']:.4f}",
            "cache_hits": self.usage_stats["cache_hits"],
            "cache_efficiency": f"{(self.usage_stats['cache_hits']/max(1, self.usage_stats['total_requests']))*100:.1f}%",
            "avg_tokens_per_request": self.usage_stats["total_tokens"] / max(1, self.usage_stats["total_requests"]),
            "requests_per_minute": (self.usage_stats["total_requests"] / max(1, runtime / 60)),
        }


def print_optimization_strategies():
    """In ra các chiến lược tối ưu hóa"""
    print("🎯 CHIẾN LƯỢC TỐI ỨU API KEY")
    print("=" * 50)

    strategies = [
        {
            "title": "1. 💰 Tiết Kiệm Chi Phí",
            "tips": [
                "• Sử dụng cache cho các câu hỏi lặp lại",
                "• Giới hạn max_tokens để tránh response quá dài",
                "• Batch multiple requests khi có thể",
                "• Sử dụng local Ollama cho development/testing",
            ],
        },
        {
            "title": "2. ⚡ Tăng Hiệu Suất",
            "tips": [
                "• Implement connection pooling",
                "• Sử dụng async/await cho multiple requests",
                "• Rate limiting để tránh bị throttle",
                "• Fallback strategy (Turbo API -> Local Ollama)",
            ],
        },
        {
            "title": "3. 🛡️ Bảo Mật API Key",
            "tips": [
                "• Lưu trong .env file, không commit vào git",
                "• Sử dụng environment variables",
                "• Monitor usage để phát hiện bất thường",
                "• Rotate key định kỳ nếu cần",
            ],
        },
        {
            "title": "4. 📊 Monitoring & Logging",
            "tips": [
                "• Track số requests và tokens used",
                "• Log error rates và response times",
                "• Set up alerts cho usage limits",
                "• Regular usage reports",
            ],
        },
    ]

    for strategy in strategies:
        print(f"\n{strategy['title']}")
        print("-" * 30)
        for tip in strategy["tips"]:
            print(f"  {tip}")


def print_usage_examples():
    """Ví dụ sử dụng API key hiệu quả"""
    print("\n\n💡 VÍ DỤ SỬ DỤNG TỐI ỨU")
    print("=" * 50)

    examples = [
        {
            "title": "Smart Caching",
            "code": """
# Sử dụng cache thông minh
optimizer = OllamaAPIOptimizer(api_key)

def smart_query(prompt):
    if optimizer.should_use_cache(prompt):
        return optimizer.get_cached_response(prompt)
    
    # Make API call
    response = api_call(prompt)
    optimizer.cache_response(prompt, response)
    return response
""",
        },
        {
            "title": "Batch Processing",
            "code": """
# Xử lý nhiều requests cùng lúc
async def batch_process(prompts):
    tasks = []
    for prompt in prompts:
        task = asyncio.create_task(api_call(prompt))
        tasks.append(task)
    
    responses = await asyncio.gather(*tasks)
    return responses
""",
        },
        {
            "title": "Cost-Aware Requests",
            "code": """
# Kiểm soát chi phí
def cost_aware_request(prompt, max_cost=0.01):
    estimated_cost = optimizer.estimate_cost(prompt)
    
    if estimated_cost > max_cost:
        print(f"⚠️ Chi phí ước tính: ${estimated_cost:.4f} > ${max_cost}")
        return None
    
    return api_call(prompt)
""",
        },
    ]

    for example in examples:
        print(f"\n📝 {example['title']}:")
        print(example["code"])


def create_optimized_config():
    """Tạo file config tối ưu"""
    config = {
        "api_settings": {
            "turbo_api_key": "5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP",
            "primary_endpoint": "https://api.turbo.ai/v1",
            "fallback_endpoint": "http://127.0.0.1:11434",
            "timeout": 30,
            "max_retries": 3,
        },
        "optimization": {
            "cache_enabled": True,
            "cache_ttl_seconds": 600,
            "rate_limit_requests_per_minute": 60,
            "max_tokens_per_request": 1000,
            "batch_size": 5,
        },
        "cost_control": {"daily_budget_usd": 5.0, "max_cost_per_request": 0.10, "alert_threshold": 0.80},
        "fallback_strategy": {
            "use_local_ollama_for_dev": True,
            "fallback_on_error": True,
            "fallback_on_rate_limit": True,
        },
    }

    with open("ollama_api_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("\n✅ Config file created: ollama_api_config.json")


def main():
    """Main function"""
    print("🚀 OLLAMA API KEY OPTIMIZATION GUIDE")
    print("=" * 60)
    print("API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print_optimization_strategies()
    print_usage_examples()

    print("\n\n🔧 SETUP RECOMMENDATIONS")
    print("=" * 50)

    recommendations = [
        "1. 🔐 Bảo mật API key trong .env file",
        "2. ⚡ Sử dụng local Ollama cho development",
        "3. 💰 Monitor usage để kiểm soát chi phí",
        "4. 🚀 Implement caching và rate limiting",
        "5. 📊 Set up logging và monitoring",
        "6. 🔄 Configure fallback strategy",
    ]

    for rec in recommendations:
        print(f"  {rec}")

    print("\n📋 NEXT STEPS:")
    print("  • Run: python optimized_turbo_client.py")
    print("  • Config: Edit ollama_api_config.json")
    print("  • Monitor: Check usage stats regularly")

    # Create optimized config
    create_optimized_config()

    print("\n🎉 API Key ready for optimized usage!")


if __name__ == "__main__":
    main()
