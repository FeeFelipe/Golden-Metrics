# Testes do Lab 1 — Correlação OpenTelemetry

Execute a partir da **raiz do lab** (`lab1-otel-correlacao`):

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

Testes E2E (com `docker compose up` rodando):

```bash
pytest tests/ -m e2e -v
```
