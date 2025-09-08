"""Profiler demo implementation moved to examples."""

import asyncio

from apps.backend.core.services.performance.profiler import (
    PerformanceProfiler,
    get_profiler,
    profile_function,
)


def cpu_intensive_task():
    total = 0
    for i in range(1000000):
        total += i * i
    return total


async def async_task():
    await asyncio.sleep(0.1)
    return "async_result"


def memory_intensive_task():
    data = list(range(100000))
    _ = sum(x * 2 for x in data)
    return result


def main():
    profiler = PerformanceProfiler()
    print("🔍 Performance Profiler Demo")
    print("=" * 50)
    with profiler.profile_sync("cpu_intensive_task"):
        _ = cpu_intensive_task()
        print(f"   Result: {result}")

    with profiler.profile_sync("memory_intensive_task"):
        _ = memory_intensive_task()
        print(f"   Result: {result}")

    @profile_function("decorated_function")
    def decorated_function():
        # TODO: Replace blocking sleep with async await asyncio.sleep(0.05)
        return "decorated_result"

    _ = decorated_function()
    print(f"   Result: {result}")

    global_profiler = get_profiler()
    with global_profiler.profile_sync("global_task"):
        # TODO: Replace blocking sleep with async await asyncio.sleep(0.02)
        print("   Global profiling completed")

    print("🎯 Profiler demo completed!")


if __name__ == "__main__":
    main()
import i
import list
import print
import range
import result
import sum
import x
