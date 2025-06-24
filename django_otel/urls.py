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
import requests
import random

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from django_otel.metrics import REQUEST_COUNT, REQUEST_LATENCY

def wait(seconds: float = None):
    if not seconds:
        seconds = random.random()
    time.sleep(seconds)

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


def hello_view(request):
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    wait()
    return JsonResponse({"message": "Hello, OpenTelemetry from Django!"})

def test_view(request):
    REQUEST_COUNT.labels(method='GET', endpoint='/test').inc()
    data = {
        "inputCode": "Function to calculate area",
        "language":  "python"
    }
    wait(0.2)
    response = requests.post("https://codeapi.puneetdixit.in/ai-response", json=data, verify=False)
    return JsonResponse({"message": "Hello, OpenTelemetry from Django!2", "response": response.json()})

def test2(request):
    REQUEST_COUNT.labels(method='GET', endpoint='/test-2').inc()
    result = 10/something  # Throwing error
    return JsonResponse({"message": "Hello, OpenTelemetry from Django!"})


urlpatterns = [
    path('', hello_view),
    path('test', test_view),
    path('test2', test2),
    path('metrics/', metrics_view),
    path('admin/', admin.site.urls),
]

