from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.consumers import SensorDataConsumer
from core.models import Device, Sensor, SensorData

User = get_user_model()


class WebSocketTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.device = Device.objects.create(
            user=self.user,
            user_email=self.user.email,
            device_name='Test Device',
            status='active'
        )
        self.sensor = Sensor.objects.create(
            device=self.device,
            sensor_type='temperature',
            unit='celsius'
        )

    async def test_sensor_data_consumer_connection(self):
        communicator = WebsocketCommunicator(SensorDataConsumer.as_asgi(), "/ws/sensor-data/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_sensor_data_consumer_receive_message(self):
        communicator = WebsocketCommunicator(SensorDataConsumer.as_asgi(), "/ws/sensor-data/")
        connected, subprotocol = await communicator.connect()
        
        # Test receiving a message
        await communicator.send_json_to({
            'type': 'sensor_data',
            'sensor_id': self.sensor.sensor_id,
            'value': 25.5
        })
        
        response = await communicator.receive_json_from()
        self.assertIn('type', response)
        
        await communicator.disconnect()
