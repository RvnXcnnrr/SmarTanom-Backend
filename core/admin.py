from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Device, QrCode, Hydroponic, Sensor, SensorData


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'username', 'first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'name', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('name', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'user', 'user_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('device_name', 'user__email', 'user_email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QrCode)
class QrCodeAdmin(admin.ModelAdmin):
    list_display = ('qr_id', 'device', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('device__device_name', 'qr_code_data')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Hydroponic)
class HydroponicAdmin(admin.ModelAdmin):
    list_display = ('hydroponic_name', 'device', 'plant_type', 'start_date', 'end_date', 'location')
    list_filter = ('plant_type', 'start_date')
    search_fields = ('hydroponic_name', 'device__device_name', 'location')
    date_hierarchy = 'start_date'


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'device', 'sensor_type', 'unit', 'created_at')
    list_filter = ('sensor_type', 'unit', 'created_at')
    search_fields = ('device__device_name', 'sensor_type')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'sensor', 'value', 'created_at')
    list_filter = ('sensor__sensor_type', 'created_at')
    search_fields = ('sensor__device__device_name', 'sensor__sensor_type')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
