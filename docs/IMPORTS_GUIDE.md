# IMPORTS_GUIDE — Chuẩn hoá import cho Server (Python) & Desktop (Electron/React)

Mục tiêu: chuẩn hoá import để rõ ràng, nhất quán, tránh vòng lặp, dễ mở rộng plugin và giúp Copilot/IDE tự đề xuất chính xác.

Ngôn ngữ: hướng dẫn bằng tiếng Việt; đoạn code/biến vẫn giữ tiếng Anh.

## Checklist nhanh

* [ ] Server & Shared dùng `src` layout và đã `uv pip install -e .` (editable install)
* [ ] Mọi import Python là absolute, theo layering
* [ ] `__init__.py` xác định public API rõ ràng (`__all__` / re-exports có kiểm soát)
* [ ] `import-linter` pass (không vi phạm layers)
* [ ] Desktop có `tsconfig` path alias và ESLint `import/order`
* [ ] Types TS generate từ OpenAPI và cập nhật tự động trong CI


## 1) Nguyên tắc vàng

* Dùng absolute imports theo tầng; tránh `..` lồng nhiều cấp.
* Áp dụng `src-layout` + editable install (PEP 517/518) — không dùng `PYTHONPATH` thủ công.
* Tách public API bằng `__init__.py` + `__all__` (re-export có kiểm soát).
* Chống vòng lặp import bằng layering: `domain → services/usecases → adapters → api`.
* Plugin discovery chuẩn hoá bằng entry points (Python) và alias (TS).
* Tự động kiểm bằng `ruff`/`isort`, `mypy`, `import-linter`.


## 2) Tổng quan repo & sharing

* `zeta_server` phụ thuộc `zeta_shared` bằng path dependency (editable install) trong monorepo.
* Desktop (Electron) generate types từ OpenAPI của server và dùng alias trong TS để import sạch.


## 3) Python (Server) — Quy tắc import

### 3.1 src-layout + editable install

Trong `pyproject.toml` của server, khai báo path dependency vào `zeta_shared`:

```toml
[project]
name = "zeta-vn"
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]",
  "pydantic>=2",
  "httpx",
  "zeta-shared @ file://../zeta_shared",
]
requires-python = ">=3.10"
```

Cài editable install:

```powershell
cd zeta\zeta_shared; uv pip install -e .
cd ..\zeta_server; uv pip install -e .
```

Không thêm `PYTHONPATH`. Luôn chạy module bằng `python -m` hoặc `uvicorn zeta_vn.app.main:app`.

### 3.2 Layering & absolute import

Thư mục khuyến nghị:

```
zeta_vn/core/domain
zeta_vn/core/services
zeta_vn/core/adapters
zeta_vn/app/api
```

Luôn import theo absolute: `from zeta_vn.core.services.chat_service import ChatService`.

### 3.3 Public API bằng `__init__.py`

Ví dụ `zeta_vn/core/services/__init__.py`:

```python
from .chat_service import ChatService
from .memory_service import MemoryService

__all__ = ["ChatService", "MemoryService"]
```

Router dùng: `from zeta_vn.core.services import ChatService`.

### 3.4 Chống vòng lặp import

* Tách interface/port ra module riêng (ví dụ `ports.py`) và dùng `from __future__ import annotations` để type-hint.
* Dùng DI (FastAPI `Depends`) thay vì singletons global.

Ví dụ `ports.py`:

```python
from typing import Protocol

class EmbeddingPort(Protocol):
    def embed(self, text: str) -> list[float]: ...
```

Adapter thực hiện:

```python
from zeta_vn.core.domain.ports import EmbeddingPort

class OpenAIEmbedding(EmbeddingPort):
    def embed(self, text: str) -> list[float]:
        ...
```

### 3.5 Plugin discovery (entry points)

Khuyến nghị khai báo entry points trong `zeta_shared/pyproject.toml`:

```toml
[project.entry-points."zeta.plugins"]
qdrant = "zeta_shared.plugins.qdrant:QdrantVectorStore"
chroma = "zeta_shared.plugins.chroma:ChromaVectorStore"
```

Loader:

```python
from importlib.metadata import entry_points

def load_plugin(name: str):
    eps = entry_points(group="zeta.plugins")
    return eps[name].load()()
```

### 3.6 Kiểm soát import bằng import-linter

Ví dụ config `import-linter` ở root:

```ini
[importlinter]
root_package = zeta_vn

[contract:layers]
name = server_layers
type = layers
layers =
    zeta_vn.core.domain
    zeta_vn.core.services
    zeta_vn.core.adapters
    zeta_vn.app
```

Chạy `lint-imports` trong CI để fail nếu vi phạm layering.


## 4) TypeScript / Electron / React — Quy tắc import

### 4.1 `tsconfig` path alias

`zeta_desktop/tsconfig.json` ví dụ:

```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@app/*": ["renderer/app/*"],
      "@entities/*": ["renderer/entities/*"],
      "@features/*": ["renderer/features/*"],
      "@shared/*": ["renderer/shared/*"],
      "@main/*": ["main/*"],
      "@preload/*": ["preload/*"]
    }
  }
}
```

Nếu dùng Vite, bật `vite-tsconfig-paths`.

### 4.2 ESLint import order

`.eslintrc.cjs` ví dụ:

```js
module.exports = {
  plugins: ["import"],
  rules: {
    "import/order": ["warn", {
      "groups": [["builtin", "external"], ["internal"], ["parent", "sibling", "index"]],
      "pathGroups": [
        { "pattern": "@app/**", "group": "internal", "position": "after" },
        { "pattern": "@shared/**", "group": "internal", "position": "after" }
      ],
      "alphabetize": { "order": "asc", "caseInsensitive": true }
    }]
  }
}
```

### 4.3 Ví dụ import (renderer)

```ts
import { useQuery } from '@tanstack/react-query';
import { getUserProfile } from '@shared/api';
import { ProfileCard } from '@features/profile/ui/ProfileCard';
```


## 5) Chia sẻ schema: OpenAPI → TS types

Server expose `openapi.json` tại `/openapi.json`.

Desktop script (in `zeta_desktop/package.json`):

```json
"scripts": {
  "gen:api": "openapi-typescript http://localhost:8000/openapi.json -o src/renderer/shared/api/types.ts"
}
```

Sử dụng `openapi-typescript` hoặc `openapi2ts`, cân nhắc kết hợp `zod` cho runtime validation.


## 6) Mẫu import cho Router (Server)

```python
# zeta_vn/app/api/v1/chat.py
from fastapi import APIRouter, Depends
from zeta_vn.core.services import ChatService
from zeta_shared.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

def get_chat_service() -> ChatService:
    return ChatService()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, svc: ChatService = Depends(get_chat_service)):
    return await svc.handle(req)
```


## 7) Tránh lỗi test/import khi chạy PyTest

* Đặt tests dưới `zeta_server/tests/`.
* Tối ưu: dùng editable install; tránh `PYTHONPATH` thủ công.
* Chạy `pytest` từ thư mục `zeta_server`.


## 8) CI & pre-commit

Gợi ý `.pre-commit-config.yaml` (root):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.8
    hooks:
      - id: ruff
        args: ["--fix"]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: ["pydantic>=2"]
  - repo: https://github.com/seddonym/import-linter
    rev: v1.11.0
    hooks:
      - id: import-linter
        files: ^zeta_server/src/zeta_vn/
```


## 9) Lộ trình migrate imports hiện tại

1. Bật `src-layout`: di chuyển mã Python vào `zeta_server/src/` & `zeta_shared/src/`.
2. Thêm `zeta-shared @ file://../zeta_shared` vào `zeta_server`.
3. Viết `__init__.py` cho các package xuất public API.
4. Sửa import sang absolute theo layers.
5. Thêm tsconfig alias cho apps/desktop + cập nhật import.
6. Sinh types từ OpenAPI và thay thế `any` nơi cần.
7. Bật pre-commit + CI để khoá chuẩn.


## 10) Q&A ngắn

* Có cần `PYTHONPATH`? Không — dùng editable install + `python -m`.
* Tại sao import vẫn vòng lặp? Thường do violations trong layering; tách `ports`/interfaces.
* Copilot sẽ hiểu cấu trúc? Có — giữ import nhất quán + `__init__.py` + TS alias sẽ giúp đề xuất chính xác.


Nếu bạn muốn, tôi có thể tiếp tục và:

* Thêm/điều chỉnh `ruff` / `isort` config trong `pyproject.toml` để set `known-first-party = ["zeta_vn", "zeta_shared"]` (hiện đã có một số cấu hình, tôi sẽ kiểm tra và cập nhật nếu cần);
* Tạo mẫu `.eslintrc.cjs` trong `desktop_ai_zeta` hoặc `zeta_desktop` nếu chưa có;
* Viết script CI step (GitHub Actions) để chạy `import-linter` + `ruff` + `mypy`.

Hãy cho tôi biết bạn muốn tôi thực hiện bước tự động nào tiếp theo — tôi có thể chỉnh `pyproject.toml`, tạo file cấu hình cho apps/desktop, hoặc bổ sung CI workflow.
