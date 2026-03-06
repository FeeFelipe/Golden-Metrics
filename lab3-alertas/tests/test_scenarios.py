# -*- coding: utf-8 -*-
"""
Lab 3: CONFIGURAÇÃO DE ALERTAS

Cenários garantidos:
- Alerta ≠ notificação: alerta acionável (ação necessária)
- Alertas baseados em SLO/SLA/Error Budget (não só métricas brutas)
- Exemplo: Erro ≥ 2% por N min → severidade (ex.: média/critical)
- Regras Prometheus + Alertmanager configurados
"""
import os
import yaml
import pytest

# Raiz do lab (pasta lab3-alertas)
LAB_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestAlertRules:
    """Valida regras de alerta SLO-driven."""

    @pytest.fixture
    def rules(self):
        path = os.path.join(LAB_ROOT, "prometheus", "rules", "golden-metrics.rules.yml")
        assert os.path.isfile(path), f"Arquivo de regras não encontrado: {path}"
        return _read_yaml(path)

    @pytest.fixture
    def alert_rules(self, rules):
        out = []
        for g in rules.get("groups", []):
            for r in g.get("rules", []):
                if "alert" in r:
                    out.append(r)
        return out

    def test_existe_alerta_baseado_em_taxa_de_erro(self, alert_rules):
        """Deve existir alerta de taxa de erro (ex.: Erro > 2%)."""
        error_alerts = [
            r for r in alert_rules
            if "error" in r.get("alert", "").lower()
            or "Error" in r.get("annotations", {}).get("summary", "")
            or "erro" in r.get("annotations", {}).get("summary", "").lower()
        ]
        assert len(error_alerts) >= 1, (
            "Deve existir pelo menos um alerta baseado em taxa de erro (ex.: HighErrorRate)."
        )

    def test_alerta_erro_usar_limiar_percentual_e_janela(self, rules):
        """Alerta de erro deve usar limiar (ex.: 2%) e janela (for: Xm)."""
        for g in rules.get("groups", []):
            for r in g.get("rules", []):
                alert_name = r.get("alert", "")
                if "error" in alert_name.lower() or "ErrorRate" in alert_name:
                    expr = r.get("expr", "")
                    for_duration = str(r.get("for", ""))
                    assert "0.02" in expr or "job:http_error_rate" in expr or "rate(" in expr, (
                        "Alerta de erro deve usar limiar 2% (0.02) ou recording rule."
                    )
                    assert "m" in for_duration or "s" in for_duration, (
                        "Alerta deve ter 'for' (janela de tempo) para evitar flapping."
                    )
                    return
        pytest.fail("Nenhum alerta de erro encontrado para validar limiar/for.")

    def test_existe_recording_rule_ou_expr_com_rate_erro(self, rules):
        """Deve haver recording rule ou expr com taxa de erro (rate 5xx / total)."""
        all_exprs = []
        for g in rules.get("groups", []):
            for r in g.get("rules", []):
                all_exprs.append(r.get("expr", ""))
                if r.get("record"):
                    all_exprs.append(r.get("expr", ""))
        full = " ".join(all_exprs)
        assert "5.." in full or "5xx" in full or "http_status" in full
        assert "rate(" in full

    def test_severidade_rotulada_em_alertas(self, alert_rules):
        """Alertas devem ter label de severidade (severity)."""
        for r in alert_rules:
            labels = r.get("labels", {})
            assert "severity" in labels, (
                f"Alerta '{r.get('alert')}' deve ter label 'severity'."
            )


class TestAlertmanager:
    """Valida configuração do Alertmanager."""

    def test_alertmanager_config_existe(self):
        path = os.path.join(LAB_ROOT, "alertmanager", "alertmanager.yml")
        assert os.path.isfile(path)

    def test_alertmanager_config_valida(self):
        path = os.path.join(LAB_ROOT, "alertmanager", "alertmanager.yml")
        config = _read_yaml(path)
        assert "global" in config or "route" in config or "receivers" in config
