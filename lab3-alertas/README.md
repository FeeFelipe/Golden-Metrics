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

### 2.1) Testar Prometheus
Para verificar se o Prometheus está coletando métricas corretamente:

- Acesse [http://localhost:9090](http://localhost:9090) no navegador.
- No menu "Graph", digite uma consulta como:
	- `up` (verifica se os targets estão ativos)
	- `http_server_requests_total` (ou outra métrica relevante do app)
- Clique em "Execute" para visualizar os resultados.

Para checar regras e alertas:
- Vá em "Status → Rules" para ver as regras carregadas.
- Vá em "Alerts" para ver o estado dos alertas (*Inactive*, *Pending*, *Firing*).

### 3) Gerar carga
> Execute por alguns minutos para acionar os alertas (as regras usam janelas e `for: 2m`).
```bash
watch -n 0.2 curl -s http://localhost:8080/orders > /dev/null
```


### 4) Verificar alertas
- **Prometheus → Status → Rules**: confira as regras carregadas
- **Prometheus → Alerts**: veja estados *Inactive → Pending → Firing*
- **Alertmanager UI**: veja os grupos e os alertas recebidos

O dashboard do Grafana facilita o entendimento dos cenários ao apresentar visualmente as métricas de erro (%) e latência P99. Com ele, é possível correlacionar rapidamente os gráficos com o disparo dos alertas, tornando mais intuitivo identificar períodos de alta latência ou aumento na taxa de erros, e como esses eventos refletem nos estados dos alertas (Inactive, Pending, Firing) e nos grupos do Alertmanager.

---

## 🔔 Regras de alerta (resumo)
- **HighErrorRate**: Erro % > 2% por 2 min  

Arquivo: `prometheus/rules/golden-metrics.rules.yml`

## 📊 Dashboard Grafana (Golden Metrics)

Para facilitar a visualização dos Golden Metrics, o dashboard é provisionado automaticamente:

- Acesse o Grafana em [http://localhost:3000](http://localhost:3000)
- Menu lateral → Dashboards → Browse
- O dashboard "Golden Metrics Dashboard" estará disponível na pasta "General"
- Visualize gráficos de Taxa de Erro (%) e Latência P99

Se não aparecer, confira se o arquivo `grafana/dashboards/golden-metrics.json` existe e reinicie o container do Grafana.


---

## 🧪 Testes
Para validar as regras de alerta e o Alertmanager:
```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

---

## 🛠 Ajustes úteis
- Para acelerar o disparo, reduza o `for:` para `1m` e a janela do `rate()` para `1m`.
- Para enviar para Slack/E-mail, edite `alertmanager/alertmanager.yml` adicionando um `receiver` real.

---

## 🧩 Encerramento
```bash
docker compose down -v
```
