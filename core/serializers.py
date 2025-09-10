from rest_framework import serializers
from .models import User, Device, QrCode, Hydroponic, Sensor, SensorData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id', 'user', 'user_email', 'device_name', 'status', 'created_at', 'updated_at']
        read_only_fields = ['device_id', 'created_at', 'updated_at']


class QrCodeSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    
    class Meta:
        model = QrCode
        fields = ['qr_id', 'device', 'device_name', 'qr_code_data', 'method', 'created_at', 'updated_at']
        read_only_fields = ['qr_id', 'created_at', 'updated_at']


class HydroponicSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    
    class Meta:
        model = Hydroponic
        fields = ['hydroponic_id', 'device', 'device_name', 'hydroponic_name', 'plant_type', 
                 'start_date', 'end_date', 'location']


class SensorSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['sensor_id', 'device', 'device_name', 'sensor_type', 'unit', 'created_at', 'updated_at']
        read_only_fields = ['sensor_id', 'created_at', 'updated_at']


class SensorDataSerializer(serializers.ModelSerializer):
    sensor_type = serializers.CharField(source='sensor.sensor_type', read_only=True)
    device_name = serializers.CharField(source='sensor.device.device_name', read_only=True)
    unit = serializers.CharField(source='sensor.unit', read_only=True)
    
    class Meta:
        model = SensorData
        fields = ['data_id', 'sensor', 'sensor_type', 'device_name', 'value', 'unit', 'created_at', 'updated_at']
        read_only_fields = ['data_id', 'created_at', 'updated_at']


class SensorDataCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating sensor data"""
    class Meta:
        model = SensorData
        fields = ['sensor', 'value']
