const express = require('express');
const promClient = require('prom-client');
const { randomInt, randomFloat } = require('./utils');

const app = express();

// Prometheus metrics
const reqCounter = new promClient.Counter({
  name: 'http_server_requests_total',
  help: 'Requests total',
  labelNames: ['endpoint', 'method', 'http_status']
});
const reqLatency = new promClient.Histogram({
  name: 'http_server_request_duration_seconds',
  help: 'Request latency',
  buckets: [0.05, 0.1, 0.2, 0.5, 1, 1.5, 2, 3, 5]
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType);
  res.end(await promClient.register.metrics());
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/orders', async (req, res) => {
  const latency = [0.05, 0.1, 0.2, 0.4, 0.8, 1.2, 2.0][randomInt(0, 6)];
  const end = reqLatency.startTimer();
  await new Promise(r => setTimeout(r, latency * 1000));
  if (Math.random() < 0.08) {
    reqCounter.inc({ endpoint: '/orders', method: 'GET', http_status: '500' });
    end();
    res.status(500).json({ error: 'payment timeout' });
  } else {
    reqCounter.inc({ endpoint: '/orders', method: 'GET', http_status: '200' });
    end();
    res.json({ items: [{ id: 1, amount: 42.0 }], latency });
  }
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Orders service listening on port ${port}`);
});
