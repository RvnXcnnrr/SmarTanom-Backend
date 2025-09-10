"""
WebSocket URL routing for the core app
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensor-data/$', consumers.SensorDataConsumer.as_asgi()),
    re_path(r'ws/device/(?P<device_id>\w+)/$', consumers.DeviceConsumer.as_asgi()),
    re_path(r'ws/sensor/(?P<sensor_id>\w+)/$', consumers.SensorConsumer.as_asgi()),
]
