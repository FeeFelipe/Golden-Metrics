#!/usr/bin/env bash
# Roda os cenários dos READMEs de cada lab: sobe o ambiente, valida endpoints e derruba.
# Uso: ./scripts/run-lab-scenarios.sh [--build]
# Se as portas 8080, 9090 ou 3000 estiverem em uso, usa portas alternativas (9080, 9091, 3001).

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Limpar qualquer lab que tenha ficado rodando (evita conflito de portas 4317, 9080, etc.)
for lab in lab1-otel-correlacao lab2-dashboards lab3-alertas lab4-carga; do
  (cd "$REPO_ROOT/$lab" && docker compose down -v 2>/dev/null) || true
done
sleep 2

BUILD_FLAG=""
[[ "${1:-}" == "--build" ]] && BUILD_FLAG="--build"

# Portas padrão
APP_PORT=8080
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
ALERTMANAGER_PORT=9093

# Lab 4 Locust: valores padrão se não definidos
export LOCUST_USERS="${LOCUST_USERS:-80}"
export LOCUST_SPAWN_RATE="${LOCUST_SPAWN_RATE:-10}"
export LOCUST_DURATION="${LOCUST_DURATION:-5m}"

# Se 8080 em uso, usa portas alternativas para não conflitar com outros projetos
if command -v lsof &>/dev/null && lsof -i :8080 &>/dev/null; then
  echo "Porta 8080 em uso; usando portas alternativas: App=9080, Prometheus=9091, Grafana=3010, Alertmanager=9094"
  export APP_PORT=9080
  export PROMETHEUS_PORT=9091
  export GRAFANA_PORT=3010
  export ALERTMANAGER_PORT=9094
  export TARGET_HOST="http://localhost:9080"
fi

wait_for() {
  local url="$1"
  local max="${2:-30}"
  local i=0
  while ! curl -sf --connect-timeout 2 --max-time 8 "$url" &>/dev/null; do
    sleep 2
    i=$((i + 1))
    if [[ $i -ge $max ]]; then
      echo "Timeout aguardando $url"
      return 1
    fi
  done
  return 0
}

run_lab() {
  local lab="$1"
  local lab_path="$REPO_ROOT/$lab"
  echo "========== $lab =========="
  cd "$lab_path"
  docker compose down -v 2>/dev/null || true
  if ! docker compose up -d $BUILD_FLAG 2>&1; then
    echo "Falha ao subir $lab"
    docker compose down -v 2>/dev/null || true
    return 1
  fi
  # Lab 4 sobe Locust junto; dar mais tempo para o app estabilizar sob carga
  if [[ "$lab" == "lab4-carga" ]]; then
    echo "Aguardando serviços (Lab 4: 60s para app + Locust)..."
    sleep 60
  else
    echo "Aguardando serviços (até 45s)..."
    sleep 45
  fi
  local ok=0
  if wait_for "http://localhost:$APP_PORT/health" 15; then
    echo "  OK App /health"
  else
    echo "  (App /health não disponível neste lab)"
  fi
  # /orders pode retornar 200 ou 500 (labs 3/4 simulam erros); latência aleatória
  orders_ok=0
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    code=$(curl -s --connect-timeout 2 --max-time 10 -o /dev/null -w "%{http_code}" "http://localhost:$APP_PORT/orders")
    if [[ "$code" =~ ^(200|500)$ ]]; then orders_ok=1; break; fi
    sleep 2
  done
  if [[ $orders_ok -eq 1 ]]; then
    echo "  OK App /orders (GET)"
  else
    echo "  FALHA App /orders"
    ok=1
  fi
  # POST /orders só existe no Lab 1; nos outros pode ser 404
  if code=$(curl -s -X POST "http://localhost:$APP_PORT/orders" -H "Content-Type: application/json" -d '{}' -o /dev/null -w "%{http_code}" --max-time 8) && [[ "$code" =~ ^(200|500)$ ]]; then
    echo "  OK App /orders (POST)"
  else
    echo "  (POST /orders opcional; Lab 1 expõe, outros podem retornar 404)"
  fi
  if wait_for "http://localhost:$APP_PORT/metrics" 5 2>/dev/null; then
    echo "  OK App /metrics"
  else
    echo "  (metrics pode não existir em todos os labs)"
  fi
  if wait_for "http://localhost:$PROMETHEUS_PORT/-/ready" 10; then
    echo "  OK Prometheus"
  else
    echo "  FALHA Prometheus"
    ok=1
  fi
  if wait_for "http://localhost:$GRAFANA_PORT/api/health" 10; then
    echo "  OK Grafana"
  else
    echo "  FALHA Grafana"
    ok=1
  fi
  docker compose down -v 2>&1
  cd "$REPO_ROOT"
  return $ok
}

# Labs em sequência (um por vez para não disputar portas)
FAIL=0
for lab in lab1-otel-correlacao lab2-dashboards lab3-alertas lab4-carga; do
  if ! run_lab "$lab"; then
    FAIL=1
  fi
  echo ""
done

if [[ $FAIL -eq 0 ]]; then
  echo "Todos os cenários dos labs foram validados."
else
  echo "Alguns cenários falharam. Verifique os logs acima."
  exit 1
fi
