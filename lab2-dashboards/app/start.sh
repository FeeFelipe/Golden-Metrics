#!/usr/bin/env bash
set -euo pipefail
opentelemetry-instrument --traces_exporter none --metrics_exporter otlp           --service_name "${OTEL_SERVICE_NAME:-orders-service}" gunicorn -w 2 -b 0.0.0.0:8080 app:app
