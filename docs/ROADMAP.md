## Giá trị cốt lõi AI Agent ZETA

1) Tự chủ và ra quyết định độc lập
- Modules: core/services/agent_orchestrator.py, core/services/workflow_engine.py, data/implementations/automation_planner_impl.py, automation_executor_impl.py

2) Học hỏi và thích nghi liên tục
- Modules: core/services/self_learning_service.py, core/services/reward_functions.py, core/services/performance_optimizer.py

3) Chủ động giải quyết vấn đề (an ninh)
- Modules: core/services/security_ai_service.py, core/services/security_ai_agent.py, core/services/prompt_injection_guard.py, app/middleware/zero_trust.py

4) Cá nhân hóa trải nghiệm
- Modules: core/services/memory_service.py, core/services/memory_manager_service.py, core/services/rag_service.py

5) Kết nối và xử lý đa nền tảng
- Modules: data/external/llm/*, desktop_ai_zeta/*

6) Khả năng siêu năng suất
- Modules: data/implementations/automation_*.py, core/services/performance/profiler.py

### Enable nhanh theo lộ trình
- MoE + học online: dùng learner.suggest(...) trước call LLM; canary 20% (moe_canary_ratio=0.2)
- Long context + RAG: chọn model dài ngữ cảnh trong config/ml_config.py; dùng rag_service
- An ninh: bật prompt_injection_guard + zero_trust middleware; theo dõi risk trong metadata

# 🗺️ Product Roadmap - ZETA AI Server

High-level roadmap for features and improvements.

## Q3

- Multi-tenant RBAC v2
- Improved memory store abstraction
- Native fine-tuning pipelines
- Integration marketplace (beta)

## Q4

- On-prem inference connectors
- Vector DB adapters (PGVecto.rs, Qdrant)
- Cost dashboards & alerts
- Guardrails and policy engine

## 2026

- Multi-region HA
- HIPAA compliance pack
- Agent collaboration tools

Contributions welcome via issues and discussions.

Last updated: 2025-08-14
