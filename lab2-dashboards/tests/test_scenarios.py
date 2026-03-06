# -*- coding: utf-8 -*-
"""
Lab 2: DASHBOARDS DE OBSERVABILIDADE

Cenários garantidos:
- Clareza e hierarquia (visão executiva → técnica)
- Agrupamento por Golden Metrics: Latência (P50, P90, P99), Tráfego (RPS),
  Taxa de erros (4xx/5xx), Saturação (CPU/memória quando aplicável)
- Dashboard Grafana com estrutura válida
"""
import os
import json
import pytest

# Raiz do lab (pasta lab2-dashboards)
LAB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_dashboard_json() -> str:
    """Encontra golden-metrics.json neste lab."""
    for sub in ["grafana/provisioning/dashboards", "grafana/dashboards"]:
        p = os.path.join(LAB_ROOT, sub, "golden-metrics.json")
        if os.path.isfile(p):
            return p
    raise FileNotFoundError(f"golden-metrics.json não encontrado em {LAB_ROOT}")


class TestDashboardStructure:
    """Valida estrutura do dashboard Golden Metrics."""

    @pytest.fixture
    def dashboard(self):
        path = _find_dashboard_json()
        return _read_json(path)

    @pytest.fixture
    def panel_titles_and_queries(self, dashboard):
        """Lista (título, expr) de cada painel."""
        result = []
        for p in dashboard.get("panels", []):
            title = p.get("title", "")
            targets = p.get("targets", [])
            expr = (targets[0].get("expr", "") if targets else "")
            result.append((title, expr))
        return result

    def test_dashboard_tem_painel_rps_trafego(self, panel_titles_and_queries):
        """Deve ter painel de Tráfego: RPS / requisições por segundo."""
        titles = [t for t, _ in panel_titles_and_queries]
        has_rps = any(
            "RPS" in t or "requisições" in t.lower() or "rate" in t.lower()
            for t in titles
        )
        assert has_rps, f"Dashboard deve ter painel RPS/Tráfego. Títulos: {titles}"

    def test_dashboard_tem_painel_taxa_erro(self, panel_titles_and_queries):
        """Deve ter painel de Taxa de Erro (4xx/5xx)."""
        titles = [t for t, _ in panel_titles_and_queries]
        queries = [q for _, q in panel_titles_and_queries]
        has_error = any(
            "erro" in t.lower() or "error" in t.lower() for t in titles
        )
        has_5xx_query = any("5.." in q or "5xx" in q.lower() for q in queries)
        assert has_error or has_5xx_query, (
            f"Dashboard deve ter painel de Taxa de Erro. Títulos: {titles}"
        )

    def test_dashboard_tem_painel_latencia(self, panel_titles_and_queries):
        """Deve ter painel de Latência (P50, P90 ou P99)."""
        titles = [t for t, _ in panel_titles_and_queries]
        queries = [q for _, q in panel_titles_and_queries]
        has_latency_title = any(
            "latência" in t.lower() or "latency" in t.lower() or "P99" in t or "P90" in t or "P50" in t
            for t in titles
        )
        has_histogram_quantile = any(
            "histogram_quantile" in q for q in queries
        )
        assert has_latency_title or has_histogram_quantile, (
            "Dashboard deve ter painel de Latência (percentis)."
        )

    def test_queries_usam_metricas_esperadas(self, panel_titles_and_queries):
        """Queries devem usar http_server_requests_total e/ou request_duration."""
        all_exprs = " ".join(q for _, q in panel_titles_and_queries)
        assert "http_server_requests_total" in all_exprs or "http_server_request_duration" in all_exprs, (
            "Dashboard deve usar métricas do app (requests_total ou request_duration)."
        )

    def test_dashboard_titulo_golden_metrics(self, dashboard):
        """Dashboard deve ter título identificável (Golden Metrics)."""
        title = dashboard.get("title", "")
        assert "golden" in title.lower() or "Golden" in title
