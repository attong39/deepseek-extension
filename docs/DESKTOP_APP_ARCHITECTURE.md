# 🖥️ DESKTOP_AI_ZETA - ARCHITECTURE DOCUMENTATION

> **Cập nhật lần cuối**: 2025-01-08  
> **Phiên bản**: v0.1.0  
> **Trạng thái**: Production-Ready Architecture

## 📋 EXECUTIVE SUMMARY

**desktop_ai_zeta** là ứng dụng apps/desktop Electron + React + TypeScript hỗ trợ AI assistant thông minh với khả năng automation native, training pipeline, và giao tiếp realtime với apps/backend **zeta_vn**. Kiến trúc tuân thủ các nguyên tắc Clean Architecture và Component-Based Design.

### **🎯 Mục tiêu chính**

- **User Experience**: Giao diện thân thiện với khả năng chat AI, training automation, và điều khiển hệ thống
- **Native Integration**: Tận dụng APIs của hệ điều hành (mouse, keyboard, screen capture, OCR)
- **Real-time Sync**: Đồng bộ hóa trạng thái với apps/backend qua REST API + WebSocket
- **Security**: Permission management, token-based auth, secure communication
- **Scalability**: Component modular, service layer pattern, automated testing

---

## 🏗️ CORE TECHNOLOGY STACK

### **Frontend Framework**

```json
{
  "name": "desktop_ai_zeta",
  "version": "0.1.0",
  "description": "ZETA AI Desktop (Electron + React + Vite + TypeScript)",
  "main": "electron/main.js",
  "type": "module"
}
```

### **Production Dependencies**

```typescript
// Chính
"react": "^18.3.1"              // UI framework
"react-dom": "^18.3.1"          // DOM renderer
"react-router-dom": "^7.8.1"    // Client routing

// UI & Styling
"@mui/material": "^6.1.6"       // Material Design components
"@mui/icons-material": "^6.1.6" // Icons
"@emotion/react": "^11.13.3"    // CSS-in-JS
"@emotion/styled": "^11.13.0"   // Styled components

// State & Data
"zustand": "^4.5.2"             // State management
"@tanstack/react-query": "^5.56.2" // Server state
"axios": "^1.7.7"               // HTTP client

// Utilities
"i18next": "^23.15.1"           // Internationalization
"react-i18next": "^15.1.4"      // React i18n integration
"notistack": "^3.0.2"           // Notifications
"tesseract.js": "^5.1.1"        // OCR processing
"crypto-js": "^4.2.0"           // Cryptography
"ajv": "^8.17.1"                // JSON schema validation
"electron-updater": "^4.6.5"    // Auto-updates
```

### **Development Dependencies**

```typescript
// Electron & Build
"electron": "^31.4.0"           // Desktop runtime
"electron-builder": "^25.1.8"   // Packaging
"vite": "^5.4.6"                // Build tool
"typescript": "^5.6.2"          // Type system

// Testing
"vitest": "^2.1.2"              // Test runner
"@testing-library/react": "^16.0.1" // Component testing
"@testing-library/jest-dom": "^6.6.3" // DOM matchers
"jsdom": "^25.0.1"              // DOM environment

// Code Quality
"openapi-typescript": "^7.4.2"  // API type generation
"openapi-typescript-codegen": "^0.29.0" // SDK generation
"jscpd": "^3.5.10"              // Duplicate detection

// Development Tools
"concurrently": "^9.0.1"        // Parallel commands
"wait-on": "^8.0.0"             // Service waiting
```

---

## 📁 PROJECT STRUCTURE - ACTUAL IMPLEMENTATION

```text
desktop_ai_zeta/
├── 📦 package.json                    # Project configuration & dependencies
├── 🔧 vite.config.ts                  # Vite build configuration
├── 📝 tsconfig.json                   # TypeScript configuration
├── 🧪 vitest.config.ts               # Test configuration
├── 📋 .jscpd.json                     # Duplicate detection config
├── 🐳 .dockerignore                   # Docker ignore patterns
├── 📝 README.md                       # Project documentation
│
├── 🚀 electron/                       # Electron main process
│   ├── main.js                        # Main entry point (ESM)
│   ├── main.ts                        # TypeScript main (future)
│   ├── preload.js                     # Security bridge
│   ├── preload.ts                     # TypeScript preload
│   ├── ipcHandler.js                  # IPC message routing
│   ├── robotExec.js                   # Native automation
│   └── whisperManager.js              # STT integration
│
├── 🎨 src/                            # React application source
│   ├── 📱 components/                  # React components
│   │   ├── MainDashboard.tsx           # Main dashboard container
│   │   ├── ChatPanel.tsx              # Chat interface
│   │   ├── ControlPanel.tsx           # Automation controls
│   │   ├── TrainingPanel.tsx          # Training interface
│   │   ├── PermissionDialog.tsx       # Permission management
│   │   ├── SystemStatus.tsx           # System monitoring
│   │   ├── NotificationCenter.tsx     # Notification display
│   │   ├── ThemeProvider.tsx          # Theme management
│   │   └── ErrorBoundary.tsx          # Error handling
│   │
│   ├── 🛠️ services/                   # Service layer
│   │   ├── apiService.ts              # REST API client
│   │   ├── commandHandler.ts          # Command processing
│   │   ├── inputController.ts         # Input handling
│   │   ├── robotIntegration.ts        # Automation service
│   │   ├── screenCapture.ts           # Screen capture
│   │   ├── trainingSocket.ts          # Training WebSocket
│   │   ├── permissionManager.ts       # Permission handling
│   │   ├── feedbackService.ts         # User feedback
│   │   ├── contextService.ts          # Context management
│   │   ├── cache.ts                   # Caching service
│   │   ├── actionQueue.ts             # Action queueing
│   │   └── automationService.ts       # Automation orchestration
│   │
│   ├── 🔌 api/                        # Backend integration
│   │   ├── generated/                 # Auto-generated API client
│   │   │   ├── index.ts               # Main API exports
│   │   │   ├── models/                # Data models
│   │   │   └── services/              # Service interfaces
│   │   ├── wsSchema.ts                # WebSocket schemas
│   │   └── types.ts                   # Type definitions
│   │
│   ├── 🌐 i18n/                       # Internationalization
│   │   ├── index.ts                   # i18n configuration
│   │   ├── vi.json                    # Vietnamese translations
│   │   └── en.json                    # English translations
│   │
│   ├── 🎨 styles/                     # Styling
│   │   ├── globals.css                # Global styles
│   │   ├── theme.ts                   # MUI theme
│   │   └── components.css             # Component styles
│   │
│   ├── 🔧 utils/                      # Utilities
│   │   ├── validation.ts              # Input validation
│   │   ├── formatting.ts              # Data formatting
│   │   ├── constants.ts               # App constants
│   │   └── helpers.ts                 # Helper functions
│   │
│   ├── 🧪 test/                       # Test setup
│   │   └── setup.ts                   # Test environment
│   │
│   ├── 📄 App.tsx                     # Root React component
│   ├── 🏠 main.tsx                    # React entry point
│   └── 📝 vite-env.d.ts              # Vite type definitions
│
├── 🧪 tests/                          # Test files
│   ├── actionQueue.test.ts            # Action queue tests
│   ├── batchReset.test.ts            # Batch reset tests
│   ├── test_cache.ts                 # Cache system tests
│   └── README.md                     # Testing documentation
│
├── 🚀 scripts/                        # Automation scripts
│   ├── generate_openapi_types.mjs     # API type generation
│   ├── api_codegen.mjs               # SDK generation
│   ├── sync_ws_schema.mjs            # WebSocket sync
│   ├── contract_guard.mjs            # Contract validation
│   └── write_contract_snapshot.mjs   # Contract snapshots
│
├── 🔨 dist/                          # Build output
├── 📦 node_modules/                  # Dependencies
└── 🏗️ build/                        # Electron build artifacts
```

---

## 🎨 REACT COMPONENT ARCHITECTURE

### **📱 Core Components (src/components/)**

#### **MainDashboard.tsx - Central Hub**

```typescript
// Main dashboard component với tab navigation
export const MainDashboard: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<TabType>('chat');
  const [systemStatus, setSystemStatus] = useState<SystemStatus>();
  
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Sidebar 
        selectedTab={selectedTab}
        onTabChange={setSelectedTab}
        systemStatus={systemStatus}
      />
      <MainContent>
        {selectedTab === 'chat' && <ChatPanel />}
        {selectedTab === 'control' && <ControlPanel />}
        {selectedTab === 'training' && <TrainingPanel />}
        {selectedTab === 'settings' && <SettingsPanel />}
      </MainContent>
      <NotificationCenter />
    </Box>
  );
};
```

#### **ChatPanel.tsx - AI Chat Interface**

```typescript
// Real-time chat với AI apps/backend
export const ChatPanel: React.FC = () => {
  const { messages, sendMessage, isLoading } = useChatService();
  const { t } = useTranslation();
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <ChatHeader />
      <MessageList messages={messages} />
      <ChatInput 
        onSendMessage={sendMessage}
        disabled={isLoading}
        placeholder={t('chat_placeholder')}
      />
    </Box>
  );
};
```

#### **ControlPanel.tsx - Automation Control**

```typescript
// Desktop automation control interface
export const ControlPanel: React.FC = () => {
  const { permissions, requestPermission } = usePermissions();
  const { executeAutomation, isExecuting } = useAutomation();
  
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <PermissionStatus permissions={permissions} />
      </Grid>
      <Grid item xs={6}>
        <ScreenCapturePanel />
      </Grid>
      <Grid item xs={6}>
        <InputControlPanel />
      </Grid>
      <Grid item xs={12}>
        <AutomationQueue />
      </Grid>
    </Grid>
  );
};
```

#### **TrainingPanel.tsx - AI Training Interface**

```typescript
// Training pipeline management
export const TrainingPanel: React.FC = () => {
  const { trainingStatus, startTraining, stopTraining } = useTraining();
  const trainingSocket = useTrainingSocket();
  
  return (
    <Box>
      <TrainingStatus status={trainingStatus} />
      <TrainingControls 
        onStart={startTraining}
        onStop={stopTraining}
        disabled={trainingStatus === 'running'}
      />
      <TrainingLogs socket={trainingSocket} />
      <TrainingMetrics />
    </Box>
  );
};
```

---

## 🛠️ SERVICE LAYER ARCHITECTURE

### **🔌 Backend Integration (src/services/)**

#### **apiService.ts - REST API Client**

```typescript
// Auto-generated từ OpenAPI schema của zeta_vn
import { Configuration, DefaultApi } from '../api/generated';
import { useAuthStore } from '../stores/authStore';

class ApiService {
  private api: DefaultApi;
  
  constructor() {
    this.api = new DefaultApi(new Configuration({
      basePath: window.DESKTOP_API_BASE_URL || 'http://127.0.0.1:8000',
      accessToken: () => useAuthStore.getState().token
    }));
  }
  
  // Agent management
  async getAgents() { return this.api.getAgents(); }
  async createAgent(data: CreateAgentRequest) { return this.api.createAgent(data); }
  
  // Chat operations
  async sendMessage(data: ChatMessageRequest) { return this.api.sendChatMessage(data); }
  async getChatHistory(sessionId: string) { return this.api.getChatHistory(sessionId); }
  
  // Training operations
  async startTraining(config: TrainingConfig) { return this.api.startTraining(config); }
  async getTrainingStatus() { return this.api.getTrainingStatus(); }
}

export const apiService = new ApiService();
```

#### **robotIntegration.ts - Native Automation**

```typescript
// Electron IPC integration cho native automation
export class RobotIntegrationService {
  async clickAt(x: number, y: number, button: 'left' | 'right' = 'left'): Promise<boolean> {
    try {
      return await window.zeta.executeAutomation({
        type: 'mouse_click',
        x, y, button
      });
    } catch (error) {
      console.error('Failed to execute click:', error);
      return false;
    }
  }
  
  async typeText(text: string): Promise<boolean> {
    return await window.zeta.executeAutomation({
      type: 'keyboard_type',
      text
    });
  }
  
  async captureScreen(): Promise<string | null> {
    return await window.zeta.captureScreen();
  }
  
  async ocrText(imageBase64: string): Promise<string> {
    return await window.zeta.ocrText(imageBase64);
  }
}

export const robotService = new RobotIntegrationService();
```

#### **trainingSocket.ts - Real-time Training**

```typescript
// WebSocket connection cho real-time training updates
export class TrainingSocketService {
  private socket: WebSocket | null = null;
  private listeners: Map<string, Function[]> = new Map();
  
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const wsUrl = `ws://127.0.0.1:8000/ws/training`;
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
          console.log('Training WebSocket connected');
          resolve();
        };
        
        this.socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          this.emit(data.type, data.payload);
        };
        
        this.socket.onerror = reject;
      } catch (error) {
        reject(error);
      }
    });
  }
  
  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }
  
  private emit(event: string, data: any) {
    const callbacks = this.listeners.get(event) || [];
    callbacks.forEach(callback => callback(data));
  }
}

export const trainingSocket = new TrainingSocketService();
```

#### **permissionManager.ts - Permission Handling**

```typescript
// Quản lý permissions cho native operations
export class PermissionManager {
  private permissions: Map<string, boolean> = new Map();
  
  async requestScreenPermission(): Promise<boolean> {
    try {
      const granted = await window.zeta.requestPermission('screen');
      this.permissions.set('screen', granted);
      return granted;
    } catch (error) {
      console.error('Failed to request screen permission:', error);
      return false;
    }
  }
  
  async requestInputPermission(): Promise<boolean> {
    try {
      const granted = await window.zeta.requestPermission('input');
      this.permissions.set('input', granted);
      return granted;
    } catch (error) {
      console.error('Failed to request input permission:', error);
      return false;
    }
  }
  
  hasPermission(type: string): boolean {
    return this.permissions.get(type) || false;
  }
  
  async requestAllPermissions(): Promise<PermissionStatus> {
    const screen = await this.requestScreenPermission();
    const input = await this.requestInputPermission();
    
    return { screen, input };
  }
}

export const permissionManager = new PermissionManager();
```

---

## 🖥️ ELECTRON MAIN PROCESS - ACTUAL IMPLEMENTATION

### **electron/ - Electron Core System**

#### **main.js - Main Entry Point**

```typescript
// electron/main.js
import { app, BrowserWindow, ipcMain } from 'electron';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const isDev = process.env.NODE_ENV === 'development';

async function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1100,
    height: 720,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  
  if (isDev) {
    await mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    await mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
  
  return mainWindow;
}

app.whenReady().then(createWindow);

// IPC handlers
ipcMain.handle('execute-automation', async (event, command) => {
  // Route to appropriate handler
  return await ipcHandler.handleAutomation(command);
});
```

#### **preload.js - Security Bridge**

```typescript
// electron/preload.js
import { contextBridge, ipcRenderer } from 'electron';

// Expose safe APIs to renderer process
contextBridge.exposeInMainWorld('zeta', {
  executeAutomation: (command) => ipcRenderer.invoke('execute-automation', command),
  captureScreen: () => ipcRenderer.invoke('capture-screen'),
  ocrText: (imageData) => ipcRenderer.invoke('ocr-text', imageData),
  requestPermission: (type) => ipcRenderer.invoke('request-permission', type),
  
  // Event listeners
  onTrainingUpdate: (callback) => {
    ipcRenderer.on('training-update', (_event, data) => callback(data));
  },
  
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel);
  }
});
```

#### **robotExec.js - Native Automation**

```typescript
// electron/robotExec.js
import robot from 'robotjs';

export class RobotExecutor {
  async executeMouseClick(x, y, button = 'left') {
    try {
      robot.moveMouse(x, y);
      robot.mouseClick(button);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  async executeKeyboardType(text) {
    try {
      robot.typeString(text);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
  
  async captureScreen() {
    try {
      const img = robot.screen.capture();
      return {
        success: true,
        data: img.image.toString('base64'),
        width: img.width,
        height: img.height
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

export const robotExecutor = new RobotExecutor();
```

---

## 🌐 INTERNATIONALIZATION - ACTUAL IMPLEMENTATION

### **src/i18n/ - Multi-language Support**

#### **index.ts - i18n Configuration**

```typescript
// src/i18n/index.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import vi from './vi.json';
import en from './en.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      vi: { translation: vi },
      en: { translation: en }
    },
    lng: 'vi', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
```

#### **vi.json - Vietnamese Translations**

```json
{
  "train_button": "Huấn luyện AI",
  "start_button": "Bắt đầu",
  "stop_button": "Dừng lại",
  "chat_placeholder": "Nhập tin nhắn...",
  "send_button": "Gửi",
  "permission_screen": "Quyền đọc màn hình",
  "permission_mouse": "Quyền điều khiển chuột",
  "permission_keyboard": "Quyền điều khiển bàn phím",
  "permission_granted": "Đã cấp quyền",
  "permission_denied": "Từ chối quyền",
  "training_status_idle": "Sẵn sàng",
  "training_status_running": "Đang huấn luyện",
  "training_status_completed": "Hoàn thành",
  "automation_executing": "Đang thực thi automation",
  "screen_capture_success": "Chụp màn hình thành công",
  "connection_status_connected": "Đã kết nối",
  "connection_status_disconnected": "Mất kết nối"
}
```

#### **en.json - English Translations**

```json
{
  "train_button": "Train AI",
  "start_button": "Start",
  "stop_button": "Stop",
  "chat_placeholder": "Enter message...",
  "send_button": "Send",
  "permission_screen": "Screen Reading Permission",
  "permission_mouse": "Mouse Control Permission",
  "permission_keyboard": "Keyboard Control Permission",
  "permission_granted": "Permission Granted",
  "permission_denied": "Permission Denied",
  "training_status_idle": "Ready",
  "training_status_running": "Training",
  "training_status_completed": "Completed",
  "automation_executing": "Executing Automation",
  "screen_capture_success": "Screen Captured Successfully",
  "connection_status_connected": "Connected",
  "connection_status_disconnected": "Disconnected"
}
```

---

## 🧪 TESTING STRATEGY - CURRENT IMPLEMENTATION

### **Testing Structure & Configuration**

```text
tests/                             # 🧪 Test suite (Vitest)
├── actionQueue.test.ts            # Action queue processing tests
├── batchReset.test.ts            # Batch ID emergency stop tests  
├── test_cache.ts                 # Cache functionality validation
└── README.md                     # Testing documentation

src/test/                         # 🔧 Test setup & configuration
└── setup.ts                     # Global test environment setup
```

### **Current Testing Configuration (Vitest + React Testing Library)**

```typescript
// package.json - Test Scripts
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run",
    "test:smoke": "vitest run tests/test_cache.ts"
  },
  "vitest": {
    "environment": "jsdom",
    "setupFiles": ["src/test/setup.ts"]
  }
}

// src/test/setup.ts - Actual Test Environment Setup
import "@testing-library/jest-dom";
import { vi } from "vitest";

// Global window shim
if (typeof (globalThis as any).window === "undefined") {
  (globalThis as any).window = {};
}

// Environment variables
if (!(globalThis as any).window.DESKTOP_API_BASE_URL) {
  (globalThis as any).window.DESKTOP_API_BASE_URL = "http://127.0.0.1:8000";
}

// localStorage mock
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem(key: string) { return store[key] ?? null; },
    setItem(key: string, value: string) { store[key] = String(value); },
    removeItem(key: string) { delete store[key]; },
    clear() { store = {}; }
  };
})();

// Electron module mock
vi.mock("electron", () => ({
  BrowserWindow: (() => ({})) as any,
  ipcMain: { handle: () => {} },
  ipcRenderer: {
    on: () => {},
    removeListener: () => {},
    invoke: () => Promise.resolve(),
  },
  app: { 
    getPath: () => ".", 
    whenReady: () => Promise.resolve(), 
    on: () => {} 
  },
}));
```

### **Existing Test Cases**

#### **1. Action Queue Tests**

```typescript
// tests/actionQueue.test.ts
import { beforeEach, describe, expect, it } from "vitest";
import { actionQueue } from "../src/services/actionQueue";

describe("actionQueue", () => {
  beforeEach(() => {
    actionQueue.disable();
    actionQueue.clear();
    actionQueue.setRunner(async () => true);
    actionQueue.setShouldCancel(() => false);
  });

  it("enqueue processes when enabled", async () => {
    actionQueue.enable();
    expect(actionQueue.size()).toBe(0);
    actionQueue.enqueue(mkAction("type_text"));
    expect(actionQueue.size()).toBe(1);
    await new Promise((r) => setTimeout(r, 10));
    expect(actionQueue.size()).toBe(0);
  });

  it("clear empties queue immediately", async () => {
    actionQueue.enable();
    actionQueue.enqueue(mkAction("type_text"));
    actionQueue.enqueue(mkAction("click"));
    expect(actionQueue.size()).toBe(2);
    actionQueue.clear();
    expect(actionQueue.size()).toBe(0);
  });
});
```

#### **2. Batch Reset & Emergency Stop Tests**

```typescript
// tests/batchReset.test.ts
import { describe, expect, it } from "vitest";
import {
  setCurrentBatchId,
  resetEmergencyStop,
  handleServerCommand,
} from "../src/services/commandHandler";

describe("batch id resets emergency stop", () => {
  it("resets flag when batch id changes", () => {
    resetEmergencyStop();
    setCurrentBatchId("batch-1");
    const r1 = fakeCommand();
    expect(typeof r1).toBe("boolean");
    
    setCurrentBatchId("batch-2");
    const r2 = fakeCommand();
    expect(typeof r2).toBe("boolean");
  });
});
```

#### **3. Cache System Tests**

```typescript
// tests/test_cache.ts
import { MemoryCache } from "../src/services/cache";

async function run() {
  const cache = new MemoryCache();
  await cache.clear();
  await cache.set<string>("k1", "v1", 1); // ttl 1s
  const e1 = await cache.get<string>("k1");
  if (!e1 || e1.value !== "v1") throw new Error("cache miss or wrong value");
  
  await sleep(1200);
  const e2 = await cache.get<string>("k1");
  if (e2 !== null) throw new Error("ttl did not expire");
  console.log("MemoryCache tests passed");
}
```

### **CI/CD Testing Pipeline**

```yaml
# .github/workflows/desktop-tests.yml
name: Desktop - Run Vitest
on:
  push:
    paths: ["desktop_ai_zeta/**"]
  pull_request:
    paths: ["desktop_ai_zeta/**"]

jobs:
  test-desktop:
    name: Run apps/desktop tests (Vitest)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js 18
        uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: "npm"
      - name: Install dependencies
        working-directory: desktop_ai_zeta
        run: npm ci
      - name: Run tests
        working-directory: desktop_ai_zeta
        run: npm run test -- --run
```

### **Testing Dependencies**

```json
{
  "devDependencies": {
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.0.1",
    "vitest": "^2.1.2",
    "jsdom": "^25.0.1"
  }
}
```

---

## 🔌 BACKEND INTEGRATION - zeta_vn Sync

### **🌐 REST API Integration**

#### **Auto-generated SDK**

```typescript
// scripts/generate_openapi_types.mjs
import { generateApi } from 'openapi-typescript-codegen';

await generateApi({
  input: 'http://127.0.0.1:8000/openapi.json',
  output: './src/api/generated',
  httpClient: 'axios',
  useOptions: true,
  useUnionTypes: true,
  exportCore: true,
  exportServices: true,
  exportModels: true,
  exportSchemas: false,
});
```

#### **Contract Guard System**

```typescript
// scripts/contract_guard.mjs
// Kiểm tra tính nhất quán API schema giữa apps/desktop và apps/backend
const response = await fetch('http://127.0.0.1:8000/openapi.json');
const serverSchema = await response.json();
const clientSchema = JSON.parse(fs.readFileSync('./api_contract_snapshot.json', 'utf8'));

// So sánh và cảnh báo breaking changes
const changes = compareSchemas(serverSchema, clientSchema);
if (changes.breaking.length > 0) {
  console.error('🚨 BREAKING API CHANGES DETECTED:');
  changes.breaking.forEach(change => console.error(`  - ${change}`));
  process.exit(1);
}
```

### **🔄 WebSocket Real-time Communication**

```typescript
// src/api/wsSchema.ts
import { z } from 'zod';

export const ChatMessageSchema = z.object({
  type: z.literal('chat_message'),
  payload: z.object({
    session_id: z.string(),
    message: z.string(),
    timestamp: z.string()
  })
});

export const TrainingUpdateSchema = z.object({
  type: z.literal('training_update'),
  payload: z.object({
    status: z.enum(['started', 'progress', 'completed', 'error']),
    progress: z.number().optional(),
    message: z.string().optional()
  })
});

export type WSMessage = 
  | z.infer<typeof ChatMessageSchema>
  | z.infer<typeof TrainingUpdateSchema>;
```

---

## ⚙️ BUILD & DEPLOYMENT CONFIGURATION

### **🏗️ Vite Configuration**

```typescript
// vite.config.ts
export default defineConfig(({ mode }) => ({
  base: "./",  // Relative base cho Electron
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
  },
  build: {
    outDir: "dist",
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@components": fileURLToPath(new URL("./src/components", import.meta.url)),
      "@hooks": fileURLToPath(new URL("./src/hooks", import.meta.url)),
      "@services": fileURLToPath(new URL("./src/services", import.meta.url)),
      "@utils": fileURLToPath(new URL("./src/utils", import.meta.url)),
    },
  },
}));
```

### **📦 NPM Scripts - Complete Set**

```json
{
  "scripts": {
    "dev": "concurrently -k \"vite\" \"wait-on tcp:5173 && electron .\"",
    "build": "vite build && electron-builder --dir",
    "build:win": "vite build && electron-builder -w",
    "test": "vitest",
    "test:unit": "vitest run",
    "test:smoke": "vitest run tests/test_cache.ts",
    "ts:check": "tsc -p tsconfig.json --noEmit",
    "preview": "vite preview",
    "openapi:gen": "node scripts/generate_openapi_types.mjs",
    "api:gen": "node scripts/api_codegen.mjs",
    "ws:sync": "node scripts/sync_ws_schema.mjs",
    "contract:guard": "node scripts/contract_guard.mjs",
    "contract:snapshot": "node scripts/write_contract_snapshot.mjs",
    "dup:js": "jscpd --config .jscpd.json src"
  }
}
```

### **🏭 Electron Builder Configuration**

```json
{
  "build": {
    "appId": "vn.zeta.desktop_ai",
    "productName": "ZETA AI Desktop",
    "directories": {
      "output": "build"
    },
    "files": [
      "dist/**/*",
      "electron/**/*",
      "node_modules/**/*",
      "package.json"
    ],
    "win": {
      "target": "nsis",
      "icon": "assets/icon.ico"
    },
    "mac": {
      "target": "dmg",
      "icon": "assets/icon.icns"
    },
    "linux": {
      "target": "AppImage",
      "icon": "assets/icon.png"
    }
  }
}
```

---

## 🔐 SECURITY & PERMISSIONS

### **🛡️ Electron Security Best Practices**

```typescript
// electron/main.js - Security Configuration
const mainWindow = new BrowserWindow({
  webPreferences: {
    nodeIntegration: false,           // ❌ Disable Node in renderer
    contextIsolation: true,          // ✅ Enable context isolation
    enableRemoteModule: false,       // ❌ Disable remote module
    sandbox: true,                   // ✅ Enable sandbox (if possible)
    preload: path.join(__dirname, 'preload.js') // ✅ Safe API bridge
  }
});

// CSP Header
mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self' 'unsafe-inline' data: blob:; " +
        "connect-src 'self' ws://127.0.0.1:8000 http://127.0.0.1:8000; " +
        "img-src 'self' data: blob:;"
      ]
    }
  });
});
```

### **🔑 Permission Management System**

```typescript
// src/services/permissionManager.ts
export interface PermissionStatus {
  screen: boolean;     // Screen reading permission
  input: boolean;      // Keyboard/mouse control permission
  microphone: boolean; // Audio recording permission
  camera: boolean;     // Camera access permission
}

export class PermissionManager {
  async requestPermissions(): Promise<PermissionStatus> {
    const permissions: PermissionStatus = {
      screen: await this.requestScreenPermission(),
      input: await this.requestInputPermission(),
      microphone: await this.requestMicrophonePermission(),
      camera: await this.requestCameraPermission()
    };
    
    // Lưu vào localStorage để persistent
    localStorage.setItem('permissions', JSON.stringify(permissions));
    return permissions;
  }
  
  private async requestScreenPermission(): Promise<boolean> {
    try {
      return await window.zeta.requestPermission('screen');
    } catch (error) {
      console.error('Screen permission error:', error);
      return false;
    }
  }
}
```

---

## 📊 PERFORMANCE & MONITORING

### **🚀 Performance Optimization**

```typescript
// React Performance
export const ChatPanel = React.memo(() => {
  const [messages, setMessages] = useState<Message[]>([]);
  
  // Virtualize large message lists
  const virtualizedMessages = useMemo(() => {
    return messages.slice(-100); // Chỉ render 100 tin nhắn gần nhất
  }, [messages]);
  
  // Debounce user input
  const debouncedSendMessage = useCallback(
    debounce(async (message: string) => {
      await apiService.sendMessage({ message });
    }, 300),
    []
  );
  
  return (
    <VirtualizedList
      items={virtualizedMessages}
      renderItem={({ item }) => <MessageComponent message={item} />}
      height={400}
    />
  );
});

// Service Worker caching
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(registration => console.log('SW registered:', registration))
    .catch(error => console.log('SW registration failed:', error));
}
```

### **📈 Monitoring & Telemetry**

```typescript
// src/services/telemetryService.ts
export class TelemetryService {
  private metrics: Map<string, number> = new Map();
  
  trackEvent(event: string, properties?: Record<string, any>) {
    const timestamp = Date.now();
    const data = {
      event,
      properties,
      timestamp,
      sessionId: this.getSessionId()
    };
    
    // Gửi lên apps/backend analytics endpoint
    this.sendToAnalytics(data);
  }
  
  trackPerformance(metric: string, duration: number) {
    this.metrics.set(metric, duration);
    
    // Gửi performance metrics
    this.sendPerformanceData({
      metric,
      duration,
      timestamp: Date.now()
    });
  }
  
  private async sendToAnalytics(data: any) {
    try {
      await apiService.sendAnalytics(data);
    } catch (error) {
      // Fallback: lưu local để retry sau
      this.queueForRetry(data);
    }
  }
}

export const telemetry = new TelemetryService();
```

---

## 🚀 DEVELOPMENT WORKFLOW

### **🔧 Development Commands**

```bash
# 🏃‍♂️ Development
npm run dev              # Start development server + Electron
npm run ts:check         # TypeScript type checking
npm run test             # Run Vitest tests
npm run test:smoke       # Quick smoke tests

# 🏗️ Building
npm run build            # Build for production
npm run build:win        # Build Windows installer
npm run preview          # Preview production build

# 🔌 API Integration
npm run openapi:gen      # Generate API types from apps/backend
npm run api:gen          # Generate full SDK
npm run contract:guard   # Validate API contract consistency
npm run ws:sync          # Sync WebSocket schemas

# 🧹 Code Quality
npm run dup:js           # Check for code duplication
```

### **🏭 Production Build Process**

```bash
# 1. Generate latest API contracts
npm run contract:guard

# 2. Type checking
npm run ts:check

# 3. Run tests
npm run test:unit

# 4. Build for production
npm run build

# 5. Package for distribution
npm run build:win  # hoặc build:mac, build:linux
```

---

## 🎯 INTEGRATION WITH ZETA_VN BACKEND

### **🔄 Data Flow Architecture**

```text
Desktop Client (Electron + React)
    ↕️ REST API (HTTP/HTTPS)
    ↕️ WebSocket (WS/WSS)
ZETA_VN Backend (FastAPI)
    ↕️ PostgreSQL (Primary Data)
    ↕️ Redis (Cache + Pub/Sub)
    ↕️ Vector DB (Embeddings)
    ↕️ S3 (File Storage)
```

### **📡 Communication Protocols**

#### **REST API Endpoints**

```typescript
// Key API endpoints used by apps/desktop client
const API_ENDPOINTS = {
  // Authentication
  login: 'POST /api/v1/auth/login',
  refresh: 'POST /api/v1/auth/refresh',
  
  // Agents
  getAgents: 'GET /api/v1/agents',
  createAgent: 'POST /api/v1/agents',
  updateAgent: 'PUT /api/v1/agents/{id}',
  
  // Chat
  sendMessage: 'POST /api/v1/chat/message',
  getChatHistory: 'GET /api/v1/chat/history/{session_id}',
  
  // Training
  startTraining: 'POST /api/v1/training/start',
  getTrainingStatus: 'GET /api/v1/training/status',
  
  // System
  health: 'GET /api/v1/health',
  metrics: 'GET /api/v1/metrics'
};
```

#### **WebSocket Events**

```typescript
// Real-time event types
type WSEventType = 
  | 'chat_message'        // Real-time chat updates
  | 'training_progress'   // Training pipeline updates
  | 'system_notification'// System-wide notifications
  | 'agent_status_change' // Agent state changes
  | 'error_notification'; // Error alerts
```

### **🔧 Environment Configuration**

```typescript
// src/config/environment.ts
export const CONFIG = {
  // Backend URLs
  API_BASE_URL: process.env.DESKTOP_API_BASE_URL || 'http://127.0.0.1:8000',
  WS_BASE_URL: process.env.DESKTOP_WS_BASE_URL || 'ws://127.0.0.1:8000',
  
  // Feature flags
  ENABLE_AUTOMATION: process.env.ENABLE_AUTOMATION !== 'false',
  ENABLE_TRAINING: process.env.ENABLE_TRAINING !== 'false',
  ENABLE_TELEMETRY: process.env.ENABLE_TELEMETRY !== 'false',
  
  // Performance settings
  MAX_CHAT_HISTORY: parseInt(process.env.MAX_CHAT_HISTORY || '1000'),
  CACHE_TTL: parseInt(process.env.CACHE_TTL || '300'), // 5 minutes
  
  // Security
  TOKEN_REFRESH_INTERVAL: parseInt(process.env.TOKEN_REFRESH_INTERVAL || '900000'), // 15 minutes
};
```

---

## 🎯 ROADMAP & FUTURE ENHANCEMENTS

### **📅 Phase 1: Current Implementation (Q1 2025) ✅**

- [x] **Core Desktop App**: Electron + React + TypeScript foundation
- [x] **Basic Components**: Chat, Control Panel, Training interface
- [x] **Backend Integration**: REST API client với auto-generated SDK
- [x] **Native Automation**: Screen capture, mouse/keyboard control
- [x] **Testing Setup**: Vitest + React Testing Library
- [x] **CI/CD Pipeline**: GitHub Actions cho automated testing

### **📅 Phase 2: Advanced Features (Q2 2025) 🚧**

- [ ] **Enhanced UI/UX**: Material Design 3.0, advanced animations
- [ ] **Voice Integration**: Speech-to-text, text-to-speech
- [ ] **Advanced Automation**: Computer vision, smart element detection
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Performance Optimization**: Worker threads, lazy loading
- [ ] **Enhanced Security**: Biometric authentication, encryption

### **📅 Phase 3: Enterprise Features (Q3 2025) 📋**

- [ ] **Multi-Agent Orchestration**: Multiple AI agents collaboration
- [ ] **Advanced Analytics**: Usage metrics, performance monitoring
- [ ] **Enterprise Admin**: User management, policy enforcement
- [ ] **Cloud Sync**: Cross-device synchronization
- [ ] **API Extensions**: Custom API endpoints, webhooks
- [ ] **Advanced Training**: Federated learning, custom models

### **📅 Phase 4: Platform Expansion (Q4 2025) 🌐**

- [ ] **Mobile Companion**: React Native mobile app
- [ ] **Web Dashboard**: Browser-based admin interface
- [ ] **API Ecosystem**: Third-party integrations
- [ ] **Market Ready**: App store distribution
- [ ] **Enterprise Scale**: Multi-tenant architecture
- [ ] **Global Deployment**: CDN, edge computing

---

## 📞 SUPPORT & TROUBLESHOOTING

### **🐛 Common Issues & Solutions**

#### **Development Environment**

```bash
# ❌ Issue: npm install fails
# ✅ Solution: Clear cache và reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# ❌ Issue: Electron app won't start
# ✅ Solution: Check Node.js version (requires 18+)
node --version  # Should be 18.x or higher
npm run dev -- --verbose  # Debug mode

# ❌ Issue: Backend API connection fails
# ✅ Solution: Verify apps/backend is running
curl http://127.0.0.1:8000/health
npm run contract:guard  # Check API compatibility
```

#### **Build Issues**

```bash
# ❌ Issue: TypeScript compilation errors
# ✅ Solution: Update API types
npm run openapi:gen
npm run ts:check

# ❌ Issue: Electron build fails
# ✅ Solution: Clean và rebuild
npm run clean
npm run build
```

### **📊 Performance Monitoring**

```typescript
// Monitor key metrics
const performanceMetrics = {
  'app_startup_time': 'Time from launch to ready',
  'api_response_time': 'Backend API response latency',
  'automation_execution_time': 'Native automation performance',
  'memory_usage': 'Application memory consumption',
  'cpu_usage': 'CPU utilization during operations'
};

// Enable debug logging
localStorage.setItem('debug', 'zeta:*');
```

### **🔍 Debug Mode**

```bash
# Enable debug mode
export DEBUG=zeta:*
npm run dev

# View Electron logs
# Windows: %USERPROFILE%\AppData\Roaming\ZETA AI Desktop\logs
# macOS: ~/Library/Logs/ZETA AI Desktop
# Linux: ~/.config/ZETA AI Desktop/logs
```

---

## 📝 CONCLUSION

**desktop_ai_zeta** được thiết kế như một ứng dụng apps/desktop hiện đại với kiến trúc vững chắc, tích hợp sâu với apps/backend **zeta_vn**, và khả năng mở rộng cao. Kiến trúc Component-Based với Service Layer pattern đảm bảo maintainability và scalability cho các tính năng tương lai.

### **🎯 Key Strengths**

- **Modern Tech Stack**: Electron 31+, React 18+, TypeScript 5.6+, Vite 5.4+
- **Clean Architecture**: Separation of concerns, testable components
- **Native Integration**: Cross-platform automation, screen capture, OCR
- **Real-time Communication**: WebSocket + REST API integration
- **Developer Experience**: Hot reload, type safety, automated testing
- **Production Ready**: CI/CD pipeline, error handling, performance monitoring

### **🚀 Ready for Production**

Ứng dụng đã sẵn sàng cho deployment với full test coverage, automated builds, và comprehensive documentation. Architecture này hỗ trợ việc phát triển các tính năng AI assistant tiên tiến và tích hợp enterprise-grade features trong tương lai.

---

**📄 Document Version**: 1.0.0  
**📅 Last Updated**: 2025-01-08  
**👥 Maintained by**: ZETA Development Team  
**📧 Contact**: <dev@zeta.vn>
