"""
Django signals for real-time WebSocket broadcasting
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import SensorData, Device


@receiver(post_save, sender=SensorData)
def broadcast_sensor_data(sender, instance, created, **kwargs):
    """
    Broadcast new sensor data to WebSocket consumers
    """
    if created:  # Only broadcast new data
        channel_layer = get_channel_layer()
        
        # Prepare sensor data for broadcasting
        sensor_data = {
            'id': instance.data_id,
            'sensor_id': instance.sensor.sensor_id,
            'sensor_type': instance.sensor.sensor_type,
            'device_id': instance.sensor.device.device_id,
            'device_name': instance.sensor.device.device_name,
            'value': instance.value,
            'unit': instance.sensor.unit,
            'timestamp': instance.created_at.isoformat(),
        }
        
        # Broadcast to general sensor data group
        async_to_sync(channel_layer.group_send)(
            'sensor_data',
            {
                'type': 'sensor_data_message',
                'sensor_data': sensor_data
            }
        )
        
        # Broadcast to device-specific group
        async_to_sync(channel_layer.group_send)(
            f'device_{instance.sensor.device.device_id}',
            {
                'type': 'sensor_data_message',
                'sensor_data': sensor_data
            }
        )
        
        # Broadcast to sensor-specific group
        async_to_sync(channel_layer.group_send)(
            f'sensor_{instance.sensor.sensor_id}',
            {
                'type': 'sensor_reading_message',
                'sensor_data': {
                    'id': instance.data_id,
                    'value': instance.value,
                    'timestamp': instance.created_at.isoformat(),
                    'sensor_type': instance.sensor.sensor_type,
                    'unit': instance.sensor.unit
                }
            }
        )


@receiver(post_save, sender=Device)
def broadcast_device_status(sender, instance, created, **kwargs):
    """
    Broadcast device status changes to WebSocket consumers
    """
    if not created:  # Only broadcast updates, not new devices
        channel_layer = get_channel_layer()
        
        # Broadcast to device-specific group
        async_to_sync(channel_layer.group_send)(
            f'device_{instance.device_id}',
            {
                'type': 'device_status_message',
                'status': instance.status,
                'device_id': instance.device_id
            }
        )
