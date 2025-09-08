# Project Map – zeta-monorepo

> Tự động sinh: cấu trúc thư mục, thống kê ngôn ngữ, mô tả heuristic cho folder/file then chốt.

## Tổng quan
- **Gốc**: `E:/zeta-monorepo`
- **Độ sâu cây**: `1`
- **Số thư mục (xấp xỉ)**: `17,955`
- **Số file (đếm trong cây)**: `199`
- **Phân bố ngôn ngữ (ước lượng theo đuôi file)**:
  - `other`: 73
  - `python`: 47
  - `markdown`: 28
  - `config`: 26
  - `powershell`: 23
  - `javascript`: 1
  - `shell`: 1

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
├── .benchmarks
├── .continue
├── .github
├── apps
├── backups
├── config
├── dedupe_reports
├── docs
├── examples
├── extension
├── packages
├── production
├── refactored
├── reports
├── scripts
├── shared
├── src
├── tests
├── tools
├── zeta_vn
├── .ai_knowledge_graph.json
├── .ai_knowledge_graph.json.security_backup
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
├── .prettierrc.json.security_backup
├── ai_auto_optimizer.py
├── ai_auto_optimizer.py.security_backup
├── ai_auto_refactor.py
├── ai_auto_refactor.py.security_backup
├── AI_CODE_EXPERT_PROPOSAL.md
├── AI_OPTIMIZATION_READY_TO_RUN.md
├── AI_OPTIMIZATION_RECOMMENDATIONS.md
├── AI_OPTIMIZATION_SUMMARY.md
├── ai_optimize_project.py
├── ai_optimize_project.py.security_backup
├── ai_project_analysis.json
├── ai_project_analysis.json.security_backup
├── AI_PROJECT_ANALYSIS_REPORT.md
├── ai_project_scanner.py
├── ai_project_scanner.py.security_backup
├── ai_refactor_report.json
├── AI_REFACTOR_SUMMARY.md
├── api_endpoint_discovery.py
├── api_endpoint_discovery.py.security_backup
├── API_KEY_USAGE_RECOMMENDATIONS.md
├── api_status.py
├── api_status.py.security_backup
├── benchmark_results.json
├── check_ollama_vscode.py
├── check_ollama_vscode.py.security_backup
├── check_venv_health.ps1
├── cicd_generator.py
├── cicd_generator.py.security_backup
├── configure_turbo_ollama.py
├── configure_turbo_ollama.py.security_backup
├── configure_vscode_ollama.ps1
├── consolidate_monorepo.ps1
├── consolidate_monorepo.py
├── consolidate_monorepo.py.security_backup
├── CONSOLIDATION_SUMMARY.md
├── directory_structure.py
├── directory_structure.py.security_backup
├── docker-compose.dev.yml
├── docker-compose.monitoring.yml
├── FINAL_AI_OPTIMIZATION_SUMMARY.md
├── final_project_demo.py
├── final_project_demo.py.security_backup
├── FINAL_PROJECT_STATUS.json
├── FINAL_PROJECT_STATUS.md
├── finalize_ollama_setup.py
├── finalize_ollama_setup.py.security_backup
├── find_turbo_endpoint.py
├── find_turbo_endpoint.py.security_backup
├── fix_continue.py
├── fix_continue.py.security_backup
├── fix_imports_exports.py
├── fix_imports_exports.py.security_backup
├── fix_syntax_errors.py
├── fix_syntax_errors.py.security_backup
├── gen_project_map.py
├── install_vscode_extensions.bat
├── INTEGRATION_MAP.md
├── integration_mapper.py
├── integration_mapper.py.security_backup
├── local_models_fallback.ps1
├── login.ps1
├── Makefile
├── manual_venv_recovery.ps1
├── master_optimizer.py
├── master_optimizer.py.security_backup
├── metrics_server.py
├── metrics_server.py.security_backup
├── Modelfile
├── Modelfile.zeta
├── MONITORING_SETUP.md
├── mypy.ini
├── mypy_temp.ini
├── network_diagnostics.py
├── network_diagnostics.py.security_backup
├── next_steps_advisor.ps1
├── ollama_api_config.json
├── ollama_api_optimization_guide.py
├── ollama_api_optimization_guide.py.security_backup
├── ollama_benchmark.py
├── ollama_benchmark.py.security_backup
├── ollama_config_analysis.json
├── OLLAMA_INTEGRATION_README.md
├── ollama_online_auth.py
├── ollama_online_auth.py.security_backup
├── ollama_smart_setup.py
├── ollama_smart_setup.py.security_backup
├── OLLAMA_TURBO_API_STATUS.md
├── ollama_turbo_config.json
├── ollama_turbo_integration.py
├── ollama_turbo_integration.py.security_backup
├── OPTIMIZATION_REPORT.md
├── optimization_results.json
├── OPTIMIZATION_RESULTS.md
├── optimized_turbo_client.py
├── optimized_turbo_client.py.security_backup
├── package-lock.json
├── package.json
├── PERFORMANCE_ANALYSIS_REPORT.json
├── PERFORMANCE_ANALYSIS_REPORT.md
├── performance_profiler.py
├── performance_profiler.py.security_backup
├── PHASE_2_IMPLEMENTATION_ROADMAP.md
├── production_deploy.py
├── production_deploy.py.security_backup
├── PROJECT_MAP.md
├── PROJECT_OPTIMIZATION_ROADMAP.md
├── pyproject.base.toml
├── pytest.ini
├── quick_start_turbo.py
├── quick_start_turbo.py.security_backup
├── README.md
├── REFACTORING_ANALYSIS_REPORT.json
├── REFACTORING_ANALYSIS_REPORT.md
├── REFACTORING_SUGGESTIONS.md
├── reinstall_ollama.bat
├── requirements-dev.txt
├── requirements.txt
├── ruff.toml
├── run_integration_mapper.bat
├── run_integration_mapper.ps1
├── SafeColors.psm1
├── SECURITY.md
├── SECURITY_AUDIT_REPORT.json
├── SECURITY_AUDIT_REPORT.md
├── security_auditor.py
├── security_auditor.py.security_backup
├── setup.ps1
├── setup_api_key_complete.ps1
├── setup_dev.py
├── setup_dev.py.security_backup
├── setup_local_ollama.ps1
├── setup_ollama.bat
├── setup_ollama.ps1
├── setup_ollama_turbo_online.ps1
├── setup_turbo_api.ps1
├── setup_turbo_env.bat
├── setup_turbo_ollama.py
├── setup_turbo_ollama.py.security_backup
├── setup_vscode_continue.py
├── setup_vscode_continue.py.security_backup
├── setup_vscode_ollama.py
├── setup_vscode_ollama.py.security_backup
├── setup_vscode_turbo_api.py
├── setup_vscode_turbo_api.py.security_backup
├── simple_turbo_setup.py
├── simple_turbo_setup.py.security_backup
├── smart_refactorer.py
├── smart_refactorer.py.security_backup
├── start_dev.ps1
├── start_ollama_vscode.bat
├── stop_all_background.bat
├── stop_all_background.ps1
├── test_complete_integration.ps1
├── test_local_ollama.ps1
├── test_ollama_integration.ps1
├── test_turbo_api.ps1
├── test_turbo_comprehensive.ps1
├── test_turbo_curl.bat
├── tsconfig.base.json
├── turbo_api_examples.py
├── turbo_api_implementation.py
├── turbo_api_implementation.py.security_backup
├── turbo_api_online_auth.py
├── turbo_api_online_auth.py.security_backup
├── turbo_demo.py
├── turbo_demo.py.security_backup
├── turbo_demo_report.json
├── turbo_ollama_client.py
├── turbo_ollama_client.py.security_backup
├── turbo_ollama_login.py
├── turbo_ollama_login.py.security_backup
├── turbo_quick_start.bat
├── turbo_quick_start.sh
├── turbo_setup.py
├── turbo_setup.py.security_backup
├── turbo_setup_complete.ps1
├── venv_integrity_check.ps1
├── VenvHelper.psm1
├── verify_ai_setup.py
├── verify_ai_setup.py.security_backup
├── vn_python_dataset.jsonl
├── zeta-agent-package.json
├── zeta-monorepo.md
├── ZETA_AI_AGENT_README.md
├── ZetaVenvHelper.psm1
└── 🎉_DỰ_ÁN_HOÀN_TẤT.md
```

## Gợi ý dùng làm context cho AI / Copilot
- Dùng phần **Thư mục chính** để ưu tiên nạp vào context trước (core / domain / app / infrastructure / tests).
- Đính kèm `README.md` của từng module khi yêu cầu AI tạo / tối ưu mã.
- Kết hợp với tài liệu kiến trúc để AI hiểu flow: request → use‑case → repo → external adapter.
