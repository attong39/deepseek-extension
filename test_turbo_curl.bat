@echo off
echo 🧪 Testing Turbo API with curl...
echo.

curl -X POST "https://api.turbo.ai/v1/chat/completions" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP" ^
  -d "{\"model\": \"turbo\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello, can you respond in Vietnamese?\"}], \"max_tokens\": 100}"

echo.
echo Test complete.
pause
