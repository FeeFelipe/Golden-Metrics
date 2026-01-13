import time, random
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

REQ_COUNTER = Counter("http_server_requests_total", "Requests total", ["endpoint", "method", "http_status"])
REQ_LATENCY = Histogram("http_server_request_duration_seconds", "Request latency",
                        buckets=(0.05, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 5))

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return generate_latest(REGISTRY), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/orders")
def orders():
    latency = random.choice([0.05, 0.2, 0.4, 1.0, 2.0])
    time.sleep(latency)
    status = "200" if random.random() > 0.9 else "500"  # ~10% erro para facilitar alertas
    REQ_COUNTER.labels("/orders", "GET", status).inc()
    REQ_LATENCY.observe(latency)
    payload = {"latency": latency, "status": status}
    return jsonify(payload), int(status)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
