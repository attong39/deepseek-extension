# Duplicate Cleanup Plan

- DELETE production/src/refactored/test_generator_refactored.py

- DELETE production/src/refactored/test_ai_project_scanner_refactored.py

- DELETE production/src/refactored/test_setuptools_validation_refactored.py

- DELETE production/src/refactored/test_data_processor_refactored.py

- MOVE apps/backend/core/adapters/vector/tests/test_memory_vector_store.py → tests/_shared/test_memory_vector_store.py
  + SHIM apps/backend/data/adapters/vector/tests/test_memory_vector_store.py (import *)

- DELETE production/src/refactored/setuptools_validation_refactored.py

- MOVE apps/backend/core/services/tests/test_database_service.py → tests/_shared/test_database_service.py
  + SHIM apps/backend/data/services/tests/test_database_service.py (import *)

- DELETE production/src/refactored/ai_auto_optimizer_refactored.py

- DELETE production/src/refactored/data_processor_refactored.py

- MOVE apps/backend/app/websockets/tests/test_chat_websocket.py → tests/_shared/test_chat_websocket.py
  + SHIM apps/backend/app/api/websockets/tests/test_chat_websocket.py (import *)

- DELETE production/src/refactored/ai_project_scanner_refactored.py

- DELETE production/src/refactored/test_test_generator_refactored.py

- MOVE apps/backend/app/websockets/tests/test_agent_websocket.py → tests/_shared/test_agent_websocket.py
  + SHIM apps/backend/app/api/websockets/tests/test_agent_websocket.py (import *)

- DELETE production/src/refactored/test_ai_auto_optimizer_refactored.py
