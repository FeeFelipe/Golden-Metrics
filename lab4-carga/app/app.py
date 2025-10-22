import time, random
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}, 200

@app.get("/orders")
def orders():
    latency = random.choice([0.05, 0.2, 0.4, 1.0, 2.0])
    time.sleep(latency)
    status = 200 if random.random() > 0.9 else 500
    payload = {"latency": latency, "status": status}
    return jsonify(payload), status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
