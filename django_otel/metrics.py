from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'app_request_count', 'Total HTTP Requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 'Request latency',
    ['endpoint']
)
