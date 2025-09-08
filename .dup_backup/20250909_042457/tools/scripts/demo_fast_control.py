# Demo Fast Control - Ultra-Fast Desktop Control Pack Demo
from __future__ import annotations

import time

from apps.backend.data.implementations.input_control_fast import VK, TurboInputControl
from apps.backend.data.implementations.screen_capture_dxgi import ScreenCapture, benchmark_capture
from apps.backend.data.implementations.screen_control_manager import ScreenControlManager
from apps.backend.data.implementations.screen_targeting import TargetFinder
from apps.backend.data.instrumentation.latency_timer import Timer
import Exception
import KeyboardInterrupt
import bgr
import cap
import color_name
import demo_func
import demo_name
import e
import len
import max
import min
import operation
import operation_name
import print
import range
import sum
import timer
import x
import y


def demo_input_control() -> None:
    """Demo ultra-fast input control"""
    print("=== Input Control Demo ===")

    input_ctrl = TurboInputControl()

    print("1. Mouse movement test...")
    # Move mouse to center of screen
    input_ctrl.move_to(960, 540)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)

    print("2. Click test...")
    input_ctrl.click("left")
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)

    print("3. Keyboard test...")
    # Type "Hello" using VK codes
    input_ctrl.tap(VK.H)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
    input_ctrl.tap(VK.E)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
    input_ctrl.tap(VK.L)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
    input_ctrl.tap(VK.L)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
    input_ctrl.tap(VK.O)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)

    print("4. Hotkey test...")
    # Ctrl+A to select all
    input_ctrl.hotkey(VK.CTRL, VK.A)
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)

    print("5. Scroll test...")
    input_ctrl.scroll(240)  # Scroll up
    # TODO: Replace blocking sleep with async await asyncio.sleep(0.5)

    print("Input control demo completed!")


def demo_screen_capture() -> None:
    """Demo screen capture performance"""
    print("\n=== Screen Capture Demo ===")

    print("Running capture benchmark...")
    results = benchmark_capture(duration=3.0, monitor=0)

    print(f"Capture method: {results['method']}")
    print(f"FPS: {results['fps']:.1f}")
    print(f"Frame count: {results['frame_count']}")
    print(f"Avg frame time: {results['avg_frame_time'] * 1000:.2f} ms")
    print(f"Min frame time: {results['min_frame_time'] * 1000:.2f} ms")
    print(f"Max frame time: {results['max_frame_time'] * 1000:.2f} ms")


def demo_target_finding() -> None:
    """Demo target finding capabilities"""
    print("\n=== Target Finding Demo ===")

    # Test with different colors
    colors = [
        ("Red", (0, 0, 255)),
        ("Green", (0, 255, 0)),
        ("Blue", (255, 0, 0)),
        ("White", (255, 255, 255)),
        ("Black", (0, 0, 0)),
    ]

    with ScreenCapture(target_fps=60) as cap:
        cap.start()
        # TODO: Replace blocking sleep with async await asyncio.sleep(1)  # Let capture stabilize

        for color_name, bgr in colors:
            finder = TargetFinder(bgr, tol=20)

            try:
                frame = cap.frame()
                target = finder.locate(frame)

                if target:
                    x, y = target
                    print(f"{color_name} target found at ({x}, {y})")
                else:
                    print(f"{color_name} target not found")

            except Exception as e:
                print(f"Error finding {color_name} target: {e}")


def demo_integrated_control() -> None:
    """Demo integrated screen control manager"""
    print("\n=== Integrated Control Demo ===")

    # Look for green pixels (you can put a green dot on screen to test)
    manager = ScreenControlManager(color_bgr=(0, 255, 0), tolerance=30)

    print("Starting integrated control (will click on green pixels)...")
    print("Put a green dot on screen to test, or press Ctrl+C to stop")

    try:
        with manager:
            stats = manager.run_continuous(duration=5.0, target_loop_rate=100.0)

        print("\nPerformance Statistics:")
        print(f"Frames processed: {stats['frames_processed']}")
        print(f"Targets found: {stats['targets_found']}")
        print(f"Clicks performed: {stats['clicks_performed']}")
        print(f"Target hit rate: {stats['target_hit_rate']:.2%}")
        print(f"Avg latency: {stats['avg_latency_ms']:.2f} ms")
        print(f"Min latency: {stats['min_latency_ms']:.2f} ms")
        print(f"Max latency: {stats['max_latency_ms']:.2f} ms")

    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    except Exception as e:
        print(f"Demo error: {e}")


def demo_latency_measurement() -> None:
    """Demo latency measurement capabilities"""
    print("\n=== Latency Measurement Demo ===")

    # Test different operations
    operations = {
        "Mouse move": lambda: TurboInputControl().move_to(500, 500),
        "Mouse click": lambda: TurboInputControl().click("left"),
        "Key tap": lambda: TurboInputControl().tap(VK.SPACE),
        "Screen capture": lambda: test_capture_once(),
    }

    def test_capture_once():
        with ScreenCapture() as cap:
            cap.start()
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)  # Brief wait
            cap.frame()

    for operation_name, operation in operations.items():
        latencies = []

        for _ in range(10):  # Test each operation 10 times
            with Timer(operation_name) as timer:
                try:
                    operation()
                except Exception:
                    continue
            latencies.append(timer.ms)
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)  # Brief pause between tests

        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)

            print(f"{operation_name}:")
            print(f"  Avg: {avg_latency:.2f} ms")
            print(f"  Min: {min_latency:.2f} ms")
            print(f"  Max: {max_latency:.2f} ms")


def demo_priority_boost() -> None:
    """Demo process priority boosting"""
    print("\n=== Priority Boost Demo ===")

    input_ctrl = TurboInputControl()

    print("Testing performance before priority boost...")

    # Test operation speed before boost
    start_time = time.perf_counter()
    for _ in range(100):
        input_ctrl.move_to(100, 100)
    before_time = time.perf_counter() - start_time

    print("Boosting process priority...")
    input_ctrl.boost_priority()

    print("Testing performance after priority boost...")

    # Test operation speed after boost
    start_time = time.perf_counter()
    for _ in range(100):
        input_ctrl.move_to(200, 200)
    after_time = time.perf_counter() - start_time

    print(f"Before boost: {before_time * 1000:.2f} ms for 100 operations")
    print(f"After boost: {after_time * 1000:.2f} ms for 100 operations")

    if after_time < before_time:
        improvement = ((before_time - after_time) / before_time) * 100
        print(f"Performance improvement: {improvement:.1f}%")
    else:
        print("No significant improvement detected")


def main() -> None:
    """Run all demos"""
    print("🚀 Ultra-Fast Desktop Control Pack Demo")
    print("=" * 50)

    demos = [
        ("Input Control", demo_input_control),
        ("Screen Capture", demo_screen_capture),
        ("Target Finding", demo_target_finding),
        ("Latency Measurement", demo_latency_measurement),
        ("Priority Boost", demo_priority_boost),
        ("Integrated Control", demo_integrated_control),
    ]

    for demo_name, demo_func in demos:
        try:
            print(f"\n{'=' * 20} {demo_name} {'=' * 20}")
            demo_func()
            # TODO: Replace blocking sleep with async await asyncio.sleep(1)  # Brief pause between demos
        except KeyboardInterrupt:
            print(f"\n{demo_name} demo interrupted")
            break
        except Exception as e:
            print(f"Error in {demo_name} demo: {e}")

    print("\n✅ All demos completed!")
    print("\nNotes:")
    print("- Make sure you have dxcam and mss installed for best performance")
    print("- Run as administrator for best input control performance")
    print("- Test in a safe environment (demos will move mouse and click)")


if __name__ == "__main__":
    main()
