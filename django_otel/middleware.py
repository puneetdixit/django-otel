import time
from prometheus_client import Counter, Histogram
from django_otel.metrics import REQUEST_COUNT, REQUEST_LATENCY

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.path

        start_time = time.time()
        response = self.get_response(request)
        resp_time = time.time() - start_time

        REQUEST_COUNT.labels(method=method, endpoint=path).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=path).observe(resp_time)

        return response
