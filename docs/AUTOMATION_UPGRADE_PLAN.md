# 🎯 ZETA AI - UI AUTOMATION UPGRADE PLAN

## 📋 TỔNG QUAN

Nâng cấp ZETA AI Server để tích hợp khả năng **UI Automation & Learning** theo sơ đồ trong `zeta_ai_ui_automation_learning_module_folder_map_boilerplate.md`.

## 🎯 MỤC TIÊU

1. **Computer Vision**: AI nhìn màn hình, hiểu UI, tìm elements
2. **Input Control**: Điều khiển chuột/bàn phím tự động
3. **Plan Execution**: LLM sinh plan → thực thi từng bước
4. **Learning Pipeline**: Thu thập demo → imitation learning
5. **Safety & Observability**: Giám sát, rollback, audit trail

## 📦 DEPENDENCIES CẦN THÊM

### 🔧 Thêm vào `pyproject.toml`:

```toml
# ==================== UI AUTOMATION & COMPUTER VISION ====================
"opencv-python>=4.10.0,<5.0.0",
"mss>=9.0.1,<10.0.0",  # Fast screen capture
"pyautogui>=0.9.54,<1.0.0",  # Mouse/keyboard control
"pynput>=1.7.7,<2.0.0",  # Low-level input handling
"pillow>=10.0.0,<11.0.0",  # Image processing
"orjson>=3.9.0,<4.0.0",  # Fast JSON for trajectories

# ==================== OPTIONAL AI VISION ====================
"easyocr>=1.7.1,<2.0.0",  # OCR capabilities
"ultralytics>=8.3.0,<9.0.0",  # YOLO object detection
"torch>=2.1.0,<3.0.0",  # PyTorch for learning
"torchvision>=0.16.0,<1.0.0",  # Computer vision models
```

## 🏗️ KIẾN TRÚC MỚI (Bổ sung)

### 📁 Cấu trúc thư mục:

```
zeta_vn/
├─ app/
│  ├─ api/v1/endpoints/
│  │  └─ automation.py                    # ✨ NEW: REST endpoint /api/v1/automation/*
│  ├─ websockets/
│  │  └─ automation_ws.py                 # ✨ NEW: WS stream execution events
│  ├─ middleware/
│  │  └─ safety.py                        # ✨ NEW: Safety middleware cho automation
│  └─ serializers/
│     └─ automation.py                    # ✨ NEW: Input/Output schemas
│
├─ core/
│  ├─ domain/
│  │  ├─ entities/
│  │  │  └─ automation_session.py         # ✨ NEW: AutomationSession entity
│  │  └─ value_objects/
│  │     └─ automation.py                 # ✨ NEW: ActionType, Step, Plan, BBox, Point
│  ├─ interfaces/
│  │  ├─ perception.py                    # ✨ NEW: ScreenPerception, OCR protocols
│  │  ├─ input_controller.py              # ✨ NEW: MouseKeyboardController protocol
│  │  └─ trajectory_repo.py               # ✨ NEW: TrajectoryRepository protocol
│  ├─ services/automation/
│  │  ├─ planner.py                       # ✨ NEW: LLM-based plan generation
│  │  ├─ executor.py                      # ✨ NEW: Step-by-step execution
│  │  ├─ supervisor.py                    # ✨ NEW: Monitoring & rollback
│  │  └─ safety_engine.py                # ✨ NEW: Safety rules & validation
│  └─ use_cases/automation/
│     ├─ execute_plan.py                  # ✨ NEW: Main automation use case
│     ├─ record_demo.py                   # ✨ NEW: Demo recording for learning
│     └─ train_model.py                   # ✨ NEW: Imitation learning pipeline
│
├─ data/
│  ├─ external/
│  │  ├─ opencv_perception.py             # ✨ NEW: OpenCV + MSS implementation
│  │  ├─ easyocr_ocr.py                   # ✨ NEW: OCR implementation
│  │  └─ pyautogui_controller.py          # ✨ NEW: Input control implementation
│  ├─ repositories/
│  │  └─ trajectory_repository.py         # ✨ NEW: Save/load trajectories (JSONL/DB)
│  └─ utils/
│     ├─ cv_utils.py                      # ✨ NEW: Computer vision utilities
│     └─ template_matcher.py              # ✨ NEW: Template matching algorithms
│
├─ scripts/
│  ├─ record_demo.py                      # ✨ NEW: Interactive demo recording
│  ├─ train_imitation.py                  # ✨ NEW: Behavior cloning training
│  └─ validate_automation.py              # ✨ NEW: Automation testing
│
└─ storage/
   ├─ automation/
   │  ├─ trajectories/                    # ✨ NEW: Recorded trajectories
   │  ├─ templates/                       # ✨ NEW: UI element templates
   │  ├─ models/                          # ✨ NEW: Trained models
   │  └─ demos/                           # ✨ NEW: Demo recordings
   └─ screenshots/                        # ✨ NEW: Debug screenshots
```

## 🔄 IMPLEMENTATION PHASES

### 🚀 **PHASE 1: Core Foundation (1-2 tuần)**

1. **Value Objects & Interfaces**
   ```bash
   # Tạo automation value objects
   core/domain/value_objects/automation.py

   # Tạo protocols
   core/interfaces/perception.py
   core/interfaces/input_controller.py
   core/interfaces/trajectory_repo.py
   ```

2. **Basic Implementations**
   ```bash
   # Computer vision
   data/external/opencv_perception.py
   data/external/pyautogui_controller.py
   data/repositories/trajectory_repository.py
   ```

3. **Core Services**
   ```bash
   # Business logic
   core/services/automation/planner.py
   core/services/automation/executor.py
   core/services/automation/supervisor.py
   ```

### ⚡ **PHASE 2: API & Integration (1 tuần)**

1. **REST Endpoints**
   ```bash
   app/api/v1/endpoints/automation.py
   app/serializers/automation.py
   ```

2. **Use Cases**
   ```bash
   core/use_cases/automation/execute_plan.py
   core/use_cases/automation/record_demo.py
   ```

3. **DI Integration**
   ```bash
   # Cập nhật app/dependencies.py
   # Thêm automation factories
   ```

### 🧠 **PHASE 3: Learning & Intelligence (2-3 tuần)**

1. **Demo Recording**
   ```bash
   scripts/record_demo.py
   core/use_cases/automation/record_demo.py
   ```

2. **Imitation Learning**
   ```bash
   scripts/train_imitation.py
   core/services/automation/learning_engine.py
   ```

3. **Advanced Perception**
   ```bash
   data/external/easyocr_ocr.py
   data/utils/cv_utils.py
   ```

### 🛡️ **PHASE 4: Safety & Production (1 tuần)**

1. **Safety Engine**
   ```bash
   core/services/automation/safety_engine.py
   app/middleware/safety.py
   ```

2. **Monitoring & Observability**
   ```bash
   app/websockets/automation_ws.py
   # Metrics & logging integration
   ```

3. **Testing & Validation**
   ```bash
   tests/unit/automation/
   tests/integration/automation/
   scripts/validate_automation.py
   ```

## 🔧 TECHNICAL SPECIFICATIONS

### 🎯 **Core Components:**

1. **LLM Planner**: GPT-4o sinh plan từ natural language goal
2. **Computer Vision**: Template matching + OCR để tìm UI elements
3. **Input Controller**: Async mouse/keyboard control với safety guards
4. **Trajectory Repository**: JSONL storage cho imitation learning
5. **Safety Engine**: Rule-based validation + human-in-the-loop
6. **Learning Pipeline**: Behavior cloning từ demo recordings

### 📊 **API Design:**

```python
# POST /api/v1/automation/execute
{
    "goal": "Save current Photoshop document as PNG",
    "context": "Windows 11, Photoshop 2024 opened",
    "safety_mode": "strict"
}

# WebSocket /ws/automation
{
    "type": "step_start",
    "step": {"action": "CLICK", "target": "save_button"},
    "screenshot": "data:image/png;base64,..."
}
```

### 🛡️ **Safety Features:**

1. **Domain Allowlist**: Chỉ automation trong apps được phép
2. **Panic Hotkey**: Ctrl+Alt+Shift+ESC để dừng ngay
3. **Human Confirmation**: Xác nhận cho các hành động nguy hiểm
4. **Rollback**: Undo actions khi detect lỗi
5. **Rate Limiting**: Giới hạn tần suất automation

## 🧪 TESTING STRATEGY

### Unit Tests:
- Mock OpenAI cho planner
- Mock CV functions cho perception
- Mock input controller cho executor

### Integration Tests:
- E2E automation workflows
- Safety mechanism validation
- Performance benchmarks

### Manual Testing:
- Notepad automation (simple)
- Browser automation (medium)
- Photoshop automation (complex)

## 📈 SUCCESS METRICS

1. **Accuracy**: >90% step execution success rate
2. **Safety**: 0 unintended actions outside target apps
3. **Performance**: <2s average step execution time
4. **Learning**: 80% demo → automation conversion rate
5. **Reliability**: <1% system crashes during automation

## 🚧 RISKS & MITIGATIONS

### ⚠️ **Risks:**
- **Security**: Potential malicious automation
- **Stability**: Screen detection failures
- **Performance**: High CPU usage from CV
- **Compatibility**: OS/app version differences

### 🛡️ **Mitigations:**
- Strict safety engine + domain allowlist
- Fallback detection strategies (template + OCR + heuristics)
- Optimized CV algorithms + background processing
- Version-aware templates + adaptive thresholds

## 🎯 QUICK START (Development)

```bash
# 1. Install dependencies
pip install opencv-python mss pyautogui pynput easyocr

# 2. Set up environment
export OPENAI_API_KEY=sk-...
export ZETA_AUTOMATION_SAFETY_MODE=strict

# 3. Run development server
uvicorn app.main:app --reload

# 4. Test automation endpoint
curl -X POST http://localhost:8000/api/v1/automation/execute \
  -H 'Content-Type: application/json' \
  -d '{"goal":"Open Notepad and type Hello World"}'
```

## 🔮 FUTURE ROADMAP

### Q1 2025:
- ✅ Basic automation (click, type, hotkeys)
- ✅ Template matching perception
- ✅ JSONL trajectory storage

### Q2 2025:
- 🎯 OCR-based element detection
- 🎯 Imitation learning pipeline
- 🎯 Multi-monitor support

### Q3 2025:
- 🚀 YOLO-based object detection
- 🚀 Reinforcement learning from human feedback
- 🚀 Advanced safety mechanisms

### Q4 2025:
- 🌟 Natural language → automation (no templates)
- 🌟 Self-healing automation (adaptive to UI changes)
- 🌟 Enterprise deployment tools

---

**💡 Kết luận:** Upgrade này sẽ biến ZETA AI từ text-based assistant thành **full-stack automation platform** có thể thao tác UI như con người, mở ra khả năng automation cho Photoshop, game, và mọi apps/desktop application.
