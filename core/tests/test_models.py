from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Device, Sensor, SensorData, Hydroponic, QrCode

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'test@example.com')


class DeviceModelTest(TestCase):
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

    def test_device_creation(self):
        self.assertEqual(self.device.device_name, 'Test Device')
        self.assertEqual(self.device.status, 'active')
        self.assertEqual(self.device.user, self.user)

    def test_device_string_representation(self):
        expected = f"Test Device - {self.user.email}"
        self.assertEqual(str(self.device), expected)


class SensorModelTest(TestCase):
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

    def test_sensor_creation(self):
        self.assertEqual(self.sensor.sensor_type, 'temperature')
        self.assertEqual(self.sensor.unit, 'celsius')
        self.assertEqual(self.sensor.device, self.device)

    def test_sensor_string_representation(self):
        expected = f"temperature sensor - {self.device.device_name}"
        self.assertEqual(str(self.sensor), expected)


class SensorDataModelTest(TestCase):
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
        self.sensor_data = SensorData.objects.create(
            sensor=self.sensor,
            value=25.5
        )

    def test_sensor_data_creation(self):
        self.assertEqual(self.sensor_data.value, 25.5)
        self.assertEqual(self.sensor_data.sensor, self.sensor)

    def test_sensor_data_ordering(self):
        # Create another sensor data entry
        newer_data = SensorData.objects.create(
            sensor=self.sensor,
            value=26.0
        )
        
        # Check that newer data comes first (due to Meta ordering)
        latest_data = SensorData.objects.first()
        self.assertEqual(latest_data, newer_data)
