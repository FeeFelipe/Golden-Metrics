#!/usr/bin/env bash
set -euo pipefail
export OTEL_METRIC_EXPORT_INTERVAL=1000
opentelemetry-instrument --traces_exporter otlp --metrics_exporter otlp --logs_exporter otlp           --service_name "${OTEL_SERVICE_NAME:-orders-service}" gunicorn -w 2 -b 0.0.0.0:8080 app:app
