import os, random, time
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

REQ_COUNTER = Counter("http_server_requests_total", "Requests total", ["endpoint", "method", "http_status"])
REQ_LATENCY = Histogram("http_server_request_duration_seconds", "Request latency",
                        buckets=(0.05, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 5))

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return generate_latest(REGISTRY), 200, {"Content-Type": CONTENT_TYPE_LATEST}

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/orders")
def orders():
    start = time.time()
    latency = random.choice([0.05, 0.1, 0.2, 0.4, 0.8, 1.2, 2.0])
    time.sleep(latency)
    if random.random() < 0.08:
        REQ_COUNTER.labels(endpoint="/orders", method="GET", http_status="500").inc()
        with REQ_LATENCY.time():
            pass
        return jsonify({"error": "payment timeout"}), 500
    else:
        REQ_COUNTER.labels(endpoint="/orders", method="GET", http_status="200").inc()
        with REQ_LATENCY.time():
            pass
        return jsonify({"items": [{"id": 1, "amount": 42.0}], "latency": latency}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
