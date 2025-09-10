"""
WebSocket consumers for real-time data streaming
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Device, Sensor, SensorData


class SensorDataConsumer(AsyncWebsocketConsumer):
    """Consumer for streaming all sensor data"""
    
    async def connect(self):
        # Join sensor data group
        self.group_name = 'sensor_data'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to sensor data stream'
        }))

    async def disconnect(self, close_code):
        # Leave sensor data group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'sensor_data':
                # Handle new sensor data
                await self.handle_sensor_data(text_data_json)
            elif message_type == 'ping':
                # Respond to ping
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': text_data_json.get('timestamp')
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def handle_sensor_data(self, data):
        """Handle incoming sensor data from IoT devices"""
        try:
            sensor_id = data.get('sensor_id')
            value = data.get('value')
            
            if sensor_id and value is not None:
                # Save to database
                sensor_data = await self.save_sensor_data(sensor_id, value)
                
                if sensor_data:
                    # Broadcast to all clients in the group
                    await self.channel_layer.group_send(
                        self.group_name,
                        {
                            'type': 'sensor_data_message',
                            'sensor_data': {
                                'id': sensor_data['id'],
                                'sensor_id': sensor_data['sensor_id'],
                                'sensor_type': sensor_data['sensor_type'],
                                'device_id': sensor_data['device_id'],
                                'device_name': sensor_data['device_name'],
                                'value': sensor_data['value'],
                                'unit': sensor_data['unit'],
                                'timestamp': sensor_data['timestamp'],
                            }
                        }
                    )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error processing sensor data: {str(e)}'
            }))

    async def sensor_data_message(self, event):
        """Send sensor data to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'sensor_data',
            'data': event['sensor_data']
        }))

    @database_sync_to_async
    def save_sensor_data(self, sensor_id, value):
        """Save sensor data to database"""
        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
            sensor_data = SensorData.objects.create(
                sensor=sensor,
                value=float(value)
            )
            return {
                'id': sensor_data.data_id,
                'sensor_id': sensor.sensor_id,
                'sensor_type': sensor.sensor_type,
                'device_id': sensor.device.device_id,
                'device_name': sensor.device.device_name,
                'value': sensor_data.value,
                'unit': sensor.unit,
                'timestamp': sensor_data.created_at.isoformat(),
            }
        except Sensor.DoesNotExist:
            return None
        except Exception:
            return None


class DeviceConsumer(AsyncWebsocketConsumer):
    """Consumer for device-specific data streaming"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_id = None
        self.group_name = None

    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.group_name = f'device_{self.device_id}'
        
        # Check if device exists
        device_exists = await self.check_device_exists(self.device_id)
        if not device_exists:
            await self.close()
            return
        
        # Join device group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send device info
        device_info = await self.get_device_info(self.device_id)
        await self.send(text_data=json.dumps({
            'type': 'device_connected',
            'device': device_info
        }))

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'device_status':
                await self.handle_device_status(text_data_json)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def handle_device_status(self, data):
        """Handle device status updates"""
        status = data.get('status')
        if status:
            await self.update_device_status(self.device_id, status)
            
            # Broadcast status update
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'device_status_message',
                    'status': status,
                    'device_id': self.device_id
                }
            )

    async def device_status_message(self, event):
        """Send device status to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'device_status',
            'device_id': event['device_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def check_device_exists(self, device_id):
        """Check if device exists"""
        return Device.objects.filter(device_id=device_id).exists()

    @database_sync_to_async
    def get_device_info(self, device_id):
        """Get device information"""
        try:
            device = Device.objects.get(device_id=device_id)
            return {
                'device_id': device.device_id,
                'device_name': device.device_name,
                'status': device.status,
                'user_email': device.user_email
            }
        except Device.DoesNotExist:
            return None

    @database_sync_to_async
    def update_device_status(self, device_id, status):
        """Update device status"""
        try:
            device = Device.objects.get(device_id=device_id)
            device.status = status
            device.save()
            return True
        except Device.DoesNotExist:
            return False


class SensorConsumer(AsyncWebsocketConsumer):
    """Consumer for sensor-specific data streaming"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensor_id = None
        self.group_name = None

    async def connect(self):
        self.sensor_id = self.scope['url_route']['kwargs']['sensor_id']
        self.group_name = f'sensor_{self.sensor_id}'
        
        # Check if sensor exists
        sensor_exists = await self.check_sensor_exists(self.sensor_id)
        if not sensor_exists:
            await self.close()
            return
        
        # Join sensor group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send sensor info and latest data
        sensor_info = await self.get_sensor_info(self.sensor_id)
        await self.send(text_data=json.dumps({
            'type': 'sensor_connected',
            'sensor': sensor_info
        }))

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'sensor_reading':
                await self.handle_sensor_reading(text_data_json)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def handle_sensor_reading(self, data):
        """Handle new sensor reading"""
        value = data.get('value')
        if value is not None:
            # Save sensor data
            sensor_data = await self.save_sensor_reading(self.sensor_id, value)
            
            if sensor_data:
                # Broadcast to sensor group
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'sensor_reading_message',
                        'sensor_data': sensor_data
                    }
                )

    async def sensor_reading_message(self, event):
        """Send sensor reading to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'sensor_reading',
            'data': event['sensor_data']
        }))

    @database_sync_to_async
    def check_sensor_exists(self, sensor_id):
        """Check if sensor exists"""
        return Sensor.objects.filter(sensor_id=sensor_id).exists()

    @database_sync_to_async
    def get_sensor_info(self, sensor_id):
        """Get sensor information with latest reading"""
        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
            latest_reading = sensor.readings.first()
            
            sensor_info = {
                'sensor_id': sensor.sensor_id,
                'sensor_type': sensor.sensor_type,
                'unit': sensor.unit,
                'device_id': sensor.device.device_id,
                'device_name': sensor.device.device_name,
                'latest_reading': None
            }
            
            if latest_reading:
                sensor_info['latest_reading'] = {
                    'value': latest_reading.value,
                    'timestamp': latest_reading.created_at.isoformat()
                }
            
            return sensor_info
        except Sensor.DoesNotExist:
            return None

    @database_sync_to_async
    def save_sensor_reading(self, sensor_id, value):
        """Save sensor reading to database"""
        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
            sensor_data = SensorData.objects.create(
                sensor=sensor,
                value=float(value)
            )
            return {
                'id': sensor_data.data_id,
                'value': sensor_data.value,
                'timestamp': sensor_data.created_at.isoformat(),
                'sensor_type': sensor.sensor_type,
                'unit': sensor.unit
            }
        except (Sensor.DoesNotExist, ValueError):
            return None
