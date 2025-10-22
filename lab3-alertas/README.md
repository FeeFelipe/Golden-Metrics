# LAB 3 — Configuração de Alertas (SLO-driven)

Este laboratório mostra como **configurar e validar alertas** baseados em **Golden Metrics** (Erro % e Latência P99) usando **Prometheus + Alertmanager**.
O serviço Python simula latências variáveis e ~10% de erros para facilitar o disparo.

---

## 🎯 Objetivo
- Criar regras de alerta (Prometheus) alinhadas a SLIs/SLOs.
- Visualizar estado dos alertas no Prometheus e no Alertmanager.
- Entender *for*, severidade e agregação.

---

## 🧰 Tecnologias
- Python + Flask (serviço simulado)
- OpenTelemetry Collector (exporta métricas para Prometheus)
- Prometheus (regras e avaliação)
- Alertmanager (gestão e entrega de alertas)
- Grafana (consulta e visualização — opcional neste lab)

---

## 🚀 Como executar

### 1) Subir o ambiente
```bash
docker compose up -d --build
```

### 2) Acessar as UIs
- App (testar): http://localhost:8080/orders
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- Grafana: http://localhost:3000  (admin / admin)

### 3) Gerar carga
> Execute por alguns minutos para acionar os alertas (as regras usam janelas e `for: 2m`).
```bash
watch -n 0.2 curl -s http://localhost:8080/orders > /dev/null
```

### 4) Verificar alertas
- **Prometheus → Status → Rules**: confira as regras carregadas
- **Prometheus → Alerts**: veja estados *Inactive → Pending → Firing*
- **Alertmanager UI**: veja os grupos e os alertas recebidos

---

## 🔔 Regras de alerta (resumo)
- **HighErrorRate**: Erro % > 2% por 2 min  
- **HighLatencyP99**: P99 > 1.5s por 2 min  

Arquivo: `prometheus/rules/golden-metrics.rules.yml`

---

## 🛠 Ajustes úteis
- Para acelerar o disparo, reduza o `for:` para `1m` e a janela do `rate()` para `1m`.
- Para enviar para Slack/E-mail, edite `alertmanager/alertmanager.yml` adicionando um `receiver` real.

---

## 🧩 Encerramento
```bash
docker compose down -v
```
