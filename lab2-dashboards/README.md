# LAB 2 — Dashboards de Observabilidade (Golden Metrics)

Este laboratório demonstra como construir um **dashboard de observabilidade** baseado nas *Four Golden Metrics* usando **Prometheus** e **Grafana**.

---

## 🎯 Objetivo
Consolidar métricas de latência, tráfego, taxa de erro e saturação em dashboards práticos.

---

## 🧰 Tecnologias utilizadas
- Python + Flask (serviço simulado)
- Prometheus (scrape e armazenamento de métricas)
- Grafana (visualização e dashboards)

---

## 🚀 Execução

### 1. Subir o ambiente
```bash
docker compose up -d --build
```

### 2. Acessar os serviços
- **App:** http://localhost:8080/orders  
- **Prometheus:** http://localhost:9090  
- **Grafana:** http://localhost:3000 (login: **admin** / **admin**)

### 3. Validar Prometheus
Para confirmar que o Prometheus está coletando métricas da aplicação:
- Acesse http://localhost:9090
- No campo "Expression", digite: `http_server_requests_total` e clique em "Execute".
- As métricas devem aparecer após algum tráfego na app.

### 4. Gerar tráfego
```bash
watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
```

### 5. Visualizar no Grafana
- O dashboard **Golden Metrics Dashboard** é provisionado automaticamente.
- Principais painéis:
  - **Requests per Second (RPS)** — tráfego
  - **Error Rate (%)** — taxa de erro
  - **Latency P99 (s)** — latência (desempenho)

---

## ✅ Resultado esperado
O aluno visualiza as *Four Golden Metrics* atualizando em tempo real e entende como estruturar dashboards de observabilidade eficientes.

---

## 🧠 Conceitos-chave
- **Latency:** tempo de resposta (ex.: P99)
- **Traffic:** requisições por segundo (RPS)
- **Errors:** taxa de erros (ex.: 5xx)
- **Saturation:** uso de recursos (neste lab, indiretamente via latência/erros)

---

## 🧪 Testes
Para validar a estrutura do dashboard (Golden Metrics), execute a partir da **raiz do lab** (`lab2-dashboards`):
```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```
Ver `tests/README.md` para detalhes.

---

## 🧩 Encerramento
Pare o ambiente após o teste:
```bash
docker compose down -v
```
