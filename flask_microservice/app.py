from flask import Flask
import time
import random

# OpenTelemetry
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
# Resource describing the service
resource = Resource(attributes={"service.name": "flask-microservice"})

# ----- Tracing -----
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Replace with actual Jaeger host if not local
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# ----- Metrics -----
reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = metrics.get_meter(__name__)
counter = meter.create_counter("flask_requests_total", unit="requests", description="Total requests")
latency = meter.create_histogram("flask_request_duration_seconds", unit="s", description="Request duration")

# ----- Flask App -----
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    start = time.time()
    with tracer.start_as_current_span("home-endpoint"):
        time.sleep(random.uniform(0.1, 0.5))
        duration = time.time() - start
        counter.add(1, {"endpoint": "/", "method": "GET"})
        latency.record(duration, {"endpoint": "/", "method": "GET"})
        return "Flask microservice reporting to Jaeger + Prometheus"

@app.route("/metrics")
def metrics_view():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(port=5000, debug=True)
