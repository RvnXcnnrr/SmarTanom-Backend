"""
Management command to seed the database with sample data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Device, Sensor, SensorData, Hydroponic, QrCode
from datetime import date, datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create sample users
        users = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                email=f'user{i+1}@smartanom.com',
                defaults={
                    'username': f'user{i+1}',
                    'first_name': f'User{i+1}',
                    'last_name': 'Test'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Create sample devices
        devices = []
        for i, user in enumerate(users):
            device, created = Device.objects.get_or_create(
                device_name=f'Hydroponic System {i+1}',
                user=user,
                defaults={
                    'user_email': user.email,
                    'status': 'active'
                }
            )
            devices.append(device)

        # Create QR codes for devices
        for device in devices:
            QrCode.objects.get_or_create(
                device=device,
                defaults={
                    'qr_code_data': f'DEVICE:{device.device_id}:SMARTANOM'
                }
            )

        # Create hydroponic systems
        plant_types = ['lettuce', 'tomato', 'herbs']
        for i, device in enumerate(devices):
            Hydroponic.objects.get_or_create(
                device=device,
                defaults={
                    'hydroponic_name': f'Hydro Garden {i+1}',
                    'plant_type': plant_types[i % len(plant_types)],
                    'start_date': date.today() - timedelta(days=30),
                    'location': f'Greenhouse Section {i+1}'
                }
            )

        # Create sensors
        sensor_types = [
            ('temperature', 'celsius'),
            ('humidity', 'percent'),
            ('ph', 'ph_units'),
            ('ec', 'ec_units'),
            ('water_level', 'cm')
        ]

        sensors = []
        for device in devices:
            for sensor_type, unit in sensor_types:
                sensor, created = Sensor.objects.get_or_create(
                    device=device,
                    sensor_type=sensor_type,
                    defaults={'unit': unit}
                )
                sensors.append(sensor)

        # Create sample sensor data (last 7 days)
        for sensor in sensors:
            for day in range(7):
                for hour in range(0, 24, 2):  # Every 2 hours
                    timestamp = datetime.now() - timedelta(days=day, hours=hour)
                    
                    # Generate realistic values based on sensor type
                    if sensor.sensor_type == 'temperature':
                        value = random.uniform(20, 30)  # 20-30°C
                    elif sensor.sensor_type == 'humidity':
                        value = random.uniform(60, 80)  # 60-80%
                    elif sensor.sensor_type == 'ph':
                        value = random.uniform(5.5, 7.5)  # pH 5.5-7.5
                    elif sensor.sensor_type == 'ec':
                        value = random.uniform(1.0, 2.5)  # EC 1.0-2.5
                    elif sensor.sensor_type == 'water_level':
                        value = random.uniform(10, 50)  # 10-50 cm
                    else:
                        value = random.uniform(0, 100)

                    SensorData.objects.get_or_create(
                        sensor=sensor,
                        created_at=timestamp,
                        defaults={'value': round(value, 2)}
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(users)} users\n'
                f'- {len(devices)} devices\n'
                f'- {len(sensors)} sensors\n'
                f'- Sample sensor data for the last 7 days'
            )
        )
