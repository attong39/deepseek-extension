# Pre-commit & CI Linting

## Cài đặt pre-commit

```powershell
pip install pre-commit
pre-commit install
# Chạy với toàn bộ file lần đầu
pre-commit run --all-files
```


## Hooks bao gồm

- pre-commit-hooks: check-yaml, end-of-file, trailing-whitespace
- ruff: check + format (tự fix)
- mypy: cho thư mục `zeta_vn/`
- bandit: security scan (`zeta_vn/`)
- local: prettier cho frontend
- local: gen-ws-types (nếu bạn muốn sinh TS từ WS schemas ở server)


## GitHub Actions (CI)

Workflow `lint.yml` sẽ tự chạy Ruff trên PR và nhánh `main`/`develop`.
