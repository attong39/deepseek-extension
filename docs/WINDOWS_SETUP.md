# ZETA_AI Development Setup - Windows PowerShell

Hướng dẫn cài đặt và chạy ZETA_AI trên Windows với PowerShell.

## 📋 Prerequisites

- Windows 10/11
- PowerShell 5.1+ (built-in) hoặc PowerShell 7+
- Node.js 20+ (tùy chọn nvm-windows)
- Docker Desktop (cho PostgreSQL)
- Git

## 🚀 Quick Start

> 💡 **Tip**: Để setup tự động, chạy `.\setup.ps1` thay vì làm thủ công từng bước!

### 1. Cài đặt Python và dependencies

```powershell
# Cài uv (Python package manager hiện đại)
iwr https://astral.sh/uv/install.ps1 -UseBasicParsing -OutFile uv.ps1; .\uv.ps1; Remove-Item uv.ps1

# Cài Python 3.11
uv python install 3.11

# Sync dependencies
uv sync --all-extras --dev
```

### 2. Cơ sở dữ liệu PostgreSQL

```powershell
# Chạy PostgreSQL với pgvector extension
docker run --rm -d --name zeta-pg `
  -e POSTGRES_PASSWORD=pass `
  -e POSTGRES_DB=zeta `
  -e POSTGRES_USER=postgres `
  -p 5432:5432 `
  pgvector/pgvector:pg16

# Kiểm tra PostgreSQL đã chạy
docker ps | findstr zeta-pg
```

### 3. Cấu hình môi trường

```powershell
# Tạo file .env
@"
# Database
DATABASE_URL=postgresql+asyncpg://postgres:pass@localhost:5432/zeta

# Server
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Outbox pattern
OUTBOX_WORKERS=2
OUTBOX_BATCH_SIZE=50

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-change-in-production

# AI/ML
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL=text-embedding-ada-002
"@ | Out-File -FilePath .env -Encoding UTF8
```

### 4. Database migration

```powershell
# Chạy migration
uv run alembic upgrade head

# (Tùy chọn) Seed data
uv run python scripts/seed_data.py
```

### 5. Desktop App Setup

```powershell
cd desktop_ai_zeta

# Cài Node.js dependencies
npm ci

# Generate API types từ server OpenAPI schema
npm run api:gen

cd ..
```

## 🏃‍♂️ Chạy Development

### Terminal 1: FastAPI Server

```powershell
# Chạy server với hot reload
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Hoặc chạy production mode
uv run uvicorn app.main_production:app --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Terminal 2: Electron Desktop App

```powershell
cd desktop_ai_zeta
npm run dev
```

Desktop app sẽ mở cửa sổ Electron.

### Terminal 3: Background Workers (tùy chọn)

```powershell
# Celery worker cho background tasks
uv run celery -A app.worker.celery_app worker -l info

# Celery beat cho scheduled tasks
uv run celery -A app.worker.celery_app beat -l info
```

## 🧪 Quality Checks

### Chạy toàn bộ quality gates

```powershell
# Master quality check
uv run python tools/master_quality_check.py

# Hoặc từng bước
uv run ruff check .
uv run ruff format .
uv run mypy --config-file mypy.ini .
uv run pytest -v --cov=app --cov=core --cov=data
```

### Pre-commit hooks

```powershell
# Cài pre-commit
uvx pre-commit install

# Chạy trên tất cả files
uvx pre-commit run --all-files
```

## 📱 VS Code Setup

### Extensions khuyến nghị

Cài các extensions trong `.vscode/extensions.json`:

```powershell
# Cài tất cả extensions khuyến nghị
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension ms-python.pytest
code --install-extension ms-python.mypy-type-checker
```

### Workspace settings

VS Code sẽ tự động load settings từ `.vscode/settings.json`.

## 🔧 Troubleshooting

### Lỗi thường gặp

1. **uv command not found**
   ```powershell
   # Restart PowerShell hoặc reload PATH
   $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
   ```

2. **PostgreSQL connection error**
   ```powershell
   # Kiểm tra Docker container
   docker logs zeta-pg

   # Restart container
   docker restart zeta-pg
   ```

3. **Import errors trong Python**
   ```powershell
   # Kiểm tra PYTHONPATH
   $env:PYTHONPATH = "$(pwd)\zeta_vn;$(pwd)\zeta_vn\app;$(pwd)\zeta_vn\core;$(pwd)\zeta_vn\data"
   ```

4. **Node.js version issues**
   ```powershell
   # Cài nvm-windows và switch version
   nvm install 20.10.0
   nvm use 20.10.0
   ```

### Performance tips

```powershell
# Bật Windows Developer Mode (optional)
# Settings > Update & Security > For developers > Developer Mode

# Exclude project folder từ Windows Defender
# Settings > Windows Security > Virus & threat protection > Exclusions
```

## 📚 Additional Commands

### Database management

```powershell
# Tạo migration mới
uv run alembic revision --autogenerate -m "Your migration message"

# Reset database
docker stop zeta-pg; docker rm zeta-pg
# Chạy lại database setup từ bước 2
```

### API client generation

```powershell
# Re-generate OpenAPI client cho apps/desktop
cd desktop_ai_zeta
npm run api:gen
cd ..
```

### Docker development

```powershell
# Build và chạy toàn bộ stack với Docker Compose
docker compose up --build

# Chỉ database
docker compose up postgres redis
```

## 🎯 Next Steps

1. Đọc `GUIDE.md` để hiểu kiến trúc
2. Xem `PROJECT_MAP.md` cho cấu trúc dự án
3. Check `README.md` cho thông tin chi tiết

## ✅ Quick Test

Sau khi setup xong, test nhanh:

```powershell
# Test server khởi động
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &
Start-Sleep -Seconds 5
curl http://127.0.0.1:8000/health

# Test quality tools
uv run ruff check --version
uv run mypy --version
uv run pytest --version

# Test database connection
uv run python -c "import asyncpg; print('asyncpg OK')"
```

Nếu tất cả commands trả về kết quả mà không có error → Setup thành công! 🎉

## 📞 Support

Nếu gặp vấn đề:
1. Check logs: `logs/` folder
2. Run health check: `curl http://localhost:8000/health`
3. Check GitHub Issues
4. Review troubleshooting section above

## ⏱️ Setup Time

**Total setup time: ~5-10 phút** (tùy internet speed) 🚀

- Python + uv installation: ~2-3 phút
- Dependencies sync: ~2-3 phút
- Docker PostgreSQL: ~1-2 phút
- Desktop npm install: ~1-2 phút

*Lần đầu sẽ lâu hơn do cần download Docker images và Python packages.*

---

Happy coding! 🚀
