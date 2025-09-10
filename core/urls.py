from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'qrcodes', views.QrCodeViewSet)
router.register(r'hydroponics', views.HydroponicViewSet)
router.register(r'sensors', views.SensorViewSet)
router.register(r'sensor-data', views.SensorDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('websocket-test/', views.websocket_test_view, name='websocket_test'),
]
