# LAB 2 — Dashboards de Observabilidade (Golden Metrics)

Este laboratório demonstra como construir um **dashboard de observabilidade** baseado nas *Four Golden Metrics* usando **Prometheus**, **OpenTelemetry** e **Grafana**.

---

## 🎯 Objetivo
Consolidar métricas de latência, tráfego, taxa de erro e saturação em dashboards práticos.

---

## 🧰 Tecnologias utilizadas
- Python + Flask (serviço simulado)
- OpenTelemetry Collector (coleta de métricas)
- Prometheus (armazenamento de métricas)
- Grafana (visualização e dashboards)

---

## 🚀 Execução

### 1. Subir o ambiente
```bash
docker compose up -d --build
```

### 2. Acessar os serviços
- App: http://localhost:8080/orders  
- Prometheus: http://localhost:9090  
- Grafana: http://localhost:3000 (admin / admin)

### 3. Gerar tráfego
```bash
watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
```

### 4. Visualizar no Grafana
- Dashboard **Golden Metrics Dashboard** será carregado automaticamente.
- Principais painéis:
  - **Requests per Second (RPS)** — tráfego
  - **Error Rate (%)** — taxa de erro
  - **Latency P99 (s)** — desempenho

---

## ✅ Resultado esperado
O aluno visualiza as *Four Golden Metrics* atualizando em tempo real e entende como estruturar dashboards de observabilidade eficientes.

---

## 🧩 Encerramento
```bash
docker compose down -v
```
