# Python Assistant (Ollama)

Simple interactive assistant that talks to Ollama's chat API.

- Windows-friendly: run `test-live.bat`
- Uses `requests` and `pydantic` (v2)
- Optional `OLLAMA_API_KEY` for remote/protected servers

## Quick start (Windows)

1. Open terminal in this folder
2. Optionally: copy `.env.example` to `.env` and set `OLLAMA_API_KEY`
3. Run the batch script:

```bat
.\u005ctest-live.bat
```

This will create/activate a venv, install requirements, and launch the assistant.

## Environment variables

- `OLLAMA_ENDPOINT` (default `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` (default `gpt-oss:20b`)
- `OLLAMA_API_KEY` (optional for remote/proxy)
- `OLLAMA_TIMEOUT` (default `120`)
- `OLLAMA_MAX_TOKENS` (optional integer)

## Notes

- For local Ollama, no key is required. Pull model first:
  - `ollama pull gpt-oss:20b`
- For remote servers that require auth, set `OLLAMA_API_KEY`.

