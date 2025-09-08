# 🚀 COPILOT PLAYBOOK: Desktop ↔ AI Server Integration

## 📌 MỤC TIÊU TỔNG
Triển khai trọn vẹn hệ thống tích hợp **Desktop (Electron/React) ↔ AI Server (FastAPI)** với đầy đủ tính năng upload, training, rules, logs, real-time notifications và privacy compliance.

---

## 🏗️ KIẾN TRÚC & STACK CONFIRMED

### Backend (FastAPI)
```
✅ HOÀN THÀNH: Simple Demo Server tại localhost:8002
✅ DEPENDENCIES: FastAPI, Pydantic v2, uvicorn, websockets v11
✅ ENDPOINTS: /health, /api/v1/{uploads,training,rules,logs}
✅ SCHEMAS: Pydantic models với type safety
✅ STORAGE: In-memory demo (sẵn sàng upgrade Redis)
```

### Frontend (Electron/React)
```
✅ SETUP: React 18, TypeScript, Electron 31, Material-UI, Vite
✅ SERVICES: API service layer với React Query
✅ COMPONENTS: Dashboard + TrainingPanel đã tạo
🔄 PENDING: Routing, Settings, Logs, ChatUpload, WebSocket
```

---

## 📋 ROADMAP CHI TIẾT (7 PHASES)

### **PHASE 1: API Client Generation** ⏱️ 30 phút
**Mục tiêu:** Generate TypeScript client từ OpenAPI schema

```bash
# 1. Ensure server running
cd E:\zeta
uv run python simple_demo_server.py &

# 2. Generate OpenAPI schema
curl http://localhost:8002/openapi.json > desktop_ai_zeta/openapi.json

# 3. Generate TypeScript client  
cd desktop_ai_zeta
npm install openapi-typescript-codegen
npx openapi-typescript-codegen --input openapi.json --output src/api/generated --client fetch

# 4. Verify generation
ls src/api/generated/
```

**Acceptance Criteria:**
- [ ] TypeScript client được generate thành công
- [ ] Type definitions match server schemas
- [ ] API methods có proper return types
- [ ] Error handling included

---

### **PHASE 2: Core UI Framework** ⏱️ 45 phút
**Mục tiêu:** Hoàn thiện React app structure với routing

```typescript
// src/App.tsx - Main app với routing
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, CssBaseline } from '@mui/material';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import TrainingPanel from './pages/TrainingPanel';
import Settings from './pages/Settings';
import Logs from './pages/Logs';

// src/components/Layout.tsx - Sidebar navigation
// src/components/Sidebar.tsx - Navigation menu
// src/components/TopBar.tsx - Header với notifications
```

**Files to create:**
1. `src/App.tsx` - Main app component  
2. `src/components/Layout.tsx` - Layout wrapper
3. `src/components/Sidebar.tsx` - Navigation sidebar
4. `src/components/TopBar.tsx` - Header bar
5. `src/stores/appStore.ts` - Zustand global state

**Acceptance Criteria:**
- [ ] Routing hoạt động giữa các pages
- [ ] Sidebar navigation responsive
- [ ] Global state management setup
- [ ] Material-UI theme consistent

---

### **PHASE 3: Settings & Rules Management** ⏱️ 60 phút
**Mục tiêu:** Settings page với rules management UI

```typescript
// src/pages/Settings.tsx
- Backend connection status indicator
- Rules CRUD interface (tối giản)
- Privacy settings display
- System configuration

// src/components/RuleEditor.tsx
- Form để tạo/edit rules
- JSON config editor
- Enable/disable toggle
- Validation feedback
```

**Features to implement:**
1. **Connection Status:** Real-time apps/backend health check
2. **Rules Manager:** CRUD operations với validation
3. **Privacy Notice:** Prominent display của privacy policy
4. **System Info:** Version, capabilities, diagnostics

**Acceptance Criteria:**
- [ ] Rules CRUD hoạt động complete
- [ ] Connection status real-time updates
- [ ] Privacy notice clearly visible
- [ ] Form validation works properly

---

### **PHASE 4: Logs & Notifications** ⏱️ 45 phút
**Mục tiêu:** Real-time logs viewing và notification system

```typescript
// src/pages/Logs.tsx
- Real-time log streaming (polling)
- Filter by level/source
- Export logs functionality
- Auto-scroll to latest

// src/components/NotificationCenter.tsx  
- Toast notifications
- Notification history
- System alerts
- Training job notifications
```

**Features to implement:**
1. **Log Viewer:** Table với filtering và search
2. **Real-time Updates:** Polling every 5s
3. **Export:** CSV/JSON export functionality
4. **Notifications:** Toast system cho events

**Acceptance Criteria:**
- [ ] Logs display real-time với auto-refresh
- [ ] Filter by level/source works
- [ ] Export functionality produces valid files
- [ ] Notifications appear for key events

---

### **PHASE 5: ChatUpload & Multi-media** ⏱️ 75 phút
**Mục tiêu:** Chat interface với multi-media upload

```typescript
// src/components/ChatUploadBox.tsx
- Chat message interface
- Drag & drop file upload
- File preview (images, docs)
- Upload progress indication

// src/components/FilePreview.tsx
- Image thumbnails
- Audio/video players
- Document icons
- File metadata display
```

**Features to implement:**
1. **Chat Interface:** Message input với file attachment
2. **Multi-media Upload:** Support images, audio, video, docs
3. **File Preview:** Inline preview cho uploaded files
4. **Progress Tracking:** Real-time upload progress

**Acceptance Criteria:**
- [ ] Chat interface functional
- [ ] Multiple file types supported
- [ ] File preview works for images/docs
- [ ] Upload progress accurately displayed

---

### **PHASE 6: WebSocket Real-time** ⏱️ 90 phút
**Mục tiêu:** Upgrade to real-time với WebSocket

**Backend Upgrades:**
```python
# Upgrade simple_demo_server.py hoặc dùng demo_server_standalone.py
- WebSocket endpoint cho notifications
- Real training progress simulation
- Event broadcasting system
- Connection management
```

**Frontend Upgrades:**
```typescript
// src/services/websocketService.ts
- WebSocket connection management
- Auto-reconnection logic
- Event subscriptions
- Message queuing

// Update components with real-time data
- Training progress real-time
- Log streaming via WebSocket
- System notifications
- Connection status indicator
```

**Acceptance Criteria:**
- [ ] WebSocket connection stable
- [ ] Training progress updates real-time
- [ ] Auto-reconnection works
- [ ] No message loss during disconnection

---

### **PHASE 7: Optional Recorder** ⏱️ 120 phút
**Mục tiêu:** Screen/action recording cho automation

```python
# Backend: Recorder service
- Screen capture API
- Action recording endpoints
- Playback functionality
- Macro management

# Frontend: Recorder UI
- Record button với indicators
- Recorded actions list
- Playback controls
- Macro editing interface
```

**Features to implement:**
1. **Screen Recording:** Capture user actions
2. **Action Playback:** Replay recorded macros
3. **Macro Management:** Save/load/edit macros
4. **Integration:** Connect với training pipeline

**Acceptance Criteria:**
- [ ] Screen recording captures actions
- [ ] Playback reproduces actions accurately
- [ ] Macro editing interface usable
- [ ] Integration với existing features

---

## 🧪 TESTING & QA STRATEGY

### Unit Tests (pytest)
```bash
# Run acceptance tests
uv run pytest test_integration_acceptance.py -v

# Run specific test categories
uv run pytest -k "test_health_check" -v
uv run pytest -k "test_training_job_lifecycle" -v
```

### Integration Tests (Desktop)
```typescript
// desktop_ai_zeta/src/__tests__/
- API service tests
- Component rendering tests
- User workflow tests
- WebSocket connection tests
```

### End-to-End Tests
```bash
# Full workflow tests
1. Upload file → Verify in apps/backend
2. Create training job → Start → Monitor progress
3. Create rule → Enable → Test trigger
4. View logs → Filter → Export
```

---

## 🔒 PRIVACY COMPLIANCE CHECKLIST

- [ ] **UI Notice:** Privacy notice visible on all main pages
- [ ] **Data Minimization:** API chỉ collect cần thiết data
- [ ] **Local Processing:** No data sent to external services
- [ ] **User Control:** Clear data deletion options
- [ ] **Transparency:** Open source code available for review

---

## 📊 ACCEPTANCE CRITERIA MASTER LIST

### Functional Requirements
- [ ] **File Upload:** Multi-format support với progress tracking
- [ ] **Training Jobs:** Full lifecycle management (create/start/pause/cancel)
- [ ] **Rules Management:** CRUD operations với validation
- [ ] **Logs & Monitoring:** Real-time viewing với filtering
- [ ] **Dashboard:** System overview với key metrics
- [ ] **Settings:** Configuration management
- [ ] **Notifications:** Real-time alerts và updates

### Technical Requirements  
- [ ] **Performance:** API response < 500ms, UI renders < 100ms
- [ ] **Reliability:** Auto-reconnection, error recovery
- [ ] **Security:** Input validation, safe file handling
- [ ] **Usability:** Intuitive UI, clear error messages
- [ ] **Maintainability:** Clean code, comprehensive tests

### Privacy Requirements
- [ ] **Transparency:** Clear privacy notice displayed
- [ ] **Data Minimization:** Only necessary data collected
- [ ] **User Control:** Data deletion và export options
- [ ] **Local Processing:** No external data transmission

---

## 🎯 FINAL DELIVERABLES

1. **✅ Backend API:** FastAPI server với all endpoints
2. **🔄 Desktop App:** React/Electron app với full features  
3. **✅ API Client:** TypeScript client generated từ OpenAPI
4. **✅ Test Suite:** Comprehensive tests với acceptance criteria
5. **✅ Documentation:** Setup guide và user manual
6. **✅ Privacy Compliance:** Clear notices và data handling

---

## 🚀 QUICK START COMMANDS

```bash
# Start apps/backend
cd E:\zeta
uv run python simple_demo_server.py

# Start apps/desktop app (after setup complete)
cd desktop_ai_zeta
npm run dev

# Run tests
uv run pytest test_integration_acceptance.py -v

# Generate API client
cd desktop_ai_zeta
npm run codegen:api
```

---

## 📞 COPILOT NEXT ACTIONS

**Bạn muốn tôi thực hiện phase nào tiếp theo?**

1. **🔄 Phase 1:** Generate OpenAPI client cho apps/desktop
2. **🔄 Phase 2:** Complete React app routing và layout  
3. **🔄 Phase 6:** Upgrade WebSocket real-time (bỏ qua 3-5)
4. **🔄 Phase 7:** Optional recorder system
5. **⚡ All-in-one:** Implement phases 1-2-6 liên tiếp

**Hoặc focus vào specific features:**
- **Settings & Rules UI** (Phase 3)
- **Logs & Notifications** (Phase 4) 
- **Chat & Upload** (Phase 5)
- **End-to-end Testing** 
- **Privacy & Security hardening**