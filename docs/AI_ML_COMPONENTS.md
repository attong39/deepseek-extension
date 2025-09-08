# AI/ML Components (recommendations)

Tổng quan đề xuất cho các thành phần AI/ML (server + apps/desktop/edge).

1) OCR
- Ưu tiên: PaddleOCR (tốt cho tiếng Việt).
- Fallback: EasyOCR hoặc Tesseract khi không cần độ chính xác cao.
- Pattern: run local on apps/desktop client by default; server-side batch OCR via PaddleOCR GPU when available.

2) STT (Speech-to-Text)
- Giải pháp: Whisper family (faster-whisper for local CPU/GPU) cho chính xác ngoài luồng.
- Lightweight: Web Speech API (browser) hoặc use hosted Whisper API for server-side.
- Design: abstract STT provider interface so app can switch providers via config.

3) Edge / Desktop ML
- Desktop: tích hợp desktopCapturer + local OCR/STT.
- Controller/automation: nut.js / RobotJS / PyAutoGUI / pynput (client-side) cho điều khiển UI.
- Safety: panic/stop button, user confirmation for risky steps.

4) Model orchestration & fallback
- Create provider abstraction (AIService) to fallback chain: local -> hosted -> alternative model.
- Monitor: health checks + circuit-breaker for model endpoints.

5) Data & privacy
- All media with PII: encrypt before upload (envelope encryption), store metadata only on server.
- Event schema: standardize action/result/event for audit and downstream fine-tune.

6) Observability
- Collect latency, error rate, token costs per provider, and sample LLM responses (PII-scrubbed) for QA.

7) Quick infra note
- Server-side heavy jobs (OCR/ASR) run on separate GPU workers (Celery) and not in request thread.

---

File created for reference and to drive infra changes (Compose, workers, GPU nodes) later.
