
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');
const { Resource } = require('@opentelemetry/resources');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  resource: new Resource({
    'service.name': process.env.OTEL_SERVICE_NAME || 'orders-service',
    'deployment.environment': process.env.OTEL_RESOURCE_ATTRIBUTES?.split('=')[1] || 'dev'
  })
});

sdk.start();
console.log('OpenTelemetry SDK started');
require('./app');
