# Pre-commit Installation Guide for Zeta AI Server

## 🚀 Quick Setup

### 1. Install pre-commit
```bash
pip install pre-commit
```

### 2. Install hooks in your repository
```bash
cd /path/to/zeta
pre-commit install
```

### 3. Test on all files (optional)
```bash
pre-commit run --all-files
```

## 🔧 What happens on each commit?

### Automatic Checks:
1. **🔍 Ruff Linter** - Code quality & style
2. **🎨 Ruff Formatter** - Code formatting
3. **🏷️ MyPy** - Static type checking
4. **🛡️ Bandit** - Security vulnerability scan
5. **📝 Import Sorting** - Organize imports
6. **✨ Code Cleanup** - Trailing whitespace, end-of-file fixes

### On Commit Failure:
- ❌ Commit is **blocked**
- 🔧 Auto-fixable issues are **automatically fixed**
- 📝 Manual fixes required for remaining issues
- ✅ Re-commit after fixes

## 📊 GitHub Actions CI/CD

### Triggers:
- 📤 Push to `main` or `develop`
- 🔄 Pull Requests to `main` or `develop`
- 🎯 Manual workflow dispatch

### Pipeline Jobs:

#### 1. 🔍 **Lint & Type Check**
- Ruff linting
- Ruff formatting validation
- MyPy type checking
- Reports added to PR

#### 2. 🔒 **Security Scan**
- Bandit security analysis
- Safety dependency check
- Security reports uploaded

#### 3. 🧪 **Tests**
- Unit tests with coverage
- Integration tests
- Coverage reports to Codecov

#### 4. 🏗️ **Build & Docker**
- Docker image build test
- Dockerfile validation

#### 5. 🏛️ **Architecture Check**
- Clean Architecture compliance
- Code complexity analysis
- Dead code detection

#### 6. 🚀 **Deployment Readiness**
- Final validation (main branch only)
- Deployment status summary

## 💡 Developer Workflow

### Normal Development:
```bash
# Make changes
git add .
git commit -m "feat: add new feature"
# ✅ Pre-commit hooks run automatically
git push
```

### Bypass Hooks (Emergency Only):
```bash
git commit -m "hotfix: urgent fix" --no-verify
```

### Manual Hook Run:
```bash
# Run specific hook
pre-commit run ruff --all-files

# Run all hooks
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

## 🎯 Benefits

### ✅ **Quality Assurance**
- Consistent code style across team
- Early bug detection
- Security vulnerability prevention
- Type safety enforcement

### ⚡ **Developer Experience**
- Fast feedback loop
- Automated fixes
- Clear error messages
- No manual tool running

### 🚀 **CI/CD Integration**
- Fail fast on quality issues
- Detailed reports in PRs
- Deployment readiness validation
- Automated security scanning

## 🔧 Customization

### Skip Specific Hooks:
```bash
SKIP=mypy git commit -m "skip mypy for this commit"
```

### Modify Hook Configuration:
Edit `.pre-commit-config.yaml`:
```yaml
- id: ruff
  args: [--fix, --ignore=E501]  # Ignore line length
```

### Add Custom Hooks:
```yaml
- repo: local
  hooks:
    - id: custom-check
      name: Custom Project Check
      entry: python tools/custom_check.py
      language: system
```

## 📈 Monitoring

### GitHub Actions Dashboard:
- Monitor build success rates
- Track test coverage trends
- Security scan results
- Performance metrics

### Pre-commit Analytics:
```bash
# Check hook performance
pre-commit run --verbose --all-files

# See what would run
pre-commit run --dry-run --all-files
```

---

🎉 **With this setup, every commit is automatically validated for quality, security, and architecture compliance!**
