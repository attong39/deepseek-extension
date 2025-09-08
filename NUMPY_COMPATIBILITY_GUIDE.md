# NumPy 2.x Compatibility Guide

## 🎯 Mục tiêu
- **Deploy ngay**: NumPy 1.x (default) cho production ổn định
- **Test future**: NumPy 2.x (np2 profile) cho compatibility testing  
- **Không phá pipeline**: Tất cả lệnh hiện tại vẫn hoạt động bình thường
- **CI matrix**: Test song song cả NumPy 1.x và 2.x

## 🚀 Quick Start

### Production (NumPy 1.x - Recommended)
```bash
cd apps/backend
uv sync --extra dev --extra ocr
```

### Future Testing (NumPy 2.x)
```bash
cd apps/backend
uv sync --extra dev --extra np2
```

### Windows OCR Fallback
```bash
cd apps/backend
uv add --optional ocr-alt pytesseract pillow
```

## 🔍 Version Check
```bash
cd apps/backend
uv run python -c "
import numpy, torch, cv2, faiss
print(f'NumPy: {numpy.__version__}')
print(f'PyTorch: {torch.__version__}')
print(f'OpenCV: {cv2.__version__}')
print(f'FAISS: {faiss.__version__}')
"
```

## 🧪 Compatibility Test
```bash
# Test NumPy 1.x (default)
python test_numpy_switch.py default

# Test NumPy 2.x 
python test_numpy_switch.py np2
```

## 📊 Startup Compatibility Logging
FastAPI app sẽ tự động log thông tin compatibility khi khởi động:

```python
# apps/backend/app/compat/startup_check.py
from app.compat.startup_check import report
compat_info = report()
# Output: {"numpy": "1.26.4", "faiss": "1.8.0", "warnings": [...]}
```

## 🔧 CI Matrix Testing

CI sẽ tự động test trên matrix:
- **OS**: Ubuntu, Windows
- **Python**: 3.10, 3.11, 3.12  
- **NumPy**: default (1.x), np2 (2.x)
- **Special**: Windows + OCR fallback

Xem: `.github/workflows/numpy-compatibility.yml`

## ⚠️ Known Issues & Solutions

### 1. FAISS + NumPy 2.x
**Problem**: FAISS chưa hỗ trợ NumPy 2.x đầy đủ
**Solution**: Sử dụng `faiss-cpu>=1.8.0` trong np2 profile

### 2. PaddleOCR + Windows
**Problem**: PaddleOCR khó compile trên Windows
**Solution**: Fallback `pytesseract` trong `ocr-alt` profile

### 3. PyTorch + NumPy 2.x  
**Problem**: PyTorch cũ không tương thích NumPy 2.x
**Solution**: Upgrade `torch>=2.4.0` trong np2 profile

## 📝 pyproject.toml Configuration

```toml
[project]
dependencies = [
    "numpy<2.0",          # Pin NumPy 1.x by default
    "faiss-cpu>=1.8.0",
    # ... other deps
]

[project.optional-dependencies]
# Production OCR (default)
ocr = [
    "paddleocr>=2.7.0",
    "opencv-python>=4.8.0",
]

# NumPy 2.x testing
np2 = [
    "numpy>=2.0,<3.0",
    "torch>=2.4.0",
    "faiss-cpu>=1.8.0",
    "paddleocr>=2.7.0",
    "opencv-python>=4.8.0",
]

# Windows OCR fallback  
ocr-alt = [
    "pytesseract>=0.3.10",
    "pillow>=10.0.0",
]
```

## 🎯 Usage Patterns

### Development
```bash
# Cài đặt mặc định (NumPy 1.x)
uv sync --extra dev --extra ocr

# Test với NumPy 2.x
uv sync --extra dev --extra np2

# Windows development
uv sync --extra dev --extra ocr-alt
```

### Production Deployment
```bash
# Recommended: NumPy 1.x cho stability
uv sync --extra ocr

# Future: Khi NumPy 2.x ecosystem stable
uv sync --extra np2
```

### CI/CD
CI sẽ tự động:
1. Test cả default và np2 profiles
2. Log compatibility matrix  
3. Upload artifacts cho debugging
4. Generate summary report

## 🚨 Migration Strategy

### Phase 1: Current (NumPy 1.x)
- ✅ Production stable với `numpy<2.0`
- ✅ CI test baseline với NumPy 1.x
- ✅ All existing commands work unchanged

### Phase 2: Dual Support (Both)  
- ✅ CI matrix test cả NumPy 1.x và 2.x
- ✅ Compatibility logging và monitoring
- ✅ Optional np2 profile cho early testing

### Phase 3: Future (NumPy 2.x)
- 🔜 Khi ecosystem fully supports NumPy 2.x
- 🔜 Switch default từ `numpy<2.0` sang `numpy>=2.0`
- 🔜 Maintain np1 profile cho legacy compatibility

## 🛠️ Troubleshooting

### Import Errors
```bash
# Check what's installed
uv run python -c "import sys; print(sys.path)"
uv show numpy faiss-cpu torch opencv-python

# Reinstall if needed
uv sync --reinstall --extra dev --extra np2
```

### Version Conflicts
```bash
# Check dependency tree
uv tree

# Force resolution
uv lock --upgrade
uv sync --extra dev --extra np2
```

### Windows Issues
```bash
# Use OCR fallback
uv sync --extra dev --extra ocr-alt

# Or manual install
uv add pytesseract pillow
```

## 📚 References

- [NumPy 2.0 Migration Guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
- [FAISS NumPy 2.0 Support](https://github.com/facebookresearch/faiss/issues/3190)
- [PyTorch NumPy 2.0 Compatibility](https://github.com/pytorch/pytorch/issues/110436)
- [OpenCV NumPy 2.0 Status](https://github.com/opencv/opencv-python/issues/871)

---

## ✅ Summary

**Hiện tại**: Mọi thứ hoạt động bình thường với NumPy 1.x
**Tương lai**: Sẵn sàng cho NumPy 2.x khi ecosystem stable  
**CI/CD**: Test matrix coverage cho cả 2 versions
**Deploy**: Zero breaking changes, smooth transition path