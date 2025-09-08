#!/usr/bin/env python3
"""
🏥 Health Check Script
Monitor the health of AI-optimized services
"""

import json
import sys
import time

import requests
import Exception
import all
import e
import f
import open
import print
import service
import status
import str
import url


def check_service_health():
    """Check health of all services."""
    services = {
        "ai-optimizer": "http://localhost:8000/health",
        "prometheus": "http://localhost:9090/-/healthy",
        "grafana": "http://localhost:3000/api/health"
    }
    
    results = {}
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results[service] = "HEALTHY"
                print(f"✅ {service}: HEALTHY")
            else:
                results[service] = f"UNHEALTHY (HTTP {response.status_code})"
                print(f"❌ {service}: UNHEALTHY (HTTP {response.status_code})")
        except Exception as e:
            results[service] = f"UNREACHABLE ({str(e)})"
            print(f"❌ {service}: UNREACHABLE ({str(e)})")
    
    # Save results
    with open("health_check_results.json", "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results
        }, f, indent=2)
    
    return all(status == "HEALTHY" for status in results.values())

if __name__ == "__main__":
    healthy = check_service_health()
    sys.exit(0 if healthy else 1)
