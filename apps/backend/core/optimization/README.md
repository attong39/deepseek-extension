# 🚀 **PHASE 5: CODE QUALITY FIXES & PERFORMANCE OPTIMIZATION**

## 🎯 **Trạng Thái Hiện Tại**
- ✅ **Phase 4 (Monitoring)**: Hoàn thành - Enterprise-grade monitoring system
- ❌ **Code Quality**: 2153 lỗi ruff (F821/F822 undefined names)
- ❌ **Performance**: Chưa optimize theo roadmap

## 🔥 **Phase 5A: Critical Code Quality Fixes (Tuần 1)**

### **Vấn đề chính:**
- **2153 lỗi F821/F822**: Undefined variables trong tests và __all__
- **Import errors**: Missing imports trong __init__.py files
- **Test failures**: Broken test cases do undefined variables

### **Giải pháp:**

#### 1. **Fix Undefined Variables trong Tests**
```python
# BEFORE: zeta_vn/tests/unit/test_specifications.py
def test_agent_name_specification():
    # ❌ Missing variable definitions
    assert spec.is_satisfied_by(valid_agent)  # valid_agent undefined

# AFTER: Fix với proper fixtures
@pytest.fixture
def valid_agent():
    return Agent(name="ValidAgent", description="Test")

def test_agent_name_specification(valid_agent):
    assert spec.is_satisfied_by(valid_agent)  # ✅ Now defined
```

#### 2. **Fix __all__ Declarations**
```python
# BEFORE: zeta_vn/tests/unit/test_permission_service.py
__all__ = [
    "test_create_role",  # ❌ Undefined
    "user_id",           # ❌ Undefined
]

# AFTER: Only export what actually exists
__all__ = [
    "TestPermissionService",  # ✅ Class exists
    # Remove undefined items
]
```

#### 3. **Automated Fix Script**
```python
# NEW: tools/fix_undefined_variables.py
"""Auto-fix undefined variables in tests and __all__"""

import ast
import os
from pathlib import Path

def fix_undefined_variables():
    """Fix F821/F822 errors automatically"""
    test_files = Path("zeta_vn/tests").rglob("*.py")

    for file_path in test_files:
        fix_file_undefined_vars(file_path)

def fix_file_undefined_vars(file_path: Path):
    """Fix undefined variables in single file"""
    content = file_path.read_text()

    # Parse AST to find undefined names
    tree = ast.parse(content)

    # Find all undefined names in __all__
    undefined_in_all = find_undefined_in_all(tree, content)

    # Remove undefined items from __all__
    if undefined_in_all:
        content = remove_undefined_from_all(content, undefined_in_all)

    # Add missing fixtures for undefined test variables
    undefined_vars = find_undefined_test_vars(tree, content)
    if undefined_vars:
        content = add_missing_fixtures(content, undefined_vars)

    file_path.write_text(content)

# ... implementation details
```

## 🚀 **Phase 5B: Performance Optimization (Tuần 2)**

### **Mục tiêu:**
- **Startup Time**: `< 3 giây` (hiện tại ~8-12s)
- **Memory Usage**: `< 300MB` (hiện tại ~600-800MB)
- **Task Processing**: `< 100ms` (hiện tại ~300-500ms)

### **Implementation Plan:**

#### 1. **Lazy Import System**
```python
# NEW: zeta_vn/core/optimization/lazy_loader.py
"""Lazy loading system for < 3s startup"""

import importlib
from typing import Dict, Any, Callable

class LazyLoader:
    """Lazy module loader with caching"""

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._loaders: Dict[str, Callable] = {}

    def register_lazy_import(self, name: str, loader: Callable):
        """Register lazy import"""
        self._loaders[name] = loader

    def __getattr__(self, name: str) -> Any:
        if name in self._cache:
            return self._cache[name]

        if name in self._loaders:
            self._cache[name] = self._loaders[name]()
            return self._cache[name]

        raise AttributeError(f"LazyLoader has no attribute '{name}'")

# Usage in __init__.py
_lazy_loader = LazyLoader()

_lazy_loader.register_lazy_import(
    "create_app",
    lambda: importlib.import_module("zeta_vn.app.factory").create_app
)

def __getattr__(name: str):
    return getattr(_lazy_loader, name)
```

#### 2. **Memory Optimization**
```python
# NEW: zeta_vn/core/optimization/memory_optimizer.py
"""Memory optimization for < 300MB target"""

import gc
import psutil
from weakref import WeakValueDictionary

class MemoryOptimizer:
    """Intelligent memory management"""

    def __init__(self, target_mb: int = 300):
        self.target_bytes = target_mb * 1024 * 1024
        self._object_cache = WeakValueDictionary()

    def optimize_memory(self) -> Dict[str, Any]:
        """Run memory optimization"""
        # Force garbage collection
        collected = gc.collect()

        # Clear weak references
        self._object_cache.clear()

        # Check current memory
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            "collected_objects": collected,
            "current_mb": memory_info.rss / 1024 / 1024,
            "target_mb": self.target_bytes / 1024 / 1024,
            "within_target": memory_info.rss < self.target_bytes
        }

    def monitor_memory_usage(self) -> Dict[str, Any]:
        """Real-time memory monitoring"""
        process = psutil.Process()
        memory_info = process.memory_info()

        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "cpu_percent": process.cpu_percent(interval=1),
            "within_target": memory_info.rss < self.target_bytes
        }
```

#### 3. **Task Performance Optimizer**
```python
# NEW: zeta_vn/core/optimization/task_optimizer.py
"""Task performance optimization for < 100ms target"""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Dict, Any, List

class TaskOptimizer:
    """High-performance task processing"""

    def __init__(self, target_ms: int = 100):
        self.target_seconds = target_ms / 1000
        self._metrics: Dict[str, List[float]] = {}

    @asynccontextmanager
    async def timed_execution(self, task_name: str):
        """Time execution with automatic optimization"""
        start_time = time.perf_counter()

        try:
            yield
        finally:
            duration = time.perf_counter() - start_time
            self._record_metric(task_name, duration)

            if duration > self.target_seconds:
                await self._optimize_slow_task(task_name, duration)

    def _record_metric(self, task_name: str, duration: float):
        """Record performance metrics"""
        if task_name not in self._metrics:
            self._metrics[task_name] = []

        metrics = self._metrics[task_name]
        metrics.append(duration)

        # Keep last 100 measurements
        if len(metrics) > 100:
            metrics.pop(0)

    async def _optimize_slow_task(self, task_name: str, duration: float):
        """Auto-optimize slow tasks"""
        print(f"⚠️ Slow task: {task_name} took {duration*1000:.1f}ms")

        # Trigger optimizations:
        # - Cache warming
        # - Connection pool scaling
        # - Async batching
        # - Circuit breaker

    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance summary"""
        report = {}

        for task_name, durations in self._metrics.items():
            if durations:
                avg_duration = sum(durations) / len(durations)
                max_duration = max(durations)

                report[task_name] = {
                    "avg_ms": avg_duration * 1000,
                    "max_ms": max_duration * 1000,
                    "within_target": avg_duration < self.target_seconds,
                    "sample_count": len(durations)
                }

        return report
```

## 📊 **Implementation Roadmap**

### **Week 1: Code Quality Fixes**
1. **Day 1-2**: Fix undefined variables (F821/F822)
   - Run automated fix script
   - Manual review of critical files
   - Update test fixtures

2. **Day 3-4**: Fix import errors
   - Clean up __init__.py files
   - Add missing imports
   - Remove circular dependencies

3. **Day 5-7**: Quality validation
   - Run full test suite
   - Performance baseline measurement
   - Documentation updates

### **Week 2: Performance Optimization**
1. **Day 1-2**: Lazy loading implementation
   - Create lazy loader system
   - Update __init__.py files
   - Test startup time improvement

2. **Day 3-4**: Memory optimization
   - Implement memory optimizer
   - Add garbage collection tuning
   - Monitor memory usage

3. **Day 5-7**: Task optimization
   - Implement task optimizer
   - Add performance monitoring
   - Fine-tune for < 100ms target

## 🎯 **Success Metrics**

| Metric        | Target  | Current    | Expected After |
| ------------- | ------- | ---------- | -------------- |
| Ruff Errors   | 0       | 2153       | 0              |
| Startup Time  | < 3s    | ~8-12s     | < 3s           |
| Memory Usage  | < 300MB | ~600-800MB | < 300MB        |
| Task Time     | < 100ms | ~300-500ms | < 100ms        |
| Test Coverage | > 90%   | ~70%       | > 90%          |

## 🚀 **Next Steps**

1. **Immediate**: Chạy automated fix script
2. **Today**: Fix critical undefined variables
3. **This Week**: Implement lazy loading
4. **Next Week**: Memory & task optimization

---

**🎉 Expected Result**: Clean, fast, maintainable codebase meeting all performance targets!</content>
<parameter name="filePath">e:\zeta\PHASE5_OPTIMIZATION_ROADMAP.md
