# -*- coding: utf-8 -*-
"""
Lab 4: SIMULAÇÃO DE CARGA

Cenários garantidos:
- Curvas de latência subindo sob carga
- Crescimento de erros ou saturação
- Disparo do alerta (regras compatíveis com Golden Metrics)
- Locust configurado para gerar tráfego contra /orders
"""
import os
import yaml
import pytest

# Raiz do lab (pasta lab4-carga)
LAB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestLoadSimulation:
    """Valida configuração da simulação de carga."""

    def test_locustfile_existe_e_tem_task_orders(self):
        """Locust deve ter task que chama /orders."""
        path = os.path.join(LAB_ROOT, "load", "locustfile.py")
        assert os.path.isfile(path), "locustfile.py deve existir em load/"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "/orders" in content
        assert "task" in content or "@task" in content
        assert "HttpUser" in content or "Locust" in content

    def test_docker_compose_tem_locust_e_app(self):
        """docker-compose deve ter serviço locust e app."""
        config = _read_yaml(os.path.join(LAB_ROOT, "docker-compose.yml"))
        services = list(config.get("services", {}).keys())
        assert "locust" in services
        assert "app" in services
        assert "prometheus" in services
        assert "alertmanager" in services

    def test_app_gera_latencia_e_erros_para_disparar_alertas(self):
        """App deve ter variabilidade de latência e % de erros (ex.: 10%)."""
        path = os.path.join(LAB_ROOT, "app", "app.py")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "latency" in content or "sleep" in content or "random" in content
        assert "500" in content or "5.." in content
        assert "http_server_requests_total" in content
        assert "http_server_request_duration_seconds" in content


class TestAlertRules:
    """Regras de alerta devem permitir disparo sob carga."""

    @pytest.fixture
    def rules(self):
        path = os.path.join(LAB_ROOT, "prometheus", "rules", "golden-metrics.rules.yml")
        assert os.path.isfile(path)
        return _read_yaml(path)

    def test_tem_alerta_high_error_rate(self, rules):
        """Deve ter alerta HighErrorRate (ex.: > 2%)."""
        alerts = []
        for g in rules.get("groups", []):
            for r in g.get("rules", []):
                if r.get("alert"):
                    alerts.append(r["alert"])
        assert "HighErrorRate" in alerts or any("error" in a.lower() for a in alerts)

    def test_tem_alerta_latencia_ou_saturacao(self, rules):
        """Deve ter alerta de latência (P99) ou saturação."""
        alerts = []
        for g in rules.get("groups", []):
            for r in g.get("rules", []):
                if r.get("alert"):
                    alerts.append(r["alert"])
        has_latency = any("latency" in a.lower() or "Latency" in a or "P99" in a for a in alerts)
        assert has_latency, "Lab 4 deve ter alerta de latência para cenário de carga."
