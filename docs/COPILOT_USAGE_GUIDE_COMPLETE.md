# 🚀 Hướng dẫn sử dụng GitHub Copilot trong ZETA_VN

## ✅ Cài đặt hoàn tất

GitHub Copilot đã được cấu hình với các tính năng nâng cao:

### 🔧 Tính năng đã kích hoạt:
- ✅ **Auto completions** - Gợi ý code tự động
- ✅ **Inline suggestions** - Gợi ý code inline với nhiều options
- ✅ **Code actions** - Actions để fix và refactor
- ✅ **Iterative editing** - Chỉnh sửa lặp đi lặp lại
- ✅ **Chat integration** - Chat với Copilot về code
- ✅ **Context understanding** - Hiểu ngữ cảnh project
- ✅ **Full code generation** - Sinh code đầy đủ không giới hạn
- ✅ **Project patterns** - Tuân thủ patterns của dự án

### 🎯 Tối ưu hóa cho ZETA_VN:
- 🏗️ **Clean Architecture** patterns được tích hợp
- 🔒 **Security-first** approach trong code generation
- 📚 **Domain-driven design** patterns
- 🧪 **Test-driven development** support
- 📝 **Full documentation** generation

## 🎮 Phím tắt chính

| Phím tắt          | Chức năng                |
| ----------------- | ------------------------ |
| `Ctrl+Shift+I`    | Mở chat Copilot mới      |
| `Ctrl+Shift+C`    | Thêm selection vào chat  |
| `Ctrl+Alt+I`      | Inline chat              |
| `Ctrl+Alt+R`      | Review code với Copilot  |
| `Ctrl+Alt+F`      | Fix test failures        |
| `Ctrl+Alt+E`      | Explain problems         |
| `Ctrl+Shift+A`    | Generate tests           |
| `Ctrl+Shift+D`    | Generate documentation   |
| `Tab`             | Accept suggestion        |
| `Alt+]` / `Alt+[` | Next/Previous suggestion |

## 💡 Cách sử dụng hiệu quả

### 1. Sinh code đầy đủ với ngữ cảnh
```
@workspace Tạo một UserService hoàn chỉnh với CRUD operations, 
tuân thủ Clean Architecture, bao gồm authorization, validation, 
domain events, và error handling. Sinh đầy đủ implementation.
```

### 2. Sử dụng snippets có sẵn
- `domain-entity` - Tạo domain entity
- `app-service` - Tạo application service
- `repo-interface` - Tạo repository interface
- `fastapi-router` - Tạo FastAPI router
- `pydantic-schema` - Tạo API schemas
- `pytest-test` - Tạo test cases

### 3. Chat prompts hiệu quả

#### Tạo feature mới:
```
Tôi cần tạo feature quản lý Projects trong hệ thống. 
Hãy tạo đầy đủ:
1. Domain entity Project với fields: name, description, owner_id, status
2. Repository interface và implementation
3. Application service với CRUD operations
4. FastAPI router với API endpoints
5. Pydantic schemas cho request/response
6. Unit tests và integration tests
7. Database migration

Tuân thủ Clean Architecture và security patterns hiện tại.
```

#### Refactor code:
```
#file:zeta_vn/core/services/user_service.py
Refactor service này để:
1. Thêm caching layer
2. Improve error handling
3. Add comprehensive logging
4. Optimize database queries
5. Add rate limiting

Giữ nguyên API interface và backward compatibility.
```

#### Fix bugs:
```
#selection
Code này đang có lỗi performance. Hãy:
1. Analyze vấn đề
2. Suggest optimizations
3. Implement caching if needed
4. Add monitoring/metrics
5. Write tests để verify fix

Explain từng step.
```

#### Generate tests:
```
#file:zeta_vn/core/services/auth_service.py
Generate comprehensive test suite cho service này:
1. Unit tests cho tất cả methods
2. Integration tests với database
3. Security tests cho authorization
4. Performance tests
5. Edge cases và error scenarios

Use pytest fixtures và mocking appropriately.
```

### 4. Sử dụng agents đặc biệt

#### @workspace agent:
```
@workspace Analyze toàn bộ codebase và suggest improvements cho:
- Architecture inconsistencies
- Security vulnerabilities  
- Performance bottlenecks
- Code quality issues
- Missing tests coverage
```

#### @terminal agent:
```
@terminal Setup development environment:
1. Check Python version
2. Install dependencies với uv
3. Run quality checks
4. Setup pre-commit hooks
5. Verify all tests pass
```

## 🏗️ Patterns được tối ưu

### 1. Domain Entity Generation
Copilot sẽ tự động:
- Thêm proper type hints
- Include mixins cần thiết
- Generate domain events
- Add validation logic
- Create proper __str__ methods

### 2. Service Layer Generation  
Copilot sẽ:
- Inject dependencies correctly
- Add authorization checks
- Include error handling
- Emit domain events
- Add comprehensive logging

### 3. API Layer Generation
Copilot sẽ:
- Create proper FastAPI routers
- Add dependency injection
- Include response models
- Add error responses
- Generate OpenAPI docs

### 4. Test Generation
Copilot sẽ:
- Create comprehensive test suites
- Use proper fixtures
- Test authorization scenarios
- Include edge cases
- Add performance tests

## 🔍 Debugging với Copilot

### Analyze errors:
```
#selection
Lỗi này đang xảy ra, hãy:
1. Explain root cause
2. Suggest multiple solutions
3. Show impact of each solution
4. Recommend best approach
5. Help implement fix
```

### Performance issues:
```
#file:problem_file.py
Code này chạy chậm, hãy:
1. Profile performance bottlenecks
2. Suggest optimizations
3. Add caching where appropriate
4. Optimize database queries
5. Add monitoring/metrics
```

## 📚 Learning & Documentation

### Explain code:
```
#selection
Explain code này như thể bạn đang training junior developer:
1. What it does
2. How it works
3. Why it's designed this way
4. Potential improvements
5. Related patterns trong codebase
```

### Generate docs:
```
#file:service_file.py
Generate comprehensive documentation cho service này:
1. Class-level docstrings
2. Method docstrings với examples
3. Usage examples
4. Configuration guide
5. Troubleshooting section
```

## 🚦 Quality Assurance

Copilot được cấu hình để:
- ✅ Pass `ruff` formatting và linting
- ✅ Pass `mypy` strict type checking  
- ✅ Generate comprehensive tests
- ✅ Follow security best practices
- ✅ Maintain backward compatibility
- ✅ Include proper error handling
- ✅ Add comprehensive logging

## 🎯 Tips Pro

1. **Luôn cung cấp context**: Sử dụng `#file`, `#selection`, `@workspace`
2. **Specific requests**: Càng cụ thể càng tốt
3. **Multi-step tasks**: Break down thành steps nhỏ
4. **Review suggestions**: Luôn review code trước khi accept
5. **Use chat for complex tasks**: Dùng chat cho logic phức tạp
6. **Leverage project knowledge**: Copilot hiểu patterns của dự án

## 🔄 Workflow Integration

1. **Development cycle**:
   ```
   Code → Copilot Review → Tests → Quality Check → Commit
   ```

2. **Feature development**:
   ```
   Plan → Generate scaffolding → Implement logic → Tests → Documentation
   ```

3. **Bug fixing**:
   ```
   Analyze → Understand → Fix → Test → Verify
   ```

Với cấu hình này, Copilot sẽ sinh code đầy đủ, hiểu ngữ cảnh dự án, và giúp bạn maintain code quality cao nhất! 🚀