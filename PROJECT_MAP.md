# Project Map – zeta-monorepo

> Tự động sinh: cấu trúc thư mục, thống kê ngôn ngữ, mô tả heuristic cho folder/file then chốt.

## Tổng quan
- **Gốc**: `E:/zeta-monorepo`
- **Độ sâu cây**: `4`
- **Số thư mục (xấp xỉ)**: `21,950`
- **Số file (đếm trong cây)**: `3,749`
- **Phân bố ngôn ngữ (ước lượng theo đuôi file)**:
  - `markdown`: 1306
  - `config`: 1082
  - `python`: 973
  - `other`: 152
  - `powershell`: 94
  - `javascript`: 63
  - `shell`: 37
  - `typescript`: 36
  - `html`: 5
  - `styles`: 1

## Thư mục chính (ưu tiên theo số file)
| Thư mục | #files | Gợi ý chức năng |
|---|---:|---|
| `reports/ai-monitor` | 1800 |  |
| `tools/scripts` | 254 | Scripts CLI / devops, tiện ích build / test / deploy. |
| `docs` | 245 | Tài liệu hướng dẫn, kiến trúc, quyết định kỹ thuật. |
| `tools/scripts/tests` | 199 | Kiểm thử unit / integration / e2e, fixtures, helpers. |
| `scripts` | 69 | Scripts CLI / devops, tiện ích build / test / deploy. |
| `tests` | 49 | Kiểm thử unit / integration / e2e, fixtures, helpers. |
| `apps/zeta-ai-agent` | 48 |  |
| `extension/out` | 42 |  |
| `apps/backend/tests` | 34 | Kiểm thử unit / integration / e2e, fixtures, helpers. |
| `apps/desktop` | 32 | Frontend / desktop layer (Electron / React / Vite). |
| `apps/backend` | 28 |  |
| `.dup_backup/20250909_042457` | 27 |  |
| `.dup_backup/20250909_042810` | 27 |  |
| `apps/backend/config` | 27 | Cấu hình (env, constants, typed settings). |
| `reports/ai-codemod` | 25 |  |

## File then chốt
| File | Gợi ý vai trò |
|---|---|
| `.env` | Biến môi trường (không commit secrets!). |
| `Makefile` | Targets build / test tiện dụng. |
| `mypy.ini` | MyPy strict typing config. |
| `README.md` | Tài liệu chính cho module / thư mục. |
| `ruff.toml` | Ruff linter config. |
| `.env.turbo` | Biến môi trường (không commit secrets!). |
| `.env.ollama` | Biến môi trường (không commit secrets!). |
| `.env.example` | Biến môi trường (không commit secrets!). |
| `package.json` | Node project manifest & scripts. |
| `docs/README.md` | Tài liệu chính cho module / thư mục. |
| `extension/.env` | Biến môi trường (không commit secrets!). |
| `requirements.txt` | Danh sách dependencies Python. |
| `apps/backend/.env` | Biến môi trường (không commit secrets!). |
| `apps/desktop/.env` | Biến môi trường (không commit secrets!). |
| `extension/LICENSE` | Giấy phép dự án. |
| `extension/README.md` | Tài liệu chính cho module / thư mục. |
| `requirements-dev.txt` | Danh sách dependencies Python. |
| `production/Dockerfile` | Docker image build instructions. |
| `apps/desktop/README.md` | Tài liệu chính cho module / thư mục. |
| `extension/package.json` | Node project manifest & scripts. |

## Cấu trúc thư mục
```text
.
├── .cleanup_backup
│   └── redundant_1757367219
│       ├── backup_dirs
│       │   └── consolidation_trash
│       ├── backup_files
│       │   └── README.md~
│       └── cache_dirs
├── .continue
│   ├── docs
│   │   └── new-doc.yaml
│   ├── mcpServers
│   │   └── new-mcp-server.yaml
│   ├── prompts
│   │   ├── new-prompt-1.yaml
│   │   └── new-prompt.yaml
│   └── rules
│       ├── new-rule-1.md
│       └── new-rule.md
├── .dup_backup
│   ├── 20250909_042457
│   │   ├── apps
│   │   │   ├── backend
│   │   │   └── zeta-ai-agent
│   │   ├── docs
│   │   │   └── examples
│   │   ├── examples
│   │   │   └── turbo_ollama_usage_examples.py
│   │   ├── production
│   │   │   ├── scripts
│   │   │   └── src
│   │   ├── scripts
│   │   │   ├── apply_consolidation_plan.py
│   │   │   ├── benchmark_latency.py
│   │   │   ├── cleanup_reports.py
│   │   │   ├── consolidation_audit.py
│   │   │   ├── consolidation_plan_builder.py
│   │   │   ├── dedupe_scan.py
│   │   │   ├── lo_finetune.py
│   │   │   ├── prepare_vn_dataset.py
│   │   │   └── update_references.py
│   │   ├── tests
│   │   │   ├── ai-codemod
│   │   │   ├── ai-project-intelligence
│   │   │   ├── run_ai_codemod_tests.py
│   │   │   ├── run_ai_intelligence_tests.py
│   │   │   ├── test_ai_auto_refactor.py
│   │   │   ├── test_final_project_demo.py
│   │   │   └── test_turbo_demo.py
│   │   ├── tools
│   │   │   ├── ai-codemod
│   │   │   ├── ai-project-analyzer
│   │   │   ├── ai-project-intelligence
│   │   │   ├── ai_code_optimizer
│   │   │   ├── scripts
│   │   │   ├── tests
│   │   │   ├── cleanup_duplicates.py
│   │   │   ├── find_duplicate_files.py
│   │   │   ├── reference_updater.py
│   │   │   └── run_ai_optimization.py
│   │   ├── ai_auto_optimizer.py
│   │   ├── ai_auto_refactor.py
│   │   ├── ai_project_scanner.py
│   │   ├── final_project_demo.py
│   │   ├── gen_project_map.py
│   │   ├── metrics_server.py
│   │   ├── ollama_api_optimization_guide.py
│   │   ├── ollama_benchmark.py
│   │   ├── ollama_turbo_integration.py
│   │   ├── optimized_turbo_client.py
│   │   ├── production_deploy.py
│   │   ├── quick_duplicate_checker.py
│   │   ├── quick_start_turbo.py
│   │   ├── safe_backup_cleanup.py
│   │   ├── setup_dev.py
│   │   ├── setup_one_click_learning.py
│   │   ├── setup_vscode_ollama.py
│   │   ├── setup_vscode_turbo_api.py
│   │   ├── simple_turbo_setup.py
│   │   ├── smart_refactorer.py
│   │   ├── turbo_api_implementation.py
│   │   ├── turbo_api_online_auth.py
│   │   ├── turbo_demo.py
│   │   ├── turbo_ollama_client.py
│   │   ├── turbo_ollama_login.py
│   │   ├── turbo_setup.py
│   │   └── verify_ai_setup.py
│   └── 20250909_042810
│       ├── apps
│       │   ├── backend
│       │   └── zeta-ai-agent
│       ├── docs
│       │   └── examples
│       ├── examples
│       │   └── turbo_ollama_usage_examples.py
│       ├── production
│       │   ├── scripts
│       │   └── src
│       ├── scripts
│       │   ├── apply_consolidation_plan.py
│       │   ├── benchmark_latency.py
│       │   ├── cleanup_reports.py
│       │   ├── consolidation_audit.py
│       │   ├── consolidation_plan_builder.py
│       │   ├── dedupe_scan.py
│       │   ├── lo_finetune.py
│       │   ├── prepare_vn_dataset.py
│       │   └── update_references.py
│       ├── tests
│       │   ├── ai-codemod
│       │   ├── ai-project-intelligence
│       │   ├── run_ai_codemod_tests.py
│       │   ├── run_ai_intelligence_tests.py
│       │   ├── test_ai_auto_refactor.py
│       │   ├── test_final_project_demo.py
│       │   └── test_turbo_demo.py
│       ├── tools
│       │   ├── ai-codemod
│       │   ├── ai-project-analyzer
│       │   ├── ai-project-intelligence
│       │   ├── ai_code_optimizer
│       │   ├── scripts
│       │   ├── tests
│       │   ├── cleanup_duplicates.py
│       │   ├── find_duplicate_files.py
│       │   ├── reference_updater.py
│       │   └── run_ai_optimization.py
│       ├── ai_auto_optimizer.py
│       ├── ai_auto_refactor.py
│       ├── ai_project_scanner.py
│       ├── final_project_demo.py
│       ├── gen_project_map.py
│       ├── metrics_server.py
│       ├── ollama_api_optimization_guide.py
│       ├── ollama_benchmark.py
│       ├── ollama_turbo_integration.py
│       ├── optimized_turbo_client.py
│       ├── production_deploy.py
│       ├── quick_duplicate_checker.py
│       ├── quick_start_turbo.py
│       ├── safe_backup_cleanup.py
│       ├── setup_dev.py
│       ├── setup_one_click_learning.py
│       ├── setup_vscode_ollama.py
│       ├── setup_vscode_turbo_api.py
│       ├── simple_turbo_setup.py
│       ├── smart_refactorer.py
│       ├── turbo_api_implementation.py
│       ├── turbo_api_online_auth.py
│       ├── turbo_demo.py
│       ├── turbo_ollama_client.py
│       ├── turbo_ollama_login.py
│       ├── turbo_setup.py
│       └── verify_ai_setup.py
├── .github
│   ├── tests
│   │   └── test_gen_project_map.py
│   ├── workflows
│   │   ├── ai-codemod.yml
│   │   ├── ai-intelligence-tests.yml
│   │   ├── ai-optimization.yml
│   │   ├── ci-root.yml
│   │   ├── monorepo-standards.yml
│   │   ├── numpy-compatibility.yml
│   │   ├── quality-gates.yml
│   │   ├── security-audit.yml
│   │   ├── semantic-pr.yml
│   │   ├── stress-test-gpu.yml
│   │   ├── stress-test-linux.yml
│   │   └── stress-test.yml
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── gen_project_map.py
│   └── pull_request_template.md
├── .venv-optimized
│   ├── Lib
│   │   └── site-packages
│   │       ├── _distutils_hack
│   │       ├── pip
│   │       ├── pip-24.0.dist-info
│   │       ├── pkg_resources
│   │       ├── setuptools
│   │       ├── setuptools-65.5.0.dist-info
│   │       └── distutils-precedence.pth
│   ├── Scripts
│   │   ├── pip.exe
│   │   ├── pip3.11.exe
│   │   ├── pip3.exe
│   │   ├── python.exe
│   │   └── pythonw.exe
│   └── pyvenv.cfg
├── apps
│   ├── backend
│   │   ├── .artifacts
│   │   ├── .venv-ollama
│   │   │   ├── Lib
│   │   │   ├── Scripts
│   │   │   └── pyvenv.cfg
│   │   ├── app
│   │   │   ├── ai
│   │   │   ├── api
│   │   │   ├── asr
│   │   │   ├── auth
│   │   │   ├── common
│   │   │   ├── compat
│   │   │   ├── containers
│   │   │   ├── controllers
│   │   │   ├── dependencies
│   │   │   ├── deps
│   │   │   ├── exceptions
│   │   │   ├── handlers
│   │   │   ├── infrastructure
│   │   │   ├── middleware
│   │   │   ├── minimal_rag
│   │   │   ├── monitoring
│   │   │   ├── observability
│   │   │   ├── ocr
│   │   │   ├── rag
│   │   │   ├── realtime
│   │   │   ├── schemas
│   │   │   ├── security
│   │   │   ├── serializers
│   │   │   ├── services
│   │   │   ├── startup
│   │   │   ├── status
│   │   │   ├── tests
│   │   │   ├── utils
│   │   │   ├── validators
│   │   │   ├── websockets
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── db.py
│   │   │   ├── demo_integration_main.py
│   │   │   ├── dependencies.py
│   │   │   ├── deps.py
│   │   │   ├── deps_compat.py
│   │   │   ├── di_container.py
│   │   │   ├── factory.py
│   │   │   ├── lifespan.py
│   │   │   ├── logger.py
│   │   │   ├── main.py
│   │   │   ├── main_clean.py
│   │   │   ├── main_production.py
│   │   │   ├── main_production_clean.py
│   │   │   ├── test_blueprint.py
│   │   │   └── worker.py
│   │   ├── cli
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── dlq_replay.py
│   │   │   └── maintenance.py
│   │   ├── config
│   │   │   ├── environments
│   │   │   ├── settings
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── advanced_settings.py
│   │   │   ├── advanced_settings.py.backup
│   │   │   ├── api.json
│   │   │   ├── api_config.py
│   │   │   ├── auth_config.py
│   │   │   ├── cache.py
│   │   │   ├── cache_config.py
│   │   │   ├── capabilities.yaml
│   │   │   ├── celery_config.py
│   │   │   ├── core.json
│   │   │   ├── database.json
│   │   │   ├── database.py
│   │   │   ├── external_services.py
│   │   │   ├── logging.py
│   │   │   ├── ml_config.py
│   │   │   ├── model_matrix.yaml
│   │   │   ├── models.py
│   │   │   ├── observability.json
│   │   │   ├── production.py
│   │   │   ├── redis.py
│   │   │   ├── security.json
│   │   │   ├── security.py
│   │   │   ├── settings.py
│   │   │   ├── settings_shim.py
│   │   │   ├── storage_config.py
│   │   │   └── unified_settings.py
│   │   ├── core
│   │   │   ├── adapters
│   │   │   ├── application
│   │   │   ├── async_templates
│   │   │   ├── auth
│   │   │   ├── caching
│   │   │   ├── common
│   │   │   ├── cost
│   │   │   ├── distillation
│   │   │   ├── domain
│   │   │   ├── exceptions
│   │   │   ├── implementations
│   │   │   ├── infrastructure
│   │   │   ├── ingest
│   │   │   ├── interfaces
│   │   │   ├── kpis
│   │   │   ├── learning
│   │   │   ├── llm
│   │   │   ├── memory
│   │   │   ├── mlops
│   │   │   ├── model_management
│   │   │   ├── multimodal
│   │   │   ├── observability
│   │   │   ├── optimization
│   │   │   ├── orchestrator
│   │   │   ├── outbox
│   │   │   ├── performance
│   │   │   ├── plugins
│   │   │   ├── policies
│   │   │   ├── ports
│   │   │   ├── quality
│   │   │   ├── reasoning
│   │   │   ├── registry
│   │   │   ├── resilience
│   │   │   ├── security
│   │   │   ├── self_awareness
│   │   │   ├── self_improvement
│   │   │   ├── services
│   │   │   ├── shared
│   │   │   ├── testing
│   │   │   ├── tests
│   │   │   ├── triage
│   │   │   ├── use_cases
│   │   │   ├── utils
│   │   │   ├── value_objects
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── chunking.py
│   │   │   ├── container.py
│   │   │   ├── CORE_FILE_MAP.md
│   │   │   ├── pipeline.py
│   │   │   └── types.py
│   │   ├── data
│   │   │   ├── adapters
│   │   │   ├── clients
│   │   │   ├── config
│   │   │   ├── database
│   │   │   ├── dto
│   │   │   ├── dtos
│   │   │   ├── external
│   │   │   ├── factories
│   │   │   ├── implementations
│   │   │   ├── instrumentation
│   │   │   ├── knowledge
│   │   │   ├── mappers
│   │   │   ├── migrations
│   │   │   ├── models
│   │   │   ├── repositories
│   │   │   ├── seeds
│   │   │   ├── services
│   │   │   ├── shared
│   │   │   ├── tests
│   │   │   ├── utils
│   │   │   ├── vector_stores
│   │   │   ├── __init__.py
│   │   │   ├── database_async.py
│   │   │   ├── database_init.py
│   │   │   ├── migrations.py
│   │   │   ├── models.py
│   │   │   └── outbox_tables.py
│   │   ├── datasets
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── registry.yaml
│   │   ├── deployment
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── rollout.py
│   │   ├── docs
│   │   │   ├── api
│   │   │   ├── examples
│   │   │   ├── guides
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── API.md
│   │   │   ├── ARCHITECTURE.md
│   │   │   ├── BEST_PRACTICES.md
│   │   │   ├── CHANGELOG.md
│   │   │   ├── CONTRIBUTING.md
│   │   │   ├── DEPLOYMENT.md
│   │   │   ├── DI_PATTERN_SETUP.md
│   │   │   ├── FAQ.md
│   │   │   ├── INSTALLATION.md
│   │   │   ├── INTEGRATION.md
│   │   │   ├── LICENSE.md
│   │   │   ├── MIGRATION.md
│   │   │   ├── PERFORMANCE.md
│   │   │   ├── README.md
│   │   │   ├── ROADMAP.md
│   │   │   ├── SECURITY.md
│   │   │   ├── TROUBLESHOOTING.md
│   │   │   ├── TUTORIAL.md
│   │   │   └── USER_GUIDE.md
│   │   ├── evaluators
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── verifier_gpt5.py
│   │   ├── examples
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── profiler_demo.py
│   │   │   ├── profiler_demo_impl.py
│   │   │   ├── simple_app.py
│   │   │   └── simple_app_impl.py
│   │   ├── infra
│   │   │   ├── extractors
│   │   │   ├── tests
│   │   │   ├── vector_backends
│   │   │   ├── __init__.py
│   │   │   └── embedding.py
│   │   ├── infrastructure
│   │   │   ├── _scaffold
│   │   │   ├── phase3_artifacts
│   │   │   ├── scripts
│   │   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── ingest
│   │   │   ├── crawlers
│   │   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── integration
│   │   │   ├── api_clients
│   │   │   ├── data_fetchers
│   │   │   ├── security
│   │   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── observability
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── alert_router.py
│   │   │   ├── metrics.py
│   │   │   ├── otel_init.py
│   │   │   └── sla_slo_dashboard.py
│   │   ├── ollama
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── monitoring.py
│   │   │   └── smoke_test.py
│   │   ├── perf
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── chat_2025_09_02_02_58_41.md
│   │   │   ├── config.py
│   │   │   ├── enhanced_instrumentation.py
│   │   │   ├── instrumentation.py
│   │   │   ├── integration_manager.py
│   │   │   ├── ml_optimization.py
│   │   │   ├── production_config.py
│   │   │   ├── smoke.py
│   │   │   ├── success_metrics.py
│   │   │   └── tracing.py
│   │   ├── reports
│   │   │   ├── coverage_html
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── coverage.xml
│   │   │   └── pytest.xml
│   │   ├── scripts
│   │   │   ├── seed
│   │   │   ├── testing
│   │   │   ├── tests
│   │   │   └── __init__.py
│   │   ├── storage
│   │   │   ├── backups
│   │   │   ├── tests
│   │   │   ├── uploads
│   │   │   ├── __init__.py
│   │   │   ├── archive_storage.py
│   │   │   ├── backup_storage.py
│   │   │   ├── blob_storage.py
│   │   │   ├── cache_storage.py
│   │   │   ├── document_storage.py
│   │   │   ├── file_service.py
│   │   │   ├── local_storage.py
│   │   │   ├── log_storage.py
│   │   │   ├── media_storage.py
│   │   │   ├── s3_storage.py
│   │   │   ├── session_storage.py
│   │   │   ├── temp_storage.py
│   │   │   └── vector_storage.py
│   │   ├── stubs
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── openai.py
│   │   ├── tests
│   │   │   ├── api
│   │   │   ├── config
│   │   │   ├── core
│   │   │   ├── db
│   │   │   ├── e2e
│   │   │   ├── entities
│   │   │   ├── evaluators
│   │   │   ├── fixtures
│   │   │   ├── infrastructure
│   │   │   ├── integration
│   │   │   ├── llm
│   │   │   ├── memory
│   │   │   ├── mocks
│   │   │   ├── performance
│   │   │   ├── rag
│   │   │   ├── smoke
│   │   │   ├── standalone
│   │   │   ├── stubs
│   │   │   ├── tools
│   │   │   ├── unit
│   │   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── test___init__.py
│   │   │   ├── test_agent_orchestrator_parallel.py
│   │   │   ├── test_agent_self_improvement.py
│   │   │   ├── test_ai_runner_fix.py
│   │   │   ├── test_application.py
│   │   │   ├── test_asr_smoke.py
│   │   │   ├── test_auth_production.py
│   │   │   ├── test_auto_updater.py
│   │   │   ├── test_basic_structure.py
│   │   │   ├── test_chat.py
│   │   │   ├── test_check_duplicates.py
│   │   │   ├── test_dev_assistant.py
│   │   │   ├── test_domain_event_aliases.py
│   │   │   ├── test_dto_conversion.py
│   │   │   ├── test_enhanced_rag.py
│   │   │   ├── test_event_bus_fix.py
│   │   │   ├── test_feedback_api.py
│   │   │   ├── test_learning_api.py
│   │   │   ├── test_main.py.backup
│   │   │   ├── test_memory_normalization.py
│   │   │   ├── test_no_duplicate_concepts.py
│   │   │   ├── test_performance_advanced_caching.py
│   │   │   ├── test_plan_isolated.py
│   │   │   ├── test_profiler_demo.py
│   │   │   ├── test_protocols.py
│   │   │   ├── test_rag_optimized.py
│   │   │   ├── test_scale_agent_use_case.py
│   │   │   ├── test_security_basic.py
│   │   │   ├── test_security_system.py
│   │   │   ├── test_simple_app.py
│   │   │   ├── test_smoke.py
│   │   │   └── test_start_all_tools.py
│   │   ├── tools
│   │   │   ├── refactor
│   │   │   ├── scaffold
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── implements.py
│   │   │   └── ports_tools.py
│   │   ├── trainer
│   │   │   ├── datasets
│   │   │   ├── deployment
│   │   │   ├── evaluators
│   │   │   ├── ingest
│   │   │   ├── tests
│   │   │   ├── triage
│   │   │   ├── workflows
│   │   │   ├── __init__.py
│   │   │   ├── demo_ai_learning.py
│   │   │   ├── distill_gpt5.py
│   │   │   ├── finetune_llama4.py
│   │   │   └── model_matrix.py
│   │   ├── training
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── gpt4o_trainer.py
│   │   ├── triage
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── safety_filters.py
│   │   ├── workflows
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── trainer_pipeline.py
│   │   ├── zeta_vn
│   │   │   └── trainer
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── __init__.py
│   │   ├── _backup_metadata.json
│   │   ├── apiClient.ts
│   │   ├── application.py
│   │   ├── auth.ts
│   │   ├── dev_assistant.py
│   │   ├── Dockerfile
│   │   ├── OPTIMIZATION_COMPLETED.md
│   │   ├── OPTIMIZATION_TODO.md
│   │   ├── PHASE2_OPTIMIZATION_COMPLETED.md
│   │   ├── poetry.lock
│   │   ├── profiler_demo.py
│   │   ├── PROJECT_ANALYSIS_REPORT.md
│   │   ├── PROJECT_MAP.md
│   │   ├── protocols.py
│   │   ├── pyproject.toml
│   │   ├── quick_test.py
│   │   ├── simple_app.py
│   │   ├── simple_ollama_test.py
│   │   ├── test_full_integration.py
│   │   ├── test_ollama_client.py
│   │   ├── test_prometheus.py
│   │   ├── typedClient.ts
│   │   ├── uv.lock
│   │   ├── wsSchema.ts
│   │   └── zeta.db
│   ├── desktop
│   │   ├── .github
│   │   │   ├── ISSUE_TEMPLATE
│   │   │   ├── workflows
│   │   │   ├── CODEOWNERS
│   │   │   ├── dependabot.yml
│   │   │   └── PULL_REQUEST_TEMPLATE.md
│   │   ├── config
│   │   │   └── plugins.allowlist.json
│   │   ├── contracts
│   │   │   ├── config
│   │   │   ├── plugins
│   │   │   └── ws
│   │   ├── docs
│   │   │   ├── ADR
│   │   │   ├── COMPLIANCE_CHECKLIST.md
│   │   │   ├── DATA_RETENTION_POLICY.md
│   │   │   ├── IMPLEMENTATION_STATUS.md
│   │   │   ├── PRIVACY_POLICY.template.md
│   │   │   └── RUNBOOK_INCIDENT.md
│   │   ├── electron
│   │   │   ├── main
│   │   │   ├── ipcHandler.js
│   │   │   ├── main.js
│   │   │   ├── main.ts
│   │   │   ├── preload.js
│   │   │   ├── preload.ts
│   │   │   ├── publish.example.json
│   │   │   ├── publish.json
│   │   │   ├── robotExec.js
│   │   │   └── whisperManager.js
│   │   ├── licenses
│   │   │   ├── licenses.csv
│   │   │   └── licenses.json
│   │   ├── plugins
│   │   │   ├── system-monitor
│   │   │   └── training-monitor
│   │   ├── sbom
│   │   │   ├── bom.json
│   │   │   └── bom.xml
│   │   ├── src
│   │   │   ├── __tests__
│   │   │   ├── analytics
│   │   │   ├── api
│   │   │   ├── automation
│   │   │   ├── components
│   │   │   ├── constants
│   │   │   ├── context
│   │   │   ├── controllers
│   │   │   ├── events
│   │   │   ├── features
│   │   │   ├── hooks
│   │   │   ├── i18n
│   │   │   ├── lib
│   │   │   ├── memory
│   │   │   ├── pages
│   │   │   ├── providers
│   │   │   ├── router
│   │   │   ├── services
│   │   │   ├── stores
│   │   │   ├── test
│   │   │   ├── tests
│   │   │   ├── types
│   │   │   ├── ui
│   │   │   ├── utils
│   │   │   ├── App.tsx
│   │   │   ├── env.d.ts
│   │   │   ├── global.d.ts
│   │   │   ├── main-original.tsx
│   │   │   └── main.tsx
│   │   ├── tests
│   │   │   ├── actionQueue.test.ts
│   │   │   ├── batchReset.test.ts
│   │   │   ├── README.md
│   │   │   ├── setupTests.ts
│   │   │   └── test_cache.ts
│   │   ├── .editorconfig
│   │   ├── .env
│   │   ├── .env.build
│   │   ├── .env.development
│   │   ├── .env.example
│   │   ├── .env.production
│   │   ├── .eslintrc.cjs
│   │   ├── .gitattributes
│   │   ├── .gitignore
│   │   ├── .jscpd.json
│   │   ├── .npmrc
│   │   ├── .prettierignore
│   │   ├── .prettierrc.json
│   │   ├── compliance-report.json
│   │   ├── electron-builder.json
│   │   ├── ENTERPRISE_PACKAGING_COMPLETE.md
│   │   ├── ENTERPRISE_V1_COMPLETE.md
│   │   ├── env.d.ts
│   │   ├── index.html
│   │   ├── openapi.json
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── POSTFLIGHT_HOTFIX_COMPLETE.md
│   │   ├── README.md
│   │   ├── RELEASE_NOTES.md
│   │   ├── RELEASE_NOTES.template.md
│   │   ├── SECURITY.md
│   │   ├── tsconfig.json
│   │   ├── tsconfig.node.json
│   │   ├── V1_0_0_RELEASE_SUMMARY.md
│   │   ├── vite.config.ts
│   │   └── vitest.config.ts
│   ├── zeta-ai-agent
│   │   ├── .github
│   │   │   └── workflows
│   │   ├── config
│   │   │   ├── alertmanager
│   │   │   ├── prometheus
│   │   │   ├── tests
│   │   │   └── settings.py
│   │   ├── helm
│   │   │   └── zeta-ai-agent
│   │   ├── infra
│   │   │   ├── helm
│   │   │   └── terraform
│   │   ├── src
│   │   │   ├── core
│   │   │   ├── extension
│   │   │   ├── tests
│   │   │   ├── types
│   │   │   └── utils
│   │   ├── tests
│   │   │   ├── integration
│   │   │   ├── mocks
│   │   │   ├── test_dev_server.py
│   │   │   ├── test_fix_errors.py
│   │   │   ├── test_metrics_server.py
│   │   │   ├── test_metrics_server_optimized.py
│   │   │   └── test_optimize.py
│   │   ├── .dockerignore
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── .eslintrc.json
│   │   ├── .gitignore
│   │   ├── ADVANCED_TIMELINE.md
│   │   ├── alertmanager.yml
│   │   ├── CHANGELOG.md
│   │   ├── COMPILATION_FIXES.md
│   │   ├── DEPLOYMENT_ASSESSMENT.md
│   │   ├── DEPLOYMENT_COMMANDS.md
│   │   ├── dev_server.py
│   │   ├── DEVOPS_PLAYBOOK.md
│   │   ├── DEVOPS_SETUP_GUIDE.md
│   │   ├── Dockerfile
│   │   ├── ENVIRONMENT_STATUS.md
│   │   ├── feedback.db
│   │   ├── fix_errors.py
│   │   ├── HEALTH_CHECK_VERIFICATION.md
│   │   ├── icon.png
│   │   ├── LICENSE
│   │   ├── MARKETPLACE_PUBLISHING_GUIDE.md
│   │   ├── metrics_server.py
│   │   ├── metrics_server_optimized.py
│   │   ├── MODULE_12_COMPLETION_REPORT.md
│   │   ├── nodemon.json
│   │   ├── OPTIMIZATION_IMPLEMENTATION_REPORT.md
│   │   ├── OPTIMIZATION_PROPOSAL.md
│   │   ├── optimize.py
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── PERFORMANCE_QUICKSTART.md
│   │   ├── performance_test.py
│   │   ├── PHASE2_ROADMAP.md
│   │   ├── PRODUCTION_DEPLOYMENT_GUIDE.md
│   │   ├── PRODUCTION_READINESS_REPORT.md
│   │   ├── QUICK_COMMANDS.md
│   │   ├── QUICK_DEPLOY_GUIDE.md
│   │   ├── QUICK_START.md
│   │   ├── QUICK_START_GUIDE.md
│   │   ├── QUICK_START_OPTIMIZATION.md
│   │   ├── README.md
│   │   ├── requirements-dev.txt
│   │   ├── requirements-optimization.txt
│   │   ├── SECURITY_CHECKLIST.md
│   │   ├── tsconfig.json
│   │   ├── USER_GUIDE.md
│   │   └── zeta-ai-agent-1.0.0.vsix
│   └── zeta_vn
│       └── app
│           └── api
├── backups
│   ├── attong39_zeta_config.txt
│   ├── models_list.txt
│   └── zeta_py_teacher_config.txt
├── config
│   ├── grafana
│   │   ├── dashboards
│   │   │   ├── development
│   │   │   ├── production
│   │   │   └── zeta-ollama-dashboard.json
│   │   └── provisioning
│   │       ├── dashboards
│   │       └── datasources
│   ├── prometheus
│   │   ├── alert.rules.yml
│   │   └── prometheus.yml
│   ├── alertmanager.yml
│   ├── api.json
│   ├── core.json
│   ├── database.json
│   ├── observability.json
│   └── security.json
├── desktop
│   └── src
│       └── lib
│           └── preview
├── docs
│   ├── api
│   │   ├── error_codes.md
│   │   └── openapi.yaml
│   ├── automation
│   │   ├── auto_fix_policy.md
│   │   └── p1_pr_checklist.md
│   ├── examples
│   │   ├── python-assistant
│   │   │   ├── tests
│   │   │   ├── .env.example
│   │   │   ├── assistant.py
│   │   │   ├── benchmark.py
│   │   │   ├── examples_turbo_usage.py
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   ├── test-live.bat
│   │   │   ├── turbo_api_client.py
│   │   │   ├── turbo_assistant.py
│   │   │   ├── turbo_cli.py
│   │   │   └── turbo_ollama_integration.py
│   │   ├── tests
│   │   │   ├── test___init__.py
│   │   │   └── test_agent_creation.py
│   │   ├── __init__.py
│   │   ├── agent_creation.py
│   │   └── README.md
│   ├── guides
│   │   ├── development.md
│   │   ├── quick_start.md
│   │   └── signed_requests.md
│   ├── implementation_guides
│   │   └── rag_service_guide.md
│   ├── monitoring
│   │   ├── alertmanager
│   │   │   └── ollama_alerts.yml
│   │   ├── grafana_queries.md
│   │   └── rate_limit_dashboard.md
│   ├── prompts
│   │   ├── config.prompt.md
│   │   ├── env_configs.prompt.md
│   │   ├── monitoring.prompt.md
│   │   └── new.prompt.prompt.md
│   ├── .chat_patch_template.md
│   ├── AI_AGENT_IMPLEMENTATION_COMPLETE.md
│   ├── AI_APP_OPTIMIZATION_COMPREHENSIVE.md
│   ├── AI_ML_COMPONENTS.md
│   ├── AI_SERVER_DEPLOYMENT.md
│   ├── AI_SERVER_DESIGN.md
│   ├── AI_SERVICES_OPTIMIZATION_COMPLETE.md
│   ├── AI_SERVICES_USAGE_GUIDE.md
│   ├── API.md
│   ├── API_CONSISTENCY_GUIDE.md
│   ├── API_OPTIMIZATION_PROGRESS_DAY1.md
│   ├── API_REFERENCE.md
│   ├── API_ROUTER_SPEC.md
│   ├── API_V1_COMPLETION_REPORT.md
│   ├── API_V2_OPTIMIZATION_SUMMARY.md
│   ├── APP_DATA_OPTIMIZATION_PROGRESS.md
│   ├── ARCHITECTURE.md
│   ├── ARCHITECTURE_AUDIT_REPORT.md
│   ├── ARCHITECTURE_EVOLUTION.md
│   ├── AUTHORIZATION_ARCHITECTURE_OVERVIEW.md
│   ├── AUTO_OPTIMIZATION_REPORT.md
│   ├── AUTO_UPGRADE_GUIDE.md
│   ├── AUTOMATION_UPGRADE_PLAN.md
│   ├── BEST_PRACTICES.md
│   ├── BRANCH_PLAN_AND_EXECUTION.md
│   ├── CHANGELOG.md
│   ├── CHUNKING_CONSOLIDATION_PLAN.md
│   ├── CLEAN_ARCHITECTURE_5_FILES_OPTIMIZATION_REPORT.md
│   ├── CLEANUP_REPORT.md
│   ├── CODE_QUALITY_COMPREHENSIVE_COMPLETE.md
│   ├── CODE_QUALITY_PHASE_1_2_COMPLETE.md
│   ├── CODE_QUALITY_PHASE_3_COMPLETE.md
│   ├── CODE_STANDARDS.md
│   ├── COMPLETE_AI_SELF_MANAGEMENT_SYSTEM.md
│   ├── COMPLETE_INTEGRATION_REPORT.md
│   ├── COMPLETION_ROADMAP.md
│   ├── COMPONENT_CONSISTENCY_REPORT.md
│   ├── COMPREHENSIVE_IMPROVEMENT_PROPOSAL.md
│   ├── COMPREHENSIVE_OPTIMIZATION_PLAN.md
│   ├── COMPREHENSIVE_OPTIMIZATION_PROPOSAL.md
│   ├── COMPREHENSIVE_PROJECT_SAFETY_COMPLETE.md
│   ├── COMPREHENSIVE_SAFE_FIXING_PLAN.md
│   ├── COMPREHENSIVE_UPGRADE_PLAN.md
│   ├── CONSISTENCY_IMPLEMENTATION_ROADMAP.md
│   ├── CONSOLIDATION_CHECKLIST.md
│   ├── CONSOLIDATION_RUNBOOK.md
│   ├── CONTINUE_WITHOUT_COPILOT_GUIDE.md
│   ├── CONTRACT_GUARD_AND_VERSIONING.md
│   ├── CONTRIBUTING.md
│   ├── COPILOT_AGENT_FINAL_SUCCESS.md
│   ├── COPILOT_AGENT_SUCCESS_REPORT.md
│   ├── COPILOT_AGENT_ULTIMATE_SUCCESS.md
│   ├── COPILOT_CONFIG_FIXED.md
│   ├── COPILOT_CONTEXT.md
│   ├── COPILOT_FULL_INTELLIGENT_SYSTEM_COMPLETE.md
│   ├── COPILOT_INTEGRATION_PLAYBOOK.md
│   ├── COPILOT_INTELLIGENT_LEARNING_COMPLETE.md
│   ├── COPILOT_LEARNING_SETUP_COMPLETE.md
│   ├── COPILOT_PRODUCTION_STATUS.md
│   ├── COPILOT_RULES.md
│   ├── COPILOT_SETUP_COMPLETE.md
│   ├── COPILOT_SETUP_COMPLETE_SUMMARY.md
│   ├── COPILOT_SUPER_INTELLIGENT_COMPLETE.md
│   ├── COPILOT_SUPER_INTELLIGENT_SETUP_COMPLETE.md
│   ├── COPILOT_USAGE_GUIDE.md
│   ├── COPILOT_USAGE_GUIDE_COMPLETE.md
│   ├── CORE_IMPLEMENTATION_COMPLETE_SUMMARY.md
│   ├── CORE_IMPLEMENTATION_FINAL_SUMMARY.md
│   ├── CORE_IMPLEMENTATION_PHASE1_SUMMARY.md
│   ├── CORE_IMPLEMENTATION_PLAN.md
│   ├── CORE_OPTIMIZATION_SUMMARY.md
│   ├── CORE_ROADMAP_CORE.md
│   ├── core_services_consolidation_guides.md
│   ├── CORE_UPGRADE_COMPREHENSIVE_PLAN.md
│   ├── CRITICAL_ACTION_PLAN.md
│   ├── DATA_OPTIMIZATION_PHASE1_REPORT.md
│   ├── DATA_OPTIMIZATION_PLAN.md
│   ├── DEEPSEEK_DEPLOY_README.md
│   ├── DEEPSEEK_R1_SETUP_GUIDE.md
│   ├── DEPENDENCIES_OPTIMIZATION_PLAN.md
│   ├── DEPLOYMENT.md
│   ├── DEPRECATION_POLICY.md
│   ├── DESKTOP_APP_ARCHITECTURE.md
│   ├── DESKTOP_CONTROL_GUIDE.md
│   ├── DESKTOP_CONTROL_IMPLEMENTATION_COMPLETE.md
│   ├── DESKTOP_CONTROL_PACK.md
│   ├── DESKTOP_HARDENING_PACK_COMPLETE.md
│   ├── DESKTOP_PRODUCTION_ARCHITECTURE_COMPLETE.md
│   ├── DESKTOP_PRODUCTION_SECURITY_COMPLETE.md
│   ├── DESKTOP_SERVER_CONTRACTS.md
│   ├── DEV_PRECOMMIT_AND_CI.md
│   ├── DEVELOPER_GUIDE.md
│   ├── DEVELOPMENT_AUTOMATION.md
│   ├── DEVELOPMENT_GUIDE.md
│   ├── DEVEX_DEVSECOPS.md
│   ├── DI_SYSTEM_GUIDE.md
│   ├── DIFF_GATE_SYSTEM_COMPLETE.md
│   ├── DOCUMENTATION_SYNC_PLAN.md
│   ├── DOMAIN_EVENTS_MIGRATION_COMPLETE.md
│   ├── DTO_PATTERN_IMPLEMENTATION_COMPLETE.md
│   ├── EMERGENCY_STABILIZATION.md
│   ├── ENHANCED_FILE_INTEGRITY_GUARD_COMPLETE.md
│   ├── ENHANCED_RAG_2025_IMPLEMENTATION_REPORT.md
│   ├── ENTERPRISE_OUTBOX_COMPLETE.md
│   ├── ENTERPRISE_PRODUCTION_ROADMAP.md
│   ├── ENVIRONMENT_ISSUES_DIAGNOSIS_REPORT.md
│   ├── F821_FIX_PROGRESS_REPORT.md
│   ├── FAQ.md
│   ├── FINAL_COMPLETION_PROPOSAL.md
│   ├── FINAL_SAFETY_RECOMMENDATIONS.md
│   ├── FINAL_SPRINT.md
│   ├── FOCUS.md
│   ├── GO_LIVE_CHECK_COMPLETE.md
│   ├── GO_LIVE_CHECK_COMPLETE_FINAL.md
│   ├── GO_LIVE_CHECK_ENHANCED_COMPLETE.md
│   ├── grafana_stress_dashboard.json
│   ├── GRAPHQL_API_DEVELOPER_GUIDE.md
│   ├── GRAPHQL_API_STRUCTURE_PROPOSAL.md
│   ├── GRAPHQL_MIGRATION_COMPLETE_REPORT.md
│   ├── GRAPHQL_MIGRATION_REPORT.md
│   ├── GRAPHQL_OPTIMIZATION_PLAN.md
│   ├── GRAPHQL_OPTIMIZATION_SUCCESS_REPORT.md
│   ├── GRAPHQL_UPGRADE_PLAN.md
│   ├── GUARDIAN_UPGRADE_COMPLETE.md
│   ├── HARDENING_COMPLETE.md
│   ├── HUONG_DAN_TRIEN_KHAI_PRODUCTION.md
│   ├── IMPLEMENTATION_COMPLETE_SUMMARY.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   ├── IMPORTS_GUIDE.md
│   ├── IMPORTS_OPTIMIZATION.md
│   ├── IMPROVEMENT_ANALYSIS.md
│   ├── IMPROVEMENT_SUMMARY.md
│   ├── INIT_FILES_REPORT.md
│   ├── INIT_FIX_SUMMARY.md
│   ├── INSTALLATION.md
│   ├── INTEGRATION.md
│   ├── JSC_PD_NEXT_STEPS.md
│   ├── JSC_PD_USAGE.md
│   ├── LIBRARIES.md
│   ├── LIBRARIES_COMPLETE_SUMMARY.md
│   ├── LIBRARIES_INSTALLATION_COMPLETE.md
│   ├── LICENSE.md
│   ├── MAIN_TSX_ANALYSIS_REPORT.md
│   ├── MEMORY_DELETE_IMPLEMENTATION_COMPLETE.md
│   ├── MEMORY_DELETE_OPTIMIZATION_PROPOSAL.md
│   ├── MIDDLEWARE_ENHANCEMENT_COMPLETE_REPORT.md
│   ├── MIGRATION.md
│   ├── MIGRATION_GUIDE_RESTRUCTURED.md
│   ├── MIGRATION_PLAN_DATA_STRUCTURE.md
│   ├── MISSING_CODE_AUDIT_SUMMARY.md
│   ├── MISSING_CODE_AUDIT_SYSTEM.md
│   ├── MISSION_ACCOMPLISHED.md
│   ├── ONE_CLICK_LEARNING_COMPLETE.md
│   ├── OPTIMIZATION_DASHBOARD.md
│   ├── OPTIMIZATION_IMPLEMENTATION_PLAN.md
│   ├── OPTIMIZATION_PLAN.md
│   ├── OPTION_2_ENHANCED_RAG_PIPELINE.md
│   ├── OPTION_A_INTEGRATION_COMPLETE.md
│   ├── PERF_UPGRADE_SUMMARY.md
│   ├── PERFORMANCE.md
│   ├── PERFORMANCE_ARCH_PATTERN.md
│   ├── PERFORMANCE_OPTIMIZATION_UPGRADE_PLAN.md
│   ├── PHASE0_COMPLETION_REPORT.md
│   ├── PHASE1_DEPLOYMENT_FINAL_STATUS.md
│   ├── PHASE1_DEPLOYMENT_GUIDE.md
│   ├── PHASE1_IMPLEMENTATION_COMPLETE.md
│   ├── PHASE3_COPILOT_OPTIMIZATION_COMPLETE.md
│   ├── PHASE5C_CORE_CONSISTENCY_OPTIMIZATION.md
│   ├── PHASE_3_COMPLETION_SUMMARY.md
│   ├── PHASE_4_SECURITY_BLUEPRINT.md
│   ├── PORTS_REGISTRY.md
│   ├── PR_DRAFT_feat_self_upgrade.md
│   ├── PRE_COMMIT_GUIDE.md
│   ├── PRODUCTION_HARDENING_PACK.md
│   ├── PRODUCTION_READY_CHECKLIST.md
│   ├── PROJECT_COMPLETION_FINAL_PROPOSAL.md
│   ├── PROJECT_COMPLETION_SUMMARY.md
│   ├── PROJECT_ERROR_ANALYSIS_COMPREHENSIVE.md
│   ├── PROJECT_OPTIMIZATION_COMPLETE_ROADMAP.md
│   ├── PROJECT_OPTIMIZATION_PROPOSAL_COMPREHENSIVE.md
│   ├── PROJECT_QUALITY_IMPROVEMENT_REPORT.md
│   ├── PROJECT_ROADMAP.md
│   ├── PULL_REQUEST_DRAFT.md
│   ├── PYTHON_ENVIRONMENT_STATUS.md
│   ├── QUALITY_BASELINE_REPORT.md
│   ├── QUALITY_GATES_COMPLETE.md
│   ├── QUALITY_GATES_REPORT.md
│   ├── QUALITY_GATES_RESTRUCTURED_UPDATE_COMPLETE.md
│   ├── QUALITY_GATES_UPDATED_GUIDE.md
│   ├── QUICK_CONTINUE_COMMANDS.md
│   ├── QUICK_REFERENCE_V3.md
│   ├── QUICK_START.md
│   ├── QUICK_START_LIBRARIES.md
│   ├── README.md
│   ├── README_Toolpack.md
│   ├── REFACTOR_EXECUTION_PLAN.md
│   ├── RESTRUCTURE_COMPLETION_REPORT.md
│   ├── RESTRUCTURE_DECISION_SUMMARY.md
│   ├── RESTRUCTURE_IMPLEMENTATION_GUIDE.md
│   ├── RESTRUCTURE_PROPOSAL_2025.md
│   ├── RESTRUCTURED_COMPLETION_SUMMARY.md
│   ├── RESTRUCTURING_COMPLETION_SUMMARY.md
│   ├── ROADMAP.md
│   ├── ROADMAP_USAGE_GUIDE.md
│   ├── ROOT_CONFIG_ADOPTION.md
│   ├── RUN_WEB_UI.md
│   ├── SAFE_CHUNKING_STRATEGY.md
│   ├── SAFE_ERROR_FIX_PLAN.md
│   ├── SAFE_PHASE2_IMPLEMENTATION_COMPLETE.md
│   ├── SAFE_PHASE2_WORK_ORDERS.md
│   ├── SAFE_PHASE3_ROADMAP.md
│   ├── SECURITY.md
│   ├── SECURITY_ARCHITECTURE_PRODUCTION_READY.md
│   ├── SECURITY_MODEL.md
│   ├── SELF_UPGRADE.md
│   ├── SERVICES_REFACTOR_COMPLETE.md
│   ├── SETUP_COMPLETE.md
│   ├── SETUP_SERVER.md
│   ├── SYSTEM_UPGRADE_REPORT.md
│   ├── TEACHER_STUDENT_SYSTEM_COMPLETE.md
│   ├── TOOLPACK_SETUP_COMPLETE.md
│   ├── TROUBLESHOOTING.md
│   ├── TUTORIAL.md
│   ├── ULTIMATE_INIT_OPTIMIZATION_COMPLETE.md
│   ├── UPGRADE_SYSTEM_SUCCESS_REPORT.md
│   ├── USER_GUIDE.md
│   ├── V1_COMMON_MIGRATION_COMPLETE_REPORT.md
│   ├── VAULT.md
│   ├── VENV_RECOGNITION_ISSUE_RESOLVED.md
│   ├── VN_COPILOT_DEEPSEEK_COACH_GUIDE.md
│   ├── VN_COPILOT_SIMPLIFIED_GUIDE.md
│   ├── VSCODE_OPTIMIZATION_COMPLETE.md
│   ├── VSCODE_ULTRA_LIGHT_GUIDE.md
│   ├── VSCODE_VENV_DIAGNOSTIC_REPORT.md
│   ├── VSCODE_VENV_FIX_CHECKLIST.md
│   ├── VSCODE_VENV_ROOT_CAUSE_ANALYSIS.md
│   ├── WINDOWS_SETUP.md
│   ├── WORK_ORDERS.md
│   ├── ZETA_AI_E2E_BLUEPRINT_2025.md
│   ├── ZETA_API_BLUEPRINT_COMPLETE.md
│   ├── ZETA_CONSISTENCY_PROPOSAL_VN.md
│   ├── ZETA_OPTIMIZATION_IMPLEMENTATION_GUIDE.md
│   ├── ZETA_OPTIMIZATION_MASTER_PLAN.md
│   ├── ZETA_VN_API_BLUEPRINT_IMPLEMENTATION_REPORT.md
│   └── ZETA_VN_OPTIMIZATION_PROPOSAL_2025.md
├── examples
│   ├── tests
│   │   └── test_turbo_ollama_usage_examples.py
│   └── turbo_ollama_usage_examples.py
├── extension
│   ├── .vscode-test
│   │   ├── extensions
│   │   │   └── extensions.json
│   │   ├── user-data
│   │   │   ├── Cache
│   │   │   ├── CachedData
│   │   │   ├── CachedProfilesData
│   │   │   ├── Code Cache
│   │   │   ├── Crashpad
│   │   │   ├── DawnGraphiteCache
│   │   │   ├── DawnWebGPUCache
│   │   │   ├── GPUCache
│   │   │   ├── Local Storage
│   │   │   ├── logs
│   │   │   ├── Network
│   │   │   ├── Session Storage
│   │   │   ├── Shared Dictionary
│   │   │   ├── User
│   │   │   ├── DIPS
│   │   │   ├── languagepacks.json
│   │   │   ├── Local State
│   │   │   ├── machineid
│   │   │   └── Preferences
│   │   └── vscode-win32-x64-archive-1.103.2
│   │       ├── appx
│   │       ├── bin
│   │       ├── locales
│   │       ├── policies
│   │       ├── resources
│   │       ├── tools
│   │       ├── chrome_100_percent.pak
│   │       ├── chrome_200_percent.pak
│   │       ├── Code.exe
│   │       ├── Code.VisualElementsManifest.xml
│   │       ├── d3dcompiler_47.dll
│   │       ├── ffmpeg.dll
│   │       ├── icudtl.dat
│   │       ├── is-complete
│   │       ├── libEGL.dll
│   │       ├── libGLESv2.dll
│   │       ├── LICENSES.chromium.html
│   │       ├── resources.pak
│   │       ├── snapshot_blob.bin
│   │       ├── v8_context_snapshot.bin
│   │       ├── vk_swiftshader.dll
│   │       ├── vk_swiftshader_icd.json
│   │       └── vulkan-1.dll
│   ├── deepseek-core
│   │   └── guardian
│   ├── media
│   │   ├── deepseek.png
│   │   ├── demo.gif
│   │   ├── screenshot1.png
│   │   └── screenshot2.png
│   ├── out
│   │   ├── __tests__
│   │   │   ├── __mocks__
│   │   │   ├── setup.js
│   │   │   └── setup.js.map
│   │   ├── ai
│   │   │   ├── ollamaClient.js
│   │   │   └── ollamaClient.js.map
│   │   ├── src
│   │   │   ├── aiAgent.js
│   │   │   ├── aiAgent.js.map
│   │   │   ├── extension.js
│   │   │   └── extension.js.map
│   │   ├── test
│   │   │   ├── aiAgent.test.js
│   │   │   ├── aiAgent.test.js.map
│   │   │   ├── cache.test.js
│   │   │   ├── cache.test.js.map
│   │   │   ├── extension.test.js
│   │   │   └── extension.test.js.map
│   │   ├── aiAgent.js
│   │   ├── aiAgent.js.map
│   │   ├── aiAgent_new.js
│   │   ├── aiAgent_new.js.map
│   │   ├── aiAgent_old.js
│   │   ├── aiAgent_old.js.map
│   │   ├── aiAgentClean.js
│   │   ├── aiAgentClean.js.map
│   │   ├── aiAgentFixed.js
│   │   ├── aiAgentFixed.js.map
│   │   ├── cache.js
│   │   ├── cache.js.map
│   │   ├── config.js
│   │   ├── config.js.map
│   │   ├── extension.js
│   │   ├── extension.js.map
│   │   ├── extension_original.js
│   │   ├── extension_original.js.map
│   │   ├── extensionClean.js
│   │   ├── extensionClean.js.map
│   │   ├── extensionNew.js
│   │   ├── extensionNew.js.map
│   │   ├── inlineCompletion.js
│   │   ├── inlineCompletion.js.map
│   │   ├── ollamaClient.js
│   │   ├── ollamaClient.js.map
│   │   ├── ollamaClient.test.js
│   │   ├── ollamaClient.test.js.map
│   │   ├── ollamaClientNew.js
│   │   ├── ollamaClientNew.js.map
│   │   ├── realtimeAnalyzer.js
│   │   ├── realtimeAnalyzer.js.map
│   │   ├── responseTypes.js
│   │   ├── responseTypes.js.map
│   │   ├── test-ollama.js
│   │   ├── test-ollama.js.map
│   │   ├── test-sample.js
│   │   ├── test-sample.js.map
│   │   ├── test_ollama_client.js
│   │   ├── test_ollama_client.js.map
│   │   ├── types.js
│   │   └── types.js.map
│   ├── src
│   │   ├── test
│   │   │   └── extension.test.ts
│   │   └── extension.ts
│   ├── web
│   │   ├── assets
│   │   │   ├── icons
│   │   │   ├── demo.mp4
│   │   │   ├── favicon.png
│   │   │   ├── screenshot1.png
│   │   │   ├── screenshot2.png
│   │   │   └── thumbnail.jpeg
│   │   ├── index.html
│   │   ├── main.js
│   │   └── style.css
│   ├── .env
│   ├── .gitignore
│   ├── .vscode-test.mjs
│   ├── .vscodeignore
│   ├── CHANGELOG.md
│   ├── deekseek-extension-1.0.1.vsix
│   ├── deepseek-extension-1.0.1.vsix
│   ├── eslint.config.mjs
│   ├── LICENSE
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   ├── tsconfig.json
│   └── webview.html
├── packages
│   ├── ollama
│   │   ├── src
│   │   │   ├── index.ts
│   │   │   ├── ollama-manager.ts
│   │   │   └── ollama-service.ts
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── test-integration.js
│   │   └── tsconfig.json
│   └── shared
│       ├── src
│       │   └── index.ts
│       ├── package.json
│       └── tsconfig.json
├── production
│   ├── .github
│   │   └── workflows
│   │       └── ci-cd.yml
│   ├── config
│   │   ├── production.json
│   │   └── turbo_config.json
│   ├── docs
│   │   └── DEPLOYMENT.md
│   ├── monitoring
│   │   └── prometheus.yml
│   ├── scripts
│   │   └── health_check.py
│   ├── src
│   │   ├── refactored
│   │   ├── tests
│   │   │   ├── test_ai_auto_refactor.py
│   │   │   ├── test_final_project_demo.py
│   │   │   └── test_turbo_demo.py
│   │   ├── ai_auto_optimizer.py
│   │   ├── ai_auto_refactor.py
│   │   ├── ai_project_scanner.py
│   │   ├── final_project_demo.py
│   │   └── turbo_demo.py
│   ├── DEPLOYMENT_SUMMARY.json
│   ├── DEPLOYMENT_SUMMARY.md
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── health_check_results.json
│   └── requirements.txt
├── refactored
│   ├── ai_auto_optimizer_refactored.py
│   ├── ai_project_scanner_refactored.py
│   ├── data_processor_refactored.py
│   ├── setuptools_validation_refactored.py
│   ├── test_ai_auto_optimizer_refactored.py
│   ├── test_ai_project_scanner_refactored.py
│   ├── test_data_processor_refactored.py
│   ├── test_generator_refactored.py
│   ├── test_setuptools_validation_refactored.py
│   └── test_test_generator_refactored.py
├── reports
│   ├── ai-codemod
│   │   ├── latest
│   │   │   ├── verify_stderr.txt
│   │   │   └── verify_stdout.txt
│   │   ├── analysis_20250907_230433.json
│   │   ├── analysis_20250907_230456.json
│   │   ├── analysis_20250907_230548.json
│   │   ├── analysis_20250907_231021.json
│   │   ├── analysis_20250908_073522.json
│   │   ├── analysis_20250908_073745.json
│   │   ├── analysis_20250908_073957.json
│   │   ├── analysis_20250908_074631.json
│   │   ├── analysis_20250908_142806.json
│   │   ├── analysis_20250908_183858.json
│   │   ├── analysis_20250908_185051.json
│   │   ├── analysis_20250908_185215.json
│   │   ├── analysis_20250908_185535.json
│   │   ├── analysis_20250908_192759.json
│   │   ├── analysis_20250908_193011.json
│   │   ├── analysis_20250908_201304.json
│   │   ├── analysis_20250908_201326.json
│   │   ├── analysis_20250908_201946.json
│   │   ├── application_20250908_142806.json
│   │   ├── application_20250908_185216.json
│   │   ├── application_20250908_201304.json
│   │   ├── application_20250908_201326.json
│   │   ├── application_20250908_201947.json
│   │   ├── latest.json
│   │   └── latest.md
│   ├── ai-monitor
│   │   ├── issues_20250908_034600.json
│   │   ├── issues_20250908_034600.md
│   │   ├── issues_20250908_035001.json
│   │   ├── issues_20250908_035001.md
│   │   ├── issues_20250908_035008.json
│   │   ├── issues_20250908_035008.md
│   │   ├── issues_20250908_035306.json
│   │   ├── issues_20250908_035306.md
│   │   ├── issues_20250908_035313.json
│   │   ├── issues_20250908_035313.md
│   │   ├── issues_20250908_035340.json
│   │   ├── issues_20250908_035340.md
│   │   ├── issues_20250908_035434.json
│   │   ├── issues_20250908_035434.md
│   │   ├── issues_20250908_035441.json
│   │   ├── issues_20250908_035441.md
│   │   ├── issues_20250908_035454.json
│   │   ├── issues_20250908_035454.md
│   │   ├── issues_20250908_035501.json
│   │   ├── issues_20250908_035501.md
│   │   ├── issues_20250908_035520.json
│   │   ├── issues_20250908_035520.md
│   │   ├── issues_20250908_035526.json
│   │   ├── issues_20250908_035526.md
│   │   ├── issues_20250908_035549.json
│   │   ├── issues_20250908_035549.md
│   │   ├── issues_20250908_035555.json
│   │   ├── issues_20250908_035555.md
│   │   ├── issues_20250908_035602.json
│   │   ├── issues_20250908_035602.md
│   │   ├── issues_20250908_035608.json
│   │   ├── issues_20250908_035608.md
│   │   ├── issues_20250908_035649.json
│   │   ├── issues_20250908_035649.md
│   │   ├── issues_20250908_035656.json
│   │   ├── issues_20250908_035656.md
│   │   ├── issues_20250908_035704.json
│   │   ├── issues_20250908_035704.md
│   │   ├── issues_20250908_035711.json
│   │   ├── issues_20250908_035711.md
│   │   ├── issues_20250908_035905.json
│   │   ├── issues_20250908_035905.md
│   │   ├── issues_20250908_035911.json
│   │   ├── issues_20250908_035911.md
│   │   ├── issues_20250908_035917.json
│   │   ├── issues_20250908_035917.md
│   │   ├── issues_20250908_035924.json
│   │   ├── issues_20250908_035924.md
│   │   ├── issues_20250908_035931.json
│   │   ├── issues_20250908_035931.md
│   │   ├── issues_20250908_035937.json
│   │   ├── issues_20250908_035937.md
│   │   ├── issues_20250908_035943.json
│   │   ├── issues_20250908_035943.md
│   │   ├── issues_20250908_035949.json
│   │   ├── issues_20250908_035949.md
│   │   ├── issues_20250908_035955.json
│   │   ├── issues_20250908_035955.md
│   │   ├── issues_20250908_040002.json
│   │   ├── issues_20250908_040002.md
│   │   ├── issues_20250908_040010.json
│   │   ├── issues_20250908_040010.md
│   │   ├── issues_20250908_040017.json
│   │   ├── issues_20250908_040017.md
│   │   ├── issues_20250908_040025.json
│   │   ├── issues_20250908_040025.md
│   │   ├── issues_20250908_040032.json
│   │   ├── issues_20250908_040032.md
│   │   ├── issues_20250908_040039.json
│   │   ├── issues_20250908_040039.md
│   │   ├── issues_20250908_040047.json
│   │   ├── issues_20250908_040047.md
│   │   ├── issues_20250908_040054.json
│   │   ├── issues_20250908_040054.md
│   │   ├── issues_20250908_040100.json
│   │   ├── issues_20250908_040100.md
│   │   ├── issues_20250908_040106.json
│   │   ├── issues_20250908_040106.md
│   │   ├── issues_20250908_040113.json
│   │   ├── issues_20250908_040113.md
│   │   ├── issues_20250908_040119.json
│   │   ├── issues_20250908_040119.md
│   │   ├── issues_20250908_040125.json
│   │   ├── issues_20250908_040125.md
│   │   ├── issues_20250908_040131.json
│   │   ├── issues_20250908_040131.md
│   │   ├── issues_20250908_040138.json
│   │   ├── issues_20250908_040138.md
│   │   ├── issues_20250908_040144.json
│   │   ├── issues_20250908_040144.md
│   │   ├── issues_20250908_040151.json
│   │   ├── issues_20250908_040151.md
│   │   ├── issues_20250908_040157.json
│   │   ├── issues_20250908_040157.md
│   │   ├── issues_20250908_040205.json
│   │   ├── issues_20250908_040205.md
│   │   ├── issues_20250908_040211.json
│   │   ├── issues_20250908_040211.md
│   │   ├── issues_20250908_040217.json
│   │   ├── issues_20250908_040217.md
│   │   ├── issues_20250908_040223.json
│   │   ├── issues_20250908_040223.md
│   │   ├── issues_20250908_040229.json
│   │   ├── issues_20250908_040229.md
│   │   ├── issues_20250908_040235.json
│   │   ├── issues_20250908_040235.md
│   │   ├── issues_20250908_040243.json
│   │   ├── issues_20250908_040243.md
│   │   ├── issues_20250908_040251.json
│   │   ├── issues_20250908_040251.md
│   │   ├── issues_20250908_040257.json
│   │   ├── issues_20250908_040257.md
│   │   ├── issues_20250908_040304.json
│   │   ├── issues_20250908_040304.md
│   │   ├── issues_20250908_040311.json
│   │   ├── issues_20250908_040311.md
│   │   ├── issues_20250908_040318.json
│   │   ├── issues_20250908_040318.md
│   │   ├── issues_20250908_040326.json
│   │   ├── issues_20250908_040326.md
│   │   ├── issues_20250908_040335.json
│   │   ├── issues_20250908_040335.md
│   │   ├── issues_20250908_040346.json
│   │   ├── issues_20250908_040346.md
│   │   ├── issues_20250908_040353.json
│   │   ├── issues_20250908_040353.md
│   │   ├── issues_20250908_040400.json
│   │   ├── issues_20250908_040400.md
│   │   ├── issues_20250908_040407.json
│   │   ├── issues_20250908_040407.md
│   │   ├── issues_20250908_040414.json
│   │   ├── issues_20250908_040414.md
│   │   ├── issues_20250908_040423.json
│   │   ├── issues_20250908_040423.md
│   │   ├── issues_20250908_040430.json
│   │   ├── issues_20250908_040430.md
│   │   ├── issues_20250908_040438.json
│   │   ├── issues_20250908_040438.md
│   │   ├── issues_20250908_040445.json
│   │   ├── issues_20250908_040445.md
│   │   ├── issues_20250908_040451.json
│   │   ├── issues_20250908_040451.md
│   │   ├── issues_20250908_040457.json
│   │   ├── issues_20250908_040457.md
│   │   ├── issues_20250908_040503.json
│   │   ├── issues_20250908_040503.md
│   │   ├── issues_20250908_040512.json
│   │   ├── issues_20250908_040512.md
│   │   ├── issues_20250908_040519.json
│   │   ├── issues_20250908_040519.md
│   │   ├── issues_20250908_040525.json
│   │   ├── issues_20250908_040525.md
│   │   ├── issues_20250908_040532.json
│   │   ├── issues_20250908_040532.md
│   │   ├── issues_20250908_040538.json
│   │   ├── issues_20250908_040538.md
│   │   ├── issues_20250908_064403.json
│   │   ├── issues_20250908_064403.md
│   │   ├── issues_20250908_064705.json
│   │   ├── issues_20250908_064705.md
│   │   ├── issues_20250908_064739.json
│   │   ├── issues_20250908_064739.md
│   │   ├── issues_20250908_064814.json
│   │   ├── issues_20250908_064814.md
│   │   ├── issues_20250908_064843.json
│   │   ├── issues_20250908_064843.md
│   │   ├── issues_20250908_064910.json
│   │   ├── issues_20250908_064910.md
│   │   ├── issues_20250908_064942.json
│   │   ├── issues_20250908_064942.md
│   │   ├── issues_20250908_065018.json
│   │   ├── issues_20250908_065018.md
│   │   ├── issues_20250908_065046.json
│   │   ├── issues_20250908_065046.md
│   │   ├── issues_20250908_065115.json
│   │   ├── issues_20250908_065115.md
│   │   ├── issues_20250908_065142.json
│   │   ├── issues_20250908_065142.md
│   │   ├── issues_20250908_065210.json
│   │   ├── issues_20250908_065210.md
│   │   ├── issues_20250908_065240.json
│   │   ├── issues_20250908_065240.md
│   │   ├── issues_20250908_065334.json
│   │   ├── issues_20250908_065334.md
│   │   ├── issues_20250908_065947.json
│   │   ├── issues_20250908_065947.md
│   │   ├── issues_20250908_070140.json
│   │   ├── issues_20250908_070140.md
│   │   ├── issues_20250908_070419.json
│   │   ├── issues_20250908_070419.md
│   │   ├── issues_20250908_070444.json
│   │   ├── issues_20250908_070444.md
│   │   ├── issues_20250908_070512.json
│   │   ├── issues_20250908_070512.md
│   │   ├── issues_20250908_070541.json
│   │   ├── issues_20250908_070541.md
│   │   ├── issues_20250908_070609.json
│   │   ├── issues_20250908_070609.md
│   │   ├── issues_20250908_070641.json
│   │   ├── issues_20250908_070641.md
│   │   ├── issues_20250908_070712.json
│   │   ├── issues_20250908_070712.md
│   │   ├── issues_20250908_070744.json
│   │   ├── issues_20250908_070744.md
│   │   ├── issues_20250908_070822.json
│   │   ├── issues_20250908_070822.md
│   │   ├── issues_20250908_070854.json
│   │   ├── issues_20250908_070854.md
│   │   ├── issues_20250908_070936.json
│   │   ├── issues_20250908_070936.md
│   │   ├── issues_20250908_071004.json
│   │   ├── issues_20250908_071004.md
│   │   ├── issues_20250908_071037.json
│   │   ├── issues_20250908_071037.md
│   │   ├── issues_20250908_071111.json
│   │   ├── issues_20250908_071111.md
│   │   ├── issues_20250908_071141.json
│   │   ├── issues_20250908_071141.md
│   │   ├── issues_20250908_071206.json
│   │   ├── issues_20250908_071206.md
│   │   ├── issues_20250908_071235.json
│   │   ├── issues_20250908_071235.md
│   │   ├── issues_20250908_071307.json
│   │   ├── issues_20250908_071307.md
│   │   ├── issues_20250908_071343.json
│   │   ├── issues_20250908_071343.md
│   │   ├── issues_20250908_071416.json
│   │   ├── issues_20250908_071416.md
│   │   ├── issues_20250908_071449.json
│   │   ├── issues_20250908_071449.md
│   │   ├── issues_20250908_071530.json
│   │   ├── issues_20250908_071530.md
│   │   ├── issues_20250908_071607.json
│   │   ├── issues_20250908_071607.md
│   │   ├── issues_20250908_071635.json
│   │   ├── issues_20250908_071635.md
│   │   ├── issues_20250908_071706.json
│   │   ├── issues_20250908_071706.md
│   │   ├── issues_20250908_071732.json
│   │   ├── issues_20250908_071732.md
│   │   ├── issues_20250908_071810.json
│   │   ├── issues_20250908_071810.md
│   │   ├── issues_20250908_071839.json
│   │   ├── issues_20250908_071839.md
│   │   ├── issues_20250908_071908.json
│   │   ├── issues_20250908_071908.md
│   │   ├── issues_20250908_071941.json
│   │   ├── issues_20250908_071941.md
│   │   ├── issues_20250908_072032.json
│   │   ├── issues_20250908_072032.md
│   │   ├── issues_20250908_072125.json
│   │   ├── issues_20250908_072125.md
│   │   ├── issues_20250908_072157.json
│   │   ├── issues_20250908_072157.md
│   │   ├── issues_20250908_072227.json
│   │   ├── issues_20250908_072227.md
│   │   ├── issues_20250908_072257.json
│   │   ├── issues_20250908_072257.md
│   │   ├── issues_20250908_072329.json
│   │   ├── issues_20250908_072329.md
│   │   ├── issues_20250908_072403.json
│   │   ├── issues_20250908_072403.md
│   │   ├── issues_20250908_072433.json
│   │   ├── issues_20250908_072433.md
│   │   ├── issues_20250908_072510.json
│   │   ├── issues_20250908_072510.md
│   │   ├── issues_20250908_072549.json
│   │   ├── issues_20250908_072549.md
│   │   ├── issues_20250908_072643.json
│   │   ├── issues_20250908_072643.md
│   │   ├── issues_20250908_072739.json
│   │   ├── issues_20250908_072739.md
│   │   ├── issues_20250908_072838.json
│   │   ├── issues_20250908_072838.md
│   │   ├── issues_20250908_072917.json
│   │   ├── issues_20250908_072917.md
│   │   ├── issues_20250908_072944.json
│   │   ├── issues_20250908_072944.md
│   │   ├── issues_20250908_073016.json
│   │   ├── issues_20250908_073016.md
│   │   ├── issues_20250908_073052.json
│   │   ├── issues_20250908_073052.md
│   │   ├── issues_20250908_073124.json
│   │   ├── issues_20250908_073124.md
│   │   ├── issues_20250908_073155.json
│   │   ├── issues_20250908_073155.md
│   │   ├── issues_20250908_073229.json
│   │   ├── issues_20250908_073229.md
│   │   ├── issues_20250908_073257.json
│   │   ├── issues_20250908_073257.md
│   │   ├── issues_20250908_073323.json
│   │   ├── issues_20250908_073323.md
│   │   ├── issues_20250908_073351.json
│   │   ├── issues_20250908_073351.md
│   │   ├── issues_20250908_073418.json
│   │   ├── issues_20250908_073418.md
│   │   ├── issues_20250908_073445.json
│   │   ├── issues_20250908_073445.md
│   │   ├── issues_20250908_073513.json
│   │   ├── issues_20250908_073513.md
│   │   ├── issues_20250908_073540.json
│   │   ├── issues_20250908_073540.md
│   │   ├── issues_20250908_073604.json
│   │   ├── issues_20250908_073604.md
│   │   ├── issues_20250908_073615.json
│   │   ├── issues_20250908_073615.md
│   │   ├── issues_20250908_073624.json
│   │   ├── issues_20250908_073624.md
│   │   ├── issues_20250908_073632.json
│   │   ├── issues_20250908_073632.md
│   │   ├── issues_20250908_073641.json
│   │   ├── issues_20250908_073641.md
│   │   ├── issues_20250908_073648.json
│   │   ├── issues_20250908_073648.md
│   │   ├── issues_20250908_073656.json
│   │   ├── issues_20250908_073656.md
│   │   ├── issues_20250908_073704.json
│   │   ├── issues_20250908_073704.md
│   │   ├── issues_20250908_073711.json
│   │   ├── issues_20250908_073711.md
│   │   ├── issues_20250908_073719.json
│   │   ├── issues_20250908_073719.md
│   │   ├── issues_20250908_073726.json
│   │   ├── issues_20250908_073726.md
│   │   ├── issues_20250908_073734.json
│   │   ├── issues_20250908_073734.md
│   │   ├── issues_20250908_073741.json
│   │   ├── issues_20250908_073741.md
│   │   ├── issues_20250908_073750.json
│   │   ├── issues_20250908_073750.md
│   │   ├── issues_20250908_073800.json
│   │   ├── issues_20250908_073800.md
│   │   ├── issues_20250908_073812.json
│   │   ├── issues_20250908_073812.md
│   │   ├── issues_20250908_073822.json
│   │   ├── issues_20250908_073822.md
│   │   ├── issues_20250908_073832.json
│   │   ├── issues_20250908_073832.md
│   │   ├── issues_20250908_073842.json
│   │   ├── issues_20250908_073842.md
│   │   ├── issues_20250908_073851.json
│   │   ├── issues_20250908_073851.md
│   │   ├── issues_20250908_073900.json
│   │   ├── issues_20250908_073900.md
│   │   ├── issues_20250908_073909.json
│   │   ├── issues_20250908_073909.md
│   │   ├── issues_20250908_073917.json
│   │   ├── issues_20250908_073917.md
│   │   ├── issues_20250908_073926.json
│   │   ├── issues_20250908_073926.md
│   │   ├── issues_20250908_073935.json
│   │   ├── issues_20250908_073935.md
│   │   ├── issues_20250908_073943.json
│   │   ├── issues_20250908_073943.md
│   │   ├── issues_20250908_073952.json
│   │   ├── issues_20250908_073952.md
│   │   ├── issues_20250908_074002.json
│   │   ├── issues_20250908_074002.md
│   │   ├── issues_20250908_074013.json
│   │   ├── issues_20250908_074013.md
│   │   ├── issues_20250908_074025.json
│   │   ├── issues_20250908_074025.md
│   │   ├── issues_20250908_074036.json
│   │   ├── issues_20250908_074036.md
│   │   ├── issues_20250908_074046.json
│   │   ├── issues_20250908_074046.md
│   │   ├── issues_20250908_074055.json
│   │   ├── issues_20250908_074055.md
│   │   ├── issues_20250908_074102.json
│   │   ├── issues_20250908_074102.md
│   │   ├── issues_20250908_074109.json
│   │   ├── issues_20250908_074109.md
│   │   ├── issues_20250908_074117.json
│   │   ├── issues_20250908_074117.md
│   │   ├── issues_20250908_074124.json
│   │   ├── issues_20250908_074124.md
│   │   ├── issues_20250908_074132.json
│   │   ├── issues_20250908_074132.md
│   │   ├── issues_20250908_074140.json
│   │   ├── issues_20250908_074140.md
│   │   ├── issues_20250908_074147.json
│   │   ├── issues_20250908_074147.md
│   │   ├── issues_20250908_074154.json
│   │   ├── issues_20250908_074154.md
│   │   ├── issues_20250908_074201.json
│   │   ├── issues_20250908_074201.md
│   │   ├── issues_20250908_074207.json
│   │   ├── issues_20250908_074207.md
│   │   ├── issues_20250908_074213.json
│   │   ├── issues_20250908_074213.md
│   │   ├── issues_20250908_074220.json
│   │   ├── issues_20250908_074220.md
│   │   ├── issues_20250908_074226.json
│   │   ├── issues_20250908_074226.md
│   │   ├── issues_20250908_074233.json
│   │   ├── issues_20250908_074233.md
│   │   ├── issues_20250908_074240.json
│   │   ├── issues_20250908_074240.md
│   │   ├── issues_20250908_074248.json
│   │   ├── issues_20250908_074248.md
│   │   ├── issues_20250908_074256.json
│   │   ├── issues_20250908_074256.md
│   │   ├── issues_20250908_074304.json
│   │   ├── issues_20250908_074304.md
│   │   ├── issues_20250908_074312.json
│   │   ├── issues_20250908_074312.md
│   │   ├── issues_20250908_074321.json
│   │   ├── issues_20250908_074321.md
│   │   ├── issues_20250908_074331.json
│   │   ├── issues_20250908_074331.md
│   │   ├── issues_20250908_074339.json
│   │   ├── issues_20250908_074339.md
│   │   ├── issues_20250908_074346.json
│   │   ├── issues_20250908_074346.md
│   │   ├── issues_20250908_074353.json
│   │   ├── issues_20250908_074353.md
│   │   ├── issues_20250908_074400.json
│   │   ├── issues_20250908_074400.md
│   │   ├── issues_20250908_074408.json
│   │   ├── issues_20250908_074408.md
│   │   ├── issues_20250908_074415.json
│   │   ├── issues_20250908_074415.md
│   │   ├── issues_20250908_074422.json
│   │   ├── issues_20250908_074422.md
│   │   ├── issues_20250908_074433.json
│   │   ├── issues_20250908_074433.md
│   │   ├── issues_20250908_074442.json
│   │   ├── issues_20250908_074442.md
│   │   ├── issues_20250908_074448.json
│   │   ├── issues_20250908_074448.md
│   │   ├── issues_20250908_074456.json
│   │   ├── issues_20250908_074456.md
│   │   ├── issues_20250908_074504.json
│   │   ├── issues_20250908_074504.md
│   │   ├── issues_20250908_074512.json
│   │   ├── issues_20250908_074512.md
│   │   ├── issues_20250908_074522.json
│   │   ├── issues_20250908_074522.md
│   │   ├── issues_20250908_074530.json
│   │   ├── issues_20250908_074530.md
│   │   ├── issues_20250908_074539.json
│   │   ├── issues_20250908_074539.md
│   │   ├── issues_20250908_074548.json
│   │   ├── issues_20250908_074548.md
│   │   ├── issues_20250908_074556.json
│   │   ├── issues_20250908_074556.md
│   │   ├── issues_20250908_074605.json
│   │   ├── issues_20250908_074605.md
│   │   ├── issues_20250908_074615.json
│   │   ├── issues_20250908_074615.md
│   │   ├── issues_20250908_074625.json
│   │   ├── issues_20250908_074625.md
│   │   ├── issues_20250908_074638.json
│   │   ├── issues_20250908_074638.md
│   │   ├── issues_20250908_074651.json
│   │   ├── issues_20250908_074651.md
│   │   ├── issues_20250908_074705.json
│   │   ├── issues_20250908_074705.md
│   │   ├── issues_20250908_074717.json
│   │   ├── issues_20250908_074717.md
│   │   ├── issues_20250908_074726.json
│   │   ├── issues_20250908_074726.md
│   │   ├── issues_20250908_074735.json
│   │   ├── issues_20250908_074735.md
│   │   ├── issues_20250908_074744.json
│   │   ├── issues_20250908_074744.md
│   │   ├── issues_20250908_074753.json
│   │   ├── issues_20250908_074753.md
│   │   ├── issues_20250908_074802.json
│   │   ├── issues_20250908_074802.md
│   │   ├── issues_20250908_074811.json
│   │   ├── issues_20250908_074811.md
│   │   ├── issues_20250908_074820.json
│   │   ├── issues_20250908_074820.md
│   │   ├── issues_20250908_074829.json
│   │   ├── issues_20250908_074829.md
│   │   ├── issues_20250908_074837.json
│   │   ├── issues_20250908_074837.md
│   │   ├── issues_20250908_074845.json
│   │   ├── issues_20250908_074845.md
│   │   ├── issues_20250908_074852.json
│   │   ├── issues_20250908_074852.md
│   │   ├── issues_20250908_074859.json
│   │   ├── issues_20250908_074859.md
│   │   ├── issues_20250908_074906.json
│   │   ├── issues_20250908_074906.md
│   │   ├── issues_20250908_074913.json
│   │   ├── issues_20250908_074913.md
│   │   ├── issues_20250908_074921.json
│   │   ├── issues_20250908_074921.md
│   │   ├── issues_20250908_074928.json
│   │   ├── issues_20250908_074928.md
│   │   ├── issues_20250908_074935.json
│   │   ├── issues_20250908_074935.md
│   │   ├── issues_20250908_074942.json
│   │   ├── issues_20250908_074942.md
│   │   ├── issues_20250908_074950.json
│   │   ├── issues_20250908_074950.md
│   │   ├── issues_20250908_074957.json
│   │   ├── issues_20250908_074957.md
│   │   ├── issues_20250908_075005.json
│   │   ├── issues_20250908_075005.md
│   │   ├── issues_20250908_075012.json
│   │   ├── issues_20250908_075012.md
│   │   ├── issues_20250908_075020.json
│   │   ├── issues_20250908_075020.md
│   │   ├── issues_20250908_075028.json
│   │   ├── issues_20250908_075028.md
│   │   ├── issues_20250908_075036.json
│   │   ├── issues_20250908_075036.md
│   │   ├── issues_20250908_075044.json
│   │   ├── issues_20250908_075044.md
│   │   ├── issues_20250908_075051.json
│   │   ├── issues_20250908_075051.md
│   │   ├── issues_20250908_075059.json
│   │   ├── issues_20250908_075059.md
│   │   ├── issues_20250908_075106.json
│   │   ├── issues_20250908_075106.md
│   │   ├── issues_20250908_075113.json
│   │   ├── issues_20250908_075113.md
│   │   ├── issues_20250908_075120.json
│   │   ├── issues_20250908_075120.md
│   │   ├── issues_20250908_075128.json
│   │   ├── issues_20250908_075128.md
│   │   ├── issues_20250908_075137.json
│   │   ├── issues_20250908_075137.md
│   │   ├── issues_20250908_075144.json
│   │   ├── issues_20250908_075144.md
│   │   ├── issues_20250908_075151.json
│   │   ├── issues_20250908_075151.md
│   │   ├── issues_20250908_075159.json
│   │   ├── issues_20250908_075159.md
│   │   ├── issues_20250908_075209.json
│   │   ├── issues_20250908_075209.md
│   │   ├── issues_20250908_075219.json
│   │   ├── issues_20250908_075219.md
│   │   ├── issues_20250908_075228.json
│   │   ├── issues_20250908_075228.md
│   │   ├── issues_20250908_075237.json
│   │   ├── issues_20250908_075237.md
│   │   ├── issues_20250908_075245.json
│   │   ├── issues_20250908_075245.md
│   │   ├── issues_20250908_075254.json
│   │   ├── issues_20250908_075254.md
│   │   ├── issues_20250908_075303.json
│   │   ├── issues_20250908_075303.md
│   │   ├── issues_20250908_075311.json
│   │   ├── issues_20250908_075311.md
│   │   ├── issues_20250908_075320.json
│   │   ├── issues_20250908_075320.md
│   │   ├── issues_20250908_075330.json
│   │   ├── issues_20250908_075330.md
│   │   ├── issues_20250908_075341.json
│   │   ├── issues_20250908_075341.md
│   │   ├── issues_20250908_075351.json
│   │   ├── issues_20250908_075351.md
│   │   ├── issues_20250908_075401.json
│   │   ├── issues_20250908_075401.md
│   │   ├── issues_20250908_075411.json
│   │   ├── issues_20250908_075411.md
│   │   ├── issues_20250908_075422.json
│   │   ├── issues_20250908_075422.md
│   │   ├── issues_20250908_075432.json
│   │   ├── issues_20250908_075432.md
│   │   ├── issues_20250908_075442.json
│   │   ├── issues_20250908_075442.md
│   │   ├── issues_20250908_075453.json
│   │   ├── issues_20250908_075453.md
│   │   ├── issues_20250908_075503.json
│   │   ├── issues_20250908_075503.md
│   │   ├── issues_20250908_075513.json
│   │   ├── issues_20250908_075513.md
│   │   ├── issues_20250908_075523.json
│   │   ├── issues_20250908_075523.md
│   │   ├── issues_20250908_075533.json
│   │   ├── issues_20250908_075533.md
│   │   ├── issues_20250908_075544.json
│   │   ├── issues_20250908_075544.md
│   │   ├── issues_20250908_075557.json
│   │   ├── issues_20250908_075557.md
│   │   ├── issues_20250908_075616.json
│   │   ├── issues_20250908_075616.md
│   │   ├── issues_20250908_075636.json
│   │   ├── issues_20250908_075636.md
│   │   ├── issues_20250908_075656.json
│   │   ├── issues_20250908_075656.md
│   │   ├── issues_20250908_075716.json
│   │   ├── issues_20250908_075716.md
│   │   ├── issues_20250908_075734.json
│   │   ├── issues_20250908_075734.md
│   │   ├── issues_20250908_075750.json
│   │   ├── issues_20250908_075750.md
│   │   ├── issues_20250908_075805.json
│   │   ├── issues_20250908_075805.md
│   │   ├── issues_20250908_075822.json
│   │   ├── issues_20250908_075822.md
│   │   ├── issues_20250908_075838.json
│   │   ├── issues_20250908_075838.md
│   │   ├── issues_20250908_075854.json
│   │   ├── issues_20250908_075854.md
│   │   ├── issues_20250908_075910.json
│   │   ├── issues_20250908_075910.md
│   │   ├── issues_20250908_075926.json
│   │   ├── issues_20250908_075926.md
│   │   ├── issues_20250908_075942.json
│   │   ├── issues_20250908_075942.md
│   │   ├── issues_20250908_075959.json
│   │   ├── issues_20250908_075959.md
│   │   ├── issues_20250908_080014.json
│   │   ├── issues_20250908_080014.md
│   │   ├── issues_20250908_080029.json
│   │   ├── issues_20250908_080029.md
│   │   ├── issues_20250908_080047.json
│   │   ├── issues_20250908_080047.md
│   │   ├── issues_20250908_080105.json
│   │   ├── issues_20250908_080105.md
│   │   ├── issues_20250908_080121.json
│   │   ├── issues_20250908_080121.md
│   │   ├── issues_20250908_080137.json
│   │   ├── issues_20250908_080137.md
│   │   ├── issues_20250908_080153.json
│   │   ├── issues_20250908_080153.md
│   │   ├── issues_20250908_080209.json
│   │   ├── issues_20250908_080209.md
│   │   ├── issues_20250908_080225.json
│   │   ├── issues_20250908_080225.md
│   │   ├── issues_20250908_080239.json
│   │   ├── issues_20250908_080239.md
│   │   ├── issues_20250908_080253.json
│   │   ├── issues_20250908_080253.md
│   │   ├── issues_20250908_080307.json
│   │   ├── issues_20250908_080307.md
│   │   ├── issues_20250908_080321.json
│   │   ├── issues_20250908_080321.md
│   │   ├── issues_20250908_080336.json
│   │   ├── issues_20250908_080336.md
│   │   ├── issues_20250908_080349.json
│   │   ├── issues_20250908_080349.md
│   │   ├── issues_20250908_080405.json
│   │   ├── issues_20250908_080405.md
│   │   ├── issues_20250908_080418.json
│   │   ├── issues_20250908_080418.md
│   │   ├── issues_20250908_080433.json
│   │   ├── issues_20250908_080433.md
│   │   ├── issues_20250908_080447.json
│   │   ├── issues_20250908_080447.md
│   │   ├── issues_20250908_080501.json
│   │   ├── issues_20250908_080501.md
│   │   ├── issues_20250908_080516.json
│   │   ├── issues_20250908_080516.md
│   │   ├── issues_20250908_080530.json
│   │   ├── issues_20250908_080530.md
│   │   ├── issues_20250908_080545.json
│   │   ├── issues_20250908_080545.md
│   │   ├── issues_20250908_080559.json
│   │   ├── issues_20250908_080559.md
│   │   ├── issues_20250908_080613.json
│   │   ├── issues_20250908_080613.md
│   │   ├── issues_20250908_080628.json
│   │   ├── issues_20250908_080628.md
│   │   ├── issues_20250908_080642.json
│   │   ├── issues_20250908_080642.md
│   │   ├── issues_20250908_080657.json
│   │   ├── issues_20250908_080657.md
│   │   ├── issues_20250908_080711.json
│   │   ├── issues_20250908_080711.md
│   │   ├── issues_20250908_080725.json
│   │   ├── issues_20250908_080725.md
│   │   ├── issues_20250908_080740.json
│   │   ├── issues_20250908_080740.md
│   │   ├── issues_20250908_080754.json
│   │   ├── issues_20250908_080754.md
│   │   ├── issues_20250908_080808.json
│   │   ├── issues_20250908_080808.md
│   │   ├── issues_20250908_080823.json
│   │   ├── issues_20250908_080823.md
│   │   ├── issues_20250908_080837.json
│   │   ├── issues_20250908_080837.md
│   │   ├── issues_20250908_080852.json
│   │   ├── issues_20250908_080852.md
│   │   ├── issues_20250908_080906.json
│   │   ├── issues_20250908_080906.md
│   │   ├── issues_20250908_080920.json
│   │   ├── issues_20250908_080920.md
│   │   ├── issues_20250908_080934.json
│   │   ├── issues_20250908_080934.md
│   │   ├── issues_20250908_080949.json
│   │   ├── issues_20250908_080949.md
│   │   ├── issues_20250908_081003.json
│   │   ├── issues_20250908_081003.md
│   │   ├── issues_20250908_081018.json
│   │   ├── issues_20250908_081018.md
│   │   ├── issues_20250908_081032.json
│   │   ├── issues_20250908_081032.md
│   │   ├── issues_20250908_081046.json
│   │   ├── issues_20250908_081046.md
│   │   ├── issues_20250908_081100.json
│   │   ├── issues_20250908_081100.md
│   │   ├── issues_20250908_081115.json
│   │   ├── issues_20250908_081115.md
│   │   ├── issues_20250908_081129.json
│   │   ├── issues_20250908_081129.md
│   │   ├── issues_20250908_081144.json
│   │   ├── issues_20250908_081144.md
│   │   ├── issues_20250908_081158.json
│   │   ├── issues_20250908_081158.md
│   │   ├── issues_20250908_081213.json
│   │   ├── issues_20250908_081213.md
│   │   ├── issues_20250908_081227.json
│   │   ├── issues_20250908_081227.md
│   │   ├── issues_20250908_081241.json
│   │   ├── issues_20250908_081241.md
│   │   ├── issues_20250908_081255.json
│   │   ├── issues_20250908_081255.md
│   │   ├── issues_20250908_081309.json
│   │   ├── issues_20250908_081309.md
│   │   ├── issues_20250908_081322.json
│   │   ├── issues_20250908_081322.md
│   │   ├── issues_20250908_081337.json
│   │   ├── issues_20250908_081337.md
│   │   ├── issues_20250908_081351.json
│   │   ├── issues_20250908_081351.md
│   │   ├── issues_20250908_081405.json
│   │   ├── issues_20250908_081405.md
│   │   ├── issues_20250908_081420.json
│   │   ├── issues_20250908_081420.md
│   │   ├── issues_20250908_081434.json
│   │   ├── issues_20250908_081434.md
│   │   ├── issues_20250908_081448.json
│   │   ├── issues_20250908_081448.md
│   │   ├── issues_20250908_081503.json
│   │   ├── issues_20250908_081503.md
│   │   ├── issues_20250908_081517.json
│   │   ├── issues_20250908_081517.md
│   │   ├── issues_20250908_081530.json
│   │   ├── issues_20250908_081530.md
│   │   ├── issues_20250908_081545.json
│   │   ├── issues_20250908_081545.md
│   │   ├── issues_20250908_081559.json
│   │   ├── issues_20250908_081559.md
│   │   ├── issues_20250908_081613.json
│   │   ├── issues_20250908_081613.md
│   │   ├── issues_20250908_081627.json
│   │   ├── issues_20250908_081627.md
│   │   ├── issues_20250908_081642.json
│   │   ├── issues_20250908_081642.md
│   │   ├── issues_20250908_081656.json
│   │   ├── issues_20250908_081656.md
│   │   ├── issues_20250908_081711.json
│   │   ├── issues_20250908_081711.md
│   │   ├── issues_20250908_081725.json
│   │   ├── issues_20250908_081725.md
│   │   ├── issues_20250908_081739.json
│   │   ├── issues_20250908_081739.md
│   │   ├── issues_20250908_081753.json
│   │   ├── issues_20250908_081753.md
│   │   ├── issues_20250908_081806.json
│   │   ├── issues_20250908_081806.md
│   │   ├── issues_20250908_081820.json
│   │   ├── issues_20250908_081820.md
│   │   ├── issues_20250908_081835.json
│   │   ├── issues_20250908_081835.md
│   │   ├── issues_20250908_081849.json
│   │   ├── issues_20250908_081849.md
│   │   ├── issues_20250908_081903.json
│   │   ├── issues_20250908_081903.md
│   │   ├── issues_20250908_081918.json
│   │   ├── issues_20250908_081918.md
│   │   ├── issues_20250908_081932.json
│   │   ├── issues_20250908_081932.md
│   │   ├── issues_20250908_081946.json
│   │   ├── issues_20250908_081946.md
│   │   ├── issues_20250908_082000.json
│   │   ├── issues_20250908_082000.md
│   │   ├── issues_20250908_082015.json
│   │   ├── issues_20250908_082015.md
│   │   ├── issues_20250908_082029.json
│   │   ├── issues_20250908_082029.md
│   │   ├── issues_20250908_082043.json
│   │   ├── issues_20250908_082043.md
│   │   ├── issues_20250908_082057.json
│   │   ├── issues_20250908_082057.md
│   │   ├── issues_20250908_082112.json
│   │   ├── issues_20250908_082112.md
│   │   ├── issues_20250908_082127.json
│   │   ├── issues_20250908_082127.md
│   │   ├── issues_20250908_082142.json
│   │   ├── issues_20250908_082142.md
│   │   ├── issues_20250908_082156.json
│   │   ├── issues_20250908_082156.md
│   │   ├── issues_20250908_082209.json
│   │   ├── issues_20250908_082209.md
│   │   ├── issues_20250908_082223.json
│   │   ├── issues_20250908_082223.md
│   │   ├── issues_20250908_082237.json
│   │   ├── issues_20250908_082237.md
│   │   ├── issues_20250908_082252.json
│   │   ├── issues_20250908_082252.md
│   │   ├── issues_20250908_082305.json
│   │   ├── issues_20250908_082305.md
│   │   ├── issues_20250908_082320.json
│   │   ├── issues_20250908_082320.md
│   │   ├── issues_20250908_082334.json
│   │   ├── issues_20250908_082334.md
│   │   ├── issues_20250908_082348.json
│   │   ├── issues_20250908_082348.md
│   │   ├── issues_20250908_082403.json
│   │   ├── issues_20250908_082403.md
│   │   ├── issues_20250908_082417.json
│   │   ├── issues_20250908_082417.md
│   │   ├── issues_20250908_082431.json
│   │   ├── issues_20250908_082431.md
│   │   ├── issues_20250908_082445.json
│   │   ├── issues_20250908_082445.md
│   │   ├── issues_20250908_082500.json
│   │   ├── issues_20250908_082500.md
│   │   ├── issues_20250908_082514.json
│   │   ├── issues_20250908_082514.md
│   │   ├── issues_20250908_082528.json
│   │   ├── issues_20250908_082528.md
│   │   ├── issues_20250908_082543.json
│   │   ├── issues_20250908_082543.md
│   │   ├── issues_20250908_082557.json
│   │   ├── issues_20250908_082557.md
│   │   ├── issues_20250908_082616.json
│   │   ├── issues_20250908_082616.md
│   │   ├── issues_20250908_082636.json
│   │   ├── issues_20250908_082636.md
│   │   ├── issues_20250908_082658.json
│   │   ├── issues_20250908_082658.md
│   │   ├── issues_20250908_082718.json
│   │   ├── issues_20250908_082718.md
│   │   ├── issues_20250908_082733.json
│   │   ├── issues_20250908_082733.md
│   │   ├── issues_20250908_082748.json
│   │   ├── issues_20250908_082748.md
│   │   ├── issues_20250908_082802.json
│   │   ├── issues_20250908_082802.md
│   │   ├── issues_20250908_082817.json
│   │   ├── issues_20250908_082817.md
│   │   ├── issues_20250908_082832.json
│   │   ├── issues_20250908_082832.md
│   │   ├── issues_20250908_082846.json
│   │   ├── issues_20250908_082846.md
│   │   ├── issues_20250908_082900.json
│   │   ├── issues_20250908_082900.md
│   │   ├── issues_20250908_082916.json
│   │   ├── issues_20250908_082916.md
│   │   ├── issues_20250908_082930.json
│   │   ├── issues_20250908_082930.md
│   │   ├── issues_20250908_082944.json
│   │   ├── issues_20250908_082944.md
│   │   ├── issues_20250908_082959.json
│   │   ├── issues_20250908_082959.md
│   │   ├── issues_20250908_083012.json
│   │   ├── issues_20250908_083012.md
│   │   ├── issues_20250908_083025.json
│   │   ├── issues_20250908_083025.md
│   │   ├── issues_20250908_083037.json
│   │   ├── issues_20250908_083037.md
│   │   ├── issues_20250908_083050.json
│   │   ├── issues_20250908_083050.md
│   │   ├── issues_20250908_083102.json
│   │   ├── issues_20250908_083102.md
│   │   ├── issues_20250908_083115.json
│   │   ├── issues_20250908_083115.md
│   │   ├── issues_20250908_083129.json
│   │   ├── issues_20250908_083129.md
│   │   ├── issues_20250908_083142.json
│   │   ├── issues_20250908_083142.md
│   │   ├── issues_20250908_083155.json
│   │   ├── issues_20250908_083155.md
│   │   ├── issues_20250908_083208.json
│   │   ├── issues_20250908_083208.md
│   │   ├── issues_20250908_083221.json
│   │   ├── issues_20250908_083221.md
│   │   ├── issues_20250908_083235.json
│   │   ├── issues_20250908_083235.md
│   │   ├── issues_20250908_083248.json
│   │   ├── issues_20250908_083248.md
│   │   ├── issues_20250908_083301.json
│   │   ├── issues_20250908_083301.md
│   │   ├── issues_20250908_083315.json
│   │   ├── issues_20250908_083315.md
│   │   ├── issues_20250908_083329.json
│   │   ├── issues_20250908_083329.md
│   │   ├── issues_20250908_083342.json
│   │   ├── issues_20250908_083342.md
│   │   ├── issues_20250908_083356.json
│   │   ├── issues_20250908_083356.md
│   │   ├── issues_20250908_083410.json
│   │   ├── issues_20250908_083410.md
│   │   ├── issues_20250908_083423.json
│   │   ├── issues_20250908_083423.md
│   │   ├── issues_20250908_083437.json
│   │   ├── issues_20250908_083437.md
│   │   ├── issues_20250908_083450.json
│   │   ├── issues_20250908_083450.md
│   │   ├── issues_20250908_083504.json
│   │   ├── issues_20250908_083504.md
│   │   ├── issues_20250908_083518.json
│   │   ├── issues_20250908_083518.md
│   │   ├── issues_20250908_083532.json
│   │   ├── issues_20250908_083532.md
│   │   ├── issues_20250908_083545.json
│   │   ├── issues_20250908_083545.md
│   │   ├── issues_20250908_083559.json
│   │   ├── issues_20250908_083559.md
│   │   ├── issues_20250908_083612.json
│   │   ├── issues_20250908_083612.md
│   │   ├── issues_20250908_083626.json
│   │   ├── issues_20250908_083626.md
│   │   ├── issues_20250908_083640.json
│   │   ├── issues_20250908_083640.md
│   │   ├── issues_20250908_083654.json
│   │   ├── issues_20250908_083654.md
│   │   ├── issues_20250908_083708.json
│   │   ├── issues_20250908_083708.md
│   │   ├── issues_20250908_083722.json
│   │   ├── issues_20250908_083722.md
│   │   ├── issues_20250908_083735.json
│   │   ├── issues_20250908_083735.md
│   │   ├── issues_20250908_083749.json
│   │   ├── issues_20250908_083749.md
│   │   ├── issues_20250908_083803.json
│   │   ├── issues_20250908_083803.md
│   │   ├── issues_20250908_083816.json
│   │   ├── issues_20250908_083816.md
│   │   ├── issues_20250908_083830.json
│   │   ├── issues_20250908_083830.md
│   │   ├── issues_20250908_083844.json
│   │   ├── issues_20250908_083844.md
│   │   ├── issues_20250908_083858.json
│   │   ├── issues_20250908_083858.md
│   │   ├── issues_20250908_083912.json
│   │   ├── issues_20250908_083912.md
│   │   ├── issues_20250908_083925.json
│   │   ├── issues_20250908_083925.md
│   │   ├── issues_20250908_083939.json
│   │   ├── issues_20250908_083939.md
│   │   ├── issues_20250908_083953.json
│   │   ├── issues_20250908_083953.md
│   │   ├── issues_20250908_084006.json
│   │   ├── issues_20250908_084006.md
│   │   ├── issues_20250908_084020.json
│   │   ├── issues_20250908_084020.md
│   │   ├── issues_20250908_084034.json
│   │   ├── issues_20250908_084034.md
│   │   ├── issues_20250908_084048.json
│   │   ├── issues_20250908_084048.md
│   │   ├── issues_20250908_084102.json
│   │   ├── issues_20250908_084102.md
│   │   ├── issues_20250908_084115.json
│   │   ├── issues_20250908_084115.md
│   │   ├── issues_20250908_084129.json
│   │   ├── issues_20250908_084129.md
│   │   ├── issues_20250908_084143.json
│   │   ├── issues_20250908_084143.md
│   │   ├── issues_20250908_084157.json
│   │   ├── issues_20250908_084157.md
│   │   ├── issues_20250908_084211.json
│   │   ├── issues_20250908_084211.md
│   │   ├── issues_20250908_084225.json
│   │   ├── issues_20250908_084225.md
│   │   ├── issues_20250908_084238.json
│   │   ├── issues_20250908_084238.md
│   │   ├── issues_20250908_084252.json
│   │   ├── issues_20250908_084252.md
│   │   ├── issues_20250908_084306.json
│   │   ├── issues_20250908_084306.md
│   │   ├── issues_20250908_084320.json
│   │   ├── issues_20250908_084320.md
│   │   ├── issues_20250908_084334.json
│   │   ├── issues_20250908_084334.md
│   │   ├── issues_20250908_084348.json
│   │   ├── issues_20250908_084348.md
│   │   ├── issues_20250908_084403.json
│   │   ├── issues_20250908_084403.md
│   │   ├── issues_20250908_084417.json
│   │   ├── issues_20250908_084417.md
│   │   ├── issues_20250908_084431.json
│   │   ├── issues_20250908_084431.md
│   │   ├── issues_20250908_084447.json
│   │   ├── issues_20250908_084447.md
│   │   ├── issues_20250908_084501.json
│   │   ├── issues_20250908_084501.md
│   │   ├── issues_20250908_084515.json
│   │   ├── issues_20250908_084515.md
│   │   ├── issues_20250908_084529.json
│   │   ├── issues_20250908_084529.md
│   │   ├── issues_20250908_084544.json
│   │   ├── issues_20250908_084544.md
│   │   ├── issues_20250908_084558.json
│   │   ├── issues_20250908_084558.md
│   │   ├── issues_20250908_084612.json
│   │   ├── issues_20250908_084612.md
│   │   ├── issues_20250908_084626.json
│   │   ├── issues_20250908_084626.md
│   │   ├── issues_20250908_084640.json
│   │   ├── issues_20250908_084640.md
│   │   ├── issues_20250908_084653.json
│   │   ├── issues_20250908_084653.md
│   │   ├── issues_20250908_084708.json
│   │   ├── issues_20250908_084708.md
│   │   ├── issues_20250908_084722.json
│   │   ├── issues_20250908_084722.md
│   │   ├── issues_20250908_084736.json
│   │   ├── issues_20250908_084736.md
│   │   ├── issues_20250908_084750.json
│   │   ├── issues_20250908_084750.md
│   │   ├── issues_20250908_084804.json
│   │   ├── issues_20250908_084804.md
│   │   ├── issues_20250908_084818.json
│   │   ├── issues_20250908_084818.md
│   │   ├── issues_20250908_084832.json
│   │   ├── issues_20250908_084832.md
│   │   ├── issues_20250908_084845.json
│   │   ├── issues_20250908_084845.md
│   │   ├── issues_20250908_084858.json
│   │   ├── issues_20250908_084858.md
│   │   ├── issues_20250908_084912.json
│   │   ├── issues_20250908_084912.md
│   │   ├── issues_20250908_084925.json
│   │   ├── issues_20250908_084925.md
│   │   ├── issues_20250908_084938.json
│   │   ├── issues_20250908_084938.md
│   │   ├── issues_20250908_084951.json
│   │   ├── issues_20250908_084951.md
│   │   ├── issues_20250908_085006.json
│   │   ├── issues_20250908_085006.md
│   │   ├── issues_20250908_085019.json
│   │   ├── issues_20250908_085019.md
│   │   ├── issues_20250908_085033.json
│   │   ├── issues_20250908_085033.md
│   │   ├── issues_20250908_085047.json
│   │   ├── issues_20250908_085047.md
│   │   ├── issues_20250908_085101.json
│   │   ├── issues_20250908_085101.md
│   │   ├── issues_20250908_085114.json
│   │   ├── issues_20250908_085114.md
│   │   ├── issues_20250908_085128.json
│   │   ├── issues_20250908_085128.md
│   │   ├── issues_20250908_085142.json
│   │   ├── issues_20250908_085142.md
│   │   ├── issues_20250908_085156.json
│   │   ├── issues_20250908_085156.md
│   │   ├── issues_20250908_085210.json
│   │   ├── issues_20250908_085210.md
│   │   ├── issues_20250908_085224.json
│   │   ├── issues_20250908_085224.md
│   │   ├── issues_20250908_085238.json
│   │   ├── issues_20250908_085238.md
│   │   ├── issues_20250908_085252.json
│   │   ├── issues_20250908_085252.md
│   │   ├── issues_20250908_085306.json
│   │   ├── issues_20250908_085306.md
│   │   ├── issues_20250908_085320.json
│   │   ├── issues_20250908_085320.md
│   │   ├── issues_20250908_085334.json
│   │   ├── issues_20250908_085334.md
│   │   ├── issues_20250908_085348.json
│   │   ├── issues_20250908_085348.md
│   │   ├── issues_20250908_085402.json
│   │   ├── issues_20250908_085402.md
│   │   ├── issues_20250908_085416.json
│   │   ├── issues_20250908_085416.md
│   │   ├── issues_20250908_085430.json
│   │   ├── issues_20250908_085430.md
│   │   ├── issues_20250908_085444.json
│   │   ├── issues_20250908_085444.md
│   │   ├── issues_20250908_085457.json
│   │   ├── issues_20250908_085457.md
│   │   ├── issues_20250908_085511.json
│   │   ├── issues_20250908_085511.md
│   │   ├── issues_20250908_085524.json
│   │   ├── issues_20250908_085524.md
│   │   ├── issues_20250908_085538.json
│   │   ├── issues_20250908_085538.md
│   │   ├── issues_20250908_085552.json
│   │   ├── issues_20250908_085552.md
│   │   ├── issues_20250908_085605.json
│   │   ├── issues_20250908_085605.md
│   │   ├── issues_20250908_085618.json
│   │   ├── issues_20250908_085618.md
│   │   ├── issues_20250908_085631.json
│   │   ├── issues_20250908_085631.md
│   │   ├── issues_20250908_085644.json
│   │   ├── issues_20250908_085644.md
│   │   ├── issues_20250908_085657.json
│   │   ├── issues_20250908_085657.md
│   │   ├── issues_20250908_085711.json
│   │   ├── issues_20250908_085711.md
│   │   ├── issues_20250908_085724.json
│   │   ├── issues_20250908_085724.md
│   │   ├── issues_20250908_085738.json
│   │   ├── issues_20250908_085738.md
│   │   ├── issues_20250908_085750.json
│   │   ├── issues_20250908_085750.md
│   │   ├── issues_20250908_085804.json
│   │   ├── issues_20250908_085804.md
│   │   ├── issues_20250908_085817.json
│   │   ├── issues_20250908_085817.md
│   │   ├── issues_20250908_085830.json
│   │   ├── issues_20250908_085830.md
│   │   ├── issues_20250908_085843.json
│   │   ├── issues_20250908_085843.md
│   │   ├── issues_20250908_085857.json
│   │   ├── issues_20250908_085857.md
│   │   ├── issues_20250908_085911.json
│   │   ├── issues_20250908_085911.md
│   │   ├── issues_20250908_085926.json
│   │   ├── issues_20250908_085926.md
│   │   ├── issues_20250908_085941.json
│   │   ├── issues_20250908_085941.md
│   │   ├── issues_20250908_085955.json
│   │   ├── issues_20250908_085955.md
│   │   ├── issues_20250908_090009.json
│   │   ├── issues_20250908_090009.md
│   │   ├── issues_20250908_090023.json
│   │   ├── issues_20250908_090023.md
│   │   ├── issues_20250908_090037.json
│   │   ├── issues_20250908_090037.md
│   │   ├── issues_20250908_090051.json
│   │   ├── issues_20250908_090051.md
│   │   ├── issues_20250908_090105.json
│   │   ├── issues_20250908_090105.md
│   │   ├── issues_20250908_090119.json
│   │   ├── issues_20250908_090119.md
│   │   ├── issues_20250908_090134.json
│   │   ├── issues_20250908_090134.md
│   │   ├── issues_20250908_090147.json
│   │   ├── issues_20250908_090147.md
│   │   ├── issues_20250908_090201.json
│   │   ├── issues_20250908_090201.md
│   │   ├── issues_20250908_090214.json
│   │   ├── issues_20250908_090214.md
│   │   ├── issues_20250908_090228.json
│   │   ├── issues_20250908_090228.md
│   │   ├── issues_20250908_090242.json
│   │   ├── issues_20250908_090242.md
│   │   ├── issues_20250908_090256.json
│   │   ├── issues_20250908_090256.md
│   │   ├── issues_20250908_090310.json
│   │   ├── issues_20250908_090310.md
│   │   ├── issues_20250908_090324.json
│   │   ├── issues_20250908_090324.md
│   │   ├── issues_20250908_090337.json
│   │   ├── issues_20250908_090337.md
│   │   ├── issues_20250908_090352.json
│   │   ├── issues_20250908_090352.md
│   │   ├── issues_20250908_090405.json
│   │   ├── issues_20250908_090405.md
│   │   ├── issues_20250908_090420.json
│   │   ├── issues_20250908_090420.md
│   │   ├── issues_20250908_090434.json
│   │   ├── issues_20250908_090434.md
│   │   ├── issues_20250908_090447.json
│   │   ├── issues_20250908_090447.md
│   │   ├── issues_20250908_090500.json
│   │   ├── issues_20250908_090500.md
│   │   ├── issues_20250908_090513.json
│   │   ├── issues_20250908_090513.md
│   │   ├── issues_20250908_090526.json
│   │   ├── issues_20250908_090526.md
│   │   ├── issues_20250908_090540.json
│   │   ├── issues_20250908_090540.md
│   │   ├── issues_20250908_090553.json
│   │   ├── issues_20250908_090553.md
│   │   ├── issues_20250908_090606.json
│   │   ├── issues_20250908_090606.md
│   │   ├── issues_20250908_090619.json
│   │   ├── issues_20250908_090619.md
│   │   ├── issues_20250908_090633.json
│   │   ├── issues_20250908_090633.md
│   │   ├── issues_20250908_090646.json
│   │   ├── issues_20250908_090646.md
│   │   ├── issues_20250908_090700.json
│   │   ├── issues_20250908_090700.md
│   │   ├── issues_20250908_090713.json
│   │   ├── issues_20250908_090713.md
│   │   ├── issues_20250908_090725.json
│   │   ├── issues_20250908_090725.md
│   │   ├── issues_20250908_090739.json
│   │   ├── issues_20250908_090739.md
│   │   ├── issues_20250908_090751.json
│   │   ├── issues_20250908_090751.md
│   │   ├── issues_20250908_090805.json
│   │   ├── issues_20250908_090805.md
│   │   ├── issues_20250908_090818.json
│   │   ├── issues_20250908_090818.md
│   │   ├── issues_20250908_090832.json
│   │   ├── issues_20250908_090832.md
│   │   ├── issues_20250908_090845.json
│   │   ├── issues_20250908_090845.md
│   │   ├── issues_20250908_090858.json
│   │   ├── issues_20250908_090858.md
│   │   ├── issues_20250908_090912.json
│   │   ├── issues_20250908_090912.md
│   │   ├── issues_20250908_090925.json
│   │   ├── issues_20250908_090925.md
│   │   ├── issues_20250908_090939.json
│   │   ├── issues_20250908_090939.md
│   │   ├── issues_20250908_090952.json
│   │   ├── issues_20250908_090952.md
│   │   ├── issues_20250908_091005.json
│   │   ├── issues_20250908_091005.md
│   │   ├── issues_20250908_091018.json
│   │   ├── issues_20250908_091018.md
│   │   ├── issues_20250908_091032.json
│   │   ├── issues_20250908_091032.md
│   │   ├── issues_20250908_091046.json
│   │   ├── issues_20250908_091046.md
│   │   ├── issues_20250908_091100.json
│   │   ├── issues_20250908_091100.md
│   │   ├── issues_20250908_091114.json
│   │   ├── issues_20250908_091114.md
│   │   ├── issues_20250908_091128.json
│   │   ├── issues_20250908_091128.md
│   │   ├── issues_20250908_091142.json
│   │   ├── issues_20250908_091142.md
│   │   ├── issues_20250908_091155.json
│   │   ├── issues_20250908_091155.md
│   │   ├── issues_20250908_091210.json
│   │   ├── issues_20250908_091210.md
│   │   ├── issues_20250908_091224.json
│   │   ├── issues_20250908_091224.md
│   │   ├── issues_20250908_091238.json
│   │   ├── issues_20250908_091238.md
│   │   ├── issues_20250908_091252.json
│   │   ├── issues_20250908_091252.md
│   │   ├── issues_20250908_091307.json
│   │   ├── issues_20250908_091307.md
│   │   ├── issues_20250908_091321.json
│   │   ├── issues_20250908_091321.md
│   │   ├── issues_20250908_091334.json
│   │   ├── issues_20250908_091334.md
│   │   ├── issues_20250908_091348.json
│   │   ├── issues_20250908_091348.md
│   │   ├── issues_20250908_091403.json
│   │   ├── issues_20250908_091403.md
│   │   ├── issues_20250908_091419.json
│   │   ├── issues_20250908_091419.md
│   │   ├── issues_20250908_091433.json
│   │   ├── issues_20250908_091433.md
│   │   ├── issues_20250908_091447.json
│   │   ├── issues_20250908_091447.md
│   │   ├── issues_20250908_091501.json
│   │   ├── issues_20250908_091501.md
│   │   ├── issues_20250908_091515.json
│   │   ├── issues_20250908_091515.md
│   │   ├── issues_20250908_091529.json
│   │   ├── issues_20250908_091529.md
│   │   ├── issues_20250908_091543.json
│   │   ├── issues_20250908_091543.md
│   │   ├── issues_20250908_091557.json
│   │   ├── issues_20250908_091557.md
│   │   ├── issues_20250908_091611.json
│   │   ├── issues_20250908_091611.md
│   │   ├── issues_20250908_091624.json
│   │   ├── issues_20250908_091624.md
│   │   ├── issues_20250908_091639.json
│   │   ├── issues_20250908_091639.md
│   │   ├── issues_20250908_091653.json
│   │   ├── issues_20250908_091653.md
│   │   ├── issues_20250908_091707.json
│   │   ├── issues_20250908_091707.md
│   │   ├── issues_20250908_091721.json
│   │   ├── issues_20250908_091721.md
│   │   ├── issues_20250908_091735.json
│   │   ├── issues_20250908_091735.md
│   │   ├── issues_20250908_091748.json
│   │   ├── issues_20250908_091748.md
│   │   ├── issues_20250908_091801.json
│   │   ├── issues_20250908_091801.md
│   │   ├── issues_20250908_091815.json
│   │   ├── issues_20250908_091815.md
│   │   ├── issues_20250908_091829.json
│   │   ├── issues_20250908_091829.md
│   │   ├── issues_20250908_091842.json
│   │   ├── issues_20250908_091842.md
│   │   ├── issues_20250908_091856.json
│   │   ├── issues_20250908_091856.md
│   │   ├── issues_20250908_091910.json
│   │   ├── issues_20250908_091910.md
│   │   ├── issues_20250908_091924.json
│   │   ├── issues_20250908_091924.md
│   │   ├── issues_20250908_091938.json
│   │   ├── issues_20250908_091938.md
│   │   ├── issues_20250908_091951.json
│   │   ├── issues_20250908_091951.md
│   │   ├── issues_20250908_092004.json
│   │   ├── issues_20250908_092004.md
│   │   ├── issues_20250908_092017.json
│   │   ├── issues_20250908_092017.md
│   │   ├── issues_20250908_092030.json
│   │   ├── issues_20250908_092030.md
│   │   ├── issues_20250908_092043.json
│   │   ├── issues_20250908_092043.md
│   │   ├── issues_20250908_092057.json
│   │   ├── issues_20250908_092057.md
│   │   ├── issues_20250908_092111.json
│   │   ├── issues_20250908_092111.md
│   │   ├── issues_20250908_092125.json
│   │   ├── issues_20250908_092125.md
│   │   ├── issues_20250908_092140.json
│   │   ├── issues_20250908_092140.md
│   │   ├── issues_20250908_092155.json
│   │   ├── issues_20250908_092155.md
│   │   ├── issues_20250908_092209.json
│   │   ├── issues_20250908_092209.md
│   │   ├── issues_20250908_092223.json
│   │   ├── issues_20250908_092223.md
│   │   ├── issues_20250908_092237.json
│   │   ├── issues_20250908_092237.md
│   │   ├── issues_20250908_092251.json
│   │   ├── issues_20250908_092251.md
│   │   ├── issues_20250908_092305.json
│   │   ├── issues_20250908_092305.md
│   │   ├── issues_20250908_092319.json
│   │   ├── issues_20250908_092319.md
│   │   ├── issues_20250908_092333.json
│   │   ├── issues_20250908_092333.md
│   │   ├── issues_20250908_092347.json
│   │   ├── issues_20250908_092347.md
│   │   ├── issues_20250908_092401.json
│   │   ├── issues_20250908_092401.md
│   │   ├── issues_20250908_092415.json
│   │   ├── issues_20250908_092415.md
│   │   ├── issues_20250908_092429.json
│   │   ├── issues_20250908_092429.md
│   │   ├── issues_20250908_092443.json
│   │   ├── issues_20250908_092443.md
│   │   ├── issues_20250908_092457.json
│   │   ├── issues_20250908_092457.md
│   │   ├── issues_20250908_092511.json
│   │   ├── issues_20250908_092511.md
│   │   ├── issues_20250908_092525.json
│   │   ├── issues_20250908_092525.md
│   │   ├── issues_20250908_092539.json
│   │   ├── issues_20250908_092539.md
│   │   ├── issues_20250908_092553.json
│   │   ├── issues_20250908_092553.md
│   │   ├── issues_20250908_092606.json
│   │   ├── issues_20250908_092606.md
│   │   ├── issues_20250908_092620.json
│   │   ├── issues_20250908_092620.md
│   │   ├── issues_20250908_092636.json
│   │   ├── issues_20250908_092636.md
│   │   ├── issues_20250908_092652.json
│   │   ├── issues_20250908_092652.md
│   │   ├── issues_20250908_092707.json
│   │   ├── issues_20250908_092707.md
│   │   ├── issues_20250908_092724.json
│   │   ├── issues_20250908_092724.md
│   │   ├── issues_20250908_092739.json
│   │   ├── issues_20250908_092739.md
│   │   ├── issues_20250908_092756.json
│   │   ├── issues_20250908_092756.md
│   │   ├── issues_20250908_092813.json
│   │   ├── issues_20250908_092813.md
│   │   ├── issues_20250908_092828.json
│   │   ├── issues_20250908_092828.md
│   │   ├── issues_20250908_092846.json
│   │   ├── issues_20250908_092846.md
│   │   ├── issues_20250908_092901.json
│   │   ├── issues_20250908_092901.md
│   │   ├── issues_20250908_092914.json
│   │   ├── issues_20250908_092914.md
│   │   ├── issues_20250908_092931.json
│   │   ├── issues_20250908_092931.md
│   │   ├── issues_20250908_092948.json
│   │   ├── issues_20250908_092948.md
│   │   ├── issues_20250908_093003.json
│   │   ├── issues_20250908_093003.md
│   │   ├── issues_20250908_093011.json
│   │   ├── issues_20250908_093011.md
│   │   ├── issues_20250908_093018.json
│   │   ├── issues_20250908_093018.md
│   │   ├── issues_20250908_093025.json
│   │   ├── issues_20250908_093025.md
│   │   ├── issues_20250908_093032.json
│   │   ├── issues_20250908_093032.md
│   │   ├── issues_20250908_093039.json
│   │   ├── issues_20250908_093039.md
│   │   ├── issues_20250908_093046.json
│   │   ├── issues_20250908_093046.md
│   │   ├── issues_20250908_093053.json
│   │   ├── issues_20250908_093053.md
│   │   ├── issues_20250908_093101.json
│   │   ├── issues_20250908_093101.md
│   │   ├── issues_20250908_093108.json
│   │   ├── issues_20250908_093108.md
│   │   ├── issues_20250908_093115.json
│   │   ├── issues_20250908_093115.md
│   │   ├── issues_20250908_093122.json
│   │   ├── issues_20250908_093122.md
│   │   ├── issues_20250908_093128.json
│   │   ├── issues_20250908_093128.md
│   │   ├── issues_20250908_093135.json
│   │   ├── issues_20250908_093135.md
│   │   ├── issues_20250908_093142.json
│   │   ├── issues_20250908_093142.md
│   │   ├── issues_20250908_093148.json
│   │   ├── issues_20250908_093148.md
│   │   ├── issues_20250908_093155.json
│   │   ├── issues_20250908_093155.md
│   │   ├── issues_20250908_093202.json
│   │   ├── issues_20250908_093202.md
│   │   ├── issues_20250908_093208.json
│   │   ├── issues_20250908_093208.md
│   │   ├── issues_20250908_093215.json
│   │   ├── issues_20250908_093215.md
│   │   ├── issues_20250908_093222.json
│   │   ├── issues_20250908_093222.md
│   │   ├── issues_20250908_093230.json
│   │   ├── issues_20250908_093230.md
│   │   ├── issues_20250908_093237.json
│   │   ├── issues_20250908_093237.md
│   │   ├── issues_20250908_093245.json
│   │   ├── issues_20250908_093245.md
│   │   ├── issues_20250908_093253.json
│   │   ├── issues_20250908_093253.md
│   │   ├── issues_20250908_093300.json
│   │   ├── issues_20250908_093300.md
│   │   ├── issues_20250908_093308.json
│   │   ├── issues_20250908_093308.md
│   │   ├── issues_20250908_093315.json
│   │   ├── issues_20250908_093315.md
│   │   ├── issues_20250908_093323.json
│   │   ├── issues_20250908_093323.md
│   │   ├── issues_20250908_093330.json
│   │   ├── issues_20250908_093330.md
│   │   ├── issues_20250908_093338.json
│   │   ├── issues_20250908_093338.md
│   │   ├── issues_20250908_093345.json
│   │   ├── issues_20250908_093345.md
│   │   ├── issues_20250908_093352.json
│   │   ├── issues_20250908_093352.md
│   │   ├── issues_20250908_093358.json
│   │   ├── issues_20250908_093358.md
│   │   ├── issues_20250908_093405.json
│   │   ├── issues_20250908_093405.md
│   │   ├── issues_20250908_093411.json
│   │   ├── issues_20250908_093411.md
│   │   ├── issues_20250908_093417.json
│   │   ├── issues_20250908_093417.md
│   │   ├── issues_20250908_093424.json
│   │   ├── issues_20250908_093424.md
│   │   ├── issues_20250908_093430.json
│   │   ├── issues_20250908_093430.md
│   │   ├── issues_20250908_093437.json
│   │   ├── issues_20250908_093437.md
│   │   ├── issues_20250908_093443.json
│   │   ├── issues_20250908_093443.md
│   │   ├── issues_20250908_093450.json
│   │   ├── issues_20250908_093450.md
│   │   ├── issues_20250908_093456.json
│   │   ├── issues_20250908_093456.md
│   │   ├── issues_20250908_093502.json
│   │   ├── issues_20250908_093502.md
│   │   ├── issues_20250908_093509.json
│   │   ├── issues_20250908_093509.md
│   │   ├── issues_20250908_093515.json
│   │   ├── issues_20250908_093515.md
│   │   ├── issues_20250908_093522.json
│   │   ├── issues_20250908_093522.md
│   │   ├── issues_20250908_093528.json
│   │   ├── issues_20250908_093528.md
│   │   ├── issues_20250908_093535.json
│   │   ├── issues_20250908_093535.md
│   │   ├── issues_20250908_093541.json
│   │   ├── issues_20250908_093541.md
│   │   ├── issues_20250908_093548.json
│   │   ├── issues_20250908_093548.md
│   │   ├── issues_20250908_093554.json
│   │   ├── issues_20250908_093554.md
│   │   ├── issues_20250908_093600.json
│   │   ├── issues_20250908_093600.md
│   │   ├── issues_20250908_093606.json
│   │   ├── issues_20250908_093606.md
│   │   ├── issues_20250908_093613.json
│   │   ├── issues_20250908_093613.md
│   │   ├── issues_20250908_093619.json
│   │   ├── issues_20250908_093619.md
│   │   ├── issues_20250908_093626.json
│   │   ├── issues_20250908_093626.md
│   │   ├── issues_20250908_093632.json
│   │   ├── issues_20250908_093632.md
│   │   ├── issues_20250908_093638.json
│   │   ├── issues_20250908_093638.md
│   │   ├── issues_20250908_093645.json
│   │   ├── issues_20250908_093645.md
│   │   ├── issues_20250908_093651.json
│   │   ├── issues_20250908_093651.md
│   │   ├── issues_20250908_093658.json
│   │   ├── issues_20250908_093658.md
│   │   ├── issues_20250908_093704.json
│   │   ├── issues_20250908_093704.md
│   │   ├── issues_20250908_093711.json
│   │   ├── issues_20250908_093711.md
│   │   ├── issues_20250908_093717.json
│   │   ├── issues_20250908_093717.md
│   │   ├── issues_20250908_093725.json
│   │   ├── issues_20250908_093725.md
│   │   ├── issues_20250908_093732.json
│   │   ├── issues_20250908_093732.md
│   │   ├── issues_20250908_093739.json
│   │   ├── issues_20250908_093739.md
│   │   ├── issues_20250908_093747.json
│   │   ├── issues_20250908_093747.md
│   │   ├── issues_20250908_093754.json
│   │   ├── issues_20250908_093754.md
│   │   ├── issues_20250908_093801.json
│   │   ├── issues_20250908_093801.md
│   │   ├── issues_20250908_093808.json
│   │   ├── issues_20250908_093808.md
│   │   ├── issues_20250908_093815.json
│   │   ├── issues_20250908_093815.md
│   │   ├── issues_20250908_093822.json
│   │   ├── issues_20250908_093822.md
│   │   ├── issues_20250908_093829.json
│   │   ├── issues_20250908_093829.md
│   │   ├── issues_20250908_093836.json
│   │   ├── issues_20250908_093836.md
│   │   ├── issues_20250908_093843.json
│   │   ├── issues_20250908_093843.md
│   │   ├── issues_20250908_093851.json
│   │   ├── issues_20250908_093851.md
│   │   ├── issues_20250908_093859.json
│   │   ├── issues_20250908_093859.md
│   │   ├── issues_20250908_093907.json
│   │   ├── issues_20250908_093907.md
│   │   ├── issues_20250908_093914.json
│   │   ├── issues_20250908_093914.md
│   │   ├── issues_20250908_093922.json
│   │   ├── issues_20250908_093922.md
│   │   ├── issues_20250908_093930.json
│   │   ├── issues_20250908_093930.md
│   │   ├── issues_20250908_093938.json
│   │   ├── issues_20250908_093938.md
│   │   ├── issues_20250908_093951.json
│   │   ├── issues_20250908_093951.md
│   │   ├── issues_20250908_093959.json
│   │   ├── issues_20250908_093959.md
│   │   ├── issues_20250908_094006.json
│   │   ├── issues_20250908_094006.md
│   │   ├── issues_20250908_094013.json
│   │   ├── issues_20250908_094013.md
│   │   ├── issues_20250908_094019.json
│   │   ├── issues_20250908_094019.md
│   │   ├── issues_20250908_094025.json
│   │   ├── issues_20250908_094025.md
│   │   ├── issues_20250908_094032.json
│   │   ├── issues_20250908_094032.md
│   │   ├── issues_20250908_094038.json
│   │   ├── issues_20250908_094038.md
│   │   ├── issues_20250908_094045.json
│   │   ├── issues_20250908_094045.md
│   │   ├── issues_20250908_094051.json
│   │   ├── issues_20250908_094051.md
│   │   ├── issues_20250908_094057.json
│   │   ├── issues_20250908_094057.md
│   │   ├── issues_20250908_094104.json
│   │   ├── issues_20250908_094104.md
│   │   ├── issues_20250908_094111.json
│   │   ├── issues_20250908_094111.md
│   │   ├── issues_20250908_094117.json
│   │   ├── issues_20250908_094117.md
│   │   ├── issues_20250908_094124.json
│   │   ├── issues_20250908_094124.md
│   │   ├── issues_20250908_094131.json
│   │   ├── issues_20250908_094131.md
│   │   ├── issues_20250908_094137.json
│   │   ├── issues_20250908_094137.md
│   │   ├── issues_20250908_094144.json
│   │   ├── issues_20250908_094144.md
│   │   ├── issues_20250908_094150.json
│   │   ├── issues_20250908_094150.md
│   │   ├── issues_20250908_094156.json
│   │   ├── issues_20250908_094156.md
│   │   ├── issues_20250908_094203.json
│   │   ├── issues_20250908_094203.md
│   │   ├── issues_20250908_094209.json
│   │   ├── issues_20250908_094209.md
│   │   ├── issues_20250908_094216.json
│   │   ├── issues_20250908_094216.md
│   │   ├── issues_20250908_094222.json
│   │   ├── issues_20250908_094222.md
│   │   ├── issues_20250908_094228.json
│   │   ├── issues_20250908_094228.md
│   │   ├── issues_20250908_094235.json
│   │   ├── issues_20250908_094235.md
│   │   ├── issues_20250908_094241.json
│   │   ├── issues_20250908_094241.md
│   │   ├── issues_20250908_094248.json
│   │   ├── issues_20250908_094248.md
│   │   ├── issues_20250908_094254.json
│   │   ├── issues_20250908_094254.md
│   │   ├── issues_20250908_094300.json
│   │   ├── issues_20250908_094300.md
│   │   ├── issues_20250908_094307.json
│   │   ├── issues_20250908_094307.md
│   │   ├── issues_20250908_094313.json
│   │   ├── issues_20250908_094313.md
│   │   ├── issues_20250908_094320.json
│   │   ├── issues_20250908_094320.md
│   │   ├── issues_20250908_094326.json
│   │   ├── issues_20250908_094326.md
│   │   ├── issues_20250908_094332.json
│   │   ├── issues_20250908_094332.md
│   │   ├── issues_20250908_094339.json
│   │   ├── issues_20250908_094339.md
│   │   ├── issues_20250908_094346.json
│   │   ├── issues_20250908_094346.md
│   │   ├── issues_20250908_094352.json
│   │   ├── issues_20250908_094352.md
│   │   ├── issues_20250908_094358.json
│   │   ├── issues_20250908_094358.md
│   │   ├── issues_20250908_094405.json
│   │   ├── issues_20250908_094405.md
│   │   ├── issues_20250908_094412.json
│   │   ├── issues_20250908_094412.md
│   │   ├── issues_20250908_094419.json
│   │   ├── issues_20250908_094419.md
│   │   ├── issues_20250908_094426.json
│   │   ├── issues_20250908_094426.md
│   │   ├── issues_20250908_094434.json
│   │   ├── issues_20250908_094434.md
│   │   ├── issues_20250908_094443.json
│   │   ├── issues_20250908_094443.md
│   │   ├── issues_20250908_094452.json
│   │   ├── issues_20250908_094452.md
│   │   ├── issues_20250908_094500.json
│   │   ├── issues_20250908_094500.md
│   │   ├── issues_20250908_094507.json
│   │   ├── issues_20250908_094507.md
│   │   ├── issues_20250908_094514.json
│   │   ├── issues_20250908_094514.md
│   │   ├── issues_20250908_094520.json
│   │   ├── issues_20250908_094520.md
│   │   ├── issues_20250908_094527.json
│   │   ├── issues_20250908_094527.md
│   │   ├── issues_20250908_094534.json
│   │   ├── issues_20250908_094534.md
│   │   ├── issues_20250908_094541.json
│   │   ├── issues_20250908_094541.md
│   │   ├── issues_20250908_094548.json
│   │   ├── issues_20250908_094548.md
│   │   ├── issues_20250908_094554.json
│   │   ├── issues_20250908_094554.md
│   │   ├── issues_20250908_094601.json
│   │   ├── issues_20250908_094601.md
│   │   ├── issues_20250908_094608.json
│   │   ├── issues_20250908_094608.md
│   │   ├── issues_20250908_094614.json
│   │   ├── issues_20250908_094614.md
│   │   ├── issues_20250908_094621.json
│   │   ├── issues_20250908_094621.md
│   │   ├── issues_20250908_094628.json
│   │   ├── issues_20250908_094628.md
│   │   ├── issues_20250908_094634.json
│   │   ├── issues_20250908_094634.md
│   │   ├── issues_20250908_094641.json
│   │   ├── issues_20250908_094641.md
│   │   ├── issues_20250908_094647.json
│   │   ├── issues_20250908_094647.md
│   │   ├── issues_20250908_094653.json
│   │   ├── issues_20250908_094653.md
│   │   ├── issues_20250908_094700.json
│   │   ├── issues_20250908_094700.md
│   │   ├── issues_20250908_094706.json
│   │   ├── issues_20250908_094706.md
│   │   ├── issues_20250908_094713.json
│   │   ├── issues_20250908_094713.md
│   │   ├── issues_20250908_094719.json
│   │   ├── issues_20250908_094719.md
│   │   ├── issues_20250908_094727.json
│   │   ├── issues_20250908_094727.md
│   │   ├── issues_20250908_094734.json
│   │   ├── issues_20250908_094734.md
│   │   ├── issues_20250908_094742.json
│   │   ├── issues_20250908_094742.md
│   │   ├── issues_20250908_094750.json
│   │   ├── issues_20250908_094750.md
│   │   ├── issues_20250908_094759.json
│   │   ├── issues_20250908_094759.md
│   │   ├── issues_20250908_094813.json
│   │   ├── issues_20250908_094813.md
│   │   ├── issues_20250908_094826.json
│   │   ├── issues_20250908_094826.md
│   │   ├── issues_20250908_094833.json
│   │   ├── issues_20250908_094833.md
│   │   ├── issues_20250908_094839.json
│   │   ├── issues_20250908_094839.md
│   │   ├── issues_20250908_094846.json
│   │   ├── issues_20250908_094846.md
│   │   ├── issues_20250908_094854.json
│   │   ├── issues_20250908_094854.md
│   │   ├── issues_20250908_094902.json
│   │   ├── issues_20250908_094902.md
│   │   ├── issues_20250908_094910.json
│   │   ├── issues_20250908_094910.md
│   │   ├── issues_20250908_094917.json
│   │   ├── issues_20250908_094917.md
│   │   ├── issues_20250908_094924.json
│   │   ├── issues_20250908_094924.md
│   │   ├── issues_20250908_094931.json
│   │   ├── issues_20250908_094931.md
│   │   ├── issues_20250908_094939.json
│   │   ├── issues_20250908_094939.md
│   │   ├── issues_20250908_094946.json
│   │   ├── issues_20250908_094946.md
│   │   ├── issues_20250908_094953.json
│   │   ├── issues_20250908_094953.md
│   │   ├── issues_20250908_095000.json
│   │   ├── issues_20250908_095000.md
│   │   ├── issues_20250908_095013.json
│   │   ├── issues_20250908_095013.md
│   │   ├── issues_20250908_095022.json
│   │   ├── issues_20250908_095022.md
│   │   ├── issues_20250908_095031.json
│   │   ├── issues_20250908_095031.md
│   │   ├── issues_20250908_095040.json
│   │   ├── issues_20250908_095040.md
│   │   ├── issues_20250908_095049.json
│   │   ├── issues_20250908_095049.md
│   │   ├── issues_20250908_095058.json
│   │   ├── issues_20250908_095058.md
│   │   ├── issues_20250908_095107.json
│   │   ├── issues_20250908_095107.md
│   │   ├── issues_20250908_095116.json
│   │   ├── issues_20250908_095116.md
│   │   ├── issues_20250908_095125.json
│   │   ├── issues_20250908_095125.md
│   │   ├── issues_20250908_095135.json
│   │   ├── issues_20250908_095135.md
│   │   ├── issues_20250908_095144.json
│   │   ├── issues_20250908_095144.md
│   │   ├── issues_20250908_095153.json
│   │   ├── issues_20250908_095153.md
│   │   ├── issues_20250908_095202.json
│   │   ├── issues_20250908_095202.md
│   │   ├── issues_20250908_095211.json
│   │   ├── issues_20250908_095211.md
│   │   ├── issues_20250908_095221.json
│   │   ├── issues_20250908_095221.md
│   │   ├── issues_20250908_095245.json
│   │   ├── issues_20250908_095245.md
│   │   ├── issues_20250908_095310.json
│   │   ├── issues_20250908_095310.md
│   │   ├── issues_20250908_095333.json
│   │   ├── issues_20250908_095333.md
│   │   ├── issues_20250908_095358.json
│   │   ├── issues_20250908_095358.md
│   │   ├── issues_20250908_095424.json
│   │   ├── issues_20250908_095424.md
│   │   ├── issues_20250908_095451.json
│   │   ├── issues_20250908_095451.md
│   │   ├── issues_20250908_095519.json
│   │   ├── issues_20250908_095519.md
│   │   ├── issues_20250908_095547.json
│   │   ├── issues_20250908_095547.md
│   │   ├── issues_20250908_095615.json
│   │   ├── issues_20250908_095615.md
│   │   ├── issues_20250908_095642.json
│   │   ├── issues_20250908_095642.md
│   │   ├── issues_20250908_095711.json
│   │   ├── issues_20250908_095711.md
│   │   ├── issues_20250908_095737.json
│   │   ├── issues_20250908_095737.md
│   │   ├── issues_20250908_095804.json
│   │   ├── issues_20250908_095804.md
│   │   ├── issues_20250908_095832.json
│   │   ├── issues_20250908_095832.md
│   │   ├── issues_20250908_095906.json
│   │   ├── issues_20250908_095906.md
│   │   ├── issues_20250908_095949.json
│   │   ├── issues_20250908_095949.md
│   │   ├── issues_20250908_100033.json
│   │   ├── issues_20250908_100033.md
│   │   ├── issues_20250908_100113.json
│   │   ├── issues_20250908_100113.md
│   │   ├── issues_20250908_100208.json
│   │   ├── issues_20250908_100208.md
│   │   ├── issues_20250908_100243.json
│   │   ├── issues_20250908_100243.md
│   │   ├── issues_20250908_100324.json
│   │   ├── issues_20250908_100324.md
│   │   ├── issues_20250908_100405.json
│   │   ├── issues_20250908_100405.md
│   │   ├── issues_20250908_100449.json
│   │   ├── issues_20250908_100449.md
│   │   ├── issues_20250908_100556.json
│   │   ├── issues_20250908_100556.md
│   │   ├── issues_20250908_100636.json
│   │   ├── issues_20250908_100636.md
│   │   ├── issues_20250908_100714.json
│   │   ├── issues_20250908_100714.md
│   │   ├── issues_20250908_100750.json
│   │   └── issues_20250908_100750.md
│   ├── ai-upgrade
│   │   └── per-file-recommendations.md
│   ├── consolidation_audit
│   │   ├── 20250907_164143
│   │   │   ├── duplicates.json
│   │   │   ├── duplicates.md
│   │   │   ├── python_import_issues.json
│   │   │   ├── python_import_issues.md
│   │   │   ├── summary.md
│   │   │   ├── ts_import_issues.json
│   │   │   └── ts_import_issues.md
│   │   └── 20250907_164613
│   │       ├── duplicates.json
│   │       ├── duplicates.md
│   │       ├── near_duplicates.json
│   │       ├── python_import_issues.json
│   │       ├── python_import_issues.md
│   │       ├── summary.md
│   │       ├── ts_import_issues.json
│   │       └── ts_import_issues.md
│   ├── consolidation_logs
│   │   └── 20250907_175844
│   │       └── apply_actions.log
│   ├── consolidation_plan
│   │   ├── plan.json
│   │   └── plan.md
│   ├── current_state
│   │   ├── 20250907_223107
│   │   │   ├── duplicates.json
│   │   │   ├── duplicates.md
│   │   │   ├── near_duplicates.json
│   │   │   ├── python_import_issues.json
│   │   │   ├── python_import_issues.md
│   │   │   ├── summary.md
│   │   │   ├── ts_import_issues.json
│   │   │   └── ts_import_issues.md
│   │   └── 20250907_223444
│   │       ├── duplicates.json
│   │       ├── duplicates.md
│   │       ├── near_duplicates.json
│   │       ├── python_import_issues.json
│   │       ├── python_import_issues.md
│   │       ├── summary.md
│   │       ├── ts_import_issues.json
│   │       └── ts_import_issues.md
│   ├── duplicates
│   │   ├── duplicate_files_20250908_000417.json
│   │   ├── duplicate_files_20250908_000417.md
│   │   ├── duplicates_apps.json
│   │   └── duplicates_apps.md
│   ├── post_consolidation_audit
│   │   └── 20250907_180825
│   │       ├── duplicates.json
│   │       ├── duplicates.md
│   │       ├── near_duplicates.json
│   │       ├── python_import_issues.json
│   │       ├── python_import_issues.md
│   │       ├── summary.md
│   │       ├── ts_import_issues.json
│   │       └── ts_import_issues.md
│   ├── quick_audit
│   │   └── 20250907_221340
│   │       ├── duplicates.json
│   │       ├── duplicates.md
│   │       ├── near_duplicates.json
│   │       ├── python_import_issues.json
│   │       ├── python_import_issues.md
│   │       ├── summary.md
│   │       ├── ts_import_issues.json
│   │       └── ts_import_issues.md
│   ├── backend_duplicates.json
│   ├── backend_name_similarity.json
│   └── backup_deletions_20250908T134610Z.json
├── scripts
│   ├── tests
│   │   ├── test_apply_consolidation_plan.py
│   │   ├── test_benchmark_latency.py
│   │   ├── test_cleanup_duplicates.py
│   │   ├── test_cleanup_reports.py
│   │   ├── test_consolidation_audit.py
│   │   ├── test_consolidation_plan_builder.py
│   │   ├── test_dedupe_scan.py
│   │   ├── test_lo_finetune.py
│   │   ├── test_prepare_vn_dataset.py
│   │   └── test_update_references.py
│   ├── ai-optimization-engine.js
│   ├── apply_consolidation_plan.py
│   ├── benchmark_latency.py
│   ├── cleanup_duplicates.py
│   ├── cleanup_reports.py
│   ├── consolidation_audit.py
│   ├── consolidation_plan_builder.py
│   ├── dedupe_scan.py
│   ├── desktop_api_codegen.mjs
│   ├── desktop_api_codegen.ts
│   ├── desktop_bundle_budget.mjs
│   ├── desktop_bundle_report.mjs
│   ├── desktop_check_generated_client.mjs
│   ├── desktop_compliance_scan.mjs
│   ├── desktop_contract_guard.mjs
│   ├── desktop_contract_guard_fallback.mjs
│   ├── desktop_coverage_gate.mjs
│   ├── desktop_demo_quality_gates.ps1
│   ├── desktop_diagnostics_pack.mjs
│   ├── desktop_env_guard.mjs
│   ├── desktop_generate_openapi_types.mjs
│   ├── desktop_plugins_validate.mjs
│   ├── desktop_prepare_build_meta.mjs
│   ├── desktop_quality_gates.ps1
│   ├── desktop_quality_gates.sh
│   ├── desktop_release_postflight.mjs
│   ├── desktop_release_rollback.mjs
│   ├── desktop_sync_ws_schema.mjs
│   ├── desktop_validate_config.mjs
│   ├── desktop_validate_plugins.mjs
│   ├── desktop_write_contract_snapshot.mjs
│   ├── find-duplicates.ps1
│   ├── gen_map.bat
│   ├── gen_map.ps1
│   ├── gen_map.sh
│   ├── immediate-optimization.js
│   ├── lo_finetune.py
│   ├── prepare_vn_dataset.py
│   ├── quality_gates.ps1
│   ├── run-continuous-monitor.ps1
│   ├── run_quick_audit.ps1
│   ├── start-turbo-ollama.bat
│   ├── stress_test_ollama.ps1
│   ├── update_references.py
│   ├── validate-monitoring.sh
│   ├── zeta-ai-agent_build_docker.sh
│   ├── zeta-ai-agent_check-production-config.ps1
│   ├── zeta-ai-agent_check-production-config.sh
│   ├── zeta-ai-agent_demo-health-check.ps1
│   ├── zeta-ai-agent_deploy.bat
│   ├── zeta-ai-agent_deploy.ps1
│   ├── zeta-ai-agent_deploy.sh
│   ├── zeta-ai-agent_env-check.ps1
│   ├── zeta-ai-agent_health-check.ps1
│   ├── zeta-ai-agent_phase2-setup.ps1
│   ├── zeta-ai-agent_quick-demo.ps1
│   ├── zeta-ai-agent_quick-health-check.ps1
│   ├── zeta-ai-agent_setup-devops-tools.ps1
│   ├── zeta-ai-agent_setup-monitoring.ps1
│   ├── zeta-ai-agent_setup-performance.ps1
│   ├── zeta-ai-agent_show-green-status.ps1
│   ├── zeta-ai-agent_test_integration.sh
│   ├── zeta-ai-agent_TIMELINE_README.md
│   ├── zeta-ai-agent_verify-deployment.ps1
│   ├── zeta-ai-agent_week1-zero-downtime.ps1
│   ├── zeta-ai-agent_week2-service-mesh.ps1
│   ├── zeta-ai-agent_week3-chaos-engineering.ps1
│   ├── zeta-ai-agent_week4-multimodal-ai.ps1
│   └── zeta-ai-agent_week5-enterprise-production.ps1
├── shared
│   └── configs
│       ├── .ruff.toml
│       ├── package-lock.json
│       ├── package.json
│       ├── pyproject.toml
│       └── uv.lock
├── src
│   ├── core
│   │   ├── agent
│   │   │   ├── cognitive
│   │   │   ├── memory
│   │   │   ├── planner
│   │   │   └── agent.ts
│   │   ├── ollama
│   │   │   ├── client.ts
│   │   │   ├── models.ts
│   │   │   └── types.ts
│   │   ├── tools
│   │   └── utils
│   │       ├── cache.ts
│   │       ├── monitoring.ts
│   │       ├── rateLimiter.ts
│   │       └── validation.ts
│   ├── extension
│   │   └── extension.ts
│   └── types
│       └── shared.ts
├── tests
│   ├── _shared
│   │   ├── test_agent_websocket.py
│   │   ├── test_chat_websocket.py
│   │   ├── test_database_service.py
│   │   └── test_memory_vector_store.py
│   ├── ai-codemod
│   │   ├── integration
│   │   │   └── test_engine_integration.py
│   │   └── unit
│   │       ├── test_ci_reporter.py
│   │       └── test_markdown_reporter.py
│   ├── ai-project-intelligence
│   │   ├── test_consistency_guard.py
│   │   └── test_knowledge_graph_serialization.py
│   ├── test_data
│   │   └── python
│   │       ├── missing_type_hints.py
│   │       └── unused_imports.py
│   ├── unit
│   │   └── test_turbo_api_client.py
│   ├── run_ai_codemod_tests.py
│   ├── run_ai_intelligence_tests.py
│   ├── test_ai_auto_optimizer.py
│   ├── test_ai_auto_refactor.py
│   ├── test_ai_optimize_project.py
│   ├── test_ai_project_scanner.py
│   ├── test_api_endpoint_discovery.py
│   ├── test_api_status.py
│   ├── test_check_ollama_vscode.py
│   ├── test_cicd_generator.py
│   ├── test_configure_turbo_ollama.py
│   ├── test_consolidate_monorepo.py
│   ├── test_directory_structure.py
│   ├── test_final_project_demo.py
│   ├── test_finalize_ollama_setup.py
│   ├── test_find_turbo_endpoint.py
│   ├── test_fix_continue.py
│   ├── test_fix_imports_exports.py
│   ├── test_fix_syntax_errors.py
│   ├── test_gen_project_map.py
│   ├── test_integration_mapper.py
│   ├── test_master_optimizer.py
│   ├── test_metrics_server.py
│   ├── test_network_diagnostics.py
│   ├── test_ollama_api_optimization_guide.py
│   ├── test_ollama_benchmark.py
│   ├── test_ollama_online_auth.py
│   ├── test_ollama_smart_setup.py
│   ├── test_ollama_turbo_integration.py
│   ├── test_optimized_turbo_client.py
│   ├── test_performance_profiler.py
│   ├── test_quick_start_turbo.py
│   ├── test_security_auditor.py
│   ├── test_setup_dev.py
│   ├── test_setup_turbo_ollama.py
│   ├── test_setup_vscode_continue.py
│   ├── test_setup_vscode_ollama.py
│   ├── test_setup_vscode_turbo_api.py
│   ├── test_simple_turbo_setup.py
│   ├── test_smart_refactorer.py
│   ├── test_turbo_api_examples.py
│   ├── test_turbo_api_implementation.py
│   ├── test_turbo_api_online_auth.py
│   ├── test_turbo_demo.py
│   ├── test_turbo_ollama_client.py
│   ├── test_turbo_ollama_login.py
│   ├── test_turbo_setup.py
│   ├── test_verify_ai_setup.py
│   └── zeta-agent.test.ts
├── tools
│   ├── ai-code-optimizer
│   │   ├── tests
│   │   │   ├── test_duplicate_detector.py
│   │   │   ├── test_import_optimizer.py
│   │   │   ├── test_optimizer.py
│   │   │   ├── test_optimizer_smoke.py
│   │   │   └── test_structure_enforcer.py
│   │   ├── .coverage
│   │   ├── config.yml
│   │   ├── conftest.py
│   │   ├── duplicate_detector.py
│   │   ├── import_optimizer.py
│   │   ├── mypy.ini
│   │   ├── optimizer.py
│   │   ├── pytest.ini
│   │   ├── README.md
│   │   └── structure_enforcer.py
│   ├── ai-codemod
│   │   ├── detectors
│   │   │   ├── tests
│   │   │   ├── python_detector.py
│   │   │   └── typescript_detector.py
│   │   ├── providers
│   │   │   ├── tests
│   │   │   └── ollama.py
│   │   ├── reporters
│   │   │   └── markdown_reporter.py
│   │   ├── tests
│   │   │   └── test_engine.py
│   │   ├── ai-rules.yml
│   │   ├── ci_reporter.py
│   │   └── engine.py
│   ├── ai-project-analyzer
│   │   ├── out
│   │   │   ├── analysis.json
│   │   │   └── recommendations.json
│   │   ├── tests
│   │   │   ├── test_analyzer.py
│   │   │   ├── test_duplicates.py
│   │   │   ├── test_per_file_optimizer.py
│   │   │   ├── test_project-graph.py
│   │   │   ├── test_smart-optimizer.py
│   │   │   └── test_vs-code-helper.py
│   │   ├── analyzer.py
│   │   ├── config.yml
│   │   ├── duplicates.py
│   │   ├── per_file_optimizer.py
│   │   ├── project-graph.py
│   │   ├── smart-optimizer.py
│   │   └── vs-code-helper.py
│   ├── ai-project-intelligence
│   │   ├── out
│   │   │   ├── brain-summary.json
│   │   │   ├── inconsistencies.json
│   │   │   └── optimization-results.json
│   │   ├── tests
│   │   │   ├── test_auto-coder.py
│   │   │   ├── test_auto_fixer.py
│   │   │   ├── test_brain.py
│   │   │   ├── test_consistency-guard.py
│   │   │   ├── test_continuous-monitor.py
│   │   │   ├── test_knowledge-graph.py
│   │   │   ├── test_reporter.py
│   │   │   └── test_setup.py
│   │   ├── auto-coder.py
│   │   ├── auto_fixer.py
│   │   ├── brain.py
│   │   ├── config.yml
│   │   ├── consistency-guard.py
│   │   ├── continuous-monitor.py
│   │   ├── knowledge-graph.py
│   │   ├── README.md
│   │   ├── reporter.py
│   │   └── setup.py
│   ├── ai_code_optimizer
│   │   ├── tests
│   │   │   └── test___init__.py
│   │   └── __init__.py
│   ├── ci
│   │   ├── mypy-files.txt
│   │   └── mypy-temp.ini
│   ├── git-hooks
│   │   └── pre-commit
│   ├── scripts
│   │   ├── audit
│   │   │   ├── tests
│   │   │   └── detect_near_duplicates.py
│   │   ├── bench
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── bench_api.py
│   │   │   └── bench_rag.py
│   │   ├── consistency
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── env_consistency.py
│   │   │   ├── i18n_consistency.py
│   │   │   ├── openapi_consistency.py
│   │   │   ├── run_all.py
│   │   │   └── ws_events_consistency.py
│   │   ├── consolidation
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── consolidate_repo.py
│   │   │   └── CONSOLIDATION_MAP.yaml
│   │   ├── copilot
│   │   │   ├── tests
│   │   │   ├── agent.bat
│   │   │   ├── agent.ps1
│   │   │   ├── agent.sh
│   │   │   ├── build_context.py
│   │   │   ├── hotfix_pydantic.py
│   │   │   ├── hotfix_pydantic_v2.py
│   │   │   ├── mypy_checker.py
│   │   │   ├── simple_runner.py
│   │   │   └── ultimate_pydantic_fix.py
│   │   ├── deployment
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── production_deploy.py
│   │   │   └── production_deploy_complete.py
│   │   ├── fix
│   │   │   ├── tests
│   │   │   ├── auto_fix_env.ps1
│   │   │   ├── auto_fix_env.sh
│   │   │   ├── demo_fix_env.py
│   │   │   ├── README.md
│   │   │   ├── repair_env.py
│   │   │   ├── test_fix_env.py
│   │   │   └── verify_stack.py
│   │   ├── impl
│   │   │   ├── go_live_lite.ps1
│   │   │   ├── go_live_lite.sh
│   │   │   ├── go_live_once.ps1
│   │   │   ├── go_live_once.sh
│   │   │   ├── phase1_foundation.sh
│   │   │   ├── phase2_perf.sh
│   │   │   ├── phase3_security.sh
│   │   │   ├── phase4_deploy.sh
│   │   │   ├── run_now.ps1
│   │   │   └── run_now.sh
│   │   ├── install
│   │   │   ├── ensure_env.ps1
│   │   │   └── ensure_env.sh
│   │   ├── maintenance
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── autofix_imports.py
│   │   │   ├── backup_data.py
│   │   │   ├── careful_init_fixer.py
│   │   │   ├── comprehensive_init_fixer.py
│   │   │   └── fix_test_imports.py
│   │   ├── metrics
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── focus_index.py
│   │   ├── migration
│   │   │   ├── tests
│   │   │   └── migrate_graphql_structure.py
│   │   ├── monitoring
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── health_check.py
│   │   │   ├── performance_check.py
│   │   │   └── system_monitor.py
│   │   ├── perf
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── perf_gate.py
│   │   │   └── probe.py
│   │   ├── qa
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── check_zero_trust.py
│   │   │   ├── preflight.py
│   │   │   └── warm_and_probe_rag.py
│   │   ├── quality
│   │   │   ├── tests
│   │   │   ├── dup_guard.py
│   │   │   ├── quality_gates.ps1
│   │   │   ├── quality_gates.sh
│   │   │   ├── quality_gates_restructured.ps1
│   │   │   ├── quality_gates_updated.ps1
│   │   │   └── quality_gates_updated.sh
│   │   ├── refactor
│   │   │   ├── tests
│   │   │   ├── copilot_refactor.py
│   │   │   ├── import_map.json
│   │   │   └── refactor_plan.yaml
│   │   ├── repair
│   │   │   ├── tests
│   │   │   ├── fix_duplicates.py
│   │   │   ├── fix_empty_try_blocks.py
│   │   │   ├── fix_import_conflicts.py
│   │   │   ├── fix_migration_imports.py
│   │   │   ├── fix_service_compatibility.py
│   │   │   ├── fix_syntax_errors.py
│   │   │   ├── fix_undefined_vars.py
│   │   │   ├── fix_undefined_vars_advanced.py
│   │   │   └── queue.yml
│   │   ├── repo
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── cleanup_plan.py
│   │   │   ├── find_duplicates.py
│   │   │   └── verify_client_api.py
│   │   ├── safe
│   │   │   ├── tests
│   │   │   ├── apply_merge_plan.py
│   │   │   ├── dedup_index.py
│   │   │   └── generate_work_orders.py
│   │   ├── seed
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   ├── seed_roles.py
│   │   │   └── seed_roles_normalized.py
│   │   ├── self_upgrade
│   │   │   ├── tests
│   │   │   ├── __init__.py
│   │   │   └── cli.py
│   │   ├── testing
│   │   │   ├── __init__.py
│   │   │   ├── load_test.py
│   │   │   └── run_tests.py
│   │   ├── tests
│   │   │   ├── test___init__.py
│   │   │   ├── test_advanced_fix_undefined.py
│   │   │   ├── test_aggressive_optimization.py
│   │   │   ├── test_analyze_duplicate_name_similarity.py
│   │   │   ├── test_analyze_f821.py
│   │   │   ├── test_analyze_init_patterns.py
│   │   │   ├── test_analyze_middleware.py
│   │   │   ├── test_api_auto_fixer.py
│   │   │   ├── test_api_consistency_optimizer.py
│   │   │   ├── test_apply_base_classes.py
│   │   │   ├── test_apply_best_practices.py
│   │   │   ├── test_apply_refactor_plan.py
│   │   │   ├── test_apply_render_only.py
│   │   │   ├── test_auto_fix_comprehensive.py
│   │   │   ├── test_auto_fix_critical.py
│   │   │   ├── test_auto_fix_regression_guard.py
│   │   │   ├── test_auto_update_imports.py
│   │   │   ├── test_autobarrel_python.py
│   │   │   ├── test_backup_data.py
│   │   │   ├── test_backup_database.py
│   │   │   ├── test_backup_inits.py
│   │   │   ├── test_batch_fix_errors.py
│   │   │   ├── test_benchmark_desktop_control.py
│   │   │   ├── test_benchmark_fast_control.py
│   │   │   ├── test_check_backend_duplicates_ci.py
│   │   │   ├── test_check_conformance.py
│   │   │   ├── test_check_dependency_map.py
│   │   │   ├── test_check_env_sync.py
│   │   │   ├── test_check_external_dependencies.py
│   │   │   ├── test_check_health.py
│   │   │   ├── test_check_missing_dependencies.py
│   │   │   ├── test_check_quality.py
│   │   │   ├── test_check_related_files.py
│   │   │   ├── test_check_runtime_imports.py
│   │   │   ├── test_cleanup_backups.py
│   │   │   ├── test_cleanup_project.py
│   │   │   ├── test_cleanup_tools.py
│   │   │   ├── test_complete_fix_f_strings.py
│   │   │   ├── test_completeness_score.py
│   │   │   ├── test_component_consistency_checker.py
│   │   │   ├── test_comprehensive_project_enhancement.py
│   │   │   ├── test_consolidate_backend_backups.py
│   │   │   ├── test_consolidate_chunking.py
│   │   │   ├── test_convert_barrels_to_lazy.py
│   │   │   ├── test_convert_remaining_barrels.py
│   │   │   ├── test_copilot_guard.py
│   │   │   ├── test_copilot_intelligence_check.py
│   │   │   ├── test_cross_project_guard.py
│   │   │   ├── test_db_migrate.py
│   │   │   ├── test_deepseek_agent.py
│   │   │   ├── test_deepseek_start_assistant.py
│   │   │   ├── test_demo_ai_trainer.py
│   │   │   ├── test_demo_ai_trainer_basic.py
│   │   │   ├── test_demo_autonomous_complete.py
│   │   │   ├── test_demo_autonomous_simple.py
│   │   │   ├── test_demo_breaking_changes.py
│   │   │   ├── test_demo_fast_control.py
│   │   │   ├── test_demo_missing_code_system.py
│   │   │   ├── test_demo_one_click_learning.py
│   │   │   ├── test_demo_security_production.py
│   │   │   ├── test_dependency_safety.py
│   │   │   ├── test_deploy.py
│   │   │   ├── test_deploy_deepseek.py
│   │   │   ├── test_deploy_production.py
│   │   │   ├── test_deploy_production_automated.py
│   │   │   ├── test_detect_backend_duplicates.py
│   │   │   ├── test_diagnose_environment_comprehensive.py
│   │   │   ├── test_diagnose_venv_detailed.py
│   │   │   ├── test_diagnose_vscode_issues.py
│   │   │   ├── test_dlq_replay.py
│   │   │   ├── test_duplicate_code_analyzer.py
│   │   │   ├── test_duplicate_optimizer.py
│   │   │   ├── test_enhance_api_endpoints.py
│   │   │   ├── test_enhance_dependencies_repos.py
│   │   │   ├── test_enhance_domain_layer.py
│   │   │   ├── test_enhance_middleware.py
│   │   │   ├── test_enhance_repositories_schemas.py
│   │   │   ├── test_export_openapi.py
│   │   │   ├── test_fast_duplicate_check.py
│   │   │   ├── test_file_integrity_full_check.py
│   │   │   ├── test_final_enhancement.py
│   │   │   ├── test_final_optimization.py
│   │   │   ├── test_find_duplicate_files.py
│   │   │   ├── test_find_duplicate_files_tool.py
│   │   │   ├── test_find_unused_deps.py
│   │   │   ├── test_fix_all_declarations.py
│   │   │   ├── test_fix_all_f_strings.py
│   │   │   ├── test_fix_all_inits.py
│   │   │   ├── test_fix_all_issues.py
│   │   │   ├── test_fix_barrels_absolute.py
│   │   │   ├── test_fix_common_f821.py
│   │   │   ├── test_fix_critical_issues.py
│   │   │   ├── test_fix_f821_errors.py
│   │   │   ├── test_fix_f821_simple.py
│   │   │   ├── test_fix_f_string.py
│   │   │   ├── test_fix_graphql_resolvers.py
│   │   │   ├── test_fix_import_syntax.py
│   │   │   ├── test_fix_imports_ordering.py
│   │   │   ├── test_fix_middleware_advanced.py
│   │   │   ├── test_fix_minimal_imports_blocks.py
│   │   │   ├── test_fix_mypy_errors.py
│   │   │   ├── test_fix_repo_safe.py
│   │   │   ├── test_fix_repo_safe_v2.py
│   │   │   ├── test_fix_repo_safe_v3.py
│   │   │   ├── test_fix_syntax_tools.py
│   │   │   ├── test_fix_undefined_variables.py
│   │   │   ├── test_fix_underscore_vars.py
│   │   │   ├── test_fix_v2_dependencies.py
│   │   │   ├── test_fix_venv_recognition.py
│   │   │   ├── test_fix_vscode_venv.py
│   │   │   ├── test_focus_guard.py
│   │   │   ├── test_focus_index.py
│   │   │   ├── test_focus_optimization.py
│   │   │   ├── test_force_render_asr.py
│   │   │   ├── test_gen_ports_docs.py
│   │   │   ├── test_generate_8_layer_architecture.py
│   │   │   ├── test_generate_8_layer_full.py
│   │   │   ├── test_generate_copilot_manifest.py
│   │   │   ├── test_generate_copilot_manifest_hook.py
│   │   │   ├── test_generate_expectations_from_project_map.py
│   │   │   ├── test_guard_full_file_read.py
│   │   │   ├── test_import_optimization_report.py
│   │   │   ├── test_insert_desktop_route.py
│   │   │   ├── test_main_tsx_analyzer.py
│   │   │   ├── test_manage_inits.py
│   │   │   ├── test_master_quality_check.py
│   │   │   ├── test_migrate_imports.py
│   │   │   ├── test_missing_code_baseline.py
│   │   │   ├── test_missing_code_diff_gate.py
│   │   │   ├── test_missing_code_owner_report.py
│   │   │   ├── test_normalize_imports.py
│   │   │   ├── test_normalize_rendered_files.py
│   │   │   ├── test_optimize_imports_auto.py
│   │   │   ├── test_optimize_init_files.py
│   │   │   ├── test_optimize_init_files_fixed.py
│   │   │   ├── test_paddle_ocr_cli.py
│   │   │   ├── test_parse_jscpd_report.py
│   │   │   ├── test_patch_apply.py
│   │   │   ├── test_phase0_consolidation.py
│   │   │   ├── test_phase1_cleanup_duplicates.py
│   │   │   ├── test_phase2_layer_reorganization.py
│   │   │   ├── test_phase3_domain_consolidation.py
│   │   │   ├── test_ports_audit.py
│   │   │   ├── test_predeploy_check.py
│   │   │   ├── test_project_summary.py
│   │   │   ├── test_qa_pipeline.py
│   │   │   ├── test_quality_full_check.py
│   │   │   ├── test_quick_check.py
│   │   │   ├── test_quick_critical_fixer.py
│   │   │   ├── test_quick_duplicate_check.py
│   │   │   ├── test_quick_fix_stubs.py
│   │   │   ├── test_quick_fix_underscore.py
│   │   │   ├── test_refactor_rename.py
│   │   │   ├── test_reinstall_vscode_paths.py
│   │   │   ├── test_render_templates_update.py
│   │   │   ├── test_restore_candidate_patch.py
│   │   │   ├── test_restore_data.py
│   │   │   ├── test_restructure_project.py
│   │   │   ├── test_restructure_zeta_project.py
│   │   │   ├── test_roadmap_implementation.py
│   │   │   ├── test_roadmap_implementation_guide.py
│   │   │   ├── test_run_quality_gates.py
│   │   │   ├── test_run_scaffold_dry.py
│   │   │   ├── test_run_training_models_smoke.py
│   │   │   ├── test_safe_chunking_discovery.py
│   │   │   ├── test_safe_cleanup.py
│   │   │   ├── test_safe_error_fixer.py
│   │   │   ├── test_safety_audit.py
│   │   │   ├── test_safety_dashboard.py
│   │   │   ├── test_save_plan_asr.py
│   │   │   ├── test_scaffold_missing_dirs.py
│   │   │   ├── test_scaffold_missing_modules.py
│   │   │   ├── test_setup_development.py
│   │   │   ├── test_smart_import_cleaner.py
│   │   │   ├── test_system_upgrade.py
│   │   │   ├── test_ts_alias_migrator.py
│   │   │   ├── test_ultimate_completion.py
│   │   │   ├── test_update_init_files.py
│   │   │   ├── test_update_project_map.py
│   │   │   ├── test_update_project_paths.py
│   │   │   ├── test_update_roadmap.py
│   │   │   ├── test_upgrade_analyzer.py
│   │   │   ├── test_used_but_missing.py
│   │   │   ├── test_validate_infrastructure.py
│   │   │   ├── test_validate_inits.py
│   │   │   ├── test_validate_new_files.py
│   │   │   ├── test_verify_core_export_contracts.py
│   │   │   ├── test_verify_enhanced_roadmap_contracts.py
│   │   │   ├── test_verify_imports.py
│   │   │   ├── test_verify_middleware_enhancement.py
│   │   │   ├── test_verify_module_symbols.py
│   │   │   ├── test_verify_project_map.py
│   │   │   ├── test_verify_project_paths.py
│   │   │   ├── test_verify_vscode_config.py
│   │   │   ├── test_verify_vscode_config_simple.py
│   │   │   ├── test_vscode_config_optimizer.py
│   │   │   ├── test_vscode_final_guide.py
│   │   │   ├── test_whisper_server.py
│   │   │   └── test_workflow_health_check.py
│   │   ├── upgrade
│   │   │   ├── tests
│   │   │   ├── dead_code_guard.ps1
│   │   │   ├── dead_code_guard.sh
│   │   │   ├── dedupe_guard.ps1
│   │   │   ├── dedupe_guard.sh
│   │   │   ├── ensure_configs.py
│   │   │   ├── guardian_scan.sh
│   │   │   ├── py_quality.ps1
│   │   │   ├── py_quality.sh
│   │   │   ├── ts_quality.ps1
│   │   │   ├── ts_quality.sh
│   │   │   ├── upgrade_all.bat
│   │   │   ├── upgrade_all.sh
│   │   │   └── upgrade_wrapper.py
│   │   ├── __init__.py
│   │   ├── add_test_type_annotations.py
│   │   ├── advanced_duplicate_analysis.ps1
│   │   ├── advanced_fix_undefined.py
│   │   ├── aggressive_optimization.py
│   │   ├── analyze_duplicate_name_similarity.py
│   │   ├── analyze_f821.py
│   │   ├── analyze_init_patterns.py
│   │   ├── analyze_middleware.py
│   │   ├── api_auto_fixer.py
│   │   ├── api_consistency_optimizer.py
│   │   ├── apply_base_classes.py
│   │   ├── apply_best_practices.py
│   │   ├── apply_refactor_plan.py
│   │   ├── apply_render_only.py
│   │   ├── auto_apply_shortcuts.ps1
│   │   ├── auto_fix_comprehensive.py
│   │   ├── auto_fix_critical.py
│   │   ├── auto_fix_regression_guard.py
│   │   ├── auto_update_imports.py
│   │   ├── autobarrel_frontend.mjs
│   │   ├── autobarrel_python.py
│   │   ├── autofix_vscode_environment.ps1
│   │   ├── backup_data.py
│   │   ├── backup_database.py
│   │   ├── backup_inits.py
│   │   ├── batch_fix_errors.py
│   │   ├── benchmark_desktop_control.py
│   │   ├── benchmark_fast_control.py
│   │   ├── bootstrap.ps1
│   │   ├── bootstrap.sh
│   │   ├── bootstrap_dev.ps1
│   │   ├── bootstrap_dev.sh
│   │   ├── check.py
│   │   ├── check_backend_duplicates_ci.py
│   │   ├── check_conformance.py
│   │   ├── check_dependency_map.py
│   │   ├── check_duplicates.py
│   │   ├── check_duplication.ps1
│   │   ├── check_duplication.sh
│   │   ├── check_env_sync.py
│   │   ├── check_external_dependencies.py
│   │   ├── check_health.py
│   │   ├── check_i18n.mjs
│   │   ├── check_missing_dependencies.py
│   │   ├── check_python.sh
│   │   ├── check_quality.py
│   │   ├── check_related_files.py
│   │   ├── check_runtime_imports.py
│   │   ├── ci-local.ps1
│   │   ├── ci_check.sh
│   │   ├── cleanup_backups.py
│   │   ├── cleanup_project.py
│   │   ├── CLEANUP_SUMMARY.md
│   │   ├── cleanup_tools.py
│   │   ├── complete_fix_f_strings.py
│   │   ├── completeness_score.py
│   │   ├── component_consistency_checker.py
│   │   ├── comprehensive_project_enhancement.py
│   │   ├── consolidate_backend_backups.py
│   │   ├── consolidate_chunking.py
│   │   ├── convert_barrels_to_lazy.py
│   │   ├── convert_remaining_barrels.py
│   │   ├── copilot_guard.py
│   │   ├── copilot_intelligence_check.py
│   │   ├── cross_project_guard.py
│   │   ├── db_migrate.py
│   │   ├── deepseek_agent.py
│   │   ├── deepseek_start_assistant.py
│   │   ├── demo_ai_trainer.py
│   │   ├── demo_ai_trainer_basic.py
│   │   ├── demo_autonomous_complete.py
│   │   ├── demo_autonomous_simple.py
│   │   ├── demo_breaking_changes.py
│   │   ├── demo_fast_control.py
│   │   ├── demo_missing_code_system.py
│   │   ├── demo_one_click_learning.py
│   │   ├── demo_security_production.py
│   │   ├── dependency_safety.py
│   │   ├── deploy.py
│   │   ├── deploy_deepseek.py
│   │   ├── deploy_production.py
│   │   ├── deploy_production_automated.py
│   │   ├── deployment_analysis.json
│   │   ├── detect_backend_duplicates.py
│   │   ├── dev_aliases.ps1
│   │   ├── dev_aliases.sh
│   │   ├── dev_setup.bat
│   │   ├── diagnose_environment_comprehensive.py
│   │   ├── diagnose_venv_detailed.py
│   │   ├── diagnose_vscode_issues.py
│   │   ├── dlq_replay.py
│   │   ├── duplicate_code_analyzer.py
│   │   ├── duplicate_optimizer.py
│   │   ├── enhance_api_endpoints.py
│   │   ├── enhance_dependencies_repos.py
│   │   ├── enhance_domain_layer.py
│   │   ├── enhance_middleware.py
│   │   ├── enhance_repositories_schemas.py
│   │   ├── export_openapi.py
│   │   ├── fast_duplicate_check.py
│   │   ├── file_integrity_full_check.py
│   │   ├── final_enhancement.py
│   │   ├── final_optimization.py
│   │   ├── find_duplicate_files.py
│   │   ├── find_duplicate_files_tool.py
│   │   ├── find_unused_deps.py
│   │   ├── fix_all_declarations.py
│   │   ├── fix_all_f_strings.py
│   │   ├── fix_all_inits.py
│   │   ├── fix_all_issues.py
│   │   ├── fix_barrels_absolute.py
│   │   ├── fix_common_f821.py
│   │   ├── fix_critical_issues.py
│   │   ├── fix_environment_issues.ps1
│   │   ├── fix_f821_errors.py
│   │   ├── fix_f821_simple.py
│   │   ├── fix_f_string.py
│   │   ├── fix_graphql_resolvers.py
│   │   ├── fix_import_syntax.py
│   │   ├── fix_imports_ordering.py
│   │   ├── fix_middleware_advanced.py
│   │   ├── fix_minimal_imports_blocks.py
│   │   ├── fix_mypy_errors.py
│   │   ├── fix_pytest_simple.py
│   │   ├── fix_repo_safe.py
│   │   ├── fix_repo_safe_v2.py
│   │   ├── fix_repo_safe_v3.py
│   │   ├── fix_syntax_tools.py
│   │   ├── fix_undefined_variables.py
│   │   ├── fix_underscore_vars.py
│   │   ├── fix_v2_dependencies.py
│   │   ├── fix_venv_recognition.py
│   │   ├── fix_vscode_extension_corruption.ps1
│   │   ├── fix_vscode_settings_conflict.ps1
│   │   ├── fix_vscode_venv.ps1
│   │   ├── fix_vscode_venv.py
│   │   ├── focus_guard.py
│   │   ├── focus_index.py
│   │   ├── focus_optimization.py
│   │   ├── force_render_asr.py
│   │   ├── gen_ports_docs.py
│   │   ├── gen_ts_client.sh
│   │   ├── generate_8_layer_architecture.py
│   │   ├── generate_8_layer_full.py
│   │   ├── generate_copilot_manifest.py
│   │   ├── generate_copilot_manifest_hook.py
│   │   ├── generate_expectations_from_project_map.py
│   │   ├── git_create_branch_and_commit.ps1
│   │   ├── guard_full_file_read.py
│   │   ├── import_optimization_report.py
│   │   ├── insert_desktop_route.py
│   │   ├── install-node-smart.ps1
│   │   ├── install-node.ps1
│   │   ├── install-ollama-smart.ps1
│   │   ├── install-ollama.ps1
│   │   ├── load_test_outbox.py
│   │   ├── main_tsx_analyzer.py
│   │   ├── manage_inits.py
│   │   ├── master_quality_check.py
│   │   ├── migrate_imports.py
│   │   ├── missing_code_audit.py
│   │   ├── missing_code_baseline.py
│   │   ├── missing_code_diff_gate.py
│   │   ├── missing_code_owner_report.py
│   │   ├── moves_proposal.json
│   │   ├── normalize_imports.py
│   │   ├── normalize_rendered_files.py
│   │   ├── optimize_imports_auto.py
│   │   ├── optimize_init_files.py
│   │   ├── optimize_init_files_fixed.py
│   │   ├── paddle_ocr_cli.py
│   │   ├── parse_jscpd_report.py
│   │   ├── patch_apply.py
│   │   ├── phase0_consolidation.py
│   │   ├── phase1_cleanup_duplicates.py
│   │   ├── phase2_layer_reorganization.py
│   │   ├── phase3_domain_consolidation.py
│   │   ├── ports_audit.py
│   │   ├── predeploy_check.py
│   │   ├── project_summary.py
│   │   ├── qa_pipeline.py
│   │   ├── quality_full_check.py
│   │   ├── quick_check.py
│   │   ├── quick_critical_fixer.py
│   │   ├── quick_duplicate_check.py
│   │   ├── quick_fix_stubs.py
│   │   ├── quick_fix_underscore.py
│   │   ├── README.md
│   │   ├── refactor_rename.py
│   │   ├── reinstall_vscode_paths.py
│   │   ├── render_templates_update.py
│   │   ├── restore_candidate_patch.py
│   │   ├── restore_data.py
│   │   ├── restructure_project.py
│   │   ├── restructure_zeta_project.py
│   │   ├── roadmap_implementation.py
│   │   ├── roadmap_implementation_guide.py
│   │   ├── run_all.ps1
│   │   ├── run_all.sh
│   │   ├── run_deepseek_r1.ps1
│   │   ├── run_duplicate_checks.ps1
│   │   ├── run_optimization_roadmap.ps1
│   │   ├── run_optimization_roadmap.sh
│   │   ├── run_quality_gates.py
│   │   ├── run_scaffold_dry.py
│   │   ├── run_training_models_smoke.py
│   │   ├── safe_chunking_discovery.py
│   │   ├── safe_cleanup.py
│   │   ├── safe_error_fixer.py
│   │   ├── safety_audit.py
│   │   ├── safety_dashboard.py
│   │   ├── save_plan_asr.py
│   │   ├── scaffold_missing_dirs.py
│   │   ├── scaffold_missing_modules.py
│   │   ├── setup-complete.ps1
│   │   ├── setup_development.py
│   │   ├── setup_hooks.ps1
│   │   ├── setup_hooks.sh
│   │   ├── smart-setup.ps1
│   │   ├── smart_import_cleaner.py
│   │   ├── start_all_tools.py
│   │   ├── system_upgrade.py
│   │   ├── test-ollama-api.ps1
│   │   ├── test_desktop_control_standalone.py
│   │   ├── test_quality_gates_update.ps1
│   │   ├── test_safety.py
│   │   ├── ts_alias_migrator.py
│   │   ├── ultimate_completion.py
│   │   ├── update_init_files.py
│   │   ├── update_project_map.py
│   │   ├── update_project_paths.py
│   │   ├── update_roadmap.py
│   │   ├── upgrade_analyzer.py
│   │   ├── used_but_missing.py
│   │   ├── validate_infrastructure.py
│   │   ├── validate_inits.py
│   │   ├── validate_new_files.py
│   │   ├── validate_schemas.mjs
│   │   ├── verify-pr1-scope.ps1
│   │   ├── verify_core_export_contracts.py
│   │   ├── verify_enhanced_roadmap_contracts.py
│   │   ├── verify_imports.py
│   │   ├── verify_middleware_enhancement.py
│   │   ├── verify_module_symbols.py
│   │   ├── verify_project_map.py
│   │   ├── verify_project_paths.py
│   │   ├── verify_vscode_config.py
│   │   ├── verify_vscode_config_simple.py
│   │   ├── vscode_config_optimizer.py
│   │   ├── vscode_final_guide.py
│   │   ├── whisper_server.py
│   │   ├── workflow_health_check.py
│   │   └── zero-dependency-setup.ps1
│   ├── tests
│   │   ├── test___init__.py
│   │   ├── test_benchmark_ollama.py
│   │   ├── test_cleanup_duplicates.py
│   │   ├── test_find_duplicate_files.py
│   │   ├── test_reference_updater.py
│   │   └── test_run_ai_optimization.py
│   ├── __init__.py
│   ├── benchmark_ollama.py
│   ├── cleanup_duplicates.py
│   ├── find_duplicate_files.py
│   ├── reference_updater.py
│   ├── run_ai_optimization.py
│   └── schedule_optimization.ps1
├── zeta_vn
├── .ai_knowledge_graph.json
├── .coveragerc
├── .editorconfig
├── .env
├── .env.example
├── .env.ollama
├── .env.turbo
├── .eslintrc.base.cjs
├── .gitignore
├── .pre-commit-config.yaml
├── .prettierrc.json
├── advanced_duplicate_detector.ps1
├── ai_auto_optimizer.py
├── ai_auto_refactor.py
├── AI_CODE_EXPERT_PROPOSAL.md
├── AI_OPTIMIZATION_READY_TO_RUN.md
├── AI_OPTIMIZATION_RECOMMENDATIONS.md
├── AI_OPTIMIZATION_SUMMARY.md
├── ai_optimize_project.py
├── ai_project_analysis.json
├── AI_PROJECT_ANALYSIS_REPORT.md
├── ai_project_scanner.py
├── ai_refactor_report.json
├── AI_REFACTOR_SUMMARY.md
├── api_endpoint_discovery.py
├── API_KEY_USAGE_RECOMMENDATIONS.md
├── api_status.py
├── benchmark_results.json
├── check_ollama_vscode.py
├── check_venv_health.ps1
├── cicd_generator.py
├── cleanup_generated.sh
├── cleanup_log_20250909_035118.txt
├── cleanup_plan.md
├── cleanup_redundant_files.py
├── configure_turbo_ollama.py
├── configure_vscode_ollama.ps1
├── consolidate_monorepo.ps1
├── consolidate_monorepo.py
├── CONSOLIDATION_SUMMARY.md
├── current_venv_packages.txt
├── directory_structure.py
├── docker-compose.dev.yml
├── docker-compose.monitoring.yml
├── DUPLICATE_CLEANUP_COMPLETED.md
├── DUPLICATE_CLEANUP_SCRIPT_READY.md
├── DUPLICATE_CLEANUP_SUCCESS.md
├── duplicate_code_report_20250909_035652.html
├── duplicate_code_report_20250909_035652.json
├── FINAL_AI_OPTIMIZATION_SUMMARY.md
├── final_project_demo.py
├── FINAL_PROJECT_STATUS.json
├── FINAL_PROJECT_STATUS.md
├── finalize_ollama_setup.py
├── find_turbo_endpoint.py
├── fix_continue.py
├── fix_imports.py
├── fix_imports_exports.py
├── fix_syntax_errors.py
├── gen_project_map.py
├── install_vscode_extensions.bat
├── INTEGRATION_MAP.md
├── integration_mapper.py
├── local_models_fallback.ps1
├── login.ps1
├── Makefile
├── manual_venv_recovery.ps1
├── master_optimizer.py
├── metrics_server.py
├── Modelfile
├── Modelfile.zeta
├── MONITORING_SETUP.md
├── mypy.ini
├── mypy_temp.ini
├── network_diagnostics.py
├── next_steps_advisor.ps1
├── NUMPY_2X_COMPATIBILITY_COMPLETE.md
├── NUMPY_COMPATIBILITY_GUIDE.md
├── ollama_api_config.json
├── ollama_api_optimization_guide.py
├── ollama_benchmark.py
├── ollama_config_analysis.json
├── OLLAMA_INTEGRATION_README.md
├── ollama_online_auth.py
├── ollama_smart_setup.py
├── OLLAMA_TURBO_API_STATUS.md
├── ollama_turbo_config.json
├── ollama_turbo_integration.py
├── ONE_CLICK_LEARNING_README.md
├── OPTIMIZATION_REPORT.md
├── optimization_results.json
├── OPTIMIZATION_RESULTS.md
├── optimize_venv.ps1
├── optimized_turbo_client.py
├── package-lock.json
├── package.json
├── PERFORMANCE_ANALYSIS_REPORT.json
├── PERFORMANCE_ANALYSIS_REPORT.md
├── performance_profiler.py
├── PHASE_2_IMPLEMENTATION_ROADMAP.md
├── production_deploy.py
├── PROJECT_CONSOLIDATION_COMPLETE.md
├── PROJECT_MAP.md
├── PROJECT_OPTIMIZATION_ROADMAP.md
├── pyproject.base.toml
├── pytest.ini
├── quick_duplicate_checker.py
├── QUICK_MAP.md
├── quick_start_turbo.py
├── README.md
├── REDUNDANT_CLEANUP_SUCCESS.md
├── REFACTORING_ANALYSIS_REPORT.json
├── REFACTORING_ANALYSIS_REPORT.md
├── REFACTORING_SUGGESTIONS.md
├── reinstall_ollama.bat
├── requirements-dev.txt
├── requirements.txt
├── ruff.toml
├── run_integration_mapper.bat
├── run_integration_mapper.ps1
├── safe_backup_cleanup.ps1
├── safe_backup_cleanup.py
├── SafeColors.psm1
├── SECURITY.md
├── SECURITY_AUDIT_REPORT.json
├── SECURITY_AUDIT_REPORT.md
├── security_auditor.py
├── setup.ps1
├── setup_api_key_complete.ps1
├── setup_dev.py
├── setup_local_ollama.ps1
├── setup_ollama.bat
├── setup_ollama.ps1
├── setup_ollama_turbo_online.ps1
├── setup_one_click_learning.py
├── setup_turbo_api.ps1
├── setup_turbo_env.bat
├── setup_turbo_ollama.py
├── setup_vscode_continue.py
├── setup_vscode_ollama.py
├── setup_vscode_turbo_api.py
├── simple_turbo_setup.py
├── smart_refactorer.py
├── start_dev.ps1
├── start_ollama_vscode.bat
├── stop_all_background.bat
├── stop_all_background.ps1
├── switch_numpy.py
├── test_complete_integration.ps1
├── test_local_ollama.ps1
├── test_numpy_switch.py
├── test_ollama_integration.ps1
├── test_turbo_api.ps1
├── test_turbo_comprehensive.ps1
├── test_turbo_curl.bat
├── tsconfig.base.json
├── turbo_api_examples.py
├── turbo_api_implementation.py
├── turbo_api_online_auth.py
├── turbo_demo.py
├── turbo_demo_report.json
├── turbo_ollama_client.py
├── turbo_ollama_login.py
├── turbo_quick_start.bat
├── turbo_quick_start.sh
├── turbo_setup.py
├── turbo_setup_complete.ps1
├── venv_integrity_check.ps1
├── VenvHelper.psm1
├── verify_ai_setup.py
├── vn_python_dataset.jsonl
├── zeta-agent-package.json
├── zeta-monorepo.md
├── ZETA_AI_AGENT_README.md
├── ZETA_ONE_CLICK_LEARNING_SETUP.md
├── ZetaVenvHelper.psm1
└── 🎉_DỰ_ÁN_HOÀN_TẤT.md
```

## Gợi ý dùng làm context cho AI / Copilot
- Dùng phần **Thư mục chính** để ưu tiên nạp vào context trước (core / domain / app / infrastructure / tests).
- Đính kèm `README.md` của từng module khi yêu cầu AI tạo / tối ưu mã.
- Kết hợp với tài liệu kiến trúc để AI hiểu flow: request → use‑case → repo → external adapter.
