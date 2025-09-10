from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Device, QrCode, Hydroponic, Sensor, SensorData
from .serializers import (
    UserSerializer, DeviceSerializer, QrCodeSerializer, 
    HydroponicSerializer, SensorSerializer, SensorDataSerializer,
    SensorDataCreateSerializer
)


def websocket_test_view(request):
    """Serve the WebSocket test page"""
    return render(request, 'websocket_test.html')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['get'])
    def sensors(self, request, pk=None):
        """Get all sensors for a specific device"""
        device = self.get_object()
        sensors = device.sensors.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def hydroponics(self, request, pk=None):
        """Get all hydroponic systems for a specific device"""
        device = self.get_object()
        hydroponics = device.hydroponics.all()
        serializer = HydroponicSerializer(hydroponics, many=True)
        return Response(serializer.data)


class QrCodeViewSet(viewsets.ModelViewSet):
    queryset = QrCode.objects.all()
    serializer_class = QrCodeSerializer


class HydroponicViewSet(viewsets.ModelViewSet):
    queryset = Hydroponic.objects.all()
    serializer_class = HydroponicSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @action(detail=True, methods=['get'])
    def latest_data(self, request, pk=None):
        """Get the latest sensor reading"""
        sensor = self.get_object()
        latest_reading = sensor.readings.first()
        if latest_reading:
            serializer = SensorDataSerializer(latest_reading)
            return Response(serializer.data)
        return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def data_history(self, request, pk=None):
        """Get sensor data history with optional filtering"""
        sensor = self.get_object()
        readings = sensor.readings.all()
        
        # Optional query parameters for filtering
        limit = request.query_params.get('limit', None)
        if limit:
            readings = readings[:int(limit)]
            
        serializer = SensorDataSerializer(readings, many=True)
        return Response(serializer.data)


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return SensorDataCreateSerializer
        return SensorDataSerializer

    @action(detail=False, methods=['get'])
    def by_sensor_type(self, request):
        """Get sensor data filtered by sensor type"""
        sensor_type = request.query_params.get('type', None)
        if sensor_type:
            data = SensorData.objects.filter(sensor__sensor_type=sensor_type)
            serializer = SensorDataSerializer(data, many=True)
            return Response(serializer.data)
        return Response({'error': 'Please provide sensor type parameter'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_device(self, request):
        """Get sensor data filtered by device"""
        device_id = request.query_params.get('device_id', None)
        if device_id:
            data = SensorData.objects.filter(sensor__device_id=device_id)
            serializer = SensorDataSerializer(data, many=True)
            return Response(serializer.data)
        return Response({'error': 'Please provide device_id parameter'}, 
                       status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def websocket_info(self, request):
        """Get WebSocket connection information"""
        host = request.get_host()
        protocol = 'ws' if not request.is_secure() else 'wss'
        
        return Response({
            'websocket_endpoints': {
                'all_sensor_data': f'{protocol}://{host}/ws/sensor-data/',
                'device_specific': f'{protocol}://{host}/ws/device/<device_id>/',
                'sensor_specific': f'{protocol}://{host}/ws/sensor/<sensor_id>/',
            },
            'message_types': {
                'sensor_data': {
                    'description': 'Send new sensor data',
                    'format': {
                        'type': 'sensor_data',
                        'sensor_id': 'integer',
                        'value': 'float'
                    }
                },
                'ping': {
                    'description': 'Ping the server',
                    'format': {
                        'type': 'ping',
                        'timestamp': 'ISO string'
                    }
                }
            },
            'example_usage': {
                'javascript': '''
const ws = new WebSocket('ws://localhost:8000/ws/sensor-data/');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
ws.send(JSON.stringify({
    type: 'sensor_data',
    sensor_id: 1,
    value: 25.5
}));
                '''
            }
        })
