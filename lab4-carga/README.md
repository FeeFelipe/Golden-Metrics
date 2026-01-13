### Como validar o Prometheus
1. Acesse http://localhost:9090 no navegador.
2. No menu 'Status' → 'Targets', verifique se o serviço 'app' está listado como 'UP'.
3. No menu 'Status' → 'Rules', confira se as regras de alerta estão carregadas.
4. No menu 'Alerts', veja se os alertas aparecem e mudam de estado conforme a carga.
5. Execute consultas como `up` ou `http_server_requests_total` em 'Graph' para conferir se as métricas estão sendo coletadas.
	 - Se a consulta `http_server_requests_total` não retornar dados:
		 - Gere requisições para o endpoint `/orders` usando Locust ou o comando curl do README.
		 - Verifique se o serviço app está rodando e acessível na porta 8080.
		 - Confira se o Prometheus está coletando do target correto em Status → Targets.
		 - Veja os logs do app e do Prometheus para identificar possíveis erros de scrape ou exportação.
		 - Certifique-se de que o app está expondo métricas no formato esperado pelo Prometheus.
---

## 🛠 Troubleshooting e Validação

### Passos para validar o funcionamento:
1. Todos os serviços devem aparecer como 'Up' em `docker compose ps`.
2. Os logs dos serviços podem ser verificados com `docker compose logs <serviço>`.
3. O app demo deve mostrar mensagens de inicialização do gunicorn e escuta na porta 8080.
4. O Locust deve mostrar ramp-up dos usuários e estatísticas de requisições.
5. O Prometheus deve carregar sem erros e mostrar targets ativos.
6. O Alertmanager deve iniciar e escutar na porta 9093.
7. O Grafana deve iniciar e estar acessível na porta 3000.

### Dicas de solução de problemas:
- Se algum serviço não subir, verifique se há erros nos logs.
- Se o endpoint `/orders` estiver vazio, confira os logs do app e do Locust para garantir que as requisições estão sendo feitas.
- Certifique-se de que o arquivo `.env` está presente e corretamente configurado.
- Execute todos os comandos dentro da pasta `lab4-carga`.
- Para reiniciar o ambiente, use `docker compose down -v` e depois `docker compose up -d --build`.

### Exemplos de comandos úteis:
```bash
docker compose ps
docker compose logs app
docker compose logs locust
docker compose logs prometheus
docker compose logs grafana
```
# ⚠️ Importante
Execute todos os comandos dentro da pasta `lab4-carga` para garantir que o Docker Compose encontre o arquivo correto e todos os serviços sejam inicializados corretamente.



# LAB 4 — Simulação de Carga (Locust em Python)

## Passos rápidos

1. Instale Docker e Docker Compose.
2. Clone o repositório e acesse a pasta do lab:
	```bash
	git clone <url-do-repo>
	cd Golden-Metrics/lab4-carga
	```
3. Ajuste o arquivo `.env` se quiser mudar a carga:
	```ini
	TARGET_HOST=http://localhost:8080
	LOCUST_USERS=80
	LOCUST_SPAWN_RATE=10
	LOCUST_DURATION=5m
	```
4. Suba o ambiente:
	```bash
	docker compose up -d --build
	```
5. (Opcional) Gere mais requisições:
	```bash
	watch -n 0.5 curl -s http://localhost:8080/orders > /dev/null
	```
6. Acesse os serviços:
	- App: http://localhost:8080/health
	- Prometheus: http://localhost:9090
	- Grafana: http://localhost:3000 (admin/admin)
	- Alertmanager: http://localhost:9093
7. Valide:
	- Métricas e alertas no Grafana e Prometheus
	- Serviço demo respondendo em /health e /orders
8. Para encerrar:
	```bash
	docker compose down -v
	```
