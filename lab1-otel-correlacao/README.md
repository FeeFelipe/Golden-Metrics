# LAB 1 — Correlação na prática com OpenTelemetry

Este laboratório demonstra como correlacionar **métricas, logs e traces** usando **OpenTelemetry**, **Prometheus**, **Loki**, **Tempo** e **Grafana**.

---

## 🎯 Objetivo
Instrumentar um microserviço Python com OpenTelemetry e observar métricas, logs e traces correlacionados em tempo real.

---

## 🧰 Tecnologias utilizadas
- Python 3.12 + Flask
- OpenTelemetry SDK e auto-instrumentação
- Prometheus (métricas)
- Loki (logs)
- Tempo (traces)
- Grafana (visualização)

---

## 🚀 Execução

### 1. Subir o ambiente
```bash
docker compose up -d --build
```

### 2. Acessar os serviços
- App: http://localhost:8080/orders  
- Prometheus: http://localhost:9090  
- Grafana: http://localhost:3000 (login: admin / admin)  
- Loki API: http://localhost:3100  
- Tempo: http://localhost:3200  

### 3. Gerar tráfego
```bash
watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
```

### 4. Explorar os dados no Grafana
- **Métricas (Prometheus):** painel `rate(http_server_requests_total[1m])`
- **Logs (Loki):** `container="app"`
- **Traces (Tempo):** Explore > Tempo > `service.name="orders-service"`

---

## ✅ Resultado esperado
- Cada requisição gera:
  - uma métrica (`http_server_request_duration_seconds`)
  - um log estruturado no Loki
  - um trace completo no Tempo
- Todos correlacionados pelo atributo `service.name = orders-service`

---

## 🧠 Conceitos-chave
- **Metrics:** comportamento quantitativo (latência, taxa de erro, tráfego)
- **Logs:** contexto detalhado (mensagens e exceções)
- **Traces:** jornada ponta a ponta da requisição

---

## 🧩 Encerramento
Pare o ambiente após o teste:
```bash
docker compose down -v
```
