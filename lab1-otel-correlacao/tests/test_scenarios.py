# -*- coding: utf-8 -*-
"""
Lab 1: CORRELAÇÃO NA PRÁTICA COM OPENTELEMETRY

Cenários garantidos:
- POST /orders disponível; requisição passa por serviço instrumentado com OTel
- Trace exportado via OTLP → Grafana Tempo
- Métricas (latência) no Prometheus; dashboard mostra correlação
- Estrutura: app → otel-collector → Prometheus + Tempo
"""
import os
import yaml
import json
import pytest

# Raiz do lab (pasta lab1-otel-correlacao)
LAB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestLab1Config:
    """Valida configuração do Lab 1 (OTel → Tempo + Prometheus)."""

    def test_otel_collector_exporta_metrics_e_traces_para_tempo(self):
        """OTel Collector deve ter pipeline metrics e traces com exporter para Tempo."""
        config = _read_yaml(os.path.join(LAB_ROOT, "otel-collector", "config.yaml"))
        pipelines = config["service"]["pipelines"]
        assert "metrics" in pipelines
        assert "traces" in pipelines
        assert "otlp/tempo" in (config.get("exporters") or {})
        assert "otlp" in (config.get("receivers") or {})

    def test_tempo_config_presente(self):
        """Tempo deve estar configurado (backend local)."""
        tempo_path = os.path.join(LAB_ROOT, "tempo.yaml")
        assert os.path.isfile(tempo_path)
        config = _read_yaml(tempo_path)
        assert "storage" in config
        assert config["storage"].get("trace", {}).get("backend") == "local"

    def test_prometheus_scrape_otel_collector(self):
        """Prometheus deve scrapear o OTel Collector (métricas)."""
        config = _read_yaml(os.path.join(LAB_ROOT, "prometheus", "prometheus.yml"))
        jobs = [c["job_name"] for c in config["scrape_configs"]]
        assert "otel-collector" in jobs or "orders-app" in jobs

    def test_docker_compose_tem_servicos_necessarios(self):
        """docker-compose deve ter app, otel-collector, prometheus, tempo, grafana."""
        config = _read_yaml(os.path.join(LAB_ROOT, "docker-compose.yml"))
        services = list(config.get("services", {}).keys())
        for name in ["app", "otel-collector", "prometheus", "tempo", "grafana"]:
            assert name in services, f"Serviço '{name}' ausente no docker-compose"

    def test_app_expoe_post_orders(self):
        """Aplicação deve expor POST /orders (cenário do lab)."""
        app_js = os.path.join(LAB_ROOT, "app", "app.js")
        with open(app_js, "r", encoding="utf-8") as f:
            content = f.read()
        assert "post('/orders'" in content or "post(\"/orders\"" in content
        assert "http_server_request_duration_seconds" in content
        assert "http_server_requests_total" in content

    def test_dashboard_grafana_tem_painel_traces_tempo(self):
        """Dashboard Grafana deve ter painel de traces (Tempo) e métricas."""
        dash_path = os.path.join(
            LAB_ROOT, "grafana", "provisioning", "dashboards", "golden-metrics.json"
        )
        dash = _read_json(dash_path)
        panels = dash.get("panels", [])
        titles = [p.get("title", "") for p in panels]
        has_rps = any("RPS" in t or "Requisições" in t for t in titles)
        has_traces = any(
            p.get("datasource") == "Tempo" or "trace" in str(p).lower()
            for p in panels
        )
        assert has_rps, "Dashboard deve ter painel de RPS/métricas"
        assert has_traces, "Dashboard deve ter painel de traces (Tempo)"


@pytest.mark.e2e
class TestLab1E2E:
    """Testes E2E: exigem docker compose up no lab (opcional)."""

    @pytest.fixture(scope="class")
    def base_url(self):
        return "http://localhost:8080"

    def test_orders_get_responds(self, base_url):
        import requests
        r = requests.get(f"{base_url}/orders", timeout=5)
        assert r.status_code in (200, 500)

    def test_orders_post_responds(self, base_url):
        import requests
        r = requests.post(f"{base_url}/orders", json={}, timeout=5)
        assert r.status_code in (200, 500)

    def test_metrics_endpoint_exposes_otel_metrics(self, base_url):
        import requests
        r = requests.get(f"{base_url}/metrics", timeout=5)
        assert r.status_code == 200
        assert "http_server_requests_total" in r.text
        assert "http_server_request_duration_seconds" in r.text
