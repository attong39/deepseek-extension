#!/usr/bin/env python3
"""
Benchmark Ultra-Fast Desktop Control Pack
Performance testing và optimization validation
"""

from __future__ import annotations

import gc
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass

from apps.backend.data.implementations.input_control_fast import VK, TurboInputControl
from apps.backend.data.implementations.screen_capture_dxgi import ScreenCapture
from apps.backend.data.implementations.screen_control_manager import ScreenControlManager
from apps.backend.data.implementations.screen_targeting import TargetFinder
import Exception
import KeyboardInterrupt
import cap
import e
import f
import float
import frame
import int
import iterations
import len
import list
import max
import method_func
import method_name
import min
import operation
import operation_name
import print
import range
import self
import str
import target_name
import target_value
import tol
import warmup


@dataclass
class BenchmarkResult:
    """Kết quả benchmark"""

    operation: str
    iterations: int
    avg_time_ms: float
    min_time_ms: float
    max_time_ms: float
    std_dev_ms: float
    ops_per_second: float
    success_rate: float


class PerformanceBenchmark:
    """Benchmark suite cho desktop control pack"""

    def __init__(self):
        self.results: list[BenchmarkResult] = []
        self.input_ctrl = TurboInputControl()

    def run_benchmark(
        self,
        operation_name: str,
        operation: Callable[[], None],
        iterations: int = 100,
        warmup: int = 10,
    ) -> BenchmarkResult:
        """Chạy benchmark cho một operation"""

        print(f"Benchmarking {operation_name} ({iterations} iterations)...")

        # Warmup
        for _ in range(warmup):
            try:
                operation()
            except Exception:
                pass

        # Actual benchmark
        times = []
        failures = 0

        gc.collect()  # Clean memory before benchmark

        for i in range(iterations):
            start = time.perf_counter()
            try:
                operation()
                end = time.perf_counter()
                times.append((end - start) * 1000)  # Convert to ms
            except Exception as e:
                failures += 1
                print(f"  Failure {failures}: {e}")

        if not times:
            print(f"  ERROR: All {iterations} iterations failed!")
            return BenchmarkResult(
                operation=operation_name,
                iterations=iterations,
                avg_time_ms=0,
                min_time_ms=0,
                max_time_ms=0,
                std_dev_ms=0,
                ops_per_second=0,
                success_rate=0,
            )

        # Calculate statistics
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        ops_per_second = 1000 / avg_time if avg_time > 0 else 0
        success_rate = (iterations - failures) / iterations

        result = BenchmarkResult(
            operation=operation_name,
            iterations=iterations,
            avg_time_ms=avg_time,
            min_time_ms=min_time,
            max_time_ms=max_time,
            std_dev_ms=std_dev,
            ops_per_second=ops_per_second,
            success_rate=success_rate,
        )

        self.results.append(result)

        print(f"  ✅ Avg: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")
        print(f"     Ops/sec: {ops_per_second:.1f}, Success: {success_rate:.1%}")

        return result

    def benchmark_input_operations(self) -> None:
        """Benchmark input control operations"""
        print("\n=== Input Control Benchmarks ===")

        # Mouse movement
        self.run_benchmark("Mouse Move", lambda: self.input_ctrl.move_to(500, 500), iterations=1000)

        # Mouse clicks
        self.run_benchmark("Mouse Click", lambda: self.input_ctrl.click("left"), iterations=500)

        # Key presses
        self.run_benchmark("Key Press", lambda: self.input_ctrl.tap(VK.SPACE), iterations=500)

        # Hotkeys
        self.run_benchmark("Hotkey (Ctrl+C)", lambda: self.input_ctrl.hotkey(VK.CTRL, VK.C), iterations=200)

        # Scrolling
        self.run_benchmark("Mouse Scroll", lambda: self.input_ctrl.scroll(120), iterations=200)

    def benchmark_screen_capture(self) -> None:
        """Benchmark screen capture performance"""
        print("\n=== Screen Capture Benchmarks ===")

        # Test different capture methods
        methods = [
            ("DXGI Capture", lambda: self._test_dxgi_capture()),
            ("MSS Capture", lambda: self._test_mss_capture()),
        ]

        for method_name, method_func in methods:
            self.run_benchmark(method_name, method_func, iterations=100)

    def _test_dxgi_capture(self) -> None:
        """Test DXGI capture"""
        with ScreenCapture(method="dxgi", target_fps=120) as cap:
            cap.start()
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.001)  # Brief wait
            cap.frame()

    def _test_mss_capture(self) -> None:
        """Test MSS capture"""
        with ScreenCapture(method="mss", target_fps=60) as cap:
            cap.start()
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.001)  # Brief wait
            cap.frame()

    def benchmark_targeting(self) -> None:
        """Benchmark target finding operations"""
        print("\n=== Target Finding Benchmarks ===")

        # Capture a frame first
        with ScreenCapture(target_fps=60) as cap:
            cap.start()
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)
            test_frame = cap.frame()

        if test_frame is None:
            print("  ERROR: Could not capture test frame")
            return

        # Test different color tolerances
        tolerances = [5, 10, 20, 50]
        for tol in tolerances:
            finder = TargetFinder(color_bgr=(0, 255, 0), tol=tol)
            self.run_benchmark(
                f"Color Finding (tol={tol})",
                lambda f=finder, frame=test_frame: f.locate(frame),
                iterations=500,
            )

    def benchmark_integrated_pipeline(self) -> None:
        """Benchmark full capture-target-click pipeline"""
        print("\n=== Integrated Pipeline Benchmarks ===")

        manager = ScreenControlManager(color_bgr=(0, 255, 0), tolerance=20)

        def run_pipeline():
            with manager:
                # Single pipeline iteration
                manager.run_once()

        self.run_benchmark("Full Pipeline (Capture+Target+Click)", run_pipeline, iterations=100)

    def benchmark_priority_impact(self) -> None:
        """Benchmark impact of priority boosting"""
        print("\n=== Priority Impact Benchmarks ===")

        # Test before priority boost
        self.run_benchmark(
            "Mouse Move (Normal Priority)",
            lambda: self.input_ctrl.move_to(300, 300),
            iterations=200,
        )

        # Boost priority
        self.input_ctrl.boost_priority()

        # Test after priority boost
        self.run_benchmark("Mouse Move (High Priority)", lambda: self.input_ctrl.move_to(400, 400), iterations=200)

    def run_all_benchmarks(self) -> None:
        """Chạy tất cả benchmarks"""
        print("🚀 Ultra-Fast Desktop Control Pack - Performance Benchmark")
        print("=" * 70)

        try:
            self.benchmark_input_operations()
            self.benchmark_screen_capture()
            self.benchmark_targeting()
            self.benchmark_integrated_pipeline()
            self.benchmark_priority_impact()

        except KeyboardInterrupt:
            print("\n⚠️ Benchmark interrupted by user")
        except Exception as e:
            print(f"\n❌ Benchmark error: {e}")

        self.print_summary()

    def print_summary(self) -> None:
        """In báo cáo tổng kết"""
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 70)

        if not self.results:
            print("No benchmark results available")
            return

        # Performance targets
        targets = {
            "Mouse Move": 2.0,  # < 2ms target
            "Mouse Click": 5.0,  # < 5ms target
            "Key Press": 3.0,  # < 3ms target
            "DXGI Capture": 8.33,  # 120 FPS = 8.33ms frame time
            "MSS Capture": 16.67,  # 60 FPS = 16.67ms frame time
            "Color Finding": 1.0,  # < 1ms target
            "Full Pipeline": 10.0,  # < 10ms total pipeline
        }

        print(f"{'Operation':<30} {'Avg (ms)':<10} {'Target':<10} {'Status':<10}")
        print("-" * 70)

        for result in self.results:
            target_time = None
            status = "📈"

            # Find matching target
            for target_name, target_value in targets.items():
                if target_name in result.operation:
                    target_time = target_value
                    status = "✅" if result.avg_time_ms <= target_value else "❌"
                    break

            target_str = f"{target_time:.1f}" if target_time else "N/A"

            print(f"{result.operation:<30} {result.avg_time_ms:<10.2f} {target_str:<10} {status:<10}")

        # Overall performance assessment
        print("\n" + "=" * 70)

        # Calculate overall performance score
        passed_tests = 0
        total_tests = 0

        for result in self.results:
            for target_name, target_value in targets.items():
                if target_name in result.operation:
                    total_tests += 1
                    if result.avg_time_ms <= target_value:
                        passed_tests += 1
                    break

        if total_tests > 0:
            score = (passed_tests / total_tests) * 100
            print(f"OVERALL PERFORMANCE SCORE: {score:.1f}% ({passed_tests}/{total_tests} targets met)")

            if score >= 90:
                print("🎉 EXCELLENT! Ultra-fast performance achieved!")
            elif score >= 75:
                print("✅ GOOD! Performance targets mostly met")
            elif score >= 50:
                print("⚠️ MODERATE! Some optimization needed")
            else:
                print("❌ POOR! Significant optimization required")

        # Recommendations
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")

        for result in self.results:
            if result.success_rate < 0.95:
                print(f"- Improve reliability for {result.operation} (success rate: {result.success_rate:.1%})")

            for target_name, target_value in targets.items():
                if target_name in result.operation and result.avg_time_ms > target_value:
                    print(
                        f"- Optimize {result.operation} (current: {result.avg_time_ms:.2f}ms, target: {target_value:.2f}ms)"
                    )

        print("\n🔧 SYSTEM RECOMMENDATIONS:")
        print("- Run as Administrator for best input performance")
        print("- Close unnecessary applications")
        print("- Use DXGI capture method for best screen capture performance")
        print("- Consider process priority boosting for critical applications")


def main():
    """Main benchmark entry point"""
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()


if __name__ == "__main__":
    main()
