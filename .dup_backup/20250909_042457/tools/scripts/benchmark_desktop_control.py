# scripts/benchmark_desktop_control.py
from __future__ import annotations

from apps.backend.data.implementations import ScreenCapture, ScreenControlManager, TurboInputControl
from apps.backend.data.instrumentation.performance_benchmark import PerformanceBenchmark
import Exception
import e
import print
import r
import result
import sum


def main():
    """Run comprehensive performance benchmarks."""
    print("🚀 Starting Ultra-Fast Desktop Control Benchmarks...")

    benchmark = PerformanceBenchmark()

    # 1. Input Control Benchmark
    print("\n📱 Benchmarking TurboInputControl...")
    ic = TurboInputControl()
    ic.boost_priority()  # Max performance

    input_result = benchmark.benchmark_input_latency(ic, iterations=200)
    print(f"Input latency: {input_result.avg_time * 1000:.2f}ms avg, {input_result.fps:.1f} ops/sec")

    # 2. Screen Capture Benchmark (if available)
    print("\n📺 Benchmarking ScreenCapture...")
    try:
        cap = ScreenCapture(target_fps=240, region=(100, 100, 800, 600))  # ROI for speed
        capture_result = benchmark.benchmark_screen_capture(cap, iterations=100)
        print(f"Screen capture: {capture_result.avg_time * 1000:.2f}ms avg, {capture_result.fps:.1f} FPS")
    except Exception as e:
        print(f"Screen capture not available: {e}")

    # 3. End-to-End Benchmark
    print("\n🎯 Benchmarking End-to-End Control...")
    try:
        manager = ScreenControlManager(color_bgr=(0, 255, 0))
        e2e_result = benchmark.benchmark_end_to_end(manager, iterations=30)
        print(f"End-to-end: {e2e_result.avg_time * 1000:.2f}ms avg, {e2e_result.fps:.1f} cycles/sec")
    except Exception as e:
        print(f"End-to-end benchmark failed: {e}")

    # 4. Hot Function Benchmarks
    print("\n🔥 Benchmarking Hot Functions...")

    # Mouse move benchmark
    benchmark.benchmark_function(lambda: ic.move_to(500, 500), iterations=1000, name="mouse_move_absolute")

    # Keyboard hotkey benchmark
    benchmark.benchmark_function(
        lambda: ic.hotkey(0x11, 0x43),  # Ctrl+C
        iterations=500,
        name="keyboard_hotkey",
    )

    # Click benchmark
    benchmark.benchmark_function(lambda: ic.click("left"), iterations=500, name="mouse_click")

    # Print comprehensive results
    benchmark.print_results()

    # Performance targets check
    print("\n🎯 PERFORMANCE TARGET ANALYSIS:")
    print("=" * 60)

    # Check if we hit performance targets
    targets = {
        "input_latency": 5.0,  # < 5ms for input
        "screen_capture": 8.33,  # < 8.33ms for 120 FPS
        "end_to_end": 15.0,  # < 15ms end-to-end
        "mouse_move_absolute": 2.0,  # < 2ms for mouse move
    }

    for result in benchmark.results:
        target = targets.get(result.name)
        if target:
            avg_ms = result.avg_time * 1000
            status = "✅ PASS" if avg_ms <= target else "❌ FAIL"
            print(f"{result.name:20} {avg_ms:6.2f}ms (target: {target:5.1f}ms) {status}")

    print(f"\n💾 Total benchmark time: {sum(r.total_time for r in benchmark.results):.1f}s")


if __name__ == "__main__":
    main()
