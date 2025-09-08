# 🚀 Ultra-Fast Desktop Control Pack

High-performance Windows apps/desktop automation với sub-millisecond latency và 120+ FPS screen capture.

## ✨ Tính năng chính

### 🎯 Ultra-Fast Input Control
- **Win32 SendInput API** cho input độ trễ cực thấp (< 2ms)
- **Batch operations** cho multiple actions
- **DPI awareness** tự động
- **Multi-monitor support** 
- **Process priority boosting**
- **Absolute coordinate system**

### 📷 High-Speed Screen Capture  
- **DXGI capture** với 120+ FPS target
- **MSS fallback** cho compatibility
- **Zero-copy operations** khi có thể
- **Multi-monitor support**
- **Configurable target FPS**

### 🎪 Smart Targeting
- **Color-based pixel detection** với tolerance
- **Template matching** (planned)
- **Region-based search** (planned)
- **Multi-target support** (planned)
- **Numpy-optimized operations**

### ⚡ Integrated Pipeline
- **Capture → Detect → Click** trong single operation
- **Performance monitoring** built-in
- **Configurable loop rates** (up to 1000Hz)
- **Statistics tracking**
- **Context manager support**

## 🛠️ Cài đặt

### Dependencies
```bash
# Core requirements
pip install dxcam>=0.0.5 mss>=9.0.1 numpy>=1.24.0 pillow>=10.0.0

# Or install từ requirements file
pip install -r requirements-desktop-control.txt
```

### Platform Requirements
- **Windows 10/11** (DXGI requires Windows)
- **Python 3.11+**
- **Administrator privileges** (recommended cho best performance)

## 🎮 Sử dụng nhanh

### Basic Input Control
```python
from zeta_vn.data.implementations.input_control_fast import TurboInputControl, VK

# Khởi tạo
input_ctrl = TurboInputControl()

# Mouse operations
input_ctrl.move_to(100, 100)        # Move to absolute position
input_ctrl.click("left")            # Click
input_ctrl.scroll(120)              # Scroll up

# Keyboard operations  
input_ctrl.tap(VK.SPACE)           # Single key
input_ctrl.hotkey(VK.CTRL, VK.C)   # Hotkey combination

# Priority boost cho performance
input_ctrl.boost_priority()
```

### Screen Capture
```python
from zeta_vn.data.implementations.screen_capture_dxgi import ScreenCapture

# Context manager (recommended)
with ScreenCapture(target_fps=120) as cap:
    cap.start()
    frame = cap.frame()  # Numpy array (H, W, 3) BGR format
    
# Manual control
cap = ScreenCapture(method="dxgi", monitor=0)
cap.start()
try:
    for _ in range(100):
        frame = cap.frame()
        # Process frame...
finally:
    cap.stop()
```

### Target Finding
```python
from zeta_vn.data.implementations.screen_targeting import TargetFinder

# Tìm pixel màu xanh lá
finder = TargetFinder(color_bgr=(0, 255, 0), tol=20)

with ScreenCapture() as cap:
    cap.start()
    frame = cap.frame()
    
    target = finder.locate(frame)
    if target:
        x, y = target
        print(f"Found green pixel at ({x}, {y})")
```

### Integrated Control
```python
from zeta_vn.data.implementations.screen_control_manager import ScreenControlManager

# Auto-click trên green pixels
manager = ScreenControlManager(color_bgr=(0, 255, 0), tolerance=30)

# Single operation
with manager:
    latency_ms = manager.run_once() * 1000
    print(f"Pipeline latency: {latency_ms:.2f}ms")

# Continuous operation với stats
with manager:
    stats = manager.run_continuous(duration=10.0, target_loop_rate=100.0)
    print(f"Hit rate: {stats['target_hit_rate']:.2%}")
    print(f"Avg latency: {stats['avg_latency_ms']:.2f}ms")
```

### Performance Monitoring
```python
from zeta_vn.data.instrumentation.latency_timer import Timer

# Measure operation latency
with Timer("mouse_click") as timer:
    input_ctrl.click("left")

print(f"Click took {timer.ms:.2f}ms")
```

## 🚦 Performance Targets

| Operation | Target Latency | Achieved |
|-----------|---------------|----------|
| Mouse Move | < 2ms | ✅ |
| Mouse Click | < 5ms | ✅ |
| Key Press | < 3ms | ✅ |
| DXGI Capture | < 8.33ms (120 FPS) | ✅ |
| Color Finding | < 1ms | ✅ |
| Full Pipeline | < 10ms | ✅ |

## 🧪 Testing & Benchmarks

### Demo Script
```bash
python scripts/demo_fast_control.py
```

Chạy comprehensive demo với tất cả tính năng:
- Input control demonstrations
- Screen capture performance tests  
- Target finding examples
- Integrated pipeline demo
- Latency measurements
- Priority boost impact

### Performance Benchmarks
```bash
python scripts/benchmark_fast_control.py
```

Chạy performance benchmarks với:
- Input operation benchmarks (1000+ iterations)
- Screen capture performance tests
- Target finding speed tests
- Full pipeline latency measurements
- Priority boost impact analysis
- Performance score calculation

## ⚙️ Configuration

### Screen Capture Options
```python
# DXGI capture (fastest)
cap = ScreenCapture(
    method="dxgi",        # "dxgi" or "mss"
    monitor=0,            # Monitor index
    target_fps=120,       # Target FPS
    region=None           # (x, y, w, h) or None for full screen
)

# MSS capture (fallback)
cap = ScreenCapture(method="mss", target_fps=60)
```

### Input Control Options
```python
input_ctrl = TurboInputControl(
    move_duration=0,      # Mouse move duration (0 = instant)
    click_duration=0.01,  # Click hold duration
    key_duration=0.01     # Key press duration
)
```

### Target Finding Options
```python
finder = TargetFinder(
    color_bgr=(0, 255, 0),    # Target color in BGR
    tol=20,                   # Color tolerance (0-255)
    region=None               # Search region (x, y, w, h)
)
```

## 🔧 Optimization Tips

### Performance Optimization
1. **Run as Administrator** cho unrestricted API access
2. **Boost process priority** với `input_ctrl.boost_priority()`
3. **Use DXGI capture** thay vì MSS
4. **Close unnecessary applications** để giảm system load
5. **Use appropriate FPS targets** (120 cho gaming, 60 cho general use)

### Memory Optimization
1. **Use context managers** để auto-cleanup
2. **Reuse TargetFinder instances** cho same color
3. **Limit capture resolution** nếu không cần full screen
4. **Call gc.collect()** periodically trong long-running loops

### Latency Optimization
1. **Minimize processing** giữa capture và action
2. **Use batch operations** cho multiple inputs
3. **Avoid unnecessary memory copies**
4. **Use absolute coordinates** instead of relative

## 🐛 Troubleshooting

### Common Issues

**DXGI Capture Fails**
```
Solution: Fallback sẽ tự động chuyển sang MSS
Check: GPU drivers updated, Windows 10+ requirement
```

**High Input Latency**
```
Solution: Run as Administrator, boost priority
Check: Antivirus software conflicts, system load
```

**Target Not Found**  
```
Solution: Adjust color tolerance, check BGR vs RGB
Check: Screen scaling settings, color accuracy
```

**Memory Usage High**
```
Solution: Use context managers, reduce FPS target
Check: Long-running capture sessions, memory leaks
```

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Performance profiling
from zeta_vn.data.implementations.screen_capture_dxgi import benchmark_capture
results = benchmark_capture(duration=5.0)
print(f"Capture performance: {results['fps']:.1f} FPS")
```

## 📚 API Reference

### TurboInputControl
- `move_to(x, y)` - Move mouse to absolute coordinates
- `click(button)` - Click mouse button ("left", "right", "middle")
- `tap(vk_code)` - Press single key using VK code
- `hotkey(*vk_codes)` - Press key combination
- `scroll(delta)` - Scroll mouse wheel
- `boost_priority()` - Boost process priority

### ScreenCapture
- `start()` - Start capture thread
- `stop()` - Stop capture thread  
- `frame()` - Get latest frame (numpy array)
- `fps()` - Get current FPS
- Context manager support

### TargetFinder
- `locate(frame)` - Find target in frame, returns (x, y) or None
- `locate_all(frame)` - Find all targets (planned)
- `set_color(color_bgr)` - Change target color
- `set_tolerance(tol)` - Change color tolerance

### ScreenControlManager
- `run_once()` - Single capture-detect-click cycle
- `run_continuous(duration, target_loop_rate)` - Continuous operation với stats
- Context manager support
- Performance statistics tracking

## 🎯 Use Cases

### Gaming Automation
```python
# Auto-click on health potions (red pixels)
manager = ScreenControlManager(color_bgr=(0, 0, 255), tolerance=10)
with manager:
    stats = manager.run_continuous(duration=60.0, target_loop_rate=200.0)
```

### UI Testing
```python
# Click on specific UI elements
input_ctrl = TurboInputControl()
with ScreenCapture() as cap:
    cap.start()
    frame = cap.frame()
    
    button_finder = TargetFinder(color_bgr=(100, 200, 50))  # Button color
    button_pos = button_finder.locate(frame)
    if button_pos:
        input_ctrl.move_to(*button_pos)
        input_ctrl.click("left")
```

### Performance Monitoring
```python
# Monitor system responsiveness
from zeta_vn.data.instrumentation.latency_timer import Timer

operations = []
for _ in range(100):
    with Timer() as t:
        input_ctrl.move_to(500, 500)
    operations.append(t.ms)

avg_latency = sum(operations) / len(operations)
print(f"Average input latency: {avg_latency:.2f}ms")
```

## 🛡️ Security Notes

- **Administrator privileges** required cho full performance
- **Input simulation** có thể trigger antivirus warnings
- **Screen capture** requires appropriate permissions
- **Use responsibly** - respect application ToS and legal requirements

## 🔄 Version History

- **v1.0.0** - Initial release với core functionality
  - Win32 input control implementation
  - DXGI screen capture support
  - Basic color targeting
  - Integrated control manager
  - Performance benchmarking tools

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Add tests cho new functionality  
4. Run benchmark suite
5. Submit pull request

## 📄 License

Tuân theo license của main project (ZETA_VN).

---

**⚡ Ultra-Fast Desktop Control Pack - Making Windows automation lightning fast!**
