# LAB 1 — Correlação na prática com OpenTelemetry

Este laboratório demonstra como correlacionar **métricas e traces** usando **OpenTelemetry**, **Prometheus**, **Tempo** e **Grafana**.

---

## 🎯 Objetivo
Instrumentar um microserviço **Node.js** (orders-service) com OpenTelemetry e observar métricas e traces correlacionados em tempo real.

---

## 🧰 Tecnologias utilizadas
- Node.js + Express
- OpenTelemetry SDK e auto-instrumentação
- Prometheus (métricas)
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
- Tempo: http://localhost:3200  

### 3. Gerar tráfego
```bash
watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
```

### 4. Explorar os dados no Grafana
- **Métricas (Prometheus):** painel `rate(http_server_requests_total[1m])`
- **Traces (Tempo):** Explore > Tempo > `service.name="orders-service"`

---

## ✅ Resultado esperado
- Cada requisição gera:
  - uma métrica (`http_server_request_duration_seconds`)
  - um trace completo no Tempo
- Todos correlacionados pelo atributo `service.name = orders-service`

---

## 🧠 Conceitos-chave
- **Metrics:** comportamento quantitativo (latência, taxa de erro, tráfego)
- **Traces:** jornada ponta a ponta da requisição
---

## ⚠️ Observações importantes
- O suporte a logs via Loki pelo OpenTelemetry Collector oficial foi removido deste lab.
- Certifique-se de que o arquivo `tempo.yaml` está presente na raiz do lab para o serviço Tempo funcionar corretamente.
- Este projeto utiliza apenas Node.js, não há dependências Python.

---

## 🧩 Encerramento
Pare o ambiente após o teste:
```bash
docker compose down -v
```
