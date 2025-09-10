from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model"""
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, default='')
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Device(models.Model):
    """Device model for IoT devices"""
    DEVICE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]

    device_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    user_email = models.EmailField()
    device_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=DEVICE_STATUS_CHOICES, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_name} - {self.user.email}"


class QrCode(models.Model):
    """QR Code model for device registration"""
    qr_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='qr_codes')
    qr_code_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"QR Code for {self.device.device_name}"


class Hydroponic(models.Model):
    """Hydroponic system model"""
    PLANT_TYPE_CHOICES = [
        ('lettuce', 'Lettuce'),
        ('tomato', 'Tomato'),
        ('herbs', 'Herbs'),
        ('spinach', 'Spinach'),
        ('other', 'Other'),
    ]

    hydroponic_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='hydroponics')
    hydroponic_name = models.CharField(max_length=255)
    plant_type = models.CharField(max_length=50, choices=PLANT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hydroponic_name} - {self.plant_type}"


class Sensor(models.Model):
    """Sensor model for IoT sensors"""
    SENSOR_TYPE_CHOICES = [
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('ph', 'pH Level'),
        ('ec', 'Electrical Conductivity'),
        ('water_level', 'Water Level'),
        ('light', 'Light Intensity'),
    ]

    UNIT_CHOICES = [
        ('celsius', '°C'),
        ('fahrenheit', '°F'),
        ('percent', '%'),
        ('ph_units', 'pH'),
        ('ec_units', 'EC'),
        ('cm', 'cm'),
        ('lux', 'lux'),
        ('ppm', 'ppm'),
        ('mg_l', 'mg/L'),
    ]

    sensor_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensors')
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPE_CHOICES)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sensor_type} sensor - {self.device.device_name}"


class SensorData(models.Model):
    """Sensor data readings model"""
    data_id = models.AutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sensor Data"
        verbose_name_plural = "Sensor Data"

    def __str__(self):
        return f"{self.sensor.sensor_type}: {self.value} {self.sensor.unit} at {self.created_at}"
