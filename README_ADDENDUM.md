# Addendum – Non-invasive Enhancements

This addendum introduces **additive** modules and tooling without changing any existing files.

## What’s included
- `extensions/llm_adapter.py` + adapters for **OpenAI** and **Ollama** (local).
- `tools/state_exporter.py` – Prometheus exporter (sidecar) that listens to Socket.IO state and exposes metrics on `:9108`.
- `tests/` – minimal pytest suite for core engines and governance helpers.
- `scripts/run-tests.sh` – run tests.
- `scripts/start-stack.sh` – start the exporter; run the original app separately.
- `LICENSE_PLACEHOLDER.md` – choose your production license.

## Usage (examples)
```bash
# Local LLM via Ollama
export OLLAMA_BASE_URL=http://localhost:11434
python -c "from extensions.llm_adapter import set_backend, generate; set_backend('ollama', model='mistral'); print(generate('Hello'))"

# OpenAI backend
export OPENAI_API_KEY=sk-...
python -c "from extensions.llm_adapter import set_backend, generate; set_backend('openai', model='gpt-4o-mini'); print(generate('Hello'))"

# Metrics sidecar
export STATE_WS_URL=http://localhost:8080
export EXPORTER_PORT=9108
python tools/state_exporter.py
```

> All changes are **out-of-tree**. To wire the adapter into your app, import from `extensions.llm_adapter` in your own wrapper script or blueprint.
