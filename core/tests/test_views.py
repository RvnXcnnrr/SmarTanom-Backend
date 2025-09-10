from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Device, Sensor, SensorData

User = get_user_model()


class DeviceAPITest(APITestCase):
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

    def test_get_devices_list(self):
        url = reverse('device-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_device_detail(self):
        url = reverse('device-detail', kwargs={'pk': self.device.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['device_name'], 'Test Device')


class SensorAPITest(APITestCase):
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

    def test_get_sensors_list(self):
        url = reverse('sensor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_sensor_detail(self):
        url = reverse('sensor-detail', kwargs={'pk': self.sensor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sensor_type'], 'temperature')


class SensorDataAPITest(APITestCase):
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

    def test_get_sensor_data_list(self):
        url = reverse('sensordata-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_sensor_data_detail(self):
        url = reverse('sensordata-detail', kwargs={'pk': self.sensor_data.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['value']), 25.5)
