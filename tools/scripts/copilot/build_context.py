from __future__ import annotations

from pathlib import Path
import Exception
import dir_name
import e
import f
import item
import len
import list
import name
import print
import sorted
import str

"""
Copilot Context Builder - Tạo COPILOT_CONTEXT.md để hướng dẫn Copilot hiểu repo
"""
GOALS = """# COPILOT_CONTEXT
- Clean code chuẩn PEP8/TS strict, không trùng lặp.
- Tính năng phụ dùng decorator/middleware.
- Gate hiệu năng: Startup < 3s, RAM < 300MB, Task nhỏ < 100ms.
1) Kiểm tra file/tính năng đã tồn tại trước khi tạo mới.
2) Không dùng star-import; import tường minh.
3) Không ghi secret/PII vào log; mask ngay tại boundary.
4) Ưu tiên cấu trúc Clean Architecture + DDD; không lệch tầng.
5) Frontend: HashRouter + Vite base "./"; không dùng <a href>.
6) Backend: FastAPI + Pydantic v2; schema tách create/update/response; WS events typed.
- Coverage ≥ 80%; Ruff/Mypy strict; ESLint/TS strict.
- No circular deps; No dead code/excess exports.
- jscpd clone rate < 2%.
```
zeta_vn/
├── app/                 # FastAPI application layer
│   ├── api/            # REST/GraphQL endpoints
│   ├── worker/         # Celery/background tasks
│   └── main.py         # Application entry point
├── core/               # Domain/business logic
│   ├── domain/         # Entities, value objects
│   ├── use_cases/      # Application services
│   └── services/       # Domain services
├── data/               # Infrastructure/persistence
│   ├── repositories/   # Data access
│   └── models/         # SQLAlchemy models
└── config/             # Configuration
```
```
desktop_ai_zeta/
├── src/
│   ├── components/     # React components
│   ├── services/       # API clients
│   ├── hooks/          # Custom hooks
│   └── types/          # TypeScript definitions
├── electron/           # Electron main process
└── config/             # Build configuration
```
- **Startup**: <3s (FastAPI ready + health check)
- **Memory**: <300MB RSS (production load)
- **Response**: <100ms (simple CRUD operations)
- **Build**: <60s (full TypeScript compilation)
- **Formatting**: ruff format (100 char line length)
- **Linting**: ruff check --fix (PEP8 + import order)
- **Types**: mypy --strict (100% coverage)
- **Tests**: pytest --cov ≥80%
- **Security**: bandit + pip-audit (zero high/critical)
- **Formatting**: prettier (consistent style)
- **Linting**: eslint --fix (strict rules)
- **Types**: tsc --noEmit --strict
- **Tests**: vitest --coverage ≥80%
- **Dependencies**: depcheck + ts-prune (no unused)
- Star imports (`from module import *`)
- Circular dependencies
- God classes/functions (>100 lines)
- Hardcoded secrets/URLs
- Untyped any usage
- Dead code/unused exports
- Code duplication >2%
"""


def read_if_exists(p: Path) -> str:
    """Đọc file nếu tồn tại, giới hạn kích thước"""
    if not p.exists():
        return ""
    try:
        content = p.read_text(encoding="utf-8")
        return content[:15000] + ("..." if len(content) > 15000 else "")
    except Exception:
        return ""


def main():
    """Build comprehensive Copilot context"""
    root = Path(".")
    doc_files = [
        ".github/prompts/PROJECT_MAP.md",
        ".github/prompts/GUIDE.md",
        ".github/prompts/CREATE_OR_UPDATE_FILE.md",
        "README.md",
        "ARCHITECTURE_EVOLUTION.md",
        "GRAPHQL_OPTIMIZATION_SUCCESS_REPORT.md",
        "UPGRADE_SYSTEM_SUCCESS_REPORT.md",
    ]
    extras = []
    for name in doc_files:
        p = Path(name)
        if p.exists():
            content = read_if_exists(p)
            if content:
                extras.append(f"\n---\n# {name}\n\n{content}")
    project_structure = generate_project_structure(root)
    if project_structure:
        extras.append(f"\n---\n# Current Project Structure\n\n```\n{project_structure}\n```")
    quality_stats = generate_quality_stats(root)
    if quality_stats:
        extras.append(f"\n---\n# Code Quality Status\n\n{quality_stats}")
    output_path = Path("COPILOT_CONTEXT.md")
    final_content = GOALS + "".join(extras)
    output_path.write_text(final_content, encoding="utf-8")
    print(f"✅ Generated {output_path} ({len(final_content):,} chars)")
    print(f"📁 Included {len([e for e in extras if 'PROJECT_MAP' in e or 'README' in e])} documentation files")
    print(f"📊 Context size: {len(final_content) // 1024}KB")


def generate_project_structure(root: Path) -> str:
    """Tạo cấu trúc dự án tóm tắt"""
    try:
        important_dirs = ["zeta_vn", "desktop_ai_zeta", "scripts", ".github"]
        structure_lines = []
        for dir_name in important_dirs:
            dir_path = root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                structure_lines.append(f"{dir_name}/")
                for item in sorted(dir_path.iterdir())[:10]:
                    if item.is_dir() and not item.name.startswith("."):
                        structure_lines.append(f"  {item.name}/")
        return "\n".join(structure_lines)
    except Exception:
        return ""


def generate_quality_stats(root: Path) -> str:
    """Tạo thống kê chất lượng code hiện tại"""
    try:
        stats = []
        py_files = list(Path("zeta_vn").rglob("*.py")) if Path("zeta_vn").exists() else []
        if py_files:
            stats.append(f"- Python files: {len(py_files)}")
        ts_files = list(Path("desktop_ai_zeta/src").rglob("*.ts*")) if Path("desktop_ai_zeta/src").exists() else []
        if ts_files:
            stats.append(f"- TypeScript files: {len(ts_files)}")
        config_files = ["pyproject.toml", "package.json", "tsconfig.json", ".ruff.toml"]
        present_configs = [f for f in config_files if Path(f).exists() or Path(f"desktop_ai_zeta/{f}").exists()]
        if present_configs:
            stats.append(f"- Config files: {', '.join(present_configs)}")
        return "\n".join(stats) if stats else ""
    except Exception:
        return ""


if __name__ == "__main__":
    main()
