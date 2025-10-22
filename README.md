# 🧭 Observabilidade na Prática — Golden Metrics & OpenTelemetry

Este projeto reúne **4 laboratórios práticos** que demonstram, passo a passo, como aplicar observabilidade moderna em sistemas distribuídos com base nas *Four Golden Metrics*:  
**Latência, Tráfego, Taxa de Erro e Saturação.**

Cada lab é independente e pode ser executado separadamente, mas juntos formam uma **linha evolutiva completa** — da instrumentação até o disparo de alertas e análise sob carga.

---

## 🧩 Estrutura dos Laboratórios

```
observabilidade-labs/
├─ lab1-otel-correlacao/      → Correlação com OpenTelemetry (Metrics + Logs + Traces)
├─ lab2-dashboards/           → Dashboards de Observabilidade (Golden Metrics)
├─ lab3-alertas/              → Configuração de Alertas (SLO-driven)
└─ lab4-carga/                → Simulação de Carga (Locust)
```

---

## 🎯 Objetivos Gerais

1. **Instrumentar aplicações** com OpenTelemetry para coletar métricas, logs e traces.  
2. **Visualizar Golden Metrics** em dashboards no Grafana.  
3. **Configurar alertas** alinhados a SLIs e SLOs.  
4. **Simular carga** para validar observabilidade e resposta a incidentes.  

---

## ⚙️ Pré-requisitos

- Docker + Docker Compose  
- (Opcional) Python 3.10+ para executar Locust localmente  
- 4 GB de memória livre recomendada  

---

## 🚀 Ordem sugerida de execução

### 🔹 **LAB 1 — Correlação na prática com OpenTelemetry**
- Suba o ambiente com `docker compose up -d`.  
- Gere tráfego e explore no Grafana:  
  - Métricas (Prometheus)  
  - Logs (Loki)  
  - Traces (Tempo)  
- **Objetivo:** entender a correlação entre *Metrics, Logs e Traces (MLT)*.

📂 Pasta: `lab1-otel-correlacao/`  
📘 [README do Lab 1](lab1-otel-correlacao/README.md)

---

### 🔹 **LAB 2 — Dashboards de Observabilidade (Golden Metrics)**
- Construa um dashboard com **RPS, Erro %, Latência P99 e Saturação**.  
- Use queries PromQL e dashboards provisionados.  
- **Objetivo:** transformar dados em insights visuais.

📂 Pasta: `lab2-dashboards/`  
📘 [README do Lab 2](lab2-dashboards/README.md)

---

### 🔹 **LAB 3 — Configuração de Alertas (SLO-driven)**
- Crie alertas no Prometheus/Alertmanager baseados em SLOs.  
- Valide as regras e monitore o estado *Pending → Firing*.  
- **Objetivo:** tornar observabilidade **acionável**.

📂 Pasta: `lab3-alertas/`  
📘 [README do Lab 3](lab3-alertas/README.md)

---

### 🔹 **LAB 4 — Simulação de Carga (Locust)**
- Gere tráfego sintético com Locust.  
- Observe dashboards e alertas reagindo em tempo real.  
- **Objetivo:** validar SLIs/SLOs e demonstrar resiliência operacional.

📂 Pasta: `lab4-carga/`  
📘 [README do Lab 4](lab4-carga/README.md)

---

## 🧠 Conceitos Conectados

| Conceito | Aplicado em | Descrição |
|-----------|--------------|-----------|
| **Metrics** | Labs 1–3 | Dados quantitativos (latência, erro, tráfego) |
| **Logs** | Lab 1 | Contexto detalhado de eventos e exceções |
| **Traces** | Lab 1 | Jornada ponta a ponta da requisição |
| **Dashboards** | Lab 2 | Visualização e análise de comportamento |
| **Alertas SLO-driven** | Lab 3 | Ações baseadas em impacto real no usuário |
| **Carga sintética** | Lab 4 | Validação de métricas e alertas sob estresse |

---

## 📈 Stack Tecnológica Comum

| Categoria | Ferramenta |
|------------|-------------|
| Instrumentação | **OpenTelemetry SDK / Collector** |
| Métricas | **Prometheus** |
| Logs | **Loki** |
| Traces | **Tempo** |
| Visualização | **Grafana** |
| Alertas | **Prometheus Alertmanager** |
| Carga | **Locust (Python)** |

---

## 🔄 Relação entre os Labs

```
[L1] OpenTelemetry → Prometheus/Loki/Tempo → Grafana
[L2] Prometheus → Dashboards Golden Metrics
[L3] Prometheus + Alertmanager → Alertas SLO-driven
[L4] Locust → Gera carga → Alimenta métricas e dispara alertas
```

---

## 🧹 Limpeza geral
Após cada demonstração:
```bash
docker compose down -v
```

Para remover todos os labs:
```bash
docker system prune -a --volumes
```

---

## 🏁 Resultado Final
Ao concluir os 4 laboratórios, você será capaz de:

✅ Instrumentar aplicações com OpenTelemetry  
✅ Montar dashboards baseados em Golden Metrics  
✅ Criar alertas acionáveis baseados em SLOs  
✅ Simular e diagnosticar incidentes em tempo real  
✅ Correlacionar métricas, logs e traces como um verdadeiro engenheiro SRE

---

## 📚 Referências
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)  
- [Grafana Observability Stack](https://grafana.com/oss/)  
- [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)  
- [Google SRE Book – Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

---

> 💡 **Dica:** execute um lab por vez para evitar conflitos de portas (8080, 9090, 3000).  
> Em apresentações, use **Lab 4** para gerar carga sobre os ambientes dos **Labs 1–3** e demonstrar a observabilidade em tempo real.
