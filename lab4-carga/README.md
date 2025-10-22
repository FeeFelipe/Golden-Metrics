# LAB 4 — Simulação de Carga (Locust em Python)

Este laboratório gera **carga sintética** para observar, em tempo real, o efeito nas **Golden Metrics** (RPS, Erro %, P95/P99, Saturação) e validar **alertas** configurados nos labs anteriores.

Você pode:
1) Apontar para **um serviço externo** (por padrão `http://localhost:8080`), ou
2) Rodar um **serviço demo** incluso neste lab (perfil `demo`).

---

## 🎯 Objetivo
Simular tráfego realista e provocar variações de latência/erros para observar dashboards e disparo de alertas.

---

## 🧰 Tecnologias
- Locust (Python)
- (Opcional) Flask app demo

---

## ⚙️ Configuração via `.env`
```ini
TARGET_HOST=http://localhost:8080   # Host alvo (altere se necessário)
LOCUST_USERS=80                     # Número de usuários virtuais
LOCUST_SPAWN_RATE=10                # Usuários por segundo
LOCUST_DURATION=5m                  # Duração total do teste
```

---

## 🚀 Modo A — Apontando para um serviço já em execução
(ex.: app dos Labs 1–3 rodando em :8080)

1) Ajuste o `TARGET_HOST` no `.env` se necessário.
2) Execute:
```bash
docker compose up -d
```
3) Acompanhe seus dashboards/alertas nos ambientes dos labs anteriores.
4) Para encerrar:
```bash
docker compose down -v
```

---

## 🧪 Modo B — Subindo o serviço demo incluso (perfil `demo`)
1) Suba o app demo + locust:
```bash
docker compose --profile demo up -d --build
```
2) (Opcional) Gere tráfego adicional manual:
```bash
watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
```
3) Encerre:
```bash
docker compose --profile demo down -v
```

---

## 📌 Dicas para provocar alertas
- Aumente `LOCUST_USERS` e `LOCUST_DURATION` no `.env`.
- Combine este lab com o **Lab 3 (Alertas)** para observar estados *Pending → Firing*.
- Ajuste as regras para janelas e `for:` menores durante a demonstração.

---

## 🧩 Observabilidade (com Labs 1–3)
- **Dashboards (Lab 2):** RPS, Erro %, P95/P99 variando ao vivo.
- **Alertas (Lab 3):** HighErrorRate / HighLatency em estado firing após o limiar.
- **Correlação (Lab 1):** Traces e logs contextualizando a causa dos picos.

---

## 🧹 Limpeza
```bash
docker compose down -v
```
