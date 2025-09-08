# NumPy Compatibility Release Checklist

> **Last Updated**: September 9, 2025  
> **Version**: v0.1.0 NumPy Compatibility Pack

## ✅ Pre-Release Validation

### 1. Environment Setup
- [ ] Clean environment: `uv cache clean`
- [ ] NP1 install: `cd apps/backend && uv sync --extra dev --extra ocr`
- [ ] NP2 test: `cd apps/backend && python ../../switch_numpy.py np2`
- [ ] Verify no conflicts: `uv lock --upgrade && uv check`

### 2. Runtime Validation
```bash
# Kiểm tra NP1 (production)
cd apps/backend
uv run python ../../scripts/assert_numpy_runtime.py

# Kiểm tra NP2 (future testing)
ZETA_NUMPY_PROFILE=np2 uv run python ../../scripts/assert_numpy_runtime.py

# Cross-check compatibility
uv run python -c "from app.compat.startup_check import report; print(report())"
```

### 3. Test Matrix
- [ ] NP1 tests pass: `uv run pytest tests/compat/ -v`
- [ ] Basic imports: `uv run python -c "import numpy, torch, faiss, cv2; print('OK')"`
- [ ] Nightly CI configured và active
- [ ] Manual trigger test: workflow_dispatch works

### 4. Documentation Check
- [ ] README cập nhật với NumPy compatibility info
- [ ] `NUMPY_COMPATIBILITY_GUIDE.md` accurate
- [ ] Release notes prepared
- [ ] API compatibility documented

## 🚀 Release Steps

### 1. Version & Tagging
```bash
# Bump version
git add scripts/ tests/ .github/ docs/
git commit -m "feat: NumPy compatibility pack with nightly monitoring"

# Tag release
git tag -a v0.1.0 -m "NP1 stable + NP2 infrastructure + nightly monitoring"
git push origin main --tags
```

### 2. GitHub Release
- [ ] Create GitHub release from tag v0.1.0
- [ ] Upload artifacts: compatibility reports, test results
- [ ] Release notes include:
  - NumPy 1.x stable confirmation
  - NumPy 2.x infrastructure ready
  - Migration timeline
  - Breaking changes (none expected)

### 3. Monitoring Setup
- [ ] Enable nightly workflow: `.github/workflows/numpy-compat-nightly.yml`
- [ ] Setup notifications cho workflow failures
- [ ] Configure artifact retention (30 days)
- [ ] Create tracking issue cho NP2 ecosystem progress

## 📊 Post-Release Monitoring

### Daily Checks (Automated)
- [ ] Nightly CI status → GitHub Actions
- [ ] NP1 baseline → should always pass
- [ ] NP2 progress → expected to improve over time
- [ ] Dependency security alerts → Dependabot

### Weekly Reviews (Manual)
- [ ] Review NP2 compatibility reports
- [ ] Check upstream library updates:
  - `faiss-cpu` NP2 support progress
  - `torch` compatibility improvements
  - `opencv-python` wheel updates
  - `paddleocr` NumPy 2.x readiness

### NP2 Transition Readiness Criteria
- [ ] **Week 1-2**: NP2 nightly passes basic imports
- [ ] **Week 3-4**: NP2 nightly passes core functionality tests  
- [ ] **Week 5-6**: NP2 passes full test suite
- [ ] **Week 7-8**: NP2 performance benchmarks acceptable
- [ ] **Week 9+**: Production rollout decision

## 🆘 Troubleshooting Guide

### Common NP2 Issues (Expected)
| Issue | Likely Cause | Workaround | Tracking |
|-------|--------------|------------|----------|
| FAISS import fails | No NP2 wheels | Use CPU-only FAISS | [faiss#3190](https://github.com/facebookresearch/faiss/issues/3190) |
| PyTorch warnings | Version mismatch | Upgrade torch>=2.4 | [pytorch#110436](https://github.com/pytorch/pytorch/issues/110436) |
| OpenCV crashes | ABI incompatibility | Use opencv-python-headless | [opencv#871](https://github.com/opencv/opencv-python/issues/871) |
| PaddleOCR fails | NumPy API changes | Switch to pytesseract | Internal |

### Rollback Procedure
```bash
# Emergency rollback
cd apps/backend
git checkout v0.0.9  # previous stable tag
uv sync --extra dev --extra ocr
uv run python ../../scripts/assert_numpy_runtime.py  # verify

# Disable NP2 testing temporarily
git checkout main
# Comment out np2-nightly job in .github/workflows/
git commit -m "temporarily disable NP2 nightly"
```

### Performance Regression Detection
```bash
# Benchmark key operations
cd apps/backend
uv run python -c "
import time
import numpy as np

# RAG embedding benchmark
start = time.time()
embeddings = np.random.rand(1000, 768)
similarity = np.dot(embeddings, embeddings.T)
end = time.time()
print(f'Embedding ops: {end-start:.3f}s')

# Should be < 0.1s for 1000x768 on modern hardware
assert end-start < 0.5, 'Performance regression detected'
print('✅ Performance OK')
"
```

## 🎯 Success Metrics

### Release Goals (v0.1.0)
- [x] **Stability**: NumPy 1.x production-ready
- [x] **Infrastructure**: NP2 testing framework
- [x] **Monitoring**: Nightly compatibility checks
- [x] **Documentation**: Complete migration guide
- [x] **Zero downtime**: No breaking changes

### Future Milestones
- [ ] **v0.2.0**: NP2 opt-in ready (when ecosystem 80% compatible)
- [ ] **v0.3.0**: NP2 recommended (when ecosystem 95% compatible)
- [ ] **v1.0.0**: NP1 deprecated, NP2 default

### KPIs to Track
- NP1 nightly success rate: **Target 100%**
- NP2 nightly progress: **Track improvement over time**
- Production error rate: **Target <0.1%**
- Developer satisfaction: **Survey quarterly**

## 📋 Release Communication

### Internal Team
- [ ] Engineering team notified of NP1 stability
- [ ] DevOps team aware of CI changes
- [ ] QA team has test procedures
- [ ] Product team updated on timeline

### External Communication
- [ ] Community update on NumPy 2.x readiness
- [ ] Documentation site updated
- [ ] Social media announcement (if applicable)
- [ ] Dependency consumers notified

---

## ✅ Final Checklist

**Before tagging v0.1.0:**
- [ ] All tests pass
- [ ] Runtime validation clean
- [ ] Documentation reviewed
- [ ] CI workflows tested
- [ ] Team approval received

**After release:**
- [ ] Monitor first 24h for issues
- [ ] Verify nightly jobs running
- [ ] Update project roadmap
- [ ] Plan next milestone

---

**Release Manager**: _[Your Name]_  
**Release Date**: _[Target Date]_  
**Approval**: _[Stakeholder Sign-off]_