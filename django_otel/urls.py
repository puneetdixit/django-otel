"""
URL configuration for django_otel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse
import time

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

REQUEST_COUNT = Counter(
    'app_request_count', 'Total HTTP Requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 'Request latency',
    ['endpoint']
)

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


def hello_view(request):
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    with REQUEST_LATENCY.labels(endpoint='/').time():
        time.sleep(1)
    return JsonResponse({"message": "Hello, OpenTelemetry from Django!"})

def hello_view2(request):
    time.sleep(2)
    return JsonResponse({"message": "Hello, OpenTelemetry from Django!2"})


urlpatterns = [
    path('', hello_view),
    path('test', hello_view2),
    path('metrics/', metrics_view),
    path('admin/', admin.site.urls),
]

